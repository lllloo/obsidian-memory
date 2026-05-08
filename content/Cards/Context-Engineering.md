---
title: Context Engineering 與成本優化
created: 2026-04-20
updated: 2026-05-05
tags:
  - claude-code
  - ai-agent
  - context-engineering
  - memory
---

> AI Agent 在 demo 表現優異但在生產環境失敗，大多數情況不是模型能力不足，而是 **context engineering 做得不夠好**。本 MOC 整合官方文件、研究與多篇影片摘要；閱讀時要分清楚：哪些是 **Claude Code 官方能力**、哪些是 **社群 workflow**、哪些只是 **經驗法則而非保證**。

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

### Rot 實際起點：約 40% 容量（Anthropic 內部觀察）

Claude Code 開發者 Tariq 指出：context rot 從 **300K–400K tokens（約 40% 使用量）** 就開始出現，不是撐到接近 1M 才惡化。把 1M 當成「實際可用 1M」是危險誤解，多數人預設的 auto-compact 反而常讓事情更糟。

### 長任務 Agent 的 4 種失敗模式

context 沒管好時，長任務 agent 會出現這 4 種失敗——值得當 checklist 自查：

1. **Context pollution（污染）**：context 太雜，干擾推理
2. **Goal drift（目標漂移）**：忘掉原任務目標，反覆提醒仍跑偏
3. **Memory corruption（記憶損毀）**：內部狀態被寫錯仍依舊狀態繼續動作（典型：主 agent 建檔後 sub-agent 改了檔，主 agent 仍依舊記憶操作）
4. **Decision inaccuracy（決策不一致）**：近乎相同情境給矛盾決策（如同份程式兩處用不同 error handling pattern）

### 操作準則

- 長 context 仍有成本，但**不存在單一萬用門檻**；退化速度取決於模型、任務型態、工具輸出與工作方式
- 對 Claude Code 來說，`/clear`、`/compact`、`/resume`、auto-compaction 都是官方提供的 session 管理手段，不必自己發明一堆 hack
- **如果是新任務，就偏向新 session**；如果是同一任務的連續工作，再考慮延續當前脈絡
- 把「何時清 context」視為 workflow 決策，而不是迷信某個固定 token 數
- 在 300K–400K 區間**主動觸發 compact**，不要等 auto-compact——後者觸發時 Claude 被剝掉 system prompt、又有 recency bias，最不可靠

### 任務段落結束後的 5 種下一步（依意圖選）

每段工作完成後，下一步不只「繼續」一個選項。**依任務意圖選**：

| 選項                | 何時用                                                |
| ------------------- | ----------------------------------------------------- |
| 繼續                | 同一任務連續推進，當前 context 還健康                 |
| compact             | 想保留**部分**脈絡進新視窗（lossy，會丟細節）         |
| clear               | 開全新任務，**不需要**舊 context                      |
| clear + compaction（handoff） | 完成階段任務、需把摘要交給下一段／下一個 agent 接手 |
| rewind（雙擊 Esc）  | 上一個指令下錯了，回到那則指令前重下，**錯誤輸出不進 context** |

關鍵：別把「繼續」當預設。明確選擇能省下後面修錯的成本。

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

### `.agent/` 文件系統架構（社群 pattern，不是 Claude Code 內建）

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

針對長時間任務中 agent 「越來越笨」、重複犯錯、而單靠 session transcript 或單一記憶檔不夠好導覽的問題。

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

### 與 Claude Code 內建能力的差異

這裡最容易混淆。**Git Context Controller 不是 Claude Code 內建功能**；Claude Code 官方目前提供的是 `CLAUDE.md`、session resume、auto memory（可由環境變數控制）等能力。兩者解的是不同層次的問題：

| | Claude Code 內建記憶 / session 能力 | Git Context Controller |
|---|---|---|
| 主要用途 | 指令、session continuity、auto memory | git-style 的可導航外部記憶工作區 |
| 跨 session | 有，但以 resume / auto memory 為主 | 是，且把記憶顯式外部化 |
| 分支 / 合併 | 不是核心模型 | 是核心概念 |
| 是否官方內建 | 是 | 否，外部研究 / 工具 |

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

**停用思考模式（disable thinking）**：與 effort 不同，屬於更強的關閉方式。官方可透過 `/config`、快捷鍵切換，或用 `MAX_THINKING_TOKENS=0` / `CLAUDE_CODE_DISABLE_THINKING=1` 關閉。

