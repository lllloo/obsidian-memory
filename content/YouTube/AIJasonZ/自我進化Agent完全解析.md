---
title: Self-Evolving Agent 完全解析
tags:
  - youtube
  - ai-agent
  - claude-code
  - memory-system
  - self-learning
created: 2026-04-22
updated: 2026-04-22
published: 2026-04-21
source: https://www.youtube.com/watch?v=2zhchG0r6iI
parent: "[[01.index]]"
---

## 自我進化 Agent 的兩大分支

市面上「Self-Evolving Agent」方案可分為兩類，目標完全不同：

- **改進 Agent Harness 本身（Auto-Agent / AutoResearch）**：透過外部 for-loop 不斷修改 harness 或模型腳本，再跑評估決定保留或丟棄改動，類似 fine-tune 的概念。一旦訓練結束，輸出的 harness / model 是「凍結」的。
- **In-Context Learning / Memory（Hermes Agent、Claude Code AutoDream、Open Claude 等）**：重點在讓 agent 記住過去的行動與回饋，越用越聰明，是目前實務上最有用的方向。

Auto-Agent 需要大量可程式化驗證的任務資料庫，多數團隊不具備這條件；In-Context Learning 則幾乎每個產品都能直接落地。

## Agent 架構光譜

在跳進自我進化之前，要先理解「越 Agentic 不一定越好」：

- 單次 LLM 呼叫 → Workflow chaining（類似 Zapier、n8n） → Fully Agentic（可決策、生成 skill、自我進化）
- 越 Agentic 成本越高、速度越慢；要根據 use case 選擇決定性 vs 彈性
- HubSpot 的 AI Agent Cheat Sheet 針對不同架構做比較（影片贊助）

## In-Context Self-Learning 的三大支柱

所有自我進化 agent 的 memory 系統，核心都圍繞這三塊：

1. **Memory（事實記憶）**
   - Hot memory：永遠載入 system prompt（如 `user.md`、`CLAUDE.md`）
   - Warm memory：按需載入
2. **Skill（領域知識 / 程序性知識）**
   - 封裝特定任務的 SOP 與最佳實務
3. **History（可搜尋的 raw conversation log）**
   - 讓 agent 回頭查詢過往對話

不同 harness 對這三塊的覆蓋度不一，這決定了它們「是否感覺更聰明」。

## Claude Code：三層記憶系統

Claude Code 從「單一 `CLAUDE.md`」進化到三層記憶系統，許多使用者並不知情。

### 演進歷程

- **早期**：所有偏好與 guardrail 都塞進單一 `CLAUDE.md`，很快就過於膨脹
- **改進**：把 `CLAUDE.md` 當成 index，描述何時要讀取／更新其他檔案（hot + warm memory 模式）
- **現在**：引入 Auto-Memory 與 AutoDream

### Auto-Memory（可開啟的功能）

- 透過 special prompt 指導 agent 判斷什麼值得記憶
- memory 檔案存放於專案下的 `.claude/memory/`
- `memory.md` 扮演 index / table of content 角色，被自動載入 system prompt
- 依類型（user preference、feedback、project、reference doc）分檔存放

### AutoDream（從洩漏的原始碼發現）

- 背景 process，在 session 結束後觸發
- 用特殊 prompt 啟動新的 Claude Code session，執行以下流程：
  1. 讀取現有 memory
  2. 檢查對話歷史找出過時 memory
  3. 合併 memory 並更新 index
- 關鍵點：這是非同步執行，不依賴 agent 當下記得更新

### Claude Code 的限制

- 主要只解決「事實類 memory」
- Skill 雖然支援，但仍高度依賴人工找 skill 並安裝
- Raw conversation log 雖保留但不可搜尋（coding agent 情境下較少需求）

## Open Claude：把 Memory 當一等公民

Open Claude 讓許多人初次使用時驚艷，原因在於：

- **細分 memory 檔案**：每個檔案代表一個面向
- **`bootstrap.md`**：主動引導 agent 向使用者澄清資訊
- **Daily log**：高層次快照，紀錄人與 agent 的互動
- **Memory search tool 內建**：可橫跨所有 memory 檔案 + raw conversation history 搜尋
- **Skill 第一公民**：agent 可主動從 Claude Hub 搜尋、安裝、更新 skill

