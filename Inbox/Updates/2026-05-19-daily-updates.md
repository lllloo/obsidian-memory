---
title: "2026-05-19 Daily Updates"
created: 2026-05-19
updated: 2026-05-19
tags:
  - updates
  - claude-code
  - codex
  - copilot
  - gemini-cli
  - opencode
  - skills
  - mcp
---

## OpenAI Codex

### v0.131.0（[changelog](https://developers.openai.com/codex/changelog#codex-cli-01310)）

> **繁中摘要**：Codex CLI 0.131.0 是一個偏 workflow / remote / plugin / SDK 的大版更新，重點是 TUI 狀態可視化、unified mentions、plugin sharing / hooks、remote-control 與 Python SDK。

**變更重點**

- TUI 顯示更完整的 session controls、service tier、token usage、permission / approval mode、workspace roots 與 responsive Markdown tables。
- `@` mentions 現在可在同一 picker 搜尋 files、directories、plugins、skills。
- Plugin workflow 新增 marketplace CLI commands、version-aware sharing、share checkout、workspace bucket 顯示與 default-enabled plugin hooks。
- Remote workflow 新增 daemon-managed `codex remote-control`、runtime enable / disable APIs、status reads 與 registry-backed remote environments。
- Python SDK 移到 `openai-codex` / `openai_codex`，加入 generated types、concurrent turn routing、approval modes 與 app-server integration coverage。
- 新增 `codex doctor`，用於收集 runtime、auth、terminal、network、config、local state 診斷資訊。

**實務影響**

- 多工具 / 多 plugin 專案會更依賴 Codex 的內建 discovery 與 plugin metadata，而不是手寫工具清單。
- Remote-control 與 Python SDK 更新代表 Codex 更適合被接進外部 orchestrator、桌面 app 或長時間 runner。
- `codex doctor` 可作為 issue / support 回報前的標準診斷入口。

---

## Claude Code

### v2.1.144（[changelog](https://code.claude.com/docs/en/changelog)）

> **繁中摘要**：Claude Code v2.1.144 主要補強 background sessions、plugin / model 操作、usage credits 文案、終端顯示、MCP 工具列舉與遠端登入穩定性。

**變更重點**

- `/resume` 支援 background sessions；`claude --bg` 或 agent view 啟動的 session 會和 interactive sessions 一起顯示並標記 `bg`。
- Background subagent 完成通知新增 elapsed duration；`/plugin` browse / discover 顯示 plugin 最後更新時間。
- `/model` 改成只影響目前 session，model picker 可用 `d` 設成新 session 預設值。
- `extra usage` 文案改為 `usage credits`，`/extra-usage` 仍相容但新名稱是 `/usage-credits`。
- 修正 API 不可達時 startup 最長卡 75 秒、長 session terminal corruption、VS Code 顯示 glitch、MCP paginated `tools/list` 只取第一頁等問題。
- 修正 background session / agent view 多個 crash、wake、scroll、attach、worktree isolation、Windows terminal 與 custom provider 問題。

**實務影響**

- 長時間 background agent workflow 的 resume、通知、醒來後狀態保留更可靠。
- 同一台機器跑多 session 時，`/model` 不再意外影響其他 session，降低 model 切換造成的混亂。
- MCP server 工具數量多或有 pagination 時，這版可避免工具 silently missing。

### v2.1.143 · 2026-05-15（[changelog](https://code.claude.com/docs/en/changelog)）

> **繁中摘要**：Claude Code v2.1.143 聚焦 plugin dependency、background session 設定保留、worktree isolation、PowerShell、stop hook 與 cleanup safety。

**變更重點**

- `claude plugin disable` 會拒絕停用仍被其他 enabled plugin 依賴的 plugin，並提供 disable-chain hint；`claude plugin enable` 會 force-enable transitive dependencies。
- `/plugin` marketplace browse pane 顯示 projected context cost。
- 新增 `worktree.bgIsolation: "none"`，讓不適合 worktree 的 repo 可讓 background sessions 直接改 working copy。
- Background sessions wake 後保留 model / effort；`/bg` 保留 MCP config、settings、add-dir、plugin-dir、strict MCP config、fallback model 等設定。
- Stop hooks 若連續 block 會在 8 次後警告並結束 turn，避免無限 loop。
- Worktree cleanup 不再於 `git worktree remove` 失敗時 fallback 到 `rm -rf`，降低刪除 gitignored 或未完成檔案的風險。

