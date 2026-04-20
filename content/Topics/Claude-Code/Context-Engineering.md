---
title: Context Engineering 與成本優化
created: 2026-04-20
updated: 2026-04-20
tags:
  - claude-code
  - ai-agent
  - context-engineering
  - memory
---

> AI Agent 在 demo 表現優異但在生產環境失敗，大多數情況不是模型能力不足，而是 **context engineering 做得不夠好**。本 MOC 整合六篇影片摘要，涵蓋 Context Rot 現象、架構層與 session 層的優化策略、以及用量管理的實戰技巧。

## 為什麼 Context 是 Agent 的核心

Anthropic 對 Context Engineering 的定義：**在 LLM 推理過程中，策略性地篩選與維護最佳 token 集合的一套策略。**

**Context 的範疇**：

- System prompt（系統提示）
- Message history（對話歷史）
- Tool descriptions & outputs（工具定義與輸出）
- Documents / RAG chunks（文件與擷取的知識）
- Memory files（記憶體檔案）
- Intermediate reasoning（中間推理）
- Environment feedback（環境回饋）

**核心目標**：找到能最大化目標輸出機率的**最小高訊號 token 集合**。

## Context Rot：現象、研究與突破

### 傳統現象（Chroma 研究）

- 所有模型在超過 100K tokens 後出現斷崖式效能下滑
- 舊操作準則：到 100K–120K tokens 必須 `/clear`，否則輸出品質顯著下降

### 世代演進：從「斷崖」到「緩降」

LLM 世代更迭下，長 context 效能呈現兩階段變化：

- **舊世代**：超過特定 token 數（常見 100K 附近）後效能斷崖下滑，長 context 窗口只是「名義容量」
- **新世代**：context 容量擴大（可達百萬級），且效能退化曲線從「斷崖」變「緩降」，長 context 從假命題轉為真正可用

但退化仍在，不會消失。真正的技術進步不是「context 變大」，而是「大 context 下仍可用」。

### 操作準則

- 每堆積一段 context 就有小幅效能損耗（經驗法則：每 100K tokens 約 2%，因模型而異）
- **如果可以清，就清**（從 0 開始永遠優於從 700K 開始）
- **如果需要延續**，新世代模型下可放心維持長對話，不必做 hacky 的 context 管理
- 留意自家 plan 是否啟用長 context 支援，以及是否有 long-context surcharge

## 策略一：架構層 — 檔案系統取代 Context

### 核心思想：萬物皆檔案

Vercel 工程師提出：**最佳架構不是複雜 pipeline，而是 Unix 哲學的檔案系統**。模型在大量程式碼與目錄結構上訓練，使用 `grep`、`ls`、`find` 是它本來就擅長的事。

**工作流程**：

1. 用 `ls` / `find` 瀏覽檔案系統
2. 找到確切檔案後，用 `grep` / `cat` 進行模式比對
3. 只有小塊相關資訊送進模型，其餘保留在 context window 之外

### 三種資訊提供方式比較

| 方式 | 優點 | 缺點 |
|------|------|------|
| 詳細 system prompt | 簡單直接 | Token 上限限制資訊量 |
| 向量資料庫（RAG） | 處理大量資料 | 語義相似而非精確比對，依賴模型從 chunks 提取 |
| **檔案系統** | 結構映射領域關係、精確比對、context 最小化 | 不適合模糊查詢 |

**使用時機**：

- **檔案系統**：資料高度結構化、查詢意圖明確
- **RAG**：需要比對詞語含義、查詢較模糊或非結構化

### `.agent/` 文件系統架構

AIJasonZ 的實務作法，宣稱效能提升 10 倍：

```
.agent/
  readme.md          # 所有文件的索引
  task/              # 每個功能的 PRD / 實作計畫
  system/            # 專案架構、DB schema、API 文件
  sops/              # 標準操作程序
```

