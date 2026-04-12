---
title: Claude Code Now DESTROYS Web Design with Stitch 2.0
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/qqcpiDXPCvY
---

介紹 Google Stitch 2.0 與 Claude Code 的整合工作流程，補強 Claude Code 在前端設計的弱點。Stitch 2.0 推出後，Figma 股價下跌近 8%。

## Stitch 2.0 是什麼

- Google 推出的免費前端設計工具，Gemini 3.1 驅動
- 提供無限畫布，可視覺化瀏覽與快速迭代設計原型
- 可匯出設計為程式碼，複製到剪貼簿後貼入 Claude Code

## 工作流程

1. **尋找靈感** — 從 Dribbble、godly.website、Pinterest 找參考截圖
2. **在 Stitch 生成設計** — 上傳截圖，描述需求，Stitch 自動生成 Design System（含色彩策略、排版規則）
3. **迭代優化** — 一鍵 Regenerate，或生成多個 Variants（佈局、配色、圖片）
4. **匯出至 Claude Code** — More → Export → Code to Clipboard，貼入 Claude Code 生成完整前端

## 重點功能

- **Design System 文件**：Stitch 自動產生設計指導文件，包含創意定位、色彩策略、排版規則，確保遠離「AI 風格爛設計」
- **Live Mode**：即時對話模式，可直接對畫面上的設計下指令
- **Variants**：同時生成多個不同風格的設計方案

## 核心價值

- Claude Code 本身在前端設計偏弱，Stitch 填補這個缺口
- 設計過程完全不消耗 Claude Code token（Gemini 負擔）
- 後續部署：Claude Code → GitHub → Vercel
