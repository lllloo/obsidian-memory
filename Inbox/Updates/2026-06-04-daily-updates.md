---
title: "2026-06-04 Daily Updates"
created: 2026-06-04
updated: 2026-06-04
tags:
  - updates
  - claude-code
  - copilot
  - codex
---

## Claude Code

### v2.1.162 · 2026-06-03（[Update 2.1.162](https://code.claude.com/docs/en/changelog#21162)）

> **繁中摘要**：2.1.162 包含多項 agents 可觀測性改進、工具路由修正、slash command UX 調整，以及多個影響 Windows、SDK、MCP、LSP 的 bug fix。

**變更重點**
- `claude agents --json` 新增 `waitingFor` 欄位，顯示 session 被什麼阻塞（如 permission prompt）
- `--tools` 明確列出 Grep/Glob 現在可在 embedded search 的 native build 上正確啟用（原先靜默忽略）
- `/effort` 選定後會確認該 level 是否將成為新 session 的預設
- Slash command autocomplete：點選條目只填入、不立即執行；需按 Enter 才觸發
- Remote Control 改為常駐 footer pill 顯示（含 session 連結），不再是啟動訊息
- Windsurf 在 `/ide`、`/terminal-setup`、`/scroll-speed` 選單中更名為 Devin Desktop

**Bug Fixes（影響日常使用）**
- 修正 config 目錄不可寫時靜默卡住 → 現在以 in-memory config 啟動並顯示錯誤
- 修正 WebFetch permission rules 未套用到預批准 domain
- 修正 Windows permission rules 使用反斜線或大小寫路徑時永遠不匹配；Read deny rules 未對 Glob/Grep 隱藏檔案
- 修正 stream-json/SDK session 在 turn 開始時發送 Esc 被靜默丟棄
- 修正含 emoji 的 classifier side-query 在截斷邊界觸發 API 400 錯誤
- 修正 MCP per-server timeout 低於 1000ms 時被強制 floor 到 1 秒
- 修正 LSP tool `workspaceSymbol` 回傳空結果
- 修正 `claude agents` 在寬終端截斷 live status；截斷長 session name；attach 偶爾彈回清單；Ctrl+V 圖片貼上無效
- 修正背景 session 無法啟動時靜默丟失對話
- 修正 `SendMessage` 跨 session 訊息在 CLAUDE_CODE_TMPDIR/TMPDIR 指向深層目錄時靜默失效

**實務影響**
- `waitingFor` 讓監控腳本可精確判斷 agent 卡在哪一步（permission vs. 計算）
- Windows 用戶的路徑匹配問題修正後，permission rules 才能正確運作
- MCP timeout 修正影響所有設定低於 1 秒超時的 server 配置
- SDK/stream-json 用戶的 Esc interrupt 現在可靠

---

### v2.1.160 · 2026-06-02（[Update 2.1.160](https://code.claude.com/docs/en/changelog#21160)）

> **繁中摘要**：2.1.160 在寫入 shell startup 檔案與 build-tool config 前新增確認提示，收緊 `acceptEdits` 安全邊界；同時修正多個 Windows、背景 agent、WSL 相關問題。

**變更重點**
- 寫入 shell startup 檔案（`.zshenv`、`.zlogin`、`.bash_login`）及 `~/.config/git/` 前現在會提示確認，防止非預期指令執行
- `acceptEdits` 模式在寫入可授予程式碼執行權限的 build-tool config 前會提示：`.npmrc`、`.yarnrc*`、`bunfig.toml`、`.bazelrc`、`.pre-commit-config.yaml`、`.devcontainer/` 等
- Edit 不再需要在 grep 查看後再做獨立 Read：單一檔案 grep/egrep/fgrep 命令現在滿足 read-before-edit 檢查
- Dynamic workflow 觸發關鍵字重新命名（`workflow` → `ultracode`）

**Bug Fixes（影響日常使用）**
- 修正 WSL 上 copy-on-select 未寫入 Windows clipboard
- 修正從 `claude agents` 還原已完成 session 時丟失對話歷程並重跑原始 prompt
- 修正背景 session 在 sleep/wake 後重新 attach 時丟失對話並重跑 prompt
- 修正 `claude --bg` 在 background daemon cold-start 時偶爾報「socket missing」
- 修正 Windows 上背景 session 的起始目錄在 `claude rm` 後無法刪除
- 修正 `claude agents` 退出 session 時因 auto-updater 重複檢查導致凍結數秒
- 修正 Windows attached session 的 Esc、方向鍵、輸入無回應
- 修正背景 agent 向不支援的終端（Apple Terminal、tmux）發送 sync-output marker
- 修正 CJK IME 組字位置顯示在螢幕左下角而非輸入游標處
- 修正 `file:///C:/...` 連結在 Windows 上被改寫為錯誤路徑
- 修正 project 目錄或分支名含非 ASCII/特殊字元時 voice mode 無法連線
- 修正 `/effort ultracode` 錯誤歸咎於 dynamic workflows 設定

