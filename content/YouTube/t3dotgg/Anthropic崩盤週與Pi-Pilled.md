---
title: Crashing out at Anthropic 與 Pi-Pilled — TBPN 首集
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-08
source: https://www.youtube.com/watch?v=3DNkDIVKtK8
---

## 這集是什麼

Theo 與 Ben 錄製的新 podcast 首集（暫名 TBPN）。主題圍繞 Anthropic 的連鎖公關災難週，以及 Claude Code 訂閱政策混亂。

## Anthropic 這週發生了什麼（按順序）

### 1. Rate limit 調整（有意為之）

Anthropic 在太平洋時間 7–11 點尖峰時段降低訂閱計畫的使用額度，但在 **調整後 2.5 小時才發公告**，且只在 Thoric 帳號（社群非官方追蹤）發佈。官方 Claude 帳號從不主動揭露負面消息。

### 2. Rate limit bug 疑雲

Reddit 上有人懷疑 Claude Code 的 prompt cache 被意外破壞，導致每次 token 用量暴增。後來證明更可能是第一點的正常限制效果，加上 Anthropic 沒有買足夠的 GPU。

Cache 原理補充：LLM 推論需要重新計算所有歷史 token，cache 是把某個節點的計算結果儲存下來以節省重複計算成本。Anthropic 是少數同時收 cache write 費用的服務商（$6.25/M tokens），OpenAI 只收 cache read 費用，寫入免費。

### 3. Claude Code 原始碼洩漏

Claude Code 是 TypeScript 打包成 npm 套件，一直以來由**團隊成員各自在本地機器發布**，沒有 CI/CD 發布流程。

洩漏原因：某次本地建置時產生了 source map（為了 debug 或上傳到 Sentry），source map 沒被刪除，下次發布時 dist 資料夾沒有清空，兩份檔案一起被發布到 npm。

影響：任何人都能從 npm 下載並讀取完整的 TypeScript 原始碼，包括 Open Code 在 source code 中被直接引用的程式片段。

### 4. 訂閱政策突然變更（提前不到 24 小時通知）

Anthropic 發送 email，宣布 Claude Code Max 訂閱從 **18 小時內** 起只能透過官方 Claude Code harness 使用，Open Code、PI、OpenClaw 等第三方工具全數斷線。

Theo 的結論：整個訂閱方案（5x/20x 補貼）當初是為了搶回離職到 Cursor 的 Claude Code 原始開發者 Boris 和 Cat 而設計的行銷支出，所有後續問題都源自這個決策。

### 5. Boris 澄清推文 → Thoric 否認 → 持續混亂

Boris 在 Twitter 表示可以使用 Claude Code 的 wrapper（如 T3 Code）搭配訂閱，Theo 截圖分享。幾小時後 Thoric 發推說「這不是官方指引，我們還在整理」。

Matt Pocock 三週前開始詢問包 Claude Code 課程是否合法使用訂閱，至今沒有官方回覆。他在 Twitter 上說：「我從來沒有在任何開發工具上遇過這樣令人沮喪的使用條款不清晰。」

## Claude Code 訂閱的商業邏輯分析

- Claude Code Max（$200/月）最多等值 $5,000 的 inference，即 25 倍補貼
- Anthropic 這麼做是把它當作**行銷費用**，前提是你使用他們的 harness
- Claude Code 在官方 benchmark（SWE-bench）的 harness 排名中為第 12 名，使用 Opus 在其他任何 harness 下都能得到更好的結果

## Anthropic 公關策略的根本問題

- 內部文化假設「大家都喜歡 Anthropic」，負面反饋被視為暫時或外部操控
- 官方帳號只發好消息；壞消息由員工個人帳號（或 Thoric）發
- 員工在 Theo 抱怨時，回應是「你不了解問題的複雜性」
- 對比 OpenAI：每次有負面反饋立刻回應並修正，即使只是「謝謝我們會看」

## 開源 Claude Code 這件事

Boris 在早期訪談說過不開源是因為「這是我們的 secret sauce，不想給競爭對手好處」。Theo 認為這是錯誤的——他們應該像 Google 開源 Kubernetes 一樣，用開源鎖定標準，讓競爭對手追趕一個他們自己定義的標準。

## Pi-Pilled 這段

節目中討論了 Pi（Raspberry Pi）相關的技術話題，以及在 podcast 環境中用 Whisperflow 等語音工具的可行性（此段較輕鬆，無技術重點）。
