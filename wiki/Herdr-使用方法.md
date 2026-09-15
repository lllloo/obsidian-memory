---
title: Herdr 使用方法
description: herdr 的 session／workspace 層級、持久化邊界、agent 狀態偵測、CLI 委派原語、worktree 與 SSH 遠端用法，含偵測盲點與強度標註
created: 2026-09-15
updated: 2026-09-15
source: https://herdr.dev/docs/
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - automation
---

# Herdr 使用方法

herdr 是 client/server 架構的終端多工器，骨架與 tmux 相同：背景 server 持有 pane 裡的程序，client 只負責畫面。和 tmux 的差別在它**認得 agent**——把 pane 裡的程序辨識成 coding agent、標狀態、在側欄匯總，並開放 CLI／socket API 讓 agent 彼此開 pane、送 prompt、等對方結束。按鍵自訂另見 [[Herdr-按鍵設定]]。

**強度總註**：本頁幾乎全部出自官方 docs 與 README（2026-09-15 deep-research，12 條主張通過三票對抗查證），另以本機安裝版逐條跑 `--help` 核對指令存在。**沒有第三方實測**——狀態偵測準度、`agent wait` 阻塞穩定性都未驗證。worktree 一節是主 agent 事後補查官方 cli-reference 原始檔所得，未經對抗查證。支援的 agent 種類、integration 分類與實驗旗標會隨版本變動，確切行為以官方 [CHANGELOG](https://github.com/herdrdev/herdr/blob/master/CHANGELOG.md) 為準。repo 已由 `ogulcancelik/herdr` 轉移至 `herdrdev/herdr`（`gh api` 確認轉址）。

## 層級：session → workspace → tab → pane

| 層 | 是什麼 | 用法 |
|---|---|---|
| session | 持久的 server 命名空間，各自獨立的 pane、socket、持久化狀態 | `herdr` 接預設 session；`herdr session attach <name>` 接具名 session；`session list／stop／delete` 管理 |
| workspace | 頂層專案容器，側欄以它為單位匯總 agent 狀態 | 一個 repo、任務或調查開一個 |
| tab | workspace 內的一個版面 | 如 agents、logs、server、review 各一個 |
| pane | 真正的終端 | 向右或向下分割 |

官方建議**先用 workspace 區隔，需要完全隔離才開具名 session**。（強度：官方兩份文件一致，3-0）

## 持久化：兩層邊界要分清

**第一層，detach／斷線——程序照跑。** `ctrl+b q`（預設鍵）detach、關終端、SSH 斷線，pane 裡的 shell、agent、測試、dev server 都繼續跑，再下 `herdr` 接回。可同時開多個 client 各看不同 workspace；多個 client 看同一 tab 時，最後互動者決定 pane 尺寸。（3-0）

**第二層，server 停止或機器重啟——程序一律消失。** herdr 用 snapshot 還原 workspace、tab、pane、cwd、版面與焦點，但還原出的 pane 是在原目錄開的**新 shell**。畫面內容預設不還原（需開實驗性的 pane history 設定）。更新時要保留程序得走 `herdr update --handoff`。（3-0，session-state 頁「What survives」表）

踩雷：**更新 binary 不會替換已在跑的 server**。要吃到 server 端變更，`herdr status` 確認後 `herdr server stop` 再重開——代價是所有 pane 程序結束；具名 session 用 `herdr session stop <name>`。（官方 troubleshooting 原文，未經對抗查證）

### 原生 agent session 還原

預設開啟（`[session] resume_agents_on_restore = false` 可關）。server 重啟後，支援的 agent 用自己的 resume 指令接回對話，如 `claude --resume <id>`、`codex resume`，agy、OpenCode、Copilot、Cursor、Devin 等亦在列。接回的是**新程序、舊對話**。前提是該 pane 已透過夠新的官方 integration 回報 session reference（`herdr integration status` 檢查；版本門檻指 integration 版本，不是 agent 本身版本）；reference 缺漏或過期就還原成普通 shell。（3-0）

## agent 狀態偵測

| 狀態 | 意義 | 可接收輸入 |
|---|---|---|
| blocked | 需要輸入、核准或決定 | — |
| working | 執行中 | — |
| done | 完成但你還沒看 | 是 |
| idle | 完成或等待中且已看過 | 是 |
| unknown | 無法有把握分類——**不代表成功完成** | — |

側欄往上匯總：一個 blocked agent 會讓所屬 pane、tab、workspace 都顯示 blocked。（3-0，三份官方文件一致）

**偵測方式分兩類 integration**，這決定你裝了 integration 後得到什麼：

- **lifecycle authority 類**（Pi、OMP、Kimi、OpenCode、Kilo、MastraCode 等）：由 hook 回報狀態。
- **session identity 類**（Claude Code、Codex、Copilot、Devin、Cursor、Antigravity、Grok 等）：只回報 session 身分供還原，**狀態仍靠畫面 manifest 比對**。所以 `herdr integration install claude` 只補上原生還原，Claude 的狀態判定不會因此變準。（3-0）

**已知盲點**（官方 agents 頁，查證者轉述，中強度）：

- 只對辨識得出的 agent 有效，一般 shell pane 無意義。
- 靠畫面 manifest 的 agent，blocked 判定刻意從嚴：只有比對到已知的核准／提問／權限畫面才標 blocked，否則退回 idle——**agent 其實在等你卻不提示是可能的**。
- pane 裡再跑 tmux 時，herdr 只看到 tmux，偵測不到裡面的 agent。

排錯三件套：`herdr agent list`（偵測到哪些）、`herdr agent explain <target> --json`（為何這樣分類）、`herdr integration status`。manifest 相關：`herdr server agent-manifests`、`update-agent-manifests`（抓遠端最新）、`reload-agent-manifests`（改完本地 override 後）。

## 自動化與多 agent 委派

官方定位是 **agent-native**：agent 自己用 CLI／socket API 操作 herdr。原語分三層（3-0，本機 `--help` 核對一致）：

- **layout**：`workspace create`、`tab create`、`pane split`——管拓樸。
- **pane**：`pane run`、`pane read`、`pane send-text／send-keys`、`pane wait-output <id> --match <text>|--regex <pat>`——管 raw terminal，適合等 server 起來、測試跑完。
- **agent**：`agent start`、`agent prompt`、`agent wait`、`agent read`、`agent list`、`agent explain`——管已辨識的 agent。

### 啟動 agent

`herdr agent start <name> --kind <kind> --pane <id>` **只能在已存在、停在 shell 提示字元的 pane 裡啟動**，本身不建版面，所以流程是先 `pane split` 再 `start`。kind 涵蓋 claude、codex、gemini、agy、cursor、opencode 等二十餘種；名稱需符合 `[a-z][a-z0-9_-]{0,31}` 且存活 agent 間不重複。預設等 30 秒（`--timeout` 可調），偵測到且可接受輸入才算成功，啟動中變 blocked 立刻回 `agent_not_ready`。（3-0）

### 送 prompt 與等待

`herdr agent prompt <target> <text> [--wait] [--until STATUS]... [--timeout MS]` 是委派主指令（3-0）：

- 遵守 bracketed paste，文字與延遲送出的 Enter 視為一次提交，agent working 中也能送。
- **不加 `--wait` 時，成功只代表文字寫入**，不代表對方收到或開始做。
- `--wait` 與 `agent wait` 預設等到 idle、done、blocked 任一；要等 unknown 必須明寫 `--until unknown`；`--until` 單獨用會被拒。
- 目標已是 blocked 直接回 `agent_blocked`、不送輸入；加 `--wait` 而 5 秒內沒看到 working／blocked，回 `agent_prompt_stalled`。
- socket API 有對應的 `agent.prompt`、`agent.wait`，可訂閱 `pane.agent_status_changed` 事件（查證者轉述）。

搭配使用：`herdr notification show <title> [--body] [--sound none|done|request]` 可從腳本丟通知（本機 `--help` 核對，未經對抗查證）。

官方 agent skill 可用 `npx skills add herdrdev/herdr --skill herdr -g` 安裝或 `herdr --skill` 印出，使用 CLI 前檢查 `HERDR_ENV=1`。（3-0）本機全域的 `herdr-agent` skill 即是這套原語的應用：開新 tab 啟動另一個 agent 派工，對方用 `herdr agent prompt` 把結論打回主 pane。

## git worktree

herdr 內建 worktree 指令（官方 cli-reference 原始檔＋本機 `--help`，**未經對抗查證**）：

- `herdr worktree create [--branch NAME] [--base REF] [--path PATH]`：建 git worktree、開成 workspace，並與父 repo workspace **成組**。branch 已存在就 checkout，否則從 `--base` 或 HEAD 建新 branch；不給 `--path` 就放在 `<worktrees.directory>/<repo>/<branch-slug>`。
- `worktree open`：把既有 worktree 開成 workspace；`worktree list` 列出。
- **關閉與刪除分開**：`workspace close` 只關 herdr 狀態，不動 checkout；primary workspace 仍有連結的 worktree workspace 開著時，要加 `--group` 否則回 `workspace_group_close_required`。真正刪 checkout 用 `worktree remove`——跑 `git worktree remove`、**永不刪 branch**、dirty checkout 需 `--force`。
- 別的使用者擁有的 repo 被 git 拒絕時，`--trust-repository` 只對該次指令信任，不改 git 設定。

這是「一個 worktree 一個 workspace」的平行 agent 慣例的官方支援；多 agent 在同一 checkout 內的檔案衝突 herdr 不處理，本輪未查到官方或社群建議。

## 遠端與 SSH

三種用法（3-0，官方 persistence-remote 頁逐行核對）：

1. SSH 登入後直接在遠端跑 herdr，靠 server 持久化撐過斷線。
2. `herdr --remote workbox` 或 `herdr --remote ssh://you@server:2222`：pane 由遠端 server 持有，終端內容經 SSH 串流回來由本機繪製。
3. 儲存的 SSH machines（`herdr machine`），在同一視窗切換本機與多台遠端。

本機 client 可為 Linux、macOS、Windows；**遠端主機只能是 Linux 或 macOS**。

## 與相鄰工具的定位

- 對 [[Multica-與-agent-看板的用法與適用邊界]]（agent 判斷，非查證結論）：Multica 是非同步看板，agent 是身分、run 結束即走，人類在卡片把關點介入；herdr 是同步的終端層，agent 是常駐程序，人類即時盯側欄狀態。前者適合佇列化派工，後者適合同時跑幾個互動 session 並隨時插手。
- 同層替代方案見 [[平行跑多個-coding-agent-的工具選型]]：Claude Squad 同屬終端層但以預設 worktree 流程為核心，Emdash 等 GUI app 是另一條路線。
- herdr 不介入 agent 的 loop／tools／memory，屬 harness 之外的操作層（見 [[Herdr-按鍵設定]] 對 [[Agent-Harness-Engineering-框架綜述]] 的定位）；它的委派原語也印證 [[pi-workflow-編排-harness-與本-vault-分野]] 所述「編排職能被 harness 與周邊工具吸收」的走向。

## 勿引用與未解問題

**勿引用**：README 行銷句「herdr marks every pane as working, blocked, or idle, and tells you when an agent stops and needs an answer」——兩個 repo URL 投票結果相反（2-1／1-2）。核心有 docs 支持，但「每個 pane」「一定提示」過強：實際是五態、只對辨識出的 agent、blocked 偵測 best-effort。引用時用上方狀態表與盲點清單。

**未解（本輪未查到，不可憑推測補）**：

- 社群實際踩雷與 GitHub issues 回報（manifest 誤判、bracketed paste 相容性、Windows client 問題）——驗證名額耗盡，社群面向未送驗。
- 與「tmux + hooks 通知」的實際取捨、長期使用心得。
- 具名 session 之間能否跨 session 送 prompt。
