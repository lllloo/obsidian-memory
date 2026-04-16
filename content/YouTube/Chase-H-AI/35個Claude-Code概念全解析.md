---
title: 35 個 Claude Code 概念全解析——非工程師也能懂
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-08
source: https://www.youtube.com/watch?v=UAMAAoSPu8o
parent: "[[01.index]]"
---

## Section 1：核心基礎（概念 1–5）

### 概念 1：Claude.ai vs Claude Code 的差異

兩者使用相同 AI 大腦（例如 Opus 4.6），差異在於：

- **Claude.ai**：純對話，只能輸出文字
- **Claude Code**：大腦有了「身體」，可執行工具呼叫、寫入檔案、操作電腦、發送 email 等

### 概念 2：安裝

Google 搜尋「Claude Code install」→ 進官方文件，依作業系統複製單行安裝指令：

```bash
# macOS / Linux / WSL
npm install -g @anthropic-ai/claude-code

# Windows PowerShell（另有獨立指令）
```

安裝後輸入 `claude` 即可啟動。

### 概念 3：在哪裡使用

| 介面 | 適合誰 |
|---|---|
| 原生終端機（PowerShell / Terminal）| 最完整功能 |
| VS Code（附帶終端機）| 新手推薦：可同時看檔案結構 |
| Claude Code 桌面應用 | 想要 GUI 的用戶 |
| Cursor / co-work | 99% 功能可用，但功能較受限 |

建議：至少給終端機嘗試一到兩週再決定。

VS Code 設定：File → Open Folder → 建新資料夾 → Terminal → New Terminal → 輸入 `claude`。

### 概念 4：權限設定

按 `Shift+Tab` 切換三種模式：

| 模式 | 行為 |
|---|---|
| 預設（空白）| 每次編輯檔案都詢問 |
| Accept Edits On | 自動接受檔案編輯，bash 指令仍需確認 |
| Plan Mode | 只規劃，不執行 |

進階：啟動時加 `--dangerously-skip-permissions` 旗標，開啟 Bypass Permissions，完全略過所有確認。多數熟練用戶最終都會用這個模式。

### 概念 5：Plan Mode

`Shift+Tab` 切到 Plan Mode 後，Claude Code 不會直接執行，而是：

1. 詢問釐清問題（網站類型、技術堆疊等）
2. 輸出詳細執行計畫
3. 等待確認後才執行

**這是提升輸出品質最重要的單一技巧**，讓 Claude Code 填補 prompt 中的空缺。

---

## Section 2：工作流程心法（概念 6–15）

### 概念 6：正確心態——把 Claude Code 當協作者

- 不要只是接受它給的選項（例如技術堆疊），要主動問它為什麼
- 把它當成耐心無限的老師，要求解釋你不懂的概念
- 「vibe coding」（無腦按 Accept）和真正學習之間的差距，就在這裡

### 概念 7：CLAUDE.md 檔案

Claude Code 在每個專案自動建立，作用：

- 儲存此專案的「永久指令」——命名慣例、框架規則、注意事項等
- 每次提示都會被 Claude Code 參考
- 原則：少即是多，只放真正每次都適用的規則

### 概念 8：Context Window

```
/context   # 查看目前使用量
```

- 目前上限：1 million tokens（每個字約 1 token）
- 填滿後 session 結束
- 越接近上限，每次提示越貴（前文全部重新傳送）

### 概念 9：Context Rot

Context Window 越填越多，**Claude Code 的品質越來越差**。解法：

```
/clear   # 重置 session，從零開始
```

重置不等於失憶：Claude Code 仍可從專案檔案重新理解狀況。建議不超過 200K tokens 就重置。

### 概念 10：狀態列（Status Line）

讓 context 使用量隨時可見：

```
/status-line
# 然後輸入：建立一個持久狀態列，顯示當前資料夾、模型、context window 使用量
```

重啟後生效，之後永久顯示於終端機底部。

### 概念 11：/rewind

```
/rewind   # 回到之前的 session 狀態
```

