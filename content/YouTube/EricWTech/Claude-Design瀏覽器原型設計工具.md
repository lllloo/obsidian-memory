---
title: Claude Design 真的太猛了
created: 2026-04-20
updated: 2026-04-20
published: 2026-04-17
source: https://www.youtube.com/watch?v=x3b42X7rZ1g
parent: "[[01.index]]"
tags:
  - youtube
  - claude
  - design
  - prototyping
---

Anthropic 推出的 Claude Design 可以在瀏覽器中直接產生 app 原型、流程畫面與簡報，並可把設計稿交給 Claude Code 在本機建置成可執行的 HTML。

## 產品定位

- 執行模型：Claude Opus 4.7
- 可用方案：Claude Pro、Max、Team Plan
- 可上傳品牌素材、色票、主題、Figma 檔、字型、Logo，讓 Claude 依此建立 design system 後產出原型
- 也可指向本機程式碼 repo，由 Claude 自動解析現有樣式匯入

## 建立原型流程

1. 進入 Claude Design 建立新 prototype，輸入名稱後按 create
2. 左側為聊天與素材匯入區（可放 screenshots、Figma 檔、design system）
3. 右側為畫布，Claude 會把輸出畫在上面
4. 預設提供兩種風格：
   - **wireframe** — 只有線稿骨架、無顏色
   - **high-fidelity** — 有品牌色的完整 mock-up
5. 送出 prompt 後，Claude 會反問需求（螢幕數、步驟、色彩主次、字型方向、視覺氛圍等）
6. 回答完成後，Claude 產出 to-do 清單，建立元件、iOS frame、各畫面

示範 prompt（bike sharing app）：

```
Create a simple iOS setup flow for the bike sharing app,
show me the screens on the canvas, blue plus orange for the modern color scheme.
```

流程會產生 6 個畫面：welcome、sign up（email/password）、location sharing、plan selection、payment、success。

## 畫布編輯能力

- **Edit**：直接點元件改背景、字體、顏色
- **Draw Tools**：在畫布上畫註記並要求 Claude 套用
- **Comment**：點選單一元件留言，例如「重新設計 logo」，Claude 會針對該元件重做

## 檔案結構

- 產出會建立一個 design 資料夾，裡面包含：
  - `components/` — 各元件的 JSX
  - `design canvas` — 主畫布
  - 各畫面的程式碼
  - 輸出的 HTML 檔

## 匯出選項

可匯出格式：

- PPTX（PowerPoint）
- PDF
- 專案 zip
- Standalone HTML（單一檔案含所有畫面）
- 直接轉交給 Claude Code 繼續建置

## 交棒給 Claude Code

- Claude Design 會產出一段可貼到 Claude Code 的 prompt（引用內部 design 路徑）
- 開新資料夾啟動 Claude Code session，把 prompt 貼入
- Claude Code 會把整個流程實作為 `index.html`，可在瀏覽器直接開啟並互動操作畫面切換
