---
title: "2026-06-27 Daily Updates"
created: 2026-06-27
updated: 2026-06-27
tags:
  - updates
  - claude-code
  - copilot
---

## Claude Code

### v2.1.193 · 2026-06-25（[Changelog](https://code.claude.com/docs/en/changelog#2-1-193)）

**繁中摘要**：這版把 auto-mode 的權限治理與可觀測性再收緊——可強制所有 shell 命令走分類器、把拒絕原因留痕，並新增 assistant 回應的 OTEL log 事件；另有 bash 模式路徑自動補全與背景 shell 的記憶體回收。

- **`autoMode.classifyAllShell`**：開啟後所有 Bash/PowerShell 命令一律送進 auto-mode 分類器判斷，而非只挑部分，權限控管更一致。
- **拒絕原因留痕**：auto-mode 的拒絕理由現會寫進 transcript、拒絕 toast 與 `/permissions` 的近期拒絕清單，事後可回查為何被擋。
- **`claude_code.assistant_response` OTEL log 事件**：新增 assistant 回應的遙測事件，預設內容遮蔽；需設 `OTEL_LOG_ASSISTANT_RESPONSES=1` 才記錄原文，方便稽核但留意隱私。
- **bash 模式路徑補全**：`!` bash 模式新增即時檔案路徑自動補全。
- **MCP 認證提示**：啟動時若有 MCP server 需認證會跳提示並指向 `/mcp`，免得 server 靜默失效。
- **背景 shell 記憶體回收**：閒置的背景 shell 命令會在記憶體吃緊時自動回收（以 `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` 關閉）。

---

## GitHub Copilot

### 2026-06-26（[MAI-Code-1-Flash 登上 Copilot Business 與 Enterprise](https://github.blog/changelog/2026-06-26-mai-code-1-flash-for-copilot-business-and-copilot-enterprise)）

**繁中摘要**：Microsoft 自研的 coding 模型 MAI-Code-1-Flash 對 Copilot Business／Enterprise GA，主打高頻 agentic coding 的速度與效率；需管理員先開政策，使用者才能在 model picker 選用。

- **定位**：為 coding 而生、針對 Copilot 優化的快速模型，適合高頻、迭代式的 agentic coding workflow，速度與效率優先。
- **啟用門檻**：管理員須在 Copilot 設定先啟用 MAI-Code-1-Flash 政策，使用者才能從 model picker 下拉選用。
- **計費**：採 provider list pricing 的 usage-based billing，與標準 Copilot 模型費率一致。

### 2026-06-26（[GitHub Desktop 3.6：Worktrees 與更深的 Copilot 整合](https://github.blog/changelog/2026-06-26-github-desktop-3-6-worktrees-and-deeper-copilot-integration)）

**繁中摘要**：GitHub Desktop 3.6 把 Git worktree 帶進 GUI，並讓 Copilot 接手 commit 訊息與 merge 衝突解析；所有 Copilot 功能改跑 Copilot SDK，支援選模型與 BYOK。

- **Worktree 支援**：可同時在多個 branch 上工作，免反覆 stash／切 branch／重 clone；toolbar 新增 Current Worktree 選單。
- **Copilot SDK 為底 + BYOK**：所有 Copilot 功能改跑 Copilot SDK 統一框架，可挑模型，也能用 bring-your-own-key 接第三方或本地模型。
- **commit 訊息生成讀專案規範**：生成 commit 訊息時會讀 `.github/copilot-instructions.md` 與 `AGENTS.md`，並遵守 repo 的 commit metadata 規則，讓訊息貼合團隊慣例。
- **AI 解 merge 衝突**：可由 AI 解釋衝突並給出建議解法，使用者審閱、接受或修改後再完成 merge。

---