缺點：memory 建立、skill 建立、memory search 仍需人主動 prompt，缺少背景非同步 proactive process。

## Hermes Agent：最完整的自我進化實作

Hermes Agent 補齊 Open Claude 缺少的「自主」部分，引入兩個核心概念：

### 1. Autonomous Skill Generation

機制：

- 計算 agent 的步驟數
- 每當 agent 執行超過 10 步且未建立任何 skill，spin up 一個背景 sub-agent
- 此 sub-agent 不阻塞主流程，後台 review 已完成的工作
- 判斷「是否有可封裝為 skill 的非平凡做法」

Skill Reviewer 的 prompt 大致如下：

```
Review the conversation above and consider saving or updating a skill
if appropriate. Focus on whether a non-trivial approach was used to
complete a task that required trial and error or changing course due
to experimental findings along the way.
```

Skill 配有專屬的 skew manager tool，支援 create、patch、delete、新增／移除檔案等操作。主 agent 的 prompt 也有 proactive 提醒：

> When using a skill and finding it outdated, incomplete or wrong, patch it immediately. Don't wait to be asked. Skills that unmaintained become liabilities.

### 2. Safety Scan

- agent 建立新 skill 時會經過 `skill_guard.py`
- 內含多組 reject pattern，命中則自動刪除 skill 並回傳訊息給 agent 調整
- 通過驗證才會正式存檔

### 3. Memory Reviewer（類似 AutoDream）

Hermes 的 memory 架構有四層：

| 類型 | 檔案 | 角色 | 載入時機 |
|------|------|------|----------|
| User facts | `user.md` | 使用者身份、偏好、工作風格 | 每次 system prompt |
| Environment facts | `memory.md` | 專案慣例、作業系統 | 每次 system prompt |
| Skill | 各 skill 檔 | 領域知識 | 按需載入 |
| History | SQLite DB | 每次對話 raw log | session search 搜尋 |

補充：

- `user.md` + `memory.md` 合計字元上限約 4,000，逼迫 agent 把多數知識丟到 skill
- 每 10 turns 若未做過 memory extraction，會觸發背景 Memory Reviewer sub-agent
- 可外接 Mem0、Homecho 等 semantic memory layer

Memory Reviewer prompt 大致：檢查使用者是否表達對自己、偏好、期望的資訊，若有則寫入對應檔案。

## State-of-the-Art 實作重點

整合觀察，建構自我進化 agent 的最佳實務：

- **Skill**：封裝領域知識 / procedural knowledge
- **Memory**：封裝事實，區分 hot 與 warm
- **History**：保留可搜尋、可稽核的 raw log
- **非同步背景 process**：不依賴人或 agent 當下記得更新

這套模式本身出乎意料地簡單，核心就是「把記憶當一等公民 + 自動化維護」。

## 不換 Harness 也能升級 Claude Code / Open Claude

可直接套用第三方 skill 強化現有 agent：

- **Self-Improving Agent Skill（最熱門）**
  - 在 Open Claude 的 memory 之外增加 `learnings/` 資料夾，內含 learnings、errors、feature-request 檔案
  - 善用 hooks 減少對 prompt 的依賴：
    - `UserPromptSubmit` hook：每次使用者送出訊息後，附加一小段 prompt 提醒 agent 依循 memory 產生模式
    - `PostToolUse` hook：每個 bash 指令執行後檢查結果，匹配到 error pattern 時 append「error detected」提示
  - Open Claude bootstrap 時自動注入 `self-improvement-reminder.md` 到 system prompt

從 Open Claude 遷移到 Hermes Agent 也只要一個 migrate 指令，成本不高。

## 關鍵 Takeaway

- Auto-Agent 是「訓練 harness」，多數團隊用不到
- In-Context Self-Learning 才是目前實務最可落地的方向
- 三支柱架構（Memory / Skill / History）+ 非同步背景維護 = state-of-the-art
- Hermes Agent 最完整，但 Claude Code + self-improving skill 也能達到類似效果
- Agent 建立 skill 必須搭配 safety scan，否則容易污染 context
