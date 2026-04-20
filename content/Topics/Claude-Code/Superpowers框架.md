---
title: Superpowers 框架
created: 2026-04-20
updated: 2026-04-20
tags:
  - claude-code
  - agent-framework
  - tdd
---

Claude Code 上的 TDD 強制執行 plugin。涵蓋是什麼、與 GSD/GStack 的位置差異、完整開發流程、安裝與使用、效能與成本、何時該用。

## 核心概念

**Superpowers** 是以 **TDD（測試驅動開發）** 為核心的 Claude Code plugin，由 **Jesse Vincent（Prime Radiant）** 開發，GitHub 帳號 `obra/superpowers`，截至 2026-04 已累積 **161K+ stars**。

與單純的 spec 框架不同，Superpowers 是**「執行強制」**：未通過當前 gate 不得進入下一步。鐵律：**沒有失敗測試就不寫生產程式碼**（red-green-refactor）。

內建能力：
- **TDD gate**：agent 先寫測試再寫實作，測試失敗時禁止修改測試檔案
- **Git worktree 自動隔離**：每個 sub-agent 一個獨立 worktree，互不覆蓋
- **Sub-agent 分工**：brainstorm / plan / implement / review 各自乾淨 context；每個任務拆到 **2–5 分鐘粒度**
- **Two-stage code review**：spec compliance + code quality 兩階段檢核
- **Systematic Debugging**：四階段（定位→隔離→縮小→修復+驗證）
- **Socratic brainstorm**：以問答方式收斂需求

## 完整開發流程

1. **Brainstorm** — 主動提問釐清 app、目標用戶、tech stack，給三個架構方案與 UI mockup 選擇
2. **Spec** — 生成含 context、設計決策、架構、API routes、edge cases、acceptance criteria 的文件（存 `docs/`）
3. **Implementation Plan** — `writing plan` skill 把 spec 轉成 checkbox 任務清單，每項細分為測試→實作→驗證
4. **Execution**（兩種模式）
   - Sub-agent driven（推薦）：每任務一個新 sub-agent，任務間可 review
   - Inline/batch：同一 session 批次執行，帶 checkpoints
5. **Code Review** — 完成後 code review skill 偵測 critical issues，派 fix agent 修正
6. **PR** — worktree merge 回 main 並建 PR

全程自動 Git commit（與其他框架差異點）。

## 在三框架中的位置

| 面向 | Superpowers | GSD | GStack |
|------|-------------|-----|--------|
| 約束目標 | 流程（Process） | 環境（Context < 50%） | 視角（Perspective） |
| 核心機制 | TDD gates | 每階段換 orchestrator、狀態持久化 | 多 persona 審查 |
| 擅長階段 | 實作（TDD） | 專案管理、里程碑 | 策略規劃、QA |

詳細對比見 [[GSD框架]]、[[GStack框架]]。

## 安裝

在 Claude Code 內執行：

```
/plugin install superpowers@claude-plugins-official
```

安裝後用 `plugins` 指令管理（view description / commands / agents / skills，可 disable/uninstall）。

**注意**：舊版的 slash command（`plan`、`brainstorm`、`execute plan`）已 deprecated，改直接觸發 Superpowers skills。

## 效能實測（社群）

在 brownfield 專案新增端對端測試覆蓋率，與 GSD 同場競技（單一作者實測）：

| 指標 | Superpowers | GSD |
|------|------------|-----|
| 測試數 | 107（103 通過） | 110（102 通過） |
| 功能覆蓋率 | 46% | 53% |
| Token 消耗 | 勝出（比 GSD 省 5–7 倍） | 較高 |
| 修復 bug 數 | 約 10 | 4 |
| 迭代次數 | 1 輪 fix cycle | 2 輪 fix cycle |
| Token 分配 | 實作 60–70%、修復 20–30%、審查 10% | 實作僅 25% |

另一組「從零建 AI 代理公司網站」的三方對打（社群實測）：

| 指標 | Claude Code 原生 | Superpowers | GSD |
|------|------------------|-------------|-----|
| 總時間 | ~20 分鐘 | ~60 分鐘 | ~105 分鐘 |
| 總 token | ~200K | ~250K | ~1.2M |

Superpowers 在 token 效率上明顯勝出 GSD，但仍比原生 Claude Code 慢 3 倍。

## 何時該用

- **適合**：邊緣案例成本極高的系統（AI agent 代執行不可逆操作、金流、安全敏感）、需要 TDD 品質關卡、長期維護的生產程式碼
- **不適合**：純實驗、需求未定、快速 MVP、純 UI 調整（可只走 brainstorm + plan，實作改由原生 Claude 直接處理）
- **混合**：先用 GSD 做主功能，Superpowers 接手後續開發與測試（社群策略）

## 常見陷阱

**Context 消耗快**
- 徵兆：一輪迭代後 context 逼近滿載
- 原因：brainstorm + spec + implementation plan 文件都塞進 session
- 解法：約 50% context 時執行 `/compact`，或切 sub-agent 執行

**小任務殺雞用牛刀**
- 徵兆：簡單 UI 改動也走完整六階段，等待規劃時間遠超實作時間
- 原因：不是每個任務都需要 TDD gate
- 解法：Claude 擅長的事讓它直接做；容易失敗的複雜實作才啟動完整流程

**輸出品質相近時，時間差才是勝負關鍵**
- 徵兆：花 60 分鐘跑完 Superpowers 結果和原生 Claude 20 分鐘差不多
- 原因：Opus 4.5+ 後的 context 焦慮已緩解，框架填補的空缺縮小
- 解法：99% 情境用原生 Claude Code，真正複雜才啟動 Superpowers（社群建議）

## 來源

**官方 / 開發者**
- [obra/superpowers (GitHub)](https://github.com/obra/superpowers) — Jesse Vincent, Prime Radiant
- [Anthropic Claude Plugin 頁](https://claude.com/plugins/superpowers)

**影片 / 社群**
- https://www.youtube.com/watch?v=romGzY0Xu0s
- https://www.youtube.com/watch?v=TX91PdBn_IA
- https://www.youtube.com/watch?v=GJmlik1C4Tg
- https://www.youtube.com/watch?v=celLbDMGy8w
- https://www.youtube.com/watch?v=bzutStZJ1Ig
- https://www.youtube.com/watch?v=D5bRTv6GhXk
