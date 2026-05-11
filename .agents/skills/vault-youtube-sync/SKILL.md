---
name: vault-youtube-sync
description: 將 YouTube 頻道影片批次轉成 Obsidian 筆記，支援指定頻道 URL（@handle）或一次同步所有既有頻道；每個頻道建立 index + base view 索引，含增量同步（last_sync_id checkpoint）與失敗占位重試（draft 占位）。使用時機：使用者提供 YouTube 頻道 URL（含 @handle）、要求「同步頻道影片」、「整理 YouTube 到 vault」、「抓頻道影片建筆記」、「更新所有頻道」、「yt 全部更新」，或直接呼叫 /vault-youtube-sync。
disable-model-invocation: true
---

# YouTube Channel to Notes

將 YouTube 頻道影片批次轉換成 Obsidian vault 筆記。

> 本 skill 產出進入 `Inbox/YouTube/`，代表「待消化暫存」。使用者讀完會內化成 Cards 並歸檔至 `Topics/<主題>/`，Inbox 原篇刪除。Skill 只負責抓取，不負責消化。

## 資料夾規則

- 筆記存放：`content/Inbox/YouTube/<頻道名>/`（例：`content/Inbox/YouTube/Chase-H-AI/`）
- 此資料夾已在 `quartz.config.ts` 的 `ignorePatterns` 中，**不會發佈到網站**
- 每個頻道資料夾下建立 `01.index.md` 與 `02.影片清單.base` 作為索引（數字前綴確保固定排第一）
- 影片筆記的 frontmatter 需加 `parent: "[[01.index]]"`，讓 Obsidian 圖譜能從影片連回頻道 index（`.base` 檔案不產生圖譜連結，只有 property link 有效）

## 前置作業

```bash
[ -f "content/master-index.md" ] || { echo "ERROR: cwd 不在 repo root"; exit 1; }
```

寫入前依 `content/CLAUDE.md` 的「寫入前 Checklist」自檢。本 skill 高頻踩雷點：defuddle transcript 若含 token / 個資直接跳過該筆；頻道主題 tag 先 grep 既有 vault tags 沿用，避免 `claude-code` vs `claudeCode` drift。

## 步驟 0：判斷執行模式

依使用者輸入決定處理範圍：

- **模式 A — 指定頻道**：使用者給 handle 或頻道 URL（例：`@Chase-H-AI`、`https://www.youtube.com/@Chase-H-AI/videos`）→ 直接以該 handle 執行步驟 1-6
- **模式 B — 同步全部既有頻道**：使用者未指定頻道，或明說「同步全部 / 更新所有頻道 / yt 全部更新」→ 掃 `content/Inbox/YouTube/*/01.index.md`，從每份 frontmatter 的 `source:` 欄位抽出 handle，**依序**逐頻道跑步驟 1-6（頻道之間順序執行避免 YouTube rate limit；單頻道內步驟 5 仍維持 5-6 部一批平行）

模式 B 取得頻道清單（每行一個 `source:` URL）：

```bash
python -c "
import re, glob
for idx in sorted(glob.glob('content/Inbox/YouTube/*/01.index.md')):
    text = open(idx, encoding='utf-8').read()
    m = re.search(r'^source:\s*(https://www\.youtube\.com/@[^/\s]+)', text, re.M)
    if m: print(m.group(1))
"
```

模式 B 規則：

- 只處理已有 `01.index.md` 的頻道；**不會自動加新頻道**。新頻道首次同步仍須 `/vault-youtube-sync @handle` 顯式觸發
- 單頻道任一步驟失敗（fetch_videos error、network 異常等）→ 記錄錯誤、跳下一頻道，不中斷整批
- 全部跑完後在步驟 6 用一張總表呈現各頻道結果

## 步驟 1：抓取影片清單與頻道簡介

用 `scripts/fetch_videos.py` 一次抓取頻道頁面，同時取出影片清單與頻道簡介：

