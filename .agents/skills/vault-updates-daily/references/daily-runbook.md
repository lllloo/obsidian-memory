# Vault Updates Daily Runbook

本檔承接 `SKILL.md` 的執行細節。真正同步前必須讀全文；不要把這些細節複製回 `SKILL.md`。

## Source Index

`Inbox/Updates/01.index.md` 是唯一來源真實值：追蹤哪些工具、抓哪些 changelog、是否啟用 starred 同步，都由此檔決定。不要在 skill 或腳本硬編碼工具清單。

索引格式：

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

解析規則：

- `Official changelogs`：`- <name>|<url>|<tag>`，每行一個官方 changelog。
- `GitHub repositories`：`- <owner>/<repo>|<tag>`，每行一個明確追蹤 repo；會抓 releases 與 discussions。
- `GitHub starred`：`sync: releases` 代表啟用。有兩條路，腳本自動選：
  - **有 auth（`gh` 已登入，或 `GITHUB_TOKEN`／`GH_TOKEN` 屬於 star 擁有者本人）**：單一 GraphQL `viewer` call 抓所有 starred repos 的 releases，並**順手把 repo 清單寫回快照** `.agents/skills/vault-updates-daily/starred-repos.txt`。不要改成逐 repo REST call。
  - **無 auth（如雲端 Claude agent）**：`viewer` query 需身分憑證，headless 環境查不到「我 star 了誰」。腳本改讀快照的 repo 清單，逐 repo 抓 `https://github.com/<repo>/releases.atom`——由 github.com 提供，免身分、不吃 REST 的 60/hr rate limit。
  - discussions 仍只走 GraphQL（需 auth），無 auth 時該來源會回 `ERROR:discussions:...`；starred 有 atom fallback，discussions 沒有。

  快照維護：快照由本機 authed 執行時自動保鮮（每跑一次 daily 就更新）。要在不跑 daily 的情況下手動刷新，本機執行 `python3 .agents/skills/vault-updates-daily/scripts/fetch_updates.py --snapshot-starred`。雲端首次啟用前，務必先在本機跑過一次讓快照存在——否則雲端會回 `ERROR:starred:no auth and no snapshot ...`。
- 三段可任意省略；至少一段非空。不要自動產生預設清單。
- 新增或移除工具時，只改 index；不要改 `SKILL.md` 或 `fetch_updates.py`。

若 official URL 失效或抓到空頁，先讀該工具官網首頁找新的 changelog / release notes 路徑，再更新 index。

## Fetch Script

在 vault root 執行：

```
python3 .agents/skills/vault-updates-daily/scripts/fetch_updates.py
```

常用參數：

- `--since YYYY-MM-DD`：指定起始日。
- `--index <path>`：指定來源 index，預設 `Inbox/Updates/01.index.md`。

輸出格式：

- `META:since|||<YYYY-MM-DD>`
- `META:starred|||live|||<n> repos`：authed 走 live viewer query，快照已刷新。
- `META:starred|||snapshot|||<date>|||<n> repos`：無 auth，改用快照 + atom；`<date>` 是快照日期，過舊時在回覆標注。
- `OFFICIAL:<name>|||<url>|||<tag>`
- `CHANGELOG:<source>|||<published>|||<title>|||<url>|||<body-snippet>`
- `RELEASE:<repo>|||<published>|||<tag>|||<name>|||<url>|||<body-snippet>`
- `DISCUSSION:<repo>|||<updated>|||<comments>|||<title>|||<url>|||<body-snippet>`
- `ERROR:<source>:<message>`

記錄 `ERROR:` 後繼續處理其他來源；最後回覆列出需要人工追蹤的錯誤或候選。

抓取上限：

- starred repos：前 100 個（live viewer query）；快照 fallback 則為快照內的全部 repo。
- starred repo releases：live 路徑每 repo 前 5 筆；atom fallback 取該 repo feed 的近期 entries（github.com 預設約 10 筆），一律再用 `since` 過濾。
- explicit repo releases：`per_page=30`。
- discussions：前 20 筆。

接近上限時，在回覆的「各來源抓取數」標注可能截斷；不要讓使用者誤以為已涵蓋全部。

## Official Changelog Handling

`fetch_updates.py` 對多數 `OFFICIAL:` 只列 URL，不抓頁面。GitHub Changelog RSS 例外，會直接轉成 `CHANGELOG:`。

處理 `OFFICIAL:`：

