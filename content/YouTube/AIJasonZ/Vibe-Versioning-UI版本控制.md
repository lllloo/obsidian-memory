---
title: Vibe Versioning：Cursor UI 迭代版本控制
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-06-15
source: https://www.youtube.com/watch?v=JfMcFjD-tIA
parent: "[[01.index]]"
---

## 問題背景

- 在 cursor/Claude Code 中迭代 UI 缺乏版本控制
- v0 等平台有內建版本歷史，可在各版本間切換比較
- Git 太重量，不適合 UI 快速迭代時的頻繁儲存

## 解決方案：Yoyo 外掛

開源 cursor/Windsurf/Claude Code 外掛，提供輕量版本快照。

### 安裝

點擊安裝按鈕即可加入 IDE。

### 基本操作

- 點擊「Save version」按鈕建立快照
- 可加入說明文字（yoyo 會自動補充描述）
- 在版本清單中點擊任一版本，在 Simple Browser 中預覽

### 版本查詢

```
which version was the initial light mode?
```

yoyo extension 會自動找到對應版本並切換。

## UI 迭代工作流

### 取得設計靈感

- Dribbble：各種 UI 設計截圖
- Mobbin：真實 App 的 UI mockup

### 第一步：從截圖建立初版

提示模板：
```
作為資深前端工程師/設計師，依附件 mockup 建立 UI
請先分析設計系統、字型與元件
先用 mock data 實作第一頁
```

在 cursor 中用 `Cmd+Shift+P` → Simple Browser 預覽。

### 第二步：儲存基底版本

點擊「Save version」→ 命名為「initial UI」

### 第三步：依細節反覆迭代

- 針對特定元件給精確的修改指示
- 滿意後儲存新版本

### 版本範例

- V1：初版（dark mode）
- V2：精修深色版
- V3：light mode 版
- V4：Apple liquid glass 風格版

## Liquid Glass 風格範例

```
請將整個 UI 更新為 Apple 新的 liquid glass 風格
以下是參考 CSS（從 GitHub 複製）：<貼上 CSS>
```

## 核心價值

- 不怕 AI 亂改：隨時可回退到任一版本
- 比 git commit 輕量，適合設計探索階段
- 可跨風格比較（暗色/亮色/各種主題）
