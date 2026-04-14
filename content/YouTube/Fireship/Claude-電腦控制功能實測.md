---
title: Anthropic Claude 電腦控制功能（Computer Use）實測
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-03-26
source: https://www.youtube.com/watch?v=wfeiCZK0mNs
---

## 功能概覽

Anthropic 發布 **Computer Use**，讓 Claude 能夠以單一 prompt 自主控制整台電腦：開啟應用程式、排程工作、撰寫報告，甚至直接從手機遠端操控。

- 目前僅支援 **macOS**
- 採用**權限優先**（permission-first）設計：存取新應用程式前會先詢問使用者，只操作明確允許的資料夾

## Computer Use vs OpenClaw 比較

| 特性 | Computer Use（Anthropic） | OpenClaw（開源） |
|------|--------------------------|----------------|
| 授權 | 付費、閉源 | 免費、開源 |
| 平台 | 僅 macOS | 跨平台 |
| 模型 | 綁定 Claude | 模型無關 |
| 安全性 | 權限管控嚴謹 | 開放性帶來更高風險 |

OpenClaw 是 AI 個人助理，原名 ClaudeBot，後來收到 Anthropic 的停止函；Palo Alto Networks 警告其「私人資料存取 + 外部通訊 + 記憶體保留」的組合風險較高。

## 實際應用示範

影片以工作詐欺的幽默示例展示 Claude Computer Use 的能力：

- **求職**：自動撰寫並寄出求職信；面試時在背景即時解題
- **日常工作**：同步行事曆、自動點擊 Zoom 會議連結、以本地 AI 語音模型代替出席
- **程式碼提交**：5 分鐘寫完程式碼，但排定在週五下午 4:30 送出 PR，模擬人類工作節奏
- **財務**：登入銀行確認薪資入帳，自動轉換為 Monero

## 技術背景

- Dario Modei（Anthropic CEO）預測：未來 1-5 年內 50% 的初階律師、顧問、金融從業人員將被 AI 取代
- 給予 LLM 不受限的網路存取能力，改變了一切的可能性邊界
