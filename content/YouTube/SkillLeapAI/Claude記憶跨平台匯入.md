---
title: Claude 記憶跨平台匯入
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-04
source: https://www.youtube.com/watch?v=VVnKnGMGlu4
---

## 重點摘要

- Claude 新增記憶匯入功能，可將 ChatGPT 或 Gemini 的記憶轉移至 Claude
- 目的：切換到 Claude 時，過去的偏好、專案、指令不需從頭建立

## 操作步驟

1. 前往 claude.ai → Settings → Capabilities → 確認記憶功能已開啟
2. 點擊「Start Import」，Claude 會提供一段 prompt
3. 將該 prompt 貼至 ChatGPT 或 Gemini，取得記憶匯出檔案
4. 將匯出內容貼回 Claude，Claude 自動儲存至記憶

## 匯出 Prompt（可直接使用）

```
Export all of my stored memories and any context you've learned about me from past conversations. Preserve my words verbatim where possible, especially for instructions and preferences.

Categories (output in this order):
1. Instructions: Rules I've explicitly asked you to follow going forward — tone, format, style, "always do X"
2. Preferences: How I like responses, writing style, communication style
3. Projects: Active projects, goals, ongoing work
4. Personal context: Background information about me, my work, role
```

## 匯出內容分類

- **Instructions**：明確要求的規則（語氣、格式、「always do X」）
- **Preferences**：偏好的回應方式與寫作風格
- **Projects**：進行中的專案與目標
- **Personal context**：背景資料、職位、工作內容
