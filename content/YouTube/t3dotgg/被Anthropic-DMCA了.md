---
title: 我被 Anthropic DMCA 了（不是玩笑）
tags:
  - youtube
  - claude-code
created: 2026-04-14
updated: 2026-04-14
published: 2026-04-01
source: https://www.youtube.com/watch?v=icu0GZcSb58
---

## 事件起點

Theo 在報導 Claude Code 原始碼洩漏的隔天，收到 GitHub 的 DMCA 通知，來自 Anthropic。

**關鍵細節：**
- DMCA 對象不是含有洩漏原始碼的 fork，而是 Theo **修改了一個 skill 檔案中一個單字**的官方 Claude Code repo fork
- 一行程式碼改動 = 第一次 GitHub DMCA

## DMCA 的法律背景

- **DMCA（數位千年著作權法）**：允許著作權人向平台通知侵權內容，平台可在不自行審查的情況下下架
- 「安全港」原則：保護平台（如 GitHub）不因用戶上傳的侵權內容而承擔責任
- **反制規定**：被告方可提出反通知，若認為未侵權，著作權人必須在 14 天內提起訴訟，否則內容恢復
- **重要限制**：對未侵權內容發出 DMCA 是非法行為

## 實際發生的事：大規模誤觸發

Anthropic 向 GitHub 提交的 DMCA 涵蓋了 **8,100 個 repo**——這個數字遠超洩漏原始碼的 fork 數量。GitHub 的通知最多只列出 100 個受影響 repo，無法確認其餘情況。

Theo 隨機點選幾個：幾乎全被下架，包括：
- 用 Rust 重寫 Claude Code 的項目（100k star，GitHub 有史以來增長最快的 repo）
- 各種與洩漏原始碼無關的 fork

## Anthropic 的回應：撤回 + 道歉

DMCA 提交後，Anthropic 旋即撤回了對大多數 repo 的通知，只保留實際含有洩漏原始碼的 mirror 及其 96 個 fork。

- Thoric 表示這是**溝通失誤**，並連結撤回通知
- Boris 說明：這不是故意的，他們正在與 GitHub 確認問題所在；**沒有人在 Anthropic 下令 DMCA 這些 fork**

## 誰的責任？

Theo 最終認為責任歸屬不明確，有幾個可能：

1. Anthropic 傳送的原始通知範圍就太廣（可能涵蓋了官方 repo 的所有 fork 網路）
2. GitHub 誤解了請求，自行擴大執行範圍
3. Anthropic 故意這樣做但事後否認

Theo 傾向相信版本 1 或 2，因為：
- 撤回速度非常快
- 大量 Anthropic 員工主動在社群澄清
- 故意 DMCA Theo 對 Anthropic 公關傷害極大

## 不管誰的錯，都是違法的

即使是 GitHub 的操作失誤，若 **DMCA 通知本身要求下架不該下架的內容**，就已違法。Theo 表示若有人發起集體訴訟，他願意參與。

## Anthropic 的正面回應（意外亮點）

這次危機中，Anthropic 罕見地展現了良好的公關處理：

- Thoric 公開洩漏了 buddy 功能，並 tag 開發者 Alistair
- Boris 被問及「負責洩漏的開發者還好嗎」時，給出了標準「無責文化」回應：這是流程問題，不是個人問題；Claude Code 仍在用手動部署，已著手改善自動化
- Boris 澄清原始碼並非透過 Bun 的 source map 問題洩漏

## 根本問題：Claude Code 不應該是閉源的

Theo 的最終結論：整起事件（洩漏、DMCA、危機）都是 Anthropic 選擇閉源的直接結果。

- 所有競品（Gemini CLI、Open Code、Codex CLI）均開源
- 閉源帶來的代價（信任損失、DMCA 爭議、法律風險）遠大於「保護秘密武器」的好處
- Anthropic 在 GitHub 上提交 DMCA 的公司裡是歷史上最多的，這是他們自己造成的局面
