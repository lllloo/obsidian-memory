# Subagent：YouTube 影片轉 Obsidian 筆記

## 步驟

對每部影片：

1. 執行 `npx defuddle parse <url> --json` 取得完整 JSON（含 contentMarkdown、published 等欄位）
2. 若 defuddle 失敗（exit code 非 0 或輸出為空），用 Chrome 導航到影片頁面，執行以下 JS 確認影片是否可用，**同時順便取得 `datePublished`**：
   ```javascript
   const item = window.ytInitialData.contents.twoColumnWatchNextResults.results.results.contents[0].itemSectionRenderer && window.ytInitialData.contents.twoColumnWatchNextResults.results.results.contents[0].itemSectionRenderer.contents[0].backgroundPromoRenderer;
   const dateEl = document.querySelector('meta[itemprop="datePublished"]');
   const date = dateEl ? dateEl.content : '';
   document.title = item ? (item.title.runs[0].text) : ('available|||' + date);
   ```
   - 若 title 包含「這部影片已無法播放」→ **跳過，不建立筆記**，回報「⚠ 影片已刪除，跳過」
   - 若 title 以 `available|||` 開頭 → 影片正常，`|||` 後的值即為 `datePublished`（可能為空）；存入變數供步驟 4 使用
3. 從 JSON 取出 `published` 欄位（ISO 8601 格式），擷取日期部分（YYYY-MM-DD）寫入 frontmatter
4. 若 `published` 欄位不存在或為空：
   - 若步驟 2 已取得 `datePublished`（非空）→ 直接使用，**不再導航**
   - 否則 → 用 Chrome 導航到影片頁面，以 `document.querySelector('meta[itemprop="datePublished"]').content` 取得上傳日期
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

**情況 A — defuddle 抓到完整 transcript（contentMarkdown 超過 500 字）：**
- defuddle 的輸出格式為 `**0:00** · 逐字稿文字`，以此為內容來源；筆記中不得出現時間戳，也不可依時間順序直接排列逐字稿段落——必須依主題重新組織
- 依影片的自然章節，用 `##` heading 分段（例：`## 核心架構`、`## 設定步驟`、`## 實際案例`）
- 每段用條列或短段落說明該章節的重點，包含具體細節（指令、設定路徑、數值等）
- 可用 code block 呈現指令或結構
- 目標：讀者不看影片也能完全理解並執行

**情況 B — defuddle 只抓到 description 或極少內容（不足 500 字）：**
- 寫一個 `## 重點摘要` 段落，條列實際取得的資訊
- **禁止推測或補充** defuddle 沒有的內容

每個筆記建立後確認檔案存在。全部完成後回報結果清單。
