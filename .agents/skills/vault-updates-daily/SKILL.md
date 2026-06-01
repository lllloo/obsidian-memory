---
name: vault-updates-daily
description: 每天彙整高信任 developer tooling 更新成一篇 Obsidian daily updates briefing，來源涵蓋官方 changelog / release notes、GitHub releases（含 authenticated user 的 starred repos）、GitHub discussions；專注 coding agent 與 developer workflow 相關變更。追蹤的工具清單由 `Inbox/Updates/01.index.md` 決定，skill 不硬編碼。使用時機：使用者要求「同步 changelog」、「release notes 更新」、「官方變更同步」、「daily updates」，或直接呼叫 /vault-updates-daily。
---

# Vault Updates Daily

同步高信任 developer tooling 更新到 Obsidian。重點是可回查、可操作、可沉澱的來源：官方 changelog、release notes、GitHub releases、GitHub discussions。

## 定位

優先來源：

1. **官方 changelog / release notes**：最高信任，適合建立正式來源筆記。
2. **GitHub releases**：版本、功能、breaking change、修復資訊。
3. **GitHub discussions**：actionable workaround、maintainer confirmation、重要設計決策。

不處理：

- GitHub issues（訊噪比太差，已移除）
- YouTube 頻道同步（用 `vault-youtube-sync`）
- 既有 vault 查詢（用 `ob-read`）或單篇筆記建檔（用 `ob-write`）
- 社群日報或輿情 briefing

## 產出

- 筆記：`Inbox/Updates/<YYYY-MM-DD>-daily-updates.md`（每次 sync 一篇，按工具分 section；同日多次 sync 追加而非覆蓋）
- Index：`Inbox/Updates/01.index.md`（只保存同步來源設定，不累積日報 wikilink）
- 筆記代表「高信任待消化來源」，進 Inbox 不直接發佈；後續可由使用者整理到 `Cards/` 或 `Topics/`。

### Frontmatter

```yaml
---
title: "<YYYY-MM-DD> Daily Updates"
created: <今日 YYYY-MM-DD>
updated: <今日 YYYY-MM-DD>
tags:
  - updates
  - <涵蓋的工具 tag，取自 01.index.md 各來源行的 tag 欄位>
---
```

`updates` 永遠保留；其餘 tags 由本次涵蓋的來源決定（不額外硬編碼清單）。

### 筆記結構

```markdown
## <工具名>

### <版本或日期>（[release 標題](url)）

> **繁中摘要**：...

**變更重點**

- ...

**實務影響**

- ...

---

## <工具名>

### <版本或日期>

...
```

每個工具一個 `##` section，底下每個 release / changelog entry 一個 `###` 子標題。跳過無使用者可見變更的項目。

## Source index

`Inbox/Updates/01.index.md` 是**唯一**的來源真實值：要追蹤哪些工具、抓哪些 changelog、是否啟用 starred 同步，全部由此檔決定。skill 與腳本都不硬編碼工具清單。

**索引檔格式：**

```markdown
---
title: Tool Updates
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags:
  - updates
  - index
---

高信任 developer tooling 更新來源。

## Official changelogs

- <顯示名>|<changelog URL>|<tag>

## GitHub repositories

- <owner>/<repo>|<tag>

## GitHub starred

sync: releases
```

來源格式：

- Official changelogs：`- <name>|<url>|<tag>`，每行一個官方 changelog。
- GitHub repositories：`- <owner>/<repo>|<tag>`，每行一個明確追蹤的 repo（會額外抓 discussions）。
- GitHub starred：`sync: releases` 代表啟用，從 authenticated user 的星星清單抓 releases（`gh` CLI 需已登入）。

三個 `##` 段可任意保留或省略；至少需有其一非空，否則 skill 報錯停止。

> **URL 維護**：Official changelogs 的 URL 可能因文件改版而失效。遇到 `ERROR:` 或抓到空頁時，先 WebFetch 該工具的官網首頁找新的 changelog 路徑，再更新 `Inbox/Updates/01.index.md`。
>
> **新增 / 移除工具**：直接編輯 `Inbox/Updates/01.index.md` 對應段落即可，**不要動 SKILL.md 或 fetch_updates.py**。

