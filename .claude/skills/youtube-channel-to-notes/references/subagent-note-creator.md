# Subagent：YouTube 影片轉 Obsidian 筆記

## 步驟

對每部影片：

1. 執行以下指令取得完整 JSON（含 contentMarkdown、published 等欄位）；優先用全域安裝的 defuddle，找不到時 fallback 到 npx：
   ```bash
   defuddle parse <url> --json 2>/dev/null || npx defuddle parse <url> --json
   ```
2. 若 defuddle 失敗（exit code 非 0 或輸出為空），用 curl 一次取得可用性與上傳日期：
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
4. 若 `published` 欄位不存在或為空：使用步驟 2 的 `DATE:` 值；若仍為空則 `published` 欄位留空
5. 從 JSON 取出 `contentMarkdown` 作為筆記內容來源
6. 依下方「內容品質標準」撰寫筆記

## 筆記規則（必須嚴格遵守）

- 檔案路徑：`content/YouTube/<頻道名>/<繁體中文精簡標題>.md`
- 檔案名稱命名規則：
  - 繁體中文為主，技術名詞與品牌名保留英文
  - 不可含空格；英文/數字與中文之間用 `-` 連接（例：`Claude-Code準確度提升技巧`）；中文詞之間不加符號
  - 只保留核心主題，去掉副標題（`-效果更好還更便宜`、`-非工程師也能懂` 等說明性後綴一律刪除）
  - 去掉日期（`-2026年4月` 等）
  - 不超過 30 字元
  - 不可含 `?:;"'` 等特殊字元
- frontmatter 格式：
  ```
  ---
  title: <影片標題的繁體中文翻譯>（技術名詞與品牌名保留英文）
  tags:
    - youtube
  created: <今日 YYYY-MM-DD>
  updated: <今日 YYYY-MM-DD>
  published: <影片上傳日期 YYYY-MM-DD>
  source: <youtube url>
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
