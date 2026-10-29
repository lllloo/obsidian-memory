---
title: Coding agent 指示檔與規則載入機制對照
description: Claude Code、Codex、OpenCode、pi 與 Cursor、Copilot 的指示檔階層、多規則檔與 glob 條件載入支援度，附各家替代做法
created: 2026-09-22
updated: 2026-10-29
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - claude-code
  - agent-framework
---

2026-09-22 三輪 Query 的回存：起點是「plugin 大多只支援 Claude Code 與 Codex，pi 與 OpenCode 呢」，追到「Codex 不支援 rules」，再追到「rules 是不是 Claude Code 獨有」。來源全為各家官方文件與 GitHub 原始 repo 當日查得，強度「高」；「為什麼分兩群」一節是本頁判讀，非文件說法。

**一句話**：「多個規則檔＋glob 條件載入」不是 Claude Code 獨有，是 IDE 型 agent（Cursor、Copilot）的既有設計，Claude Code 是跟進者；**缺這功能的是終端 CLI 那一群**——Codex、OpenCode、pi 都只有目錄層級的 AGENTS.md 串接。

## 對照表

| 工具 | 指示檔階層 | 多個規則檔 | 依路徑條件載入 | 載入時機 |
|---|---|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md`＋專案 `CLAUDE.md`／`AGENTS.md`，`@` 匯入 | `.claude/rules/*.md` | 原生 frontmatter `paths` | 啟動載全域與專案檔；子目錄 CLAUDE.md／AGENTS.md 與 path-scoped rules 在 session 中途依接觸檔案延遲載入 |
| Codex | `~/.codex/AGENTS.md`＋git root 到 cwd 每層一檔 | 無（每目錄只取一檔） | 無 | 啟動時一次建鏈 |
| OpenCode | `~/.config/opencode/AGENTS.md`＋每層 `AGENTS.md`（v2 不再 fallback `CLAUDE.md`） | `instructions` 陣列（檔案／glob／`~/` 路徑／HTTP(S) URL），v1、v2 都會載入，排在 AGENTS.md 之後（原記「v2 接受但不解析」**已被取代（2026-10-29）**，見下） | 無 glob 條件；v2 子目錄 `AGENTS.md` 在讀檔或列目錄時延遲載入（目錄層級按需） | v1 啟動一次載入；v2 全域與往上找到的 AGENTS.md 在 session 中編輯會於下一請求前注入，子目錄檔延遲載入、載入後再改不會自動重注入（需開新 session）（原記「v2 子目錄檔 session 中編輯下一請求生效」**已被取代（2026-10-29）**） |
| pi | `~/.pi/agent/AGENTS.md`＋從 cwd 往上每層串接 | 無原生 | 無原生；extension 可自製 | 啟動時載入；extension 可在工具呼叫時介入 |
| Cursor | `AGENTS.md`（純 markdown） | `.cursor/rules/*.mdc` | frontmatter `globs`＋`alwaysApply`＋`description` 三模式 | 依編輯器開啟檔案觸發 |
| GitHub Copilot | `.github/copilot-instructions.md`＋就近 `AGENTS.md` | `.github/instructions/*.instructions.md` | frontmatter `applyTo` glob | 依接觸檔案觸發 |

## 各家細節

### Codex

官方 AGENTS.md 指南（developers.openai.com）的機制：全域層讀 `~/.codex/AGENTS.override.md`，否則 `AGENTS.md`；專案層從 git root 走到 cwd，每個目錄依 `AGENTS.override.md` → `AGENTS.md` → `project_doc_fallback_filenames` 順序**只取一檔**，由上往下串接。合併大小達 `project_doc_max_bytes`（預設 32 KiB，`codex-rs/config/defaults.toml` 一手核對）即**靜默停止加檔**，官方解法是調大或拆到子目錄。指示鏈在 session 開始時建好，之後不變。不支援 `@` 匯入。

替代做法與缺口：子目錄放 `AGENTS.md` 只在該目錄啟動時載入（從 root 啟動不會載子目錄的檔，因為只走 root→cwd 路徑，不看實際改了哪個檔）；寫成 skill 可按需載入但觸發靠語意比對；全塞根檔最穩但吃 32 KiB 上限。

Codex CLI 本體變動極快（2026-09 約每週一個 minor、alpha 每天數個），但近兩版 release notes 的改動集中在 app-server、daemon、Guardian 審核與 TUI，agent 看得到的指示檔介面沒有動。Claude Code 端的 `openai-codex` marketplace plugin 則自 2026-06-23 bump 到 v1.0.5 後，僅 2026-07-08 一筆修正提交（移除 git 指令的 shell expansion），之後無動靜（[GitHub commits](https://github.com/openai/codex-plugin-cc/commits/main) 一手）。

### OpenCode

**v1／v2 分歧（2026-09-22 補）**：下段描述的是 v1 文件（opencode.ai/docs/rules）。v2 文件（opencode.ai/v2/docs/instructions）改為只認 `AGENTS.md`、不再 fallback `CLAUDE.md`；`instructions` 陣列 schema 仍接受但**目前不解析**（檔案、glob、URL 都不生效）〔**已被取代（2026-10-29）**：現行 [v2 instructions 文件](https://opencode.ai/v2/docs/instructions) 寫明 `instructions` 陣列會實際載入，支援檔案、glob、`~/` 路徑與 HTTP(S) URL（5 秒逾時），依列出順序排在 AGENTS.md 之後，本機檔案變更也像 AGENTS.md 一樣更新；migrate-v1 文件亦把 `instructions` 列為不需遷移的欄位。文件未標日期，確切啟用版本未查到。它仍是無條件載入、不依接觸路徑觸發，「無 glob 條件載入」的結論不變〕；子目錄的 `AGENTS.md` 改成 agent 讀到該區域時才延遲載入，session 中編輯會在下一次請求前注入〔**已被取代（2026-10-29）**：同一份 v2 文件把兩種檔分開講——子目錄（nested）`AGENTS.md` 在讀檔或列目錄時延遲載入，載入後再修改**不會自動偵測**，要開新 session 才生效（原文「Edits to a nested file are not detected automatically after it loads. Start a new session when updated text must apply immediately.」）；「session 中編輯於下一次請求前注入」只適用全域與往上找到的 AGENTS.md〕——這是四家 CLI 裡唯一「目錄層級、session 中途按需」的機制，仍不是 glob 條件，但比 Codex 的啟動時一次建鏈更接近 rules。**已被取代（2026-10-13）**：Claude Code 的子目錄 CLAUDE.md（長期行為）與子目錄 AGENTS.md（v2.1.277 起）同樣在 Claude 讀／寫／編輯該子目錄檔案時才載入、不在啟動時載（[官方 memory 文件](https://code.claude.com/docs/en/memory)「Instead of loading them at launch」；[官方 CHANGELOG](https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md) 2.1.288／2.1.290 一手，未實測），故此機制並非四家唯一，正確說法是「Codex／pi 都沒有的目錄層級按需機制」。OpenCode v2「session 中編輯於下一請求注入」的再注入特性（2026-10-29 更正：只適用全域與往上找到的 AGENTS.md，子目錄檔載入後再改不會重注入，見上），Claude Code 文件只提 compaction 後重載，是否 session 中編輯即生效未查證。

v1 官方 rules 文件：`instructions` 陣列接受檔名、glob（範例含 `.cursor/rules/*.md`、`packages/*/AGENTS.md`）與遠端 URL（5 秒 timeout），**全部在啟動時載入並與 AGENTS.md 串接**，不解析 frontmatter、不依接觸檔案決定。相容層會讀 Claude Code 的 `CLAUDE.md`、`~/.claude/CLAUDE.md`、`~/.claude/skills/` 當 fallback（可用 `OPENCODE_DISABLE_CLAUDE_CODE*` 環境變數關閉），但文件**未提 `.claude/rules/`**。官方對「按需載入」的建議是在 AGENTS.md 寫散文叫模型「看到 `@rules/x.md` 引用時再用 Read 讀」，靠模型自律而非機制。

### pi

README「Context Files」：從 `~/.pi/agent/AGENTS.md` 與 cwd 往上每層載 `AGENTS.md`（或 `CLAUDE.md`），同目錄有 `AGENTS.override.md` 則取代之，全部串接；`--no-context-files` 可關。沒有 `instructions` 陣列、沒有 `@` 匯入。

但 extension 的 `tool_call` 事件拿得到 `read`／`edit`／`write` 的 `path`，`tool_result` 可改寫回傳內容（中介軟體式鏈接）。寫一支短 extension，在讀到符合 glob 的檔案時把對應規則附進 tool result，即可自製 `paths:` 條件載入——這是「能做」不是「內建」，得自己維護。與 [[pi-與-OpenCode-v2-比較]] 的定性一致：pi 對所有「沒有 X」的回答都是「寫 extension」。

### Cursor 與 Copilot（原型出處）

Cursor `.cursor/rules/*.mdc` 要求必有 frontmatter，純 `.md` 會被規則系統忽略；`alwaysApply: true` 永遠載、`globs` 路徑匹配自動附加、只有 `description` 則由 agent 依描述決定是否引用。Copilot `.github/instructions/NAME.instructions.md` 用 `applyTo` glob（如 `"**/*.ts,**/*.tsx"`，`"**"` 為全域）。Claude Code 的 `paths` 與 Copilot 的 `applyTo` 是同一模式換欄位名。

## 為什麼分兩群（本頁判讀）

IDE 隨時知道使用者開著哪個檔，路徑條件是自然的觸發點；終端 CLI 只在啟動時知道 cwd，所以三家都停在「目錄層級」的 AGENTS.md 串接（OpenCode v2 子目錄檔已改延遲載入，見上）。Claude Code 是 CLI 卻做了 rules，靠的是在 session 中途看工具讀寫到哪個檔再注入——這是它與其他三家在機制上的實質差異，也是把 `~/.claude/rules/` 那套搬到其他 harness 時會直接撞到的牆。

## Plugin 分發層的對應現象

大多數 plugin 只做 `.claude-plugin/`＋`.codex-plugin/` 兩份 manifest 就收手，因為 pi 與 OpenCode 各用自己的機制：pi 是 `package.json` 宣告 `"pi": { "extensions": [...], "skills": [...] }`、`pi install git:...` 安裝；OpenCode 是 `opencode.json` 的 `plugin`（v2 改名 `plugins`）陣列接 npm／git spec，且 v1 plugin 在 v2 不相容。Codex 端 2026-09 文件已改推 agent-plugins.org 的可攜 `plugin.json`（舊 `.codex-plugin/` 仍相容），並有 `.agents/plugins/marketplace.json` 目錄格式。本機實查（2026-09-22）：superpowers 6.3.0 做了 `.claude-plugin`、`.codex-plugin`、`.cursor-plugin`、`.devin-plugin`、`.hermes-plugin`、`.kimi-plugin`、`.opencode`、`.pi` 全套；diagram-design 只有 claude＋codex；`openai-codex` 的 codex plugin 只有 `.claude-plugin`。純 skill 型 plugin 把 `skills/` 目錄丟進 pi／OpenCode 的 skills 路徑即可用，前提是 skill 內不用 `${CLAUDE_PLUGIN_ROOT}` 這類 Claude 專屬替換字串（見 [[Agent-Skill-腳本路徑的規範與實況]]）；有 hook 的 plugin 則要各自改寫，沒有自動轉換。

## 關聯

- [[四套-coding-agent-能力差異對照]]——本頁是該頁「指示檔」一列的展開；其餘十四個維度在該頁。
- [[pi-與-OpenCode-v2-比較]]——該頁比兩套 harness 的整體能力取捨；本頁只切「指示檔與規則」這一個面向往下挖，pi「寫 extension 補一切」的哲學在此有具體實例。
- [[LLM-方案定價與-coding-agent-比較]]——該頁算錢與訂閱額度能否給第三方 harness；本頁是換 harness 時規則檔能不能帶走的機制面。
- [[Agent-Skill-腳本路徑的規範與實況]]——skill 跨 harness 可攜的前提（裸相對路徑），是本頁「純 skill 型 plugin 可直接搬」的依據。
