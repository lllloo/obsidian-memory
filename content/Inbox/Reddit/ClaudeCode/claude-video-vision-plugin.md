---
title: A plugin that lets Claude Code watch videos; image + audio
created: 2026-04-27
updated: 2026-04-27
source: https://www.reddit.com/r/ClaudeCode/comments/1ssub0g/a_plugin_that_lets_claude_code_watch_videos_image/
published: 2026-04-22
tags:
  - reddit
  - claude-code
  - ai-tools
  - workflow
---

> **繁中摘要**：`claude-video-vision` plugin 把影片拆成 frames（adaptive fps）+ 音訊轉錄餵給 Claude Code，補上 Claude 缺失的影片感知層。支援 Gemini API / 本地 Whisper / OpenAI Whisper 三種音訊 backend。

---

## 原文重點

**問題**：Claude 原生不接受影片或音訊輸入，過去要看影片必須手動截圖 + 抄寫音訊。

**做法**：

- Frames 用 **adaptive fps** 抽取：Claude 依照問題自行決定抽幀率（「這 1 小時演講摘要」與「1:30 畫面是什麼」抽法不同）
- 音訊三種 backend 可選：
  - **Gemini API**：原生音訊理解，能聽出語音 + 音樂 + 咳嗽 + 動物叫聲，免費額度 1500 req/day
  - **本地 Whisper**：完全離線，首次使用自動下載 model
  - **OpenAI Whisper API**
- Claude 同時拿到 frames 與帶 timestamp 的音訊轉錄，當作同一個東西去推理

**安裝指令**（在 Claude Code 內逐條執行）：

```
/plugin marketplace add https://github.com/jordanrendric/claude-video-vision
/plugin install claude-video-vision
/setup-video-vision
```

**使用**：

```
/watch-video demo.mp4
/watch-video tutorial.mp4 "what language is this person using?"
```

也可以對話中提到檔名（「看一下 bug-report.mov 的前一秒」），plugin 會自動調整 fps、解析度、時間範圍。

**主要 use case**：

- 用螢幕錄影 debug，不用文字描述 UI bug
- 摘要教學影片、talk、會議錄影
- 抓影片畫面中可見的文字或程式碼
- 「X 發生前一秒是什麼」這類定位需求

**Repo**：<https://github.com/jordanrendric/claude-video-vision>（MIT，無付費、無帳號、無 telemetry）

作者只在 macOS 測過，Linux/Windows 結果歡迎回報。

## 社群討論亮點

- 「screen recording debug」被視為殺手用例：丟 `.mov` 直接讓 Claude 看，比寫一大段 UI bug 描述快
- adaptive fps 設計合理：問特定事件時應在事件附近抽密集 frames，摘要型問題則整體稀疏
- 留言提醒：影像 token 成本，單張 image 約 1500 tokens，整段影片 frames 串流的 token 用量需注意
