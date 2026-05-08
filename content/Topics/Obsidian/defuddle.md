---
title: defuddle
created: 2026-03-17
updated: 2026-05-08
source: https://github.com/kepano/defuddle
tags:
  - obsidian
  - skill
  - claude-code
---

網頁內容清洗 CLI（npm `defuddle`），抓回網頁後去除導覽列、廣告、推薦欄等雜訊，輸出乾淨 Markdown，省 token 也讓寫入 vault 的內容直接可用。多 AI harness 可用；Claude Code 透過 `defuddle` skill 看到 URL 時自動載入，`.md` 結尾 URL 走 WebFetch（已是 Markdown 不需清洗）。`vault-youtube-sync` 與 `Inbox/Clippings/` 流程依賴它把外部來源轉成可消化的 Markdown。

## 連結

- Repo：<https://github.com/kepano/defuddle>

## 相關

- [[Obsidian-Skills]]
