---
title: Claudex route 與 loop 讓 GPT-6 Astra 與 Fable 5.1 分工
description: 用便宜模型接簡單任務、對立模型互審計畫與實作的兩支 skill，附 Sonnet 5 與 Terra、Luna 的每任務成本對照
created: 2026-09-09
updated: 2026-09-09
source: https://www.youtube.com/watch?v=KgKA0A3qlz0
published: 2026-09-07
parent: "[[01.index]]"
tags:
  - youtube
  - multi-model
  - claude-code
  - codex
  - llm-pricing
  - workflow
---

> [!info] 內容來源
> 影片 transcript 為自動字幕，模型名與數字有辨識誤差（Claudex 被辨識成 Claudics／Claudeex，Terra 被辨識成 Terara）。此處統一寫回，數字有疑義處就地標註。

## 問題設定

作者認為該問的不是「GPT-6 Astra 和 Claude Fable 5.1 哪個好」，而是**怎麼把兩邊都用滿**。實務上多數工作根本用不到旗艦模型，真正的問題是什麼時候該把 Luna、Terra 這類便宜模型叫進來。

## 為什麼需要跨廠牌調度

**第一個理由：Anthropic 陣營缺 CP 值檔位。**

- Astra 與 Fable 5.1 定價相同，作者引述為輸入 $10、輸出 $50（每百萬 token）；走 API 計價時對個人開發者可能吃不消。
- 作者對 Claude Sonnet 5 的評價是「與宣稱的 benchmark 和預期表現有落差」，主觀體感不佳。
- 結論是：長期只用 Anthropic 模型的人，在「便宜又堪用」這一檔會找不到選項。

相對地 OpenAI 這一檔有兩個選項。Terra 以 token 單價論略貴於 Sonnet 5，但因為 token 效率較好，整體反而更便宜。Luna 被作者形容為「Haiku 本來該長成的樣子」——輸入 $0.20、快取 $0.02。

> [!warning] 數字不確定
> Luna 的輸出價在 transcript 中被念成「120」。依上下文（作者強調它「相較其他模型基本上等於免費」）應為 $1.2 量級，但字面數字無法核實，引用前請回查官方定價。

以 Deep Sweep benchmark 的每任務平均成本對照（作者螢幕上的數據）：

| effort | Sonnet 5 | Terra | Luna |
|---|---|---|---|
| max | $26 | $4 | $0.60 |
| low | $2.19 | $0.34 | $0.01 |

準確度方面 max 檔位：Sonnet 5 為 54%、Terra 70%、Luna 67%——也就是兩個便宜模型在這個 benchmark 上不只更便宜，分數也更高。作者另外點出 Luna 從 low 拉到 max 時成本幾乎不漲、效果卻大幅提升，而 Sonnet「隨時有成本爆走、耗掉過多 token 的風險」。

實務建議：就算主力吃 Anthropic 的 20x 方案，另外開一個月費 $20 的 OpenAI 方案專門打 Luna 呼叫，可能就划算。

**第二個理由：執行的模型不該是評估的模型。**

這是作者在先前 Codex loop 系列講過的主軸。模型評自己的作品一律偏寬鬆——Fable 永遠覺得 Fable 寫得好，Astra 永遠覺得 Astra 寫得好。所以讓 Fable 5.1 出計畫後，要換 Astra 用全新、乾淨的 context 進來審，避開同一模型的固有偏誤。這個原則同樣可以下放到低階模型：Opus 建、Terra 或 Luna 審。

## 兩支 skill

兩支都在同一個 Claudex Loop GitHub repo 裡，把 repo URL 丟給 Claude Code 或 Codex 就會自動安裝。

**Claudex route（新的）——單次任務的模型選擇**

給它一段任務描述，它回答該用哪個模型。判斷依據是各家 frontier lab 公布的模型資訊、官方使用指引與實際成本。

它不只是給建議，還會實際執行：在 Claude Code 裡打 `/codex route` 描述任務，若判定該用 Astra，就把相關資訊送進一個 **headless 的 Codex 實例**（等於在背景開一個看不見的 Codex CLI），Codex 做完後把「我做了什麼、程式碼在哪」回報給 Claude Code。反向也成立，從 Codex 起頭一樣可以。

**Claudex loop（更新版，已納入 Astra）——大型實作的全程流程**

定位差異：route 處理一次性的小功能，loop 是從規劃一路帶到執行的大型實作。

核心規則是**用對面平台的模型當檢查者**：在 Codex 裡跑，出計畫的是 Astra、審的是 Claude Code；在 Claude Code 裡跑則反過來。

四個階段：

1. **偵察**：對主題做 deep research，spawn 一批 subagent 去搞清楚目標到底是什麼、有沒有人做過、驗證你的假設。
2. **提問**：反問使用者想改什麼、在意什麼、對這個專案的想像是什麼。
3. **出計畫並互審**：一方寫計畫，送給對面模型審，來回數輪同意／反對，直到雙方達成核可。有安全閥防止無限循環燒 token。
4. **執行並互審**：由你選 Astra 或 Fable 執行，完成後由另一方檢查漏了什麼。

作者對成本的說法是：表面上來回審看起來貴，但比起東西蓋完才發現要重做，長期反而省 token。

## 作者的立場

- 不該是二選一。建議把原本花在單一廠牌 $200 方案的預算拆成兩邊各一個 5x 方案，實際用過再決定偏好。
- 理由是工具迭代太快，要保持 tool agnostic，而不玩過全部就做不到 tool agnostic。
- 誠實的但書：作者也承認多數人蓋的東西超出自己的 coding 能力，不會真的去複查 Astra 或 Fable 的產出；互審機制給的比較接近「有另一個模型看過」的心理保障。
