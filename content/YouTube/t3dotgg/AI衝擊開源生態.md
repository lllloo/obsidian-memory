---
title: AI 衝擊開源生態
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-13
source: https://www.youtube.com/watch?v=l8pQeVVaqpY
---

## AI 對開源的三大衝擊

- AI 生成 PR 氾濫：T3 Code 開源 5 天已有 150 個 PR，即使明確聲明不接受貢獻仍擋不住
- 用戶素質下降：非工程師用 AI 開始發問，問題充斥技術術語但邏輯錯誤，甚至出現「React 已死所以不需要 React」的荒謬留言
- 資金來源縮水：Tailwind、課程銷售等傳統變現模式被 AI 直接取代

## PR 氾濫的深層問題

- AI PR 讓 codebase 理解度快速下滑——每合併一個自己不完全理解的 PR，掌控度就下降一點
- 惡意攻擊變容易：只需幾個 sock puppet 帳號、一個 agent 腳本，就能讓任何開源維護者崩潰，XZ backdoor 事件是前車之鑒
- GitHub 幾乎沒有提供任何有效工具；Twitch 的 Mod View 由 4 人在 7 個月內做出比 GitHub 更好的管理系統

## 現有解決方案

**Vouch（Mitchell Hashimoto 製作）**
- GitHub Actions workflow，維護者事先建立受信任貢獻者名單（`vouch.md`）
- 未被 vouch 的 PR 自動標記，可一鍵篩選出可信 PR
- T3 Code 用此工具將 150 個 PR 篩到 43 個

**PR Stats（Ree 製作）**
- 顯示貢獻者歷史 PR 合併率、貢獻紀錄
- 缺點：新貢獻者容易被排除，也可偽造

**Anti-slop**
- 掃描 PR 判斷是否為 AI slop
- 問題：判斷本身也要用 AI，成本可能快速升高

## 維護者能做的事

- 推動公司加入 **Open Source Pledge**：每位工程師每年 $2,000 捐給開源維護者
- 主動整理 issue（確認是否已修復、轉發給對應 PR）
- 感謝維護者——不是制式訊息，而是真誠反饋他們的具體工作

## 優質 PR 特徵

- 1-5 行改動，清楚說明原因
- 連結對應 issue
- 不搶先標記無關人員

## 核心警告

> 開源維護者已在瀕臨放棄的邊緣。AI 讓攻擊更容易、資金更少、垃圾 PR 更多。如果不積極保護這個生態，整個軟體業都會受害。
