---
title: Claude Code 效率技巧與設定
created: 2026-04-24
updated: 2026-04-25
tags:
  - claude-code
  - workflow
  - cli
  - moc
---

> Claude Code 日常操作技巧的 hub MOC。這篇只保留已核對過的 built-in features 與穩定工作流；更偏社群觀點的延伸內容，先留在其他卡片慢慢補證據。

## 延伸 Card

- [[Claude-Code-開工前-SOP]] — 開工前的規劃與文件清單（偏 workflow 建議）
- [[Claude-Code-CLI-工具生態]] — CLI-first 社群工作流與第三方工具清單（待補更多 source cleanup）

## 章節地圖

1. [日常指令技巧](#日常指令技巧) — `/insights`、`/btw`、`/statusline`、Notification hooks、`/recap`
2. [Hooks 與 exit code](#hooks-與-exit-code) — pre-tool-use 守門與 blocking/non-blocking 差異
3. [多 Agent 協作概覽](#多-agent-協作概覽) — Subagent / Agent Teams / Fork / worktree
4. [入門光譜](#入門光譜) — IDE / Terminal / 權限模式
5. [速查：情境對照技巧](#速查情境對照技巧) — 跨主題索引

## 日常指令技巧

### `/insights` — 工作習慣分析

官方內建 command，會分析你的 Claude Code sessions，整理出互動模式、常碰到的 friction points，以及可改善的工作流。適合週期性回看，把值得長期保留的規則整理進 `CLAUDE.md`。

### `/btw`（by the way）— 側邊對話

這個功能是官方文件化的 side question：

- 看得到**完整主 session context**
- **不會進主 conversation history**
- **沒有 tool access**，只能回答當前 session 已知內容
- 即使主任務正在跑，也能獨立發問

適合查名詞、補問前文、確認某個決策，不適合需要讀檔或跑指令的新研究工作。

### `/statusline` — 常駐狀態列

官方內建 command，可自然語言描述你想看的資訊，例如：模型、context 百分比、cost、git branch。

最常用的組合：

- model name
- context percentage
- git branch / dirty state
- cost / duration

**建議至少常駐 context %**，因為這比憑感覺判斷該不該 `/compact` 靠譜得多。

### Notification hook + `/hooks`

不是 `/hook` 單一命令；正確做法是：

1. 在 `settings.json` 設 `Notification` hook
2. 用系統通知指令（像 macOS `osascript`）在 Claude 完成、等待權限、或需要你回應時提醒
3. 用 `/hooks` 檢查目前已載入的 hook 配置

多 session 並行時很有感，不然很容易忘記哪個視窗已經跑完。

### `/recap` — 回來先看一行摘要

Claude Code 會在你離開終端一段時間後，自動準備 one-line session recap；也可以手動用 `/recap` 立即生成。很適合中斷後回來快速找回節奏。

### 更多 session 層指令

- `/clear` — 開新對話，清空 context
- `/compact` — 壓縮目前對話，保留主線
- `/rewind` — 回到某個 checkpoint，還原 conversation / code / 或只做 targeted summary
- `/context` — 看到目前 context 用量與重點耗用來源

## Hooks 與 exit code

Hooks 在 Claude Code lifecycle 特定時間點執行 shell 指令。**Exit code 是 hook 與 Claude 互動的核心介面。**

| Exit code | 行為 |
|---|---|
| `0` | 成功；若使用 JSON 協議，只有 `exit 0` 會被當成有效輸出處理 |
| `2` | **阻斷**：常用來 block `PreToolUse`、`UserPromptSubmit`、`Stop` 等事件 |
| 其他非 0 | **大多數事件視為 non-blocking error**：Claude 會記錄 hook error，但流程通常繼續 |

**重要提醒**：在 Claude Code 裡，`exit 1` 通常**不等於**「幫你硬擋下來」。想強制擋住，多數情況要用 `exit 2`。`WorktreeCreate` 是少數例外：它在任意非 0 時都會中止。

### 常用 pattern

**TDD 保護**：用 `PreToolUse` hook 擋掉對測試檔的修改。

**套件管理器一致性**：攔截 `pip install`，要求改用 `uv` 或專案指定工具。

**輸出降噪**：只把失敗測試或關鍵錯誤送回 context，避免把一大串通過測試塞滿對話。

## 多 Agent 協作概覽

### Subagent vs Agent Teams vs Forked subagent

| | Subagent | Agent Teams | Forked subagent |
|---|---|---|---|
| Context | 獨立 context，不繼承主對話 | 每位 teammate 都是獨立 context，但可共享 task list / mailbox | 繼承主 session 對話 |
| 互相溝通 | 否，結果回主線 | 是，可彼此傳訊 | 否，最後回主線 |
| 啟動方式 | 自動 delegation 或明確指定 | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | `CLAUDE_CODE_FORK_SUBAGENT=1` 後由 `/fork` 觸發 |
| 適合場景 | 單點研究、單點審查、隔離輸出 | 多人分工、長任務、平行 review/fix | 中途開支線、不想重講背景 |

### `/branch` vs `/fork`

- 預設情況下，`/branch` 會建立對話分支；`/fork` 是它的 alias
- 開啟 `CLAUDE_CODE_FORK_SUBAGENT=1` 後，`/fork` 會改成 forked subagent，不再等於 conversation branch

### Git worktrees 平行 Agent

官方支援 worktree isolation：

- `claude --worktree feature-auth`
- subagent frontmatter 可設 `isolation: worktree`

每個 agent 各有自己的 working tree，可避免 서로覆蓋檔案。**subagent 若沒有留下變更，worktree 會自動清掉。**

## 入門光譜

### IDE / Terminal 光譜

| 使用方式 | 控制度 | 備註 |
|---|---|---|
| Terminal | 最多 | 完整功能、最貼近原生 Claude Code |
| IDE 內建 terminal | 高 | 有檔案樹與 editor 輔助，但仍是 terminal-first |
| Desktop app | 中 | 更圖形化，適合平行 session |
| Web / mobile | 最少 | 適合遠端、排程、web session |

### 權限模式速記

預設的 `Shift+Tab` cycle 是：

`default → acceptEdits → plan`

可選模式：

- `bypassPermissions`：只有你用 `--dangerously-skip-permissions` 或 `--permission-mode bypassPermissions` 啟用後，才會進 cycle
- `auto`：帳號與模型符合條件時才出現
- `dontAsk`：**不會**出現在 cycle，只能用旗標直接開

## 速查：情境對照技巧

| 情境 | 工具 / 做法 | 深入見 |
|---|---|---|
| 想知道自己最常卡在哪 | `/insights` | 本文「日常指令技巧」 |
| 主任務跑到一半想問旁支 | `/btw` | 本文「日常指令技巧」 |
| 想持續盯 context / cost | `/statusline` | 本文「日常指令技巧」 |
| 多視窗並行，怕錯過完成時機 | Notification hook + `/hooks` | 本文「日常指令技巧」 |
| 想回到某個安全點 | `/rewind` | [[Claude-Code-Dangerously-Skip-Permissions]]（邊界）與官方 checkpointing |
| 想要只讀分析不要直接改碼 | `plan` mode | [[Claude-Code-開工前-SOP]] |
| 想讓 agent 平行工作但不要撞檔 | subagent `isolation: worktree` 或 `--worktree` | 本文「多 Agent 協作概覽」 |
| 想少一點權限提示但別完全裸奔 | `acceptEdits` / `auto` / permission rules | [[Claude-Code-Dangerously-Skip-Permissions]] |

## 相關主題

- [[Claude-Code-Skills]] — Skills 機制、Progressive Disclosure、frontmatter 與常見坑
- [[Claude-Code-Dangerously-Skip-Permissions]] — bypass mode 的邊界與替代方案
- [[Claude-Code-Agent-Packages]] — 常用社群 agent packs
- [[Topics/Obsidian/index|Obsidian]] — 在 Obsidian vault 裡使用 Claude Code 的整合實例

## 外部來源

### 官方文件（已核對）

- [Commands](https://code.claude.com/docs/en/commands)
- [Interactive mode](https://code.claude.com/docs/en/interactive-mode)
- [Common workflows](https://code.claude.com/docs/en/common-workflows)
- [Customize your status line](https://code.claude.com/docs/en/statusline)
- [Hooks](https://code.claude.com/docs/en/hooks)
- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
- [Checkpointing](https://code.claude.com/docs/en/checkpointing)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Agent Teams](https://code.claude.com/docs/en/agent-teams)

### 影片摘要（延伸參考）

- AILABS-393《Claude Code 10 個進階技巧》— <https://www.youtube.com/watch?v=TmsH-RIHvas>
- AILABS-393《Claude Code 12 個你應該立即啟用的隱藏設定》— <https://www.youtube.com/watch?v=pDoBe4qbFPE>
- Chase H AI《31 分鐘學會 Claude Code 核心概念》— <https://www.youtube.com/watch?v=TwkdDcO4vWQ>