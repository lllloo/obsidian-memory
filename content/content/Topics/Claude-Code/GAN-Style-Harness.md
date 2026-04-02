---
title: GAN Style Harness
tags:
  - claude-code
  - ai-tools
created: 2026-04-02
updated: 2026-04-02
---

模仿 GAN（生成對抗網路）概念的多 agent 協作系統，三個 agent 透過對抗式迴圈反覆提升產出品質。來自 [everything-claude-code](https://github.com/affaan-m/everything-claude-code) 的 gan-style-harness skill，靈感源自 Anthropic 2026/03 的 harness 設計論文。

## 三個角色

| Agent | 角色 | Model | 說明 |
|-------|------|-------|------|
| gan-planner | PM（紫色） | Opus | 把一句話需求展開為完整產品規格（功能、sprint、設計方向、評分標準） |
| gan-generator | 開發者（綠色） | Opus | 按規格實作，每輪讀取 evaluator 回饋逐項修正 |
| gan-evaluator | QA（紅色） | Opus | 用 Playwright 測試實際運行的應用，四維度加權打分，殘酷地嚴格 |

## 工作流程

```
用戶一句話需求
    ↓
[gan-planner] → spec.md + eval-rubric.md
    ↓
[gan-generator] → 實作 → 啟動 dev server
    ↓
[gan-evaluator] → Playwright 測試 → 打分 → feedback.md
    ↓
    分數 < 7.0 → 回到 generator 修正（反覆 5-15 輪）
    分數 ≥ 7.0 → PASS
```

## 評分標準

四維度加權，門檻 7.0/10：
- Design Quality（0.3）— 視覺一致性與辨識度
- Craft（0.3）— 排版、間距、動畫、micro-interaction
- Originality（0.2）— 是否有自己的設計語言，而非 AI 味模板
- Functionality（0.2）— 功能是否完整、edge case 處理

分數校準：7 = junior 紮實作品，9 = senior 水準，10 = 可上線產品

## 使用方式

在 Claude Code 對話中直接說：「用 GAN harness 做一個 [需求]」

或 CLI 手動跑：

```bash
claude --agent gan-planner -p Build