包含程式碼變更，可用於「哎，我剛才不應該做那個決定」。

### 概念 12-13：Context 管理最佳實踐

- 有需要帶到下一 session 的資訊？先請 Claude Code 寫簡短摘要，複製到新 session
- 越早重置，每次提示的 token 費用越低

### 概念 14：/model

```
/model   # 切換模型
```

可選：Opus 4.6、Sonnet 4.6、Sonnet（1M context）、Haiku

| 方案 | 建議模型 |
|---|---|
| Pro（$20/月）| 全用 Sonnet |
| Max 5x | 可用部分 Opus |
| Max 20x | 可大量用 Opus |

`/effort`：調整思考深度（auto / low / high），越高越耗 tokens。

### 概念 15：Git

```
# 在 Claude Code 內直接說：
git commit this
```

- Claude Code 非常擅長 git 操作
- `git commit` = 程式碼存檔點，是 `/rewind` 之外更持久的安全網
- 推送到 GitHub 前必須先 commit

---

## Section 3：工具箱（概念 16–23）

### 概念 16：Skills（技能）

Skills 本質上是**文字 prompt 模板**，讓 Claude Code 以特定方式執行特定任務。

安裝方式：
```bash
/plugin    # 打開 plugin 市場
# 搜尋 "frontend-design"，點擊安裝，reload plugins
```

呼叫方式：
```
/frontend-design  # 直接指令
# 或在 prompt 中說 "use the frontend-design skill"
# 或直接描述前端任務，Claude Code 會自動判斷
```

Skills 有兩個層級：
- **User level**：所有專案共用（預設）
- **Project level**：只在特定專案生效

### 概念 17：Skill Marketplace

`/plugin` → Discover Plugins，可搜尋官方與社群 Skills。也可以把 GitHub URL 貼給 Claude Code，請它自動安裝。

### 概念 18：Skill Creator Skill

最強大的 skill，功能：
- 自動 A/B 測試：新 skill vs 不用 skill
- 測試 skill 改版效果（量化數據）
- 協助識別哪些重複任務值得建立成 skill

**建議**：所有每天重複做多次的工作流程都應建成 skill。

### 概念 19：Few-shot Prompting

比只給文字 prompt 更好的方式：同時提供**截圖 + 原始 HTML 程式碼**。

實作範例：
```
在瀏覽器按 Ctrl+U 查看 HTML → 全選複製
拖放截圖到 Claude Code 的對話框
說：讓前端更接近 Anthropic 的風格，這是他們網站的 HTML 和截圖
```

效果：比純文字描述更精確控制輸出，遠離「prompt and pray」。

### 概念 20：MCPs（Model Context Protocol）

將 Claude Code 連接外部程式（Notion、Linear、Figma、Stripe 等），讓它能直接操作這些工具。

```
# 安裝方式
Claude Code，幫我設定 Notion 的 MCP server
# Claude Code 會搜尋文件、找到指令、引導你取得 API key
```

**趨勢**：MCPs 正在被 CLIs 取代，因為 MCPs 有更高的 overhead（較慢、token 消耗較多）。

### 概念 21：CLI 工具

CLI（Command Line Interface）工具與 Claude Code 同住終端機，整合更緊密：

- 比同類 MCP 效率高約 90%（以 Playwright 為例）
- 安裝：直接告訴 Claude Code「幫我安裝 Playwright CLI」

**選擇原則**：有需求再找 CLI，不要為了裝而裝。告訴 Claude Code「這個需求有沒有 CLI？」，讓它搜尋確認。

### 概念 22：Few-shot Prompting 進階

已在概念 19 中覆蓋（截圖 + HTML 原始碼組合）。

### 概念 23：Adversarial Code Review

AI 評估自己程式碼時會偏向認為「很好」，解法：

**方案 A**：開第二個 terminal，以新 session 的 Claude Code 檢查第一個 session 的程式碼，明確要求「以挑剔眼光審查，想像你是討厭 AI 的 Reddit 用戶」。

