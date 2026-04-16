---
title: Claude Code + Superpowers 框架：提升 AI 編程準確度完整教學
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-31
source: https://www.youtube.com/watch?v=TX91PdBn_IA
parent: "[[01.index]]"
---

## 為什麼使用 Superpowers

Superpowers 的核心賣點是**測試驅動開發（TDD）**，這是大型科技公司廣泛採用的開發框架。

- 與 GSD、SpecKit、BDD 等框架不同，Superpowers 強制先寫測試再寫程式碼
- 先定義期望行為（tests），再實作，最後重構（refactor）——不斷循環直到無需重構
- 使用 Git worktrees 隔離開發環境，支援多個實作同時進行
- 將任務分派給不同 sub-agent，每個 sub-agent 擁有乾淨的 context window，避免 context rot

## 完整開發流程

1. **Brainstorm**：確認完整計劃，Claude Code 會提出 UI mockup（HTML 頁面）讓用戶選擇設計方向
2. **Spec**：生成包含 context、設計決策、架構、API routes、edge cases、acceptance criteria 的規格文件（存於 `docs/` 資料夾）
3. **Implementation Plan**：用 `writing plan` skill 將 spec 轉換為帶 checkbox 的任務清單，每個任務細分為測試→實作→驗證步驟
4. **Execution**：兩種模式
   - **Sub-agent driven**（推薦）：每個任務派一個新 sub-agent，可在任務間 review
   - **Inline/batch execution**：在同一 session 批次執行，帶 checkpoints
5. **Code Review**：完成後觸發 code review skill，發現 critical issues 並派 fix agent 修正
6. **PR**：將 Git worktree merge 到 main branch，建立 PR 供團隊 review

## 安裝方式

```bash
# 透過 Claude Code 官方 marketplace 安裝
# 或透過 plugins marketplace 安裝（效果相同）
```

安裝後用 `plugins` 指令管理，可查看 description、commands、agents、skills，也可 disable/uninstall。

## 實際案例

以 Bookworm.ai 為例，新增「重新同步 Google Drive 資料夾」功能：

- 整個 11 個任務的實作計劃，每個任務先跑 failing test → 實作 → 驗證通過 → commit
- Code review 發現 stale credits、confirmed selections、misleading metadata 等問題，由 fix agent 自動修正
- 功能驗證：點擊 sync connected folder 後，成功偵測並匯入 6 個新增的 Google Drive 檔案

## 核心觀念

- 傳統開發 vs Superpowers：後者更現代化——使用 worktrees、sub-agent 分工、TDD 保障測試覆蓋率
- `slash command` 中的 `plan`、`brainstorm`、`execute plan` 已 deprecated，應直接觸發 Superpowers skills
