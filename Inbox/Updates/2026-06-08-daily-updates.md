---
title: "2026-06-08 Daily Updates"
created: 2026-06-08
updated: 2026-06-08
tags:
  - updates
  - claude-code
  - codex
---

## Claude Code

### v2.1.166 · 2026-06-06（[2.1.166](https://code.claude.com/docs/en/changelog#21166)）

> **繁中摘要**：此版本帶來多項影響 agent 穩定性與安全性的重大變更：fallback model 機制、cross-session messaging 安全強化、thinking token 控制，以及大量關鍵 bug fix。

**變更重點**
- **`fallbackModel` 設定**：可設定最多三個備援模型，primary model 過載或不可用時依序嘗試；`--fallback-model` 現在也適用於互動式 session
- **Glob 支援 deny rules**：tool-name 位置支援 glob pattern，`"*"` 可封鎖所有工具；allow rules 拒絕非 MCP glob；未知工具名稱在 deny rules 中會於啟動時警告
- **Cross-session messaging 安全強化**：透過 `SendMessage` 從其他 Claude session 轉發的訊息不再帶有 user authority，接收方拒絕轉發的 permission 請求，auto mode 也會封鎖
- **Thinking 停用控制**：`MAX_THINKING_TOKENS=0`、`--thinking disabled`、以及 per-model thinking toggle 現在可在預設啟用 thinking 的模型上停用（第三方 provider 不受影響）
- **自動 fallback 重試**：API 回傳非預期 non-retryable error 時自動在 fallback model 重試一次；auth、rate-limit、request-size、transport error 仍立即浮現
- **`claude update` 改善**：下載前先顯示目標版本，不再無聲無息

**Bug fixes（影響日常使用者）**
- 修正 JetBrains IDE（IntelliJ、PyCharm、WebStorm）2026.1+ terminal 閃爍
- 修正 Kitty keyboard protocol（WezTerm、Ghostty、kitty）下 Shift+非 ASCII 字元被吞（如 Shift+ä → Ä）
- 修正 macOS 上 daemon 死亡後 `claude --bg-pty-host` 行程 100% CPU 空轉
- 修正 remote session 在 worker 啟動期間後端短暫中斷後永久卡死
- 修正 voice mode 切換 `/voice` 後需要 `/login` 才能清除過期 auth 狀態
- 修正 managed settings 有無效 entry 時，其餘有效 policy 被靜默關閉
- 修正 managed-settings `allowedMcpServers`/`deniedMcpServers` 使用 `${VAR}` 參照時無法匹配
- 修正 background agent session 進入 git worktree 後重新開啟時 crash-loop "No conversation found"
- 修正 Windows PowerShell command validation 偶發性遠超時限的 hang

**實務影響**
- `fallbackModel` 對 rate-limit 頻繁命中的使用者（尤其 Opus 4 用戶）影響最大，可降低任務中斷率
- Cross-session security 強化：multi-agent 架構中 sub-agent 透過 `SendMessage` 升級自身權限的攻擊路徑被關閉，屬重要安全修補
- Thinking 停用控制改善 token budget 管理，適合 agent automation 場景
- JetBrains + Kitty 系 terminal 使用者可直接受益於 bug fix，無需額外設定

**待追蹤**
- `fallbackModel` 與第三方 provider（Bedrock/Vertex）的交互行為尚未在 changelog 中說明，需測試

---

### v2.1.163 · 2026-06-04（[2.1.163](https://code.claude.com/docs/en/changelog#21163)）

> **繁中摘要**：此版本強化 managed settings 版本管控、新增 plugin/skill 管理指令，並修復多個影響 CI、Bedrock/Vertex、Windows、macOS 使用者的重要 bug。

