---
title: AI Agent
created: 2026-04-21
updated: 2026-04-21
tags:
  - ai-agent
  - moc
---

涵蓋 AI Agent 產品開發的架構基石、交付方法論、實戰案例、術語入門。聚焦「為客戶或使用者建構通用 AI Agent 產品」的完整路徑，從底層原理到商業交付。

> 本 MOC 基於 2025–2026 年實踐整理，具體工具選型與生態（Mem0、Docling、Langfuse 等）迭代迅速，請以原始影片日期與官方 repo 為最新依據。

## 與 Agent-Harness 的分工

本 MOC 與 [[Agent-Harness]] 是**產品層**與**工具層**的互補：

| 面向 | 本 MOC（AI Agent） | [[Agent-Harness]] |
|------|--------------------|-------------------|
| 對象 | 為客戶/終端使用者建構的 AI 產品 | 你用來寫程式的 coding agent（Claude Code 等）|
| 關注 | 架構基石、交付流程、商業模式 | runtime 協作拓撲、evaluator、context 管理 |
| 代表問題 | 「如何做一個可靠的文件處理 Agent 賣給客戶？」 | 「如何讓 Claude Code 跑一晚不壞？」|

兩個主題有少量交集（記憶、評估、tool-calling 設計），但切入角度不同——本 MOC 討論產品設計，Agent-Harness 討論開發工作流。

## 一、架構基石

Agent 產品的底層建構積木。這層抓穩了，換框架、換模型都不會翻。

### 核心原則：Workflow 優於 Agent

Anthropic 對 Workflow / Agent 的官方定義：

- **Workflow**：LLM 與工具透過**預定義程式碼路徑**協作 → 可預測、易除錯
- **Agent**：LLM **動態指揮**自己的流程 → 靈活但難控制

**行動準則**：先嘗試用 Workflow 解決，只在必要時才引入 Agent 模式。大部分企業用例（文件處理、客服路由、內容生成）用 Workflow 模式就夠。

包含五種 Workflow 模式：Prompt Chaining、Routing、Parallelization、Orchestrator-Worker、Evaluator-Optimizer。

### 七大建構積木

Agent 系統拆解後的最小原子：

| # | Building Block | 作用 |
|---|----------------|------|
| 1 | Intelligence Layer | LLM API 呼叫，唯一真正的「AI」元件 |
| 2 | Memory | 傳遞對話歷史（LLM 本質 stateless）|
| 3 | Tools | 讓 LLM 呼叫外部函式、查資料 |
| 4 | Validation | Pydantic + structured output 確保可預測 |
| 5 | Control | 用 deterministic 程式碼路由，別全交給 LLM |
| 6 | Recovery | try/except + retry + fallback |
| 7 | Feedback | Human-in-the-Loop 暫停點 |

**心態**：能用 deterministic 程式碼解決的，不要呼叫 LLM。只在確實需要語意理解時才引入 API 呼叫。

### 長期記憶系統（Mem0）

承上 Block 2 的「Memory」，在跨 session 層面需外掛長期記憶。兩種層次：

- **短期記憶**：對話歷史，每次呼叫手動傳入
- **長期記憶**：跨 session 的事實、偏好，需持久化

以 Mem0 框架為代表，採兩階段 pipeline：
1. **摘要萃取**：LLM 從對話中萃取事實
2. **動態決策**：另一個 LLM 判斷 add / update / delete

**實務建議**：Mem0 等框架適合快速原型，生產環境考慮自行實作核心邏輯避免抽象層過厚。

### Human-in-the-Loop（HITL）

LLM 無法達到 100% 可靠時的安全閥。

**兩種實作模式**：
- **Router 方式**：結構化輸出 + Pydantic validator 決定何時需確認
- **Tool Calling 方式**：while 迴圈攔截特定工具呼叫

