---
title: "2026-07-31 Daily Updates"
created: 2026-07-31
updated: 2026-07-31
tags:
  - updates
  - codex
  - opencode
  - copilot
---

## OpenAI Codex

### v0.146.0 · 2026-07-29（[Changelog](https://learn.chatgpt.com/docs/changelog)）

**繁中摘要**：這版聚焦連線管理、外掛與 thread 功能：新增 session 命名／pin、thread fork、遠端 Code Mode 連線，以及更完整的 proxy 支援。

- **Session/Thread 強化**：可用 `/new` 或 `/clear` 為新 session 命名、pin 重要 thread，並可在側邊對話間切換而不需關閉當前 session。
- **Plugin marketplace 擴充**：新增 Agent Plugins manifest 支援、workspace plugin 發佈，並加入 Amazon Bedrock 與 Claude Code 的 plugin marketplace。
- **Thread forking**：支援分頁式歷史記錄 fork，含不出現在 thread 列表中的暫時性 fork。
- **Remote Code Mode**：app-server 現可透過 WebSocket 連線遠端 Code Mode host。
- **Proxy 支援**：認證、plugin 下載、MCP 授權、遠端執行、WebSocket 與轉址全面支援設定的 proxy。

---

## OpenCode

### v1.18.10 · 2026-07-30（[Changelog](https://opencode.ai/changelog)）

**繁中摘要**：Core 新增 Modal 模型自動探索（不需手動設定即可用），Desktop 端則以一批 UI／穩定性修復為主。

- **Modal 模型自動探索**：系統現在會自動偵測可用的 Modal 模型，模型選擇不需再手動設定。
- **Desktop 穩定性修復**：修正 attachment 重複、tab 損毀後無法修復、custom agent picker 設定遺失等問題；另改善 toast 通知堆疊／關閉行為與 tab hover/active 樣式。

---

## GitHub Copilot

### 2026-07-30（[GitHub Copilot in Visual Studio — July update](https://github.blog/changelog/2026-07-30-github-copilot-in-visual-studio-july-update)）

**繁中摘要**：Visual Studio 版 Copilot 七月更新推出基於 Copilot SDK 的新 agent，並內建 .NET 與 Azure 團隊的專業知識，另提供更多客製化方式。

- **新 agent**：改用 Copilot SDK 打造。
- **內建領域知識**：整合 .NET 與 Azure 團隊的專業建議，提升相關情境下的回答品質。
- **更多客製選項**：提供更多方式調整 Copilot 在 Visual Studio 中的行為。

### 2026-07-30（[Limit remote control to managed devices](https://github.blog/changelog/2026-07-30-limit-remote-control-to-managed-devices)）

**繁中摘要**：企業與組織管理員現可透過新的 `remoteControl` policy 限制哪些裝置能作為 Copilot 遠端控制 session 的 host，強化遠端存取的安全管控。

- **新 policy 設定**：`remoteControl` 讓管理員限定可承載遠端控制 session 的裝置範圍，屬 security posture 相關變更。

### 2026-07-27（[Manage GitHub Copilot app access with a dedicated policy](https://github.blog/changelog/2026-07-27-manage-github-copilot-app-access-with-a-dedicated-policy)）

**繁中摘要**：GitHub Copilot app 現有獨立的存取 policy，企業與組織層級可單獨控管其存取權，不再綁在整體 Copilot 存取設定上。

- **獨立 policy**：Copilot app 存取權可與其他 Copilot 存取設定分開管理，方便更細緻的權限治理。

### 2026-07-27（[Enterprise managed settings in the GitHub Copilot app and Copilot cloud agent](https://github.blog/changelog/2026-07-27-enterprise-managed-settings-now-apply-to-the-github-copilot-app)）

**繁中摘要**：Enterprise managed settings 現已擴及 GitHub Copilot app 與 Copilot cloud agent，管理員可用同一套集中管理政策統一治理這兩者。

- **政策涵蓋範圍擴大**：企業原本用來管控 Copilot 的集中式政策，現在同時適用於 Copilot app 與 cloud agent。

---
