---
title: "2026-05-22 Daily Updates"
created: 2026-05-22
updated: 2026-05-22
tags:
  - updates
  - codex
  - claude-code
  - copilot
  - gemini-cli
  - opencode
---

## OpenAI Codex

### 26.519 · 2026-05-21（[changelog](https://developers.openai.com/codex/changelog#appshots-goal-mode-and-more-26519)）

> **繁中摘要**：Codex app 26.519 把 Appshots、Goal mode、remote computer use、plugin sharing 與 browser-use 可靠性往前推，重點是讓 Codex 更容易從桌面、手機與瀏覽器情境接手實際工作。

**變更重點**

- macOS Codex app 新增 Appshots：按兩個 Command 鍵可把最前景 app 視窗的 screenshot 與可取得文字送給 Codex。
- Goal mode 不再是 experimental，涵蓋 Codex app、IDE extension 與 CLI，可讓 Codex 長時間朝特定 objective 推進。
- Remote computer use 允許 Mac 鎖定後仍操作桌面 app，包含經 Codex Mobile 遠端操作；範圍限於 active trusted computer-use turns，並有 short-lived authorization、covered displays、local input relock 等保護。
- ChatGPT Business 可透過 marketplace sources 分享 plugin bundles；Enterprise 支援仍在後續。
- In-app browser annotations 可直接標註字級、顏色、間距等 styling；browser-use 也加快 image asset 抽取、改善 structured data 擷取，並修正 Windows 與地區可用性等可靠性問題。

**實務影響**

- Appshots 與 remote computer use 讓 Codex 更接近跨裝置、跨 app 的 desktop agent，而不是只能處理 repo 內文字。
- Goal mode 進入穩定能力後，長時間任務可以更正式地納入 workflow，但仍需要明確 objective 與中途檢查點。
- Plugin sharing 對 Business team 有直接價值：可把 skills、app integrations、MCP servers 打包成可重複分發的工作流。

### v0.133.0 · 2026-05-21（[release](https://github.com/openai/codex/releases/tag/rust-v0.133.0)）

> **繁中摘要**：Codex CLI 0.133.0 延伸 goal、remote-control、permission profiles、plugin discovery 與 extension lifecycle，並補上多個 app-server / AGENTS / plan-mode 修正。

**變更重點**

- Goals 預設啟用，具備 dedicated storage，並可跨 active turns 追蹤進度。
- `codex remote-control` 改成 foreground-style command：等待 readiness、回報 machine status，並保留明確的 daemon-style `start` / `stop`。
- Permission profiles 新增 list APIs、inheritance、managed `requirements.toml`、runtime refresh，並強化 Windows sandbox integration。
- Plugin discovery 更容易檢查：list output 顯示 marketplace awareness、installed versions、marketplace roots 與 remote collection。
- Extensions 可觀察更多 lifecycle events，包含 subagent start / stop、tool execution、turn metadata、async approval / turn processing。
- 修正 plan-mode modified Enter 誤送出、AGENTS instruction loading、app-server startup / shutdown races、resume / fork 空路徑、plugin upgrade 與 realtime v1 websocket compatibility。

**實務影響**

- Goal 與 remote-control 都往「可長時間運行、可遠端接手」方向靠攏，適合 automation 與 mobile steering。
- Permission profiles 與 extension lifecycle 增強會影響 enterprise / plugin-heavy setup 的治理方式。
- AGENTS 與 plan-mode 修正對 Windows / PowerShell 使用者有直接穩定性收益。

---

## Claude Code

### v2.1.148 · 2026-05-22（[release](https://github.com/anthropics/claude-code/releases/tag/v2.1.148)）

> **繁中摘要**：Claude Code v2.1.148 是 v2.1.147 的緊急 hotfix，修正部分使用者 Bash tool 每次指令都回傳 exit code 127 的 regression。

**變更重點**

- 修正 Bash tool 對部分使用者每個 command 都回傳 exit code 127 的問題。

**實務影響**

- 若升到 v2.1.147 後 shell command 全面失敗，應直接升到 v2.1.148。
- 這是執行層級 regression，不適合延後處理。

### v2.1.147 · 2026-05-21（[release](https://github.com/anthropics/claude-code/releases/tag/v2.1.147)）

> **繁中摘要**：Claude Code v2.1.147 聚焦 background sessions、`/code-review`、auto-updater、PowerShell、MCP pagination、plugin agents 與 Windows terminal 穩定性。

**變更重點**

- `claude agents` 中以 Ctrl+T pinned 的 background sessions 可在 idle 時保持 alive，更新後原地 restart，並在 memory pressure 下晚於非 pinned sessions 被釋放。
- `/simplify` 改名為 `/code-review`，可指定 effort level；`--comment` 可把 findings 發成 GitHub PR inline comments；舊的 cleanup-and-fix 行為已移除。
- Auto-updater 會 retry transient network failures，並在失敗時顯示具體錯誤類型、OS error code 與目前版本。
- 修正 PowerShell hook `if` 條件比對、PowerShell tool output、Windows「Yes, and don't ask again」規則寫入、Microsoft Store / winget `pwsh` 安裝造成的失敗。
- 修正 MCP servers pagination 只取第一頁導致 resources、templates、prompts 掉失。
- 修正 plugin agents 在 `tools:` frontmatter 宣告多個 `Agent(...)` 時只保留最後一個的問題。
- 修正 auto mode 在使用者或 skill 明確需要 `AskUserQuestion` 時仍抑制提問的問題。

**實務影響**

