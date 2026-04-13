---
title: 三大框架讓 Claude Code 無可匹敵：Superpowers、GSD、GStack
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-02
source: https://www.youtube.com/watch?v=bzutStZJ1Ig
---

## 重點摘要

- 三個框架各解決不同問題，互補而非競爭：
  - **Superpowers**：約束「流程」（process）— 讓 AI 遵循軟體開發方法論，步驟：釐清意圖 → 確認 spec → 實作計畫 → 測試先行（TDD）→ 寫程式 → 重構
  - **GSD**（40K GitHub stars）：約束「環境」（environment）— 解決 context rot，將對話拆成多個階段，每階段換新 Orchestrator，確保 context window 永遠低於 50%；狀態存入本地 MD 檔案持久化
  - **GStack**（Gary Tang / YC CEO）：約束「視角」（perspective）— 將單一 agent 拆成不同專家角色（CEO、Engineer Manager、QA Lead 等），每個角色只關注自己的職責範疇

- **Superpowers vs GSD 關鍵差異**：Superpowers 用同一個 Orchestrator 貫穿整個對話 + 不同 sub agents；GSD 每個階段都換一個全新 Orchestrator + 各自的 sub agents

- **GStack 五層架構**：
  1. Role Focus — 角色只看自己職責範圍
  2. Data Flow — 工作建立在前一階段輸出之上
  3. Quality Control — 各角色完成項目的 checklist
  4. Boil the Lake — 只做能 100% 完成的事，不碰超出職責的事
  5. Keep it Simple — 結論精煉為「發現了什麼、為何重要、下一步是什麼」

- **組合使用（Power Stack）**：
  - GStack → 策略規劃（CEO/Engineer Manager lens 驗證架構可行性）
  - GSD → 執行規劃（拆分里程碑，確保每個里程碑低於 50% context）
  - Superpowers → 實際執行（TDD，先寫測試再寫程式，用 Playwright 做 UI 測試）
