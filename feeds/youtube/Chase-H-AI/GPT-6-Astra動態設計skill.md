---
title: GPT-6 Astra 用 motion design skill 做動態設計
description: 以 motion design skill 加 Higgsfield MCP 讓 GPT-6 Astra 從簡短提示產出解說動畫、產品爆炸圖與品牌宣傳片的作法與三個實例
created: 2026-09-09
updated: 2026-09-09
source: https://www.youtube.com/watch?v=eyDKoGU_vHk
published: 2026-09-08
parent: "[[01.index]]"
tags:
  - youtube
  - motion-design
  - workflow
---

> [!info] 內容來源
> 影片 transcript 為自動字幕，品牌名有辨識誤差（如 Higgsfield 被辨識成 HAXZEL／HeyGen），此處依上下文統一寫回正確名稱。

## 核心組合

作者主張 GPT-6 Astra 在動態設計（motion design）上是目前最強的模型，但要發揮潛力需要兩個外掛：

- **motion design skill**：給模型一套 motion library，也就是一組現成的參考影片與其背後的 prompt。目的是**永遠不從零開始**，而是拿已知有效的樣板改。
- **Higgsfield MCP**：skill 負責挑參考影片、寫 prompt，實際生成交給 Higgsfield，底層預設用 Seedance 2.5 產影片。

skill 本身不綁模型——影片以 GPT-6 Astra 為例，但同一套在 Claude Code、Fable 5.1 都能跑。差別在 Astra 內建圖像生成能力，而在 Claude Code 或 Fable 5.1 裡則需要另外用 Higgsfield 產參考圖。

## 安裝與設定

- 到 `higgsfield.ai` 的 MCP and CLI 頁面，MCP 或 CLI 兩種接法都可用，選自己的平台後走登入驗證流程。
- 用 ChatGPT 的話是加 Higgsfield plugin，一樣走一次帳密驗證。
- 作者提供兩段 prompt，貼進 Claude Code 或 Codex 即可自動安裝 skill，另附一份 Higgsfield 專用的設定指南。
- 安裝後在 Codex 或 Claude Code 打 `/motion-design` 呼叫該 skill，再給自己的需求描述。

MCP 的實際好處是不必在 Higgsfield UI 與 Codex 之間來回切，全部在終端裡完成。

## 可調整的預設值

- 影片模型預設 Seedance 2.5，可換成任何其他影片模型。
- 圖像模型預設 GPT image，同樣可換。
- 輸入形式可以是純文字、參考圖，甚至參考影片。
- 單支長度示範為 15 秒，作者表示 Seedance 2.5 大約可到 30 秒。

## 內建的自我修正迴圈

值得注意的機制：模型不是「一發入魂然後祈禱」。它生成第一版後，會拿成品與原始 prompt 對照，判斷哪一段沒達到目標，再用 Seedance 2.5 重生成該段，反覆調整直到接近需求。擔心 credit 或 token 消耗的話可以把迭代次數調低。

## 三個實測案例

**1. 2D 解說動畫（純文字提示）**

原始輸入只有一句「用 motion design 做一支 15 秒的 flat vector 解說片，講降噪耳機怎麼運作；沿用 flat vector 樣板、把機制演出來，生成前先給我看完整 prompt」。

skill 把這句話展開成一份完整規格：色盤、主視覺、字體、動態、以及逐格的 beat sheet（每一段要發生什麼），再送給 Higgsfield。成品含配音，共跑了兩次生成。

**2. 產品爆炸圖（樣板 + 參考圖）**

用 style gallery 裡的 deconstructed watch 樣板，提示是「用 motion design 針對這個鍵盤做一支 20 秒的產品爆炸片，用這兩張圖」，附上 Astra 自己生成的兩張參考圖（鍵盤外觀與內部結構）。

**3. 品牌宣傳片（網址當輸入）**

提示是「用 motion design 做一支 20 秒的 kinetic promo，基於 canva.com 的 visual suite」，直接給網頁連結，再補充要演一個虛構咖啡店的行銷素材如何變成社群貼文、限動、簡報，沿用 kinetic typography 樣板收在「一個想法，各種格式」。這支幾乎是一次生成過關。

## 作者的結論與保留

- 三個案例的共同點是**起始輸入都很簡短**，但輸出可用。真要做出有明確視覺主張的東西，還是得靠反覆迭代。
- 直接被問到「動態設計是否已被解決」，作者的回答是否定的——還有很多工作要做。
- 他認為真正的價值在於**抬高地板**：對不是動態設計師的人來說，Astra 或 Fable 5.1 加上這類 skill，已經能產出堪用成果。
