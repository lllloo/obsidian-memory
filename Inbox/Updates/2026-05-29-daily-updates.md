---
title: "2026-05-29 Daily Updates"
created: 2026-05-29
updated: 2026-05-29
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.154 · 2026-05-28（[Release Notes](https://code.claude.com/docs/en/changelog)）

> **繁中摘要**：Claude Opus 4.8 正式推出並成為預設高品質選項，同時引入 Dynamic Workflows（背景多 agent 協作）、Fast mode 大幅降價，以及多項 CLI/MCP/plugin 改善。

**變更重點**

- **Opus 4.8 GA**：成為預設 high effort 模型；`/effort xhigh` 可指定最高品質
- **Dynamic Workflows**：可要求 Claude 建立 workflow，在背景協調數十到數百個 agent 平行執行大型任務；`/workflows` 查看執行狀態
- **Fast mode on Opus 4.8**：現為 standard rate 的 2 倍（過去遠更高），速度為 standard 的 2.5 倍
- **Lean system prompt 成預設**：適用所有模型（Haiku、Sonnet、Opus 4.7 及更早版本除外）
- **`/simplify` 重新定位**：改為只跑 cleanup-only review（reuse、simplification、efficiency、altitude），不再觸發完整 bug-hunting code review
- **背景 shell 指令**：`claude agents` 中輸入 `! <command>` 可在背景 session 執行 shell 指令並可 attach/detach；也可用 `claude --bg --exec '<command>'`
- **Plugin 預設停用**：plugin 可在 `plugin.json` 宣告 `defaultEnabled: false`，用 `/plugin` 啟用；已啟用 plugin 的 dependency 仍自動啟用
- **Streaming tool execution**：現在永遠啟用，包含停用 telemetry 或在 Bedrock/Vertex/Foundry 環境
- **Stdio MCP server**：子行程現在會取得 `CLAUDE_CODE_SESSION_ID` 與 `CLAUDECODE=1` 環境變數
- `claude mcp list`/`get` 對未核准的 `.mcp.json` server 顯示 `⏸ Pending approval`
- 廢棄 `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE`（06/01 移除）；改用 `/model claude-opus-4-6[1m]` + `/fast on`

**實務影響**

- 使用 Opus 4.8 的 session 效能與成本比前代 Fast mode 更划算，可考慮升級預設模型
- Dynamic Workflows 讓複雜的多步驟任務可以完全後台化，不需要人在旁守候
- `/simplify` 行為改變：若期望同時修 bug，需明確呼叫 `/code-review --fix`
- Stdio MCP server 開發者：`CLAUDE_CODE_SESSION_ID` 可用於 session 識別或 audit log

---

### v2.1.153 · 2026-05-28（[Release Notes](https://code.claude.com/docs/en/changelog)）

> **繁中摘要**：多項 agent、MCP、背景 session bug 修復，以及 `/model` 新增儲存預設功能；修正 `subagent_type: 'claude'` 在暫時 worktree 執行導致輸出遺失的問題。

**變更重點**

- **`/model` 儲存預設**：選擇模型後成為新 session 預設；按 `s` 可只套用到當前 session
- **`skipLfs` 選項**：`github`/`git` plugin marketplace source 可跳過 Git LFS 下載
- **Status line 指令**：現可取得 `COLUMNS` 與 `LINES` 環境變數，讓腳本按終端寬度調整輸出
- **`claude agents` dispatch 自動完成**：現在建議 native slash commands 與 bundled skills
- **修復 `subagent_type: 'claude'` worktree bug**：`Agent` tool 不再在未記錄的暫時 worktree 中執行，避免寫入 gitignored 路徑時輸出靜默遺失
- 修復 stateful MCP server 在沒有 optional GET SSE stream 時的重連迴圈
- 修復自訂 API gateway 收到使用者 Anthropic OAuth token 而非 gateway 自身 token 的回歸
- 修復 subagent 的 frontmatter MCP server 忽略 `--strict-mcp-config` 等政策設定
- 修復 Windows 更新失敗時顯示通用錯誤而非指導訊息
- 修復高記憶體使用：以檔案路徑恢復大量 session 時可能耗用數 GB

**實務影響**

- 使用 `Agent` tool + `subagent_type: 'claude'` 的 workflow：升級後 gitignored 路徑輸出不再靜默丟失，行為更可預期
- MCP server 開發者：strict-mcp-config 現在正確套用到 subagent frontmatter MCP server
- status line 腳本可用 `$COLUMNS`/`$LINES` 做響應式輸出

---

## OpenAI Codex

### v0.135.0 · 2026-05-28（[GitHub Release](https://github.com/openai/codex/releases/tag/rust-v0.135.0)）

> **繁中摘要**：Codex CLI 0.135.0 強化診斷工具、遠端連線狀態顯示、Vim mode 文字物件編輯，以及 `/permissions` 支援命名 profile。

**變更重點**

- **`codex doctor` 增強**：回報更豐富的 environment、Git、terminal、app-server 與 thread inventory 診斷資訊，便於 support 排查
- **`/status` 遠端資訊**：TUI 透過遠端 transport 連線時，顯示 remote connection details 與 server version
- **Vim mode 改善**：新增 text-object 編輯（如 `ciw`、`da"`）、改善 word/line-end 行為、可設定 interrupt-turn binding
- **`/permissions` 支援 named profile**：顯示已設定的 custom profile，方便多情境切換
- **Python SDK `Sandbox` presets**：thread 與 turn API 提供友善的 `Sandbox` preset 物件

**實務影響**

- Vim mode 使用者：text-object 編輯大幅提升 in-editor 效率，可直接用 `ci"`、`daw` 等
- Remote transport 使用者：`/status` 現可確認連線的 server 版本，有助診斷版本不相容問題
- 以 Python SDK 建立 Codex workflow 的開發者：`Sandbox` presets 簡化沙箱設定

---

## GitHub Changelog

### 2026-05-28（[Claude Opus 4.8 正式上線於 GitHub Copilot](https://github.blog/changelog/2026-05-28-claude-opus-4-8-is-generally-available-for-github-copilot)）

> **繁中摘要**：Anthropic Claude Opus 4.8 現已在 GitHub Copilot 正式上線，GitHub 內部測試顯示程式碼理解與生成能力有明顯提升。

**變更重點**

- Claude Opus 4.8 在 GitHub Copilot 進入 GA（General Availability）
- 根據 GitHub 早期測試，Opus 4.8 在程式碼理解與生成上較前代有明顯進步

**實務影響**

- Copilot 使用者可在模型選擇器切換至 Opus 4.8 取得更高品質的程式碼補全與對話
- 適合需要深度程式碼理解的複雜任務（大型 refactor、跨檔案分析）
