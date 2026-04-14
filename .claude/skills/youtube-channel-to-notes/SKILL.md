---
name: youtube-channel-to-notes
description: 當使用者提供 YouTube 頻道網址並想要建立筆記時使用此 skill。用 curl + python3 抓取頻道影片清單（最多 10 部），用平行 subagents 將每部影片建立成 Obsidian vault 筆記（content/YouTube/<頻道名>/）。觸發詞：提供 YouTube 頻道 URL、「幫我把這個頻道的影片建成筆記」、「youtube 轉筆記」、「抓頻道影片」。
---

# YouTube Channel to Notes

將 YouTube 頻道影片批次轉換成 Obsidian vault 筆記。

## 資料夾規則

- 筆記存放：`content/YouTube/<頻道名>/`（例：`content/YouTube/Chase-H-AI/`）
- 此資料夾已在 `quartz.config.ts` 的 `ignorePatterns` 中，**不會發佈到網站**
- 每個頻道資料夾下建立 `01.index.md` 與 `02.影片清單.base` 作為索引（數字前綴確保固定排第一）

## 步驟 1：抓取影片清單與頻道簡介

**影片數量上限**：從用戶 prompt 解析（如「最多 20 部」→ `LIMIT=20`），未指定則預設 `10`，最大不超過 `30`（ytInitialData 的實際限制）。執行前先確定 `LIMIT` 的值，再帶入下方指令。

用 `curl + python3` 一次抓取頻道頁面，同時取出影片清單與頻道簡介（將 `<LIMIT>` 替換為實際數字，例如 `10`）：

```bash
curl -s "https://www.youtube.com/@<handle>/videos" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept-Language: en-US,en;q=0.9" \
  | python3 -c "
import sys, json, re
html = sys.stdin.read()
LIMIT = <LIMIT>

# 頻道簡介
desc_m = re.search(r'<meta name=\"description\" content=\"([^\"]*)\"', html)
print('DESC:' + (desc_m.group(1)[:300] if desc_m else ''))

# 影片清單（從 ytInitialData SSR 物件取出，不需執行 JS）
m = re.search(r'var ytInitialData = ', html)
if not m:
    print('ERROR:notFound')
    exit(1)
start = m.end()
try:
    decoder = json.JSONDecoder()
    data, _ = decoder.raw_decode(html[start:])
    tabs = data['contents']['twoColumnBrowseResultsRenderer']['tabs']
    count = 0
    for tab in tabs:
        grid = tab.get('tabRenderer', {}).get('content', {}).get('richGridRenderer')
        if not grid: continue
        for item in grid.get('contents', []):
            r = item.get('richItemRenderer', {}).get('content', {}).get('videoRenderer')
            if r and count < LIMIT:
                print('VIDEO:' + r['videoId'] + '|||' + r['title']['runs'][0]['text'])
                count += 1
except Exception as e:
    print('ERROR:' + str(e))
"
```

解析輸出：
- `DESC:<text>` → 頻道簡介（Step 3 使用，可能為空）
- `VIDEO:<videoId>|||<title>` → 每行一部影片，最多 10 行
- `ERROR:<message>` → **立即停止**，告知用戶錯誤訊息

組成影片 URL：`https://www.youtube.com/watch?v=<videoId>`

從頻道 URL 取得頻道名稱並正規化：
- 來源：URL 路徑中的 `@handle`（去掉 `@`）
- 正規化規則：空格轉 `-`，移除 `?:;"'!@#$%^&*()+=[]{}|\\/<>` 等特殊字元，保留英數字、中文字、`-`、`_`
- 範例：`Chase H AI` → `Chase-H-AI`、`AI進化論!` → `AI進化論`
- 後續所有步驟的 `<頻道名>` 皆使用正規化後的名稱

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

**在啟動文章生成前**，先在頻道資料夾建立 `01.index.md`（若已存在則跳過）。

頻道簡介已在步驟 1 的 `DESC:` 行取得，直接使用即可（可能為空）。寫入 index 時置於 frontmatter 下方、`![[02.影片清單]]` 上方；若為空則省略。

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

<頻道簡介（若有）>

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

- **defuddle 內容不足**：contentMarkdown 無時間戳格式（`**0:00**`）時走情況 B，只寫重點摘要，不推測補充
- **published fallback**：defuddle `--json` 有時不回傳 `published`，可用 `curl` 抓影片頁面後 grep `itemprop="datePublished"` 取得；若仍為空則留空
- **tags**：一律加 `youtube`，可依頻道主題加額外標籤（如 `claude-code`）
- **檔名長度**：超過 40 字元的標題適當縮短，保留關鍵詞
- **增量同步**：再次執行同一頻道時，Step 2 會過濾已有筆記，只建立新影片的筆記；`ytInitialData` 最多回傳 10 部（最新的），足以涵蓋一般更新週期
- **重複筆記**：若同名檔案已存在，跳過不覆寫
- **影片已刪除**：defuddle 失敗時，subagent 依 subagent-note-creator.md 的流程確認後跳過
- **不發佈**：`content/YouTube/` 已在 ignorePatterns，無需加 `draft: true`
