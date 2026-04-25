---
title: defuddle
created: 2026-03-17
updated: 2026-04-25
tags:
  - obsidian
  - skill
  - claude-code
---

`defuddle` 是 Claude Code 的網頁剪藏 skill：抓回網頁後去除導覽列、廣告、推薦欄等雜訊，輸出乾淨 Markdown，比 raw HTML 省下大量 token，也讓後續寫入 vault 的內容直接可用。

## 用法

Claude Code 看到 URL 時自動載入 `defuddle`，不需手動呼叫。輸出的 Markdown 可直接寫入筆記，或當作上下文閱讀。

## 適用範圍

- 一般網頁、文章、部落格、線上文件 → 用 `defuddle`
- `.md` 結尾的 URL → 直接用 WebFetch（原本就是 Markdown，不需要再清）
- 純語法查詢、即時系統狀態等不需要內文的問題 → 不觸發

## 與 vault 的整合

`vault-youtube-sync` skill 與 `Inbox/Clippings/` 流程都依賴 `defuddle` 把外部來源轉成可消化的 Markdown，這是把網頁納入吸收型卡片盒的第一步。

## 相關
- [[Obsidian-Skills]]
