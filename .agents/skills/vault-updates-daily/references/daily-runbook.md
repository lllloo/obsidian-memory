# Vault Updates Daily Runbook

本檔承接 `SKILL.md` 的執行細節。真正同步前必須讀全文；不要把這些細節複製回 `SKILL.md`。

## Source Index

`updates/01.index.md` 是唯一來源真實值：追蹤哪些工具、抓哪些 changelog、是否啟用 starred 同步，都由此檔決定。不要在 skill 或腳本硬編碼工具清單。

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
- `GitHub repositories`：`- <owner>/<repo>|<tag>`，每行一個明確追蹤 repo；抓 releases。
- `GitHub starred`：`sync: releases` 代表啟用。有兩條路，腳本自動選：
  - **有 auth（`gh` 已登入，或 `GITHUB_TOKEN`／`GH_TOKEN` 屬於 star 擁有者本人）**：單一 GraphQL `viewer` call 抓所有 starred repos 的 releases，並**順手把 repo 清單寫回快照** `.agents/skills/vault-updates-daily/starred-repos.txt`。不要改成逐 repo REST call。
  - **無 auth（一般 token-free 環境）**：`viewer` query 需身分憑證，headless 環境查不到「我 star 了誰」。腳本改讀快照的 repo 清單，逐 repo 抓 `https://github.com/<repo>/releases.atom`——由 github.com 提供，免身分、不吃 REST 的 60/hr rate limit。
  - **Claude Code 雲端 GitHub proxy 限制**：Anthropic agent proxy 會攔截 `github.com` / `api.github.com`，並把 session 綁定到已配置 repositories。若 session 只授權本 vault repo，`GitHub repositories` 清單中列出的 repo 與 starred repos 的 releases / atom 會被 proxy 回 `403`（例如 `GitHub access to this repository is not enabled for this session. Use add_repo to request access.` 或 `sessions are bound to their configured repositories.`）。這不是 GitHub 回的 rate limit，也不是 relay failure；`releases.atom` 也會被同一層政策擋住，快照 fallback 無法解決。有官方非 GitHub changelog 頁的工具（如 `openai/codex`、`anthropics/claude-code`）因此優先改列 `Official changelogs`，從根源避開此限制。
  - **本 vault 目前停用 starred 同步**：本 vault 只在雲端執行、不本機跑，而 starred 本質是「我在 GitHub star 了誰」，沒有非 GitHub 替代來源，即使有快照，atom fallback 仍會被上述 proxy 擋下——在純雲端模式下結構性永遠踩不通。故 `01.index.md` 目前**沒有**寫入 `## GitHub starred` / `sync: releases`。若未來改回會定期本機執行的操作模式，才考慮重新啟用（啟用前需先本機跑一次 `--snapshot-starred` 建快照，見下段快照維護說明）。

  快照維護（僅在重新啟用 starred 時適用）：快照由本機 authed 執行時自動保鮮（每跑一次 daily 就更新）。要在不跑 daily 的情況下手動刷新，本機執行 `python3 .agents/skills/vault-updates-daily/scripts/fetch_updates.py --snapshot-starred`。雲端啟用前，務必先在本機跑過一次讓快照存在——否則雲端會回 `ERROR:starred:no auth and no snapshot ...`。
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
- `--index <path>`：指定來源 index，預設 `updates/01.index.md`。

輸出格式：

- `META:since|||<YYYY-MM-DD>`
- `META:starred|||live|||<n> repos`：authed 走 live viewer query，快照已刷新。
- `META:starred|||snapshot|||<date>|||<n> repos`：無 auth，改用快照 + atom；`<date>` 是快照日期，過舊時在回覆標注。
- `OFFICIAL:<name>|||<url>|||<tag>`
- `CHANGELOG:<source>|||<published>|||<title>|||<url>|||<body-snippet>`
- `RELEASE:<repo>|||<published>|||<tag>|||<name>|||<url>|||<body-snippet>`
- `ERROR:<source>:<message>`

記錄 `ERROR:` 後繼續處理其他來源；最後回覆列出需要人工追蹤的錯誤或候選。

若 explicit repo / starred atom 大量出現 Anthropic proxy 的 repo-bound `403`，回覆時標成「session GitHub repository access 未授權」，不要寫成 GitHub 整站 egress 封鎖。

抓取上限：

- starred repos：前 100 個（live viewer query）；快照 fallback 則為快照內的全部 repo。
- starred repo releases：live 路徑每 repo 前 5 筆；atom fallback 取該 repo feed 的近期 entries（github.com 預設約 10 筆），一律再用 `since` 過濾。
- explicit repo releases：`per_page=30`。

接近上限時，在回覆的「各來源抓取數」標注可能截斷；不要讓使用者誤以為已涵蓋全部。

## Official Changelog Handling

`fetch_updates.py` 對多數 `OFFICIAL:` 只列 URL，不抓頁面，交由執行 skill 的 agent 依下列步驟處理。**任何 `github.blog/changelog/.../feed/` 網址**是例外，腳本會自動辨識並直接轉成 `CHANGELOG:`（不限定 `/changelog/feed/` 這個總覽 feed，label 專屬 feed 如 `/changelog/label/copilot/feed/` 一樣自動處理）——只有未加 `/label/` 的總覽 feed 才會套用 `CHANGELOG_KEYWORDS` 關鍵字過濾，label feed 本身已經是精準範圍，不再過濾。

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

