---
title: Claude Design 快速上手導覽
tags:
  - youtube
created: 2026-04-20
updated: 2026-04-20
published: 2026-04-17
source: https://www.youtube.com/watch?v=-tGH2tLwCEw
parent: "[[01.index]]"
---

## 核心定位

- Anthropic 推出的 Claude Design 是類似 Google Stitch 的視覺設計介面，補上 Claude Code 長期以來前端設計較弱的缺口
- 可用於 web app、mobile app 的 prototype、mockup，並能輸出成 PowerPoint 或送到 Canva
- 使用 Opus 4.7 為核心模型；Pro、Max、Enterprise 訂閱皆可使用
- 與 Google AI Studio 類似，不只是靜態 Canva 型視覺工具，是**可互動的 prototype**，具 API 連接能力

## 進入點與初始選項

- 網址：`claude.ai/design`（web app 專用，不會放進 terminal，desktop 是否支援仍未定）
- 左側選項：Prototype、Slide deck、Template、Other
- 底部可設定 **Design System**：輸入公司名稱、上傳 GitHub repo、本地資料夾、字型、logo 以建立品牌模板
- 大型 codebase 上傳時會自動挑選重要檔案，預估需 15–20 分鐘處理

## 新建專案流程

1. 建立新 prototype（例：`chase demo`）
2. 選 **Wireframe** 或 **High-fidelity Mockup**
3. 撰寫 prompt（可附加語音、檔案、選模型）
4. Claude Design 會主動反問問題（類 plan mode）

### 互動式反問（類 plan mode）

本次示例的反問題目：
- Culture 類型（mixed）
- Globe 樣式
- Flow path 視覺
- Color palette（multi-hue）
- City 範圍（top 10）
- UI 量級（full dashboard）
- Overall mood（editorial）
- 哪些元素需要 tweakable（flow、color palette 等）

與 Claude Code plan mode 只問 3 題左右相比，Claude Design 的反問更深入，可大幅降低後續 iteration 成本。

## 成品互動能力

以「dark themed graphic 展示城市文化流動的旋轉地球」為例，產出結果提供：

- 滑鼠拖曳旋轉地球
- 即時調整 rotation speed、glow intensity、color palette
- 右側生成短文排版
- Full screen 預覽實際效果

## 編輯與協作

### Tweaks

- 針對指定屬性（rotation speed 等）做快速 micro 調整
- 在畫布上已標記為 tweakable 的項目會即時反映變更

### Edit（精修模式）

- 類似 Cursor 或 Lovable 的編輯器
- 可點選個別元件（city、整個 globe）調整 color、height 等具體數值
- 比用文字描述「讓這個變大一點」直觀許多

### Comment

- 點選任一元素留言，可直接送 Claude 處理或加入 queue 待稍後批次送出
- 適合 team review 場景

### Draw

- 在畫布上手繪示意（例：加個月亮、Artemis 2 在旁邊飛）

## 輸出方式

- **Design file**：直接檢視產生的 code
- **Export**：下載 zip、匯出 PDF、PowerPoint、送 Canva
- **到 Claude Code**：提供一行 CLI 指令可直接把專案帶進 Claude Code 繼續工程化

## 與純文字 prompt 的差異

單純把同一段 prompt 丟進 Claude chat 或 Claude Code，本質上也是寫 code，但缺少「視覺迭代」這層體驗：

- 設計工作的本質是視覺的，把視覺需求轉成自然語言再轉成 code 再回到視覺，過程笨重
- Claude Design 讓使用者能一次看到多個選項、直接在視覺層調整，拍板後才進 code
- 這也是 Pencil 等視覺導向工具流行的原因，Claude Design 填補了 Anthropic 生態的這個缺口

## 使用建議

- 若已有現成網站或 codebase，先建一個 Design System 讓 Claude Design 擷取品牌色與字型再開始
- Prompt 結尾要求它先反問，可得到更精準的首版輸出
- 把 Claude Design 當作「視覺設計階段」的工具，決定視覺方向後再 export 到 Claude Code 實作功能
