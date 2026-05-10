# Subagent：YouTube 影片轉 Obsidian 筆記

> **Python 指令**：以下指令用 `python3`；Windows 環境若 `python3` 無效，改用 `python`。
>
> **路徑契約**：任務 prompt 會傳入 `NOTES_DIR`（repo root 相對路徑：`content/Inbox/YouTube/<頻道名>/`）。所有讀寫操作以 `NOTES_DIR` 為 base，cwd 必為 repo root（subagent 預設繼承父 agent cwd）。
>
> **NOTES_DIR 自檢**：開工前確認 `NOTES_DIR` 值已被主 skill 展開。若值包含字面 `<`、`>` 或仍是占位符（代表主 skill 未替換），視為傳錯，**立即回報並停止**，不寫入任何檔案。同時確認 cwd 為 repo root（`test -f content/master-index.md`）。

## 步驟

對每部影片依序執行步驟 0 → 1 →（必要時 1b → 2 → 2b）→ 3 → 4 → 5 → 6。任一步驟若決議「跳過此影片」即直接結束，進入下一部。流程刻意拆成多個 H3 子標題（不用 `1.`/`1b.` 編號清單），避免 markdown formatter 破壞層次。

### 步驟 0：重複偵測（先做）

在抓取內容前確認此影片尚未有「已完成」對應筆記：

```bash
existing=$(grep -rl "source: https://www.youtube.com/watch?v=<videoId>" "<NOTES_DIR>" 2>/dev/null)
```

- 無輸出 → 繼續步驟 1
- 有輸出且該檔含 `^draft: true` → 此為先前失敗的 draft 占位，**先 `rm "$existing"`** 再繼續步驟 1（重抓覆蓋）
- 有輸出且該檔無 `^draft: true` → 已是完整筆記，**跳過此影片**，回報「⏭ 已有筆記，跳過」

### 步驟 1：defuddle 抓 transcript + videoId 硬驗證

執行以下指令取得完整 JSON（含 contentMarkdown、published 等欄位）；優先用全域安裝的 defuddle，找不到時 fallback 到 npx：

```bash
defuddle parse <url> --json 2>/dev/null || npx defuddle parse <url> --json
```

**取得 JSON 後必須做 videoId 硬驗證**（不可省略）：defuddle 對 YouTube URL 經常把推薦影片 transcript 注入，靠「主題對不對」目測極不可靠；先前用「target ID 是否在所有提及 ID 中」也太鬆——target 自家的 embed/canonical 幾乎一定在，等於檢測不到污染。改用以下兩階段硬規則：

```bash
echo "$JSON" | python3 -c "
import sys, json, re
data = json.load(sys.stdin)
target = '<videoId>'
ID_RE = r'(?:watch\?v=|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})'

# 階段 1：檢查 defuddle 帶的主來源欄位（若有）— 最硬
for k in ('url', 'source', 'canonical'):
    v = data.get(k) or ''
    m = re.search(ID_RE, v)
    if m:
        print('MATCH' if m.group(1) == target else f'MISMATCH:{k}={m.group(1)}')
        sys.exit(0)

# 階段 2：fallback — contentMarkdown 前 2000 字第一個 ID（推薦影片通常出現在尾段）
blob = (data.get('contentMarkdown') or '')[:2000]
ids = re.findall(ID_RE, blob)
if not ids:
    print('UNKNOWN')           # 抓不到 ID 證據，視同失敗走 1b
elif ids[0] == target:
    print('MATCH')
else:
    print(f'MISMATCH:first={ids[0]}')
"
```

- `MATCH` → 進入步驟 3
- `MISMATCH` 或 `UNKNOWN` → defuddle 內容不可信，**直接走步驟 1b**，不要嘗試從污染／不確定的 contentMarkdown 撈內容

### 步驟 1b：youtube-transcript-api fallback

當步驟 1 回 MISMATCH/UNKNOWN 或抓不到 transcript 時：

```bash
pip install youtube-transcript-api -q
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
# 新版 instance API（v0.6+）；舊版 get_transcript 已移除
transcript = YouTubeTranscriptApi().fetch('<videoId>', languages=['zh-Hant','zh-TW','zh','en'])
for t in transcript:
    print(f\"**{int(t.start//60)}:{int(t.start%60):02d}** {t.text}\")
"
```

此方法直接用 video ID 抓字幕，不受頁面推薦影片干擾，是比 curl 更可靠的 fallback。成功 → 進入步驟 3 並把輸出視為 transcript；若仍失敗，再走步驟 2。

### 步驟 2：curl 確認影片狀態 + 抓上傳日期

若步驟 1 / 1b 都失敗，用 curl 一次取得可用性與上傳日期：

```bash
curl -s "https://www.youtube.com/watch?v=<videoId>" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Accept-Language: en-US,en;q=0.9" \
  | python3 -c "
import sys, re
html = sys.stdin.read()
avail = 'unavailable' if 'videoUnavailableRenderer' in html else 'available'
m = re.search(r'itemprop=\"datePublished\" content=\"([^\"]+)\"', html)
date = m.group(1)[:10] if m else ''
print('STATUS:' + avail)
print('DATE:' + date)
"
```

- 若 `STATUS:unavailable` → **跳過，不建立筆記、不寫占位**，回報「⚠ 影片已刪除，跳過」
- 若 `STATUS:available` 但 transcript 仍無 → **走步驟 2b 寫 draft 占位**（保留位置等待下次重試），不要靜默丟棄

### 步驟 2b：失敗占位（draft 重試）

