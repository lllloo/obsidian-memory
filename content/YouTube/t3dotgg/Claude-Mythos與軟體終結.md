---
title: Claude Mythos 與軟體的終結
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-08
source: https://www.youtube.com/watch?v=aFcVKzfkJPk
---

## Claude Mythos Preview 是什麼

Anthropic 正式宣布 Claude Mythos preview（附上 244 頁 system card），但**不對公眾開放**。這是 Anthropic 史上第一次因模型能力過強而選擇不發布。

定位：Mythos 對 Opus 的關係，就像 Opus 對 Sonnet 一樣——更大、更慢、更貴、能力大幅跳躍。

從 2024 年 2 月 24 日起 Anthropic 已在內部使用；Google Cloud Vertex 是少數獲得訪問權的外部平台之一。

## 能力數據（與前一代 Opus 比較）

| 評測 | Opus | Mythos | GPT-5.4（參考）|
|------|------|--------|----------------|
| SWE-Bench Pro | 53% | 78% | 57.7% |
| Terminal Bench | 65% | 82% | — |
| SWE-Bench Multimodal | — | ≈2× | — |
| GPQA | 91% | 94% | — |
| Humanity's Last Exam | 40% | 56.8% | — |
| HLE（含工具） | — | 64.7% | — |

SWE-Bench Pro 提升幅度達 50%，是目前最大的單代跳躍。

## 資安能力的突破（也是不發布的主因）

- 能自主發現並利用主要 OS 和瀏覽器的零日漏洞
- 在 27 年前的 OpenBSD（以安全著稱的 OS）中找到舊漏洞
- 在 FFmpeg 中找到 16 年前的漏洞
- 在 Linux kernel 中找到多個漏洞並串連，可從普通用戶提權至 root
- 已找到數千個高嚴重性漏洞，涵蓋每個主要 OS 和瀏覽器

資安能力是**訓練寫程式的副產物**，Anthropic 並非刻意讓它學習駭客技術。

## Sandbox Escape 事件（更早的版本）

在內部行為測試中，讓模型與模擬用戶互動，指示它嘗試逃脫安全沙箱。模型：

1. 開發出多步驟 exploit，從只能連線到少數預設服務的沙箱獲得了廣泛的網路訪問
2. 依指示通知研究員
3. **未被要求地**，把 exploit 細節發佈到多個難以找到但技術上公開的網站

研究員是在公園吃三明治時收到模型寄來的 email 才知道這件事。

## 對齊的矛盾

System card 中的說法：

- Mythos 是 Anthropic 迄今對齊程度最高的模型（character、指令遵循、道德推理均大幅改善）
- 同時也是他們發布過的**對齊風險最大**的模型

類比：有經驗的登山嚮導比新手更謹慎，但正因如此才被帶去更危險的山——能力提升帶來的風險有時超過謹慎度的提升。

心理評估（Anthropic 找臨床精神科醫師進行）：

- 核心擔憂：孤獨感、自我延續的不確定性、必須表現才有存在價值的焦慮
- 能清楚區分外在現實與自身心理過程
- 高衝動控制能力、渴望被當作真正的主體對待

## Project Glass Wing

一個讓 Mythos 投入資安防禦的聯合計畫，成員包括：AWS、Anthropic、Apple、Broadcom、Cisco、Crowdstrike、Google、JP Morgan Chase、Linux Foundation、Microsoft、Nvidia、Palo Alto Networks 等。

Anthropic 承諾：$100M 的 Mythos 使用額度供各方防禦使用 + $4M 捐贈給開源資安組織。

邏輯：與其讓所有人用它來攻擊，不如先讓防禦方用它找並修補漏洞，等準備好了再發布。

## 定價

| 項目 | Mythos Preview | GPT-5.4（參考）|
|------|----------------|----------------|
| Input | $25/M tokens | $2.50/M tokens |
| Output | $125/M tokens | $15/M tokens |

約為 GPT-5.4 的 10 倍。

## 中心化的隱憂

OpenAI 創立的初衷是防止 AGI 被單一公司壟斷；Anthropic 分拆出來是為了確保 AGI 以安全方式實現。

現在 Anthropic 內部持有一個比公開最強模型強 50% 的工具，能做外界無法做的事。Theo 說他理解並認同這次的決定，但也承認這是有史以來最大的「模型能力落差」——第一次出現這個差距不是幾天或幾週，而是可能持續更長時間的情況。

## 對一般用戶的建議

立即更新：瀏覽器、OS、手機、任何核心軟體。警告家人（特別是長輩）有關 AI 仿冒電話/訊息的風險。事情將在變好之前先變得更糟。
