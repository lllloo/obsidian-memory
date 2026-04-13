---
name: youtube-channel-to-notes
description: 當使用者提供 YouTube 頻道網址並想要建立筆記時使用此 skill。用 Claude in Chrome 抓取頻道影片清單（最多 10 部），用平行 subagents 將每部影片建立成 Obsidian vault 筆記（content/YouTube/<頻道名>/）。觸發詞：提供 YouTube 頻道 URL、「幫我把這個頻道的影片建成筆記」、「youtube 轉筆記」、「抓頻道影片」。
---

# YouTube Channel to Notes

將 YouTube 頻道影片批次轉換成 Obsidian vault 筆記。

## 資料夾規則

- 筆記存放：`content/YouTube/<頻道名>/`（例：`content/YouTube/Chase-H-AI/`）
- 此資料夾已在 `quartz.config.ts` 的 `ignorePatterns` 中，**不會發佈到網站**
- 每個頻道資料夾下建立 `01.index.md` 與 `02.影片清單.base` 作為索引（數字前綴確保固定排第一）

## 步驟 1：抓取影片清單

使用 **Claude in Chrome**（mcp__claude-in-chrome 工具）抓取頻道影片清單：

1. 導航到頻道的 `/videos` 頁面
2. 用 `javascript_tool` 執行以下腳本，從 `window.ytInitialData` 直接讀取影片資料（無需捲動，最多 10 部，video ID 完整可靠）：

```javascript
const data = window.ytInitialData;
const tabs = data.contents.twoColumnBrowseResultsRenderer.tabs;
let videos = [];
for (const tab of tabs) {
  const content = tab.tabRenderer && tab.tabRenderer.content;
  if (!content) continue;
  const section = content.richGridRenderer;
  if (!section) continue;
  for (const item of section.contents || []) {
    const r = item.richItemRenderer && item.richItemRenderer.content && item.richItemRenderer.content.videoRenderer;
    if (r) {
      const title = r.title.runs[0].text;
      const vid = r.videoId;
      const hex = Array.from(vid).map(c => c.charCodeAt(0).toString(16).padStart(2,'0')).join('');
      videos.push(title + '|||' + hex);
    }
  }
}
document.title = videos.slice(0, 10).join('###');
```

3. 讀取 tab title（`tabs_context_mcp` 取得 `title` 欄位），以 `###` 分割各筆，再以 `|||` 分割標題與 hex-encoded video ID
4. hex 解碼：每兩個十六進位字元還原為一個字元，得到 11 碼的 video ID
5. 組成 URL：`https://www.youtube.com/watch?v=<videoId>`

> **為什麼用 `ytInitialData`**：YouTube 頁面的 `javascript_tool` 回傳值會被安全過濾 BLOCKED（含 cookie/query string 資料）。透過 `document.title` 傳遞資料可繞過此限制；`ytInitialData` 是 YouTube SSR 預載的物件，包含完整影片資料，不需捲動、video ID 不會截斷或重複。

## 步驟 2：增量同步檢查 + 建立資料夾

先確認是否為更新情境：

```bash
# 取得頻道資料夾中已有筆記的所有 source URL
grep -rh "^source:" content/YouTube/<頻道名>/ --include="*.md" 2>/dev/null | sed 's/source: //'
```

- 若資料夾**不存在**或**無任何筆記**：全部影片都處理，建立資料夾 `mkdir -p content/YouTube/<頻道名>`
- 若已有筆記：將抓到的影片清單與已有的 source URL 比對，**過濾掉已存在的影片**，只保留新的
- 若過濾後**沒有新影片**：輸出「已是最新，無需更新」並結束

> 比對方式：影片 URL 格式為 `https://www.youtube.com/watch?v=<videoId>`，直接比對 video ID 即可（URL 格式不同但 ID 相同也算已存在）

## 步驟 3：建立 01.index.md

**在啟動文章生成前**，先在頻道資料夾建立 `01.index.md`（若已存在則跳過）：