**實務影響**
- `acceptEdits` 模式下的安全邊界收緊，自動化流程中若有寫入 `.npmrc` 等檔案需預期多一個確認步驟
- Windows/WSL 用戶的多項體驗問題在此版本集中修正
- CJK 用戶 IME 輸入位置修正改善可用性

---

## GitHub Changelog

### v1.120–v1.123 · 2026-06-03（[GitHub Copilot in Visual Studio Code, May releases](https://github.blog/changelog/2026-06-03-github-copilot-in-visual-studio-code-may-releases)）

> **繁中摘要**：GitHub Copilot for VS Code 在 5 月正式推出 Agents mode（GA）、加入 MCP image input 支援與 agent skills marketplace，並新增 GitHub Copilot Search、`/fix` diagnostics 指令及 notebook `Ask` 指令，大幅擴展 agentic workflow。

**變更重點**
- Agents mode 正式 GA，提供 real-time streaming 回應與 thinking indicators
- VS Code Marketplace 開放安裝 agent skills；custom instructions 支援 agent mode
- MCP 新增 image input 支援
- GitHub Copilot Search 上線
- Smart context selector 改進 + 自動從 open files 取 context
- Inline edits：新增 inline follow-ups、Next Edit Suggestions 支援更多 model
- 新增 `/fix` command（diagnostics）、notebook `Ask` command、改良 test generation flow

**實務影響**
- Agents mode GA 代表 agentic 任務流程可用於生產環境，不再 preview 限制
- MCP image input 讓 multimodal context 可直接進 Copilot agent；skills marketplace 提供可擴充的工具鏈
- `/fix` 與 notebook `Ask` 填補診斷修復與 notebook 互動的操作缺口

---

### 2026-06-02（[GitHub Copilot code review for Azure Repos is now in technical preview](https://github.blog/changelog/2026-06-02-github-copilot-code-review-for-azure-repos-is-now-in-technical-preview)）

> **繁中摘要**：Copilot code review 擴展至 Azure Repos（technical preview），可在 Azure DevOps 工作流中直接對 pull request 觸發 on-demand 審查。

**變更重點**
- Copilot code review 進入 Azure Repos technical preview
- 支援在 Azure DevOps PR 上按需觸發審查，無需離開既有工作流

**實務影響**
- 使用 Azure DevOps 的團隊現可把 Copilot 審查納入 PR 流程

---

### 2026-06-02（[Introducing Copilot CLI and agentic capabilities enhancements in JetBrains IDEs](https://github.blog/changelog/2026-06-02-introducing-copilot-cli-and-agentic-capabilities-enhancements-in-jetbrains-ides)）

> **繁中摘要**：JetBrains IDE 版 GitHub Copilot 新增 Copilot CLI 整合（終端式 AI 協助無需離開 IDE），以及 multi-file editing、custom instructions 支援與改良的 agent mode tool use。

**變更重點**
- Copilot CLI 現可在 JetBrains IDE 內使用，提供終端風格 AI 協助
- 新增 agentic 能力：multi-file editing、custom instructions 支援、agent mode tool use 改良

**實務影響**
- JetBrains 使用者可在 IDE 內直接使用 Copilot CLI，不需切換到獨立終端
- Multi-file editing 與 custom instructions 讓 JetBrains agentic workflow 與 VS Code 功能對齊

---

## GitHub Copilot CLI

### v1.0.57–v1.0.59 · 2026-06-02（[Copilot CLI releases](https://github.com/github/copilot-cli/releases/tag/v1.0.59)）

> **繁中摘要**：Copilot CLI 連續多版：Rubber Duck 與 Remote JSON RPC 改為預設開啟，新增 `/voice` 語音輸入與 `/experimental` 排程 prompt（`/every`、`/after`），Ctrl+C 改為終止整個進程樹。

**變更重點**
- v1.0.59：新增 `/voice`，用本地 speech-to-text 模型口述 prompt
- v1.0.58：Rubber Duck、Remote JSON RPC 改為預設啟用；`/experimental` 加入 `/every`／`/after` 排程 prompt、`/theme`、新 UI（issues／PR／gists 快捷）
- v1.0.57：取消執行中 shell 指令（Ctrl+C／中止 agent 指令）現在終止整個進程樹，不再留孤兒進程；plugin slash command 顯示即時進度；Azure DevOps-only repo 的內建 GitHub MCP 只暴露 `web_search`
- v1.0.57-4：preToolUse hook 錯誤改為 deny 工具呼叫（原本靜默放行）；tmux 內 Ctrl+C 等修飾鍵正確運作

**實務影響**
- Ctrl+C 進程樹清理修正避免背景／sandbox shell 留孤兒進程
- preToolUse hook 從「靜默放行」改成「擋下」，安全行為更符合預期

---

## OpenAI Codex

### 2026-06-02（[Build and deploy websites with Sites](https://developers.openai.com/codex/changelog#build-and-deploy-websites-with-sites)）