```bash
SCRIPT=$(find .agents/skills/vault-youtube-sync .claude/skills/vault-youtube-sync -name "fetch_videos.py" 2>/dev/null | head -1)
[ -z "$SCRIPT" ] && { echo "ERROR: fetch_videos.py not found"; exit 1; }
PY=$(command -v python3 || command -v python)
$PY "$SCRIPT" <handle>
```

解析輸出：

- `DESC:<text>` → 頻道簡介（Step 3 使用，可能為空）
- `VIDEO:<videoId>|||<title>` → 每行一部影片（頁面上有幾部就幾部）
- `ERROR:<message>` → **模式 A：立即停止**，告知用戶錯誤訊息；**模式 B：記錄錯誤、跳下一頻道**，不中斷整批

組成影片 URL：`https://www.youtube.com/watch?v=<videoId>`

從頻道 URL 取得頻道名稱並正規化：

- 來源：URL 路徑中的 `@handle`（去掉 `@`）
- 正規化規則：空格轉 `-`，移除 `?:;"'!@#$%^&*()+=[]{}|\\/<>` 等特殊字元，保留英數字、中文字、`-`、`_`
- 範例：`Chase H AI` → `Chase-H-AI`、`AI進化論!` → `AI進化論`
- 後續所有步驟的 `<頻道名>` 皆使用正規化後的名稱

## 步驟 2：增量同步檢查 + 內容篩選 + 建立資料夾

先確認是否為更新情境：

```bash
# 讀取上次同步的 checkpoint ID（從 01.index.md frontmatter）
grep "^last_sync_id:" "content/Inbox/YouTube/<頻道名>/01.index.md" 2>/dev/null | sed 's/last_sync_id: //'
```

**Checkpoint 過濾邏輯：**

- 若資料夾**不存在**或 `01.index.md` **無 `last_sync_id`**：全部影片都處理，建立資料夾 `mkdir -p "content/Inbox/YouTube/<頻道名>"`
- 若有 `last_sync_id`：在步驟 1 抓到的清單中找到該 ID 的位置，**只取它上方（更新）的影片**
  - 若 `last_sync_id` 不在清單中（距上次同步太久）：全部都算新的
  - 若 `last_sync_id` 是清單第一筆：無新影片，輸出「已是最新，無需更新」並結束
- 若過濾後**沒有新影片**：輸出「已是最新，無需更新」並結束

**Source URL 去重（checkpoint 之後必做）：**

即使通過 checkpoint 篩選，也必須再排除「已有完整筆記的影片」——防止 checkpoint 失效時（如距上次 sync 超過 30 部）產生重複。**`draft: true` 的筆記不算去重命中**——那是先前 transcript 失敗的占位，本次要交給 subagent 覆寫重抓：

```bash
python3 -c "
import os, re
notes_dir = 'content/Inbox/YouTube/<頻道名>'
if not os.path.isdir(notes_dir):
    raise SystemExit(0)
for f in os.listdir(notes_dir):
    if not f.endswith('.md') or f == '01.index.md':
        continue
    text = open(os.path.join(notes_dir, f), encoding='utf-8').read()
    if re.search(r'^draft:\s*true', text, re.M):
        continue  # draft 占位讓 subagent 重抓覆寫，不去重
    m = re.search(r'^source: https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]+)', text, re.M)
    if m:
        print(m.group(1))
"
```

將輸出的 ID 集合與待處理清單比對，**移除任何 ID 已出現在「非 draft」筆記 source 欄位的影片**，不論檔名是否相同。

> 此方式天然避免重抓曾刪除的影片：刪除的影片比 checkpoint 舊，不會出現在過濾結果中。
> draft 占位則反向被「保留在待處理清單」，subagent 步驟 0 會偵測並覆寫。

### 內容篩選規則（新影片套用）

確認為新影片後，依標題判斷是否值得建立筆記。**以下類型直接跳過**，不建立筆記：

**跳過（無技術價值）：**