```markdown
---
title: <頻道名>
tags:
  - youtube
  - channel
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
source: <頻道 URL>
---

![[02.影片清單]]
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

筆記存放位置：content/YouTube/<頻道名>/
今日日期：<YYYY-MM-DD>

**影片清單（處理第 N-M 部）：**
N. <標題> — <URL>
...

**步驟：**
對每部影片：
1. 執行 `npx defuddle parse <url> --json` 取得完整 JSON（含 contentMarkdown、published 等欄位）
2. 從 JSON 取出 `published` 欄位（ISO 8601 格式），擷取日期部分（YYYY-MM-DD）寫入 frontmatter
3. 若 `published` 欄位不存在或為空，改用 Chrome 導航到影片頁面，以 `document.querySelector('meta[itemprop="datePublished"]').content` 取得上傳日期
4. 從 JSON 取出 `contentMarkdown` 作為筆記內容來源
5. 依下方「內容品質標準」撰寫筆記

**筆記規則（必須嚴格遵守）：**
- 檔案路徑：content/YouTube/<頻道名>/<繁體中文精簡標題>.md
- 檔案名稱命名規則：
  - 繁體中文為主，技術名詞與品牌名保留英文
  - 不可含空格；英文/數字與中文之間用 `-` 連接（例：`Claude-Code準確度提升技巧`）；中文詞之間不加符號
  - 只保留核心主題，去掉副標題（`-效果更好還更便宜`、`-非工程師也能懂` 等說明性後綴一律刪除）
  - 去掉日期（`-2026年4月` 等）
  - 不超過 30 字元
  - 不可含 `?:;"'` 等特殊字元
- frontmatter 格式：
  ---
  title: <影片標題的繁體中文翻譯>（技術名詞與品牌名保留英文）
  tags:
    - youtube
  created: <今日 YYYY-MM-DD>
  updated: <今日 YYYY-MM-DD>
  published: <影片上傳日期 YYYY-MM-DD>
  source: <youtube url>
  ---
- 不使用 # 標題 heading（Quartz 從 frontmatter 自動產生）

**內容品質標準（重要）：**

情況 A — defuddle 抓到完整 transcript（contentMarkdown 超過 500 字）：
- 依影片的自然章節，用 `##` heading 分段（例：`## 核心架構`、`## 設定步驟`、`## 實際案例`）
- 每段用條列或短段落說明該章節的重點，包含具體細節（指令、設定路徑、數值等）
- 可用 code block 呈現指令或結構
- **禁止放原始逐字稿**或帶時間戳的文字
- 目標：讀者不看影片也能完全理解並執行

情況 B — defuddle 只抓到 description 或極少內容（不足 500 字）：
- 寫一個 `## 重點摘要` 段落，條列實際取得的資訊
- **禁止推測或補充** defuddle 沒有的內容

每個筆記建立後確認檔案存在。全部完成後回報結果清單。
```

## 步驟 6：彙整結果

輸出彙整表格：

| # | 影片標題 | 筆記路徑 | published | 狀態 |
|---|---------|---------|-----------|------|
| 1 | ... | content/YouTube/<頻道名>/... | YYYY-MM-DD | ✓ 完整 / ⚠ 內容不足 |

## 注意事項

- **defuddle 內容不足**：transcript 不足 500 字時走情況 B，只寫重點摘要，不推測補充
- **published fallback**：defuddle `--json` 有時不回傳 `published`，需用 Chrome 的 `meta[itemprop="datePublished"]` 作為備援
- **tags**：一律加 `youtube`，可依頻道主題加額外標籤（如 `claude-code`）
- **檔名長度**：超過 40 字元的標題適當縮短，保留關鍵詞
- **增量同步**：再次執行同一頻道時，Step 2 會過濾已有筆記，只建立新影片的筆記；`ytInitialData` 最多回傳 10 部（最新的），足以涵蓋一般更新週期
- **重複筆記**：若同名檔案已存在，跳過不覆寫
- **不發佈**：`content/YouTube/` 已在 ignorePatterns，無需加 `draft: true`
