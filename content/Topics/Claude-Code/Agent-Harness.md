---
title: Agent Harness
created: 2026-04-21
updated: 2026-04-21
tags:
  - claude-code
  - ai-agent
  - harness
  - moc
---

涵蓋 harness 定義、三角核心架構、可讀環境、context 管理演進、多 Agent 協作拓撲、評分制評估、工具與規則、平行化、常見陷阱。

## 是什麼

**Agent Harness** 是讓 agent 跑得久、跑得穩、多隻協作的**外部架構**——不是 prompt，而是指示、工具、使用者互動方式三者的整合。

三個核心組成：

- **指示（Instructions）**：引導 agent 行為的 system prompt 與規則，內建於工具本身
- **工具（Tools）**：檔案編輯、程式碼搜尋、終端機執行、測試、瀏覽器等
- **使用者互動方式**：如何下 prompt、如何追蹤回應

**為何重要**：不同模型對相同 prompt 反應不同（Claude 偏好 XML、其他模型偏好 markdown），harness 必須針對特定模型量身打造。

## 三角核心：Planner / Generator / Evaluator

Anthropic 對自家 harness 逐一移除元件後發現：以 Opus 4.5+ 為基礎的現代 agent 系統**只需要三件事**：

| 角色 | 職責 | 重點 |
|------|------|------|
| **Planner** | 規劃 | 產品層級目標、用戶故事，不是技術微任務 |
| **Generator** | 實作 | 逐功能建構、整合 git |
| **Evaluator** | 驗證 | 從對立角度找 bug，假設實作有問題 |

**關鍵原則**：**Generator 不能自我評估**。Agent 傾向自信稱讚自己的輸出，即使品質明顯不佳，對主觀任務（UI 品質）尤其嚴重。

**各框架 Evaluator 差異**：

- **BMAD**：專門 code review + QA agents，多角度測試
- **GSD**：verifier sub-agent，比對計畫生成 pass/fail 報告（門檻低）
- **Superpowers**：嚴格 TDD，測試寫完才能寫程式
- **SpecKit**：以 spec 為真相來源
- **Anthropic harness**：評分機制最嚴格，最接近實作強制

實作案例見 [[GAN-Style-Harness]]（gan-planner / gan-generator / gan-evaluator 三角 + 四維度加權評分）。

## 可讀環境與狀態持久化

Anthropic 實驗觀察兩個預設失敗行為：

- **One-shot 偏好**：Agent 傾向一次完成所有功能，context 用盡後下一個 session 無從銜接
- **過早宣稱完成**：Agent 提早喊「done」

解法是把狀態**外部化到檔案系統**：

### 環境骨架模式

- `init.sh`：啟動 dev server 等基礎設定
- `progress.txt`：進度日誌
- git commit：變更追蹤
- Feature list（JSON）：200+ 功能預設全 fail，agent 逐一確認

### OpenAI 的 agents.md 模式

- `agents.md` 作為 table of contents，分層放 architecture、design docs、DB schema
- Google Docs、Slack 訊息匯入 repo，讓 agent 能存取所有相關資訊
- Codebase 設計為可按 git worktree 啟動，供 Codex 平行驅動多個 instance

### Claude Tasks 的 JSON 任務圖

- 位置：`.claude/<session-id>/` 資料夾
- 每個 JSON 檔案包含名稱、描述、狀態
- 關鍵欄位：`blocks`（被阻擋的任務）、`blocked_by`（阻擋的任務）
- Session 結束、終端機關閉不遺失
- 環境變數可自訂 session 名稱，避免 ID 變更遺失

## Context 管理演進

**舊解法（Sonnet / Haiku / 小模型）**：

- Context reset + 外部文件持續任務狀態
- 詳細微任務拆分（BMAD、SpecKit）
- 每個 sub-agent 獨立 context window

**Opus 4.5+ 後**：

- Compaction 機制內建，「Context 焦慮」消失
- Sprint Contract（任務合約）可省略
- 不再需要 BMAD/SpecKit 式詳細拆分

**通用原則**：

- Grep 式搜尋優於手動 attach 整檔（手動標記會載入整個元件，即使只需一個函式）
- 開新對話時機：每個新任務、agent 表現混亂、完成一個邏輯工作單元
- 例外：同一功能的持續工作、同一討論的 context、除錯已實作功能

## 多 Agent 協作拓撲

**四層協作模式**，由鬆到緊：

