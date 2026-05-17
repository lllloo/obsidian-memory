---
title: "2026-05-14 Daily Updates"
created: 2026-05-14
updated: 2026-05-14
tags:
  - updates
  - claude-code
  - codex
  - copilot
  - gemini-cli
  - opencode
---

## Claude Code

### v2.1.141 · 2026-05-13（[changelog](https://code.claude.com/docs/en/changelog#may-13-2026)）

> **繁中摘要**：Claude Code v2.1.141 加強 hooks、workspace identity federation、agent session 管理與背景 agent 權限行為，也修正多個 Windows、MCP、Remote Control、permission prompt 與 UI edge cases。

**變更重點**

- Hook JSON output 新增 `terminalSequence`，可在沒有 controlling terminal 的情境發出 desktop notifications、window titles、bells。
- 新增 `CLAUDE_CODE_PLUGIN_PREFER_HTTPS`，讓 GitHub plugin source 可用 HTTPS clone，適合沒有 GitHub SSH key 的環境。
- 新增 `ANTHROPIC_WORKSPACE_ID`，workload identity federation 可把 minted token 限縮到特定 workspace。
- `claude agents --cwd <path>` 可用目錄範圍過濾 session list。
- `/feedback` 可附上最近 24 小時或 7 天 sessions，方便回報跨 session issue。
- Rewind menu 新增「Summarize up to here」，可壓縮早期 context、保留近期 turns。
- Background agents 透過 `/bg` 或 `←←` 啟動時會保留目前 permission mode，不再回到 default。
- 修正 Windows daemon status / `/doctor` 遇到 daemon pipe key file locked / unreadable 時只顯示 opaque failure。
- 修正 Remote Control MCP connectors 在 worker session token rotation 後全數 401 的問題。

**實務影響**

- 需要企業 federation、plugin 安裝、background agents 或 Remote Control 的團隊，這版會降低權限與 session 管理的摩擦。
- Hook 可更乾淨地把通知 / title / bell 類 terminal side effects 帶回使用者，不必依賴控制終端。
- Windows 與 Remote Control 使用者可優先升級，尤其是遇到 daemon pipe、image paste、MCP auth 或 token rotation 問題時。

---

## OpenAI Codex

### Latest changelog（[Chrome extension and enterprise governance docs](https://developers.openai.com/codex/changelog)）

> **繁中摘要**：Codex changelog 最新項目補上 Chrome extension 與 enterprise governance 文件更新：Codex 可透過 Chrome extension 在 browser tabs 背景協作，enterprise governance guide 也加入 Analytics dashboard、data export 與 Analytics API endpoints 的說明。

**變更重點**

- 新增 Codex Chrome extension 文件入口，說明 Codex 如何在多個 browser tabs 背景協作。
- 使用者可控制 Codex 能使用哪些網站，瀏覽器操作不會接管使用者整個 browser。
- Enterprise governance guide 補充 Analytics dashboard charts、data export options、enterprise Analytics API endpoints。

**實務影響**

- Local app / web workflow 可把 Chrome extension 視為 Codex browser use 的另一條路徑，但仍需把 site allowlist 當成安全邊界。
- 企業若要追蹤 Codex adoption / usage / review 效果，可以開始對接 Analytics API 或建立 export-based 報表。

---

## GitHub Copilot

### 2026-05-13（[Start Copilot cloud agent tasks via the REST API](https://github.blog/changelog/2026-05-13-start-copilot-cloud-agent-tasks-via-the-rest-api)）

> **繁中摘要**：Copilot Business / Enterprise 使用者現在可透過 Agent tasks REST API 程式化啟動 Copilot cloud agent tasks，讓 cloud agent 更容易接進外部排程、內部工具或自動化流程。

**變更重點**

- Agent tasks REST API 進入 public preview。
- Copilot Business 與 Copilot Enterprise users 可用 API 啟動 Copilot cloud agent tasks。
- 這讓原本 UI-driven 的 cloud agent task 可以被外部系統觸發。

**實務影響**

- 團隊可把 Copilot cloud agent 接進 issue triage、release checklist、internal portal 或 incident workflow。
- 因為 task 啟動變得可程式化，權限、審計、rate limit 與 secrets exposure 要一起納入治理。

### Copilot CLI 1.0.48-0 · 2026-05-13（[release](https://github.com/github/copilot-cli/releases/tag/v1.0.48-0)）

> **繁中摘要**：Copilot CLI 1.0.48-0 改善 `/ask`、skill injection 與 Azure DevOps-only workspace 行為，並修正 prompt/headless mode、cursor positioning、ACP config update 等問題。

**變更重點**

- `/ask` dialog 不再要求它無法接收的 follow-up replies。
- 注入模型的 skill content 不再包含 YAML frontmatter metadata。
- 在 Azure DevOps-only workspace 的 prompt/headless mode 會自動停用內建 `github-mcp-server`，與 interactive mode 行為一致。
- Terminal cursor 會正確落在 input field，而不是 decorative elements。
- ACP clients 在 active model 變更時會收到更新後的 config options。

**實務影響**

- Skill 內容送進模型時更乾淨，減少 frontmatter 對 prompt 的噪音。
- Azure DevOps-only 或 headless automation 使用者可少遇到 GitHub MCP server 被錯誤啟動的情況。
- ACP client / IDE integration 若依賴 active model config，升級後狀態同步會更可靠。

---

## Gemini CLI

### v0.42.0 · 2026-05-12（[changelog](https://geminicli.com/docs/changelogs/)）

> **繁中摘要**：Gemini CLI v0.42.0 加入 Auto Memory Inbox、預設啟用 Gemma 4 models，並改善 Voice Mode 的動畫與 privacy / compliance UX warning。

**變更重點**

- Auto Memory 新增 inbox flow，並採 canonical-patch contract 管理 skill 相關變更。
- Gemini API 使用者預設啟用 Gemma 4 models。
- Voice Mode 加入 wave animations。
- Gemini Live backend 增加 privacy / compliance UX warnings。

**實務影響**

- Gemini CLI 的 memory / skill 管理更接近可審核 patch flow，後續可觀察它和 Codex / Claude skills 的差異。
- 使用 Gemini CLI voice workflow 時，privacy / compliance warning 變得更明確，適合企業環境評估錄音與語音資料風險。

---

## OpenCode

### v1.14.49 · 2026-05-13（[release](https://github.com/anomalyco/opencode/releases/tag/v1.14.49)）

> **繁中摘要**：OpenCode v1.14.49 加入 v2 model / provider listing API、DigitalOcean OAuth / Inference Router support、預設建立 global `opencode.jsonc`，並改善 prompt mentions、patch diff parsing 與 config schema。

**變更重點**

- 新增 v2 model and provider listing API。
- 新增 DigitalOcean OAuth 與 Inference Router support。
- 沒有 config 時會自動建立 global `opencode.jsonc`。
- 預設啟用 `customize-opencode`，並連到完整 schema。
- Prompt 中支援 configured `@mentions` autocomplete。
- Patch diffs 預設解析 fenced Markdown code blocks。
- 修正 provider / model suggestions、permission rule ordering、attachments from custom tools、compaction 後 recent turns 保存等問題。

**實務影響**

- 多 provider / local model workflow 的設定與 discovery 會更順，適合拿來和 Codex / Claude Code 的 provider 與 skill 管理比較。
- Patch diff parsing 與 permission rule 修正會直接影響 agentic coding 的可靠性，尤其是自動套 patch 與 custom tools 的情境。