**週報式 labelled block 變體**（例如 `code.claude.com` 的 Claude Code What's New 頁）：內容不是逐條 `##`/`###` heading，而是 `<Update label="Week N" description="<日期範圍>" tags={[...]}>...內容...</Update>` 區塊，區塊內含指向該週獨立頁面的「閱讀 Week N 摘要 →」連結（如 `/zh-TW/whats-new/2026-w26`，補上網域即為完整 URL，例如 `https://code.claude.com/docs/zh-TW/whats-new/2026-w26`）。抽取規則：

1. 每個 `<Update>` block 算一筆候選。
2. `entry-date` 取 `description` 日期範圍的**結束日**（較寬鬆，避免同週稍早的更新因 since 卡在範圍中段而被漏掉）。
3. `entry-title` 用 `label` + `description`，例如 `Week 26（2026 年 6 月 22–26 日）`。
4. `url` 用該週獨立頁面的完整網址（每週各自穩定，可直接走一般 URL dedup，不必落到 `--tool/--key`）。
5. `body-snippet` 取 block 內文字內容（`label`/`description`/`tags` 屬性以外的段落），依一般規則截斷 800 字元。

**單頁版本清單變體**（例如 `opencode.ai/changelog`）：整頁列出所有版本，新到舊排列，每個版本以版本連結（如 `[v1.17.14]`）加日期起頭，非 `##`/`###` heading，頁面內也沒有各版本專屬錨點（版本連結多半指向該版本的 GitHub release，不可拿來當本頁 dedup URL）。抽取規則：

1. 依版本連結 + 日期切出每個版本區塊，只保留日期 `>= since` 的區塊。
2. `entry-date` 用區塊旁標示的日期。
3. `entry-title` 用版本號，例如 `v1.17.14`。
4. 沒有獨立 URL 可用，dedup 改走 `--tool "<index 內該來源的顯示名>" --key "<版本號>"`（見下方 Dedup 一節），**不要**傳頁面 URL。
5. `body-snippet` 取該版本區塊內文字內容，依一般規則截斷 800 字元；區塊常見子分類（如 Core／TUI／Desktop／SDK）可保留在摘要裡供分析判斷影響範圍。

同樣道理也適用於 `geminicli.com/docs/changelogs/`（Gemini CLI 全歷史頁）：這裡的 heading 是標準格式 `## Announcements: v0.45.0 - 2026-06-03`，日期就在 heading 內，可直接套用最上方的步驟 1-5 抽取；差別只在於頁面同樣沒有每筆各自的外部網址（只有頁內錨點），所以 dedup 一樣要用 `--tool/--key`，不要把錨點當獨立 URL。

## High-Precision Filtering

保留：

- 官方 changelog entry 會影響 workflow、CLI/API 使用、model、connector、billing/quota、deprecation、breaking change、security posture。
- GitHub release 有新功能、breaking change、security fix、workflow 變更、重要 regression 修復。

跳過：

- 只有 dependency bump、alpha / beta noise、內部維護、無使用者可見變更。
- 與 coding agent、developer tooling、developer workflow 無關。
- Body 為空且標題不足以判斷價值。

粗篩後仍過多時，最多 24 筆進分析；優先 official changelog，其次 stable / user-facing release。

## Dedup

日報是合併格式，不靠 `source:` frontmatter。寫入前每筆候選都跑 `dedup_check.py`。

Release（`RELEASE:`）與 GitHub Changelog（`CHANGELOG:`）都有 per-entry 穩定 URL，比 URL：

```
python3 .agents/skills/vault-updates-daily/scripts/dedup_check.py "<url>"
```

`--tool/--key` 模式用於「單頁列出全部版本、無獨立外部網址」型官方 changelog（`OpenCode`、`Gemini CLI` 皆屬此類，見上方「單頁版本清單變體」），改用工具名與穩定鍵、**不傳頁面 URL**：

```
python3 .agents/skills/vault-updates-daily/scripts/dedup_check.py --tool "<工具名>" --key "<版本或標題關鍵字>"
```

- 不要拿這類頁面 URL 走 URL 比對：頁面 URL 為整頁所有條目共用，舊日報任何指向該頁的連結都會命中，新條目必被誤判 DUP → 默默漏報。故只傳 `--tool/--key`、不傳 URL。
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
- 不把日報 wikilink 追加回 `updates/01.index.md`。

## Final Response

回覆固定包含：

- 各來源抓取數 / 粗篩通過數 / 已寫入數。
- 日報路徑。
- 跳過原因分布。
- 需要人工追蹤但未建檔的候選，最多 5 筆。
- 若有 `ERROR:` 或接近抓取上限，明確列出。
- starred 路徑據實標注：讀到 `META:starred|||snapshot|||<date>|||...` 時，回覆點明「starred 走快照（<date>）+ atom，非 live」；快照過舊（如超過 30 天）提醒本機刷新。讀到 `ERROR:starred:no auth and no snapshot` 時，明確說 starred 這次整段沒抓到、需先本機建快照——不要讓空的 starred section 被誤讀成「本週無更新」。
