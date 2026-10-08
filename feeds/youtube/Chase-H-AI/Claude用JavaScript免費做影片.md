---
title: Claude 靠 JavaScript 免費做影片
description: Claude 以 JavaScript 逐格繪圖、Playwright 自檢、FFmpeg 合成影片，分 prompt、迴圈、參考素材、skill 四層。
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=rscb1DgJtNg
published: 2026-10-06
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - motion-design
  - workflow
---

不需要 Remotion、不需要 After Effects，只靠 Claude Code 加 JavaScript 就能做出視覺講解、產品 demo、純 motion graphics 類影片。這不是 AI 影片生成器，成本只有用量，幾乎免費。

## 運作原理：影片是時間的函數

- Claude 寫一個函數：給定時間 `t`，回傳一張畫面；同一個 `t` 永遠回傳同一張，所以任何一格都能單獨重繪或檢查。
- 每秒取 60 張畫面依序播放，就是 1 秒影片。
- 用 headless browser（如 Playwright，等於 Claude Code 自己的一個 Chrome）繪製每一格。
- Claude 看不了影片，但能逐格看畫面、找出問題、修正函數。
- 滿意後（Claude 自判或你核可）用開源的 FFmpeg 把畫面串成 MP4。
- 聲音也可以是時間函數；示範影片的旁白用 ElevenLabs 生成，先寫腳本再讓畫面配合。

作者把整件事拆成四個層級。

## Level 1：Prompt 與 effort

- 測試 prompt：「做一支 15 秒動態 motion graphics 影片，展現你是多厲害的動態設計師，像履歷用的 show reel，全力發揮，不用任何 skill」。
- 分別用 Opus 5.5 的 low、high、ultra 跑：low 約 20 分鐘、high 約 30 分鐘、ultra 跑了 8 小時。ultra 最好，但 low 與 high 也都相當不錯。
- 結論：Claude 用 JavaScript 的基礎能力很強；如果覺得成果不好，多半是 prompt 問題，不是 effort 問題。
- **最有效的一招是先要 storyboard**：在動手寫 code 前，讓它產出代表影片各段節拍的單格畫面（例如 7 個主要場景），先在這階段調整方向。這類生成很耗時，避免「做完 20 分鐘才發現不喜歡、反覆重做好幾小時」的循環。

## Level 2：工具與自檢迴圈

Prompt 結構要交代：

- 長度與類型（如「30 秒動畫講解，主題是某某如何運作」）。
- 畫面比例：橫式全螢幕，或短影音用的直式。
- 明講用 JavaScript。
- 配樂：可以純程式生成，也可以自己提供；也能倒過來做——先給旁白音檔，讓 Claude 讓畫面對齊音訊。
- 明講用 Playwright 與 FFmpeg 輸出 MP4：Playwright 跑 headless browser 檢查畫面，FFmpeg 負責合成。
- 若有旁白：「這是旁白 MP3，讓畫面對齊時間點」。
- 收尾要求自檢迴圈，例如：

```text
Before you call it done, use ffmpeg to pull a contact sheet,
look at it, fix what's wrong, re-render, and repeat.
```

Opus 5.5 與 Fable 5.1 就算沒講也大多會自己這樣做，但理解原理才知道它沒做時該怎麼指示。必要依賴：Playwright、FFmpeg，另外要決定先做畫面再配音，還是先有音軌／旁白再讓畫面對齊。旁白可用 ElevenLabs（作者認為品質最好，月費約 5 美元，剛推出 MCP；非業配），也有不少開源替代方案。

## Level 3：加入參考素材

- 可給圖片：直接插入畫面，或要求模仿其美學風格。
- 可給影片：以其構圖為靈感、換上自己的內容。
- 示範：參考影片是用 Opus 5.5 + Remotion 做的貨幣主題影片，JavaScript 重製版改講電力史，構圖幾乎同一家族、內容完全不同。
- 靈感來源：skillery.dev 有 AI 影片分類（付費，免費版也能看不少）；Twitter 上有創作者展示這類影片的上限水準。

## Level 4：Skill 化

作者把整套流程封裝成 Claude Code skill 並公開：

- 內建 7 種預設風格（如 cut paper、cross-hatch、risograph、sketchbook、isometric），也可用參考圖／參考影片做自訂風格。
- 流程分階段且會引導你：intake 問答（主題、格式、音訊、旁白、是否要從頭貫穿到尾的主角）→ 故事結構 → storyboard → 寫 code 並交付。
- 全程自動跑 Playwright + FFmpeg 的檢查迴圈，確保同步與合理。
- 安裝可走 plugin，或把 repo URL 丟給 Claude Code 讓它自己裝；會一併確認 Playwright、FFmpeg、faster-whisper 等依賴，並詢問是否接 ElevenLabs connector。
- 仍在迭代中，歡迎開 PR 改進。
