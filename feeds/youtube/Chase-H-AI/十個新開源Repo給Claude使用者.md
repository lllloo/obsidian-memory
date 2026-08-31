---
title: 十個 Claude 使用者必試的新開源 Repo
description: 從可插拔的 DeepSeek Harness、AI 原生 Linux 發行版到文件轉 markdown、AI gateway 與對抗式審查 skill，十個當月竄起的開源專案逐一說明用途與適用對象
created: 2026-08-31
updated: 2026-08-31
source: https://www.youtube.com/watch?v=LrHY1U03IRU
published: 2026-08-30
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - harness
  - multi-model
  - workflow
---

作者挑選當月竄起的十個開源 repo，涵蓋 harness、作業系統、文件處理、終端／IDE、skill、影片製作、AI gateway、視覺化與遊戲專案，橫跨初學者到重度 tinkerer。

## Harness 與作業系統層

### DeepSeek Harness

兩週內累積超過 20 萬 star，作者稱其為成長最快的 GitHub repo。作者也直言數字受到熱情的中文社群推升，但認為它確實做到 Claude Code 與 Codex harness 做不到的事：**在最底層客製 harness 本身**。

- 核心理念是「everything is a plugin」——harness 像車體底盤，引擎、座椅、內裝都能自己換。
- 可接任意模型；影片示範中模型來自 OpenRouter，等於市面上幾乎所有模型都能用。
- plugin 能改動根本管線：tool calling 的方式、agent loop 的行為，也能改比較表面的 UI 與配色。
- 對比：Claude Code／Codex 可用 hooks 與 skill 逼近類似效果，但**改不到底層管線**。
- GitHub 上已有快速膨脹的 plugin 生態。

適合喜歡開源、愛折騰與客製化的人。

### Omarchy

一套客製 Linux 發行版，把 Arch 與 AI agent 結合，讓 agent 成為作業系統的基礎組成。例如 OS 本身出錯時，錯誤會自動送往你選定的背景 agent（Codex、Claude Code、Gemini 皆可）。

安裝與使用門檻明顯高於清單中其他項目；不熟 Linux 的人不建議，反之則值得一試。

## 文件與資料處理

### Anydoc（Firecrawl）

Rust 函式庫，把傳統 Office 文件轉成 markdown。動機是 AI 吃 markdown 效果好，但多數人手上是 Word、PowerPoint、Excel；既有轉換工具不是不準就是太慢。

Firecrawl 自家 benchmark（作者提醒需保留判斷空間）：

| 工具 | 支援格式 | 中位速度 |
|---|---|---|
| Anydoc | 14 / 14 | 4.4 毫秒 |
| Mammoth | 1 / 14 | 52.5 毫秒 |
| Office（對照組） | 12 / 14 | 1,100 毫秒 |

品質分數由第三方 AI judge 評估完整度與結構，Anydoc 也較高。適合手上有成千上萬份舊格式文件、想批次轉成 markdown 餵給 AI 的人。

## 終端與 IDE

### Herdr

作者每天在用的工具，本質是終端的加強版 UI。

- 左側面板顯示正在跑的 agent 狀態與各個 workspace，右側是標準終端。
- workspace 概念類似不同資料夾／專案，可同時掛多個 agent（agent 1、agent 2⋯）並分割面板。
- **會保存工作階段**：完全關閉所有分頁後再啟動 Herdr，先前的內容仍在。

定位是輕量、簡單的加值層，適合重度使用終端且同時操作多個 agent 的人。

### Orca

56,000 star。作者形容它是「為 AI agent 而生的 VS Code」，對應 Herdr 的定位但服務偏好重型 IDE 的人。

- 有 mobile companion，方便遠端工作。
- 內建 design mode——Claude、Codex 的桌面版陸續有 design mode，但 Orca 讓不想用桌面 App 的人也有。
- 自帶 CLI，可以讓 AI agent 反過來操控 Orca 這個 IDE。
- 支援 macOS、Windows、Linux。

## Skill 與工作流

### ClaudeX Loop

作者自製的 skill，Claude Code 與 Codex 皆可用。出發點：AI 系統評自己的作品極度寬鬆——問 Codex 自己做得如何，答案永遠是很好。解法是引入外部 AI 系統來評分。

四階段流程：

1. **Reconnaissance**：實際做 web search，釐清該怎麼做。
2. **Interrogation**：向使用者提一連串問題，可視為增強版 plan mode，發生在 Claude 產出計畫之前。
3. **對抗迴圈**：Codex 與 Claude 多輪往返辯論直到收斂。
4. **Build 與覆核**：由 Codex 或 Claude 其中之一建置，完成後另一個系統進場指出對錯。

效益是全程都有第二雙眼睛，把問題在前期解決，避免「Claude 蓋好、看似能動、實際壞掉、再回頭迭代」的循環，總體輸出更好且更省 token。適合同時使用 Claude Code 與 Codex 的人。

## 影片與模型路由

### OpenMontage

近 54,000 star，作者稱之為「盒裝的影片製作工作室」，適合想切入 AI 影片製作的人。

- 大量 human-in-the-loop：不是丟一個 prompt 就全自動跑完，過程中使用者有創意控制權。
- 涵蓋研究、腳本、prompt 產生；但要有好的成品需自備 API key 接頂級模型（如 Seedance 2.5），廉價或本地影片模型除非電腦夠強否則難以支撐。
- 不想付費也有路可走：可用 Claude Code 搭配 Run Motion、Hyper Frames 之類做出電腦生成風格的影片。
- 針對不同影片 pipeline 各有專屬 skill：動畫解說、animation、clip factory、screen demo、talking head。

### OmniRoute

58,000 star 的 AI gateway，可完全免費使用。

- 一站接上 350+ AI provider，其中 90 多個免費。
- 可設定成只用免費 provider，額度用完自動輪替到下一個，不會卡在單一 provider 的免費 token 用罄。
- 也能設定使用前沿模型，接上 Claude Code 或 Codex，並自訂優先序與切換模型的時機。
- 官方稱路由鏈為 **combo**：一條自動切換的模型鏈，任一環失敗或額度用盡就轉往下一個健康的模型，內建約 19 種預先寫好的路由策略。

適合同時用很多模型的人，或想用免費模型把 token 用量最大化的人。

## 視覺化與示範專案

### Archy

30,000 star，曾登上單日第一。把 codebase 或任何系統描述轉成可分享的活地圖，說明程式如何運作。

- 複雜的 codebase 可轉成類似 Excalidraw 的圖並分享出去，讓 AI 代寫、難以理解的程式碼變得可視。
- 不只是靜態快照：可建立 motion sequence 解釋不同互動或改動，也能呈現資料實際怎麼流動。

適合處理複雜 codebase、且經常要對非技術人員做視覺化說明的人。

### Claude of Tanks

只有約 200 star、幾乎沒人討論，但作者認為是很出色的專案：作者 Kevin Lou 純用 Claude Code 以 three.js 重製了 World of Tanks。

- 圖形品質與物理表現遠超一般 Claude 做的遊戲。
- 具備完整戰鬥系統、HUD、X 光擊殺鏡頭、破壞效果。
- 支援多人（本地 LAN 或瀏覽器 host）。
- 多張地圖、多款戰車、迷彩可調；模組涵蓋主砲、引擎、油箱、無線電。

作者認為它是「如何用 Claude Code 做遊戲專案」的絕佳範例。
