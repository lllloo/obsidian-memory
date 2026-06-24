---
title: "2026-06-24 Daily Updates"
created: 2026-06-24
updated: 2026-06-24
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.187 · 2026-06-23（[Changelog](https://code.claude.com/docs/en/changelog#2-1-187)）

**繁中摘要**：本版補上 sandbox 讀取憑證的防線、開放 org 層級限制可選 model，並把卡死已久的 remote MCP 呼叫改成直接報錯，是安全性與穩定性都有感的維護版。

- **`sandbox.credentials` 設定**：可封鎖 sandboxed 指令讀取憑證檔與 secret 環境變數，縮小 agent 在沙箱內外洩金鑰的面。
- **Org 層級 model 限制**：管理者設定的 model 白名單會套用到 model picker、`--model`、`/model` 與 `ANTHROPIC_MODEL`，企業可統一控管可用模型。
- **Remote MCP 呼叫不再卡死**：remote MCP tool call 改為逾時直接 abort 報錯，不再無限期 block 整個 session。
- **`/install-github-app` 可略過 Actions 設定**：GitHub Actions workflow 設定改為選用，只想裝 app 不必被迫配置 CI。
- **結構化輸出修復**：修好 `--json-schema` 與 workflow `agent({schema})` 的 structured output 問題；另修 `--resume` 在原 `-p` 無 model turn 時報「No conversation found」。
- **其他**：修復終端機貼上韓文／CJK 變亂碼、`/update` 經 Remote Control 卡住、背景任務永遠停在「working」等多項問題。

---

## OpenAI Codex

### Codex CLI 0.142.0 · 2026-06-22（[Changelog](https://developers.openai.com/codex/changelog#codex-cli-01420)）

**繁中摘要**：0.142.0 把用量管理（reset credits、token budget）與多 agent 委派設定做細，並加上受限的 indexed web-search 模式，適合跑長任務、管成本的重度用戶注意。

- **`/usage` 可兌換 reset credits**：除了顯示用量，現在能直接兌換 usage-limit 重置額度。
- **`/plugins` 分區**：remote plugins 改分成 curated / workspace / shared 三區，較好挑選。
- **Rollout token budget**：可設定 token 預算並跨 agent thread 追蹤用量，利於成本控管。
- **多 agent 委派設定**：可在 thread 與單回合（turn）層級各自設定 multi-agent delegation。
- **Indexed web-search 模式**：新增以 server 核准 URL 為限的索引式 web search，收斂搜尋來源範圍。
- **其他**：修復 Linux TUI 渲染、exec-server 斷線與 remote 環境問題，並透過 DNS 優化與平行載入 skill 降低啟動／session 延遲。

---

## GitHub Copilot

### 2026-06-23（[Copilot CLI: New terminal interface is generally available](https://github.blog/changelog/2026-06-23-copilot-cli-new-terminal-interface-is-generally-available)）

**繁中摘要**：Copilot CLI 在 MS Build 2026 預覽的新終端介面正式 GA，帶來分頁式版面與一系列引導式設定指令，把 GitHub 工作流（issues / PR / gists）直接搬進終端機。

- **分頁式版面**：互動 session 頂端顯示 Session、Gists、Issues、Pull Requests 分頁（在 repo 內時），不離開終端就能切換到關注的工作；`Tab` 切分頁、`c` 引用項目、`o` 開瀏覽器。
- **引導式工具設定**：`/mcp add`、`/mcp search` 設定 MCP server，`/skills` 切換 skill，`/plugin` 管 marketplace/repo plugin，`/settings` 內嵌檢視設定，免再手改設定檔。
- **無障礙與自適應**：`/theme` 提供 default／dim／high-contrast／colorblind 主題並自動支援螢幕報讀；窄終端機下版面自適應不截斷內容。
- **GA 意義**：可用 `copilot update` 更新，這套介面成為正式預設體驗而非預覽。

### 2026-06-23（[GitHub Copilot app support for BYOK](https://github.blog/changelog/2026-06-23-github-copilot-app-support-for-byok)）

**繁中摘要**：Copilot app 開放 bring your own key，可用自己的 model provider 跑 agent session，沿用既有計費、配額與資料落地條款，並能混搭 frontier 與本地模型。

- **支援多家 provider**：OpenAI、Azure OpenAI、Microsoft Foundry、Anthropic、LM Studio、Ollama，以及任何 OpenAI 相容端點。
- **設定方式**：Settings → Model Providers 填入 endpoint 與 API key；金鑰存於本機 OS keychain、UI 不會回讀；你的 model 會與 Copilot 託管 model 一起出現在 picker。
- **使用情境**：維持與 provider 的既有計費／配額／區域資料條款，把推論導向自有基礎設施以符合企業資料邊界；可用 frontier model 處理複雜、本地 model 跑執行。
- **限制**：Business / Enterprise 方案需 org/enterprise 管理者在 policy 啟用 Copilot CLI；且需下載 GitHub Copilot app 才能使用。

---
