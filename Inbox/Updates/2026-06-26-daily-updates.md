---
title: "2026-06-26 Daily Updates"
created: 2026-06-26
updated: 2026-06-26
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.191 · 2026-06-24（[Changelog](https://code.claude.com/docs/en/changelog#2-1-191)）

**繁中摘要**：以效能與可靠性為主的一版——streaming CPU 用量大降、MCP 對暫時性網路錯誤改為重試，並補上 `/rewind` 跨 `/clear` 復原與 sandbox 網路權限記憶。

- **`/rewind` 跨 `/clear`**：可從執行 `/clear` 之前的點恢復對話，誤清不再無法挽回。
- **streaming CPU 降約 37%**：把 text update 合併到 100ms 批次，並減少長 session 的終端輸出快取記憶體成長。
- **MCP 可靠性**：capability discovery（`tools/list` 等）與 OAuth 對暫時性網路錯誤改為短 backoff 重試；headless 環境 OAuth 直接走貼 URL 流程不再彈瀏覽器。
- **sandbox 網路權限記憶**：用「Yes」放行的 host 整個 session 記住，不再每次連線重問。
- **修正 background agent 復活**：從 tasks 面板停止 agent 現在永久生效，不會被重新喚起。
- **修正 hooks 逗號 matcher**：`"Bash,PowerShell"` 這類逗號分隔 matcher 過去靜默不觸發，已修復。

---

## OpenAI Codex

### Codex CLI 0.142.2 · 2026-06-25（[Changelog](https://developers.openai.com/codex/changelog#codex-cli-01422)）

**繁中摘要**：Codex Remote 正式 GA，可從 ChatGPT 手機 app 控制已連線的桌機 host；CLI 同步多項預設與相容性調整。

- **Codex Remote GA**：在 ChatGPT 手機 app 控制連線的 Mac/Windows host、審閱進度並核准動作，裝置間用認證 QR 配對；新增 DigitalOcean plugin 供遠端 workspace 佈建與 SSH 設定。
- **CLI 預設變更**：MCP tools 預設改用 tool search、新增 macOS 系統 proxy 支援、dark-mode plugin logo 與 safety-buffering UI。
- **修正**：remote plugin catalog、過期憑證、MCP server 接受絕對路徑、PowerShell safety check 等。

### Codex CLI 0.142.1 · 2026-06-25（[Changelog](https://developers.openai.com/codex/changelog#codex-cli-01421)）

**繁中摘要**：補上 Windows 系統 proxy 支援，讓驗證流程能走企業網路。

- **Windows 系統 proxy（opt-in）**：驗證支援 PAC、WPAD、靜態 proxy 與 bypass 規則，相容企業網路環境。

---

## GitHub Copilot

### 2026-06-25（[Copilot code review：分析深度與效率更新](https://github.blog/changelog/2026-06-25-copilot-code-review-analysis-depth-and-efficiency-updates)）

**繁中摘要**：Copilot code review 改用內建檔案探索工具，成本降約 20% 而品質不變；Medium 分析深度 preview 增加透明度與 org 層級設定。

- **改用 CLI 探索工具**：以內建 `grep`、`rg`、`glob`、`view` 取代自訂工具，code review 成本約降 20%、審閱品質維持不變。
- **Medium 分析深度 preview**：PR overview 留言會標注「Medium」來源；org 可設跨 repo 的預設審閱等級，個別 repo 仍可覆寫。

### 2026-06-25（[Enterprise-managed settings 支援 strictKnownMarketplaces](https://github.blog/changelog/2026-06-25-enterprise-managed-settings-now-support-strictknownmarketplaces-in-vs-code-and-the-cli)）

**繁中摘要**：企業可限制 Copilot CLI 與 VS Code 只能從核准過的 marketplace 安裝 plugin，屬執行前的治理控管（public preview）。

- **strictKnownMarketplaces**：寫進 enterprise-managed `settings.json` 後，Copilot 只允許從明確定義的 marketplace 安裝 plugin；Copilot Business/Enterprise 授權的使用者會自動套用此政策，防止安裝未受信任的 plugin。

### 2026-06-25（[GitHub Copilot for Jira 正式 GA](https://github.blog/changelog/2026-06-25-github-copilot-for-jira-is-now-generally-available)）

**繁中摘要**：在 Jira 內直接驅動 coding agent，免在工具間切換；GA 強化即時進度與會後追加指令。

- **即時可見性**：可在 Jira issue 內即時看 coding agent 進度，狀態回流到 ticket。
- **會後 steering**：agent 產出 draft PR 後，可在 Jira chat 面板追加指令，把變更收斂進同一個 PR 而非開多個。
- **簡化 setup**：連接 GitHub org 與 repo 的設定步驟減少。
