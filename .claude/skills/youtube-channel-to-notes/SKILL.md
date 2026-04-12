---
name: youtube-channel-to-notes
description: 當使用者提供 YouTube 頻道網址並想要建立筆記時使用此 skill。用 Claude in Chrome 抓取頻道影片清單（最多 30 部），用平行 subagents 將每部影片建立成 Obsidian vault 筆記（content/YouTube/<頻道名>/）。觸發詞：提供 YouTube 頻道 URL、「幫我把這個頻道的影片建成筆記」、「youtube 轉筆記」、「抓頻道影片」。
---

# YouTube Channel to Notes

將 YouTube 頻道影片批次轉換成 Obsidian vault 筆記。

## 資料夾規則

- 筆記存放：`content/YouTube/<頻道名>/`（例：`content/YouTube/Chase-H-AI/`）
- 此資料夾已在 `quartz.config.ts` 的 `ignorePatterns` 中，**不會發佈到網站**
- 每個頻道資料夾下建立一個 `影片清單.base` 作為動態索引

## 步驟 1：抓取影片清單

使用 **Claude in Chrome**（mcp__claude-in-chrome 工具）抓取頻道影片清單：

1. 導航到頻道的 `/videos` 頁面
2. 向下捲動讓 YouTube 載入更多影片（重複捲動 + 等待）
3. 用 `read_page` 或 `get_page_text` 取得影片標題與連結
4. 取最多 30 部，按照頁面順序（最新在前）

> 注意：YouTube 使用虛擬捲動，需多次捲動才能看到所有影片。每次捲動後確認 DOM 中影片數量增加。

## 步驟 2：建立頻道資料夾

```bash
mkdir -p content/YouTube/<頻道名>
```

## 步驟 3：分批平行處理

將影片清單分成每批 6 部（最多 5 批），在**同一個 response** 中用 Agent tool 平行啟動所有 subagents。

每個 subagent 的任務 prompt 格式：

```
任務：用 defuddle 抓取 YouTube 影片內容，並在 Obsidian vault 建立筆記。

工作目錄：/Users/barney/code/obsidian-memory
筆記存放位置：content/YouTube/<頻道名>/

**影片清單（處理第 N-M 部）：**
N. <標題> — <URL>
...

**步驟：**
對每部影片：
1. 執行 `defuddle parse <url> --md` 取得影片頁面內容
2. 執行 `defuddle parse <url> -p description` 取得描述
3. 根據取得的內容建立筆記

**筆記規則（必須嚴格遵守）：**
- 檔案路徑：content/YouTube/<頻道名>/<標題>.md
- 檔案名稱：不可含空格，空格改為 -
- frontmatter 格式：
  ---
  title: <影片標題>
  tags:
    - youtube
  created: <今日 YYYY-MM-DD>
  updated: <今日 YYYY-MM-DD>
  source: <youtube url>
  ---
- 不使用 # 標題 heading（Quartz 從 frontmatter 自動產生）
- 內容包含：影片描述、重點摘要（若 defuddle 有抓到內容）
- 若 defuddle 抓不到內容，僅記錄標題與連結

每個筆記建立後確認檔案存在。全部完成後回報結果清單。
```

## 步驟 4：建立 影片清單.base

所有筆記建立完成後，在頻道資料夾建立 `影片清單.base`：

```yaml
filters:
  and:
    - 'file.inFolder("YouTube/<頻道名>")'
    - 'file.ext == "md"'

properties:
  source:
    displayName: 連結
  created:
    displayName: 日期
  file.name:
    displayName: 筆記

views:
  - type: table
    name: 影片清單
    order:
      - file.name
      - source
      - created
    sort:
      - property: created
        direction: DESC
```

## 步驟 5：彙整結果

輸出彙整表格：

| # | 影片標題 | 筆記路徑 | 狀態 |
|---|---------|---------|------|
| 1 | ... | content/YouTube/<頻道名>/... | ✓ 完整 / ⚠ defuddle timeout |

## 注意事項

- **defuddle timeout**：若某部影片抓取失敗，subagent 仍應建立基本筆記（標題 + URL），不中斷整批
- **tags**：一律加 `youtube`，可依頻道主題加額外標籤（如 `claude-code`）
- **檔名長度**：超過 60 字元的標題適當縮短，保留關鍵詞
- **重複筆記**：若同名檔案已存在，跳過不覆寫
- **不發佈**：`content/YouTube/` 已在 ignorePatterns，無需加 `draft: true`
