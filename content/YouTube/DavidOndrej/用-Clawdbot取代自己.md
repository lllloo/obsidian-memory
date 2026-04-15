---
title: 用 Clawdbot 取代自己
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-26
source: https://www.youtube.com/watch?v=2zWGFLrTVmI
---

## 概覽

- Clawdbot（即 OpenClaw 早期稱呼）是一個自托管 AI 助理，可從任何 App（WhatsApp、Telegram、Slack 等）傳訊息使用。
- 核心優勢：資料不送給 Anthropic 或 OpenAI，持久記憶儲存在自己的機器上，完全可自訂技能。

## 典型應用案例

- 傳 WhatsApp 訊息給 Clawdbot 預訂餐廳 → 當 OpenTable 預訂系統失敗時，自動使用 11 Labs 語音技能**打電話**給餐廳完成預訂。
- 管理多個 AI Agent：接受點子 → 協調 Codex 與 Claude → 讓它們辯論解法 → Agent 完成後通知使用者，自動完成 PR 合併。
- 其他使用者的案例：
  - 依重要性將任務排入行事曆
  - 根據所有會議記錄進行每週回顧
  - 通知家人關於孩子的考試
  - 研究大型專案並拆解為子任務
  - 在會議前研究對方並建立簡報文件
  - 管理行事曆衝突、建立發票、摘要工作

## 安裝步驟（VPS 方案）

1. 前往 claude.bot，複製 oneliner 安裝指令。
2. 在 Hostinger Terminal 貼上並執行（自動偵測 Linux、安裝 Node.js、安裝 Clawdbot）。
3. 安全確認：輸入「yes, I understand this is powerful and risky.」
4. 選擇 Onboarding 模式：Quick Start。
5. 選擇模型提供商：**OpenRouter**（可存取所有最新模型）。
6. 取得 OpenRouter API key → 貼入。
7. 手動選擇模型（Opus 4.5 或 4.6 推薦）。
8. 選擇通訊頻道：**WhatsApp**（也可選 Telegram、Discord、Slack、iMessage 等）。

## WhatsApp 設定

- 選擇 WhatsApp 後，Clawdbot 生成 QR Code。
- 在 WhatsApp 手機版：設定 → 連結裝置 → 連結裝置 → 掃描 QR Code。
- 完成掃描後，在終端機輸入你的手機號碼完成配對。
- 建議：安裝 **WhatsApp Business** App（可在同一手機使用兩個 WhatsApp 帳號），一個作為 Clawdbot，另一個是你自己的帳號。

## 技能（Skills）安裝

- 安裝過程中可選擇多種技能（按空格鍵選擇，Enter 確認）：
  - **OpenAI Whisper**（語音轉文字，高品質）
  - **OpenAI Image Generation**
  - Google Places、Apple Notes、Apple Reminders、Obsidian、Nabana Pro 等
- 推薦優先安裝：OpenAI API（同時開啟 Whisper 和 Image Generation）
- 其他技能可後續根據需求新增

## 常用指令

- `cloudbot channels login` — 設定或更改頻道（WhatsApp、Telegram 等）
- `cloudbot channels logout --channel whatsapp` — 移除特定頻道憑證

## 調試技巧

- Clawdbot 是較新的工具，AI 模型（ChatGPT、Claude 等）的訓練資料可能包含錯誤的指令。
- 建議：在 VPS 上安裝 **OpenCode** 作為調試工具，用它來調試 Clawdbot 的設定問題（AI Agent 互相幫助設定）。
- 在調試過程中，切換到 Plan Mode 讓 Agent 先分析再執行。

## 為什麼選 VPS 而非 Mac Mini

- 不要在自己的主機上安裝 Clawdbot——它有完整的系統存取權限，可能誤刪重要檔案。
- VPS 費用（約 $7/月）vs Mac Mini（$600 以上），VPS 更靈活、可遠端存取、易擴展。
- Hostinger KVM2 方案：2 vCPU、8 GB RAM、100 GB 磁碟、8 TB 頻寬，完全夠用。

## 使用場景

Clawdbot 的核心價值：**用你已在使用的 App（如 WhatsApp）與 AI 互動，讓 AI 完成那些你過去需要私人助理才能完成的任務。**

- 發語音訊息在健身房組間休息時預訂餐廳
- 接收航班 check-in 提醒、自動完成 check-in
- 管理 Google 行事曆、整理電子郵件收件匣
- 協調多個 Claude Code / Codex Agent 完成複雜開發任務
