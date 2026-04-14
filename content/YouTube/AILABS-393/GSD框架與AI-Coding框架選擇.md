---
title: GSD 框架與 AI Coding 框架的選擇策略
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: ""
source: https://www.youtube.com/watch?v=uEit1oOJK0w
---

## 三大框架的定位比較

### GSD（Get Shit Done）

**適用場景：**
- 需求不確定、需要大量實驗的專案
- 快速打造 MVP
- 從未有人做過的客製化解法（例：做一個 on-screen interview assistant，螢幕分享時需躲避偵測）

**特色：**
- 詢問 broad scope，但不鎖死後期細節
- 逐步規劃每個實作步驟，每個 phase 獨立計畫
- 使用子 agent 平行處理獨立任務，防止主 agent context 污染（context rot prevention）
- 計畫透過 adversarial planning 自動交叉驗證（planning agent + verifier agent 互相挑戰）
- 安裝後設定保存在 `.claude/` 下（agents、commands、hooks），使用 XML 格式的 prompt（Claude 對 XML 結構解析更精準）

### BMAD Method

**適用場景：**
- 需求確定、不需要彈性調整的大型系統
- 要求完整文件、嚴格執行的專案（如客製 CRM、社群平台）
- 不需要中途變更需求

**特色：**
- 從 Business Analyst、Design Thinker 等角色出發，進行全面前期研究
- 生成 PRD 與架構文件，再拆分成 sharded tasks
- 需求變更時系統容易不穩定（模型容易漏掉細節）
- 缺點：前期規劃時間長，適合需求鎖定的場合

### Superpowers（TDD 框架）

**適用場景：**
- 邊緣案例成本極高的系統（如 AI agent 代替用戶執行不可逆操作的平台）
- 對品質要求高、需要測試先行的場合

**特色：**
- 先生成測試，再實作
- 規劃按 feature 進行，僅有 outline，不預先詳規
- 不適合實驗性強或需求變動的專案

**混合使用策略：** 先用 GSD 完成主功能，再引入 Superpowers 接手後續開發。

## GSD 安裝與使用

```bash
# 在專案資料夾下安裝（選 project level 保持各專案獨立設定）
# 安裝後 .claude/ 下會出現 agents、commands、hooks
```

啟動新專案：

```bash
/new-project
```

- 會先掃描現有 codebase（可跳過空白專案）
- 詢問 app 想法、目標用戶、功能範圍等
- 生成 `.planning/project.md`（刻意保持短小精煉，避免 agent 迷失在文件中）

## GSD 工作流程

### Phase 1：初始化

1. 執行 `/new-project`
2. 回答 app 想法、用途、範圍
3. GSD 生成 `project.md`（含 out-of-scope 清單、context constraints、key decisions）
4. 進入研究階段：多個 sub-agent 平行研究不同面向，完成後由 **synthesizer agent**（使用較輕量的 Sonnet 模型）整合並標示潛在風險
5. MVP 需求確認：GSD 只問哪些功能 V1 真正需要，聚焦快速交付
6. 批准 roadmap，初始化完成

### Phase 2：逐 phase 實作

1. 選擇「with discussion」或「skip discussion」
2. Discussion 模式：agent 追問確認需求，生成 `.planning/phases/<phase>/context.md`（同樣刻意精簡）
3. 研究 → 計畫（planning agent 生成，verifier agent 交叉驗證）→ 計畫通過後 commit
4. 計畫拆成多個 wave，獨立 wave 平行執行
5. 每個 wave 完成後用 **Playwright 自動測試**驗證（腳本用完即刪）
6. 呈現 summary + 驗證指引，等待人工批准後進入下一 phase

### Context 管理

- 使用 git 追蹤所有工作（commit 前有 pre-commit 品質檢查腳本）
- 每個 sub-agent 使用適合其工作量的模型（輕任務用 Sonnet，重任務用 Opus）
- 即使清空 context，agent 也能從文件重新定位繼續工作

## 適用邊界

| 情境 | 建議 |
|------|------|
| 需求模糊、大量實驗 | GSD |
| 需求確定、要求嚴謹文件 | BMAD |
| 高成本邊緣案例、TDD | Superpowers |
| 簡單小型 app | 直接用 Claude，不需框架 |

GSD 在功能完整的大型 app 表現良好，但對簡單應用屬於 overkill。
