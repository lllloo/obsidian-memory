---
title: "2026-07-12 Daily Updates"
created: 2026-07-12
updated: 2026-07-12
tags:
  - updates
  - codex
  - claude-code
  - opencode
  - copilot
---

## OpenAI Codex

### 2026-07-09（[Codex joins the ChatGPT desktop app](https://developers.openai.com/codex/changelog)）

**繁中摘要**：Codex 整併進 macOS/Windows 的 ChatGPT 桌面應用，既有專案、設定與 workflow 保留，並新增桌面內編輯與 PR 審查能力。

- **桌面整併**：Codex 併入 ChatGPT 桌面應用，既有 projects/settings/workflows 沿用。
- **inline 編輯 + PR review**：可在應用內直接編輯 Markdown/程式碼，側欄審 GitHub PR。
- **多 repo 專案**：單一專案支援多 repository。
- **Computer Use 效能**：搭配 GPT-5.6 的 Computer Use 效能改善。

### Codex CLI 0.144.0 · 2026-07-09（[changelog](https://developers.openai.com/codex/changelog)）

**繁中摘要**：新增 `writes` app-approval 模式與正式版 MCP 互動認證，降低審批與認證的操作摩擦。

- **`writes` 審批模式**：read-only 動作可免逐次審批放行。
- **MCP 互動認證**：脫離 experimental flag 正式支援；app-server host 可帶 redirect 提供 runtime 認證。
- **credits／診斷**：reset credits 顯示類型、到期與兌換選項；global pnpm 安裝可被偵測用於診斷與更新。

### Codex CLI 0.143.0 · 2026-07-08（[changelog](https://developers.openai.com/codex/changelog)）

**繁中摘要**：remote plugins 預設啟用、新增系統 proxy 支援與手動配對命令；MCP 工具預設改走 tool search。

- **Remote plugins 預設開**：catalog 版本追蹤更完整。
- **系統 proxy**：macOS/Windows 支援 PAC/WPAD（`respect_system_proxy`）。
- **`codex remote-control pair`**：產生手動配對碼供裝置配對。
- **Bedrock GPT-5.6**：Amazon Bedrock 上的 Sol/Terra/Luna 支援 `max` reasoning effort；MCP 預設 tool search。

---

## Claude Code

### Week 28（2026 年 7 月 6–10 日）（[閱讀 Week 28 摘要](https://code.claude.com/docs/zh-TW/whats-new/2026-w28)）

**繁中摘要**：Desktop 版新增內建應用內瀏覽器，讓 Claude 能調出網站並如本機 dev server 預覽般互動；另有設定健檢與 auto mode 安全強化。

- **內建瀏覽器（Desktop）**：Claude 可開文件/設計/任意網站並與頁面互動。
- **`/doctor`（別名 `/checkup`）**：完整設定檢查，能診斷問題並修復。
- **Auto mode 安全強化**：阻止文字記錄篡改，對未解析變數執行 `rm -rf` 前先詢問。
- **Agent view rows**：彩色狀態字與分類器編寫的標題。

---

## OpenCode

### v1.17.15–v1.17.18 · 2026-07-07 ~ 07-09（[changelog](https://opencode.ai/changelog)）

**繁中摘要**：連續四個 patch 聚焦 model handling 與 v2 桌面 UI 精修，並修復 GitHub Copilot 模型導致的崩潰。

- **崩潰修復**：Copilot 回傳 zero billing batch size 模型時的崩潰與錯誤定價已修（v1.17.18）。
- **模型處理**：Grok 開放 reasoning effort 變體、xAI prompt cache 路由與 Responses PDF 支援改善；Meta reasoning 變體處理增強。
- **Desktop v2**：新增 composer add 選單（檔案/命令/context/shell）、inline 檔案瀏覽分頁、命令面板刷新，並記憶 per-session review 面板與檔案選取。
- **錯誤分類**：Z.ai context-window 溢位錯誤分類更精準，config 目錄不可用時處理更 graceful。

---

## GitHub Copilot

### 2026-07-09（[OpenAI's GPT-5.6 Sol, Terra, and Luna are now available in GitHub Copilot](https://github.blog/changelog/2026-07-09-openais-gpt-5-6-sol-terra-and-luna-are-now-available-in-github-copilot)）

**繁中摘要**：GPT-5.6 三變體（Sol/Terra/Luna）進入 Copilot，可依任務取向挑選對應模型。

- **三變體選擇**：Sol/Terra/Luna 對應不同工作取向，讓模型與任務匹配。

### 2026-07-09（[Ask Copilot for a repository overview](https://github.blog/changelog/2026-07-09-ask-copilot-for-a-repository-overview)）

**繁中摘要**：首次瀏覽陌生 repo 時可請 Copilot 給出高層次總覽，加速上手不熟悉的程式庫。

- **Repo overview**：在 repo 首頁向 Copilot 索取結構化概覽。

### 2026-07-08（[Enterprise-managed OpenTelemetry export for VS Code and CLI](https://github.blog/changelog/2026-07-08-enterprise-managed-opentelemetry-export-for-vs-code-and-cli)）

**繁中摘要**：組織可統一指定 Copilot 的 OTel 資料匯出目的地，開發者不必各自設定 `OTEL_*` 環境變數。

- **集中式 OTel**：telemetry 直送核准的 collector，免逐人配置環境變數，涵蓋 VS Code 與 CLI。

---
