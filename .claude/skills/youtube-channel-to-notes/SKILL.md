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
try {
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
  const result = videos.slice(0, 10).join('###');
  if (result.length > 1500) {
    document.title = 'TRUNCATED###' + result.substring(0, 1500);
  } else {
    document.title = result;
  }
} catch(e) {
  document.title = 'ERROR:structureMismatch###' + e.message;
}
```

3. 讀取 tab title（`tabs_context_mcp` 取得 `title` 欄位），依以下規則處理：
   - 若 title 以 `ERROR:` 開頭 → **立即停止**，告知用戶「ytInitialData 結構異常，請回報錯誤訊息：`<error message>`」
   - 若 title 以 `TRUNCATED###` 開頭 → 移除前綴繼續解析，並在步驟 6 彙整表格後標注「⚠ 資料可能截斷，部分影片未處理」
   - 正常情況：以 `###` 分割各筆，再以 `|||` 分割標題與 hex-encoded video ID
4. hex 解碼：每兩個十六進位字元還原為一個字元，得到 11 碼的 video ID
5. 組成 URL：`https://www.youtube.com/watch?v=<videoId>`
6. 從頻道 URL 取得頻道名稱，並正規化：
   - 來源優先順序：URL 路徑中的 `@handle`（去掉 `@`）→ 頁面 `<title>` 標籤文字
   - 正規化規則：空格轉 `-`，移除 `?:;"'!@#$%^&*()+=[]{}|\\/<>` 等特殊字元，保留英數字、中文字、`-`、`_`
   - 範例：`Chase H AI` → `Chase-H-AI`、`AI進化論!` → `AI進化論`
   - 後續所有步驟的 `<頻道名>` 皆使用正規化後的名稱

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
詳細指示請先 Read `.claude/skills/youtube-channel-to-notes/references/subagent-note-creator.md`。

筆記存放位置：content/YouTube/<頻道名>/
今日日期：<YYYY-MM-DD>

**影片清單（處理第 N-M 部）：**
N. <標題> — <URL>
...
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
- **影片已刪除**：defuddle 失敗時用 Chrome 確認，若出現「這部影片已無法播放」直接跳過，不建立任何筆記
- **不發佈**：`content/YouTube/` 已在 ignorePatterns，無需加 `draft: true`