- 新聞 / 週報類：標題含「AI News」「News You Can Use」「本週」「This Week」「Weekly」「AI 週報」「重大發佈」等
- 純時事 / 爭議：公司收購、訴訟、爭議事件、產品發布公告（無教學內容）
- 純觀點 / 抱怨：個人感想、預測、使用心得流水帳、無具體技術步驟
- Python 專屬教學：標題明確針對 Python 開發者，且無通用 AI 概念（如「Python for AI」「PydanticAI」「FastAPI」課程）

**保留（有技術價值）：**

- 技術教學、工具使用方法、架構設計概念
- 新工具 / 新 API 介紹（含實際操作示範）
- 軟體工程實踐（TDD、測試、系統設計等）
- 可帶來新觀念或新應用的內容

判斷模糊時，傾向**跳過**而非強行建立低品質筆記。

## 步驟 3：建立 01.index.md

**在啟動文章生成前**，先在頻道資料夾建立 `content/Inbox/YouTube/<頻道名>/01.index.md`（若已存在則跳過）。

頻道簡介已在步驟 1 的 `DESC:` 行取得（可能為空）。寫入 index 前，**將簡介翻譯為繁體中文**（技術名詞/品牌名保留英文）；若為空則省略。

```markdown
---
title: <頻道名>
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
source: <頻道 URL>
last_sync_id: <步驟 1 清單中第一筆的 videoId>
tags:
  - youtube
  - channel
---

<頻道簡介（若有）>

![[02.影片清單.base]]
```

## 步驟 4：建立 02.影片清單.base

**在啟動文章生成前**，先在頻道資料夾建立 `content/Inbox/YouTube/<頻道名>/02.影片清單.base`（若已存在則跳過）：

```yaml
filters:
  and:
    - file.inFolder("Inbox/YouTube/<頻道名>")
    - file.ext == "md"
    - file.name != "01.index"
properties:
  published:
    displayName: 上傳日期
  source:
    displayName: 連結
  file.name:
    displayName: 筆記
views:
  - type: table
    name: 影片清單
    order:
      - file.name
      - published
      - source
    sort:
      - property: published
        direction: DESC
```

## 步驟 5：分批平行處理文章

01.index.md 與 02.影片清單.base 建立完成後，將影片清單分成每批 5-6 部，在**同一個 response** 中用 Agent tool 平行啟動所有 subagents。

每個 subagent 的任務 prompt 格式如下。**下列所有 `<...>` 占位符，主 skill 端必須在送出前全部替換為實際值**（頻道名帶入、日期填上），不要把未替換的 `<…>` 傳給 subagent。subagent cwd 必為 repo root，所有路徑為 repo root 相對：

```
任務：用 defuddle 抓取 YouTube 影片內容，並在 Obsidian vault 建立筆記。
詳細指示請先 Read `.claude/skills/vault-youtube-sync/references/subagent-note-creator.md`。

NOTES_DIR：content/Inbox/YouTube/<頻道名>/    # 例：content/Inbox/YouTube/Chase-H-AI/
今日日期：<YYYY-MM-DD>                        # 例：2026-04-24
語言要求：正文內容一律繁體中文，技術名詞/品牌名保留英文。

**影片清單（處理第 N-M 部）：**
N. <標題> — <URL>
...
```

## 步驟 6：彙整結果 + 更新 Checkpoint

輸出彙整表格（單頻道）：

| #   | 影片標題 | 筆記路徑                           | published  | 狀態                |
| --- | -------- | ---------------------------------- | ---------- | ------------------- |
| 1   | ...      | content/Inbox/YouTube/<頻道名>/... | YYYY-MM-DD | ✓ 完整 / ⚠ 內容不足 |

**模式 B（多頻道）額外彙總表**：所有頻道跑完後，最末再加一張總覽：

| 頻道       | 新增完整     | draft 占位 | 跳過（篩選/已存在/已刪） | 失敗 |
| ---------- | ------------ | ---------- | ------------------------ | ---- |
| Chase-H-AI | 3            | 0          | 2                        | 0    |
| AIJasonZ   | 0 (已是最新) | -          | -                        | -    |
| ...        | ...          | ...        | ...                      | ...  |

