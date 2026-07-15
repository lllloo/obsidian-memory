---
title: "2026-07-15 Daily Updates"
created: 2026-07-15
updated: 2026-07-15
tags:
  - updates
  - codex
  - opencode
  - copilot
---

## GitHub Copilot

### 2026-07-14（[Security reviews now available in the GitHub Copilot app](https://github.blog/changelog/2026-07-14-security-reviews-now-available-in-the-github-copilot-app)）

**繁中摘要**：Copilot app 新增 `/security-review` slash command（public preview），在不離開編輯環境下對 in-flight 變更做輕量、on-demand 的安全掃描，補位 code scanning／Dependabot／secret scanning。

- **`/security-review` command**：分析目前程式碼變更，回傳依 severity 與 confidence 評分的高信心 findings 與修補建議，涵蓋 injection、XSS、不安全資料處理、path traversal、弱加密等常見高影響漏洞。
- **可用範圍**：public preview，Copilot Free / Pro / Business / Enterprise 皆可用；定位為既有安全工具的補充而非取代。

### 2026-07-10（[Agentic autofix for code scanning alerts in public preview](https://github.blog/changelog/2026-07-10-agentic-autofix-for-code-scanning-alerts-in-public-preview)）

**繁中摘要**：code scanning alert 現可交由 agentic autofix 自動修補——探索 codebase、產生修法、以 CodeQL 重跑驗證後開 PR 送審；原免費「Generate Fix」被「Assign to Copilot」取代，改走 cloud agent 並消耗 AI Credits 與 Actions minutes。

- **運作流程**：像開發者一樣跨檔探索 → 產生 proposed fix → 重跑 CodeQL 驗證有效 → 建立 PR 供人審查。
- **啟用條件與計費**：需 Code Security / Advanced Security license 加上啟用 cloud agent 的 Copilot；preview 期間吃 AI Credits 並扣 Actions minutes；可從單一 alert、alert 清單、campaign 或 REST API 觸發，管理員可於 Settings 或 enterprise policy 關閉。

### 2026-07-14（[GitHub Copilot in Visual Studio — June update](https://github.blog/changelog/2026-07-14-github-copilot-in-visual-studio-june-update)）

**繁中摘要**：Visual Studio 六月更新聚焦用量可視化與 MCP 信任層——新的 usage 視窗即時顯示帳單與接近上限的主動提醒，MCP server 設定於啟動時比對信任基準並在變動時要求核准。

- **用量可視化**：refreshed Copilot Usage 視窗即時顯示 billing，接近上限、達上限、overage 啟動時各有主動提醒。
- **MCP server 信任層**：啟動時驗證 MCP server 設定、比對 trusted baseline，偵測到變動即提示核准。
- **其他**：C++ modernization agent 進入 GA（支援 MSVC 的自動與 guided 升級）；edit 建議可預測作用中檔案任意位置的後續編輯（不限游標附近）；可把 PR 加入 Copilot Chat 當 context 並在 VS 內審核／核准 PR。全 plan tier 可用。

---

## OpenAI Codex

### v0.144.2 · 2026-07-13（[Codex CLI changelog](https://developers.openai.com/codex/changelog)）

**繁中摘要**：patch 版，回退一個 prompting regression，並還原先前的 Guardian auto-review policy、request format 與 tool 行為——若近期覺得 Codex 審查或工具行為異常，升到此版可復原。

- **Regression 回退**：撤銷造成 prompting 行為改變的變更，Guardian auto-review policy 與 request/tool 行為恢復到 regression 前狀態。

---

## OpenCode

### v1.18.0 · 2026-07-14（[OpenCode changelog](https://opencode.ai/changelog)）

**繁中摘要**：Desktop 完成 v2 遷移，帶來版面升級與 onboarding，並提供新舊版面切換 toggle 供過渡期使用；Home 冷啟動時間大幅縮短。

- **v2 版面與 onboarding**：修正 file view 背景、project picker 位置與各 server 權限狀態；改善 terminal tab focus 與 remote session 的權限 auto-accept；強化 timeline 歷史載入與組合功能。
- **過渡切換**：新增新舊版面 toggle；status indicator 更清楚，Home cold-load 明顯加快。

---
