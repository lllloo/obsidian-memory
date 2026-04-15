---
title: Gemini 3.1 Pro 在 Antigravity 的應用展示
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-24
source: https://www.youtube.com/watch?v=mAwJYUJib1I
---

## 概覽

- Gemini 3.1 Pro 可能是目前最強的 AI 模型，可在 Anti-Gravity 中免費使用。
- Anti-Gravity 是 Google 的 AI 程式開發工具，競爭對手為 Cursor 和 Claude Code。

## Benchmark 表現

- **ARC-AGI 2**（抽象推理）：77%，遠超 Opus 4.6 和 GPT-5.2
- **GPQA Diamond**（科學問答）：94%，再次領先競爭對手
- **Browse Comp**（Agentic 搜尋）：85%，微幅領先 Opus 4.6

## Anti-Gravity 安裝設定

1. 搜尋並下載 Anti-Gravity，支援從 Cursor/VS Code 匯入設定。
2. 選擇開發模式：嚴格模式（需確認每步）、Review-Driven（推薦）、Agent-Driven（最積極，本影片使用）。
3. 用 Google 帳號登入即可免費使用 Gemini 3.1 Pro（Google AI 付費方案可獲得更高配額與速度）。

## Anti-Gravity 的核心優勢

- **Agent Manager**：與其他 IDE 最大的差異，可以輕鬆管理並協調多個 AI Agent 同時在同一專案工作。
- Agent 不只寫程式，還能自行開啟瀏覽器、截圖、測試 UI——當瀏覽器出現藍色外框時表示 Agent 正在自主控制。

## 實作：地緣政治風險儀表板

### 專案描述

- 全棧網頁 App，以 3D 旋轉地球展示即時地緣政治風險。
- 資料來源：Firecrawl API（新聞、油價、航班禁區、國防股票行情）。

### 開發流程

1. 建立 `idea.md` 描述專案願景。
2. 先切換到「規劃模式」讓 Gemini 制定步驟計畫，確認後再切換到「執行模式」。
3. Gemini 自動建立完整資料夾結構，並在過程中自行開啟瀏覽器驗證效果。
4. 主動下載 curl 紋理貼圖改善 3D 地球外觀。
5. 透過簡短指令（「地球看起來太暗，修掉那個色調」）即時調整效果。

### Firecrawl 整合

- Firecrawl 是為 AI Agent 設計的開源網路爬取 API，輸出乾淨的 Markdown 或結構化 JSON。
- 免費方案提供 500 次爬取，使用優惠碼 `david` 額外獲得 1000 次。
- 前往 firecrawl.dev 建立帳號，在 Anti-Gravity 中貼入 API key 即可使用。

### 最終成果

- 成功渲染帶有顏色編碼的 3D 地球，不同地區顯示對應風險等級。
- 側邊欄即時顯示：最新情報、油價、防衛股票行情、航班警告。
- 點擊地球上的事件熱區可查看詳情（伊朗風險 64/100，烏克蘭次之）。

## 模型使用建議

| 使用情境 | 推薦模型 |
|---------|---------|
| 複雜後端/技術問題 | Opus 4.6 |
| 最佳編程能力 | GPT-5.3 Codex |
| 前端設計/Landing Page | Gemini 3.1 Pro |
| SVG 動畫/視覺設計 | Gemini 3.1 Pro（在設計競技場排名第一） |

## 使用注意事項

- Gemini 3.1 Pro 在 Anti-Gravity **表現最佳**，在其他工具中效果差很多。
- 在 OpenClaw 中測試時出現無限訊息迴圈，表現不穩定。
- 原因：Google 為 Anti-Gravity 專門優化了 Gemini 的整合，在其他工具中 API 層品質較差。
- 建議：在 Anti-Gravity 以外的工具，繼續使用 Opus 4.6 或 GPT-5.3 Codex。

## Gemini 3.1 Pro 的設計優勢來源

- Google 擁有 YouTube、Google 搜尋、Android 等平台的大量多模態訓練資料。
- 更豐富的圖像、影片訓練資料讓 Gemini 3.1 在視覺與設計任務上有天然優勢。
- 在 SVG 動畫設計競技場（Design Arena）以大幅差距排名第一。
