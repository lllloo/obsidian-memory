---
title: "這個 AI 技能能取代初級工程師 90% 的工作（Claude Code Agent Teams）"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-09
source: https://youtu.be/PjenU4zwY5U
---

## 影片描述

示範作者自製的 Claude Code Skill「Fix Ticket」，能從讀取 Jira 票券到部署修復、更新票券狀態，全程自動化 bug 修復流水線，涵蓋多代理程式碼審查與 Playwright 自動化測試驗證。

## 重點摘要

### Fix Ticket Skill 是什麼

- 一個 Claude Code Skill，自動化整個 bug 修復流程
- 目標：讓 AI 處理初階工程師的大部分工作（讀票、研究、實作、審查、部署）
- 開源，放在作者的 GitHub（startup-cloud-skills）

### 完整自動化流水線（8 個階段）

1. **Branch Strategy**：詢問在哪個 branch 工作（main / feature branch / work tree）
2. **Read Jira Ticket**：讀取票券描述與所有評論，產生摘要
3. **QA Verify（Playwright）**：用 Playwright CLI Skill 在瀏覽器中重現 bug，截圖確認
4. **Plan**：研究根本原因、製作 bug flow diagram、提出修復方案，請用戶確認
5. **Implementation**：實作修復，執行 build 與 lint 確保通過
6. **Multi-Agent Code Review**：
   - 3 個並行審查代理，從不同角度審查（race condition、edge case、silent failure）
   - 發現問題後自動修正
7. **QA Check**：再次用 Playwright 驗證修復已生效
8. **Vercel Deploy & Jira Handoff**：
   - 每 45 秒輪詢 Vercel 部署狀態
   - 部署成功後在 Jira 留下完整測試說明，並指派給 QA 工程師

### Skill 參數設定

| 參數 | 說明 |
|------|------|
| `ticket` | Jira 票券編號（如 `CAN-191`） |
| `branch` | 工作 branch（main / new / feature / work-tree） |
| `skip_review` | 是否跳過程式碼審查 |
| `skip_jira` | 是否跳過 Jira 更新 |
| `skip_deploy` | 是否跳過 Vercel 部署監控 |
| `skip_qa` | 是否跳過 QA 驗證步驟 |
| `auto_commit` | 是否自動 commit（預設 true） |
| `assign_to` | 完成後指派給誰 |

### 所需 MCP 與工具

- Jira MCP
- Vercel MCP
- Supabase MCP
- Playwright CLI Skill（上一影片介紹）

### 組成結構

Fix Ticket 是一個「mega skill」，內含多個子 Skill：
- `dev-team`：規劃、審查、實作、建立 PR 的代理團隊
- `review-team`：5 個代理組成的 PR 審查團隊（含 devil's advocate 角色）
- `review-fix`：平行代理即時審查修復
- `playwright-cli`：無頭瀏覽器自動化測試

### 核心價值

這個 Skill 複製了初階工程師的典型工作流程：
**讀票 → 研究 → 分析 → 實作 → 審查 → 驗證 → 部署 → 交接**
作者認為可以自動化一名初階工程師約 90% 的日常工作。