**實務影響**

- Plugin ecosystem 開始需要考慮 dependency graph，不只是單一 plugin enable / disable。
- Background agent 若要直接改原 working copy，現在有明確 setting 可控；但 repo 要自己承擔 isolation 風險。
- Worktree cleanup safety 對長時間 agent run 很重要，避免背景任務清理時誤刪未追蹤工作。

---

## GitHub Copilot

### 2026-05-18（[One-click fixes for failing Actions with Copilot cloud agent](https://github.blog/changelog/2026-05-18-one-click-fixes-for-failing-actions-with-copilot-cloud-agent)）

> **繁中摘要**：GitHub Actions job 失敗時，Copilot Business / Enterprise 使用者可用 Copilot cloud agent 一鍵嘗試修復。

**變更重點**

- GitHub Actions failed job 頁面新增 `Fix with Copilot` 類型的入口。
- 功能面向 Copilot Business 與 Copilot Enterprise。

**實務影響**

- CI failure triage 會更容易被轉成 agent task，但團隊仍需要 review agent 產出的修補 PR。
- 適合用在 lint、test failure、dependency config 這類可由 cloud agent 自行改檔並驗證的場景。

### 2026-05-18（[Copilot cloud agent: Fast, cost-efficient models for simple tasks](https://github.blog/changelog/2026-05-18-copilot-cloud-agent-fast-cost-efficient-models-for-simple-tasks)）

> **繁中摘要**：Copilot cloud agent model picker 新增偏低成本 / 快速的模型選項，讓簡單任務不一定要用高成本模型處理。

**變更重點**

- Delegating task to Copilot cloud agent 時，可選的 supported models 擴大。
- 新選項定位在 simple tasks 的 speed / cost efficiency。

**實務影響**

- 團隊可以把 low-risk cleanup、簡單修補、文件更新交給便宜模型，把高風險任務留給較強模型。
- 需要重新校準 model policy，避免所有 cloud agent task 都用同一個 expensive default。

### 2026-05-18（[Ask questions in context with Copilot on web](https://github.blog/changelog/2026-05-18-ask%2Dquestions-in-context-with-copilot-on-web)）

> **繁中摘要**：GitHub web 上的 Copilot chat 會以目前正在看的頁面作為 context，降低查 PR、issue、repo 頁面時的 context switching。

**變更重點**

- Copilot chat on the web 會在目前 GitHub page context 中開啟。
- 目標是讓使用者直接針對當前頁面提問。

**實務影響**

- Review PR、看 failing check、查 issue 時，可直接問頁面相關問題。
- 若團隊依賴 GitHub web review，這會讓 Copilot 成為更接近 inline reviewer / navigator 的工具。

### 2026-05-18（[Audit repository Copilot cloud agent configuration via the REST API](https://github.blog/changelog/2026-05-18-audit-repository-copilot-cloud-agent-configuration-via-the-rest-api)）

> **繁中摘要**：GitHub 新增 REST API，可程式化 audit repository 的 Copilot cloud agent configuration，目前是 public preview。

**變更重點**

- 新增取得 repository Copilot cloud agent configuration 的 REST API。
- 目標是讓管理者能檢查 repository-level cloud agent 設定。

**實務影響**

- Enterprise / platform team 可把 Copilot cloud agent 設定納入 compliance audit 或 repo baseline 檢查。
- 對多 repo organization，這比逐一進 UI 檢查更可操作。

### 2026-05-18（[Copilot Spaces API now generally available](https://github.blog/changelog/2026-05-18-copilot-spaces-api-now-generally-available)）

> **繁中摘要**：Copilot Spaces API GA，允許程式化 create、read、update、delete Spaces。

**變更重點**

- Copilot Spaces API 從 preview 進入 generally available。
- 支援從自家 application 或 workflow 管理 Spaces。

**實務影響**

- 可把 team knowledge / project context 的 Spaces 建立與更新接進內部工具。
- 對 agent workflow 來說，Spaces 更容易成為可管理的 context container。

### 2026-05-18（[Remote control for Copilot CLI sessions now generally available on mobile, web, and VS Code](https://github.blog/changelog/2026-05-18-remote-control-for-copilot-cli-sessions-now-generally-available-on-mobile-web-and-vs-code)）

