---
title: 本週必做的五個 Fable 5 使用案例
description: 示範五個能榨出 Fable 5 價值的專案：複製既有軟體、稽核 Claude Code 使用方式、打造 agentic OS、程式碼審查除錯、以及打造長時程自訂軟體。
created: 2026-07-06
updated: 2026-07-06
source: https://www.youtube.com/watch?v=lplVBFr0Ndc
published: 2026-07-01
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - workflow
---

影片背景：Fable 5 到 7 月 7 日前還能用 Max 方案（但每週只能用到方案用量上限的 50%），之後就要吃 API 價格。作者列出五個值得在這一週把 Fable 5 指過去、榨出最大價值的專案類型。共通策略：用 Opus 4.8 搭配 deep research 做前期規劃，plan 定稿後才交給 Fable 5 執行，避免用 Fable 跑會噴大量 sub-agent 的 dynamic workflow。

## 案例一：複製既有軟體

複製你正在付費使用的軟體，並客製成自己需要的樣子。示範複製 Whisper Flow，做成純本地、跑在自己機器上、資料不外流的版本。

流程模板：

- 用 Opus 4.8 跑 `/deep-research`（dynamic workflows），研究目標 app（Whisper Flow）如何運作、要在本地重建基本功能需要什麼；可用 Codex 檢查 plan。
- 把 research 報告用 `/goal` 轉成給 Fable 5 的 prompt。`/goal` 適合長時程 agentic 任務，會設定 success criteria 讓模型持續執行到達成目標。
- 切換 model 到 Fable 5，貼上 prompt 讓它執行。

成果是一個本地版 Whisper Flow：聽麥克風、轉錄、送本地 AI model 清理，講完把文字填入輸入框。不含完整功能但涵蓋基本。作者強調不要用 Fable 5 跑 dynamic workflows，否則會燒光用量。

## 案例二：稽核你的 Claude Code 使用方式

讓 Fable 5 對你「怎麼使用 Claude Code」做完整拆解與診斷，跨越所有過往 session 檢視你的 skills、automations、tasks，找出做對、做錯、以及可改進之處（新增 / 修改 skill、加 automation 等）。

- prompt 要點：reflect 過往 Claude Code sessions 找出最高槓桿的 setup 改進；用 sub-agents 從 transcripts 拉原始訊號、跨 session 分群，逐群判斷需要新 skill / automation、修正、或不動；先寫進一份 md 檔，一開始只做診斷、執行前先給人看。
- 這種 prompt 結構參考 Anthropic 官方對 Fable 5 / Mythos 的 prompting 文件（與 Opus 的用法有差異）。

示範中 Fable 5 掃過作者最近 39 個 session，依槓桿高低分成三批建議，從建立新 skill、把某些 skill 設為 automation、到修改 CLAUDE.md 等簡單調整。越是 power user 越能受益。

## 案例三：打造自己的 agentic OS

作者用 Fable 5 打造一個蓋在 Claude Code 上的自訂 wrapper（web app）。是案例二的延伸——把日常 / 每週例行工作編纂成 skills 與 automations，再加上終端機給不了的視覺化 metrics（例如跨平台的內容狀態、morning reports，並串接 Obsidian）。

- 重點不在畫面，而在底層那些 skills 與 automations：用 Fable 5 產出對你有意義的 skill（研究、內容、銷售、財務等），把個別 task 轉成 skill 與 automation，必要時對 skill 套用 loop engineering。
- 底層是跑 Claude headless，不吃 API 價格（Anthropic 幾週前已收回該收費）。
- 商業價值：AI agency 可把這個 web app 打包販售，或 clone 給不用 CLI / 不用 Claude app 的隊友。

## 案例四：程式碼審查與除錯

這個用途直接來自 Anthropic 官方。把 Fable 5 指向複雜專案 / 大型 codebase，找出寫得爛的 code 與真正的 bug。prompt 不需複雜，直接請它做 full code review 並回報找到的 bug 即可。

示範中約 5 分鐘內：四個平行 reviewer 找出 45 個 raw findings，去重成 24 個，再依 severity 分級、逐項說明問題所在與位置，並給出具體修正的優先順序，最後詢問是否要開始處理。作者強調這是在不算複雜的 codebase 上就找到這麼多問題，越複雜的專案越該讓 Fable 5 過目。

## 案例五：打造長時程自訂軟體

讓 Fable 5 打造需要長 horizon 的自訂軟體。示範是一個跑在瀏覽器、用 3JS 做的網頁遊戲（純瀏覽器圖形、非下載式），品質接近 current-gen Unreal Engine 5 展示畫面——作者認為 Opus 4.8 除非你很懂否則做不出來。

- 該專案是 Brapholk 的 open-source 作品，在 Fable 5 首次推出時用它打造。價值在於能看到他如何從零做出來。
- 關鍵是那份 PRD（product requirements document）：一份由人「部分手寫」的 markdown，寫明要 build 什麼、視覺目標、application pillars、instructions、constraints 等。
- 要做自己的專案，先把 PRD 釘死。Opus 4.8 可協助起頭寫出帶具體 instructions 與 requirements 的 PRD（同樣可用 deep research 輔助），定稿後交給 Fable 5 跨長時程自主 session 執行，複用案例一的流程。

此設定中 Fable 5 寫了 21,000 行 TypeScript、跨 90 多個 commit 完成上述遊戲。
