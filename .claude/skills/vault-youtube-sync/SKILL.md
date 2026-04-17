---
name: vault-youtube-sync
description: 當使用者提供 YouTube **頻道** URL（含 @handle 的網址，如 youtube.com/@XXX 或 youtube.com/@XXX/videos）並想建立、同步或整理 Obsidian 筆記時，一定要用此 skill。觸發情境：「頻道影片建成筆記」、「youtube 轉筆記」、「yt 轉 ob」、「整理到 vault」、「存成 Obsidian 筆記」、「同步這個頻道」、「看有沒有新影片沒存到的」、「抓頻道影片」。不應觸發：單部影片 URL（watch?v=XXX）、使用者明確說「不用建筆記」或只是查詢既有筆記。
---

# YouTube Channel to Notes

將 YouTube 頻道影片批次轉換成 Obsidian vault 筆記。

## 資料夾規則

- 筆記存放：`content/YouTube/<頻道名>/`（例：`content/YouTube/Chase-H-AI/`）
- 此資料夾已在 `quartz.config.ts` 的 `ignorePatterns` 中，**不會發佈到網站**
- 每個頻道資料夾下建立 `01.index.md` 與 `02.影片清單.base` 作為索引（數字前綴確保固定排第一）
- 影片筆記的 frontmatter 需加 `parent: "[[01.index]]"`，讓 Obsidian 圖譜能從影片連回頻道 index（`.base` 檔案不產生圖譜連結，只有 property link 有效）

## 步驟 1：抓取影片清單與頻道簡介

用 `scripts/fetch_videos.py` 一次抓取頻道頁面，同時取出影片清單與頻道簡介：

```bash
python3 .claude/skills/vault-youtube-sync/scripts/fetch_videos.py <handle> 2>/dev/null || \
python  .claude/skills/vault-youtube-sync/scripts/fetch_videos.py <handle>
```

解析輸出：
- `DESC:<text>` → 頻道簡介（Step 3 使用，可能為空）
- `VIDEO:<videoId>|||<title>` → 每行一部影片（頁面上有幾部就幾部）
- `ERROR:<message>` → **立即停止**，告知用戶錯誤訊息

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
grep "^last_sync_id:" content/YouTube/<頻道名>/01.index.md 2>/dev/null | sed 's/last_sync_id: //'
```

**Checkpoint 過濾邏輯：**
- 若資料夾**不存在**或 `01.index.md` **無 `last_sync_id`**：全部影片都處理，建立資料夾 `mkdir -p content/YouTube/<頻道名>`
- 若有 `last_sync_id`：在步驟 1 抓到的清單中找到該 ID 的位置，**只取它上方（更新）的影片**
  - 若 `last_sync_id` 不在清單中（距上次同步太久）：全部都算新的
  - 若 `last_sync_id` 是清單第一筆：無新影片，輸出「已是最新，無需更新」並結束
- 若過濾後**沒有新影片**：輸出「已是最新，無需更新」並結束

**Source URL 去重（checkpoint 之後必做）：**

即使通過 checkpoint 篩選，也必須再排除「已有筆記的影片」——防止 checkpoint 失效時（如距上次 sync 超過 30 部）產生重複：

```bash
# 取出資料夾內所有筆記已記錄的 video ID
grep -rh "^source: https://www.youtube.com/watch" content/YouTube/<頻道名>/ 2>/dev/null \
  | grep -oP "(?<=v=)[A-Za-z0-9_-]+"
```

將輸出的 ID 集合與待處理清單比對，**移除任何 ID 已出現在現有筆記 source 欄位的影片**，不論檔名是否相同。

> 此方式天然避免重抓曾刪除的影片：刪除的影片比 checkpoint 舊，不會出現在過濾結果中。

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

**在啟動文章生成前**，先在頻道資料夾建立 `01.index.md`（若已存在則跳過）。

頻道簡介已在步驟 1 的 `DESC:` 行取得（可能為空）。寫入 index 前，**將簡介翻譯為繁體中文**（技術名詞/品牌名保留英文）；若為空則省略。

```markdown
---
title: <頻道名>
tags:
  - youtube
  - channel
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
source: <頻道 URL>
last_sync_id: <步驟 1 清單中第一筆的 videoId>
---

