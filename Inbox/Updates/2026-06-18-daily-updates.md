---
title: "2026-06-18 Daily Updates"
created: 2026-06-18
updated: 2026-06-18
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.181 · 2026-06-17（[Changelog](https://code.claude.com/docs/en/changelog#2-1-181)）

**繁中摘要**：2.1.181 帶來多項實用新功能與大批 bug 修復，其中 `/config key=value` 語法可直接從 prompt 切換任何設定，prompt caching 修復影響自訂 API endpoint 與 Foundry 用戶。

- **`/config key=value` 語法**：在 interactive、`-p`、Remote Control 模式下均可即時切換設定（如 `/config thinking=false`），不需手動編輯 settings.json。
- **Prompt caching 修復**：自訂 `ANTHROPIC_BASE_URL` 與 Foundry 因 per-request attestation token 每輪變動導致 cache 讀取失效，現已修復，可有效降低 token 成本。
- **Write/Edit 修復**：在 network drive 與 cloud-sync 資料夾（如 OneDrive）下產生 0-byte 或截斷檔案的問題已修復，Windows 用戶特別受益。
- **Subagent 深度限制**：foreground subagent 現在同樣受 5 層巢狀上限約束，防止 unbounded nested chain 失控。
- **啟動效能**：修復 2.1.169 引入的 ~120ms 啟動 regression 及帳戶設定 fetch 慢時最長卡 15 秒的問題；另修復 `.claude.json` 含損壞 null entries 導致的 crash。
- **其他新功能**：`CLAUDE_CLIENT_PRESENCE_FILE` 可抑制 mobile push notification；`sandbox.allowAppleEvents` 允許沙箱指令發送 Apple Events（macOS）；Bun runtime 升至 1.4。

---

### v2.1.179 · 2026-06-16（[Changelog](https://code.claude.com/docs/en/changelog#2-1-179)）

**繁中摘要**：2.1.179 為純修復版，重點解決 mid-stream 斷線保留部分回應、WSL2 滾輪 regression，以及 sandbox glob 在大型目錄樹下讓 Bash 工具描述膨脹到 session 無法使用的嚴重問題。

- **Mid-stream 斷線修復**：連線中斷時部分回應現在會保留而非直接報錯，spinner 也不再卡在「running tool」。
- **Sandbox glob 效能修復**：`denyRead`/`allowRead` glob 指向大型目錄樹時 Bash tool description 異常膨脹、Linux session 無法使用的問題已修復——使用 sandbox 限制的用戶需注意。
- **WSL2 滾輪修復**：Windows Terminal 與 VS Code 下 WSL2 的滑鼠滾輪捲動（2.1.172 regression）已恢復正常。

---

## OpenAI Codex

### 2026-06-16（[Codex app features available in EEA/UK/Switzerland](https://developers.openai.com/codex/changelog#codex-app-eea-2026-06-16)）

**繁中摘要**：Codex 多項進階功能正式擴展至 EEA、英國、瑞士地區，包含 Computer Use 桌面操作、Chrome 擴充功能跨分頁瀏覽、Memories 偏好記憶（預設關閉）等，對歐洲地區用戶的 workflow 可用性有直接影響。

- **Computer Use（macOS / Windows）**：可直接操作桌面應用程式，現已向 EEA/UK/CH 用戶開放。
- **Codex Chrome Extension**：支援需要已登入 Chrome 情境的跨分頁瀏覽任務，擴展 browser automation 適用場景。
- **Memories**：可儲存偏好與 workflow 模式，EEA 區域預設關閉，需手動啟用。
- **Chronicle**：ChatGPT Pro（macOS）的 opt-in 研究預覽功能，目前仍是預覽階段。

---

### 2026-06-15（[ChatGPT for iOS 1.2026.160](https://developers.openai.com/codex/changelog#chatgpt-ios-12026160)）

**繁中摘要**：iOS 端大幅強化 Codex 使用體驗，新增 workspace 檔案瀏覽、MCP 核准粒度控制與 LaTeX 渲染，並改善 thread 效能與連線穩定性，對行動端 coding agent 工作流有實質提升。

- **Workspace 檔案瀏覽器**：可預覽檔案並將路徑直接帶入 prompt，減少手動輸入路徑的摩擦。
- **MCP 核准選擇**：可選擇「僅本次 chat」或「所有 chat」套用動作，讓 MCP 授權粒度更細。
- **LaTeX 渲染**：Codex 訊息中的數學公式可正確顯示，提升技術內容可讀性。
- **Diff 控制 & Thread 效能**：可展開/收合 diff，subagent 狀態指示更清晰，thread 執行效能強化。

---

### 2026-06-11（[Codex app rate-limit banking & Developer mode](https://developers.openai.com/codex/changelog#codex-app-eea-rate-limit)）

**繁中摘要**：引入 rate-limit reset 銀行制度（Plus/Pro 可透過推薦取得額外重置次數）、Developer mode（CDP 存取）與 `/init` 指令，對重度 Codex 用戶的配額管理與 browser automation 開發有直接影響。

- **Rate-limit Reset 銀行**：Plus/Pro 用戶獲得初始重置額度，並可透過邀請累積，有效緩解 rate-limit 瓶頸。
- **Developer Mode（Browser）**：Chrome 與 in-app 瀏覽器開放 Chrome DevTools Protocol 存取，可用於效能 profiling 與 debug。
- **/init 指令**：與 CLI 相同的專案初始化流程現在在 app 內可直接執行。
- **Computer Use 擴展**：Enterprise 用戶（非受限地區）及 Windows per-app 存取控制正式支援。

---

## GitHub Changelog

### 2026-06-17（[Auto mode in Copilot Chat available for all users](https://github.blog/changelog/2026-06-17-auto-mode-in-copilot-chat-available-for-all-users)）

**繁中摘要**：GitHub Copilot Chat 的 auto 模型選擇模式正式 GA，對所有 Copilot 方案開放，Copilot 將自動挑選最適模型，使用者不再需要手動切換，降低日常使用摩擦。

- **Auto 模型選擇（GA）**：github.com 與 GitHub 行動 App 的 Copilot Chat 均支援，適用所有 Copilot 方案；Copilot 自行決定使用哪個模型，省去手動選擇步驟。

---

### 2026-06-17（[Agent finder for GitHub Copilot now available](https://github.blog/changelog/2026-06-17-agent-finder-for-github-copilot-now-available)）

**繁中摘要**：GitHub Copilot 新增 Agent Finder，可自動發現並組合所需的 MCP servers、skills、agents 與 tools，無需手動配置，大幅降低 agent setup 的複雜度與 context 消耗。

- **Agent Finder**：Copilot 自動識別任務所需工具組合，取代原本需要手動指定 MCP server 與 agent 的流程——對維護多個 MCP 設定的使用者尤其省力。
- **Context 效率**：不再因手動填入 agent 清單而消耗大量 context window，讓 agent 可用於實際任務。

---

### 2026-06-17（[GitHub Copilot app generally available](https://github.blog/changelog/2026-06-17-github-copilot-app-generally-available)）

**繁中摘要**：GitHub Copilot 桌面 App 正式 GA，支援 macOS、Windows、Linux，以 agent-driven development 為核心設計，是繼 VS Code extension 之後的獨立桌面入口。

- **Copilot App GA**：跨三大平台正式發佈，定位為 agent-driven 開發的桌面主場，原生整合 GitHub 生態系；有別於 IDE 外掛，提供獨立應用程式體驗。

---
