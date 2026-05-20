---
title: ADLC：Agentic 開發生命週期七階段
created: 2026-05-20
updated: 2026-05-20
source: https://www.youtube.com/watch?v=aMBQB_IJ0dQ
published: 2026-05-18
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - ai-coding
  - agent-development
---

> [!info] 影片定位
> 解釋傳統 SDLC（Software Development Life Cycle）為何在 AI agent 時代失靈，並提出 ADLC（Agentic Development Life Cycle）作為新框架；逐一拆解七個階段的目標、與 SDLC 的差異、以及在每階段如何借助 planning mode 推進。

## SDLC 為何失效

- SDLC 假設「相同輸入 → 相同輸出」，過去靠這個確定性走過 design / development / testing / deployment / maintenance。
- AI agent 是非確定性系統：行為受 prompt、context、模型、外部工具影響，輸出無法 100% 預測。
- 把 agent 套進 SDLC 等於拿確定性的指標去衡量機率性的系統 → 必然失敗。ADLC 把軟體視為「持續學習的活系統」而非靜態交付物。

## 七階段總覽

| 階段 | 對應 SDLC | 重點產出 |
| --- | --- | --- |
| 1. Preparation & hypothesis | Planning | 工作流梳理、可驗證假設 |
| 2. Scope & problem identification | Analysis / feasibility | 邊界、KPI、人機責任模型 |
| 3. Design & architecture | Design | agent pattern、data flow、cost model |
| 4. Simulation & proof of value | （SDLC 無對應） | 原型、ground truth、ROI gate |
| 5. Implementation | Development | 程式 + prompts + 模型 + 工具 + MCP |
| 6. Testing | Testing | 持續評估：accuracy、hallucination、cost per outcome |
| 7. Deployment | Deployment | 受控啟用 + 持續觀察 |
| 維運 / 持續學習 | Maintenance | feedback loop、模型更新、安全護欄 |

## 階段 1：Preparation and hypothesis

- 不是規劃「程式怎麼寫」，而是規劃「agent 將要解決什麼」。
- 對齊 stakeholders，找出 workflow 斷裂點與重複性人力勞動 → 這才是 agent 要替換的對象。
- 形成「可驗證的假設」：哪段工作 agent 能協助／自動化、預期效益是什麼。
- 操作：開啟 planning mode，叫 agent 只規劃行為（behavior），不要碰 implementation；列出 user interaction、可能出錯點、隱性假設。
- 跳過後果：自動化錯誤工作，比沒做還糟。

## 階段 2：Scope and problem identification

- 拉清楚 agent 邊界與技術限制；事先定義 KPI（時間、成本、延遲、可行性）。
- 核心產出是 **human–agent responsibility model**：哪些決策由人擔、哪些可放手給 agent。
- 沒有這層責任地圖，出事時模型無法扛責，accountability 必然落回人類；事前明文化才能避免合規與信任問題。
- 操作：planning mode 規劃 workflow、latency、可能失效模式；輸出含 KPI 與責任分界的文件。

## 階段 3：Design and architecture

- 決定 agent pattern：ReAct、plan-and-act、multi-agent 等。
- 規劃 data flow：multi-agent 下尤其關鍵，資料錯一個 hop 整條鏈就壞。
- Cost model：token economics、context editing、compaction 策略；估算多用戶下的營運成本。
- 此階段也選定 model、orchestration framework、database 與其他依賴。
- 在寫 code 之前就定義「成功長什麼樣」→ 才能走 TDD（test-driven）。
- 同樣靠 planning mode 一次性產出 architecture / data flow / cost model 的完整 plan。

## 階段 4：Simulation and proof of value

- ADLC 特有，SDLC 沒有對應階段。
- 用真實資料測試先前所有假設；建 prototype 驗證高風險假設。
- 核心活動：
  - 準備 ground truth dataset（之後也會當 regression / fine-tuning 的資產）
  - 建 prototype 跑高風險假設
  - 量化 data quality、hallucination rate、accuracy、response quality
  - 重新檢視最初的 hypothesis 是否仍有 ROI
- 這階段是 **validation gate**：通過才往下走，否則砍掉重練。在原型階段砍比進 production 後砍便宜得多。

## 階段 5：Implementation

- ADLC 與 SDLC 的差異在這裡最明顯：
  - SDLC：邏輯落在 code、設定檔、第三方依賴。
  - ADLC：邏輯散落在 code、prompts、models、tools、external services；每一層都會改變行為。
- Multi-agent 編排可以用 Claude Code 新的 agents view：以單一 orchestration layer 統管多個 agent，比手動切多個 session 好管理。
- Tool 整合：建 personal assistant 就掛 Google Calendar MCP、Gmail MCP、Notion MCP 之類。
- **Context management 是 production 第一痛點**：即使 Gemini 1M / Opus 1M 等大 context 也要小心處理；無關 context 過多 → attention 分散 → 品質下滑（context rot）。
- 開發階段不能與驗證分離：每改一處要立即手動跑一遍對需求的 behavioral consistency check；agentic 系統小改動可能整條 workflow 偏掉。

## 階段 6：Testing

- 跟 SDLC 最大的差別：成功指標從「pass/fail」變成「分佈」。
  - SDLC：functional correctness，測試結果是布林值。
  - ADLC：accuracy distribution、hallucination rate、cost per outcome；無法塌成單一 pass/fail。
- 從「跑一遍既定 path」變成「持續評估推理 / 安全 / tool 使用」，因為同一個 agent 不會跑兩次同樣的路徑。
- 評估框架可用 Ragas、DeepEval 之類；最終判準仍是事先定義的 metrics。
- 測試類型：functional、non-functional、structural、load；常用 agentic 系統去找邊界案例。

## 階段 7：Deployment

- 部署不再是「軟體進入穩定運行」的終點，而是「主動監控與控制」的起點。
- 系統健康監控之外，更要監控 **behavioral metrics**；建立告警規則攔截品質 / 安全 / 效能異常。
- Roll-out 策略：先丟給小群真實用戶在真實情境下用，觀察一段時間再分批擴大；不一次性 GA。
- 部署的本質：受控啟動 + 持續觀察，與「實際使用者並肩運轉」的階段。

## 維運與持續學習

- 傳統系統的回饋迴路：使用者報 bug → 工程師改 → 結案。
- Agentic 系統的回饋迴路是持續、不間斷的：
  - UI 訊號（thumbs up/down、多輸出排序）餵回模型優化用，類似 ChatGPT / Claude 的回饋機制。
  - 定期更新資料源與 embeddings，避免資訊過時。
  - 持續監控 alignment 與安全護欄，對抗 prompt injection 等新型攻擊。
- 主要變數：cost management、quality tracking、product backlog、model upgrade，全部要持續維護。

## 核心啟示

- ADLC 不是 SDLC 的修補，而是承認 agent 系統的非確定性後的整體框架重組。
- Phase 4（Simulation）是新增的 ROI gate；Phase 7（Deployment）的語意被改寫成「監控起點」而非「開發終點」。
- Planning mode 在 1、2、3、5 都是主要工具，先規劃 behavior 再規劃 implementation。
