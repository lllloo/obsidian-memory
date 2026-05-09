---
title: "2026-05-09 Weekly Updates"
created: 2026-05-09
updated: 2026-05-09
tags:
  - updates
  - claude-code
  - codex
  - copilot
  - cursor
---

## Claude Code（v2.1.126 ~ v2.1.138）

本週發布 v2.1.126 至 v2.1.138，核心變更如下：

**新功能**

- `worktree.baseRef`（`fresh` | `head`）：控制 worktree 起點分支；預設 `fresh` = 從 `origin/<default>` 分，`head` = 保留本地未推送 commits
- Hooks 可讀取 `effort.level` / `$CLAUDE_EFFORT` 動態調整行為
- `settings.autoMode.hard_deny`：無條件封鎖特定操作，優先於 allow 例外
- `claude project purge [path]`：刪除 project 所有 Claude Code 狀態（支援 `--dry-run`、`--all`）
- `CLAUDE_CODE_SESSION_ID` 注入 Bash tool subprocess
- `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1`：退出 fullscreen renderer，保留原生 scrollback
- `--plugin-url <url>`：從 URL 下載 plugin `.zip` 供當前 session 使用
- `skillOverrides` 設定生效（`off` / `user-invocable-only` / `name-only`）
- `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`：Homebrew/WinGet 自動背景升級
- `claude auth login` 支援在 terminal 貼上 OAuth code（WSL2/SSH/container）

**Bug Fixes（重要）**

- 修正 subagents 無法透過 Skill tool 發現 project/user/plugin skills（v2.1.133）
- 修正 MCP OAuth refresh tokens 並發更新遺失，不再需要每日重登（v2.1.136）
- 修正 `/clear` 後 MCP servers 靜默消失（VS Code、JetBrains、Agent SDK）（v2.1.136）
- 修正 plan mode 在有匹配 `Edit(...)` allow rule 時未封鎖 file write（v2.1.136）
- 修正 `--resume` / `--continue` 在 project path 含底線時找不到 session（v2.1.136）
- 修正並行 session refresh-token race 導致全部 401（v2.1.133）
- 修正 extended thinking 在 tool call 後 redacted thinking block 觸發 API 400（v2.1.136）
- 修正 1 小時 prompt cache TTL 被靜默降為 5 分鐘（v2.1.129）
- 修正 deferred tools（WebSearch 等）在 `context: fork` subagent 第一個 turn 不可用（v2.1.126）
- WSL2：xclip/wl-paste 失敗時透過 PowerShell fallback 貼上 Windows clipboard 圖片

**安全**

- 修正 `allowManagedDomainsOnly` / `allowManagedReadPathsOnly` 在 higher-priority managed-settings source 缺少 `sandbox` block 時被忽略（v2.1.126）

**待注意**

- `worktree.baseRef` 在 v2.1.128 與 v2.1.133 之間有行為反轉，需確認設定
- `hard_deny` 語法待官方文件補充

---

## OpenAI Codex（v0.129.0 ~ v0.130.0）

**v0.130.0（2026-05-08）**

- 新增 `codex remote-control` 指令，簡化 headless app-server 啟動
- App-server 支援分頁瀏覽大型 thread（unloaded / summary / full turn item views）
- Plugin 詳情頁顯示 bundled hooks，分享時帶入 link metadata 與可探索性控制
- AWS Bedrock 支援 console-login 憑證（`aws login` profiles）
- 移除 `codex exec` 啟動 banner 的「research preview」字樣（暗示正式化）

**v0.129.0（2026-05-07）**

- **TUI Vim 模式**：composer 支援 modal Vim 編輯（`/vim`）
- **Session picker 重設計**：resume/fork 更方便，新增 raw scrollback、`/ide` context injection
- **Memories MCP v1**：記憶體 MCP 支援分頁 list、搜尋（multi-query、windowed）
- **Hooks 強化**：`/hooks` 瀏覽介面、compaction 前後可觸發 hook、`PreToolUse` additionalContext
- **Plugin 管理擴充**：workspace 分享、存取控制、marketplace remove/upgrade

**社群：改善版 Compaction Prompt**

社群用戶 `Zaczero` 分享改善版 compaction prompt，要求 LLM 輸出「executive summary handoff」（timeline、已完成工作、推理過程、parking 任務），長 session 跨 compaction 的上下文保留度顯著提升。需手動 patch `codex-rs/core/src/compact.rs` 並禁用 remote compaction。