## 前置作業

用 `Read vault-map.md` 確認 cwd 為 repo root（harness-native，不經 shell）；讀不到就停止並請使用者 cd 到 repo root。

## 步驟 1：讀取來源

讀 `Inbox/Updates/01.index.md`：

- `## Official changelogs` 段：官方 changelog / release notes。
- `## GitHub repositories` 段：GitHub release / discussion 來源。
- `## GitHub starred` 段：是否啟用 starred 同步。

若 index 不存在，**停止並請使用者依「Source index」段建立**，不要自動產生預設清單（避免引入未經確認的追蹤源）。若三段皆為空，同樣停止並提示使用者至少加一個來源。單段為空時略過該來源類型，不中止整體流程。

## 步驟 2：抓候選

預設同步最近 7 天；使用者指定日期時用該日期到今天。

腳本自己解析 `Inbox/Updates/01.index.md` 的三段來源（official changelogs / repositories / starred），`--since` 預設 7 天前。cwd 為 vault root，用完整相對路徑執行：

```
python .agents/skills/vault-updates-daily/scripts/fetch_updates.py
```

- `python3` 無效時改 `python`。
- 指定日期：加 `--since YYYY-MM-DD`。
- 自訂 index 路徑：加 `--index <path>`（預設 `Inbox/Updates/01.index.md`）。

> 解析 index 與算 since 的邏輯都在腳本內（`parse_index`），跨平台、零 shell 膠水。SKILL 不再硬編碼工具清單——唯一真實來源是 `01.index.md`。
>
> **抓取上限（silent cap，避免誤判為已涵蓋全部）**：腳本對各來源有硬上限——starred repos 取前 100、每 repo releases 前 5、explicit repo releases `per_page=30`、discussions 前 20。starred 超過 100 個或單來源超過上限時會靜默漏抓。來源接近上限時，於回覆「各來源抓取數」一併標注可能截斷。

輸出格式：

- `META:since|||<YYYY-MM-DD>`
- `OFFICIAL:<name>|||<url>|||<tag>`
- `CHANGELOG:<source>|||<published>|||<title>|||<url>|||<body-snippet>`
- `RELEASE:<repo>|||<published>|||<tag>|||<name>|||<url>|||<body-snippet>`
- `DISCUSSION:<repo>|||<updated>|||<comments>|||<title>|||<url>|||<body-snippet>`（explicit repos 才抓；starred repos 只抓 releases）
- `ERROR:<source>:<message>`（記錄後繼續）

**OFFICIAL 行的處理**：腳本只列出 URL，不會自行抓取。對每個 `OFFICIAL:` 行（GitHub Changelog 除外，已由 RSS 轉成 `CHANGELOG:` 行），主 agent 用 Defuddle 或 WebFetch 讀取該 URL。若有多個 OFFICIAL URL 且有 subagent 能力，平行各呼叫一個 subagent 抓取；無 subagent 能力時串列執行。

抓到頁面後，找出日期格式的 heading（如 `## 2025-01-01`、`## v1.5.0 (2025-01-01)`），擷取 `since` 日期之後的 section（heading 到下一個同級 heading 之間的內容）作為一筆候選。無法識別日期 heading 時，以最近 5 個 major section 作為候選。每筆格式化為：

```
CHANGELOG:<name>|||<entry-date>|||<entry-title>|||<url>#<slug>|||<body-snippet>
```

其中 `<body-snippet>` 從段落提取純文字，截斷至 800 字元。無法取得個別 entry URL 時，用頁面 URL 加 heading slug（`<url>#<slug>`）作為 canonical URL，確保後續去重可識別。

## 步驟 3：高精度粗篩

保留候選：

- 官方 changelog entry 有 workflow / CLI / API / model / connector / billing-quota / deprecation / breaking change 影響。
- GitHub release 包含新功能、breaking change、security fix、workflow 變更、重要 bug fix。
- GitHub discussion 形成具體做法、官方回答、或重要設計決策。

跳過候選：

