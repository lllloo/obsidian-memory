---
title: Claude Mythos 被 Anthropic 封鎖的危險模型
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-10
source: https://www.youtube.com/watch?v=d3Qq-rkp_to
---

## Mythos 是什麼

- Anthropic 發佈了一個名為 Mythos 的新模型，但不對外公開
- 官方聲稱其能力強大到若公開釋出，可能對經濟、公共安全與國家安全造成嚴重威脅
- 消息一出引發業界廣泛恐慌，也有人認為 Anthropic 只是在炒作

## Mythos 的安全研究成果

Anthropic 內部測試中，Mythos 展現出驚人的漏洞挖掘能力：

- 發現 FFmpeg 長達 16 年的漏洞，可透過惡意影片檔案觸發記憶體錯誤
- 發現 OpenBSD 長達 27 年的漏洞，可讓遠端攻擊者透過 TCP 讓系統瞬間崩潰
- 在各大主流瀏覽器找到 JavaScript 引擎漏洞，可讓惡意網頁逃脫瀏覽器沙箱，進而竊取跨站資料或直接寫入 OS kernel
- 發現 Linux kernel 漏洞，可翻轉鄰近記憶體頁面的單一 bit，將密碼執行檔改為可寫入，進而取得 root 權限

美國財政部長與聯準會主席也因 Mythos 的安全風險，緊急召集銀行 CEO 開會。

## Project Glass Wing

- Anthropic 宣布「Project Glass Wing」，聯合一批付費大客戶，讓 Mythos 僅限這些機構用於修補全球關鍵軟體
- 邏輯是：Mythos 對普通用戶太危險，但在大型企業手中是安全的
- 計畫是在其他組織建出同等能力的模型之前，搶先修補全球軟體漏洞

## 質疑聲浪

並非所有人都信服 Mythos 的能力：

- Anthropic 自 2024 年 2 月起內部使用 Mythos，期間卻發生 Claude Code 原始碼外洩、Mythos 文件外洩、API 持續不穩定等問題
- OpenBSD 漏洞是透過 **千次平行 agent 跑遍 codebase**，花費近 **$20,000 算力** 才找到，並非單次查詢
- 若用 Opus 4.6 或 GPT-5.4 Pro 以相同方式跑，應該也能找到類似問題
- Firefox 的 84% 漏洞成功率，是在關掉沙箱與其他防護的 SpiderMonkey shell 上測試，並非對真實 Firefox

## 結論

Mythos 很可能確實比目前旗艦 Opus 4.6 有所進步，但「毀滅世界」的說法過度誇大。目前它仍是個大俱樂部，普通開發者進不去。
