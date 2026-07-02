---
title: "2026-07-02 Daily Updates"
created: 2026-07-02
updated: 2026-07-02
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.198 · 2026-07-01（[Changelog](https://code.claude.com/docs/en/changelog#2-1-198)）

**繁中摘要**：這版重點在 background agent 自動化程度大幅提高——worktree 內完成工作後會直接 commit、push 並開 draft PR，且新增 `Notification` hook 事件可在 agent 需要輸入或完成時通知；另外 Claude in Chrome 正式 GA，subagent 品質相關的模型與 thinking 繼承行為也有調整。

- **Background agents 自動開 PR**：從 `claude agents` 啟動的 background agent 在 worktree 完成程式工作後，改為自動 commit、push 並開 draft PR，不再停下來詢問——對不想被自動 push 的 workflow 需留意這個行為變更。
- **Background agent 通知**：sessions 需要輸入或完成時會觸發 `Notification` hook（`agent_needs_input` / `agent_completed`），可以此串接自己的提醒機制。
- **Claude in Chrome GA**：瀏覽器整合正式開放。
- **Subagent 品質繼承**：內建 Explore agent 改為繼承主 session 模型（上限 opus）而非固定跑 haiku；subagents 與 context compaction 也會繼承 session 的 extended thinking 設定，委派任務輸出品質提升。
- **Gateway 支援 Claude Platform on AWS**（anthropicAws）作為 upstream provider，model-not-found 會沿 failover chain 繼續嘗試；STS token 過期時 `awsAuthRefresh` 自動執行，不再卡在 "Please run /login"。
- **移除 `/agents` wizard**：改用自然語言請 Claude 建立／管理 subagent，或直接編輯 `.claude/agents/`；另修復 20+ bug，值得注意的是網路瞬斷（ECONNRESET）改為 backoff 重試不再中斷回合，以及 agent team 成員 API error 死掉時會回報 "failed" 給 lead。

---

## OpenAI Codex

### Codex CLI 0.142.5 · 2026-07-01（[Changelog](https://developers.openai.com/codex/changelog#codex-cli-01425)）

**繁中摘要**：單一修復版，堵住 trace log 洩漏完整 request payload 的問題，屬隱私／安全面修補。

- **Trace log 隱私修復**：不再把完整 Responses WebSocket request payload 寫入 trace logs——先前版本的 trace log 可能含 prompt／程式碼內容，分享 log 除錯前需留意。

---

## GitHub Copilot

### 2026-07-01（[Kimi K2.7 Code is generally available in GitHub Copilot](https://github.blog/changelog/2026-07-01-kimi-k2-7-is-now-available-in-github-copilot)）

**繁中摘要**：Kimi K2.7 Code 在 GitHub Copilot 正式 GA，是 Copilot model picker 首個可選的 open-weight 模型，模型選擇面多了開放權重選項。

- **首個 open-weight 選項**：Kimi K2.7 Code 進入 Copilot model picker 成為可直接選用的模型，是 Copilot 第一次把開放權重模型列為正式選項。

### 2026-07-01（[Copilot vision is generally available](https://github.blog/changelog/2026-07-01-copilot-vision-is-generally-available)）

**繁中摘要**：Copilot vision 正式 GA，chat prompt 可直接附上圖片與 PDF 讓 Copilot 連同程式碼一起推理。

- **圖片／PDF 附件 GA**：可在 chat prompt 直接附加 image 與 PDF，適合把設計稿、錯誤截圖、規格文件直接餵給 Copilot 對照程式碼。

### 2026-07-01（[Set AI credit session limits in Copilot CLI and SDK](https://github.blog/changelog/2026-07-01-set-ai-credit-session-limits-in-copilot-cli-and-sdk)）

**繁中摘要**：Copilot CLI 與 SDK 新增 AI credit session limit，可為單一 session 設定 agent 花費上限，控管自動化 agent 的成本風險。

- **Session 花費上限**：可在 Copilot CLI 與 GitHub Copilot SDK 設定 AI credit session limit，避免長跑或失控的 agent session 燒掉超額 credit——對無人看管的自動化 agent workflow 特別實用。

### 2026-07-01（[Browser tools for GitHub Copilot in VS Code are generally available](https://github.blog/changelog/2026-07-01-browser-tools-for-github-copilot-in-vs-code-are-generally-available)）

**繁中摘要**：VS Code 內的 GitHub Copilot browser tools 正式 GA，agent 可操作瀏覽器；官方同日補充說明權限與網域控制仍由使用者掌握。

- **Browser tools GA**：Copilot 在 VS Code 的瀏覽器工具結束預覽正式開放，agent 可透過瀏覽器驗證前端行為。
- **權限說明補充**：官方同日更新公告，補充哪些 permission 仍由使用者控制、以及既有 network domain 控制的適用方式——啟用前值得確認這些安全邊界設定。

### 2026-07-01（[Copilot CLI auto model selection routes based on task](https://github.blog/changelog/2026-07-01-copilot-cli-auto-model-selection-routes-based-on-task)）

**繁中摘要**：Copilot CLI 的 auto model selection 改為依任務類型路由到最適合的模型，計費說明也改以 AI credits 表述。

- **依任務路由模型**：CLI 中選 auto 時不再是單一預設，而是按任務性質自動挑選最佳模型——想固定用特定模型的 workflow 需明確指定，不要依賴 auto。
- **計費表述更新**：官方同日修訂公告，premium request 成本改以 AI credits 為單位表述。

### 2026-07-01（[Enterprises can default to auto model selection](https://github.blog/changelog/2026-07-01-enterprises-can-default-to-auto-model-selection)）

**繁中摘要**：企業管理員可在 managed settings 把 model 設為 `auto`，讓 Copilot auto model selection 成為新對話的預設，適合想全組織統一走自動選模的團隊。

- **企業層級預設 auto**：在 `managed-settings.json`（`.github-private/.github/copilot/managed-settings.json`）把 model 設為 `auto`，新對話即預設走 auto model selection——搭配前述「依任務路由」的 auto 行為，等於整組織預設交由系統挑模型。

### 2026-07-01（[New C++ language server config skill for Copilot CLI](https://github.blog/changelog/2026-07-01-new-c-language-server-config-skill-for-copilot-cli)）

**繁中摘要**：Microsoft C++ Language Server 上架 Copilot Plugins marketplace，內建一個自動化專案設定的 setup skill，C++ 專案接 Copilot CLI 的初始設定更省事。

- **C++ 專案設定 skill**：新 plugin 附帶 built-in setup skill 協助自動化 C++ 專案設定——C++ 使用者可透過 Copilot CLI plugin marketplace 安裝，簡化 language server 接入流程。

---

## GitHub Changelog

### 2026-07-01（[GitHub Models is being fully retired on July 30, 2026](https://github.blog/changelog/2026-07-01-github-models-is-being-fully-retired-on-july-30-2026)）

**繁中摘要**：GitHub Models 確定於 2026-07-30 完全退役，有依賴其 API 或 playground 的專案需在期限前遷移。

- **退役時程確定**：六月已宣布退役並停收新客戶，現公布 2026-07-30 為完全關閉日——仍在用 GitHub Models 做 model inference 的 workflow 需改用其他 provider。
