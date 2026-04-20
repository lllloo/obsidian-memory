---
title: GStack 規劃管線省下數週開發時間
created: 2026-04-20
updated: 2026-04-20
published: 2026-04-17
source: https://www.youtube.com/watch?v=6kM27uGP4n4
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - gstack
  - agent
  - planning
---

Y Combinator CEO Gary Tan 推出的 Claude Code toolkit **G-Stack** 最被低估的是 planning pipeline。影片實際在一個有付費用戶的 SaaS 專案（bookzero.ai）上，用 G-Stack 規劃一個新功能（AI Chat Agent 查詢支出），全程不寫一行程式碼，用 CEO、設計、工程、QA、Devil's Advocate 五種角色審核設計稿。

## 整體管線結構

規劃管線共 3 個 skill，依序執行，各自在獨立的 Claude Code session 跑以保持乾淨的 context window：

1. **Office Hours Skill** — 定義問題與收斂 MVP
2. **Spec Team Skill** — 細化技術決策
3. **Auto Plan Skill** — 多 persona 平行審查

影片示範的新功能：讓付費用戶用自然語言查詢自己在 bookzero.ai 上的支出資料（例：「Q1 我花多少在加油」、「這個月金額前五」、「所有超過 100 美元的收據」），AI 會將其轉為 SQL 查詢資料庫並回傳結果。

## 安裝

- 把 G-Stack 的安裝指令貼到 Claude Code 讓它安裝到專案
- 或複製 repo URL、請 Claude follow 該 repo 完成安裝

## Office Hours Skill（定義問題）

把 Jira ticket URL 給 Claude（搭配 Jira MCP），並說明要跑 planning pipeline。Claude 會：

1. 啟動多個 sub-agent 理解目前 codebase、data model、service
2. 問框架設定問題：是否可以複製其他專案的 coding pattern、專案階段（ideation / 有付費用戶 / hackathon）
3. 根據專案階段（有付費用戶）的情境，追問：
   - 這週就能交給付費用戶用的最小版本是什麼
   - 是否有實際觀察用戶行為的資料
   - 用戶目前實際做了哪些設計者沒預期到的事
4. 做市場研究（AI conversational expense management 領域）
5. **Phase 3 — 挑戰前提**：把前面收斂到的 6 個 premise 條列，逐條要求確認
6. **Phase 3.5 — Cross Model Second Opinion**：啟動一個沒看過對話歷史的獨立 sub-agent，只看 problem statement、key answers、premise、landscape 給第二意見
7. **Phase 4 — Alternative Generation**：提出多種技術方案並評估
8. 產出 design doc 存在根目錄 `.md`

### MVP 收斂過程

初始 prompt 列出 5 個功能（spending analysis、chart visualization、save queries、dashboard customization、credit-based monetization），Claude 直接 push back：

> 這不是 wedge，這是 platform。

要求挑出最能製造 word of mouth 的一個功能，其他放 phase 2。最後收斂到：

- 只做 **spending analysis 與 unusual spending detection**
- 表格呈現，**不做 chart、不做 saved queries、不做 dashboard customization**
- credit-based pricing（每次對話扣點）
- AI 只查詢已存在資料，不生成財務紀錄
- 目標回應時間 < 5 秒

### Phase 4 的技術方案比較

| 方案 | 做法 | 風險 |
|------|------|------|
| A. Structured Query Mapper | LLM 把自然語言轉成 JSON intent，對應到既有 query | 低；零 SQL injection |
| B. Direct SQL Generation | LLM 對 read-only view 直接產生 parameterized SQL | 中高；需要 read-only view、有 SQL injection 風險 |
| Hybrid | Mapper 為主、SQL fallback | 結合兩者 |

推薦選 A，可覆蓋 90% 查詢，其餘 10% 以後再處理，屬於 boiled lake principle（先煮一部分）。

### 輸出結果

- Design doc 過了兩輪 adversarial review
- 修正 15 個問題，品質評分 8/10
- 給出下一個 session 的 handoff prompt，可用乾淨 context 繼續

## Spec Team Skill（細化規格）

用新的 Claude session 觸發 Spec Team skill 並指向前一階段產出的 design doc。Claude 會問：

- **Chat UI 擺放**：dedicated page / slide-out panel / floating widget → 選 dedicated page
- **Conversation context 長度**：5 / 10 / session only / single query → 選 5（支援「幫我按 vendor 再分一次」這類後續問題）
- **資料 aggregation 方式**：Postgres RPC / JavaScript 聚合 → 選擇透過 ORM（Supabase client）放在 backend service layer，之後切換資料庫較不需 migration
- **Table UI**：inline markdown、限制筆數、預設收合、長對話自動收合、過多記錄時先追問澄清
- **Credits 計費**、**Edge case**（空資料引導匯入、模糊查詢要求澄清、跨幣別分開顯示、rate limit）

## Auto Plan Skill（多 persona 平行審查）

指向 spec 檔啟動 Auto Plan skill，Claude 會依序啟動 sub-agent 以不同角色審查：

- CEO
- Design review
- Engineering review
- DX review
- Devil's Advocate

### 結果

- 共 41 findings（CEO 10、Design 15、Engineering 16）
- 22 個決策自動下定
- 若干標記需要使用者決策的項目會停下等回覆

## Token 消耗

| 階段 | 消耗 |
|------|------|
| Office Hours | 170k |
| Spec Team | 200k |
| Auto Plan | 200k |
| **合計** | **~600k** |

在 brownfield 專案上規劃一個新功能的成本。

## 執行階段

規劃完成後，可接：

- G-Stack 自己的 build pipeline
- GSD 或 Superpowers 來執行 spec（作者提過 Superpowers 有 test-driven 元素是 G-Stack 較弱的部分，所以 build 階段他傾向換框架）

## 關鍵 takeaway

- G-Stack 的 planning pipeline 強在讓 Claude **主動 push back**，把大 idea 收斂成 MVP
- Cross model second opinion 能抓到同一個 session 會錯過的盲點
- 分階段換 session 保持 context 乾淨，每階段輸出一個 handoff prompt
- 最強烈的訊號是「用戶在匯出 CSV 自己分析」這件事，代表這個 feature 有真實需求
