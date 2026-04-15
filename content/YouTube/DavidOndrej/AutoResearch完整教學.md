---
title: AutoResearch 完整教學
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-27
source: https://www.youtube.com/watch?v=uBWuKh1nZ2Y
---

## 什麼是 AutoResearch

- AutoResearch 是 Andrej Karpathy 的開源專案，讓 AI 自主改善自身表現。
- 核心概念：AI Agent 自動跑實驗，保留有效的，丟棄無效的，循環不斷。
- Karpathy 在優化 GPT-2 訓練腳本時靈光一閃：「為什麼不讓 AI Agent 自己跑實驗？」
- 在睡覺的時候，可以跑約 100 個實驗，天亮時看結果。

## Andrej Karpathy 是誰

- OpenAI 共同創辦人之一，Tesla Autopilot 主要負責人，發明「vibe coding」一詞。
- 對開源社群貢獻卓著，尤其在 AI 領域。

## 運作機制

- **三個核心檔案**：
  1. `program.md`：人類設定目標、限制與規則——最重要的檔案
  2. `train.py`：Agent 可以修改的唯一檔案（可以是任何程式、設定或 prompt）
  3. `prepare.py`：評估指標腳本，Agent **絕對不能碰**，因為這是衡量成效的標準

- **實驗迴圈**：
  1. Agent 提出假設（認為可以改善什麼）
  2. 修改 `train.py`
  3. 訓練約 5 分鐘
  4. 跑評估
  5. 結果更好 → commit 到 Git 歷史；結果更差 → git reset，重新嘗試

- **固定時間預算**：讓每次實驗都在相同條件下競爭，防止 Agent 靠「訓練更久」作弊。

## AutoResearch 不只適用於 ML

- 許多人誤以為這只是機器學習的工具，實際上只要有清晰指標且可以自動評估，幾乎任何領域都適用。

### 實際應用場景

- **交易策略**：調整買賣規則，依 Sharpe Ratio 評分，自動測試數百種策略
- **行銷**：自動 A/B 測試 Email 文案、廣告創意、Landing Page 標題——下一代行銷團隊每天可跑 36,000 個實驗（vs 現在的 30 個/年）
- **程式碼最佳化**：對任何 codebase 說「讓它更快」，Agent 自動找方法
- **開源模型微調**：讓模型在本地設備上跑得更快，預計 6 個月內可在 iPhone 上跑到 Sonnet 4.6 等級
- **Prompt Engineering**：自動優化 AI Agent 的系統提示詞，找到最有效的措辭與語言

## 成功的三個必要條件

1. **清晰的指標**：單一數字、有明確方向
2. **自動化評估**：不能有人工介入評分迴圈
3. **單一可修改檔案**：讓 Agent 專注修改一個地方

## AutoResearch 的失敗場景

- 品牌設計、UX、定價——凡是「好壞」主觀的事情都不適用
- 評估迴圈太慢（需要人工判斷）
- 指標設定錯誤：Agent 會非常自信地優化錯誤的方向

## Karpathy 的終極願景

- 類似 2000 年代的 SETI@home：讓任何人捐出電腦算力，但這次是為 AI 研究
- 分散在全球數百萬台電腦的 AI Agent 協作，推動科學進步

## 實作：建立你的第一個 AutoResearch 迴圈

### 準備工作

1. 從 GitHub clone Karpathy 的 auto-research 儲存庫
2. 安裝 IDE（VS Code 或 Cursor）
3. 建立兩個資料夾：
   - `/original`：存放原始儲存庫（作為參考）
   - `/website`：存放你的專案

### 實驗範例：網站載入速度最佳化

1. 用 Claude Code 建立一個簡單的 Express 靜態網站（Alex Morgan 作品集範例）
2. 用 Codex 建立 `benchmark.mjs`，使用 Puppeteer 測量載入時間（基準值：50ms）
3. 在 `/website` 中撰寫 `program.md`——借鑒 Karpathy 的指令格式並調整為你的目標
4. 告訴 Agent：「讀 program.md，先跑基準測試，記錄結果，然後開始實驗迴圈，不要停止也不要問我任何問題。」

### 結果

- 首輪實驗就找到改善：50ms → 33ms（節省 34%）
- 幾分鐘後：33ms → 28ms（再省 15%）
- 4 分鐘內：下降到 25ms，速度減半
- 整個過程完全自動，不需要人工介入

## 結語

- AutoResearch 只是開始，後續會有更多相關內容。
- 想用於 AI 事業的創業者，作者提供免費點子驗證通話（限額）。