> **繁中摘要**：Copilot CLI sessions 的 remote control 已在 GitHub Mobile、github.com、VS Code 一般可用。

**變更重點**

- 使用者可在 terminal 啟動工作，再從 mobile、web 或 VS Code 遠端推進 session。
- 功能從 preview 走向 GA。

**實務影響**

- Long-running CLI agent task 可以離開本機 terminal 後繼續監看 / 操作。
- 這讓 Copilot CLI 更接近 Claude Code / Codex 類「跨裝置 remote session」工作流。

### 2026-05-17（[GPT-5.3-Codex is now the base model for Copilot Business and Enterprise](https://github.blog/changelog/2026-05-17-gpt-5-3-codex-is-now-the-base-model-for-copilot-business-and-enterprise)）

> **繁中摘要**：GPT-5.3-Codex 成為 Copilot Business / Enterprise organizations 的 base model，取代 GPT-4.1。

**變更重點**

- Copilot Business / Enterprise base model 從 GPT-4.1 改為 GPT-5.3-Codex。
- Base model 會影響 organization 沒有指定其他 premium model 時的預設模型行為。

**實務影響**

- Enterprise 使用者應重新檢查 coding suggestion / chat / fallback 行為是否改變。
- 這也會影響 Copilot usage-based billing 討論中「base model 是否消耗 premium requests」的理解。

---

## GitHub Copilot CLI

### v1.0.49 · 2026-05-19（[release](https://github.com/github/copilot-cli/releases/tag/v1.0.49)）

> **繁中摘要**：Copilot CLI v1.0.49 增加 session search、critique、session id、Alpine 支援，並修正 hook context、CJK / emoji cursor、MCP OAuth token refresh 等日常問題。

**變更重點**

- `postToolUse` hook 的 `additionalContext` 會注入為 system message，不再被 silently discarded。
- 新增 `/chronicle search`，可依 keyword / topic 搜尋所有 session content。
- 新增 `/rubber-duck`，可對 agent 目前工作取得 independent critique。
- 新增 `/session id`，顯示並複製目前 session ID。
- MCP servers 使用 static OAuth clients 時，registration 會正確保存以支援 token refresh。
- 新增 Alpine Linux（musl libc）支援。

**實務影響**

- Hook 與 MCP OAuth 修正會影響進階 automation / enterprise setup 的可靠性。
- `/chronicle search` 與 `/rubber-duck` 讓長 session 回查與自我 review 更像一等功能。

---

## Gemini CLI

### 2026-05-19（[Addressing Antigravity Bans & Reinstating Access](https://github.com/google-gemini/gemini-cli/discussions/20632)）

> **繁中摘要**：Gemini CLI repo discussion 公告，近期 Antigravity ban 連帶影響 Gemini CLI / Gemini Code Assist access；官方表示正在 system-wide automated unban，並調整後端讓 Antigravity enforcement 不再阻擋 Gemini CLI / Code Assist access。

**變更重點**

- 近期帳號中斷與 Antigravity ToS enforcement 有關，且因 backend layer 造成 Gemini CLI / Code Assist 也被擋。
- 公告表示已協調 Antigravity 進行 system-wide automated unban。
- 後端已調整，Antigravity enforcement 不應再阻擋 Gemini CLI 或 Code Assist access。

**實務影響**

- 若 Gemini CLI 出現 403 / permission 類問題，需區分是 Antigravity enforcement、OAuth / subscription 權限，還是 MCP 權限問題。
- 對依賴 Gemini CLI 的 agent workflow，這是 access reliability 與 account policy 風險訊號。

---

## opencode

### v1.15.5 · 2026-05-18（[release](https://github.com/anomalyco/opencode/releases/tag/v1.15.5)）

> **繁中摘要**：opencode v1.15.5 加入 experimental native OpenAI runtime path preview、resume replay，並修正 plugin tools、event subscription、workspace-scoped file references 與 Desktop notifications。

**變更重點**

- Core 新增 native OpenAI runtime path preview experimental flag。
- 新增 `--replay` 與 `--replay-limit`，resume interactive runs 時可顯示近期歷史。
- 修正 plugin tools 使用 `ask` 時 tool calls 無法正確完成。
- 修正 `/event` subscription race 造成的 missed updates。
- TUI 保持 file references scoped to current workspace，並改善 paste / long tool output 顯示。
- Desktop renderer 可發送 desktop notifications。

