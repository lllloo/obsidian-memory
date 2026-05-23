---
title: "2026-05-23 Daily Updates"
created: 2026-05-23
updated: 2026-05-23
tags:
  - updates
  - claude-code
  - copilot
---

## Claude Code

### v2.1.149 · 2026-05-22（[changelog](https://code.claude.com/docs/en/changelog)）

> **繁中摘要**：Claude Code v2.1.149 帶來 `/usage` 分類細項、`/diff` 鍵盤滾動、GFM checkbox 渲染，並修補多個 PowerShell 權限繞過與 git worktree sandbox 邊界問題。

**變更重點**

- `/usage` 新增 per-category 細項：skills、subagents、plugins、每個 MCP server 各自的用量，讓費用來源更可追蹤。
- `/diff` 詳情面板可用鍵盤操作（方向鍵、`j`/`k`、PgUp/PgDn、Space、Home/End）。
- Markdown 輸出正確渲染 GFM task list checkboxes（`- [ ] todo` / `- [x] done`），不再顯示為純子彈點。
- Enterprise：新增 `allowAllClaudeAiMcps` managed setting，可同時載入 claude.ai cloud MCP connectors 與 `managed-mcp.json`。
- 修正 PowerShell 權限繞過：內建 `cd` 函數（`cd..`、`cd\`、`cd~`、`X:`）在未偵測狀態下變更工作目錄，導致後續指令可讀取 workspace 外部。
- 修正 git worktrees 下 sandbox write allowlist 涵蓋整個主 repo 根目錄，而非只有共用 `.git` 目錄（`hooks/` 和 `config` 已被拒絕存取）。
- 修正 PowerShell prefix/wildcard allow rules 未預先核准 native executables 與 scripts。
- 修正 `find` 工具在 macOS 大型目錄樹耗盡 vnode table 導致主機 crash 的問題。
- 修正 `/ultraplan` 與 remote session 建立在工作樹無實際變更時失敗的問題。
- 修正 thinking spinner 在 tool calls 之間維持琥珀色的視覺問題。
- 修正 `/config` 在切換無關設定時錯報 auto-compact 和 theme 假性變更。
- 改善 `/feedback` 報告：現在包含 context compaction 之前的對話，讓長 session 早期問題更容易追查。

**實務影響**

- `/usage` 細項對同時跑多個 MCP server 或大量 skill 的 workflow 是必要的成本觀測工具。
- PowerShell 與 worktree sandbox 修正屬安全層修補，建議 Windows / worktree 使用者盡快升級。
- `find` crash 修正對在大型 monorepo 使用 Bash tool 的人有直接穩定性收益。

---

## GitHub Copilot

### 2026-05-21（[GitHub Copilot for Eclipse is open source](https://github.blog/changelog/2026-05-21-github-copilot-for-eclipse-is-open-source)）

> **繁中摘要**：GitHub Copilot for Eclipse 在 MIT license 下開源，程式碼公開於 github.com/microsoft/copilot-for-eclipse，可看到 inline completions、Next Edit Suggestions、chat、multi-step agents 與 MCP 整合的實作細節。

**變更重點**

- Copilot for Eclipse 程式碼在 MIT license 下開源，社群可提交 bug report、feature request 與 PR。
- 已公開的實作涵蓋：inline code completions、Next Edit Suggestions（NES）、chat interface、multi-step agentic workflows、custom agents、MCP integration、Bring Your Own Key（BYOK）。

**實務影響**

- 對想了解 IDE-level Copilot 實作或建立類似整合的開發者，這是可直接參考的實作範例。
- MCP 整合與 custom agents 的實作公開，有助於理解 GitHub 在 IDE 中如何實現 agent 協定。

### 2026-05-20（[Updates to available models in Copilot on web](https://github.blog/changelog/2026-05-20-updates-to-available-models-in-copilot-on-web)）

> **繁中摘要**：GitHub Copilot Chat on web 移除 Gemini 全系列、GPT-5.2 Codex 與 GPT-5.4 nano，縮減可選模型數量，改以「一致高品質」為由限定更少的穩定模型。

**變更重點**

- Web Copilot Chat 移除：Gemini 全系列模型、GPT-5.2 Codex、GPT-5.4 nano。
- OpenAI 與 Claude 系列模型繼續保留。
- GitHub 說明此為提升一致性與品質的主動決策，未來也傾向維持較少的模型選項。

**實務影響**

- 依賴 Gemini 模型進行特定任務的 web workflow 需要切換到其他可用模型或改用 API 直接存取。
- 這是可見的模型可用性倒退，需更新團隊的 model selection guide。

### 2026-05-20（[Auto model selection now routes based on your task in VS Code](https://github.blog/changelog/2026-05-20-auto-model-selection-now-routes-based-on-your-task-in-vs-code)）

> **繁中摘要**：VS Code 的 Copilot Auto 模式現在根據任務（reasoning、code generation、bug diagnosis、tool orchestration）動態路由到最佳模型，並提供 10% multiplier 折扣。

**變更重點**

- Auto 模式評估 reasoning 複雜度、code generation 難度、bug 診斷難度、tool orchestration 需求，動態選擇最適合的模型。
- 現實時考量 model availability 與 reliability metrics，確保路由品質。
- 目前只選用 0x–1x multiplier 的模型；使用 Auto 的付費訂閱者有 10% multiplier 折扣（消耗 0.9 premium requests 而非 1.0）。
- 可在回覆上 hover 查看實際選用模型，可隨時切換 Auto 與特定模型。
- 遵守管理員設定的 model policy。

**實務影響**

- Auto 模式降低手動選模型的心智負擔，並對簡單任務自動省成本；10% 折扣讓習慣使用 Auto 的人有額外誘因。
- 需確認 admin model policy 是否有排除 Auto 所需的模型，避免路由失效。

### 2026-05-20（[Semantic issue search in Copilot Chat](https://github.blog/changelog/2026-05-20-semantic-issue-search-in-copilot-chat)）

> **繁中摘要**：GitHub Copilot Chat on web 新增語意 issue 搜尋，支援自然語言查詢，可找出即使措辭不同但語意相關的 issues；對所有 Copilot 計劃 GA。

**變更重點**

- Copilot Chat on web 整合語意 issues index，支援以自然語言描述（非關鍵字精確匹配）搜尋、分組、分析 issues。
- 可理解查詢意圖，找出語意相關但措辭不同的 issues。
- 可依特定 platform 或環境快速篩選 issues。
- 對所有 Copilot 計劃 generally available。

**實務影響**

- Issue triage 與 planning 可以直接在 Copilot Chat 中完成，不需要記住精確標題或關鍵字。
- 對管理大型 issue backlog 的團隊，這讓重複 issue 偵測與主題聚合更容易。