> **繁中摘要**：Codex app 新增 Sites plugin（preview），可直接在 app 內建立、部署、管理 OpenAI 托管的網站與 web app；ChatGPT Business workspace 預設開啟，Enterprise 由管理員以 role-based controls 管控。

**變更重點**
- Sites plugin 進入 preview，支援建立、儲存、部署、查看網站、dashboard、內部工具、web app、遊戲
- 專案管理透過 app sidebar 操作
- ChatGPT Business workspace 預設包含此功能；Enterprise 管理員可控存取權限

**實務影響**
- 若使用 Codex app 進行 web prototype 或 internal tooling，可直接在同一介面內部署，不需另起 hosting 流程
- Enterprise 環境需留意 admin 是否已開放 Sites 存取

**待追蹤**
- Preview 階段，正式 GA 時間未定；功能邊界（如自訂 domain、版本管理）尚未揭露

---

### Codex CLI 0.137.0 · 2026-06-04（[Codex CLI 0.137.0](https://developers.openai.com/codex/changelog#codex-cli-01370)）

> **繁中摘要**：Codex CLI 0.137.0：TUI 支援 F13-F24 鍵與在搜尋選單貼上，plugin 工作流提供機器可讀 JSON 輸出與快取的遠端 catalog 建議，multi-agent v2 改進每 thread 的 runtime 選擇與 follow-up 預設。

**變更重點**
- TUI 支援 F13-F24 keybinding，並可在可搜尋選單中貼上
- Enterprise／admin 工作流顯示每月 credit 上限、套用 cloud-managed 設定 bundle
- Remote-control client 可透過 app-server RPC 發起配對與管理 controller 授權
- Plugin 工作流提供機器可讀 JSON 輸出與快取的遠端 catalog 建議
- Hosted web／image 工具支援更多 code-mode 流程，含平行獨立 web 搜尋
- Multi-agent v2 維持每 thread 的 runtime 選擇，改進 follow-up 預設

**實務影響**
- Plugin JSON 輸出便於把 Codex plugin 狀態接進自動化腳本
- Multi-agent v2 的 per-thread runtime 對多代理協調工作流有用

---

## Spec Kit

### v0.8.18–v0.9.3 · 2026-06-03（[Spec Kit releases](https://github.com/github/spec-kit/releases/tag/v0.9.3)）

> **繁中摘要**：Spec Kit 連續多版：新增 `specify self upgrade`、把 agent context 更新遷移到 agent-context extension（舊 fallback 將於 v0.12.0 移除），並修多項 Windows UTF-8 編碼與 workflow resume 問題。

**變更重點**
- v0.9.0：agent context 更新遷移到 agent-context extension，現自動啟用以維持相容；此 fallback 已棄用，將於 v0.12.0 移除
- 新增 `specify self upgrade`（CLI 自我升級）；workflow resume 可接受更新後的 inputs
- 多項 Windows 修正：強制 UTF-8 stdout/stderr 防 UnicodeEncodeError、init-options／`.extensionignore` I/O 釘 UTF-8 編碼
- 新增 `continue_on_error` step 欄位（非中止式失敗）；native Cline 整合

**實務影響**
- 既有依賴自動 agent context 更新的專案需在 v0.12.0 前明確啟用 agent-context extension
- Windows 用戶的 UTF-8 編碼崩潰問題在此系列集中修正

---

## Vercel Skills

### v1.5.10 · 2026-06-03（[vercel-labs/skills v1.5.10](https://github.com/vercel-labs/skills/releases/tag/v1.5.10)）

> **繁中摘要**：新增 `run` 指令可不安裝直接執行 skill，加入一批 agent 整合（含 kimi-code-cli、Antigravity CLI），並修 GitHub clone 認證 fallback 與全域 skill 歸屬。

**變更重點**
- 新增 `run` 指令：不安裝即執行 skill
- 新增多個 agent 整合：kimi-code-cli、Antigravity CLI
- 修正：clone 時 fall back 到 `gh` 與 ssh 認證；global skill 歸屬到 universal agents

**實務影響**
- `run` 讓一次性試用 skill 不必先安裝

---

## Nuxt

### v4.4.7 / v3.21.7 · 2026-06-02（[Nuxt v4.4.7](https://github.com/nuxt/nuxt/releases/tag/v4.4.7)）

> **繁中摘要**：Nuxt 安全 hotfix（4.x 與 3.x 同步），修補 test component wrapper 的 sibling-directory traversal、buildCache 路徑邊界檢查，以及 Vite `allowDirs` 共享前綴過濾問題。

**變更重點**
- 安全 hotfix：修 test component wrapper 的 sibling-directory traversal
- `buildCache` 路徑邊界檢查改用 `pathe` 的 resolve
- Vite：避免把共享前綴的目錄從 `allowDirs` 過濾掉
- Nitro：`noSSR` 在決定 payload extraction 前先指派

**實務影響**
- 屬安全釋出，建議查 nuxt security advisories 確認受影響範圍並升級

**待追蹤**
- 詳見 [nuxt security advisories](https://github.com/nuxt/nuxt/security/advisories)
