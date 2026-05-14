---
title: BMAD Method 流程
created: 2026-05-13
updated: 2026-05-13
source: https://docs.bmad-method.org/llms-full.txt
tags:
  - claude-code
  - agent-framework
---

BMAD Method 把 agile lifecycle 切成 4 個階段（BMad Method / Enterprise track）。Quick Flow 是平行路徑，用單一 `bmad-quick-dev` 跳過完整 phase 1-3 規劃，處理小型、明確的開發任務。每個階段以特定 agent 為主軸；除了 agent menu triggers 外另有可直接以 skill 名稱呼叫的 workflow skills。

## 目前公司工作流程

| 階段     | 負責     | Skill                          |
| -------- | -------- | ------------------------------ |
| 規劃前期 | PM       | `bmad-product-brief`           |
| 規劃前期 | PM       | `bmad-create-prd`              |
| 架構     | 工程師   | `bmad-create-architecture`     |
| 規劃後期 | PM       | `bmad-create-epics-and-stories` |
| 開發     | 工程師   | `bmad-sprint-planning`         |
| 開發     | 工程師   | `bmad-create-story`            |
| 開發     | 工程師   | `bmad-dev-story`               |

常用 agent skill 對照：

| Agent                    | 先載入的 skill     |
| ------------------------ | ------------------ |
| Analyst (Mary)           | `bmad-analyst`     |
| PM (John)                | `bmad-pm`          |
| Architect (Winston)      | `bmad-architect`   |
| Developer (Amelia)       | `bmad-agent-dev`   |
| UX-Designer (Sally)      | `bmad-ux-designer` |
| Technical Writer (Paige) | `bmad-tech-writer` |

## 階段 1 — 分析

由 Analyst (Mary) 主導。全選填（打底用，可省略），但 `CB` 強烈建議執行。

| 代號 | 動作                      | Agent   | Skill                     | 必填 | 備註                               |
| ---- | ------------------------- | ------- | ------------------------- | ---- | ---------------------------------- |
| `BP` | Brainstorming             | Analyst | `bmad-brainstorming`      | —    |                                    |
| `MR` | Market Research           | Analyst | `bmad-market-research`    | —    |                                    |
| `DR` | Domain Research           | Analyst | `bmad-domain-research`    | —    |                                    |
| `TR` | Technical Research        | Analyst | `bmad-technical-research` | —    |                                    |
| `CB` | Create Product Brief      | Analyst | `bmad-product-brief`      | —    | 建議執行，後續 `CP` PRD 會比較準確 |
| `WB` | PRFAQ / Working Backwards | Analyst | `bmad-prfaq`              | —    | 用 Working Backwards 壓力測試概念  |

## 階段 2 — 規劃

| 代號 | 動作             | Agent               | Skill                   | 必填 | 備註                   |
| ---- | ---------------- | ------------------- | ----------------------- | ---- | ---------------------- |
| `CP` | Create PRD       | PM (John)           | `bmad-create-prd`       | ⭐   | 輸出 `PRD.md`          |
| `VP` | Validate PRD     | PM                  | implicit review         | —    |                        |
| `EP` | Edit PRD         | PM                  | implicit edit           | —    | `VP` 後修訂            |
| `CU` | Create UX Design | UX-Designer (Sally) | `bmad-create-ux-design` | —    | Optional；有 UI 才需要 |

## 階段 3 — 方案設計

Architecture drives stories。

| 代號 | 動作                           | Agent               | Skill                                 | 必填 | 備註                              |
| ---- | ------------------------------ | ------------------- | ------------------------------------- | ---- | --------------------------------- |
| `CA` | Create Architecture            | Architect (Winston) | `bmad-create-architecture`            | ⭐   | 輸出 `architecture.md`            |
| `CE` | Create Epics & Stories         | PM                  | `bmad-create-epics-and-stories`       | ⭐   | 需 PRD + Architecture 同時就位    |
| `IR` | Check Implementation Readiness | PM / Architect      | `bmad-check-implementation-readiness` | —    | Highly Recommended，cohesion 檢查 |

## 階段 4 — 實作

由 Developer (Amelia) 主導。`SP` 後進 Story 循環。