<頻道簡介（若有）>

![[02.影片清單.base]]
```

## 步驟 4：建立 02.影片清單.base

**在啟動文章生成前**，先在頻道資料夾建立 `02.影片清單.base`（若已存在則跳過）：

```yaml
filters:
  and:
    - file.inFolder("YouTube/<頻道名>")
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

每個 subagent 的任務 prompt 格式：

```
任務：用 defuddle 抓取 YouTube 影片內容，並在 Obsidian vault 建立筆記。
詳細指示請先 Read `.claude/skills/vault-youtube-sync/references/subagent-note-creator.md`。

筆記存放位置：content/YouTube/<頻道名>/
今日日期：<YYYY-MM-DD>
語言要求：正文內容一律繁體中文，技術名詞/品牌名保留英文。

**影片清單（處理第 N-M 部）：**
N. <標題> — <URL>
...
```

## 步驟 6：彙整結果 + 更新 Checkpoint

輸出彙整表格：

| # | 影片標題 | 筆記路徑 | published | 狀態 |
|---|---------|---------|-----------|------|
| 1 | ... | content/YouTube/<頻道名>/... | YYYY-MM-DD | ✓ 完整 / ⚠ 內容不足 |

**更新 checkpoint**：所有筆記建立完成後，將 `01.index.md` 的 `last_sync_id` 更新為**步驟 1 清單中第一筆**的 video ID（即目前頻道最新的影片）：

```bash
# 用 Python 更新（跨平台，避免 Windows sed -i 不穩定）
python -c "
import re
path = 'content/YouTube/<頻道名>/01.index.md'
text = open(path, encoding='utf-8').read()
text = re.sub(r'^last_sync_id: .*', 'last_sync_id: <NEW_ID>', text, flags=re.MULTILINE)
text = re.sub(r'^updated: .*', 'updated: <TODAY>', text, flags=re.MULTILINE)
open(path, 'w', encoding='utf-8').write(text)
"
```

> 若本次無新影片（早已是最新），不需更新 checkpoint。

**更新 `master-index.md`**：同步更新 `content/master-index.md` 中的 YouTube 篇數（`YouTube/ — N 篇影片摘要`）；若為新頻道，加入頻道清單與描述。

## 注意事項

- **defuddle 內容不足**：contentMarkdown 無時間戳格式（`**0:00**`）時走 subagent-note-creator.md 的情況 B，只寫重點摘要，不推測補充
- **tags**：一律加 `youtube`，可依頻道主題加額外標籤（如 `claude-code`）
- **檔名長度**：超過 40 字元的標題適當縮短，保留關鍵詞
- **增量同步**：再次執行同一頻道時，Step 2 會用 checkpoint 過濾，只建立新影片的筆記；ytInitialData 一次最多回傳約 30 部，足以涵蓋一般更新週期
- **往前追溯限制**：ytInitialData 最多回傳約 30 部。若距上次同步超過 30 部新影片，checkpoint 不會出現在清單中，全部都會視為新的。更早的影片需改走 YouTube continuation token API（非本 skill 範圍）
- **YouTube 429 rate limit**：大量平行抓取多頻道時容易觸發。受影響的影片先建立為 `draft: true` 筆記保留位置，等數小時後 rate limit 解除再補完內容
- **published 欄位不穩定**：defuddle 解析 YouTube 頁面時 `published` 欄位常為空，屬正常現象。無論 defuddle 是否成功，只要 `published` 為空都需用 curl 抓 `itemprop="datePublished"` meta tag 補全；若仍為空才留空
- **Windows Python subprocess 編碼**：若在 skill 外用 Python `subprocess` 抓 YouTube 頁面，必須用 bytes 模式（不加 `text=True`）再手動 `.decode('utf-8', errors='replace')`，否則 Windows 預設 cp950 會解碼失敗
- **重複筆記**：Step 2 的 Source URL 去重是主要防線（以 video ID 為準，不依賴檔名）；subagent 寫檔前也會再做一次 grep 確認。兩道防線確保同一支影片不會產生兩份筆記
- **影片已刪除**：defuddle 失敗時，subagent 依 subagent-note-creator.md 的流程確認後跳過
- **不發佈**：`content/YouTube/` 已在 ignorePatterns，無需加 `draft: true`
