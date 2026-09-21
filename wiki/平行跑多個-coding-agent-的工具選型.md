---
title: 平行跑多個 coding agent 的工具選型
description: Herdr、Multica 以外本機平行跑 coding agent 的四類方案，逐項標各 agent 與 Linux 的支援度、維護狀態
created: 2026-09-15
updated: 2026-09-21
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - coding-agent
  - agent-framework
---

本頁回答：除了 [[Herdr-使用方法]]（終端多工）與 [[Multica-與-agent-看板的用法與適用邊界]]（看板派工），**在本機平行跑多個 coding agent** 還有哪些方案。選型條件以使用者環境為準：Claude Code、Codex CLI、Antigravity CLI（`agy`）三者並用，平台 Linux／WSL2。

證據來源分三層，強度逐條就地標：
- **一手**：官方文件、GitHub repo 與 API、原始碼，經 deep-research 3 票對抗驗證（2026-09-15）。
- **廠商比較文**：augmentcode、codeagentswarm、parallelcode、nimbalyst 相關作者都在賣同類產品，**排名與定位描述不可直接引用**，只採能回查 GitHub／官方文件的事實。
- **主 agent 補查**：研究 harness 驗證名額用完，「第一手使用心得」與「值不值得」兩面向零條通過，由主 agent 以 HN Algolia API、arXiv 摘要、原文回讀補上。

星數、commit 日期、價格、preview／實驗性狀態都是 2026-09 的快照，變動快，引用前回查。

## 四類方案總表

