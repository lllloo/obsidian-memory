# Subagent：YouTube 影片轉 Obsidian 筆記

> **Python 指令**：以下指令用 `python3`；Windows 環境若 `python3` 無效，改用 `python`。
>
> **路徑契約**：任務 prompt 會傳入 `NOTES_DIR`（絕對路徑到 `<vault>/Inbox/YouTube/<頻道名>/`）。所有讀寫操作一律以 `NOTES_DIR` 為 base，不可用 cwd-relative 路徑，避免從非 repo cwd 呼叫時誤寫到別處。
>
> **NOTES_DIR 自檢**：開工前確認 `NOTES_DIR` 值已被主 skill 展開。若值包含字面 `<`、`>`、或 `$OBSIDIAN_VAULT_ROOT` 字樣（代表占位符未替換 / env var 未展開），視為主 skill 傳錯，**立即回報並停止**，不寫入任何檔案。

## 步驟

對每部影片：

0. **重複偵測（先做）**：在抓取內容前，確認此影片尚未有對應筆記：
   ```bash
   grep -rl "source: https://www.youtube.com/watch?v=<videoId>" "<NOTES_DIR>"
   ```
   若有任何輸出（即已存在對應筆記），**跳過此影片**，回報「⏭ 已有筆記，跳過」。

1. 執行以下指令取得完整 JSON（含 contentMarkdown、published 等欄位）；優先用全域安裝的 defuddle，找不到時 fallback 到 npx：
   ```bash
   defuddle parse <url> --json 2>/dev/null || npx defuddle parse <url> --json
   ```
   **取得 transcript 後必須驗證內容**：確認 contentMarkdown 的主題與影片標題相關。若內容明顯是其他頻道的影片（YouTube 頁面有時會把推薦影片或廣告的 transcript 注入），視為 defuddle 失敗，改走步驟 1b。

1b. **youtube-transcript-api fallback**（defuddle 失敗或 transcript 不符時）：
   ```bash
   pip install youtube-transcript-api -q
   python3 -c "
   from youtube_transcript_api import YouTubeTranscriptApi
   transcript = YouTubeTranscriptApi.get_transcript('<videoId>', languages=['en', 'zh-TW', 'zh'])
   for t in transcript:
       print(f\"**{int(t['start']//60)}:{int(t['start']%60):02d}** {t['text']}\")
   "
   ```
   此方法直接用 video ID 抓字幕，不受頁面推薦影片干擾，是比 curl 更可靠的 fallback。若仍失敗，再走步驟 2。

2. 若以上皆失敗，用 curl 一次取得可用性與上傳日期：
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
   - 若 `STATUS:unavailable` → **跳過，不建立筆記**，回報「⚠ 影片已刪除，跳過」
   - 若 `STATUS:available` → 影片正常，繼續執行；`DATE:` 行的值即為上傳日期
3. 從 JSON 取出 `published` 欄位（ISO 8601 格式），擷取日期部分（YYYY-MM-DD）寫入 frontmatter
4. 若 `published` 欄位不存在或為空（defuddle 常回傳空值，屬正常現象）：用 curl 抓影片頁面取得上傳日期：
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
   若仍為空，`published` 欄位留空
5. 從 JSON 取出 `contentMarkdown` 作為筆記內容來源
6. 依下方「內容品質標準」撰寫筆記

## 筆記規則（必須嚴格遵守）

`$OBSIDIAN_VAULT_ROOT/CLAUDE.md` 的「寫入前 Checklist」是真實來源，本檔只列本 subagent 高頻踩到的點。敏感資料零容忍、tag 沿用既有、白名單制等通則詳見 Checklist 本身。

- **語言**：正文內容一律以**繁體中文**撰寫；技術名詞、品牌名、工具名保留英文（例：Claude Code、OpenAI、defuddle）
- **敏感資料**：defuddle transcript 若含 token / 私鑰 / 個資 → 移除該段或跳過整筆，不寫入
- **`#` 開頭內容**：hex 色碼（`#57F287`）或其他 `#` 開頭字串在 Obsidian 會被當 tag，**必須用反引號包住**（寫成 `` `#57F287` ``）；前端/設計類影片容易踩到
- 檔案路徑：`<NOTES_DIR>/<繁體中文精簡標題>.md`（`NOTES_DIR` 從任務 prompt 取得，為絕對路徑）
- 檔案名稱命名規則：
  - 繁體中文為主，技術名詞與品牌名保留英文
  - 不可含空格；英文/數字與中文之間用 `-` 連接（例：`Claude-Code準確度提升技巧`）；中文詞之間不加符號
  - 只保留核心主題，去掉副標題（`-效果更好還更便宜`、`-非工程師也能懂` 等說明性後綴一律刪除）
  - 去掉日期（`-2026年4月` 等）
  - 不超過 30 字元
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

每個筆記建立後確認檔案存在。全部完成後回報結果清單。