1. 用 Defuddle 或 WebFetch 讀頁面。
2. 找日期或版本 heading，例如 `## 2026-01-01`、`## v1.5.0 (2026-01-01)`。
3. 擷取 `since` 之後的 section，heading 到下一個同級 heading 之間算一筆候選。
4. 無法識別日期 heading 時，只取最近 5 個 major section。
5. 每筆格式化為：

```text
CHANGELOG:<name>|||<entry-date>|||<entry-title>|||<url>#<slug>|||<body-snippet>
```

`body-snippet` 取純文字並截斷到 800 字元。無法取得個別 entry URL 時，用頁面 URL 加 heading slug 只作顯示連結；anchor 不作為去重依據。

## High-Precision Filtering

保留：

- 官方 changelog entry 會影響 workflow、CLI/API 使用、model、connector、billing/quota、deprecation、breaking change、security posture。
- GitHub release 有新功能、breaking change、security fix、workflow 變更、重要 regression 修復。
- GitHub discussion 形成具體 workaround、maintainer confirmation、重要設計決策，或多人命中且會影響日常使用。

跳過：

- 只有 dependency bump、alpha / beta noise、內部維護、無使用者可見變更。
- 與 coding agent、developer tooling、developer workflow 無關。
- Body 為空且標題不足以判斷價值。

粗篩後仍過多時，最多 24 筆進分析；優先 official changelog，其次 stable / user-facing release，再來有具體結論的 discussion。

## Dedup

日報是合併格式，不靠 `source:` frontmatter。寫入前每筆候選都跑 `dedup_check.py`。

Release / discussion 有穩定 URL：

```
python3 .agents/skills/vault-updates-daily/scripts/dedup_check.py "<url>"
```

官方網頁 changelog 單條沒有穩定 URL，只用工具名與穩定鍵，**不傳頁面 URL**：

```
python3 .agents/skills/vault-updates-daily/scripts/dedup_check.py --tool "<工具名>" --key "<版本或標題關鍵字>"
```

- 不要拿頁面 URL 走 URL 比對：頁面 URL 為整頁所有條目共用，舊日報任何指向該頁的連結都會命中，新條目必被誤判 DUP → 默默漏報。腳本在 `--key` 模式已忽略 URL 引數，但正確用法是不傳。
- `--tool` 對應日報的 `## <工具名>`，限縮比對範圍。
- `--key` 有版本號就用版本；無版本時用 distinctive 標題關鍵字。
- 腳本只在 `### ` 標題行比對 key，避免內文順帶提及版本造成誤判。
- `DUP:<檔案>`：跳過。
- `UNIQUE`：保留進分析。

## Analysis

去重後每批 8-10 筆。可用 `Agent` 工具時平行呼叫，固定 `subagent_type: "general-purpose"`；無 Agent 工具時主 agent 直接執行。

呼叫前讀 `references/item-analyzer.md` 全文，貼進 prompt；不要叫 subagent 自己讀檔。

Prompt 形狀：

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

回傳格式：

```text
SAVE <url>
TOOL: <工具名>
META: <版本或日期，如 v1.5.0 · 2026-01-01 或 2026-01-01>
CONTENT:
<此 item 的 markdown 內容，不含 ## 或 ### heading>
END_CONTENT

SKIP <url> <一行原因>
```

## Assembly

收集 `SAVE` 後依 `TOOL:` 分組。

日報寫入格式：

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

**繁中摘要**：...

- **<變更名>**：...

---
```

組裝規則：

- 每個 `TOOL:` 寫成一個 `## <工具名>`。
- 同工具多筆時，每筆用 `### <META>（[標題](url)）`。
- 同工具只有一筆時，可省略 `###`，但仍要讓來源 URL 可見。
- 工具之間用 `---` 分隔。
- 同日已有日報時追加到檔尾，不覆蓋；同步合併 tags 並更新 `updated`。
- 不把日報 wikilink 追加回 `Inbox/Updates/01.index.md`。

## Final Response

回覆固定包含：

- 各來源抓取數 / 粗篩通過數 / 已寫入數。
- 日報路徑。
- 跳過原因分布。
- 需要人工追蹤但未建檔的候選，最多 5 筆。
- 若有 `ERROR:` 或接近抓取上限，明確列出。
- starred 路徑據實標注：讀到 `META:starred|||snapshot|||<date>|||...` 時，回覆點明「starred 走快照（<date>）+ atom，非 live」；快照過舊（如超過 30 天）提醒本機刷新。讀到 `ERROR:starred:no auth and no snapshot` 時，明確說 starred 這次整段沒抓到、需先本機建快照——不要讓空的 starred section 被誤讀成「本週無更新」。
