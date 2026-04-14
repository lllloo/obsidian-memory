---
title: Anthropic 團隊在生產環境使用的 Claude Skills 與工具
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-03
source: https://www.youtube.com/watch?v=AhXfI1rSUPc
---

## Frontend Design Plugin（開源）

- 用途：用簡潔 prompt 將設計轉換成 UI，同時提升 UI/UX 品質
- 核心目標：避免 AI 收斂到相同的通用 AI 審美（常見紫白藍白配色）
- 安裝：Claude Code 官方 plugin marketplace，或用 `plugins add marketplace` 指令
- 安裝後可直接用 `/` 指令調用，或 Claude 在需要時自動觸發

## Batch Skill（內建）

- 用途：自動化可並行的任務（如：把某個 library 的用法全面改成另一個）
- 與一般 agent 分工的差異：使用獨立的 **work tree**（repo 的隔離副本），各 agent 互不干擾
- 流程：
  1. 進入 plan mode，分析任務並拆解成工作單元
  2. 核准計畫後，spawn 對應數量的 agents，每個在獨立 work tree 執行
  3. 各 agent 回報進度，完成後主 agent 合併所有 work tree
  4. 若設定了 remote，可自動管理 PR

## Code Simplifier Plugin（開源）

- 用途：重構程式碼提升清晰度，同時保留功能
- 安裝方式：與 Frontend Design Plugin 相同，從官方 plugins repo 安裝
- 執行後：spawn 單一 agent 掃描整個 codebase，移除重複與不必要的檔案

**與內建 `simplify` skill 的差異：**
- `simplify` 會 spawn 三個 agents，從多個指標嚴格評估，是更徹底的版本

## Verify Skill（內部工具，未公開）

- 用途：執行 app、從多角度測試變更、自動修復失敗
- 目前隱藏在 CLI flag 後，system prompt 直接注入環境，非常 project-specific
- 可用 skill creator 或官方 repo 作為模板，為自己的專案建立對應的 verify skill
- 驗證方式依專案而異，可整合 Playwright MCP 視覺驗證、CLI 工具、linter、npm test

## Skillify Skill（內部工具，未公開）

- 用途：錄製一次完整的工作流程對話，自動產出可重用的 skill
- System prompt 包含在原始碼中（可參考洩漏版本）
- 流程：
  1. 與 Claude 進行工作流程的腦力激盪對話
  2. 調用 Skillify 後，它分析整個 session
  3. 確認可重複流程、所需工具與 agents
  4. 與用戶確認推論，追問細節，最終生成 `skill.md`
- 可用 skill creator skill（開源）自行建立等效工具

## Security Scan Command（已內建）

- 用途：掃描 codebase 的安全漏洞並建議修補
- 涵蓋面向：輸入驗證、身份驗證、Secret 管理、Injection、程式碼執行、Endpoint 暴露等
- 直接在 Claude Code 執行安全審查，回報後可進一步請 Claude 修復

## Commit-Push-PR Command（開源）

- 用途：一鍵 commit、push 到 repo 並開啟 Pull Request
- 可在 Claude Code 官方 plugin marketplace 搜尋 `commit` 安裝
- 包含 commit 生成工作流程，適合整合進重複性任務

## Tech Debt Skill（內部工具，未公開）

- 用途：每次 session 結束時執行，找出重複程式碼並清理技術債
- 建議自行建立，用 skill creator 生成，依專案客製化

**Tech Debt Skill 應包含的指示：**
- 如何識別變更
- 如何偵測重複項目
- 檔案結構的處理方式
- 結尾驗證步驟（執行 npm test、linter）

執行後：用多個 agents 並行分析 codebase → 回報冗餘 → 建立共用 library → 更新相關 components

## Dedupe Skill（內部工具，未公開）

- 用途：檢查 GitHub issue 是否為重複，若是則自動留言說明
- 判斷邏輯：確信度達 ~70% 才標記為重複
- 適合多人協作專案，避免重複處理相同問題

## Remotion Skill（可安裝）

- 用途：用簡單 prompt 建立動態圖形與影片
- Anthropic 行銷團隊用於製作所有產品宣傳影片
- 可直接在 Claude Code 中安裝使用
