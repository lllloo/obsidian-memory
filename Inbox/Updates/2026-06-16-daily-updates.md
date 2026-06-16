---
title: "2026-06-16 Daily Updates"
created: 2026-06-16
updated: 2026-06-16
tags:
  - updates
  - claude-code
  - codex
---

## Claude Code

### v2.1.178 · 2026-06-15（[Changelog](https://code.claude.com/docs/en/changelog#21178)）

**繁中摘要**：本版強化了 permission rule 語法與 nested `.claude/` 目錄的解析邏輯，並補上 auto mode 分類器在 subagent 啟動前的審查缺口，是安全與工作流程都有實質影響的版本。

- **Tool(param:value) permission 語法**：permission rule 現在支援比對 tool 輸入參數，例如 `Agent(model:opus)` 可封鎖 Opus subagent，`*` 為萬用字元；能更精細控制 agent 行為。
- **Nested skills 載入**：在子目錄工作時，該目錄下的 `.claude/skills/` 會自動載入；名稱衝突時以 `<dir>:<name>` 格式共存，不再互蓋。
- **Nested `.claude/` 目錄優先序**：agent、workflow、output-style 統一由「最近的 `.claude/`」決定；project-scope workflow 也儲存到最近的 `.claude/workflows/`，多專案巢狀設定更可預測。
- **Auto mode 安全補丁**：subagent 啟動前現在先過 classifier，補上原本 subagent 可在未審查下觸發封鎖動作的缺口。
- **Workflow 觸發改為精確詞組**：紫色 shimmer 高亮僅在明確說出「run a workflow」或「workflow:」時啟動，不再被任何提及 "workflow" 的句子誤觸發。
- **`/bug` 強制填描述**：送出前必須有說明文字，且不再以模型拒絕回應當 issue 標題；另修復多項 crash、vim undo、MCP 設定 bug。

---

## OpenAI Codex

### v0.140.0 · 2026-06-15（[Changelog](https://developers.openai.com/codex/changelog#codex-cli-01400)）

**繁中摘要**：Codex CLI 0.140.0 新增 token 用量視圖與 Bedrock managed auth，並首次提供 Claude Code 設定匯入功能，適合同時使用兩套工具的用戶注意。

- **Token 用量視圖**：可直接在 CLI 查看 token 使用活動，有助成本監控。
- **Claude Code 設定匯入**：新增 import 功能，可將 Claude Code 現有設定帶入 Codex CLI，降低雙工具切換的設定成本。
- **Unified @ mentions menu**：統一以 `@` 符號呼叫 mentions，操作更一致。
- **Managed Bedrock API-key 驗證**：支援 managed Bedrock 認證方式，企業用戶可直接對接。
- **永久刪除 session（含防護）**：可徹底刪除 session 紀錄，並有確認防護避免誤刪。
- **Bug fixes**：修復 SQLite 資料庫損毀回復、review crash、MCP 穩定性、plugin 管理與背景指令中斷處理。

---
