---
title: AI週報：Claude Mythos 資安震撼、Meta Muse Spark、GLM-5.1
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-10
source: https://www.youtube.com/watch?v=SguncMvE77I
---

## Claude Mythos 與 Project Glasswing

Anthropic 發布了內部代號 Mythos 的新模型，定位為史上最強 coding 模型，但因資安風險選擇不公開發布：

- 在 Swebench Pro 上比 Opus 4.6 高出 24 個百分點
- Terminal Bench 高出 17 個百分點；Swebench multimodal 約兩倍
- 發現 27 年前的 OpenBSD 漏洞、16 年前的 FFmpeg 漏洞，並自主串接 Linux kernel 多個漏洞
- 附 245 頁 System Card，明確說明因資安能力過強而不對外開放

**Project Glasswing**：Anthropic 將 Mythos 提供給 Apple、Microsoft、Nvidia、Cisco、CrowdStrike 等合作公司的資安專家，目的是在類似能力的模型被惡意行為者取得前，提前修補既有產品漏洞。

Mythos 的訓練目標是 coding，資安能力是副產品——模型越懂程式碼，就越懂漏洞利用。

## Meta Muse Spark

Meta AI Super Intelligence Labs（由 Alexander Wang 主導）首發模型：

- 圖表理解（figure understanding）超越所有 frontier 模型
- Swebench coding 排名低於 Opus 4.6 和 Gemini 3.1，與 Grok 4.2 相近
- HealthBench hard open-ended 排名最高
- 整體在 Artificial Analysis Intelligence Index 從 Llama 4 Maverick 墊底躍升至第四名
- Token 效率佳，預期 API 定價較低；**非開源**

## GLM-5.1（ZAI）

這週最被低估的模型：

- MIT license 開源，模型權重可從 HuggingFace 下載
- Swebench Pro：58.4（GPT 5.4 為 57.7，Opus 4.6 為 57.3）
- 開源模型中首次達到 frontier 閉源模型的 coding 水準

## Gemini 新功能

- **互動視覺化**：可生成帶滑桿的互動模擬（與 OpenAI / Anthropic 類似功能）
- **Notebooks**：類似 Claude Projects 的工作空間，可同步 Notebook LM，目前限付費用戶

## Seedance 2.0

ByteDance 影片模型，本週起可在美國透過 Runway 和 CapCut 使用：
- 生成速度快於 Kling 3.0
- 因版權問題，商標 IP 和名人臉孔等功能已被移除

## HeyGen Avatar V

- 只需錄製 15 秒影片即可建立數位分身
- 語音和唇形同步仍有改善空間

## 其他快訊

- **OpenAI 新訂閱方案**：推出 $100/月方案，Codex 用量為 Plus 的 5 倍
- **Claude Managed Agents**：在 platform.claude.com 可建立連結 Notion、Slack、Asana 的 Agent
- **Claude 訂閱不再涵蓋第三方工具**（如 OpenClaw）：2026-04-04 起生效，需改用 API key
- **Perplexity + Plaid**：可連結金融帳戶，唯讀取用
- **Factory AI Desktop App**：從 CLI 轉為桌面應用，可直接啟動 AI droid 任務
- **Cursor**：可從手機遠端控制電腦上的 Cursor
- **xAI 圖片編輯**：文字描述修改圖片，iOS 先行
- **Spotify Prompted Podcasts**：依描述生成播客清單
