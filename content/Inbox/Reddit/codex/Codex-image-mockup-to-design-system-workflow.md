---
title: How to get Codex to create proper UIs out of gpt-image-2 mock ups
created: 2026-05-04
updated: 2026-05-04
source: https://www.reddit.com/r/codex/comments/1t1klni/how_to_get_codex_to_create_proper_uis_out_of/
published: 2026-05-02
tags:
  - reddit
  - codex
  - workflow
  - best-practices
---

> **繁中摘要**：把 gpt-image-2 mockup 直接丟給 Codex 做 UI 通常產出非響應式或破碎介面；正確流程是先讓 image model 生「設計系統」（顏色、layout、控件各自一張圖），再叫 Codex 實作設計系統，最後才實作 UI。如此可獲得一致主題與細粒度可改性。

---

## 原文重點

- **常見錯誤流程**：「生 mockup → 叫 Codex 復刻」→ 結果非響應式、可能破碎，因為人類前端不會這樣工作。
- **建議流程（模仿前端工程師工作方式）**：
  1. 把 mockup 給 image model，要它拆成設計系統（每個元素一張圖：顏色、layout、控件等）。
  2. 把設計系統交給 Codex 實作（或先請它研究是否有現成 UI framework 與設計接近，能省時且更穩）。
  3. 設計系統實作完，才開始建 UI（mockup 只是該設計系統的其中一個 realization）。
- **可貼上的 prompt**：

  > Now create a design system out of it. Create as many images you need so every part of the design system has its own image (like an image for colors, one image for layout, one image for controls, and so on)

- **副效益**：之後改設計用「請把設計系統的色彩改成 xxxxx」，主題一致性遠勝直接對 mockup 說「make it more pink」。
- **背後原則**：把人類流程映射給 bot，而不是把它當「深呼吸用力想」的黑盒。junior dev 之所以能成功，是因為有 daily meeting、文件、可以 10 分鐘問一次同事——bot 也要這層 context。

## 社群討論亮點

- **多數質疑**：留言反覆要求 OP 出示真正成功的 UI 實作、不只 mockup 圖，目前未補上實際成品；可作為「方法論值得試但效果尚未公開驗證」的提醒。
- **批評觀點**：「這還是一堆圖、不是設計系統」——真正可消化的設計系統應有 token / variant 文字定義，純 image 仍需 model 二次解讀。
