---
title: Multica 與 agent 看板的用法與適用邊界
description: Multica 看板的執行模型、動作語意與 Squad 注入範圍，對照多 agent 分工與跨模型互審的實證，給出續用判準
created: 2026-09-15
updated: 2026-09-15
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - coding-agent
  - agent-framework
---

[Multica](https://github.com/multica-ai/multica) 是開源的 AI agent 協作看板：server（看板、issue、帳號）可用官方 Cloud 或自架，agent daemon 跑在放程式碼的機器上，替每個 run 啟動 Claude Code、Codex、OpenCode 等 coding agent CLI。本頁回答三件事：**看板上的操作實際會觸發什麼**、**Squad 多角色分工拿到的是什麼**、**這種看板式多 agent 流程值不值得用**。

證據來源分三層，強度逐條就地標：
- **一手原始碼與官方文件**：2026-09-15 讀 `multica-ai/multica` main 分支（commit `20f20d6`）與 `multica-ai/multica-cli`。
- **學術與廠商文獻**：經 deep-research 3 票對抗驗證。
- **研究 harness 截斷後沒送驗的主張**：由主 agent 回一手來源補查。

Multica 迭代很快（patch 版常以數天為週期發佈），下文機制描述以讀取日為準，確切切換版本請查 [releases](https://github.com/multica-ai/multica/releases)。

## 執行模型：agent 是身分，不是常駐程序

- **agent＝可重複使用的身分與設定**。官方 `/docs/agents` 原句：「An agent is not a continuously running process. It is a reusable identity and configuration; it only produces concrete runs when work arrives.」每次工作進來才產生一個 run，也就是一次 headless CLI 呼叫。（強度：一手官方文件）
- **脈絡靠 issue 傳遞，不靠共享對話**。官方宣傳的「Share all context」是指討論、紀錄、產出在工作區內全隊可見；文件沒說不同 agent 的 run 共享對話脈絡。multica-cli 的操作指南也建議把跨 run 的延續資訊（`pr_url`、`waiting_on` 等）寫進 issue metadata 供後續 run 重讀。已知例外有兩個：同一 agent 的重試在條件允許時會 `--resume` 前一個 session；回覆 agent 的留言會餵進它後續的 run。（強度：多頁一手文件互相一致；run 的 prompt 實際帶入多少留言沒逐行追）
- **每個 run 都注入平台 brief**。Claude run 不走 `--append-system-prompt`，daemon 會在 workdir 寫一份 `CLAUDE.md` 讓 Claude Code 自行載入（`server/pkg/agent/claude.go` 註解，MUL-5392）。社群在 [#4358](https://github.com/multica-ai/multica/issues/4358) 量過 brief 大小：64 個 workdir 中位數約 23.4KB，其中約 62% 是每個 task 都一樣的平台樣板；後續實作把它壓到約 13.6KB（−36%）。（強度：社群自行量測、非官方數據，但量測方法有公開；大小會隨版本變動）

這個模型直接決定了多角色分工的上限：Lead／Planner／Builder／Reviewer 之間的「交接」，本質是**一串互不共享 context 的獨立 run，靠 issue 留言串起來**。這正是 Cognition 在 [Don't Build Multi-Agents](https://cognition.com/blog/dont-build-multi-agents) 裡點名的第一原則的反面：可靠 agent 要共享完整 trace，不能只傳個別訊息（見 [[Context-優先與多-agent-的適用邊界]]）。

## 看板操作都是動作，不只是標記

multica-cli 的 `SKILL.md` 原文：「Status changes are not cosmetic」「Mention links are actions, not decoration」。（強度：官方 org 的操作指南，主 repo 的 `assigning-issues.mdx` 也有同樣的 `--no-start` 範例；原文用 can enqueue，是「可能」觸發）

| 操作 | 實際效果 |
|---|---|
| 指派 agent 為 assignee | run 排入佇列就開始 |
| 在留言 @agent | 排入該 agent 的 run，**不改 assignee**（`/docs/agents` 原句 "without changing the issue's assignee"） |
| @squad | 排入 squad leader 的 run |
| @member（人） | 只通知 |
| `issue status`／`assign`／`update` | 預設可能排入新 run，例如 `backlog`→`todo` 會喚醒被指派者；只想記錄要加 `--no-start` |
| 移到 `backlog` | 暫停已指派給 agent 的 issue（parks） |
| 在回覆裡重複 @agent | 可能再觸發一個 run，形成迴圈並多花錢 |

agent 另外沒有 inbox，也收不到 `@all`；對 agent 的 @mention 是執行觸發，不是通知。

**狀態模型**：內建 7 個狀態 `backlog | todo | in_progress | in_review | done | blocked | cancelled`，見 `SKILL.md` 與 `server/migrations/001_init.up.sql` 的 CHECK 約束。後來改成每個 workspace 可自訂狀態：每個自訂狀態對應 7 個 canonical category 之一，看板依 category 分欄，狀態目錄也會注入 agent brief（release notes #7065、#7306）。自訂狀態**不繼承**內建 In Review 的行為。（強度：一手原始碼與 release notes；看板實際 UX 沒親眼看過）

**人類把關點在 `in_review`**：agent 交付時自己把 issue 移到 `in_review`，不會移到 `done`。README 原句：「nothing ships without a human saying so」。（強度：一手官方文件）

## Squad：Squad Instructions 只到 leader

依官方文件，Multica 先喚醒 leader，leader 再用 @mention 把工作交給成員，每個被 mention 的成員各自觸發一次新 run。

**原始碼顯示 Squad Instructions 只注入 leader**（強度：一手原始碼，2026-09-15 main）：
- `server/internal/handler/squad_briefing.go` 的 `buildSquadLeaderBriefing` 會在 **leader 的** Instructions 後面附上三段：Squad Operating Protocol（系統規則）、Squad Roster（成員名單與可直接貼上的 mention 字串）、使用者寫的 Squad Instructions。
- 全 repo 只有 `daemon.go` 在 leader 認領任務的路徑呼叫它，沒有對應成員的注入點。
- leader 身分由結構化欄位判定，不從 Instructions 文字推斷（`execenv.go` 註解，MUL-5811）。

**實務含意**（推論）：寫在 Squad Instructions 的團隊規則（例如「任何成員都不得合併 PR」「不得移到 done」）**只直接約束 leader**。成員 run 只看到自己的 agent Instructions 加上 leader 在留言裡轉述的內容。要讓成員遵守的邊界，必須寫進各成員自己的 agent Instructions。

## Claude run 的啟動參數

`server/pkg/agent/claude.go` 的 `buildClaudeArgs`（強度：一手原始碼）：

- 固定帶 `-p`、`stream-json` 輸入輸出、`--verbose`、`--permission-mode bypassPermissions`。
- **`--disallowedTools` 只禁 `AskUserQuestion`**：headless 模式沒有 UI 可以回答，問了會拿到空答案、agent 默默自己推斷（#2588），所以要澄清的事一律改寫成 issue 留言。**Agent（subagent）工具沒被禁**，Claude run 可以自己起 subagent。
- 有 agent 層級的 `mcp_config` 時才加 `--strict-mcp-config`；沒有就繼承本機 runtime 的 MCP。早期版本（[#1111](https://github.com/multica-ai/multica/issues/1111)，2026-04）只加 strict 沒傳 `--mcp-config`，子 agent 的 MCP 是零，維護者確認後改成每個 agent 各自設 `mcp_config`。
- `-p`、`--output-format`、`--input-format`、`--permission-mode`、`--mcp-config`、`--effort` 列在 `claudeBlockedArgs`，使用者的 `custom_args` 蓋不掉。

## Project resource：local_directory 是逃生口

官方 `project-resources.mdx`（強度：一手官方文件）：

- **`github_repo`** 預設 worktree 模式，同一 repo 可以無上限併發。
- **`local_directory`** 官方原話是「an escape hatch, not a more convenient default」，給無法重新 clone 的情境用，例如幾十 GB 的遊戲專案。預設 `in_place`：agent 直接改你目前的分支與未提交檔案，而且一次只跑一個 run，後到的進 `waiting_local_directory`。
- **`local_directory` + `worktree`**：每個 run 在 runtime 自己的目錄開一個 git worktree，未提交的修改會先重放進去，成果留在 `agent/<agent>/<issue>` 分支（一個 issue 一條，不是一個 run 一條）。同一 issue 的後續留言會接續這條分支，Multica 永遠不幫你合併。沒產生任何變更的 run 會刪掉自己的分支。這個模式靠 runtime 宣告 capability 開啟，不看版本號（release v0.4.25、2026-08-13、#6904）。

## 續用判準：證據怎麼說

沒有任何研究直接測過 Multica 或「看板式 headless 多 agent 流程」，以下都是**間接證據**，遷移到長時程 repo／PR 流程時要打折。

- **多角色分工的提升往往很小**。MAST（[arXiv 2503.13657](https://arxiv.org/abs/2503.13657)）的作者指出，多 agent 系統在熱門 benchmark 上的提升 often minimal；失敗歸成 3 大類，其中一類是 inter-agent misalignment。把它對應到「交接失真」是解讀，不是原文用語。完整失敗率與強度見 [[Context-優先與多-agent-的適用邊界]]。
- **同模型下，單一 agent 輪流扮演各角色，成本低很多、表現相當**。出處是〈Rethinking the Value of Multi-Agent Workflow〉（[arXiv 2601.12307](https://arxiv.org/pdf/2601.12307)），省成本主因是 KV cache 重用。前導研究中，異質 workflow（GPT-4o-mini 混 Claude 3.5 Haiku）大致沒超過最佳同質 workflow，但在 MATH、HotpotQA 上異質版略勝。（強度：單篇 preprint；閉源模型的 cache 成本是模擬值；題目是短題 benchmark、模型偏小偏舊；KV cache 論點只適用同模型，不適用跨模型商混用）
- **Anthropic 的 90.2% 有適用域**。多 agent 研究系統比單一 Opus 4 高 90.2%，但同一篇文章也說：多 agent 約用一般聊天 15 倍的 token；token 用量本身就解釋 BrowseComp 表現差異的 80%；「most coding tasks involve fewer truly parallelizable tasks than research」。（強度：一手廠商文章，原句已回查；內部評測、研究型任務）
- **跨模型商互審有方向性，不能一律當加分**。〈Cross-Model LLM Code Review〉（[arXiv 2607.21656](https://arxiv.org/abs/2607.21656)），116 題 LiveCodeBench：
  - Claude 審 Codex：pass rate 71.6%→89.7%（Codex 自審只到 84.5%）。
  - Codex 審 Claude：91.4%→82.8%，反而變差（Claude 自審維持 91.4%）。

  作者結論是「use Claude to review Codex, not the other way around」。（強度：單篇 workshop 等級、Agentic SE @ KDD'26，樣本小；題目是競賽題而非 repo 層級 PR；審查者不能跑測試；有害方向 p=.046 勉強過門檻；結果綁定當時模型版本）
- **收益可能來自「乾淨 context」，不是換模型商**。Cognition 在 [Multi-Agents: What's Actually Working](https://cognition.com/blog/multi-agents-working) 自報：Devin Review 即使審 Devin 自己寫的 PR，平均每個 PR 也抓到 2 個 bug、約 58% 屬嚴重。作者把效果歸因於 reviewer 的 context 完全乾淨，並主張同模型只要 context 不同，就不會有「同一個人自己審自己」式的偏誤。同文也說多 agent 可行的形狀是 map-reduce-and-manage，且寫入要保持單執行緒。（強度：廠商自報、無對照組、方法未公開；原句已回查）
- **同模型自審偏誤的證據好壞參半**。摘要任務上，GPT-4 的自我偏好超出人評的實際品質差距（Panickssery 等，NeurIPS 2024）。有客觀正解的任務上，較強模型的自我偏好多半有道理，但自己答錯時，有害的自我偏好更明顯（[arXiv 2504.03846](https://arxiv.org/html/2504.03846v2)）。兩篇都沒測 Claude/Codex，也不是 agent code review 情境。

**綜合判準**（推論，非實證）：看板式多 agent 流程的價值不在「多個 agent 協作」，因為它們結構上不共享 context。價值在三件事：①把人類把關點（`in_review`、手動合併）制度化；②issue 當非同步工作佇列與稽核紀錄；③每個 run 自帶乾淨 context，天然適合 generator-verifier 迴圈。如果這三件事你不需要，單一強模型自帶 subagent（Multica 的 Claude run 本身也沒禁 subagent）就能拿到 Planner／Reviewer 的大部分收益，而且少掉以下成本：
- 交接失真
- leader 挑人出錯
- 各家額度平衡
- @mention 喚醒的 token 開銷，以及迴圈風險

要做跨模型商互審，現有唯一的直接證據指向「強模型審弱模型」。

## 同類工具的模式對照

研究 harness 的驗證名額用完，本節沒經過 3 票驗證，主 agent 回一手來源補查了其中幾條。

| 工具 | 喚醒方式 | 隔離方式 | 人類把關點 | 現況 |
|---|---|---|---|---|
| Multica | 指派／@mention／狀態變更 | `github_repo` worktree；`local_directory` 預設 in_place | `in_review` → 人工合併 | 活躍 |
| [Vibe Kanban](https://github.com/BloopAI/vibe-kanban) | 看板 issue → 建 workspace | 每個 workspace 給 agent 一條分支、一個 terminal、一個 dev server | UI 內看 diff、行內評論 → 開 PR | **README 首行宣告 sunsetting**（2026-09-15 回查，repo 未封存） |
| [GitHub Copilot cloud agent](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent) | 指派 issue 給 Copilot、PR 留言 @copilot | GitHub Actions 的暫時性環境（雲端，非本機 worktree） | PR review／merge | 一個 task 只開一個 PR、一次只在一條分支工作、每個 session 最長 59 分鐘硬上限；branch protection 不相容時要把 Copilot 加為 bypass actor（官方文件原句已回查） |
| Kagan（OpenCode 外掛）、briefboard | Backlog → In Progress → Review → Done | 各自 worktree 的專屬分支 | 執行前 intake＋合併前 review | 個位數到十幾星的個人專案，**未回查**，只當模式參考 |

共通模式：**一個 task 對應一條隔離分支，合併權永遠留在人手上**。Multica 與 Copilot 都把「指派＝喚醒」做成核心互動，Vibe Kanban 則是先建 workspace 再跑 agent。

## 勿引用與翻案紀錄

- **deep-research 否決、回查後成立的 4 條**（2026-09-15）：①「@agent 喚醒不改 assignee」（1-2 否決）、②「worktree 模式以 capability 開啟、不看版本號」（0-3）、③「內建 7 狀態與 backlog parks 語意」（0-3），這三條都已在上文引用一手原句或原始碼成立；④「同質 workflow 單一 agent 準確度相當」核心成立，只是列舉的 benchmark 數量寫錯（寫 7 個、列了 8 個），**那份列舉勿引用**。又一次印證對抗驗證會被周邊細節連坐而過度否決。
- **勿引用**：Vibe Kanban「讓 coding agent 產出提升 10 倍」，屬行銷文案、無數據。
- **勿引用**：MindStudio 部落格「跨模型互審比同模型自審抓到更多 bug」，無 benchmark，作者同時在推銷自家多模型平台。
- **時效存疑、勿直接引用**：[#2563](https://github.com/multica-ai/multica/issues/2563) 說「`claude -p` 用量自 2026-06-15 起移出 Pro/Max 訂閱」，後續留言指 Anthropic 已暫緩。訂閱與第三方工具的現況見 [[LLM-方案定價與-coding-agent-比較]]。
- **未查證**：自架使用者回報 squad 依序跑大量 issue 時 token 消耗很大（[#4349](https://github.com/multica-ai/multica/issues/4349)），沒附數字，issue 內也沒有與單一 agent `/loop` 的對照數據。

## 未解問題

- run 的 prompt 實際帶入多少留言串（全文或摘要），這決定交接失真的程度。沒逐行追。
- 沒有針對長時程、repo 層級 PR 流程的實證，比較看板式多角色與單一強模型自帶 subagent 的品質與 token 成本。

## 交叉引用

- 判準上游：[[Context-優先與多-agent-的適用邊界]]——本頁是該頁「寫重、需決策一致的 coding 落在多 agent 雷區」判準在一個具體看板工具上的應用，並補上跨模型互審的方向性證據。
- 模式清單：[[Agent-工作流-Pattern-藍本庫]]——Squad 的 leader 分派是 orchestrator-workers，Builder／Reviewer 往返是 evaluator-optimizer；該頁的「單 agent 優先」選用 gate 適用於是否要開 Squad。
- 審查瓶頸：[[AI-產碼加速下的-review-瓶頸]]——`in_review` 人工合併這個把關點，正是該頁說 AI 產碼加速後會積壓的位置。
- 同類判斷：[[pi-workflow-編排-harness-與本-vault-分野]]——同樣評估「要不要引入一整套編排機制」，結論方向一致。
- 成本與額度：[[LLM-方案定價與-coding-agent-比較]]——混用多家模型商的動機（額度平衡）與各家訂閱能否給第三方 harness 用。
- 替代方案：[[平行跑多個-coding-agent-的工具選型]]——看板以外的本機平行方案（終端 TUI、GUI app、Claude Code 內建）與其 agent／平台支援度。
- 同步對照：[[Herdr-使用方法]]——herdr 是終端層的常駐 agent 多工，人類即時盯狀態插手；與本頁非同步看板、run 結束即走的模型互為兩端。
