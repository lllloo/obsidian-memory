---
title: 讓 Fable 5 與 GPT-5.6 成為網頁設計神器的 Skill
description: 用 Scroll World skill 一次生成含多段捲動動畫的高質感網站，透過 Higgs Field MCP 產圖產片，並比較 Claude Code 的 Fable 5 與 Codex Soul 的 GPT-5.6 表現
created: 2026-07-14
updated: 2026-07-14
source: https://www.youtube.com/watch?v=KBH8P0z2AL8
published: 2026-07-11
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - ai-image
  - multi-model
  - web-design
---

## Scroll World skill 概念

整個示範網站是用一個 skill 在 Claude Fable 5 上一次生成（one-shot）的，內含多段捲動動畫（scroll animation）拼接成連貫、順滑的高質感體驗。若要手動做同樣效果得反覆錄影片、逐一對齊起始幀、逐幀取出，非常繁瑣；這個 skill 把整個流程自動化。

原始版本由 Peter Wing 製作並開源（名為 Scroll World）。作者 fork 後加了幾項改進：

- 引入 **budget tier（預算分級）**，不必每個網站都做滿六個場景，可省成本
- 改善 **mobile 版本** 呈現
- 補上 SEO 相關處理

## 捲動動畫原理

大方向的運作流程：

1. 從一張單一圖片（still image）出發
2. 把該圖片轉成一段影片（scroll animation 本質上曾是一段影片）
3. 用 **FFmpeg** 把影片逐幀拆出
4. 把每一幀對應到使用者在網頁上捲動的位置

背後另有處理讓體驗順滑、不卡頓，並讓各場景（scene）在生成時互相參照，維持整體像是同一個故事的視覺一致性。

## 工具鏈與設定

- 圖片與影片生成透過 **Higgs Field MCP**：呼叫圖像模型（GPT image 2）與影片模型（Seed Dance），全程不必離開終端機。
- 可搭配 **Claude Code** 或 **Codex** 使用，兩者皆可透過 MCP 或 CLI 呼叫這些模型。
- 連接步驟：進 Higgs Field → MCP and CLI → 複製 MCP 的 URL 完成驗證。
- 之後只需要 skill 本身：複製 URL 交給 Claude Code 或 Codex，或以 plugin 形式安裝皆可。

**圖片生成的差異**：在 Codex + Soul（GPT-5.6）下，本身具備原生圖像生成，anchor 等圖片不必送去 Higgs Field，只有影片生成仍需送 Higgs Field。在 Claude Code 下沒有原生圖像生成，圖與片全程都靠 Higgs Field。

## 實際生成流程

skill 會帶你走一段互動式的 interview，全程「牽著手」，不是跑完就把成品丟給你、你毫無置喙餘地：

- **創意方向**：作者範例是「a boutique Japan travel brand」，藝術方向走 origami（摺紙）風格。若沒想法可與 AI 來回問答收斂。
- **預算（場景數）**：範例用 6 個場景，屬於偏長、偏 overkill 的旅程，且吃很多 Higgs Field credits（作者這次約花 800 credits）。若非高階方案，**4 個場景是甜蜜點**，最少可壓到 3 個。
- **mobile 處理**：從安全裁切（crop safe）到完整直式串接（full portrait chain，額外為 mobile 生成影片）都可選；範例走最省的 lean + crop save。
- **journey proposal**：列出每個場景樣貌與所需生成數，例如 4 張圖、4 段場景影片，加上場景間的 connector 與 cross fade，總計約 9 次生成，並給出（通常偏保守的）預估時間。
- **anchor（起始幀）**：核准後先生成 anchor，即主導整體藝術方向的起始靜態圖。**這步要特別把關**——一旦說 yes，後面全部都會以它為基礎。

範例最終約 32 分鐘完成，產出 4 個場景、共 10 次生成，直接跑在 localhost 上。

## Fable 5 與 GPT-5.6 的比較

作者用同一個 skill 分別在 Codex（Soul，GPT-5.6）與 Claude Code（Fable 5）跑，主要差異在**場景轉場（scene transition）**：

- **GPT-5.6（Soul）版**：各場景內部進展（如地鐵駛入的畫面）表現很好，視覺細節也強；但場景一到二、二到三是偏硬的 hard cut。唯獨場景三到四是很棒的轉場——下一個場景先在背景由模糊浮現、帶出 3D 般的景深，再無縫切入。
- **Fable 5（Claude Code）版**：場景到場景的轉場明顯更順滑俐落，接近 seamless。

作者結論：在轉場這點上給 **Fable 5 較高評價**，勝過 GPT-5.6。但兩者都是單一 skill 的 one-shot 成果，整體都相當令人印象深刻。

## 可延伸性

作者認為這種視覺型網站要進一步做成有功能的網站並不難。真正困難的是「做出連貫、不卡頓、不廉價的捲動動畫網站」這個技術問題本身——有了這個基底，後續加文字、CTA、把使用者從 hero 一路引導到填表單，都是每個網站都在做的事，不需要重造輪子。把這些疊在 Fable 5 或 GPT-5.6 生成的基底上並非難事，而「這一切只是一個 skill 的 one-shot」本身就相當驚人。
