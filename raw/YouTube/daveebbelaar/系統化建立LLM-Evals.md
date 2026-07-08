---
title: 如何系統化建立 LLM Evals（指標、單元測試、LLM-as-a-Judge）
description: 以 analyze-measure-improve 循環貫穿 LLM 評估的三個層級——單元測試、人類與模型評估、A/B 測試，核心是先靠人類標註對齊再讓 LLM-as-a-Judge 規模化。
created: 2026-05-29
updated: 2026-05-29
source: https://www.youtube.com/watch?v=a3SMraZWNNs
published: 2025-09-04
parent: "[[01.index]]"
tags:
  - youtube
  - llm-eval
  - llm-as-a-judge
  - ai-engineering
  - prompt
---

## 為什麼需要 Evals

LLM 非確定性、受 context 影響：可能事實對但語氣錯、一題多個有效答案、失敗模式細微。光看 production trace 只能事後補救，無法判斷「改一個 prompt 是否在別處戳出新洞」。Evals = 系統化衡量品質、定位該改哪裡。

多數團隊只做「看 trace 除錯」，缺另兩塊而停在 demo：①系統化評估品質 ②可除錯 ③能依洞察改變行為。三者齊備才掌控得住。

## Analyze → Measure → Improve 循環

核心心智模型（Hamel Husain / Shankar）：

- **Analyze**：蒐集真實案例、分類失敗模式（使用者抱怨、看資料、程式錯誤）。
- **Measure**：把洞察轉成量化指標，從 boolean（pass/fail）起步即可。
- **Improve**：調 prompt、換模型、改架構。

## 三個評估層級（成本由低到高）

- **Level 1 單元測試**：對 structured output 寫 `assert`，每次改 code/prompt 都跑。測什麼來自失敗模式——出錯定位後就補一個測試防回歸。實務：`evals/` 資料夾放 raw JSON event 餵測試，複雜後改 `pytest`。

  ```python
  assert result.category in ["billing", "technical", "general"]
  assert 0 <= result.confidence <= 1
  ```

- **Level 2 人類與模型評估**：每週/雙週跑。**先對齊人類再上模型**，這是最關鍵也最多人想跳過的一步（見下）。
- **Level 3 A/B 測試**：真實使用者實驗衡量商業影響，成本最高，應用成熟才划算。

## 關鍵：對齊 LLM-as-a-Judge

不可一開始就讓 LLM 自動監控整套系統。流程：

1. 移除看資料阻力（一份 Excel 就能走很遠），初期大量看真實資料、domain expert 進場。
2. 對「人怎麼評」有感後，才上 LLM-as-a-Judge（用負擔得起的最強模型，非 mini 級）。
3. Judge 要**產生詳細 critique 而非只給分數**，先 binary 評分。
4. 比對 model outcome vs human outcome 算 agreement，**human critique 是黃金標準不動，只迭代 judge prompt**。
5. 最推薦 **meta-prompting**：把 input/output、human critique、現行 judge prompt 與不一致處丟給最強模型，請它優化 judge prompt 逼近 100% agreement。

system 漂移（prompt/資料/使用者變），「好」的定義會變——持續追蹤 human-model agreement，不是做兩週就結束。

## 指標兩大類

- **Reference-based**（有黃金答案）：exact match、semantic similarity、code 執行、SQL 正確性。多可用 Level 1 涵蓋，較易。
- **Reference-free**（無唯一正解，真實世界更常見）：語氣、長度、無 hallucination、格式合規、安全毒性。做成 0–1 或 1–5 評分，較難。

一律從 binary 起步。

## 常見錯誤

- **Tool-first**：一有問題就換 vector DB／換模型／買 eval 平台 → 從簡單自建開始。
- **沉迷通用指標**：helpfulness 4.2 之類無從行動 → 聚焦具體可行動指標。
- **逃避資料**：靠 vibes → 持續大量看 trace（Zapier 工程師每天看三小時）。
- **未對齊的 judge**：先帶人類驗證 judge 對齊。

## 做對的徵兆

能自信部署、失敗在使用者看到前被攔、改進隨時間複利。反之：修一處壞一處、被抱怨嚇到、進展像試錯、無法衡量改動是否有幫助。
