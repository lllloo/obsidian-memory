---
title: Stitch vs Claude Design 設計工具對決
created: 2026-05-15
updated: 2026-05-15
source: https://www.youtube.com/watch?v=PJ9CmTODmVo
published: 2026-05-12
parent: "[[01.index]]"
tags:
  - youtube
  - ai-design
  - claude-code
  - google-stitch
---

> [!info] 影片定位
> 在 Claude Design（隨 Opus 4.7 推出）與 Google Stitch 2.0（搭 Gemini 3）兩款 AI 設計工具皆升級後，跨「功能 / 價格 / 設計品質 / 圖片 / 動畫 / 迭代 / 設計系統 / 交付」八個面向實測對比，分項判定誰勝出，回答「Figma killer 之爭」實際答案。

## 結論一覽（誰勝在哪）

| 面向 | 勝出 | 關鍵原因 |
| --- | --- | --- |
| 功能廣度 | Claude Design | 簡報、speaker notes、團隊權限分離 |
| 價格 / 額度 | Google Stitch | 免費 + 每日 400 design credits |
| 首版設計品質 | Google Stitch | 色彩配置更有深度、速度更快 |
| 圖片生成 | Google Stitch | 內建 nano banana，非 SVG |
| 動畫 | Claude Design | 用 shaders 等 library、可隨滑鼠互動 |
| 迭代修改 | Claude Design | 直接在畫面上 comment、不另開螢幕 |
| 設計系統 | Google Stitch | design.md 跨工具可用、不鎖平台 |
| 交付到程式 | Google Stitch | 有 MCP，coding agent 直接雙向溝通 |

## 功能差異

- Claude Design 可建立**簡報**並寫 speaker notes；Stitch 只做 mobile / web UI，不涉其他設計類型
- 風格參考：Claude Design 透過連 **GitHub repo** 匯入既有設計風格；Stitch 用 **design system**，貼上網站 URL 即抽取風格
- 修改方式：
  - Claude Design：直接點選畫面區塊下 comment，可堆疊多個 comment 一起送
  - Stitch：除文字外不能直改，需先 annotate 再送 comment 給 Gemini
- 語音輸入：Claude Design 是語音輸入 prompt；Stitch 的 **voice canvas** 是真正的對話式設計，模型會反問細節後出稿
- 預覽：Stitch 有獨立 pane 切換 desktop / mobile / tablet 看 responsive；Claude Design 在同一 pane 直接互動，但無響應式預覽
- 團隊協作：Claude Design 支援編輯／註解權限分離；Stitch 只能整個 project 共享

## 價格與用量

- **Google Stitch**：免費，credit 制
  - 每日 **400 design credits** + **15 redesign credits**
  - 一個簡單設計約 3 credits（依複雜度與生成次數變動）
- **Claude Design**：限 Pro / Max / Team / Enterprise plan
  - 用量限制為**週**為單位，不吃 Claude Code 主額度
  - Pro plan 額度實務上「不夠實驗」，跑幾個設計就耗盡；要正式用得上 Max plan

## 首版設計實測

同一個 prompt（含網站風格與所需 sections）餵兩邊：

- **Stitch** 先建 design system（色彩、字型、icon、button 全部視覺化），用該系統產出 landing page，主色與輔色平衡良好；速度快，Claude Design 還沒完成它就已完工
- **Claude Design** 仿 Claude Code 風格先建 to-do 列表逐項執行；完成後跑 verification step，並讓使用者在主色與 accent 之間做選擇
- 設計品質：Stitch 用色更有層次、貼合 app 氛圍；Claude Design 偏 generic

## 圖片生成

- **Claude Design**：未提供素材時靠 SVG 生成並塞入設計，再高品質的 SVG 仍打不過 image model
- **Google Stitch**：直接整合 Google 自家的 **nano banana** 影像模型，即使不主動要求也會自動為各 section 生圖

## 動畫測試

- **Stitch**：嘗試加動畫但效果有限，只有 hero 區有 scroll reveal，且需另開 tab 才能預覽
- **Claude Design**：自動加 marquee（hero 下方）、scroll reveal 套用到各 component、能用 **shaders** 等 library 產出隨滑鼠移動／點擊變化的互動動畫

## 迭代修改

新增 signup / login 頁面測試：

- **Stitch**：先完成，沿用同一 design system，header / footer 一致；prototype 功能可看 button 連結關係。但每次修改都會**生成新畫面**，畫面很快變得擁擠；範例中加 footer 還被放錯位置
- **Claude Design**：login 頁更貼合 app 概念，signup 頁主動實作多種帳號類型；改動透過 comment 直接反映在原畫面，理解 app 後改得不偏離既有風格

## 設計系統

- **Claude Design**：design system = 品牌識別，包含品牌描述、字型、logo、assets 等，鎖定團隊的 brand kit 場景
- **Google Stitch**：design system = 一個**檔案**（代表某個設計風格），不綁特定品牌
  - 已 open-source `design.md`，內含 npm 安裝指令與格式規範
  - **可匯出到任何 agent** 直接讀懂並套用 → 跨平台不鎖死

## 交付到程式（Handoff）

- **Claude Design**：
  - 複製單一 prompt 貼進 Claude Code 即可實作
  - 額外可匯出 PDF slides、Canva 繼續編輯
  - **沒有 MCP**
- **Google Stitch**：
  - 有 **MCP**：coding agent 與 Stitch 雙向溝通，agent 用 Stitch 偏好的語言下 prompt，省去 prompt 工程
  - 可匯出 zip code、Google AI Studio（內建 Firebase 整合）、Figma
  - 可匯出 **PRD**，直接交給其他人或 coding agent 實作

## 取捨建議

- 要做**團隊品牌 design system + 互動動畫 + 與 Claude Code 緊密整合** → Claude Design
- 要**便宜大量生成 + 高品質首版 + MCP 雙向交付 + 跨工具設計系統** → Google Stitch
- 額度上 Stitch 對「實驗階段」近乎無痛；Claude Design 在 Pro plan 幾乎無法正常摸索