**實務影響**

- Resume / replay 對長時間 CLI agent session 更實用。
- Workspace-scoped references 與 plugin `ask` 修正會降低多 repo / 多 plugin 工作流的誤觸與卡住風險。

---

## Vercel Skills

### v1.5.7 · 2026-05-14（[release](https://github.com/vercel-labs/skills/releases/tag/v1.5.7)）

> **繁中摘要**：Vercel Skills v1.5.7 支援 v2 well-known skill discovery，修正 symlinked skill directories 與 local folder handling，並把 GitHub token 使用延後到 rate-limit fallback。

**變更重點**

- 支援 v2 well-known skill discovery。
- GitHub token 改為 lazy use，只在 rate-limit fallback 時使用。
- 修正 project-level update 對 local folders 的處理。
- 修正 symlinked skill directories discovery。
- Git clone timeout 提高並允許 override；缺少 git-lfs 時停用 LFS filter 以提高 clone 成功率。

**實務影響**

- 對跨工具 skill discovery 與 local skill folder 管理有直接影響。
- Symlink skill directory 修正對現有 `.agents/skills` / `.claude/skills` 兼容布局有用。

---

## GitHub Spec Kit

### v0.8.11 · 2026-05-15（[release](https://github.com/github/spec-kit/releases/tag/v0.8.11)）

> **繁中摘要**：Spec Kit v0.8.11 主要是 catalog / docs / extension workflow 更新，包含 high-assurance spec workflow 文件、community catalog extensions 與 preset skill description precedence 修正。

**變更重點**

- 新增 high-assurance spec workflow 文件。
- Community catalog 新增 Time Machine extension 與 Architecture Workflow extension。
- 修正 PowerShell template UTF-8 BOM 問題。
- 修正 preset skill description precedence。
- 新增 version feature reporting。

**實務影響**

- 若用 Spec Kit 管理規格驅動開發，可回看 high-assurance workflow 與 Architecture Workflow extension。
- Preset / extension catalog 修正會影響多 preset 或 community extension 的初始化一致性。

---

## BMAD-METHOD

### v6.7.0 · 2026-05-17（[release](https://github.com/bmad-code-org/BMAD-METHOD/releases/tag/v6.7.0)）

> **繁中摘要**：BMAD-METHOD v6.7.0 重建 PRD / Product Brief 為更精簡的 facilitator，新增 bmad-investigate 與 decision-log pattern，偏向把 planning、validation、bug triage 做成更可追蹤的流程。

**變更重點**

- PRD 與 Product Brief 改為 `bmad-prd`、`bmad-brief`，支援 Create / Update / Validate intents。
- 新 PRD validation pipeline 以 quality-rubric synthesis 取代 adversarial reviewer，輸出 HTML 與 markdown reports。
- 新增 `bmad-investigate` skill，用於 bug triage、incident RCA、陌生 code exploration。
- 新增 `.decision-log` pattern，讓 workflow 從開始就追蹤 decisions，方便 continuation 或修改。

**實務影響**

- 對需要嚴格 planning / validation 的 agent workflow，BMAD 開始把 artifacts 與 decisions 做得更可審計。
- `bmad-investigate` 可評估是否納入 bug triage 或 unfamiliar-code exploration 流程。

---

## GSD

### v1.42.3 · 2026-05-16（[release](https://github.com/gsd-build/get-shit-done/releases/tag/v1.42.3)）

> **繁中摘要**：GSD v1.42.3 是 stable hotfix，重點是 Codex CLI 0.130.0+ install routability，避免 `$gsd-*` skills 在 Codex 新版中沒有 routable entrypoints。

**變更重點**

- 修正 Codex CLI 0.130.0+ 下 `npx get-shit-done-cc@latest --codex` 安裝後 `$gsd-*` skills 無法 resolve 的問題。
- Slash formatting 會依 runtime 產生對應 routing shape：Claude 使用 `/gsd-*`，Codex 使用 `$gsd-*`。
- `check.ship-ready` 改用 argv-based subprocess，降低 git refname shell-injection 類風險。
- 新增 `phase_status` field 以 gate phase lifecycle。

**實務影響**

- 若在 Codex 裡裝 GSD，這版是必要 hotfix，否則 skill entrypoint 可能不可用。
- Runtime-aware slash formatting 對同時支援 Claude / Codex 的 skill distribution 有參考價值。