### CLAUDE.md 精簡原則

- 建議控制在 **300 行以內**
- 不要放 Claude 本來就知道的事（dev server 啟動、專案結構解說）
- 只放：不該做的事、開發慣例、Claude 預設不知道的規範

**文件拆分策略**：特定區域（DB schema、API 規範）拆獨立文件，在 CLAUDE.md 連結，Claude 用到才載入。

**Path-specific rules / 分檔規則**：把不同領域規範拆到獨立文件，避免所有規則都塞進一份長文件。這可以透過 repo 自己的規範檔結構實作；若你使用 Claude Code 的 rules / skill / 文件分檔機制，也要遵守同一原則：**只讓當前任務載入真正相關的規則**。

### `.claude` 資料夾設定

```
// .claude/settings.json
{
  "alwaysThinkingEnabled": true,
  "showThinkingSummaries": false,
  "env": {
    "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
    "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS": "1"
  }
}
```

- `alwaysThinkingEnabled`、`showThinkingSummaries` 是官方 `settings.json` keys
- **prompt caching 不是 `disablePromptCaching: false` 這種設定鍵**；若要全域停用，官方是用環境變數 `DISABLE_PROMPT_CACHING=1`
- 停用 auto memory / background tasks 也是透過 `env` 內的官方環境變數，而不是 `autoMemory: false`、`disableBackgroundTask: true` 這類舊寫法

### Hooks 與 skills

- **Hooks 過濾輸出**：例如讓測試結果只注入失敗的測試，略過通過的測試
- **Skills**：重複工作流程封裝為 skill，搭配腳本執行確定性任務，避免把可程式化的工作浪費在 Claude token 上

### 其他旗標

- **`--append-system-prompt`**：一次性指令用此帶入，session 結束後消失，不永久佔 context
- **max output tokens**：可透過 `CLAUDE_CODE_MAX_OUTPUT_TOKENS` 控制；不需長輸出的任務可適度壓低

### Claude 用量限制機制

- 所有付費方案採 **5 小時滾動視窗**，從第一則訊息開始計算
- 視窗期間無論是否閒置都持續倒數，多裝置共用
- **不要把固定訊息數當正式承諾**：Anthropic 近年的官方說法已偏向「依訊息長度、對話長度、工具使用、模型與系統負載而變動」，而不是保證某個固定 messages 數
- **週上限存在，但方案細節會變動**：至少 Pro 已明確有 weekly usage limit；其他方案與門檻請以當下 Help Center 與 Usage 頁面為準，不要把舊日期或舊額度寫死
- Opus 比 Sonnet 消耗約 3 倍 token，實際訊息數更少
- 高峰時段可用量可能更緊，實際體感會受當下容量與負載影響
- Claude.ai 與 Claude Code 共用同一 usage bucket

### Claude Code 常見的 context 浪費來源（實務觀察）

- 手動 attach 整個大檔，明明只需要其中一段
- MCP / tools / docs 一次載太多，但當前任務根本用不到
- 把通過的測試、冗長 log、完整 build output 全部留在對話裡
- 明明是新任務，卻沿用已經很長的舊 session

比起追逐神祕數字，更有用的是：**持續檢查哪些資訊真的幫助當前任務，哪些只是噪音。**

## 測試思維的轉變

傳統軟工：寫功能 → 單元測試 → 通過即可。

AI 系統：不只第 1 輪要通過，**第 10 輪、第 20 輪都要通過**。Context 隨對話積累，問題往往在深度互動後才浮現。

**解法**：定期審視真實使用者的完整 trace，而不是只在開發環境跑幾輪短測試。

## 按需載入：5 種讓 context 只在需要時出現的機制

把資訊放進 context 應該是**按需的**，不是預先全塞。Claude Code 提供 5 種按需載入機制，搭配使用可避免 context 一開機就被填滿：

| 機制                       | 觸發時機                          | 典型用途                                                              |
| -------------------------- | --------------------------------- | --------------------------------------------------------------------- |
| **Rules（path-scoped）**   | 模型動到對應檔案類型時            | Python 規則只在動 .py 才注入；前端規則只在動 frontend/ 才注入         |
| **Hooks**                  | 預設事件觸發                      | 涉及時間的訊息 → 注入「先確認今日日期」；工具跑完 → 注入「檢查輸出有無洩密」 |
| **Skills**                 | 用戶 `/skill` 或模型讀主檔判斷需用 | 把例行流程封裝；主檔簡述、副檔按需                                    |
| **Sub-agent**              | 主 agent 派任務時                 | 長文件處理、研究步驟外包，只回傳摘要                                  |
| **MCP Tool Search**        | 預設啟用                          | 工具描述按需呼叫，不全部 upfront；用 `ENABLE_TOOL_SEARCH` 控制（`auto` 模式：可塞進 10% context window 才一次載入），server/tool 層可用 `alwaysLoad: true` opt-out |

