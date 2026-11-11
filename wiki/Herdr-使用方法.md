---
title: Herdr 使用方法
description: herdr TUI 的層級、持久化、狀態偵測、CLI 委派、worktree 與 SSH 遠端用法，另記 Herdr app／herdr-core 與 Windows 接 WSL
created: 2026-09-15
updated: 2026-11-11
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

預設開啟（`[session] resume_agents_on_restore = false` 可關）。server 重啟後，支援的 agent 用自己的 resume 指令接回對話，如 `claude --resume <id>`、`codex resume`，agy、OpenCode、Copilot、Cursor、Devin 等亦在列。接回的是**新程序、舊對話**。前提是該 pane 已透過夠新的官方 integration 回報 session reference（`herdr integration status` 檢查；版本門檻指 integration 版本，不是 agent 本身版本）；reference 缺漏或過期就還原成普通 shell。（3-0）2026-09 底起多了一條路：agent 可自行向 herdr 回報 resume 指令，server 重啟後照該指令重開 session，不需內建 integration（官方指南〈[Add Herdr support to your agent](https://herdr.dev/docs/add-herdr-support/)〉）；還原時 agent 改為逐一啟動，預設間隔 100 ms，可用 `[session] startup_per_agent_delay_ms` 調整。（官方 [CHANGELOG](https://github.com/herdrdev/herdr/blob/master/CHANGELOG.md) 一手、僅讀摘要、未實測）

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

官方 agent skill 可用 `npx skills add herdrdev/herdr --skill herdr -g` 安裝或 `herdr --skill` 印出，使用 CLI 前檢查 `HERDR_ENV=1`。（3-0）本機全域的 `herdr-agent` skill 即是這套原語的應用：開新 tab 啟動另一個 agent 派工，主 agent 在背景用 `herdr agent wait` 等對方停下、讀畫面最後一行結論轉達；只有不能背景執行的主 agent 才改由對方用 `herdr agent prompt` 回敲主 pane。官方 skill 管版面、worktree、多機等完整控制，本機 skill 只做「交派→放手→收結論」一條路徑，兩者分工不重疊。

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

本機 client 可為 Linux、macOS、Windows；**遠端主機只能是 Linux 或 macOS**。已被取代（2026-10-07）：herdr 自 2026-09 中起支援 Windows x86_64 遠端主機（Windows ARM64 走 x64 模擬，best-effort），舊文件「Windows is not supported as the remote host」一句已移除；確切版本以[官方 CHANGELOG](https://github.com/herdrdev/herdr/blob/master/CHANGELOG.md) 為準（官方 CHANGELOG 與 [persistence-remote 文件](https://github.com/herdrdev/herdr/blob/master/docs/versions/0.9.3/website/src/content/docs/persistence-remote.mdx)一手、未實測）。direct terminal attach 則仍只支援 Linux／macOS，原生 Windows 不行（官方文件所述、未實測）。

## Herdr app 與 herdr-core（另一條產品線）

官方站根目錄現在是 **Herdr app**：原生桌面 app（macOS Apple silicon、Linux x86_64／arm64、Windows x86_64，另有手機版），底下跑的是 **herdr-core**（CLI 叫 `hc`），**不是**本頁上面寫的 Herdr TUI；TUI 文件已搬到 `herdr.dev/tui/docs/`。所以 TUI 的 session、workspace 不會出現在 app 裡，app 只看得到 herdr-core 的 terminal。app 設定與給 agent 讀的說明在 `~/.config/herdr-app/AGENTS.md`，core 的手冊用 `hc --skill`。（官方 [herdr.dev](https://herdr.dev/)、[core 頁](https://herdr.dev/core/)、[herdr-app](https://github.com/herdrdev/herdr-app)／[herdr-core](https://github.com/herdrdev/herdr-core) repo 一手，2026-11-10 讀）

**與 TUI 的主要差異**（官方首頁 FAQ、herdr-core README 一手）：

- **狀態來源不同**：core 不讀畫面猜狀態、也不認 agent 品牌，只收程式自己用 OSC 7501（Program Status Protocol）回報的 working／done／blocked；不回報的程式照跑但沒有狀態，也不進 agent 清單。Claude Code（[官方 CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)）與 Codex（`openai/codex` 的 `terminal_program_status.rs`）已內建回報；agy 本輪未查。
- **重開機不接回 agent**：重開機或 core 停止後 pane 回到原資料夾的新 shell，agent 不重啟也不 resume——TUI 的原生 agent session 還原在 app 沒有對應。
- **agent 派工內建回報**：agent 可用 `hc run` 起 helper、`hc send` 改任務，helper 的報告、結束與求助自動回到派工的 agent。
- **手機版與多機**：iPhone／iPad／Android 直連你的機器（無帳號、不經 Herdr 伺服器），SSH 機器的 agent 併入同一側欄。
- **介面可改**：layout、側欄、按鍵、主題都是 `~/.config/herdr-app` 下的檔案，mod 是 JavaScript 小程式，官方有 layout／mod gallery。

**app 的其他機器都是 core 的 machine**：app 側欄每個 space 屬於一台機器——本機，或 `hc machine ls` 列出的機器。app 內的「Add machine」對話框只列 `~/.ssh/config` 的 Host，等於跑 `hc machine add <target>`；不走 SSH 的接法要自己在終端下 `hc machine add --via <command>`，加好後 app 就會出現該機器。（herdr-app `defaults/mods/machine-add`、`defaults/AGENTS.md` 原始碼一手）

### Windows app 接 WSL

在 Windows 跑 app 時，WSL distro 不需要 SSH server，官方寫法是在 **PowerShell 7（`pwsh`）** 執行（Windows PowerShell 5.1 與 cmd 會弄壞內嵌引號）：

```powershell
hc machine add --via 'wsl.exe -d <distro 名> -e sh -c' --name wsl
```

distro 名用 `wsl -l -q` 查。WSL 裡沒有 `hc` 時，在互動終端下會先詢問是否複製過去。（herdr-core `docs/machines.md` 一手）

踩雷：Windows 上的 `--via` 是 2026-11-09 才合併的修正（commit `093ddde`「fix(windows): support native via machine commands」），**修正前的發佈版在 Windows 一律拒絕 `--via`**，錯誤訊息是 `bad command "...": one line, run by sh here`（2026-11-10 本機實測重現）。遇到這個錯誤就先用 `hc --version` 看版本，更新到含此修正的版本再加；app 會自動更新 core。確切版本以 [herdr-core CHANGELOG](https://github.com/herdrdev/herdr-core/blob/main/CHANGELOG.md) 為準。

等不到新版的繞法是改走 SSH：WSL 開 sshd、Windows 公鑰放進 WSL 的 `authorized_keys`，WSL 裡用官方 `install.sh` 裝 core，Windows 的 `~/.ssh/config` 加一個 `HostName localhost` 的 Host，再 `hc machine add <該 Host>`（或在 app 的 Add machine 點選）。非互動 SSH 的 PATH 沒有 `~/.local/bin` 也沒關係，core 找不到時會退回 `$HOME/.local/bin/herdr-core`（herdr-core `machines.rs` 原始碼）。2026-11-10 本機實測連得上（WSL NAT 模式）。代價是 SSH 不會幫你開機：WSL 關機或閒置停掉後要先開一個 WSL 終端，`--via wsl.exe` 則會自己把 distro 帶起來。

### 從 TUI 遷移到 app

官方沒有獨立的遷移指南，唯一的遷移指引在 app 歡迎畫面：workspace 一律不搬（「Your herdr workspaces stay where they are; nothing moves over」），按鍵與設定則交給 agent 轉，官方給的提示句是「Read `herdr-app --skill`, then migrate my keybinds and settings from ~/.config/herdr/config.toml」。FAQ 說 TUI「keeps working」，兩邊不共用 agent，可以並存；沒提 TUI 是否繼續開發。（herdr-app `defaults/frame/welcome/main.js` 原始碼、[官方 FAQ](https://herdr.dev/faq) 一手，2026-11-11 讀）

第三方實測補充（[Classmethod 2026-11-04](https://dev.classmethod.jp/en/articles/reona-herdr-app-herdr-core/)，單一作者在 macOS 上用 BETA 版測，非官方）：

- TUI 裝的 Claude Code hook（`herdr integration install claude`）在 core 底下不會觸發，因為 hook 看 `HERDR_ENV` 這類變數，而 `hc` 起的 terminal 只帶 `HC_` 開頭的變數；Claude Code 改走 OSC 7501 回報，不需要 hook。
- 新資料夾的信任提示不會變成 `blocked`，app 看不出 agent 在等輸入，要用 `hc read`／`hc keys` 手動處理。
- `keys.json` 是一鍵對一指令，tmux 式 prefix 序列要靠 popup mod 才做得到；作者建議這類按鍵流程先留在 TUI。
- app 預設每天送匿名使用資料，TUI 不會；在 `settings.json` 關掉，或用 `DO_NOT_TRACK=1`／`HERDR_TELEMETRY=0`。

## 與相鄰工具的定位

- 對 [[Multica-與-agent-看板的用法與適用邊界]]（agent 判斷，非查證結論）：Multica 是非同步看板，agent 是身分、run 結束即走，人類在卡片把關點介入；herdr 是同步的終端層，agent 是常駐程序，人類即時盯側欄狀態。前者適合佇列化派工，後者適合同時跑幾個互動 session 並隨時插手。
- 對 [[Orca]]：herdr 聚焦在終端多工與 agent 狀態自動偵測（側欄同步監看），不介入任務生命週期或工作合約；Orca 則是面向多 agent 的整合開發環境（multi-agent IDE），除了整合 worktree 與 terminal 操作，更提供結構化的 Run/Task/Dispatch 狀態機、非同步信箱與嚴謹的 worker 監督迴圈（supervised loop）。
- 同層替代方案見 [[平行跑多個-coding-agent-的工具選型]]：Claude Squad 同屬終端層但以預設 worktree 流程為核心，Emdash 等 GUI app 是另一條路線。
- 檔案與 diff 檢視是 herdr 相對 GUI 型 ADE 的明顯缺口，補法（plugin／通用終端 TUI／旁開編輯器三條路線）與所選方案的設定見 [[Yazi-設定與踩雷]]；該頁也記了在多工器背景 pane 裡的卡頓踩雷，機制上可能波及 herdr 但尚未驗證。
- herdr 不介入 agent 的 loop／tools／memory，屬 harness 之外的操作層（見 [[Herdr-按鍵設定]] 對 [[Agent-Harness-Engineering-框架綜述]] 的定位）；它的委派原語也印證 [[pi-workflow-編排-harness-與本-vault-分野]] 所述「編排職能被 harness 與周邊工具吸收」的走向。

## 勿引用與未解問題

**勿引用**：README 行銷句「herdr marks every pane as working, blocked, or idle, and tells you when an agent stops and needs an answer」——兩個 repo URL 投票結果相反（2-1／1-2）。核心有 docs 支持，但「每個 pane」「一定提示」過強：實際是五態、只對辨識出的 agent、blocked 偵測 best-effort。引用時用上方狀態表與盲點清單。

**未解（本輪未查到，不可憑推測補）**：

- 社群實際踩雷與 GitHub issues 回報（manifest 誤判、bracketed paste 相容性、Windows client 問題）——驗證名額耗盡，社群面向未送驗。
- 與「tmux + hooks 通知」的實際取捨、長期使用心得。
- 具名 session 之間能否跨 session 送 prompt。

## 關聯

- [[訊息平台到-coding-agent-的獨立-gateway]]——ccgram 可把 Telegram topic 對應到 herdr session，是 herdr 環境零改動可接的手機端入口。
