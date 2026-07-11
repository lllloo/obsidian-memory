---
title: "2026-07-11 Daily Updates"
created: 2026-07-11
updated: 2026-07-11
tags:
  - updates
  - codex
  - copilot
  - opencode
---

## OpenAI Codex

### 2026-07-09（[Codex 進駐 ChatGPT 桌面 App](https://learn.chatgpt.com/docs/changelog)）

**繁中摘要**：Codex 併入 macOS／Windows 版 ChatGPT 桌面 App，把原本獨立的 Codex 體驗收攏進同一個桌面殼，既有專案、設定與 workflow 直接沿用。

- **桌面整合**：直接在 App 內編輯 Markdown 與程式碼、行內註解，並可在側欄審查 GitHub PR；支援多 repo 專案。
- **Computer Use × GPT-5.6**：Computer Use 效能隨 GPT-5.6 提升，任務活動可視性與 plugin 管理（移到 Settings）改善。

---

### v0.144.0 · 2026-07-09（[Codex CLI changelog](https://learn.chatgpt.com/docs/changelog)）

**繁中摘要**：CLI 新增數項會改變授權與 MCP 使用方式的能力，最值得注意的是 MCP 互動式驗證不再需要 experimental 旗標。

- **MCP 互動式驗證預設可用**：MCP tools 支援互動式 auth，不再需要 experimental opt-in。
- **新 approval 模式 `writes`**：允許唯讀動作放行、僅寫入動作需核可，介於全放行與逐項核可之間。
- **用量顯示**：usage-limit reset 顯示 credits 型別與到期資訊；多 agent 高併發時給出 ultra reasoning 警告。

---

### v0.143.0 · 2026-07-08（[Codex CLI changelog](https://learn.chatgpt.com/docs/changelog)）

**繁中摘要**：預設開啟 remote plugins 與 MCP tool search，並補上企業網路環境常見的 system proxy 自動路由，降低受管網路下的設定成本。

- **Remote plugins 預設開啟**：catalog rows 強化，遠端 plugin 開箱即用。
- **System proxy 路由**：macOS／Windows 支援 PAC、WPAD 自動代理設定。
- **MCP tool search 預設開啟**；新增 `codex remote-control pair` 手動配對碼指令；Amazon Bedrock 上線 GPT-5.6（Sol／Terra／Luna）並支援 `max` reasoning。

---

## GitHub Copilot

### 2026-07-09（[GPT-5.6 Sol、Terra、Luna 進入 Copilot](https://github.blog/changelog/2026-07-09-openais-gpt-5-6-sol-terra-and-luna-are-now-available-in-github-copilot)）

**繁中摘要**：OpenAI GPT-5.6 家族開始在 Copilot 推出，三種變體 Sol／Terra／Luna 讓你依任務性質挑選對應模型。

- **三變體選型**：Sol／Terra／Luna 對應不同工作特性，可按 job 匹配模型，而非單一模型通吃。

---

### 2026-07-09（[向 Copilot 詢問 repository 總覽](https://github.blog/changelog/2026-07-09-ask-copilot-for-a-repository-overview)）

**繁中摘要**：首次探索陌生 repo 時，可直接在 repo 首頁請 Copilot 給出高層次總覽，縮短上手一個新 codebase 的時間。

- **Repo 總覽**：造訪未看過的 repo 首頁即可請 Copilot 產生高層次說明，用於快速理解專案結構與用途。

---

## OpenCode

### v1.17.16–v1.17.18 · 2026-07-09（[OpenCode changelog](https://opencode.ai/changelog)）

**繁中摘要**：三個接連小版本以 provider 相容性修復與 Desktop v2 介面打磨為主；跨供應商的 reasoning effort 與快取路由是少數影響實際使用的 Core 變更。

- **Provider／model 相容**：Grok 開放 reasoning effort 變體、優化 xAI prompt cache 路由與 Responses model 的 PDF 支援；修復 GitHub Copilot 回傳 zero billing batch size 導致的 crash，並為 Meta Muse Spark 加入專屬 system prompt。
- **Desktop v2 打磨**：新的 free-model 選擇器、home 開資料夾、composer add 選單擴充（files／commands／context／shell mode 並保留草稿）、review pane 與 sub-agent task row 對齊 v2 樣式；另修多項 session pane 與導覽相關 bug。
