---
title: Open Design 開源 Claude Design 替代品
created: 2026-05-04
updated: 2026-05-04
source: https://www.youtube.com/watch?v=BGQ9i3fvNds
published: 2026-05-01
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
---

## 為什麼會出現 Open Design

- 第二個 Claude Design 開源克隆，但這次帶**圖形介面**（前一個 Huashu Design 只有 terminal）
- 視覺上與 Claude Design 高度相似，整體流程也很接近
- 主要動機：作者愛用 Claude Design，但其 usage 額度太緊；越多開源替代品出現，越能逼 Anthropic 修正 usage 政策

## 核心特色

- 任何 coding agent 都可接：Claude Code、Codex、Gemini、Open Code（也支援自帶 API key）
- 自動偵測本機現有 coding agents
- **31 個 skills + 72 brand design systems** 預載
- 上層介面 + 底層工具集合：Huashu Design、Guzheng PowerPoint Skill、Open Code Design、Multika

## 安裝

兩種方式：

1. 進 repo 開 terminal 貼上一段安裝指令
2. 複製 repo 連結 → 丟進 Claude Code → 「幫我在新目錄安裝這個」

安裝後若沒自動起 dev server：請 Claude Code「spin up a dev server for Open Design」。

## 設定

- AI 系統選擇：選 **local CLI**（用 Claude Code / Codex 帳號，免付 API 費）
- model 選 default（即 CLI 設定）
- 可掛 media providers（OpenAI、MiniMax、ElevenLabs 等）做 image / video 生成——這項是 Claude Design 沒有的

## 介面分區評估

| 分區 | 評價 |
| --- | --- |
| Designs / 建立 prototype 與 slide deck | **核心價值**，與 Claude Design 機制幾乎相同 |
| Examples | 看似炫，實際就是 1 行 prompt 跑出來的，沒有秘方 |
| Design Systems | 類似 awesome-design.md，可用 Airbnb 等品牌的 palette/typography/components 為基底 |
| Image Templates | 作者認為是 bloat |
| Video Templates | 同樣 bloat |

## 建立 Prototype 流程

操作與 Claude Design 幾乎一樣：

1. 命名 demo
2. 選 design system（可單選或多選）
3. 選 wireframe 或 high-fidelity
4. 可上傳 Claude Design 匯出的 zip 當 design system
5. 進入訪談式 Q&A，作者反饋與 Claude Design 同等深度

## 與 Claude Design 直接對比（同樣 Lighthouse SaaS landing page prompt）

- 配色、字型、editorial 風格輸出**非常接近**
- Open Design 慢約一倍：~10 分鐘 vs Claude Design ~5 分鐘
- 介面標示的 common / edit / draw 功能在 Open Design **尚未實作**（roadmap 中）
- 想要 tweaks panel 須直接 prompt 它生成

## 自帶 Design System 的兩條路徑

無原生上傳介面：

1. **走 Claude Design 出口**：在 Claude Design 中建好 design system → share → download project as zip → 在 Open Design 內 import zip
2. **沒有 Claude Design 來源**：建議先去 Claude Design 弄一個再回來；或直接在 Codex / Claude Code 終端內請它讀 directory 的所有資產然後仿照建立——這條比較 janky

作者點評：這是 Open Design 比 Huashu Design **不便利**之處——Huashu 在 terminal 直接「讀整個資料夾」就能繼承風格，UI 反而綁手綁腳。

## Slide Deck 實測（brutalist + 自家 Agentic OS 設計系統）

訪談題：deck 對象 / 觀眾 / 頁數 / fidelity / 是否要 speaker note / visual tone / 用哪個 design system / 是否讓它決定故事節奏。

匯出 PowerPoint 觀察：

- 第 1 / 第 4 / 第 5 投影片良好
- 第 2 / 第 6 / 第 7 投影片有微幅排版瑕疵（位移、間距、邊界）
- 整體達 90% 完工度，**約 5 分鐘可手動修齊**

## 結論

- 才剛上線，能做到這程度算很穩
- 喜歡 Claude Design 的圖形介面又被 usage 限制卡住 → 推薦 Open Design
- 不需要 GUI、想要更彈性與更快輸出 → **Huashu Design 仍是更好選擇**
- 越多此類工具出現，越能促成 Anthropic 修正 usage 問題
