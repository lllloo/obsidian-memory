---
title: Claude Code Agentic OS 勢不可擋
created: 2026-04-23
updated: 2026-04-23
source: https://www.youtube.com/watch?v=pfPi04pIfaw
published: 2026-04-22
parent: "[[01.index]]"
tags:
  - youtube
---

## 核心問題：三大 Gap

一個有用的 Claude Code Agentic OS 必須同時解決三個使用者普遍遇到的落差：

- **Memory Gap（記憶）**：Claude Code 預設不記得過往對話
- **Consistency Gap（一致性）**：同樣任務每次做法／結果不一致
- **Access Gap（存取）**：Terminal 介面對非技術成員而言幾乎是黑箱

Agentic OS 的目標：讓 Claude Code 成為「車子的引擎」，周圍配齊記憶、一致性、可由任何人駕駛的介面。

## 整體架構（Org Chart 思維）

把 Claude Code 當作中樞，像組織圖一樣展開：

- **Engine**：Claude Code
- **Memory**：Obsidian Vault
- **日常生產力**：Google Workspace（透過 GWS CLI）
- **功能分支（branch）**：Research / Content / Sales / Marketing / Admin… 依個人或公司業務切
- **每個 branch 底下**：對應的 Skills（處理該領域的具體任務）
- **最外層**：Automations（何時／何地執行）+ Dashboard（非技術成員的入口）

重點不是照抄這個結構，而是用「業務組織圖」的心智模型去拆解自己的工作流。

## Memory：Obsidian 就夠了

- **不需要**完整的 agentic RAG（LightRAG、Supabase、Pinecone 等），對大多數人都過度工程化
- Obsidian 的 raw / wiki / projects 三層資料夾結構已足夠
- 好處：免費、完全可客製、本質上就是資料夾

## Consistency：Skills + Automations

### Skills 的建立邏輯

Skills 必須反映**實際的日常工作流**，而不是憑空設計：

1. 拆解每日任務（研究在哪做？怎麼做？研究完送去哪？）
2. 一個任務 = 一個 Skill，必要時拆子 Skill
3. **用 skill-creator skill 建立 skill**，讓 title / description / trigger 自動最佳化，並可量化測試
4. 每個 domain 重複上述流程
5. Skills 非定稿，持續更新調整

### Automations：Local vs Remote

建立 Skill 後判斷是否需要自動化，並選擇部署位置：

| 類型       | 條件                                                     | 範例                                           |
| ---------- | -------------------------------------------------------- | ---------------------------------------------- |
| **Local**  | 需要存取本機檔案、資料夾或本機 CLI（如 NotebookLM CLI） | Deep research 工作流（NotebookLM + Firecrawl） |
| **Remote** | 純用 Claude Code 原生工具、不觸碰本機                    | 每日 GitHub trending 報告 → 推到 GitHub repo  |

- Remote 任務優勢：電腦關機也會跑；可走 Claude Code 的 scheduled tasks 直接排程
- 這也是 Mac Mini 或 VPS 成為主流的原因：常開的機器能長時間執行 local automation

## Access：Dashboard（Command Center）

- 把所有 Skills 與 Automations 包成 dashboard 上的按鈕
- 背後是 Claude Code headless 模式執行（等於背景開著一個不可見的 terminal）
- 介面可同時呈現：最近 vault 變動、即將執行的 routines、最近執行結果、用量視窗
- 非技術成員或客戶不需打開 terminal 就能使用 90% 的 Claude Code 能力

### 商業價值

對 AI agency 或賣 AI 導入的團隊特別關鍵：

- Terminal 對大多數人等同魔法黑盒
- 用 org chart 呈現「Claude Code 有記憶、能處理 sales/marketing/admin、你只要點按鈕」後，客戶才能理解價值
- Packaging（Research Pack、Content Pack、Marketing Pack）本身就是強力 value play

## 進階使用者的價值

若已重度使用 Terminal，Dashboard 對自己而言價值有限（直接下 `/` 或自然語言呼叫 skill 即可）。但：

- 很多自稱不需要的人其實沒真正拆解過日常工作流
- Dashboard 仍可作為「所有輸出的單一入口」，比分散在 Obsidian 子資料夾更集中
- 框架本身是給團隊成員、客戶用的——你不是 ICP

## 心智模型重點

- Claude Code 夠聰明可以自己搞清楚結構，但**人類需要這個 org chart 才有辦法改進系統**
- 沒有唯一正確解；優化方向永遠是「對你自己有效」
- Skills 不是一次寫死，是持續更新；automation 不是必備，看任務屬性決定
