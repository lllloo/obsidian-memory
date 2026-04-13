---
title: GSD vs Superpowers vs Claude Code：新 AI 之王？
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-12
source: https://www.youtube.com/watch?v=celLbDMGy8w
---

## 描述

GSD、Superpowers、原生 Claude Code 三方頭對頭測試，比較最終輸出品質、使用 token 數量與完成時間。

## 重點摘要

**GSD 與 Superpowers 的共同點**
- 兩者都是架設在 Claude Code 之上的 orchestration 層
- 導入更完善的計畫系統與測試系統
- 皆使用 sub-agent 驅動開發來對抗 context rot（上下文腐化）
- 流程相似：討論計畫 → 拆分成原子任務 → 由子 agent 執行

**核心差異**
- Superpowers：強調 TDD（測試驅動開發），遵循「沒有失敗測試就不寫生產程式碼」的鐵律；另有 Visual Companion 功能，可在 dev server 上直接比對多款設計方案
- GSD：強調狀態與上下文管理，以 markdown 檔案（requirements.md、roadmap.md、各階段文件）記錄計畫進度，作為子 agent 間的北極星

**測試內容**
- 任務：為 AI 代理公司建立包含落地頁、部落格列表、部落格生成器（含 Anthropic SDK 呼叫）的完整網站
- 刻意留下詮釋空間（YouTube 逐字稿抓取方式、縮圖策略、部落格語氣設定），觀察三者的自主判斷能力

**Superpowers 亮點**
- 安裝後自動載入 14–15 個 skills，根據對話情境自動選用
- Visual Companion 一次呈現 4 種設計方案供選擇
- 初始溝通時回饋更詳盡，提供帶有優缺點對比的選項

**GSD 亮點**
- 使用 `/gsd new project` 等明確的 slash 指令啟動
- 最先回應並確認計畫細節
- 計畫文件（project.md）結構清晰

**安裝方式**
- Superpowers：在 Claude Code 內執行 `/plugin` 搜尋即可安裝
- GSD：執行單行安裝指令即完成
