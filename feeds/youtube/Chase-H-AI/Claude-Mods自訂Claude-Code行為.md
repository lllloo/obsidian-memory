---
title: Claude Mods 是 Skills 之後最大的 Claude Code 升級
description: Claude Mods 以 plugin 攔截改寫 Claude Code 事件與介面；示範下一步面板、cache 倒數，並用 session 稽核找 mod。
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=Rn4nmFRPe0s
published: 2026-10-02
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - workflow
  - token-optimization
---

> [!note] 本片 transcript 為阿拉伯語自動翻譯版，內容依翻譯稿整理為繁中。

Anthropic 推出 Claude Mods，讓 Claude Code 本身也變成「一切皆 plugin」：可以改寫事件、改變 UI、修改既有功能或新增全新功能。Claude Mods 是上個月初「function hooks」概念的正式版——當時 Anthropic 的 Boris 在推文中提到正在探索讓 Claude Code 更可客製的方式，只以 GitHub PR 形式試驗，如今已是所有人可用的正式功能。

## Mod 的運作方式

Mod 改變 Claude 的行為：每當 Claude 要做某件事，都能用 mod 介入。以「刪除 build 資料夾」為例，同一個事件可以有四種 mod：

- **事件前**：每次要刪東西時先暫停，列出將刪除的 41 個檔案給你看。
- **改寫事件本身**：不永久刪除，改丟進資源回收筒。
- **事件後**：每次刪除後回報「刪了這 41 個檔案、位置在哪」。
- **包住整個流程**：刪除前先備份，讓你能復原（相當於 Ctrl+Z）。

重點：Claude 做的任何事現在都能改。過去只能用 hooks 與 skills 繞道處理的核心行為，現在可以直接深入結構調整。

社群範例從娛樂到實用都有：等待 Claude 跑任務時開啟一個多人 Doom 伺服器（裡面都是同樣在等 Claude 的人）、即時顯示專案進度的進度條等。

## 管理位置

Mods 透過 plugin 系統運作：輸入 `/plugins` 可看到所有已安裝的 mod。在 desktop app 與 terminal 都適用。

## 範例一：下一步選項面板

- 請 Claude 做一個簡單的習慣追蹤 app 後，底部會出現一個自訂面板，列出三個「下一步」選項。
- 不用手動問「你覺得下一步該做什麼」，點一下就套用該選項並開始執行。
- 本質上是改造底部的 prompt 列：原本有時只預載一個建議 prompt，這個 mod 改成同時給多個，適合不確定要走哪條路的情況。
- 這種自訂面板過去根本不存在。

## 範例二：Prompt cache 倒數計時

- 維持 cache 熱度對成本與用量很重要：每則訊息都會把整段對話送到 Anthropic 伺服器，cache 有效時折扣可達約 95%。
- cache 只維持一小時，超過一小時沒互動就要用全價重送整段對話（作者當時 context 約 160K token），而人常常不知道過了多久。
- 這個 mod 顯示「cache 變冷前還剩 43 分鐘」，並附一個按鈕：快到期、context 又快滿、自己要離開一下時，按下去就開始 compact 對話。
- Mod 不必是龐大複雜的 workflow，可以像客製 status line 一樣簡單地強化 UI。

## 自己打造 mod：先做使用稽核

最強的 mod 是為你量身打造的。Claude 已經懂得怎麼建立與安裝 mod，只需要給一點方向——用稽核 prompt：

```text
稽核我怎麼使用 Claude Code：讀我最近 30 個 session，
找出我反覆要求的事，然後提出 5 個能解決這些問題的 Claude Code mod。
```

- 作者實跑得到五個左右的建議：demo 演練輔助、專案追蹤、mod 檢查器、cache 計時器、undo 模組，外加一個拼字修正。
- 接著直接說「我喜歡第一個，做吧」，Claude 就會建立 plugin、安裝，並提示你 reload plugins。
- Mod 不是需要呼叫的 skill，而是像 hook 一樣自動執行；設定後持續生效，直到解除安裝。要關掉或移除也只需用自然語言告訴 Claude。

## 作者看法

預期幾個月內會出現類似 skills 生態系的 mod 生態，GitHub 上會大量發佈，但最有價值的仍是針對自己 workflow 的那些，建議先跑一次稽核看看結果。
