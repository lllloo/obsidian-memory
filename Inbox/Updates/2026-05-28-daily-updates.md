---
title: "2026-05-28 Daily Updates"
created: 2026-05-28
updated: 2026-05-28
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.152 · 2026-05-27（[Release Notes](https://code.claude.com/docs/en/changelog)）

> **繁中摘要**：v2.1.152 大幅強化 skill 與 hook 生命週期控制，並將 `/code-review` 整合寫回工作樹的能力；auto mode 移除強制同意步驟，降低使用門檻。

**變更重點**

- `/code-review --fix` 可直接將 review findings（reuse、simplification、efficiency）套用到工作樹
- `/simplify` 現在改為呼叫 `/code-review --fix`
- Skill frontmatter 可設定 `disallowed-tools`，讓 skill 執行期間移除指定工具
- 新增 `/reload-skills`：不重啟即可重新掃描 skill 目錄
- `SessionStart` hook 可回傳 `reloadSkills: true`，讓安裝的 skill 在同 session 立即生效
- `SessionStart` hook 可透過 `hookSpecificOutput.sessionTitle` 設定 session 標題
- 新增 `MessageDisplay` hook event，可轉換或隱藏 assistant 訊息顯示文字
- 新增 `pluginSuggestionMarketplaces` managed setting，供管理員限制 plugin 建議市集
- Auto mode 不再需要同意步驟
- Vim mode：NORMAL 模式下 `/` 開啟反向歷史搜尋（同 Ctrl+R）

**實務影響**

- Skill 作者可精細控制工具可用性，避免 skill 執行期間觸發不相關工具
- SessionStart hook 整合更完整，可在 session 啟動時動態載入 skill 並設定標題
- `/code-review --fix` 讓 review → fix 流程可一指令完成，減少手動套用步驟

---

### v2.1.149 · 2026-05-22（[Release Notes](https://code.claude.com/docs/en/changelog)）

> **繁中摘要**：v2.1.149 修補多個 PowerShell 權限繞過漏洞，並為 `/usage`、`/diff` 增加實用操作介面。

**變更重點**

- `/usage` 新增細項分類：skills、subagents、plugins、per-MCP-server 費用明細
- `/diff` 詳細檢視現可用鍵盤捲動（方向鍵、j/k、PgUp/PgDn、Space、Home/End）
- Markdown 渲染支援 GFM task list checkboxes（`- [ ]` / `- [x]`）
- Enterprise：新增 `allowAllClaudeAiMcps` managed setting，可載入 claude.ai cloud MCP connectors

**安全修正**

- PowerShell 內建 `cd` 函式的目錄變更繞過漏洞已修補
- git worktree 中 sandbox write allowlist 修正為只涵蓋共用 `.git` 目錄
- PowerShell prefix/wildcard allow rules 預先核准原生執行檔與腳本
- 修正 `PWD`/`OLDPWD`/`DIRSTACK` 跨 cd/pushd/popd 的追蹤缺口
- 修正 `find` 在大型目錄樹耗盡 macOS vnode table 的問題

**實務影響**

- 使用 PowerShell sandbox 的 Windows 用戶應優先升級以取得安全修補
- `/usage` 細項有助追蹤各 skill / MCP server 的費用比例

---

### v2.1.147 · 2026-05-21（[Release Notes](https://code.claude.com/docs/en/changelog)）

> **繁中摘要**：v2.1.147 將 `/simplify` 升級為具備 correctness bug 偵測的 `/code-review`，並讓 background session 支援 pin 常駐。

**變更重點**

- Pinned background sessions（`Ctrl+T` 於 `claude agents`）閒置時保持存活，更新時原地重啟，僅在記憶體壓力下才回收
- `/simplify` 改名為 `/code-review`，新增指定 effort level 的 correctness bug 報告；`--comment` 可輸出 GitHub PR inline comment
- 改進 auto-updater：重試瞬時失敗、回報具體錯誤類別與 OS 代碼、失敗時顯示目前版本

**實務影響**

- 常駐 background agent 不再因閒置被回收，適合長時間掛在背景等待的工作流
- PR review 流程可直接透過 `--comment` 發 GitHub inline comment，減少手動步驟

---

## OpenAI Codex

### v0.134.0 · 2026-05-26（[Release Notes](https://developers.openai.com/codex/changelog)）

> **繁中摘要**：v0.134.0 為 CLI 加入本地對話歷史搜尋，並強化 MCP 設定與並行執行能力；Windows TUI 渲染問題修復。

**變更重點**

- 新增本地對話歷史搜尋：大小寫不敏感，含結果預覽
- `--profile` 升為主要 profile selector，統一 CLI、TUI permissions、sandbox workflow
- MCP 設定強化：per-server 環境變數目標設定、streamable HTTP server 的 OAuth 選項
- read-only MCP tools（標記 `readOnlyHint`）現支援並行執行
- Extension 與 hook context 新增對話歷史存取和 subagent identity tracking

**Bug 修正**

- WebSocket 重連、auth 重試、stream retry 改善遠端連線穩定性
- 修正 Windows TUI 虛擬終端模式未還原導致的渲染損壞
- Node-based tools 現在遵從 managed network proxy 設定

**實務影響**

- read-only MCP tools 並行執行可顯著縮短多工具同時呼叫的等待時間
- Windows 用戶 TUI 渲染問題修復，可正常使用

---

### v0.133.0 · 2026-05-21（[Release Notes](https://developers.openai.com/codex/changelog)）

> **繁中摘要**：Goals 正式預設啟用，remote-control 改為前景指令；Plugin marketplace CLI 命令讓插件管理更結構化。

**變更重點**

- Goals 現預設啟用，具備專屬儲存與跨 active turn 的進度追蹤
- `codex remote-control` 改為前景指令，支援 readiness waiting 與明確的 daemon 控制
- Permission profiles 新增 list API、繼承支援、managed `requirements.toml`、執行期刷新
- Plugin marketplace CLI 命令：marketplace-aware 列表、已安裝版本顯示、remote collection 支援
- Extensions 可觀察新生命週期事件：subagent start/stop、tool execution、turn metadata、async approvals

**實務影響**

- Goals 無需手動啟用即可開始追蹤跨 turn 的目標進度
- Extension 開發者獲得更完整的生命週期鉤子，可建立更細緻的自動化

---

### Goal Mode GA · 2026-05-21（[App Release Notes](https://developers.openai.com/codex/changelog)）

> **繁中摘要**：Goal Mode 從實驗功能升為正式功能，Appshots 登陸 macOS，遠端電腦使用能力開放。

**變更重點**

- Goal Mode 正式移除實驗標記，可在 app、IDE extension、CLI 全面使用
- Appshots（macOS）：按兩次 Command 鍵可將前景 app 視窗截圖與文字一同送入 Codex
- Remote computer use：Codex 可在 Mac 鎖定畫面後存取桌面應用
- Plugin sharing 透過 marketplace sources 開放（ChatGPT Business；Enterprise 即將支援）

**實務影響**

- Goal Mode 穩定版可放心納入正式工作流
- Appshots 大幅降低截圖 → 傳入 AI 的操作步驟

---

## GitHub Changelog

### 2026-05-26（[Copilot Memory 刪除、範圍與 CLI 控制](https://github.blog/changelog/2026-05-26-copilot-memory-has-more-controls-for-deletion-scope-and-the-copilot-cli)）

> **繁中摘要**：Copilot Memory（公開預覽）新增更細緻的刪除控制、repository-level 關閉開關，以及 Copilot CLI 中的記憶體管理命令。

**變更重點**

- 改進記憶體刪除功能
- 新增 repository-level off switch，可對特定 repo 停用 Copilot Memory
- Copilot CLI 新增 Memory 相關控制命令

**實務影響**

- 需要對敏感 repo 隔離 Memory 的團隊可直接在 repo 層級關閉，不影響其他 repo

---

### 2026-05-26（[Enterprise model rules：對 org 目標指定 Copilot 模型](https://github.blog/changelog/2026-05-26-target-copilot-models-to-organizations-with-model-rules)）

> **繁中摘要**：Enterprise owner 可為不同 org 設定不同可用 Copilot 模型，取代全域統一限制。

**變更重點**

- Enterprise owner 可對各 org 設定 targeted model rules
- 可允許特定模型只在特定 org 使用，而非全域統一套用

**實務影響**

- 多 org Enterprise 帳號可依需求差異化模型存取權，有助合規與成本控管

---

### 2026-05-21（[GitHub Copilot for Eclipse 開源](https://github.blog/changelog/2026-05-21-github-copilot-for-eclipse-is-open-source)）

> **繁中摘要**：GitHub Copilot for Eclipse 正式開源，採 MIT 授權，標誌 Copilot IDE 生態系的重要里程碑。

**變更重點**

- Copilot for Eclipse 原始碼以 MIT 授權發布於 GitHub

**實務影響**

- Eclipse 用戶可自行 fork、提交 PR；企業也可基於此建立客製化版本
