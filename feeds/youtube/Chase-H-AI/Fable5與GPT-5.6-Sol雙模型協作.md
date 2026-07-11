---
title: Fable 5 + GPT 5.6 Sol 的作弊級組合
description: 結合 Fable 深度規劃與 Codex 建置的 grill-me-codex skill：訪談產出計畫、雙模型對抗式辯論至共識、交 GPT 5.6 建置、Fable 收尾審查，兼顧品質與 token 效率。
created: 2026-07-10
updated: 2026-07-10
source: https://www.youtube.com/watch?v=gsvZn4nbFus
published: 2026-07-08
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - multi-model
  - token-optimization
---

## 核心主張：別問誰比較強，問怎麼一起用

GPT 5.6（代號 Sol）發布前夕，大家都在問它能不能打贏 Claude Fable。作者認為這是錯的問題——應該讓兩個模型分工：Fable 負責規劃與審查，GPT 5.6 負責建置。他為此提供一個 skill，整體效果是「取兩家之長」，且總 token 消耗比全程用 Fable 更省。

## 為什麼值得雙模型協作

- **GPT 5.6 Sol 的實力**：依 OpenAI 公布的 benchmark（作者提醒需保留態度），5.6 Ultra 與標準版 5.6 在 Terminal Bench 2.1 上領先 Claude Mythos，更不用說 Fable 5。
- **token 效率**：市面上大量「降低 Fable 用量」的內容（如 advisor mode——Fable 規劃、Opus 執行）本質就是這個構想；但與其讓 Opus 執行，不如用同價位但更強的 GPT 模型。作者引用的 benchmark 數據：GPT 5.5（extra high）通過率 23%、成本 $1.24；5.6 通過率 25%、成本更低（口述為 56，約為 5.5 的一半以下），分數更高且便宜得多。5.5 對 Opus 4.8 的直接比較也是「通過率更高、成本更低」。
- 作者認為除非堅決反 GPT／反 Codex，否則很難反駁這個組合，尤其在 Fable 供應吃緊的情境下。

## Skill 組成與四階段流程

作者提供兩個 skill（GitHub 連結見影片說明欄）：

- **codex-build**：已有 Fable 產出的計畫時，單純把建置交給 Codex。
- **grill-me-codex**（完整版）：以 `/grill-codex` 加上需求 prompt 啟動，走四個階段——

**階段一：訪談（Grill Me）**。直接採用 Matt PCO 的 Grill Me skill，等於「plan mode 加強版」，由 Fable 主導，連問約 8–10 個比一般 plan mode 深得多的問題，每題都附建議選項。

**階段二：對抗式規劃**。Fable 產出計畫後推給 Codex，雙方來回辯論（上限 5 輪）直到達成共識；所有往返記錄寫入一個 markdown log 檔。

**階段三：Codex 建置**。共識計畫交給 Codex 執行（影片當下用 5.5，5.6 上線後即換用）。此時也可選擇改由 Claude 建置或就此停止。

**階段四：Fable 審查**。Codex 完工後由 Fable 全面審查，發現問題就叫 Codex 修，最多兩輪；第三次仍未完成則 Fable 接手自己改。

## Demo：Trip Atlas 旅程規劃 App

- 需求：風格化、電影感的旅行規劃 web app，可輸入多個目的地。
- 訪談階段詢問用途定位（真實個人工具 vs 影片 demo）、geocoding 方案等。
- 對抗式規劃只花兩輪就通過：第一輪鎖定產品定位與技術棧，第二輪提出 12 項與資料核心強化（hardening the data core）相關的發現。
- 成品：世界地圖介面（含 GPT 圖像產生器做的自訂圖案）、可命名旅程、增刪與排序停靠點、新增地點自動顯示距離、SVG 飛機跳點的 cinematic replay 與護照戳章動畫。
- 全程 Fable 端只消耗約 130,000 tokens。