**方案 B**：安裝 Codex plugin，使用 `/codex:adversarial-review`，讓不同 AI 系統審查。

---

## Section 4：進階與Power User（概念 24–35）

### 概念 24–25：Custom Slash Commands & Hooks

```
# 建立自訂指令（範例：作者的 YouTube 研究工作流）
/yt-pipeline   # 呼叫多個 sub-skills + Notebook LM API
```

**Hooks**：在特定事件前後自動執行動作。

```
# 實用範例：任務完成時播放音效
建立一個 hook，在 Claude Code 完成任務時播放音效
```

其他 hook 例子：完成時發送 email、自動 git commit 等。

### 概念 26：Sub-agents

Claude Code 可自動生成 sub-agents 並行處理多個任務。

- Sub-agents 各自獨立、互不溝通
- 你不需要手動建立，Claude Code 自動判斷何時需要

### 概念 27：Agent Teams（實驗性功能）

Sub-agents 之間可互相溝通，加上一個「協調 agent」居中管理。

啟用方式：
```
# 在 settings.json 中啟用
# 或告訴 Claude Code：幫我在 settings.json 裡啟用 agent teams
```

使用時必須明確說「create an agent team」，不會自動觸發。

```
create an agent team：
- 一個 agent 負責前端設計
- 一個 agent 負責 newsletter 表單
- 一個 agent 負責研究 blog 主題
```

**成本**：比普通 sub-agents 耗更多 tokens（協調通訊開銷）。

### 概念 28：Multiple Sessions（多視窗）

可同時開多個 terminal 各自執行 Claude Code，但注意：

- 多個 session 同時修改同一個檔案 = 衝突（三個人共用一張紙）
- 超過 2–3 個 terminal 通常是「生產力劇場」，不是真正高效

### 概念 29：Git Worktrees

解決多 session 同時工作的衝突問題：

```bash
claude --worktree frontend-design   # 建立獨立的工作樹
claude --worktree authentication
claude --worktree payments
# 完成後回到主 session：
# "take a look at these worktrees and merge them"
```

每個 worktree 有自己的檔案副本，修改不互衝，最後合併。

### 概念 30：Frameworks（GSD、BMAD、Superpowers 等）

GitHub 上有「編排層」框架，在 Claude Code 之上改變計畫、執行、進度記錄的方式。

**作者觀點**：
- GSD 早期對處理 context rot 很有幫助，但很多功能已被 Claude Code 原生吸收
- 新手不要急著用，先把基礎掌握好
- 規則：不要為了用框架而用框架

### 概念 31–32：Triggers & Scheduled Tasks

**Loop（session-based 定時任務）**：

```
/loop 30m   # 每 30 分鐘檢查一次 deployment status
```

限制：terminal 必須保持開啟，最長 7 天。

**Scheduled Tasks（Claude Code 桌面應用）**：

- Remote task：雲端執行，電腦可關機
- Local task：電腦需開著，Claude Code 需執行中

例：每天早上 7 點自動拉 GitHub trending repos。

### 概念 33：Ultra Plan

```
/ultraplan <描述任務>
```

將計畫推送至雲端，疑似有多個 agents 在背後協作。詳細比較見 [[Claude-Code推出Plan-Mode-2.0了嗎]]。

### 概念 34：Remote Control（手機遠端操控）

從手機 Claude app 使用 Remote Control 功能，幾乎等於在手機上看到終端機的鏡像。

需求：電腦上有已開啟的 Claude Code session。若電腦睡眠後喚醒，session 會自動重連。

### 概念 35：追蹤新工具的方法

GitHub Trending 頁面是最佳情報來源：

```
# 讓 Claude Code 每天早上自動取得並整理
# 作者範例：每天收到 AI 相關 top 10 repos，含星數、主題、描述
```

或直接在 GitHub Trending 頁面篩選 AI 相關、按時間範圍過濾，也可請 Claude Code 幫你 clone 並解釋任何感興趣的 repo。