**更新 checkpoint**：所有筆記建立完成後，將 `01.index.md` 的 `last_sync_id` 更新為**步驟 1 清單中第一筆**的 video ID（即目前頻道最新的影片）：

```bash
# 用 Python 更新（跨平台，避免 Windows sed -i 不穩定）。
python -c "
import os, re, sys
if not os.path.isfile('content/master-index.md'):
    sys.exit('ERROR: cwd 不在 repo root，中止 checkpoint 更新')
path = 'content/Inbox/YouTube/<頻道名>/01.index.md'
if not os.path.isfile(path):
    sys.exit(f'ERROR: 找不到 index 檔：{path}')
text = open(path, encoding='utf-8').read()
text = re.sub(r'^last_sync_id: .*', 'last_sync_id: <NEW_ID>', text, flags=re.MULTILINE)
text = re.sub(r'^updated: .*', 'updated: <TODAY>', text, flags=re.MULTILINE)
open(path, 'w', encoding='utf-8').write(text)
"
```

> 若本次無新影片（早已是最新），不需更新 checkpoint。

## 注意事項

- **defuddle 內容不足**：contentMarkdown 無時間戳格式（`**0:00**`）時走 subagent-note-creator.md 的情況 B，只寫重點摘要，不推測補充
- **tags**：一律加 `youtube`，可依頻道主題加額外標籤（如 `claude-code`）
- **檔名長度**：超過 40 字元的標題適當縮短，保留關鍵詞
- **增量同步**：再次執行同一頻道時，Step 2 會用 checkpoint 過濾，只建立新影片的筆記；ytInitialData 一次最多回傳約 30 部，足以涵蓋一般更新週期
- **往前追溯限制**：ytInitialData 最多回傳約 30 部。若距上次同步超過 30 部新影片，checkpoint 不會出現在清單中，全部都會視為新的。更早的影片需改走 YouTube continuation token API（非本 skill 範圍）
- **失敗占位機制（draft 重試）**：subagent 任何一支影片抓不到 transcript（defuddle videoId mismatch / youtube-transcript-api 無字幕 / 429 rate limit）但 curl 確認影片可用時，寫一份 `draft: true` 占位筆記（範本見 `references/subagent-note-creator.md` 步驟 2b）。Step 2 的 Source URL 去重會跳過 draft 占位讓它留在待處理清單，subagent Step 0 偵測到 draft 後刪除並覆寫重抓——下次執行 skill 自動補完。**沒有這層占位，失敗影片會永遠落在 last_sync_id 上方被頻道 checkpoint 排除，再也不會補上。**
- **影片已刪除（不可補）**：subagent curl 拿到 `videoUnavailableRenderer` → 直接跳過，不寫筆記、不寫占位。比 last_sync_id 還新但已刪的影片下次仍會出現在清單，但 source URL 去重不會擋（因為從未寫過）→ subagent 再 curl 一次確認 unavailable → 再次跳過，等於每次重跑都會再驗一次（成本可接受）
- **published 欄位不穩定**：defuddle 解析 YouTube 頁面時 `published` 欄位常為空，屬正常現象。無論 defuddle 是否成功，只要 `published` 為空都需用 curl 抓 `itemprop="datePublished"` meta tag 補全；若仍為空才留空
- **Windows Python subprocess 編碼**：若在 skill 外用 Python `subprocess` 抓 YouTube 頁面，必須用 bytes 模式（不加 `text=True`）再手動 `.decode('utf-8', errors='replace')`，否則 Windows 預設 cp950 會解碼失敗
- **重複筆記**：Step 2 的 Source URL 去重（過濾 draft 後）是主要防線，以 video ID 為準不依賴檔名；subagent Step 0 寫檔前再 grep 一次確認。兩道防線確保同一支影片不會產生兩份完整筆記
- **不發佈**：`content/Inbox/YouTube/` 已在 ignorePatterns，正常筆記無需加 `draft: true`；`draft: true` 在此 skill 中專用於「失敗占位等待重試」語意