- release 只有內部依賴 bump、alpha/noise、或無使用者可見變更。
- changelog 與 developer tooling / coding agent / workflow 無關。
- starred repo 的 release 若與 coding agent / developer workflow 無關（例如純 UI library patch）。

若粗篩後候選仍過多，最多送 24 筆給分析階段，優先順序：

1. 官方 changelog / release notes
2. Stable GitHub releases 或明確 user-facing release
3. 有具體設計決策或官方回答的 discussion

## 步驟 4：去重與分批分析

### 去重（傳給 subagent 前先做）

日報是合併格式（無 `source:` frontmatter），用腳本做兩層 fixed-string 去重（個別筆記 `source: <url>` + 當日日報正文），fixed-string 比對自動避開 URL 裡 `?`/`&` 等 regex metachar。每個候選 URL 跑一次（cwd = repo root）：

```
python .agents/skills/vault-updates-daily/scripts/dedup_check.py "<url>" <YYYY-MM-DD>
```

輸出 `DUP:<檔案>` 即命中、標記 skip 不傳給 subagent；`UNIQUE` 則保留。若 changelog entry 沒有獨立 URL，使用該頁 URL 加 heading slug 作為 canonical URL（如 `<url>#<entry-slug>`），避免整頁只能存一次。

### 分批平行分析

去重後剩餘候選每批 8-10 筆，平行呼叫 general-purpose subagent。無 subagent 能力時由主 agent 直接讀 `references/item-analyzer.md` 全文執行同流程。

呼叫前讀取 `references/item-analyzer.md` 全文，放入 subagent prompt；不要叫 subagent 自己讀檔。

Subagent prompt 結構：

```text
[item-analyzer.md 全文]

---

今日日期：<YYYY-MM-DD>

候選清單：
1. <TYPE> <source/repo> <published/updated> <title>
   URL: <url>
   Body: <body-snippet，腳本已預先截取，無需再 fetch>
   metadata: <comments 數等>
```

Subagent 回傳格式（每個候選一條，save 附帶 section 內容）：

```text
SAVE <url>
TOOL: <工具名（依 item-analyzer.md 工具名稱正規表）>
META: <版本或日期，如 v1.5.0 · 2025-01-01 或 2025-01-01；用 · 分隔多個欄位>
CONTENT:
<此 item 的 markdown 內容，不含 ## 或 ### heading>
END_CONTENT

SKIP <url> <一行原因>
```

## 步驟 5：組裝日報與彙整

收集所有 subagent 回傳，依 `TOOL:` 分組，組裝日報：

1. 日報路徑：`Inbox/Updates/<YYYY-MM-DD>-daily-updates.md`
2. 若當日已有日報（同日第二次 sync），將新 section 追加到檔尾；不覆蓋已有內容。追加時同步更新 frontmatter：將本次涵蓋的工具 tag 合入既有 `tags`（去重），並更新 `updated` 為今日日期。
3. 寫入格式：

```markdown
---
title: "<YYYY-MM-DD> Daily Updates"
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
tags:
  - updates
  - <涵蓋的工具 tag>
---

## <工具名>

### <META>（[標題](url)）

<CONTENT block>

---

## <工具名>

### <META>

<CONTENT block>

---
```

主 agent 組裝邏輯：依 `TOOL:` 分組 → 每個 TOOL 寫 `## <工具名>` → 同 TOOL 底下每個 SAVE item 寫 `### <META>（[標題](<url>)）` 後接 CONTENT block → TOOL 之間插 `---`。若同 TOOL 下只有一筆，`### META` 標題可省略，直接放 CONTENT。

4. 不要把日報 wikilink 追加回 `Inbox/Updates/01.index.md`。此 index 只保存同步來源設定；日報本身留在 `Inbox/Updates/`，讀完後由使用者消化進 `Cards/` / `Topics/` 或刪除。

回覆固定包含：

- 各來源抓取數 / 粗篩通過數 / 已寫入數
- 日報路徑
- 跳過原因分布
- 需要人工追蹤但未建檔的候選（最多 5 筆）

所有變更留給使用者審核。
