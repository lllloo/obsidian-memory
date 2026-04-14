---
title: Claude Code 已無法使用——Anthropic 對系統提示詞的限制
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-05
source: https://www.youtube.com/watch?v=stZr6U_7S90
---

## 事件起因：Open Claw 被封鎖

Theo 透過 Claude Code 的 $200/月訂閱方案，同時將其用於四個工具，其中之一是 **Open Claw**（一個第三方 Claude 客戶端）。Anthropic 先後透過 header 封鎖 Open Claw、Open Code 等第三方工具，後來進一步封鎖**系統提示詞中提到「Open Claw」**就拒絕請求。

更諷刺的是：若帳號開啟「extra usage（超額計費）」，包含 Open Claw 字樣的請求就能成功——Anthropic 在路由層針對系統提示詞內容進行差異化計費。

## Claude Code 訂閱的經濟模型

- $200/月方案可消耗高達 $5,000+ 的推論成本，補貼比例約 25x
- Anthropic 願意補貼的原因：重度用戶通常是傳播者，能帶動更多付費用戶
- Open Claw 用戶往往耗用更多 token（缺乏快取優化、持續發送心跳請求），破壞了這個模型
- Boris（Claude Code 創始人）甚至提交 PR 幫助 Open Claw 改善快取以降低成本，共四個 PR 中三個被合入

## Anthropic 封鎖 Open Claw 的實作方式

1. 封鎖含有 Open Claw 相關 header 的請求
2. 封鎖系統提示詞中含有「Open Claw」字樣的請求（即使透過 Claude CLI 的 `-p` 繞過也無效）
3. 帶有 Open Claw 系統提示的請求若帳號開啟超額計費則照常收費

## Matt Pocock 的困境

TypeScript 教學者 Matt Pocock 為了 Claude Code 製作了一門付費課程，一個月以上無法從 Anthropic 獲得清楚的使用條款說明：

- Claude Code CLI？允許
- 用 Agent SDK 跑個人軟體？允許
- Agent SDK 商業用途？不允許
- Claude Code 在 CI 裡？不確定
- Claude `-p` 在開源軟體裡？不確定

Matt 的評語：「Anthropic 的訂閱規則比 TypeScript generics 還複雜。」

## Theo 的最終決定

- 在 zshrc 裡把 `cc`（Claude Code alias）改指向 Codex（加上 `--yolo` 標誌）
- 理由：Codex CLI 開源、模型更強、支援 OAuth 跨工具使用、OpenAI 對開發者更友善
- 這不是表演性取消訂閱，而是實際工作流程的轉換

## 陰謀論部分（Theo 自承推測）

Theo 懷疑 Anthropic 在 API 層注入額外系統提示，導致 Claude Code 近期行為異常。不過 Bad Logic Games（Pi 的作者）追蹤 Claude Code 系統提示的版本歷史，顯示並無明顯變化，此推測缺乏實證。

## 核心結論

Anthropic 的問題不是規則本身的內容，而是**規則不清晰且執行方式缺乏透明度**。針對系統提示詞內容差異化計費是業界罕見且嚴重損害信任的做法。
