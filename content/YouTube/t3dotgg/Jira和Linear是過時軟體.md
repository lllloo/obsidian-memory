---
title: Jira 和 Linear 是過時軟體
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-27
source: https://www.youtube.com/watch?v=pzUn9wTCgcw
---

## Issue Tracker 已死

Linear 自己宣告 issue tracking 已死，原因是這套系統是為「交接型開發模式」設計的：PM 規劃工作，工程師領取執行，中間需要複雜的優先序排列與工作流管理。這個模式的前提是工程師時間稀缺，需要仔細分配。

現在 AI 打破了這個前提。

## Theo 在 Twitch 的原型方法論

Theo 早在 AI 時代之前就反對先寫規格再開發的流程，主張：

1. 先用 1-3 天建出可用的原型，逼出 UX 問題與技術盲點
2. 拿原型測試用戶，收集反饋
3. 再寫規格（此時規格會準確得多）
4. 真正動工開發

約一半的情況下，原型稍加打磨就直接出貨。這套方法在 Twitch 內部被稱為「Theo prototype」，但也讓他的升遷文件沒有漂亮的規格書可以展示。

## AI 時代的 Linear 新方向

Linear 的數據：

- 超過 75% 的企業工作區已安裝 coding agent 整合
- 過去 3 個月，agent 完成的工作量成長 5 倍
- Agent 建立了近 25% 的新 issue

Linear 的目標從「issue tracker」轉向「context 與 agent 的共享執行系統」：整合客戶反饋、想法、策略方向、決策、程式碼，讓人與 agent 共同從 context 推進到產品。

## Theo 的熱觀點：工作拆分方式本身就要重新定義

傳統的 PM/工程師/設計師職能拆分，是基於人只能做一件事的限制。當 AI 足夠聰明，能同時扮演 CEO、Staff Engineer、QA Lead、Designer，這種拆分就失去意義。

Theo 的結論：未來的最佳計畫方式是「直接讓 AI 先做一個版本」，透過實際執行找出盲點和技術問題，再制定準確的後續計畫——不是事先規劃，而是以程式碼作為計畫本身。

## Codeex 的自動化功能

Theo 補充介紹了 Codeex app 的 automations 功能：讓非開發者也能設定定期觸發的自動化任務（例如每天蒐集媒體提及並傳送到 Slack）。他觀察到：使用 automations 最積極的反而是非開發者，因為開發者已習慣「評估是否值得自動化」的成本，而這個障礙對新使用者不存在。

## Jira 的終局

Jira 的開發商 Atlassian 近期收購了 The Browser Company。Theo 認為這是一個訊號：Jira 完全沒有在思考 AI 時代的轉型，而 Linear 已走在前面。
