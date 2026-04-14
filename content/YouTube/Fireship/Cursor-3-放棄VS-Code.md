---
title: Cursor 3 放棄 VS Code 改用 Rust 重寫
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-06
source: https://www.youtube.com/watch?v=JSuS-zXMVwE
---

## Cursor 版本演進

| 版本 | 定位 | 概念 |
|------|------|------|
| 1.0 | VS Code fork，AI 自動補全 | 副駕駛 |
| 2.0 | Chat 視圖，可控制終端機建置功能 | 機長 |
| 3.0 | 管理多 agent 跨 repo、跨機器、雲端 | 航管員 |

Cursor 3.0 **完全以 Rust + TypeScript 重寫**，不再是 VS Code fork，但舊版 VS Code 編輯器仍保留。

## Composer 2 模型爭議

- Cursor 同步發布 **Composer 2** 自家訓練模型，宣稱超越 Claude Opus 4.6
- 後來被發現其實是基於 **Moonshot 的 Kimi K2 模型**，透過強化學習調整而來
- 有人在 Composer metadata 找到 model ID，在 Twitter 公開後 Cursor 才承認
- Kimi 本身曾被指控用 Claude 輸出訓練，因為偶爾會回應「Hi, I'm Claude」
- Cursor 後來為不透明道歉，並發布完整技術報告

## Cursor 3 新功能

**多 Agent 並行管理：**
- 可同時在多個 repo、機器（含遠端 SSH）、雲端執行不同 agent
- 黃點：需要人類介入（通常是授權執行危險指令）
- 藍點：工作完成，等待審核

**Plan Mode：**
- 在開始寫程式前，先讓 agent 規劃基本架構

**內建瀏覽器：**
- 可直接在介面內瀏覽 app 並預覽結果

**Design Mode：**
- 直接框選 UI 元素要求 AI 修改，不用手動改 CSS

## 實際示範

以「Horse Tinder」為例：
1. 開新專案 → Plan Mode 規劃架構
2. 同時啟動另一個 agent 做 landing page
3. SSH 到雲端伺服器讓 agent 做遠端工作
4. 幾分鐘後生成 13,000 行程式碼
5. 用 Design Mode 調整 UI 細節
6. 全程幾乎不需親自寫程式

## 爭議

部分人認為新介面與 OpenAI Codex 過於相似。Rust 重寫對記憶體使用有所改善，但不是所有人都適應這個以 agent 為核心的新方向。