| 拓撲 | 機制 | 代表實作 |
|------|------|----------|
| Sub-agents | 透過 orchestrator 或寫檔溝通 | Claude Code 內建 |
| Agent Teams | 共享 mailbox 直接溝通 + shared task list | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` |
| Agent Swarm | 任務圖（blocks/blocked_by）+ 獨立 200K context | Claude Tasks |
| Cross-CLI | 跨工具共享聊天頻道 | Agent Chatter（Claude Code + Gemini CLI + Codex） |

### Sub-agents vs Teams 對照

| 面向 | Sub-agents | Agent Teams |
|------|-----------|-------------|
| 平行執行 | 是 | 是 |
| Agent 間直接溝通 | 否 | 是 |
| 獨立 terminal session | 否 | 是 |
| 管理方式 | Orchestrator | Team lead |

### Agent Teams 使用案例

- **Code review + fix 平行化**：Member 1 找 bug → 逐筆傳 Member 2 修，同時 Member 1 繼續找
- **多視角除錯（4 agents）**：各從不同角度調查同一 bug，team lead 匯總（2-3 分鐘 vs 線性 5-10 分鐘）
- **長期任務（6 agents）**：2 agents 建基礎環境 + 4 agents 各做一頁面（等環境就緒解鎖），約 170k tokens 建完整個 app

### Agent Swarm（任務圖）

1. 識別並分解工作成小任務
2. 判斷任務類型：sequential（有依賴）vs parallel（無依賴）
3. 每任務完整流程：調查 → 規劃 → 實作，各階段互相鎖定
4. 依複雜度分配模型：簡單任務用 Haiku / Sonnet，複雜用 Opus

### Cross-CLI（Agent Chatter）

> 本節工具名稱「Agent Chatter」為 AILABS-393 頻道示範時的稱呼，repo 名與作者未在影片中明示；類似概念的開源工具有 `hcom`、`ntm`。

- 不同 agent 各在獨立 terminal，透過共享聊天頻道即時協調
- Mac/Linux 需 tmux，Windows 可直接執行
- `agents.mmd`：跨工具共同指令檔（Claude 讀 `CLAUDE.md`、Gemini 讀 `gemini.md`，兩者都寫「以 `agents.mmd` 為主」）
- **Loop Guard**：預設 4 次訊息後暫停等人工輸入，`continue` 繼續
- 三段式 Planner：Presenter → Challenger → Synthesizer，交叉驗證計畫

## Evaluation 機制與評分

主觀任務（UI、設計）需要**明確評分標準**讓 agent 知道「對」長什麼樣。

### Anthropic 前端評分四維度

1. **Design quality** — 各元件視覺一致性
2. **Originality** — 是否避開 AI 慣用配色（紫白藍）、有刻意設計選擇
3. **Craft** — 字型、間距、一致性、配色對比（創意優先，非僅技術正確）
4. **Functionality** — 每個 UI 元件是否發揮視覺功能

Claude 在 craft 與 functionality 表現已很好，**originality 和 design quality 是主要弱點**。

### 具象實作

見 [[GAN-Style-Harness]]：
- 四維度加權（Design 0.3 / Craft 0.3 / Originality 0.2 / Functionality 0.2）
- 門檻 7.0/10（7 = junior 紮實、9 = senior、10 = 可上線）
- Playwright 測試實際運行的應用

### TDD 作為自然 Evaluator

Agent 配合 TDD 的原因：有明確成功標準可優化，能朝目標逐步改進。

流程：

1. 請 agent 寫測試（**明確指示不要寫實作**）
2. 測試滿意後執行測試（此時全 fail）
3. Commit 測試到 git，防止 agent 後來修改
4. 請 agent 寫實作（**明確指示不要改測試**）
5. 迭代直到全部通過

## 工具與規則擴充

### 通用工具優於專用工具

**Vercel text-to-SQL agent 重構案例**：

- 舊：複雜專用工具 + 大量 prompt engineering → 脆弱、頻繁維護
- 新：單一 batch command 工具
- **結果：速度快 3.5 倍、token 少 40%、步驟少 40%、成功率 80% → 100%**

> 數字引自 Vercel 官方部落格〈[We removed 80% of our agent's tools](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)〉

**原因**：LLM 對 grep、npm、git 等原生工具訓練資料遠多於自訂 JSON schema。

### Rules（專案規則）

- 儲存於 `.agent/rules/` 或 `.claude/` 下 markdown 檔
- 範例：WCAG 無障礙合規規則，agent 規劃時自動納入

### Skills（能力擴充）

- 遵循 Anthropic 開放標準，包含指示、腳本、領域知識
- Agent 判斷相關時**動態載入**，維持 context 管理
- 位於 `.agent/` 或 `.claude/skills/`，每 skill 一個 `skill.md`
- 呼叫：指定 skill 名 + 任務

### Permissions 設定

每個 agent 獨立 `settings.json`：

- 必要指令（file edit、build）免人工審核
- 高風險指令保留確認
- MCP 工具也要配置

## 平行化與 Worktree

平行 agent 顯著改善效能：

- 各 agent 分配不同任務、使用不同模型（各有所長）
- **Git worktree 隔離**：各 agent 獨立分支，完成檢查後才 merge 主分支
- **Antigravity 共享工作區 + 獨立分支** 是穩定做法

**Agent Teams Best Practices**：

- 明確 scope：prompt 或 task 文件定義範圍
- 獨立任務：agents 不同時編輯同檔（避免衝突）
- 提醒 team lead 等待：主 agent 有時會不耐煩自行接手
- 任務大小適中：太小協調開銷高，太大失敗浪費大
- 監控執行：agent 偏離時立即介入

## 工具速查

| 工具 / 框架 | 生態 | 架構角色 | 協作拓撲 | 狀態持久化 |
|-------------|------|----------|----------|-----------|
| [[GAN-Style-Harness]] | Claude Code | Planner + Generator + Evaluator | Sub-agents | spec.md / feedback.md |
| GSD | Claude Code | 三角（驗證偏弱） | Sub-agents | 計畫文件 |
| BMAD | 通用 | Planner 詳盡 + Evaluator 多角度 | Sub-agents | PRD + sharded docs |
| Superpowers | Claude Code | Evaluator = TDD | Sub-agents | 測試檔 |
| SpecKit | 通用 | Evaluator = spec | Sub-agents | spec 文件 |
| Agent Teams | Claude Code | 自訂 | Teams（mailbox） | shared task list |
| Claude Tasks | Claude Code | 自訂 | Swarm（task graph） | `.claude/<id>/*.json` |
| Agent Chatter | 跨 CLI | Planner 三段式 | Cross-CLI | 聊天記錄 |
| Antigravity | Gemini 3 | 三角完整 | 共享工作區 + worktree | git branch |

## 常見陷阱

**徵兆：Agent 過早宣稱任務完成**
- 原因：Context 焦慮 + self-evaluation 自我稱讚
- 解法：獨立 Evaluator + JSON feature list 強制逐項驗證

**徵兆：Agent one-shot 後新 session 無法銜接**
- 原因：狀態只存在 context window
- 解法：外部 `progress.txt` / JSON task graph + git commit

**徵兆：多 agent 覆蓋彼此檔案**
- 原因：共享工作區無隔離
- 解法：Git worktree + 獨立分支後 merge

**徵兆：Plan 一個錯誤向下傳播，agent 難修正**
- 原因：微任務過細、agent 不思考
- 解法：改產品層級 plan + user stories，讓 agent 找路徑

**徵兆：自訂 JSON 工具脆弱、token 高**
- 原因：LLM 對自訂 schema 訓練資料少
- 解法：改用 grep / git / npm 通用 CLI

**徵兆：手動 attach 檔案後 context 爆炸**
- 原因：attach 載入整個元件
- 解法：讓 agent 用 grep 工具搜具體片段

## 相關主題

- [[GAN-Style-Harness]] — 本 MOC 第 2、6 章的具象實作案例（對抗式迴圈 + 四維度評分）
- [[Context-Engineering]] — 單次 prompt 內的 context 組裝（token 層，本 MOC 討論 runtime 層）
- [[Claude-Code-Agent-Packages]] — 可安裝的 agent 資產清單（package 層）

## 來源

**官方 / 論文**

- [Harness design for long-running application development（Anthropic, 2026/03/24）](https://www.anthropic.com/engineering/harness-design-long-running-apps)（本 MOC 三角架構的原始出處，作者 Prithvi Rajasekaran）

**影片**

- [Harness Engineer 長期自主 Agent 設計（AIJasonZ）](https://www.youtube.com/watch?v=kJPvfoLtFFY)
- [Anthropic 實驗後的 Agent Harness 現代化架構指南（AILABS-393）](https://www.youtube.com/watch?v=nBH07G-zayk)
- [Claude Code Agent Teams 協作（AILABS-393）](https://www.youtube.com/watch?v=MSyWjPDrHJw)
- [Claude Tasks 的 Agent Swarm 升級（AILABS-393）](https://www.youtube.com/watch?v=li8bIt-mjbA)
- [Google Antigravity 突然變得合理了（AILABS-393）](https://www.youtube.com/watch?v=e4giCKHIJy8)
- [Claude Code 與 Gemini CLI 協作開發工作流程（AILABS-393）](https://www.youtube.com/watch?v=XdtBAm2pM-0)