**即將推出：Memories 功能**

OpenAI 官方維護者正在開發跨 session memories 功能（目前 rate limit 期，勿嘗試使用）。預計支援自動/手動觸發，credentials 不會被記憶。

---

## Cursor（v3.3，2026-04-30 ~ 2026-05-07）

**Agent 並行化**

- **Build in Parallel**：Agent 自動識別計畫中的獨立段落，以 async subagents 並行執行
- **Split PRs**：一鍵將變更拆成多個有依賴序的 PR，帶備份 snapshot

**PR 工作流深化**

- PR Review 介面：Reviews / Commits / Changes 三分頁，可全程留在 Cursor 不需切換 GitHub UI
- Inline review threads + top-level comments

**可觀測性**

- Context Usage Breakdown：顯示每次執行中 rules、skills、MCPs、subagents 各自的 context 佔用，可診斷 context 爆量根因

**企業功能**

- Model access controls：以 provider 或 configuration 為粒度設黑名單；**既有 blocklist 需在 2026-06-01 前遷移**
- Soft spend limits：50% / 80% / 100% 自動告警，不再直接封鎖用戶
- Security Review（Beta）：自動掃 PR 漏洞與 prompt injection；Vulnerability Scanner 定期掃整個 codebase

**Team Marketplace**

- 不再需要 repo 作為前置條件即可建立。三種分發模式：Default Off / Default On / Required

---

## GitHub Copilot

**模型汰換（需立即確認）**

| 模型 | 棄用日 | 替代 |
|------|--------|------|
| Claude Sonnet 4 | 2026-05-06（已生效） | Claude Sonnet 4.6 |
| GPT-4.1 | 2026-06-01 | GPT-5.5 |

涵蓋 Chat、inline edits、ask/agent mode、code completions 全功能。有腳本或設定檔指定這兩個 model ID 需盡快更新。

**Copilot CLI v1.0.44（2026-05-08）**

- Slash commands 可在輸入中途出現，單一訊息可呼叫多個 skills
- `userPromptSubmitted` hooks 可直接回應，不觸發 LLM call（可用作 prompt guard 或快速回應層）
- Autopilot mode tool 權限跨 `/clear` 保留
- Free 用戶 quota 顯示修正（不再一律顯示 100%）
- Ctrl+C 在 permission prompt 等待時不再 hang

**Rubber Duck 跨 model 家族**

- GPT 主流程 + Claude Rubber Duck（`/experimental on`）
- Claude 主流程 + GPT-5.5 Rubber Duck（舊版 GPT 升級）

**Cloud Agent：org-level secrets/variables**

- 新增獨立「Agents」secrets/variables 類型，支援 org 層級設定，一次配置可跨全部 repo 共用
- 與 Actions secrets 分離，避免權限混用

**VS Code 四月版重點（v1.116-v1.119）**

- Semantic Search 全面開放（全 workspace 皆可用）
- 跨 Repo Grep：對 GitHub org/repo 直接 grep，不需 clone
- BYOK 擴大至 Business/Enterprise（可接 OpenRouter、Google、Anthropic、OpenAI、Ollama）
- Skill 探索支援 `.claude/skills/` 與 `.agents/skills/` 目錄（跟進 Claude Code 生態慣例）
- Terminal 存取：Agent 可讀寫開啟中的 terminal

---

## 其他

**Gemini CLI v0.41.2**

Patch release，cherry-pick v0.41.1 的 formatter regression 修正，無新功能。

**opencode v1.14.41**

- 修正 formatter 輸出處理（寫入 stdout/stderr 正常運作）
- Session warping 可攜帶未 commit 的檔案變更
- ACP client 載入 session 時可還原上次的 model、mode、effort
- Desktop macOS：新增 Settings 選單項目

**notebooklm-py v0.4.0**

- Multi-account profiles：`notebooklm profile create/list/switch` 管理多個 Google 帳號
- `notebooklm skill install`：一鍵部署到 `~/.claude/skills/notebooklm` 與 `~/.agents/skills/notebooklm`
- `notebooklm doctor --fix`：自動診斷並修復 auth / profile 問題
- Browser cookie import：免 Playwright 直接複用現有瀏覽器 session