- `/code-review` 現在是 correctness review 入口，不應再期待它做整理型 cleanup。
- Pinned background sessions 與 auto-updater 修正讓長時間 agent dashboard 更可靠。
- MCP pagination 與 multi-agent plugin 修正會直接影響大型 MCP / plugin setup 的可見工具面。

---

## GitHub Copilot CLI

### v1.0.52 · 2026-05-21/22（[v1.0.52-0](https://github.com/github/copilot-cli/releases/tag/v1.0.52-0), [v1.0.52-1](https://github.com/github/copilot-cli/releases/tag/v1.0.52-1)）

> **繁中摘要**：Copilot CLI v1.0.52 加入 deferred tool loading、compact focus instructions、quota 顯示與多個 Windows / session resume 修正，偏向讓長 session 與大型 tool surface 更穩。

**變更重點**

- Custom agents 可在 frontmatter 用 `deferred-tool-loading` opt in 延後載入工具，讓大型 tool list 透過 tool-search discovery。
- `/compact` 接受 optional focus instructions，可指定壓縮摘要的重點。
- `/usage` 顯示 session 與 weekly limits 的 quota progress bars。
- General-purpose subagents 在可用時使用 GPT-5.4 或 GPT-5.5。
- Status line command 支援 plain shell commands，不限 executable script path。
- 自動清理 `~/.copilot/logs/` 舊 process logs，避免磁碟無限制成長。
- 修正 session resume 對非 URL 字串、HTTP/2 upload stall timeout retry、Windows high-bit exit code、legacy MCP OAuth config migration 等問題。

**實務影響**

- Deferred tool loading 對自訂 agents 與大型 MCP/tool bundle 很關鍵，可降低啟動時上下文壓力。
- `/compact` focus instructions 讓長 session 的摘要更可控，適合在大型 refactor 或多階段調查中使用。
- Quota bars 與 auto log pruning 都是長期使用 Copilot CLI 的日常維護改善。

### v1.0.51 · 2026-05-20（[release](https://github.com/github/copilot-cli/releases/tag/v1.0.51)）

> **繁中摘要**：Copilot CLI v1.0.51 增加指定 session id、remote policy error、remote mid-turn 使用、status line、MCP 啟動速度、security review hook 與 memory cost tips。

**變更重點**

- `--session-id=<id>` 可 resume 已知 sessions / tasks，或以指定 UUID 開新 session。
- `/remote` commands 遵守 organization remote control / cloud view policy，禁用時會顯示清楚錯誤；agent 工作中也可用 `/remote`。
- Terminal footer status line 可顯示 session info，例如 model、context window、git branch。
- 多 HTTP MCP servers 的 startup 載入更快。
- 新增 experimental `/security-review` slash command。
- 新增 `preMcpToolCall` hook，讓 hook providers 控制 outgoing MCP request metadata。
- `/chronicle cost-tips` 可產生個人化 token usage / cost reduction 建議。

**實務影響**

- 固定 session id 與 remote policy error 對 automation / enterprise 管理更友善。
- Status line 把 session 狀態拉到常駐介面，對多 branch / 多 model 工作流有用。
- `preMcpToolCall` 代表 Copilot CLI 的 MCP 治理面更細，適合 enterprise proxy / audit / policy 類整合。

---

## Gemini CLI

### v0.43.0 · 2026-05-22（[release](https://github.com/google-gemini/gemini-cli/releases/tag/v0.43.0)）

> **繁中摘要**：Gemini CLI v0.43.0 是穩定版更新，包含 edit tool 使用引導、Auto Memory / skills 文件、YOLO / AUTO_EDIT redirect 修正與 macOS binaries 產物調整。

**變更重點**

- Core prompt / steering 改善，讓模型更傾向使用 edit tool 做精準修改。
- 文件澄清 Auto Memory 會提出 memory updates 與 skills。
- 修正 `GOOGLE_CLOUD_PROJECT` numeric project ID 處理。
- 修正 YOLO 與 AUTO_EDIT modes 下 redirection / sandboxing 相關行為。
- Release 流程建置並附上 unsigned macOS binaries。

**實務影響**

- Edit tool steering 會影響 Gemini CLI 的實際改檔行為，對避免粗暴重寫有幫助。
- Auto Memory / skills 文件更新顯示 Gemini CLI 也在把可遷移 skill 與記憶工作流產品化。
- YOLO / AUTO_EDIT redirect 修正影響高自動化權限模式下的 shell 行為，升級後應重跑幾個常用自動編輯流程。

---

## opencode

### v1.15.7 · 2026-05-21（[release](https://github.com/anomalyco/opencode/releases/tag/v1.15.7)）

> **繁中摘要**：opencode v1.15.7 增加 Grok OAuth sign-in，補強 v2 session API error safety，並修復 Codex / OpenAI OAuth refresh 與 tool schema error 呈現。

**變更重點**

- 新增 Grok OAuth sign-in，包含 device-code login。
- v2 session APIs 對 corrupted stored messages 回傳 safe `UnknownError` 與 log reference IDs，不再暴露 server config。
- v2 API 針對尚不可用 mutation、missing session、generic unknown errors 提供更具體且安全的錯誤型別。
- Deduped concurrent Codex OAuth refresh，避免重複 refresh failures。
- Restored native OpenAI OAuth requests。
- Tool schema failures 會呈現為較友善的 tool errors。
- 新增 Grok PDF attachment support。

**實務影響**

- opencode 的 auth surface 繼續擴張，且 OpenAI / Codex OAuth refresh 更穩。
- v2 API error schema 更適合被外部 client 或 automation 可靠處理。
- Tool schema error 變友善後，plugin / provider integration debugging 會比較容易定位。