| 代號 | 動作               | Agent     | Skill                        | 必填 | 備註                                   |
| ---- | ------------------ | --------- | ---------------------------- | ---- | -------------------------------------- |
| `SP` | Sprint Planning    | Developer | `bmad-sprint-planning`       | ⭐   | 輸出 `sprint-status.yaml`              |
| `CS` | Create Story       | Developer | `bmad-create-story`          | ⭐   | 每張 Story 起點                        |
| `DS` | Dev Story          | Developer | `bmad-dev-story`             | ⭐   | 實作                                   |
| `CR` | Code Review        | Developer | `bmad-code-review`           | —    | 品質驗證                               |
| `QA` | QA E2E Tests       | Developer | `bmad-qa-generate-e2e-tests` | —    | Epic 全部 stories 完成並 review 後選跑 |
| `ER` | Epic Retrospective | Developer | `bmad-retrospective`         | —    | **Epic 完成後**才跑，非 per-story      |
| `QD` | Quick Dev          | Developer | `bmad-quick-dev`             | —    | bug fix / 小改動一站式                 |
| `CC` | Correct Course     | PM        | `bmad-correct-course`        | —    | 中途改 scope                           |

Story 循環（官方 build cycle 三步）：

```
CS ⭐ → DS ⭐ → CR（recommended） → 下一個 Story
```

`QA` 是 epic-level 驗證：全部 stories 完成且跑過 `CR` 後選跑；完成該 epic 後再跑 `ER` → 下個 Epic 或結束。

## Technical Writer (Paige)

獨立 agent，與四階段平行；可在任何階段需要寫文件時使用。

| 代號 | 動作             | 觸發類型                     | 用途                       |
| ---- | ---------------- | ---------------------------- | -------------------------- |
| `DP` | Document Project | workflow（Analyst 也有）     | 對既有 codebase 產文件     |
| `WD` | Write Document   | conversational（需描述需求） | 自訂文件撰寫               |
| `US` | Update Standards | conversational               | 補充慣例 / standards       |
| `MG` | Mermaid Generate | conversational               | 產 sequence / flowchart 等 |
| `VD` | Validate Doc     | conversational               | 文件驗證                   |
| `EC` | Explain Concept  | conversational               | 解釋概念                   |

## Skills（直接以 skill 名稱呼叫，不需透過 agent menu）

所有 workflow 都是 skill；下表是常從 skill 入口（而非 agent trigger）呼叫的橫向工具與替代入口。

| Skill                           | 用途                                                                        |
| ------------------------------- | --------------------------------------------------------------------------- |
| `bmad-help` ⭐                  | 智能導引，回答 80% 操作問題（檢視專案狀態給「下一步」建議）                 |
| `bmad-customize`                | 引導式客製化（per-skill agent/workflow override）                           |
| `bmad-party-mode`               | 多 agent 圓桌討論，BMad Master 主持                                         |
| `bmad-advanced-elicitation`     | 對 LLM 生成結果套用 reasoning method 重新檢視                               |
| `bmad-generate-project-context` | 產 `project-context.md`；供 implementation workflows 與 architecture 參考   |
| `bmad-quick-dev`                | Quick Flow 一站式（亦可由 Developer 的 `QD` trigger 進入）                  |
| `bmad-document-project`         | 對既有 codebase 產文件（亦可由 Analyst / Tech Writer 的 `DP` trigger 進入） |

## 必經節點

僅這 6 個是必走（BMad Method / Enterprise track；Quick Flow 用 `bmad-quick-dev` 一站到底）：

1. `CP` Create PRD
2. `CA` Create Architecture
3. `CE` Create Epics & Stories
4. `SP` Sprint Planning
5. `CS` Create Story（每張 Story 內）
6. `DS` Dev Story（每張 Story 內）

## 關鍵規則

- **Fresh chats required**：每個 workflow 開新 session，避免上下文污染
- **Architecture drives stories**：`CE` 必在 `CA` 之後
- **Project context optional**：可手動建立或用 `bmad-generate-project-context`；implementation workflows 會載入，architecture 也會讀取技術偏好
- **`bmad-help` 隨時可用**：卡住先問它

## 相關

- [[BMAD框架]] — 框架定位與 12+ persona 介紹
