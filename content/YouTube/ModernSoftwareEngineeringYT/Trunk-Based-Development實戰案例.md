---
title: Trunk-Based Development 實戰案例：結果令人震驚
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-12-10
source: https://www.youtube.com/watch?v=CR3LP2n2dWw
---

## 案例背景：MFT Energy

- 公司：MFT Energy（能源交易）
- 團隊：新團隊、新領域（電力交易競標整合服務）
- 限制：緊迫截止日期、混合經驗水準、幾乎沒有 TDD 或單元測試經驗
- 規模：約 2,500 次 commit，90% 少於 200 行

做法稱為 **MAD TBD（Main as Default Trunk-Based Development）**：直接 commit 到 main，pipeline 自動 build、跑單元測試、部署到測試環境、跑驗收測試，全過通即可部署到 production。

## 事前疑慮 vs 實際結果

開始前的擔憂：main 會一直壞掉、無法部署、feature toggle 很痛苦、沒有 PR 品質會下降、開發者不夠負責任。

**問卷結果（專案結束後調查）：**
- 「main 常常壞掉無法 build」→ **全員強烈不同意**
- 「main 持續處於可部署狀態」→ **平均 9/10**
- 「服務整體品質良好」→ **8.5/10**
- DORA metrics 主觀評分極佳：低 change lead time、高部署頻率、低 change failure rate、低 MTTR
- 整體 TBD 評分 **7.6/10**，net promoter score **+33**
- 「未來專案是否繼續用 TBD」→ **8.5/10**

## 成功的三個工程原則

**1. 小批量降低風險**
- 小 commit → 少未知數 → 每個改動更容易推理、出問題更容易修
- 每個 DORA 報告自 2014 年以來都驗證了這一點

**2. 快速回饋強化系統**
- 使用 feature toggle、dark launch、增量 DB 改動、mock data、parallel verification
- 快速在真實環境驗證每個小改動

**3. 低交易成本鼓勵良好行為（Coase 交易成本原則）**
- 阻塞式 PR、長 feature branch、繁重 QA → 慢 → 大批量 → 更多問題
- 保持改動成本低 → 改動保持小、安全、可觀測、可回復

## 非同步 Code Review 的失敗

相比之下，non-blocking review 的結果差：**平均 6/10，net promoter score -7**。

失敗原因：
- 「non-blocking」被理解為「non-urgent」，review 常常太晚，回饋已過時
- 很多人投票用腳，根本不參與
- 最根本問題：**沒有人知道 code review 的目的是什麼**——安全性？bug？合規？知識分享？部署安全？
- Dave 的觀點：這不是工具問題，是目的不明確的問題

## 結論與經驗

- TBD 不是魯莽，是把每個改動設計成小、安全、可觀測、可回復
- 「持續可部署的 main」是良好工程的結果，不是繁重流程的產物
- **不需要完整的單元測試覆蓋才能開始 TBD**；TDD 和 pair programming 是加分，不是前提
- 開始 TBD 需要的：小批量組織工作、feature toggle、安全增量設計、快速回饋、可觀測性
- 最容易的起點：全新 greenfield 專案，但既有專案不需要數月準備