- **task/**：plan mode 產生的實作計畫存檔，後續類似功能可引用
- **system/**：跨功能全域架構文件，隨 codebase 成長持續更新
- **sops/**：記錄標準流程，agent 犯錯後生成 SOP 避免重複
- **readme.md**：所有文件的導覽索引，agent 初始化時先讀

**`/update-doc` 指令設計**：

- `/update-doc initialize` → 掃描 codebase 建立初始架構
- 實作功能後 → 更新相關文件、SOP
- agent 犯錯修正後 → 生成 SOP、更新 readme

## 策略二：記憶體管理 — Git Context Controller

針對長時間任務中 agent 「越來越笨」、重複犯錯、Claude Code MEMORY.md 僅單 session 有效的問題。

### GCC 方法（學術論文 + 社群實作）

**原始論文**：*Git Context Controller: Manage the Context of LLM-based Agents like Git* — arXiv:2508.00031（Oxford）

論文核心觀點：把 agent context 從 transient token stream 升級為 persistent, navigable memory workspace，具備 COMMIT / BRANCH / MERGE / CONTEXT 明確操作。

讓 agent 像用 git 管理代碼一樣管理記憶體：

```
project/
  main.md          # 全域 roadmap 與專案脈絡
  branches/
    <approach>/
      commit.md    # 里程碑摘要（類似 git commit log）
      log.md       # 完整對話歷史
      metadata.md  # 高層次元資料，方便搜尋
```

**四個操作**：

- **branch**：決定探索新方向時建立（如 `playwright`、`api`）
- **commit**：完成子任務或里程碑時更新
- **merge**：探索完成後將 branch 記憶合併回 `main.md`
- **search**：根據查詢搜尋特定 session 或 turn

**效果**（論文數據）：

- SWE-Bench Verified 上任務解決率相對強 long-context baseline 提升超過 13%
- Resolution rate 48%，在所測 26 個系統中最高
- 讓較小型模型達到 frontier model 等級

### 與 Claude Code 自有記憶的差異

| | Claude Code MEMORY.md | Git Context Controller |
|---|---|---|
| 跨 session | 有限 | 是 |
| 跨 agent | 否 | 是 |
| 可分享 | 否 | 可產生分享 URL |
| 複雜度 | 單一檔案易膨脹 | 分層結構 |

**實作變體**：

- **one-context**（影片中示範）：`npm i -g one-context-ai` → `one-context` 啟動左右分割介面，含 stop hook 自動儲存、跨 session/agent 記憶共享
- **Contexa**（<https://github.com/swadhinbiswas/contexa>）：論文官方實作，支援 Python / TypeScript / Rust / Go 等 7 種語言，共用 `.GCC/` on-disk 格式（Markdown + YAML）

## 策略三：System Prompt 與提示工程

### 常見陷阱

1. **太模糊**：初始版本只有基本指令，使用者回饋後堆積限制
2. **太具體**：大量 if/else 式語句，例如「不要這樣說」、「如果使用者說 X 就回 Y」

### 正確做法

- 讓 prompt **足夠具體但保留創意空間**
- 遇到需要大量規則時**拆分問題**：加 router 先分流，再用更小 prompt 處理各子問題
- 使用結構化格式（XML 或 Markdown）：
  ```
  ## Background
  ## Instructions
  ## Tool Guidance
  ## Output Format
  ```

### 常見工程錯誤

**使用負面範例而非正面範例**：LLM 不擅長處理負面指令。改為「要做什麼」、提供正面 few-shot examples。

**不看資料與 trace**：從第一天接入追蹤工具（如 Langfuse），可視化 system prompt、訊息歷史、工具呼叫。大多數 LLM 行為異常，看完整 trace 幾乎立刻發現問題。

**混淆 Workflow 與 Agent**：

- **Workflow (DAG)**：確定性強、可測試，適合後端自動化、客戶服務
- **Agent (LLM + 工具迴圈)**：彈性強，適合有人在回路的聊天介面

不要因為「agent」這個詞流行就對每個問題都用 agent 方案。

### 各類 Context 的管理策略

| Context 類型 | 策略 |
|--------------|------|
| 文件 | 使用 RAG：先廣撈 50 chunks，再用 reranker 取最相關 8 個 |
| 工具 | 描述簡短、聚焦、不重疊；數量多時拆 sub-agent |
| 記憶體與對話歷史 | Pruning / Summarization / State Machine |

### 動態 System Prompt 注入（State Machine）

多階段 agent 不要把所有階段規則塞進一個大 system prompt：

1. 資料庫記錄使用者目前階段（state）
2. 每次訊息從資料庫拉取對應 context
3. 根據 state 動態組合 system prompt

優點：每階段的 prompt 更小更聚焦，不互相干擾。

## Session 層級操作技巧

### 清空 context

- **`/clear`**：任務完成後直接重置，下個任務從乾淨 context 開始
- **`/compact`**：保留必要資訊並壓縮（適合想延續部分脈絡）
- **`/btw`**（by the way）：問旁支問題，回應不帶入主 context
- **`/rewind`**（或雙擊 Escape）：回到 Claude 沒按指示的那則訊息之前，錯誤輸出不進入 context

### 規劃優先

前期花 token 規劃，遠比後期花更多 token 修正划算。

### 移除不常用的 MCP

可釋放 2%+ context。`/context` 指令可查看 token 消耗分佈。

### Sub-agent 隔離

將研究步驟隔離到獨立 thread，只回傳摘要給主 thread。

## 設定層級優化

### 模型與推理深度

| 任務難度 | 模型 | 備註 |
|---------|------|------|
| 簡單 | Haiku | 成本最低 |
| 中等 | Sonnet | 平衡 |
| 複雜 | Opus | 消耗最高（約 Sonnet 的 3 倍 token） |

**Effort 設定**：預設 `auto`；非複雜任務手動設為 `low`。

**停用思考模式（disable thinking）**：與 effort 不同，完全關閉內部推理步驟，適合不需深度推理的任務。

### CLAUDE.md 精簡原則

- 建議控制在 **300 行以內**
- 不要放 Claude 本來就知道的事（dev server 啟動、專案結構解說）
- 只放：不該做的事、開發慣例、Claude 預設不知道的規範

**文件拆分策略**：特定區域（DB schema、API 規範）拆獨立文件，在 CLAUDE.md 連結，Claude 用到才載入。

**Path-specific rules**：不同路徑設不同規則，只載入當前任務相關。

### `.claude` 資料夾設定

```
disablePromptCaching: false   # 啟用快取，減少重複 prefix 費用
autoMemory: false             # 停用背景記憶分析
disableBackgroundTask: true   # 停用 dream、memory refactor、indexing
```

### Hooks 與 skills

- **Hooks 過濾輸出**：例如讓測試結果只注入失敗的測試，略過通過的測試
- **Skills**：重複工作流程封裝為 skill，搭配腳本執行確定性任務，避免把可程式化的工作浪費在 Claude token 上

### 其他旗標

- **`--append-system-prompt`**：一次性指令用此帶入，session 結束後消失，不永久佔 context
- **max output tokens**：無預設值，可手動設上限；不需長輸出的任務設低一點

### Claude 用量限制機制

- 所有付費方案採 **5 小時滾動視窗**，從第一則訊息開始計算
- 視窗期間無論是否閒置都持續倒數，多裝置共用
- **訊息配額**：
  - Pro ≈ 40–45 messages / 5hr
  - Max 5x ≈ 225 messages / 5hr
  - Max 20x ≈ 900 messages / 5hr
- **週上限**：2025-08-28 起對重度使用者引入 7 天週上限（weekly ceiling），與 5 小時滾動視窗疊加
- Opus 比 Sonnet 消耗約 3 倍 token，實際訊息數更少
- 高峰時段 Anthropic 會額外加速限制到期
- Claude.ai 與 Claude Code 共用同一 usage bucket

### Claude Code 已知隱性浪費

從洩漏的原始碼中發現：

- 截斷的回應（如 rate limit 錯誤）會保留在 context 繼續累積
- Skills 清單在啟動時自動注入，即使不需要也佔空間
- Claude Code 的 autocompact buffer 為 33K tokens

## 測試思維的轉變

傳統軟工：寫功能 → 單元測試 → 通過即可。

AI 系統：不只第 1 輪要通過，**第 10 輪、第 20 輪都要通過**。Context 隨對話積累，問題往往在深度互動後才浮現。

**解法**：定期審視真實使用者的完整 trace，而不是只在開發環境跑幾輪短測試。

## 實務速查：何時用什麼

| 情境 | 策略 |
|------|------|
| Context 到 100K+，擔心效能 | 新世代模型（支援 1M context）可續用；舊世代建議 `/clear` |
| 多個任務切換 | 每個任務之間 `/clear` |
| 想延續部分脈絡但瘦身 | `/compact` |
| 旁支問題 | `/btw` |
| 大量結構化資料查詢 | 檔案系統 + `grep`，非 RAG |
| 跨 session 記憶需求 | Git Context Controller |
| MCP 工具太多佔 context | 停用不用的 MCP、使用 `--no-mcp-upfront`、或將常用工具獨立成 skill |
| 多階段 agent | 動態 system prompt + state machine |
| 連鎖規則越堆越多 | 加 router 拆問題，不要堆 if/else |
| 重複性確定任務 | 封裝為 skill，不要佔 Claude token |
| 測試結果雜訊多 | Hook 過濾，只留失敗項 |
| 一次性指令 | `--append-system-prompt` |
| 發現 agent 跑偏 | 看完整 trace（Langfuse 等工具） |

## 延伸閱讀（vault 內其他相關主題）

以下筆記與本主題相關但未整合進 MOC（屬於其他主題的子範圍）：

- [[Harness-Engineer長期自主Agent設計]] — 長期 agent 的 harness 設計必涉 context 管理
- [[Claude-Code-Agent-Teams協作]] — 多 agent 拆分 context
- [[Claude-Tasks-Agent-Swarm升級]] — swarm 模式下的 context 分配
- [[Claude-Code-Skills]] — Skills 避免佔 context 的機制

## 外部來源

### 影片摘要（本 MOC 整合來源）

- daveebbelaar《AI Agent 有效的 Context Engineering》（2025-12-19）— <https://www.youtube.com/watch?v=nkJXADeI62c>
- Chase H AI《Claude 1M Context Window 攻克 Context Rot》（2026-03-14）— <https://www.youtube.com/watch?v=dk0QMbsdV8s>
- AILABS-393《Vercel 揭示 Claude Code 的最大優勢（檔案系統降成本）》（2026-01-22）— <https://www.youtube.com/watch?v=gZr5VmsXmXQ>
- AIJasonZ《.agent 資料夾讓 Claude Code 效能提升 10 倍》（2025-10-06）— <https://www.youtube.com/watch?v=MW3t6jP9AOs>
- AIJasonZ《Agent 記憶體管理 — Git Context Controller》（2026-02-18）— <https://www.youtube.com/watch?v=pAIF7vZm5k0>
- AILABS-393《Claude Code 用量限制優化指南》（2026-04-07）— <https://www.youtube.com/watch?v=YsdQE6juGXY>

### 官方與學術資源

- Claude Code 用量限制官方：<https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work>
- 論文《Git Context Controller: Manage the Context of LLM-based Agents like Git》— <https://arxiv.org/abs/2508.00031>
- GCC 官方實作 Contexa — <https://github.com/swadhinbiswas/contexa>
