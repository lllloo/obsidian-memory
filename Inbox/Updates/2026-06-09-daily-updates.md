---
title: "2026-06-09 Daily Updates"
created: 2026-06-09
updated: 2026-06-09
tags:
  - updates
  - claude-code
---

## Claude Code

### v2.1.169 · 2026-06-08（[2.1.169](https://code.claude.com/docs/en/changelog#21169)）

> **繁中摘要**：新增 `--safe-mode`、`/cd` 指令、`disableBundledSkills` 設定；修復企業 MCP 策略執行漏洞、Windows `claude -p` hang（2.1.161 regression）、macOS 首 turn UI stall，並改善 CPU 使用率與 TaskCreate 可靠性。

**變更重點**
- **`--safe-mode` / `CLAUDE_CODE_SAFE_MODE`**：啟動時停用所有客製化（CLAUDE.md、plugins、skills、hooks、MCP servers），用於疑難排解
- **`/cd` 指令**：在 session 中移動工作目錄而不中斷 prompt cache
- **`disableBundledSkills` / `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`**：隱藏內建 skills、workflows、slash commands，讓 model 不看到這些
- **`/workflows` 即時開啟**：即使 turn 正在進行中也能立即開啟
- **`TaskCreate` 可靠性**：malformed inputs 自動修復，validation error 附帶 schema
- **Vertex/Foundry idle timeout 恢復**：預設 5 分鐘閒置超時防 stream hang；可設 `API_FORCE_IDLE_TIMEOUT=0` 關閉
- **Remote-managed settings 部分無效修復**：有無效 entry 時仍套用剩餘有效 policies 並回報錯誤（之前整包丟棄）

**Bug fixes（影響日常使用者）**
- 修正企業 managed MCP policies（`allowedMcpServers`/`deniedMcpServers`）在 reconnect、IDE config、`--mcp-config`、cold start 時未被執行
- 修正 macOS claude.ai 登入用戶每 turn 開始時 ~30-50ms UI stall
- 修正 Windows 上 `claude -p` 慢/hang（2.1.161 regression，slash-command/skill 掃描）
- 修正 Remote Control 在 OAuth token refresh 同時 resume session 後卡在 "reconnecting"
- 修正 Windows 啟動時 Git Credential Manager "Connect to GitHub" popup 意外出現
- 修正 custom statusline 用戶看不到 footer hints（如 "esc to interrupt"）
- 修正重新 attach 到已死 remote session 時 stale permission/dialog prompts 反覆出現
- 修正 `claude agents --json` 遺漏 blocked 和剛 dispatch 的 session；新增 `--all` flag 含完成 session
- 修正 background agents 忽略 project-level `env` 設定（如 `ANTHROPIC_MODEL`）

**實務影響**
- `--safe-mode` 對 debug CLAUDE.md / hook 衝突問題的使用者直接有用，不需手動停用各設定
- 企業環境 managed MCP policy 漏洞修復屬安全性補丁，managed Claude Code 部署應儘速升級
- Vertex/Foundry 用戶若曾遇到 stream hang，5 分鐘 idle timeout 恢復後可減少卡死問題

**待追蹤**
- `disableBundledSkills` 與現有 MCPB plugin 的交互行為尚無文件說明

---

### v2.1.161 · 2026-06-02（[2.1.161](https://code.claude.com/docs/en/changelog#21161)）

> **繁中摘要**：改善 multi-agent 並行工具可靠性（failed Bash 不再取消同批其他工具）、OpenTelemetry 自訂標籤支援、Linux clipboard 行為，並修復多個 managed settings、Windows hooks 與 background session 問題。

**變更重點**
- **`OTEL_RESOURCE_ATTRIBUTES` 支援**：值作為 metric datapoints 的 labels，可依 team/repo 等自訂維度切片 usage metrics
- **並行工具改善**：同批次中 Bash 失敗不再取消其他並行 tool call，各自獨立回傳結果
- **`claude agents` rows 顯示 done/total**：fan-out 任務顯示進度；peek 顯示最長執行項目
- **`/mcp` 收折未使用 claude.ai connectors**：從未登入的 connector 收在 "Show unused connectors" 後，減少雜訊
- **Linux fullscreen clipboard**：優先使用 `wl-copy`/`xclip`/`xsel`，同時複製到 clipboard 和 PRIMARY selection（支援 middle-click paste）

**Bug fixes（影響日常使用者）**
- 修正 `forceLoginOrgUUID`/`forceLoginMethod` managed settings 誤擋 Bedrock/Vertex/Foundry session（2.1.146 regression）
- 修正 Windows hooks 顯式呼叫 bash（如 `/usr/bin/bash script.sh`）時 "command not found"
- 修正 `claude mcp` list/get/add 將 secrets 印到 terminal（`${VAR}` 不再展開，credential headers 和 URL secrets 遮蔽）
- 修正 OpenTelemetry log events 在 telemetry 初始化完成前發出時被靜默丟棄
- 修正 Workflow agents 在 background session 中使用 `isolation: "worktree"` 時被擋無法編輯 worktree 內檔案
- 修正 background session dispatch 使用 daemon 環境的舊 model，而非 `settings.json` 中的 model

**實務影響**
- Bedrock/Vertex/Foundry 用戶若升級 2.1.146 後 org pin managed settings 出現問題，2.1.161 修復（regression fix）
- `claude mcp` 印出 secrets 的安全問題修復，shared terminal 環境中操作 MCP 設定時更安全
- `OTEL_RESOURCE_ATTRIBUTES` 讓有 observability pipeline 的企業可依 team/repo 細分 Claude Code 用量
- 多工具並行（如同時跑多個 Bash 命令）不再因一個失敗而全體取消，agent automation 更可靠

---
