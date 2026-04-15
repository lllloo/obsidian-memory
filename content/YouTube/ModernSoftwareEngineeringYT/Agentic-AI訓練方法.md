---
title: Agentic AI 訓練方法
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-04
source: https://www.youtube.com/watch?v=nnjzPJ2ZI6E
---

Emily Bache 探討什麼樣的訓練方式能真正讓開發者學會使用 Agentic AI 工具。

## Agentic AI 是什麼？

Agentic AI 是一種可以接受完整任務、在迴圈中運作、使用工具（執行測試、查文件、修改程式碼）的 AI。與 IDE sidebar 或行內補全有本質差異，是更大的工作方式轉變。

Emily Bache 認為這是繼 1950 年代高階語言出現後最大的範式轉移。

## 為什麼傳統訓練方法不適用？

### Code Kata 太小
- Kata 是為人類大腦設計的練習大小
- 對 AI 來說沒有挑戰性，無法反映真實學習場景

### 自定義訓練題目有 data leakage 問題
- 標準訓練題（todo list、micro blog）早已有無數解法在 GitHub
- LLM 直接重現訓練資料，而非真正「學習」解題
- 封閉原始碼的真實生產程式碼行為完全不同

### Prompt 工程書籍過時太快
- Addie Osmani 的《Beyond Vibe Coding》（6個月前出版）中的部分 patterns 已被新工具內建
- 例：「contextual prompting」（把 API 文件貼進 prompt）—— 現在 AI agent 會自行查找文件

## 有效的學習方法

### Augmented Coding Patterns
Emily Bache 推薦 Lauard Kesler、Iet Erdog 等人整理的「Augmented Coding Patterns」：
- 針對 LLM 的根本限制設計
- 基於實際 Agentic AI 使用經驗
- 比 prompt 工程書籍更貼近現實

範例 pattern — **Check Alignment**：
> 給 agent 新任務時，提醒它先問問題、說明計畫再開始。
> 防止 agent 往錯誤方向走。

（現在最新模型已會自動做這件事，無需提醒——工具變化極快。）

### 在真實生產程式碼中接受技術教練
- 試錯是最慢的學習方式
- 應找現代軟體工程的專家做 coaching，在真實程式碼中學習
- 傳統課程難以提供有效的 AI 技能訓練環境

## 核心技能的不變性

Dave Farley 的兩大核心關注：**優化學習** 與 **管理複雜度**，在 Agentic AI 時代不變：
- 仍然是小步驟、尋求回饋（類似 TDD）
- 仍然需要決定如何分割問題、分離關注點
- 多了一層：管理給每個 AI agent 的上下文

TDD 心態仍是最佳工程流程建議，但具體做法因 Agentic AI 而改變。

## 結論

Prompt engineering（或更好的說法：Augmented Coding）是軟體工程中可以學習的技能。現階段最有價值的做法：學習 Augmented Coding Patterns，並在真實程式碼中接受有經驗的工程師指導。