關鍵原則：**不要把可以按需的東西預先塞進 system prompt 或 CLAUDE.md**。長期來看，按需載入比單次 `/clear` 更省 context。

## 實務速查：何時用什麼

| 情境 | 策略 |
|------|------|
| Context 到 100K+，擔心效能 | 新世代模型（支援 1M context）可續用；舊世代建議 `/clear` |
| 多個任務切換 | 每個任務之間 `/clear` |
| 想延續部分脈絡但瘦身 | `/compact` |
| 旁支問題 | `/btw` |
| 大量結構化資料查詢 | 檔案系統 + `grep`，非 RAG |
| 跨 session 記憶需求 | Git Context Controller |
| MCP 描述太多佔 context | 預設 Tool Search 已按需載入；停用不用的 MCP；常用流程封 skill |
| MCP 工具大輸出灌爆 context | 把 MCP 呼叫包成 bash 命令（或經 CLI 包裝層），輸出重導向到檔案，再 `grep` 提取真正需要的段落 |
| 多階段 agent | 動態 system prompt + state machine |
| 連鎖規則越堆越多 | 加 router 拆問題，不要堆 if/else |
| 重複性確定任務 | 封裝為 skill，不要佔 Claude token |
| 測試結果雜訊多 | Hook 過濾，只留失敗項 |
| 一次性指令 | `--append-system-prompt` |
| 發現 agent 跑偏 | 看完整 trace（Langfuse 等工具） |

## 延伸閱讀（vault 內其他相關主題）

以下筆記與本主題相關但未整合進 MOC（屬於其他主題的子範圍）：

- [[Harness-Engineering]] — Harness 架構、多 Agent 協作拓撲、context 管理演進（已整合 Harness-Engineer / Agent-Teams / Agent-Swarm 等相關內容）
- [[Claude-Code-Skills]] — Skills 避免佔 context 的機制

## 外部來源

### 影片摘要（本 MOC 整合來源）

- daveebbelaar《AI Agent 有效的 Context Engineering》（2025-12-19）— <https://www.youtube.com/watch?v=nkJXADeI62c>
- Chase H AI《Claude 1M Context Window 攻克 Context Rot》（2026-03-14）— <https://www.youtube.com/watch?v=dk0QMbsdV8s>
- AILABS-393《Vercel 揭示 Claude Code 的最大優勢（檔案系統降成本）》（2026-01-22）— <https://www.youtube.com/watch?v=gZr5VmsXmXQ>
- AIJasonZ《.agent 資料夾讓 Claude Code 效能提升 10 倍》（2025-10-06）— <https://www.youtube.com/watch?v=MW3t6jP9AOs>
- AIJasonZ《Agent 記憶體管理 — Git Context Controller》（2026-02-18）— <https://www.youtube.com/watch?v=pAIF7vZm5k0>
- AILABS-393《Claude Code 用量限制優化指南》（2026-04-07）— <https://www.youtube.com/watch?v=YsdQE6juGXY>
- AILABS-393《Anthropic 修復 1M Context Window 的問題》（2026-04-22）— <https://www.youtube.com/watch?v=O1XLCh-uA_E>（Tariq 300K–400K rot 起點、4 種失敗模式、5 種下一步）
- AgentcrewAcademy《Claude 上下文總是爆滿、回答變蠢？5 個按需載入》（2026-04-20）— <https://www.youtube.com/watch?v=J1WjxzzSzv8>（按需載入 5 機制框架）
- AILABS-393《MCP2CLI — 用 CLI 工具解決 MCP Context 膨脹問題》— <https://www.youtube.com/watch?v=LqN_ItMqovA>

### 官方與學術資源

- Claude Code 用量限制官方：<https://support.claude.com/en/articles/11647753-how-do-usage-and-length-limits-work>
- 論文《Git Context Controller: Manage the Context of LLM-based Agents like Git》— <https://arxiv.org/abs/2508.00031>
- GCC 官方實作 Contexa — <https://github.com/swadhinbiswas/contexa>