寫一份 `draft: true` 的占位筆記，下次執行 skill 時步驟 0 會偵測 draft 並覆蓋重抓。為何要占位而不直接跳過：SKILL.md 步驟 2 的 Source URL 去重以 video ID 為鍵；若不留任何痕跡，下次依然會被頻道 checkpoint 排除（位置已在 `last_sync_id` 上方），等於這支影片**永遠不會補上**。

檔案路徑與命名規則同正常筆記（依下方「筆記規則」），frontmatter 範本：

```
---
title: <影片原標題的繁體中文翻譯>
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
source: https://www.youtube.com/watch?v=<videoId>
published: <步驟 2 curl 抓到的日期；無則省略此欄>
parent: "[[01.index]]"
draft: true
tags:
  - youtube
---

> [!warning] Transcript 抓取失敗，等待下次重試
> defuddle / youtube-transcript-api / curl 三層 fallback 皆未取得內容。
> 失敗原因：<簡述，例：defuddle videoId mismatch、transcript-api NoTranscriptFound、429 rate limit>
> 下次執行 vault-youtube-sync 會自動偵測此 draft 並覆寫重抓。
```

寫完回報「📝 transcript 失敗，已建 draft 占位」並結束此影片流程（**不要**進入步驟 3-6）。

### 步驟 3：取 published 日期

從步驟 1 的 JSON 取出 `published` 欄位（ISO 8601 格式），擷取日期部分（YYYY-MM-DD）寫入 frontmatter。

### 步驟 4：補抓上傳日期（若 published 為空）

若 `published` 欄位不存在或為空（defuddle 常回傳空值，屬正常現象）：用 curl 抓影片頁面取得上傳日期：

```bash
curl -s "https://www.youtube.com/watch?v=<videoId>" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Accept-Language: en-US,en;q=0.9" \
  | python3 -c "
import sys, re
m = re.search(r'itemprop=\"datePublished\" content=\"([^\"]+)\"', sys.stdin.read())
print(m.group(1)[:10] if m else '')
"
```

若仍為空，`published` 欄位留空。

### 步驟 5：取 contentMarkdown 作為內容來源

從 JSON 取出 `contentMarkdown` 作為筆記內容來源；若走步驟 1b 取得 transcript，則以 1b 的時間戳輸出為來源。

### 步驟 6：撰寫筆記

依下方「內容品質標準」撰寫筆記。建立後確認檔案存在；全部完成後回報結果清單。

## 筆記規則（必須嚴格遵守）

`content/CLAUDE.md` 的「寫入前 Checklist」是真實來源，本檔只列本 subagent 高頻踩到的點。敏感資料零容忍、tag 沿用既有、白名單制等通則詳見 Checklist 本身。

- **語言**：正文內容一律以**繁體中文**撰寫；技術名詞、品牌名、工具名保留英文（例：Claude Code、OpenAI、defuddle）
- **敏感資料**：defuddle transcript 若含 token / 私鑰 / 個資 → 移除該段或跳過整筆，不寫入
- **`#` 開頭內容**：hex 色碼（`#57F287`）或其他 `#` 開頭字串在 Obsidian 會被當 tag，**必須用反引號包住**（寫成 `` `#57F287` ``）；前端/設計類影片容易踩到
- **不主動加 wikilink**：Inbox/ 是「消化完刪除」的暫存，筆記彼此 `[[wikilink]]` 沒意義（會一起被刪）。即使偵測到主題重疊，也**不要**掃 `<NOTES_DIR>` 找兄弟筆記補連結——wikilink 真正長出來的時機是使用者把 Cards/ 歸檔到 Topics/，由人決定，不是 AI。例外：`parent: "[[01.index]]"` 是 schema 必填，照寫
- 檔案路徑：`<NOTES_DIR>/<繁體中文精簡標題>.md`（`NOTES_DIR` 從任務 prompt 取得，為 repo root 相對路徑）
- 檔案名稱命名規則：
  - 繁體中文為主，技術名詞與品牌名保留英文
  - 不可含空格；英文/數字與中文之間用 `-` 連接（例：`Claude-Code準確度提升技巧`）；中文詞之間不加符號
  - 只保留核心主題，去掉副標題（`-效果更好還更便宜`、`-非工程師也能懂` 等說明性後綴一律刪除）
  - 去掉日期（`-2026年4月` 等）
  - 不超過 40 字元
  - 不可含 `?:;"'` 等特殊字元
- frontmatter 格式（欄位順序須與 `scripts/vault-schema.mjs` 的 `FIELD_ORDER` 一致）：
  ```
  ---
  title: <影片標題的繁體中文翻譯>（技術名詞與品牌名保留英文）
  created: <今日 YYYY-MM-DD>
  updated: <今日 YYYY-MM-DD>
  source: <youtube url>
  published: <影片上傳日期 YYYY-MM-DD>
  parent: "[[01.index]]"
  tags:
    - youtube
  ---
  ```
- 不使用 `#` 標題 heading（Quartz 從 frontmatter 自動產生）

## 內容品質標準

判斷依據：contentMarkdown 是否含有時間戳格式（`**0:00**`，正規表達式：`\*\*\d+:\d+\*\*`）。

**情況 A — 有時間戳（真實 transcript）：**

- 以時間戳行為內容來源；筆記中不得出現時間戳，也不可依時間順序直接排列——必須依主題重新組織
- 依影片的自然章節，用 `##` heading 分段（例：`## 核心架構`、`## 設定步驟`、`## 實際案例`）
- 每段用條列或短段落說明重點，包含具體細節（指令、設定路徑、數值等）
- 可用 code block 呈現指令或結構
- 篇幅依實際內容而定，不強制展開，也不補充推測

**情況 B — 無時間戳（description 或無字幕）：**

- 寫一個 `## 重點摘要` 段落，條列實際取得的資訊
- **禁止推測或補充** defuddle 沒有的內容