**生產架構關鍵**：
- **Deferred Execution**：需確認時儲存狀態，**不要**在等待期間保持連線
- **State Serialization**：持久化完整 context（訊息、待辦動作、工具參數）
- **Stateless Resume**：每次恢復從儲存載入，不依賴記憶體

### 知識系統（RAG Pipeline）

Agent 要用企業內部知識時的資料準備流程：**提取 → 分塊 → 嵌入 → 檢索 → 應用**。

以 Docling + LanceDB 為例的完整 pipeline：
- **Docling**（IBM 開源）：PDF/DOCX/網頁統一轉 Markdown，表格提取品質最佳
- **HybridChunker**：同時處理階層式分塊與 token 上限
- **LanceDB / pgvector**：前者適合原型，後者適合生產

## 二、交付方法論

2 人團隊完成 50+ B2B AI 專案的實戰流程。

### Discovery（用例選擇）

核心問題：**ROI 在哪裡？** 建構客製化 AI 軟體成本不低。

**優先原則**：快贏優於大夢想。大部分組織有大量低垂果實被忽略，而專注在複雜大問題。

**紅旗警示**（要避免接的案）：
- 「因為大家都在用 AI」→ 無明確 ROI
- 沒有清晰成功標準
- 客戶期望 Day 1 完美
- 資料存取/安全性未解決

### 準確率管理

LLM 不是確定性軟體，需教育客戶**迭代式開發**：

| 階段 | 預期準確率 |
|------|-----------|
| V1 交付 | 70–80% |
| 迭代後 | ~90% |
| 完美 | 通常不切實際 |

**框架轉變**：從「一次完美」改為「快速交付 → 建立回饋 → 持續改進」。

### PoC vs MVP

| 類型 | 定義 | 交付物 |
|------|------|--------|
| PoC | 驗證是否能達標 | 本地 Demo + 報告 |
| MVP | 已知可行，建最小可用版本 | 可部署系統 |

### Sprint 結構與定價

**2 週 Sprint 模型**：

```
Day 1–2：架構與鷹架
Day 3–8：核心開發
Day 9–14：測試、打磨、Demo
```

**現實中的 Sprint 間隔**：客戶在 Sprint 之間常「消失」2–8 週進行內部評估 → 多專案交錯管線避免現金流壓力。

### 標準化技術棧

Fork 專屬 Launchpad 專案起手，每新專案都從同一套基礎開始：
- **後端**：FastAPI + Celery + Redis + PostgreSQL（自架 Supabase）
- **LLM**：Azure OpenAI（客戶資料合規驅動）
- **LLM 整合**：Pydantic AI + Langfuse trace + Sentry
- **前端**：Next.js
- **部署**：Docker Compose + CI/CD + Hetzner VM（比 AWS/Azure 便宜 10×）

### 商業模式

**定價策略**：AI 讓生產力 5–10×，但**維持同樣定價、用速度換更多專案量與更高品質**，而非降價。

**長期收入**：
- 維護費（軟體永遠不完整）
- API 費用分成
- 新專案透過信任建立而來

## 三、實戰案例

### End-to-End GenAI 專案

**AI 新聞聚合器**：每日 email 聚合 AI 新聞，包含：
- **資料來源**：YouTube Transcript API、RSS feeds
- **Pipeline**：Scraper → DB → Digest Agent → Aggregator Agent → Email Agent
- **架構重構**：三個 scraper 共用邏輯 → BaseScraper 基類
- **踩坑**：重量級依賴（OCR model）超出記憶體限制，換輕量替代品

**心得**：先讓系統跑起來看具體結果，再逐步完善；不要從資料庫模型開始，先建 scraper。

### AI 作業系統架構

**AI 作業系統（Jensen Huang 框架）**：借用「電腦作業系統」比喻的三層 Agent 系統：

| 層 | 觸發方式 | 代表場景 |
|----|---------|---------|
| 第一層 | Webhook / API | WhatsApp 訊息觸發自動回覆 |
| 第二層 | Cron / Scheduled | 每週競爭對手分析 |
| 第三層 | 使用者對話 | WhatsApp agent 動態委派任務 |