**變更重點**
- **版本範圍管控**：`requiredMinimumVersion` / `requiredMaximumVersion` managed settings — 版本不在允許範圍時 Claude Code 拒絕啟動並引導至核准版本；適合企業環境強制版本一致性
- **`/plugin list` 指令**：列出已安裝 plugin，支援 `--enabled`/`--disabled` 過濾
- **`/btw` 新增 "c to copy" 捷徑**：將 raw markdown 答案複製到剪貼簿，貼出時保留格式
- **Hooks 改善**：Stop 和 SubagentStop hooks 現在可回傳 `hookSpecificOutput.additionalContext`，讓 Claude 持續該 turn 而不被標記為 hook error
- **Skills `\$` escape**：指令 body 中可用 `\$` 在數字前插入字面 `$`，修正變數展開衝突
- **stdio MCP servers**：`--resume` 時收到與 hooks/Bash 相同的 `CLAUDE_CODE_SESSION_ID`

**Bug fixes（影響日常使用者）**
- 修正 `claude -p` 最終結果輸出後永久 hang（因 background command 從未退出）
- 修正 Bedrock/Vertex/Foundry 且 `CI=true`、無 Anthropic API key 時 `claude -p` 報 "ANTHROPIC_API_KEY required" 失敗
- 修正 bazel / EDR-protected Go workflow 下 `$TMPDIR` 被覆寫至 `/tmp/claude-{uid}` 導致 Bash 指令失敗（2.1.154 regression）
- 修正 Windows OneDrive 或唯讀屬性目錄下 session-env 目錄 "EEXIST" 失敗
- 修正 org-managed permission rules 在 fresh config 目錄啟動時未完整套用
- 修正 hook `if: "Bash(...)"` 條件在含 `$()` 或 `$VAR` 的 Bash 指令上誤觸發
- 修正 deny rules 對 `~/` 路徑使用 `$HOME` 展開時未封鎖
- Background agent sessions 現在在背景更新至新版，重新開啟不需等待 cold restart

**實務影響**
- Bedrock/Vertex CI pipeline 的 `claude -p` 使用者應儘速升級，此 bug 會導致 CI 完全失敗
- Bazel / Go EDR workflow 使用者的 `$TMPDIR` 問題是 2.1.154 regression，2.1.163 修復
- Hooks 作者現在可以讓 Stop/SubagentStop hook 回傳 context 繼續對話，不再只能中止
- 企業管理員可透過 `requiredMinimumVersion`/`requiredMaximumVersion` 強制所有使用者在核准版本範圍內

**待追蹤**
- `requiredMinimumVersion`/`requiredMaximumVersion` 的 MDM 部署與 managed settings 文件尚待補充

---

## OpenAI Codex

### v1.2026.146 · 2026-06-02（[ChatGPT for iOS 1.2026.146](https://developers.openai.com/codex/changelog#chatgpt-for-ios-12026146)）

> **繁中摘要**：iOS 版 Codex 新增 Face ID/密碼鎖、SSH Windows 支援與跟進行為預設值設定，涉及安全性與跨平台使用情境。

**變更重點**
- 可選擇性啟用 Face ID / 密碼鎖保護 Codex 存取
- 新增設定項：跟進行為（follow-up）的預設值
- 支援 Windows 機器的 SSH 連線
- 支援 `/side` 指令
- 改善跟進提示（follow-up prompts）體驗

**實務影響**
- 在 iOS 上使用 Codex 操作敏感 repo 時可加上生物辨識鎖，降低裝置遺失風險
- Windows 使用者現在可以透過 iOS 端 SSH 連進機器，擴展遠端 agent workflow 的行動端入口
- `/side` 指令可在 iOS 端使用，與桌面端操作習慣更一致

---

### 26.601 · 2026-06-01（[Terminal placement controls 26.601](https://developers.openai.com/codex/changelog#terminal-placement-controls-26601)）

> **繁中摘要**：新增 Terminal 預設位置設定，可選擇捷徑開啟時使用底部或右側面板，影響日常 terminal 操作佈局偏好。

**變更重點**
- 在 General preferences 新增「Default terminal location」設定
- 可選擇 terminal 捷徑開啟時預設放在底部（bottom）或右側（right）面板

**實務影響**
- 使用多面板佈局的開發者可固定 terminal 位置，減少手動調整面板的摩擦

---