| 方案 | 類型 | Claude Code | Codex | agy | Linux／WSL2 | 維護 |
|---|---|---|---|---|---|---|
| Claude Code 內建 | harness 內建 | 原生 | ✗（worker 皆為 Claude） | ✗ | ✓ | 官方；agent view 為 research preview、agent teams 實驗性 |
| [Claude Squad](https://github.com/smtg-ai/claude-squad) | 終端 TUI（tmux＋worktree） | 預設 | `-p` 啟動 | 推測可用 `-p`，未驗證 | ✓（有 Linux binary；原生 Windows 跑不起來） | 活躍，AGPL-3.0 |
| [Emdash](https://github.com/generalaction/emdash) | GUI app | ✓ | ✓ | ✓（原始碼有 `antigravity` provider） | ✓（AppImage／DEB／RPM） | 活躍，Apache-2.0，YC W26 |
| [Nimbalyst](https://github.com/nimbalyst/nimbalyst) | GUI workspace | 正式 | 正式 | 未提 | ✓（.deb／AppImage） | 活躍，MIT；承接已棄用的 Crystal |
| [Conductor](https://www.conductor.build/docs/installation) | GUI app（閉源） | ✓ | ✓ | ✗ | ✗ 僅 macOS | 活躍，但 Linux 使用者不能用 |

**對本環境的結論**：三種 agent 都要原生支援又要 Linux 版，查到的唯一選項是 **Emdash**（一手原始碼證實，WSL2 實際表現未測）。偏終端、想貼近 herdr 手感的是 **Claude Squad**，agy 支援屬推論。

## 一、Claude Code 內建（一手，3-0）

依[官方文件](https://code.claude.com/docs/en/agents)，有四種平行方式：

- **subagents**：結果摘要回主 context；每個 subagent 可選擇各開一個 worktree。
- **agent view**（`claude agents`，research preview）：在單一畫面派工並監看背景 session，session 動手改檔前自動移進自己的 worktree。
- **agent teams**（實驗性、預設關閉，需 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`）：lead 管共享 task list，teammate 互傳訊息。**不做 worktree 隔離**，官方要求自行切分各人負責的檔案。
- **dynamic workflows**：用腳本編排多個 subagent 並交叉比對。

**worker 限制（主 agent 補查）**：[agent teams 文件](https://code.claude.com/docs/en/agent-teams)寫明每個 teammate 是「a full, independent Claude Code session」。deep-research 以 0-3 否決了「非 Claude agent 只能經 MCP 接入」這條，否決點應在「只能經 MCP」過強（Claude session 本就能經 shell 呼叫 `codex`、`agy`），**「原生 worker 都是 Claude」這一半文件支持**。要混派 Codex／agy，仍得靠外部工具或 shell 委派（如 [[Herdr-使用方法]] 的 `agent start／prompt`）。

## 二、Claude Squad：終端 TUI（一手，3-0）

- tmux＋git worktree 架構，需 tmux 與 `gh`；約 8.5k 星，未封存，最後 commit 2026-08-20。
- 有 Linux amd64／arm64 binary，WSL2 可用。Windows 雖有 binary，issue #275 回報 creack/pty 在原生 Windows 跑不起來。
- Claude Code 是預設；Codex、Gemini CLI、Aider 用 `-p <program>` 啟動。OpenCode、Amp 也只是通用 `-p`。README 沒提 agy。
- `--autoyes` 仍實驗性，只涵蓋 Claude Code 與 Aider。無共享記憶或 agent 間通訊。
- 與 herdr 的差異在「每個 session 自動開 worktree」是預設流程；herdr 的 worktree 是另下指令。

## 三、跨平台 GUI app（一手，3-0）

**Emdash**：開源平行 agent 開發環境，約 5.7k 星、2026-09-14 仍有 push。provider 約 37 個是固定清單（「支援任何 provider」是行銷用語），`packages/plugins/src/agents/impl/antigravity/index.ts` 證實原生支援 agy。

**Nimbalyst**：範圍比 Crystal 廣的視覺化 workspace，不只是改名。macOS／Windows／Linux，另有 iOS／Android companion（只能監看與回覆）。約 1.7k 星。Claude Code、Codex 正式；OpenCode、Copilot alpha；有 Gemini provider 但未提 agy。個人免費，Teams $20／人／月（beta）。「local-first」是廠商自述。

**Crystal 已棄用**：`stravu/crystal` 2026-02 宣告由 Nimbalyst 取代，最後 push 2026-02-26。**勿再當現役工具引用**（「Crystal 是讓 Codex、Claude Code 平行跑的 GUI app」0-3 否決，否決點在時態）。

## 四、僅限 macOS 或已停用

- **Conductor**（Melty Labs，YC S24）：[安裝文件](https://www.conductor.build/docs/installation)明寫「not available for Windows or Linux yet」。支援 Claude Code、Codex、Cursor、OpenCode 四種 harness。Free 只有 Mac 本機平行 workspace；Cloud workspace、協作、API、mobile 要 Pro $50／月或 Teams $60／人／月。「閉源」依據是找不到公開 repo，官方沒明講。
- **Terragon**：已停止服務（官網標題「Terragon Shutdown」）。
- **Vibe Kanban**（約 28k 星）、**opcode**（約 22.4k 星）：高星但活動停滯；opcode 最後 commit 2025-10-16，Vibe Kanban 已宣告 sunsetting。
- 單一廠商快照（CodeAgentSwarm 2026-08-31，自揭利益衝突，數據經 GitHub API 核實）：T3 Code、Superset、Pane、Paseo 在 2026-08 下旬仍有 commit。**這幾個工具對三種 agent 與 Linux 的支援度沒有可靠結論**——同文相關主張 0-3 否決。

## 值不值得平行跑：第一手經驗（主 agent 補查）

deep-research 這兩面向零條通過驗證，以下由主 agent 回原文核對，**全為個人經驗或單一資料集，非效益實證**。

**Simon Willison〈[Embracing the parallel coding agent lifestyle](https://simonw.substack.com/p/embracing-the-parallel-coding-agent)〉**（2025-10-05，單一作者經驗）：原本懷疑，理由是**review 速度才是瓶頸**，多開只會落後更多。後來改觀，但只把平行用在四類「不增加主要工作認知負擔」的任務：研究／POC、「這段系統怎麼運作」的解說、低風險維護（如修 deprecation warning）、**已由自己寫好詳細規格**的實作——規格是自己定的，review 成本才低。他本人當時沒用 worktree，改用 `/tmp` 另 checkout；風險高的任務丟 Codex Cloud 非同步跑。這與 [[AI-產碼加速下的-review-瓶頸]] 的主張一致。

**HN〈[Ask HN: Is it actually possible to run multiple coding sessions in parallel?](https://news.ycombinator.com/item?id=47573483)〉**（2026-03-30，11 分、15 則留言，經 Algolia API 核對原句；樣本小、自我選擇）：
- 正面：worktree 平行 5–10 個可行，前提是任務原子化、盡快合併，「掛著的 worktree 太多會變惡夢」（rox_kd）；Superpowers 先規劃＋worktree 執行效果好，但 Claude Code 會忘記自己在哪個目錄（nathan_douglas）；3 個 worktree 各做一區，先寫帶驗收條件的 ticket（dontwannahearit）；模型變慢反而讓 worktree 更必要（nojs，用 workmux）。
- 保留：會同時開 Claude 與 Codex，但**很少讓它們做真正不同的任務**，大 bug 得先完成測試合併（kevinsync）；靠前後端 hot-reload 看結果時，worktree 的依賴與 port 處理太麻煩，改在 main 上切開範圍（sprobertson）；有人追問「5+ agent 各自在做什麼」未見具體回答（ex-aws-dude）。
- 共通前提：**先規劃再並行**，把人的介入壓到回答簡單問題（the_robvb）。

**合併衝突的量化訊號**：[AgenticFlict](https://arxiv.org/abs/2604.03551)（arXiv 2604.03551，2026-04，~~preprint 未同儕審查~~ **已被取代（2026-09-16）**：arXiv 頁註明已獲 AIware 2026 接受、有 ACM DOI，屬同儕審查）模擬合併 107K+ 個 AI agent PR，textual merge conflict 率 27.67%，且各 agent 差異明顯。注意這是 GitHub 上 agent PR 與目標分支的衝突，**不是**本機多 agent 互相衝突的量測，只能當「agent 產出整合成本不低」的旁證。跨 agent 與同 agent 的衝突率對比、切分與合併做法見 [[平行-agent-產出的合併與-review]]。

綜合判準與 [[Context-優先與多-agent-的適用邊界]] 一致：平行的收益落在**讀重、可切割、規格先定**的任務；寫重、需一致決策、互相依賴的改動，瓶頸在人的 review 與合併，多開不會變快。

## 勿引用

- 「Conductor 只支援 Claude Code 與 Codex」「Conductor 目前免費、之後才收費」——已過時，0-3 否決。
- 「Superset 支援 Antigravity 與 Codex、Linux 版為實驗性 AppImage；T3 Code 無 Antigravity；CodeAgentSwarm 支援 agy 但無 Linux 版」——整條 0-3 否決，不代表反面為真，只是無可靠結論。
- 「Crystal 是現役 GUI app」——已棄用。
- 廠商比較文的排名與「最佳」評價。

## 未解問題

- Emdash、Nimbalyst、Claude Squad 在 WSL2 上實際表現（GUI 經 WSLg、worktree 放 `/mnt` 的效能、agy 登入流程）——無人實測。
- uzi、Sculptor、Codex cloud 平行任務、tmux 腳本做法——本輪無主張通過驗證，狀態不明。
- 平行跑多 agent 的產出效益（token 成本、注意力切換）量化證據——目前只有個人經驗。

## 交叉引用

- 終端層對照：[[Herdr-使用方法]]——herdr 以 agent 狀態偵測為核心，Claude Squad 以預設 worktree 流程為核心；兩者都能經通用指令跑 Codex／agy。
- 看板層對照：[[Multica-與-agent-看板的用法與適用邊界]]——該頁附的 Vibe Kanban 已 sunsetting，本頁的 GUI app 類是看板以外的另一條視覺化路線。
- 判準上游：[[Context-優先與多-agent-的適用邊界]]——「讀重可平行、寫重慎用」的適用域劃分，本頁第一手經驗是它在本機工具層的印證。
- 瓶頸：[[AI-產碼加速下的-review-瓶頸]]——Simon Willison 懷疑平行的理由正是 review 瓶頸。
- 下游：[[平行-agent-產出的合併與-review]]——本頁選完工具之後，多份產出怎麼合併、review、挑選的實證與做法。
- 額度：[[LLM-方案定價與-coding-agent-比較]]——三家混用的動機與 agy 生態「被派工為主」的分布。
