---
title: Most slept on feature in the Codex App
created: 2026-04-27
updated: 2026-04-27
source: https://www.reddit.com/r/codex/comments/1svaj3v/most_slept_on_feature_in_the_codex_app/
published: 2026-04-25
tags:
  - reddit
  - codex
  - workflow
  - frontend
---

> **繁中摘要**：Codex App（GUI）內建的 browser interaction 面板能截圖+標註特定 UI 元素並送進對話，是前端工作流的大幅升級，含完整啟用步驟。

---

## 原文重點

Codex App（非 CLI）內建一個常被忽略的 browser 面板，能讓你直接在 dev server 預覽中圈選 UI 元素，截圖+標註會自動附到對話中讓模型精準定位。

啟用步驟（macOS 鍵盤）：

1. 在 Codex App 開啟一個 chat（選好 GPT 模型）
2. `Cmd + J` 啟動 dev server
3. `Cmd + Option + B` 開右側 panel
4. 點 `+` → 選 `Browser` → 輸入 localhost URL
5. dev browser 右上會出現 `Screenshot` 與 `Annotations` 按鈕

操作流程：

- 在 dev browser 中點選任一 UI 元素 → 描述要改什麼
- Codex 自動截圖並把標註的元素位置帶進對話
- 等同於「對著畫面指給人看」，省下大量描述成本

延伸體驗：

- 點右上 expand 進入全螢幕 → 中央浮動 chat，是目前看過最佳的互動式設計改稿 UI
- 目前限制：一次只能選一個 component（作者向官方許願多選）

## 社群討論亮點

- 此功能僅 Codex App（GUI）有，CLI 版本沒有；Windows 版操作方式留言詢問中尚未確認
- 替代方案：在 CLI 中用 `@browser` 讓 Codex 開瀏覽器測試與點擊（可看到操作過程），但少了截圖標註的精準定位
