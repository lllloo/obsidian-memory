---
title: "2026-06-23 Daily Updates"
created: 2026-06-23
updated: 2026-06-23
tags:
  - updates
  - claude-code
  - copilot
---

## Claude Code

### v2.1.186 · 2026-06-22（[Changelog](https://code.claude.com/docs/en/changelog#2-1-186)）

**繁中摘要**：本版把 MCP 認證搬到 CLI（免進互動選單、支援 SSH），並讓 `!` bash 指令預設觸發 Claude 回應、`/review <pr>` 改用與 `/code-review medium` 同一引擎，是日常操作流程有感調整的版本。

- **`claude mcp login/logout <name>`**：可在 CLI 直接認證 MCP server，免開互動選單；`--no-browser` 支援 SSH 無瀏覽器環境。
- **`!` bash 指令自動回應**：執行 `!` 指令後 Claude 預設會接著回應；不想要可設 `"respondToBashCommands": false` 關閉。
- **`/review <pr>` 統一引擎**：改用與 `/code-review medium` 相同的 review 引擎，PR 審查行為與本地一致。
- **背景 subagent 權限提示前移**：背景 subagent 的 permission prompt 改在主 session 顯示並標注是哪個 agent，避免漏看卡住。
- **Retry 上限與看門狗**：`CLAUDE_CODE_MAX_RETRIES` 上限封頂 15；無人值守 session 改用 `CLAUDE_CODE_RETRY_WATCHDOG`。
- **修復睡眠喚醒後串流中斷**：修掉機器喚醒後出現「Content block not found」或 JSON parse 失敗；skill frontmatter 鍵名同時接受 kebab/snake/camel 寫法。

---

## GitHub Copilot

### 2026-06-22（[New features and Claude as agent provider preview in JetBrains IDEs](https://github.blog/changelog/2026-06-22-new-features-and-claude-as-agent-provider-preview-in-jetbrains-ides)）

**繁中摘要**：Copilot 把 Claude 帶進 JetBrains IDE 當可選 agent（public preview），並補上 org/enterprise 統一發布 agent、Copilot CLI 執行中可 queue/steer 訊息等治理與互動改進。

- **Claude 作為 agent provider（JetBrains, preview）**：裝好 Claude Code CLI 並在設定填路徑後，可在 chat panel 切換到 Claude；注意目前以 bypass permissions 模式跑，所有檔案編輯與 tool call 自動核准。
- **Org / Enterprise agents**：管理者可發布一組整理過的 agent，自動對全組織／企業成員可用，方便標準化、可治理的工作流。
- **Copilot CLI 訊息控制**：請求執行中可 queue 後續訊息、中途 steer 改方向，或直接停下送新指令，長任務不必空等。
- **Agent 除錯日誌摘要**：Agent Debug panel 新增 summary view，彙整整個 session 的統計，活動更一目了然。
- **其他**：每回合 AI credits 顯示、`/models` 快速切換 model、local agent picker 新增最近使用 model 區塊，以及多項效能與穩定性修復。

---
