---
title: Hermes Agent 進階用法
description: Hermes Agent 的 wake agent、no agent、Slack 記憶與自動化流程，適合用來降低長期任務的 token 成本。
created: 2026-06-11
updated: 2026-06-11
source: https://www.youtube.com/watch?v=qMEm1bgxnUM
published: 2026-06-10
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - ai-agent
---

## 桌面版與 profile 管理

Hermes Agent 新增 desktop app，本質上是 agent setup 的 UI wrapper。相較 TUI，桌面版更容易監看多個 agent profile、切換設定、啟用 skills，並管理 memory / profile 的字元預算。

profile 是彼此隔離的 Hermes agent，每個 profile 有獨立 memory 與 skills。桌面版可並行啟動多個 profile，把不同 persona 或任務分開處理，避免長期使用時互相污染。

## Wake Agent：只在值得時呼叫 LLM

`wake agent` 是 cron task 裡的判斷旗標。當事件沒有真正需要 LLM 介入時，agent 不會被喚醒；只有偵測到值得注意的變化，才花 token 呼叫模型。

適合場景：

- 監控 AWS、Gemini API 或其他成本異常，只有超出平常範圍才回報。
- 監控 Google Play app review，只在負評或異常回饋出現時彙整並通知 Slack。
- 搭配 Stripe MCP 或其他工具，在異常發生後不只通知，也能進一步執行補救動作。

這個模式的重點是：定期任務照常跑，但 LLM 不是每次 cron 都被呼叫，而是由事件變化決定是否值得喚醒。

## No Agent：在 Hermes 生態內跑低成本 cron

`no agent` 旗標代表任務不呼叫 AI model，只做 deterministic 的自動化。它看起來像一般 cron job，但仍由 Hermes 生成與管理流程，並可沿用 Hermes ecosystem 的技能與設定。

例子：

- 監控 TLS、網站健康狀態、Stripe app health。
- 將健康檢查結果送到 Slack。
- 平常不花 LLM token；需要 agent 判斷或修復時，再在聊天裡 tag Hermes 接手。

這讓 Hermes 同時支援「便宜的例行監控」與「需要時才喚醒的智慧處理」。

## 公司第二大腦

Hermes 可以接到 Slack workspace，讓團隊成員直接與 bot 互動。長期使用後，它會累積公司任務、進度、目標與常見流程，並生成對應 skill 作為組織脈絡。

這種用法和一般聊天 bot 的差異在於 memory editing 與 skills：Hermes 不只是回答問題，而是把重複任務變成 reusable workflows，讓專案經理可追蹤目標、分派任務、同步進度。

風險在於 memory 膨脹。影片主張 Hermes 比 OpenClaw 更能處理長期任務，因為 OpenClaw 的 soul file 可能變得過大，最後需要重置。

## Gmail、webhook 與 lead 回覆

Hermes 內建 Google Workspace 相關 skills。連接 Gmail 前，需要在 Google Cloud 建 project、設定 credentials 與 callback token。

完成後可建立 webhook：

- 監控 incoming email。
- 判斷是否為 potential lead。
- 根據公司脈絡生成回覆。
- 若涉及會議，依 calendar 空檔安排時間。

這類自動化的關鍵不是單次回信，而是 Hermes 已經累積公司資訊與任務脈絡，能把回覆建立在既有 context 上。

## PRD skill 與競品監控

影片建議把 PRD 保存成 skill，而不是普通文件。理由是 skill 只在需要時載入，且較容易出現在 context window 的新鮮區域，避免長任務中需求被稀釋。

Hermes 可用同一份 PRD skill 建立競品監控 cron：

- 定期檢查競品更新。
- 維護競品分析文件。
- 把可能新增的 feature 回寫到 PRD 建議中。

這讓 PRD 不只是靜態文件，而是會隨市場與競品狀態更新的工作材料。

## 社群內容產製

Hermes 也可把長影片 script 改寫成 X 與 LinkedIn 貼文，先輸出到資料夾供人 review，再由 Hermes 呼叫 XURL 等 skill 發佈。

這裡保留 human review 是必要的：社群貼文涉及品牌語氣與事實正確性，不適合全自動直接發佈。
