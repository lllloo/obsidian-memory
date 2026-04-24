---
title: Claude Code 效率技巧與設定
created: 2026-04-24
updated: 2026-04-24
tags:
  - claude-code
  - workflow
  - cli
  - moc
---

> Claude Code 日常操作技巧的 hub MOC。整合七篇影片摘要，聚焦可重用的日常 patterns。深度內容拆分為以下 Card，本 MOC 保留日常指令、Hooks、多 Agent 概覽、跨主題情境速查。

## 延伸 Card

- [[Claude-Code-開工前-SOP]] — Plan → PRD → 文件四件組 → CLAUDE.md → Skills/Agents/MCP → negative constraints → progress/learnings → test-first 完整 SOP
- [[Claude-Code-CLI-工具生態]] — 為何 CLI 優於 MCP、工具分類速查、讓 agent 看 runtime、部署流程、進階技巧

## 章節地圖

1. [日常指令技巧](#日常指令技巧) — `/insights`、`/btw`、`/hook`、`/status line`、Ctrl+S
2. [Hooks 與 exit code](#hooks-與-exit-code) — pre-tool-use 守門與 RALF loop 基礎
3. [多 Agent 協作概覽](#多-agent-協作概覽) — Sub-agent / Agent Teams / Fork 差異、worktree、強化開源專案
4. [入門光譜](#入門光譜) — IDE / Terminal / 權限三層 / Obsidian 整合
5. [速查：情境對照技巧](#速查情境對照技巧) — 跨 Card 的索引表

## 日常指令技巧

### `/insights` — 工作習慣分析

分析過去所有 sessions 產報告：最常出問題的地方、可改善的 workflow 功能。把報告中的 tips 複製進 `CLAUDE.md` 供未來使用。

### `/btw`（by the way）— 側邊對話

長任務進行時開側邊對話（官方已文件化）：

- 看得到完整主 session context，但**沒有 tool access**
- 回答**不會進主 conversation history**，用完即丟
- 適合查詢、確認名詞、問旁支問題——比 spawn subagent 更輕量

### `/hook` — 完成聲音

任務完成時播提示音。多視窗並行時避免忘記查看結果，每週可省數小時。語音包可選（`Peon Ping` 等 skill 提供遊戲角色語音）。

### `/status line` — 常駐狀態列

在 prompt 欄下方顯示常駐資訊：當前目錄、使用模型、context window 用量百分比。指定項目即可建立。**建議常駐 context %，避免憑感覺判斷該不該 `/clear`**。

### `Ctrl+S` — Prompt Stashing

正在輸入 prompt 時，若需先送另一個任務：`Ctrl+S` 暫存目前 prompt。送完新任務後，暫存的 prompt 自動回到輸入框。

### 更多 session 層指令

`/clear` / `/compact` / `/rewind` 及 context rot 的應用準則見 [[Context-Engineering]]。

## Hooks 與 exit code

Hooks 在 Claude Code lifecycle 特定時間點執行 shell 指令。**Exit code 是 hook 與 Claude 互動的唯一介面**。

| Exit code | 行為 |
|---|---|
| `0` | 成功；stdout 通常只進 debug log（例外：`UserPromptSubmit` / `UserPromptExpansion` / `SessionStart` 的 stdout 會進 context 讓 Claude 看到）；若用 JSON 輸出協議，**只在 exit 0 時處理** |
| `2` | **阻斷**：忽略 stdout，**stderr 作為錯誤訊息回饋給 Claude**；對 `PreToolUse` 是阻斷 tool call、對 `UserPromptSubmit` 是阻斷 prompt 並清空輸入、對 `Stop` 是阻止 Claude 停止（完整事件清單見官方 Hooks 文件，另 `SubagentStop` / `TaskCompleted` / `PreCompact` 等也支援阻斷） |
| 其他非 0 | **大多數事件視為 non-blocking**：transcript 顯示 `<hook name> hook error` 與 stderr 首行，但動作仍繼續 |

**重要提醒**：Claude Code 把 **exit 1**（傳統 Unix 失敗碼）當 non-blocking 處理。若 hook 意圖強制執行某政策，**必須用 `exit 2`**，不要依賴 exit 1。唯一例外是 `WorktreeCreate` 事件——該事件下任何非 0 都會中止 worktree 建立。

### 常用 pattern

**TDD 保護（pre-tool-use）** — 阻止 Claude 修改測試檔：

```bash
# 若 tool 路徑包含 test 目錄或 test 關鍵字 → exit 2
```

**強制套件管理器一致性（pre-bash）** — 攔截 pip，導向 uv：

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
if echo "$COMMAND" | grep -q "pip install"; then
  echo "請使用 uv 而非 pip 安裝套件" >&2
  exit 2
fi
```

**過濾測試輸出** — 只把失敗的測試注入 context，通過的略過。細節見 [[Context-Engineering]] 的 Hooks 段。

## 多 Agent 協作概覽

### Sub-agent vs Agent Teams vs Fork

| | Sub-agent | Agent Teams | Fork（實驗功能） |
|---|---|---|---|
| Context | 獨立 context；載入專案 CLAUDE.md/MCP/skills，不繼承 parent 對話 | 獨立 context；同 subagent 載入規則，但多了 shared task list 與 mailbox | **繼承主 session 完整對話** |
| 跨成員溝通 | 只把結果回報主 session（不與其他 subagent 直接通訊） | member 之間可互相溝通（單一 session 內） | 只有最終結果回主 session |
| 系統提示 | subagent 定義的 body 即 system prompt | 預設 system prompt +（若引用 subagent 定義）body 附加為額外指示 | 與主 session 相同 |
| 啟動 | 自動或 `--agent` | `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` | `CLAUDE_CODE_FORK_SUBAGENT=1` + `/fork` |
| 適用 | 單一隔離任務、大量輸出隔離 | 跨 session 協調、長期並行 | 主 session 做到一半想開支線、不想重新解釋脈絡 |
| 限制 | **無法 spawn 其他 subagent** | — | 只在互動 session 可用，fork 不能再 fork |

> teammate 的 skills/MCP 一律讀專案與 user settings，不吃 subagent frontmatter 的 `skills` / `mcpServers`。

### Git worktrees 平行 Agent

branches 共用 working directory 會造成衝突，改用 worktrees：每個 agent 有獨立 working tree，完成後 merge。也可在 subagent frontmatter 設 `isolation: worktree` 自動套用——**subagent 未改動檔案時 worktree 會自動清除**。

### Adversarial 對抗式協作

兩個 agent 分工對抗：

- Research + Fact checker
- Implementer + Reviewer

fact checker 阻止錯誤資訊流出；reviewer 阻止偏離規格的實作。**這類模式的深入設計見 [[Agent-Harness]] 與 [[GAN-Style-Harness]]**。

### 強化開源專案

影片提及的專案（repo URL 請在使用時以工具名搜尋最新位置，避免引用失效）：

| 專案 | 用途 | 適用場景 |
|---|---|---|
| AutoResearch（Karpathy） | 自動實驗迴圈 | 有二元評分的任務：Python 優化、Prompt 優化、skill pass/fail；不適合創意、主觀任務 |
| OpenSpace（HKUST） | 技能品質監控 | MCP 自動把 skill 分入 autofix / autoimprove / autolearn 三桶 |
| CLI Anything（HKUST） | Meta 工具 | 把任何開源專案轉為 Claude Code 可用的 CLI |
| Claude Peers | 多 session 通訊 | MCP + SQLite 讓 sessions 互通，配合 harness 做 generator/evaluator 對話 |
| Google Workspace CLI（GWS） | Google 套件整合 | Gmail / Docs / Sheets / Drive；可沙箱化、內建 Model Armor prompt injection 防護 |

## 入門光譜

### IDE / Terminal 光譜（從多控制到少控制）

| 使用方式 | 控制度 | 備註 |
|---|---|---|
| Terminal | 最多 | 完整功能 |
| IDE 內建 Terminal（VS Code / Cursor） | 高 | Terminal + 檔案管理視覺化 |
| Claude Code 桌面應用 | 中 | |
| Co-work / Web | 最少 | 流暢但功能受限 |

95% 使用情境下各方式效果相近。VS Code 常用法：``Ctrl+` `` 開 terminal，`cd` 到專案後 `claude` 啟動。

### 權限三層

`Shift+Tab` 切換：預設（每次詢問）→ Accept Edits On（檔案免詢問）→ Bypass Permissions On（完全不詢問）。

Bypass Permissions On 可在 session 內 Shift+Tab 切入，或以 `--dangerously-skip-permissions` 啟動時直接進入該模式；多數 power user 常駐 Bypass，初學者建議從 Accept Edits 開始。細節見 [[Claude-Code-Dangerously-Skip-Permissions]]。

### 與 Obsidian 整合

工作目錄設在 Obsidian vault，所有輸出以 Markdown 存入 vault。Claude Code 建立整理文件，Obsidian 提供圖形介面看連結關係。相關整合細節見 [[Topics/Obsidian/index|Obsidian]]。

## 速查：情境對照技巧

跨 Card 的情境索引——看到痛點直接跳對應 Card 的深入段落。

| 情境 | 工具 / 做法 | 深入見 |
|---|---|---|
| 開新專案、想避免 agent 跑偏 | Planner agent → PRD → 文件四件組 → negative constraints | [[Claude-Code-開工前-SOP]] |
| 多視窗並行、怕忘記查結果 | `/hook` 完成聲音 + `/status line` 常駐 context % | 本 MOC「日常指令技巧」 |
| 主任務跑到一半想問旁支 | `/btw` 側邊對話，不佔主 context | 本 MOC「日常指令技巧」 |
| 正在打字卻需先送別的任務 | `Ctrl+S` 暫存 prompt | 本 MOC「日常指令技巧」 |
| MCP 工具太多佔 context | 改用對應 CLI 工具，或把 `mcpServers` 收進 subagent frontmatter | [[Claude-Code-CLI-工具生態]] |
| 防止 agent 亂改測試檔 | pre-tool-use hook + `exit 2` | 本 MOC「Hooks 與 exit code」 |
| 強制套件管理器一致性 | pre-bash hook + `exit 2` | 本 MOC「Hooks 與 exit code」 |
| 多 agent 併行、怕互改互覆 | Git worktrees 或 sub-agent `isolation` | 本 MOC「多 Agent 協作概覽」 |
| 想要 research 有「監督者」 | Adversarial（research + fact checker） | [[Agent-Harness]] |
| 要求 agent 自行驗證實作 | 「列出這份實作中可能但尚未發生的問題」 | [[Claude-Code-CLI-工具生態]] |

## 相關主題

- [[Context-Engineering]] — `/clear`、Context Rot、CLAUDE.md 精簡原則、用量機制
- [[Claude-Code-Skills]] — Skills 運作機制、Progressive Disclosure、常見坑、社群精選 Skills 實例
- [[Agent-Harness]] — Multi-agent 拓撲、adversarial 協作、harness engineering
- [[GAN-Style-Harness]] — Adversarial harness 的具體實作
- [[Claude-Code-Dangerously-Skip-Permissions]] — Bypass 模式的旗標說明
- [[Claude-Code-雙帳號設定]] — 同機多帳號切換
- [[Claude-Code-Agent-Packages]] — 已安裝的社群 Agent Packages
- [[skill-creator-是什麼]] — 建立與優化 Skills 的工具

## 外部來源

### 影片摘要（本 MOC 整合來源）

- AILABS-393《Claude Code 10 個進階技巧》— <https://www.youtube.com/watch?v=TmsH-RIHvas>
- AILABS-393《Claude Code 12 個你應該立即啟用的隱藏設定》— <https://www.youtube.com/watch?v=pDoBe4qbFPE>
- AILABS-393《Claude Code 專案開始前的完整設置指南》— <https://www.youtube.com/watch?v=ywIhw15za9Y>
- Chase H AI《31 分鐘學會 Claude Code 核心概念》— <https://www.youtube.com/watch?v=TwkdDcO4vWQ>
- Chase H AI《九個 Claude Code 效率技巧》— <https://www.youtube.com/watch?v=XkSBO-CZDFs>
- Chase H AI《十個讓 Claude Code 如虎添翼的 CLI 工具》— <https://www.youtube.com/watch?v=uULvhQrKB_c>
- Chase H AI《五個強化 Claude Code 的開源專案》— <https://www.youtube.com/watch?v=6SnFH43qPAw>

### 官方文件（已核對）

- [Claude Code Settings](https://code.claude.com/docs/en/settings)
- [Hooks](https://code.claude.com/docs/en/hooks)
- [Create custom subagents](https://code.claude.com/docs/en/sub-agents)
- [Agent Teams](https://code.claude.com/docs/en/agent-teams)
- [Environment variables](https://code.claude.com/docs/en/env-vars)