**關鍵概念**：Context Hub 階層式載入（`abstract.md` → `overview.md` → 完整檔案），讓 agent 按需深入，避免 context 爆炸。

**Soul 檔案**（靈感來自 Open Claw 的 `soul.md`）：深度描述個人/組織的價值觀與做事方式，放在 system prompt 最前面提升對話品質。

## 四、術語入門

給決策者、投資者、新手的速查卡：

| 術語 | 一句話解釋 |
|------|-----------|
| AI Agents | LLM 在環境中循環執行、獲得反饋，直到達成停止條件 |
| Vector Databases | 依語義組織的知識庫，等於給 AI 長期記憶 |
| RAG | 開卷考試——檢索相關段落 + LLM 組織答案 |
| MCP | LLM 與外部工具的標準介面（萬能遙控器） |
| Context Engineering | 決定 context window 放什麼、不放什麼 |
| Fine-tuning | 用自訂資料集繼續訓練，調整模型行為 |
| Guardrails | 輸入/輸出的安全與品質檢查 |

## 常見陷阱

**徵兆：Demo 好用但上線失敗**
- 原因：沒從一開始建評估系統，規模化後 RAG 維護崩潰
- 解法：Day 1 就建 LLM Evals，並接入 Langfuse 追蹤

**徵兆：Scope Creep 吃掉 Sprint**
- 原因：需求邊界模糊，客戶追加
- 解法：提案明確列 must-have / nice-to-have / exclusions

**徵兆：Agent 在生產環境跑崩**
- 原因：沒有 Recovery 與 HITL 機制
- 解法：try/except + retry + Deferred Execution + 通知服務

**徵兆：Context 在長任務中爆炸**
- 原因：一次載入太多資料或所有對話歷史
- 解法：Context Hub 階層式載入 + 每輪 retrieve 相關記憶

## 相關主題

- [[Agent-Harness]] — Coding agent 的 runtime 架構（工具層，本 MOC 為產品層）
- [[Context-Engineering]] — 單次 prompt 的 context 組裝（token 層）
- [[Claude-Code-Skills]] — Skill 機制作為 Agent 能力擴充

## 延伸來源

**官方 / 部落格**

- [Anthropic: Building effective agents](https://www.anthropic.com/research/building-effective-agents)（Workflow vs Agent 原始定義）
- [Mem0 GitHub](https://github.com/mem0ai/mem0)（開源記憶框架）
- [Docling GitHub](https://github.com/DS4SD/docling)（IBM 文件提取）

**影片**

- [建構可靠 AI Agent 的 7 大基石（daveebbelaar）](https://www.youtube.com/watch?v=T1Lowy1mnEg)
- [建構有效 AI Agent 實用技巧（daveebbelaar）](https://www.youtube.com/watch?v=tx5OapbK-8A)
- [Human-in-the-Loop 實作指南（daveebbelaar）](https://www.youtube.com/watch?v=7GOxUgVTz3s)
- [Mem0 長期記憶實作（daveebbelaar）](https://www.youtube.com/watch?v=ynhl8KjjS3Y)
- [開源文件提取 Pipeline（daveebbelaar）](https://www.youtube.com/watch?v=9lBTS5dM27c)
- [End-to-End GenAI 專案實戰（daveebbelaar）](https://www.youtube.com/watch?v=E8zpgNPx8jE)
- [如何建構並交付 AI 客製化解決方案（daveebbelaar）](https://www.youtube.com/watch?v=Q679gH7oszg)
- [自建 AI 作業系統全架構解析（daveebbelaar）](https://www.youtube.com/watch?v=rZX1OYetbSM)
- [投資 AI 前必懂的 7 個術語（daveebbelaar）](https://www.youtube.com/watch?v=hKC_pI_yhZc)
