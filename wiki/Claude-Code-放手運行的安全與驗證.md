---
title: Claude Code 放手運行的安全與驗證
description: 深讀 Lydia Hallie 演講並對照官方文件，整理 auto mode、deny、沙箱、cloud、hook 與 CI 的分工、缺口及落地步驟
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/lydia-hallie
published: 2026-11-11
parent: "[[wiki/01.index]]"
tags:
  - claude-code
  - coding-agent
  - ai-agent
  - testing
---

2026-11-19 研究 [AI懶人報 EP474](https://www.youtube.com/watch?v=-m3yj9YLmxs) 的回存。影片整理 Anthropic Claude Code 團隊 Lydia Hallie 的演講〈[Rethinking Claude Code Best Practices](https://www.youtube.com/watch?v=vlfCjWuv4es)〉，本頁逐項回查演講與官方文件。2026-11-19 第二輪深讀了 AI Engineer 官方閱讀頁與整場機器逐字稿（約 17 分半，講者因現場 AV 中斷事後自錄），落地於 [[AI-Engineer-Hallie-Rethinking-Claude-Code-Best-Practices]]，並補上「演講脈絡」「第二輪回查」「個人工作流程落地」三節。**證據強度**：功能行為來自官方文件；安全數字是 Anthropic 自測；演講內容來自官方機器逐字稿（含辨識錯誤，如 Claude 被寫成 Cloud）；指令與設定都未實跑。功能變動快，引用前請回查文件。

**一句話**：人退出迴圈後，方向交給模型、核准交給 auto mode、硬限制交給 deny 規則與執行環境、結果交給測試、hook 與 CI。影片的分工正確，但有兩個缺口要補：沙箱有「失敗後改到沙箱外重試」的出口，Projects 的 cloud thread 不套用 repo 裡的權限規則與 hook。

## 講者與立場

Lydia Hallie 是 Anthropic Claude Code 團隊的 Member of Technical Staff（官方閱讀頁的講者欄）。演講於 2026-11-11 的 AI Engineer CODE 2026 Day 1 發表。整場用的功能（auto mode、`/doctor prompt-audit`、cloud session、network secret、CI auto-fix、Projects）都是自家產品，示範的流程等於產品使用路線圖，屬 **vendor 立場**。她說的「Anthropic 內部同時跑幾十個 session、跑好幾小時」是內部使用描述，沒有給量化資料；唯二的數字（每日變更數、14%／89%）都出自 Anthropic 自家文章。

## 演講脈絡（依時間序）

時間碼對應替代錄影 [vlfCjWuv4es](https://www.youtube.com/watch?v=vlfCjWuv4es)。

1. **今昔對比（0:36–1:42）**：年初的 session 是較舊模型跑一小段就停，人不斷糾正、在 `CLAUDE.md` 加「IMPORTANT!」，沒有 auto mode，只能逐一核准或冒險用 dangerously-skip-permissions。現在 Anthropic 內部同時跑幾十個 session、每個跑數小時、自己驗證結果，還有 session 去編排其他 session，人變成管理者。
2. **產量與問題設定（1:43–2:45）**：引用 Anthropic 十月的文章，每日變更從五月約 2,500 增到九月超過 3 萬。年初的最佳實務是「引導、核准、拒絕、限制、審輸出、啟動 session」；人每退出一個環節，就要由**模型、harness 或執行環境**之一接手。核心兩問：沒人盯時品質怎麼保證、跑數小時時怎麼保證安全。
3. **先換預設（2:46–4:10）**：升級到當時最新的模型、權限改 auto mode（她說八月起已是預設）。模型更懂意圖與程式庫，中途少引導。但這也代表 `CLAUDE.md` 要重想：「IMPORTANT」「never」加驚嘆號這類寫法對新模型不需要，還會讓模型偏離、多做工具呼叫、結果變差。只留 Claude 從程式碼看不到的事，例如某服務仍依賴程式裡沒直接引用的 legacy 來源；用什麼 stack、去哪找檔案就不必寫。`/doctor prompt-audit` 會依目前模型檢查 `CLAUDE.md` 與 skills 中不再需要的內容。
4. **auto mode 與信任範圍（4:11–5:33）**：auto mode 對讀檔、改專案內檔案以外的幾乎所有動作跑獨立分類器；跑測試、裝依賴這類已知安全的放行，不確定的擋。例子：叫它推到 staging 的 deploy repo，預設只信任目前資料夾與 repo，所以被擋、人又被拉回迴圈。解法是在個人 settings 用白話寫信任的 repo、bucket、domain，以及一定允許／一定不做的事，這段文字會送給分類器。到這一步「離開迴圈很容易」，難的是確認不在場也沒問題：先講安全，再講驗證。
5. **分類器不是保證（5:42–7:13）**：八月的研究中真人只抓到約 14% 的明顯危險指令，auto mode 擋 89%，但仍有約一成漏過。要保證只能在 harness 做：deny 規則比分類器先判，符合 deny 的呼叫分類器根本看不到。判斷要不要寫規則的準則是**「Claude 錯一次，我收得回來嗎？」**：寫錯程式可 revert，交給模型；丟掉未提交修改、把金鑰讀進 transcript，就該寫規則。例子：auto mode 預設允許讀 `.env`，加 deny 後連 `cat` 也打不開。
6. **看似無害的指令（7:14–9:09）**：`npm test` 是正常指令，但執行時會跑依賴套件或 Claude 臨時寫的腳本；若其中之一被入侵，可以讀 `.env`、SSH key 送到陌生伺服器。就算人還在逐一核准也只會按允許，因為表面上沒東西可拒。**權限只決定呼叫能不能執行，管不到執行後碰得到什麼**；不能封鎖 `npm test`，只能限制它的環境。本機用沙箱：由作業系統強制限制讀哪些檔、寫哪些資料夾、連哪些 host，子行程一併適用；開沙箱後 deny 規則會傳給作業系統，依賴去開 `.env` 時直接被拒。預設仍可讀大部分機器，SSH key 要另加規則；未核准的 host 連不到。
7. **沙箱的邊界與 cloud session（9:10–10:46）**：沙箱只管 Claude 跑的 shell 指令及其子行程，Claude 自身檔案、MCP server、hook 都在沙箱外，整個 session 仍在你的機器上。理想是讓整件事跑在這些東西根本不存在的地方，也就是 cloud session：獨立機器、新 clone 的 repo、關筆電照跑。`.env`、SSH key、GitHub token 都不在 git 裡，自然不在那台機器上；需要 API key 時設成 network secret，session 中途缺 key 會提示你，模型本身看不到 key。預設網路只通套件 registry 與 GitHub，其他 domain 要明確加。但**機器可丟，離開機器的東西不可丟**：push 的 commit、經 connector 送出的訊息。所以雲端仍跑 auto mode，並把 deny 規則 commit 進 repo 一起帶過去，還能擋 force push 或 commit 裡夾帶 secret。
8. **驗證點（10:47–13:22）**：人在迴圈時看過每個改動，背景跑數小時就沒了，結束時也不會逐檔讀。例子：「把 auth 搬到新 API」，同一個 prompt 可能得到三種合理結果：搬了但保留舊 API、只搬新登入、搬了但把所有人登出。解法是沿途設**回傳 pass／fail 的驗證點**（測試、build、截圖都行），人只審驗證點，比審整包改動短得多；會把人登出的那次跑在第一個檢查就過不去，只能換路。設法有三層：prompt 裡寫「完成長什麼樣」並拆成各自有測試的任務、要求貼出實際輸出（因為你不在場）；但 prompt 不保證，一定要跑的用 hook：每次改檔跑 linter、標記任務完成時跑該任務相關測試（動到 auth 就要過 auth 測試）、結束 session 時跑全套測試。失敗就回去修。細節：多數工具失敗時 exit 1，但 exit 1 時任務仍會被標成完成，腳本要 exit 2 才會把 Claude 送回去修。
9. **多 session 與 CI（13:23–15:09）**：單一 session 可放心後就多開，每個有自己的機器，不必自己管 worktree。但人仍逐一啟動、逐一審，此時最重要的是 CI：所有 session 最終都開 PR，CI 對每個 PR 跑同一套檢查，不管 session 怎麼設、途中做了什麼決定。開 CI auto-fix 讓 Claude 看到失敗就回去修，人不必把 review 花在檢查本可抓到的東西。部分 PR 可開 GitHub 的 merge when ready，檢查全過就自動合；但這不是預設，取決於風險。她團隊的做法：每個 PR 先由 Claude review（不是寫它的那個 session，而是全新 context），再由另一組 agent 複查每個找到的 bug；人審多少看風險，文件或文案不需要人，一般產品改動一人，高風險兩人。
10. **編排者（15:10–16:33）**：她自認不擅長 context switching，同時管很多 session 效果不好。方向是由一個主 session 當 orchestrator，例如仍在 beta 的 Claude Code Projects：你說要做什麼，它拆任務、為每個任務開 thread（新 session）、追蹤回報並驗證，你只跟一個對話而不是八個。主 session 不寫程式，要用擅長決策與判斷結果的模型；未完成就退回直到真的完成並通過所有檢查。thread 要用擅長實作的模型，兩者可分開設。Projects 還會自動管 context，不必再想何時 compact 或 clear。
11. **總結與起手式（16:34–17:30）**：舊的最佳實務都還在，只是搬家了：模型負責引導，auto mode 負責核准、deny 規則負責硬限制，環境限制可能性，測試、hook、CI 負責檢查，最後連啟動 session 都交給 Claude，人只啟動第一個、審最後產出。建議做法：挑一件比平常交給 Claude 大得多的工作、確認 CI 真的抓得到你在意的問題、花點時間設定環境（網路、secret、setup script），然後在雲端開跑，觀察 session 卡在哪、你還在哪一步被拉回迴圈，那就是下一個要交出去的環節。

## 影片主張的查證結果

| 影片主張 | 查證結果 | 依據 |
|---|---|---|
| Anthropic 每天的程式碼改動從約 2,500 增到超過 3 萬 | **成立**：原文是 monorepo 每日合併的變更數（2026 年 5 月到 9 月），不是 Claude Code session 數 | [Anthropic 工程文](https://www.anthropic.com/engineering/redesigning-source-control) |
| `CLAUDE.md` 只寫 Claude 從程式碼看不到的事 | **大致成立**：官方範例仍保留測試、型別檢查等指令與專案慣例，`/doctor` 也保留地雷、理由和不同於工具預設的慣例 | [Best practices](https://code.claude.com/docs/en/best-practices)、[Memory](https://code.claude.com/docs/en/memory) |
| auto mode 已是預設權限模式 | **有條件成立**：較新版本的終端與 VS Code 預設啟動 auto；已自訂 `defaultMode`、模型不支援或組織停用時不一定會進入 | [Permission modes](https://code.claude.com/docs/en/permission-modes) |
| 跑測試、裝套件會自動放行 | **需補條件**：預設放行的是安裝 lock file 或 manifest 已宣告的依賴 | 同上 |
| 預設只信任目前資料夾與 repo，可用白話設定信任範圍 | **成立**：寫在 `autoMode.environment`；分類器不讀 repo 內 `.claude/settings.json` 的 `autoMode`，避免 repo 替自己加白名單 | [Auto mode config](https://code.claude.com/docs/en/auto-mode-config) |
| 真人只抓到約 14% 危險指令，auto mode 擋下 89% | **成立但情境受限**：1,053 位受測者在測試環境中各遇到一個植入的明顯危險指令（143 對 937），不是在自己的專案裡 | [Anthropic 部落格](https://claude.com/blog/auto-mode-default-in-claude-code) |
| deny 規則先於分類器，連 `cat .env` 也擋 | **成立，有邊界**：擋得到 Claude Code 認得的檔案指令，擋不到腳本間接讀檔或未點名檔案的 `grep -r` | [Permissions](https://code.claude.com/docs/en/permissions) |
| 沙箱由作業系統強制，只管 shell 指令 | **成立**：`~/.ssh` 預設可讀要另外擋；內建檔案工具、MCP 與 hook 都在沙箱外 | [Sandboxing](https://code.claude.com/docs/en/sandboxing) |
| cloud session 沒有本機 `.env`、SSH key、GitHub token，network secret 不給模型看 | **成立**：network secret 限 Anthropic 託管環境；模型看不到金鑰，但仍能透過 proxy 使用它呼叫對應 host | [Cloud environments](https://code.claude.com/docs/en/cloud-environments) |
| 測試失敗要用 exit 2，exit 1 不會擋 | **成立**：`TaskCompleted`、`Stop` 可被 exit 2 擋下；`PostToolUse` 只能把錯誤回給 Claude，因為工具已執行 | [Hooks](https://code.claude.com/docs/en/hooks) |
| Projects 會拆任務、自動管理 context | **成立**：仍是 public beta，只開放 Pro、Max、Ultra 並逐步推出，消耗額度也比單一 session 快 | [Projects](https://code.claude.com/docs/en/claude-projects) |

### 第二輪回查（2026-11-19，讀官方文件原文）

| 演講主張 | 查證結果 | 依據 |
|---|---|---|
| `/doctor prompt-audit` 會檢查 `CLAUDE.md` 與 skills 中新模型不需要的內容 | **成立且範圍更廣**：預設涵蓋 `CLAUDE.md`、`CLAUDE.local.md`、`AGENTS.md`，以及 `.claude/` 與 `~/.claude/` 下的 rules、skills、commands、subagents、output styles；也抓指向不存在檔案的指令與互相矛盾的指令。只產出報告與建議修改，你同意才動檔；可傳路徑只審單一檔案或目錄。它透過內建的 `/claude-api` skill 執行，該 skill 被停用時無法使用 | [Memory：Audit your instruction files](https://code.claude.com/docs/en/memory)、[Best practices](https://code.claude.com/docs/en/best-practices) |
| auto mode 八月起成為預設 | **成立**：Anthropic 部落格 2026-08-07 公告，自 08-14 起 Pro、Max、Team 的新 session 預設 auto mode；已自設其他預設者可能看到一次性切換提示 | [Anthropic 部落格](https://claude.com/blog/auto-mode-default-in-claude-code) |
| deny 規則先於分類器，分類器看不到 | **成立**：官方決策順序第一步就是 allow／ask／deny 規則，命中即結案；其餘才送分類器 | [Permission modes：How the classifier evaluates actions](https://code.claude.com/docs/en/permission-modes) |
| 開沙箱後 deny 規則會交給作業系統 | **成立，限 `Read`／`Edit` deny**：沙箱設定會吸收 `Read` 與 `Edit` 的 deny 規則；反過來，沙箱的 `denyRead` 擋不到內建 Read 工具，兩邊要各自設。另有 `sandbox.credentials` 可同時擋 `~/.ssh` 這類檔案，並在沙箱指令執行前移除 `GITHUB_TOKEN` 等環境變數 | [Sandboxing](https://code.claude.com/docs/en/sandboxing) |
| cloud 預設網路只通套件 registry 與 GitHub | **成立**：新環境預設 Limited 並勾選 Allow package managers，可連預設 allowlist（套件 registry、GitHub、雲端 SDK）加上你列的 domain；環境也可設 setup script 與環境變數 | [Cloud environments](https://code.claude.com/docs/en/cloud-environments) |
| CI auto-fix 讓 Claude 自動修失敗的檢查 | **成立**：需安裝 Claude GitHub App；可在 cloud session 的 PR 選單開、在終端對 PR 分支跑 `/autofix-pr`，或貼 PR URL 請它接手 | [Claude Code on the web：Auto-fix](https://code.claude.com/docs/en/claude-code-on-the-web) |
| merge when ready：檢查全過由 GitHub 自動合 | **成立，是 GitHub 自身功能**：auto-merge 在所有必要 review 與 status check 通過後合併，需 repo 先啟用；「Merge when ready」是 merge queue 分支上的變體。沒寫 required checks 的 repo 等於沒有閘門 | [GitHub Docs：Automatically merging a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/automatically-merging-a-pull-request) |
| orchestrator 與 thread 可設不同模型，context 自動管理 | **成立，但預設不是她的配置**：Projects 分 **Coordinator model／effort** 與 **Thread model／effort**；新專案預設全用 Opus，thread 高 effort、對話低 effort。「主 session 用 Fable、thread 用 Opus」是她個人偏好。thread 會自動 compact，對話只依近期訊息、近期 thread 與 project memory 運作，絕不能遺失的要寫進 project memory | [Projects](https://code.claude.com/docs/en/claude-projects) |

## 影片沒講清楚的缺口

- **沙箱有逃生口**。指令在沙箱內失敗時，Claude 可用 `dangerouslyDisableSandbox` 改到沙箱外重試。auto mode 下由分類器判斷，符合 allow 規則的指令則會直接放行。要當硬邊界，應設 `"allowUnsandboxedCommands": false`。
- **Projects 的 cloud thread 不吃 repo 的權限規則與 hook**。Lydia 說可把 deny 規則 commit 進 repo 帶上雲端，這適用於單一 repo 的 cloud session。Projects 的 cloud thread 只載入 `CLAUDE.md`，`.claude/settings.json` 的權限規則與 hook 都不套用。此時能依靠的是 auto mode、cloud environment 和 CI；需要 hook 就把 thread 放回自己電腦跑。
- **cloud 不是零風險**。機器可丟棄，但 push、connector 訊息和 network secret 對應的 API 呼叫都會留下後果。無論網路層級怎麼設，GitHub、已啟用的 MCP connector 與 network secret 的 host 都仍可連到。
- **auto mode 不能取代高風險審查**。部落格的受控實驗有利於 auto mode，但 Anthropic 較早的[工程文](https://www.anthropic.com/engineering/claude-code-auto-mode)在真實越權動作資料集上回報 17% 漏判，並說它不能直接取代高風險基礎設施的仔細人工審查。兩者資料集不同，數字不可相減。
- **無人值守也可能停下**。分類器連續擋 3 次或累計擋 20 次，auto mode 會暫停並改回詢問。
- **Auto-fix 有副作用**。它需要安裝 Claude GitHub App，回覆會以你的帳號發出並標示來自 Claude Code，可能觸發靠留言驅動的自動化；base branch 前進造成的衝突也不會自動處理。
- **在對話裡講的邊界會被 compact 掉**。官方文件說 auto mode 分類器每次檢查都從 transcript 重讀使用者講過的邊界，context compaction 若刪掉那則訊息，邊界就失效；要硬保證就寫 deny 規則（[Permission modes](https://code.claude.com/docs/en/permission-modes)）。這正好支持她「做不得錯的事要寫成規則」的準則，但她沒點出這條失效路徑。
- **hook 壞掉時預設是放行**。她只講了 exit 2；官方文件另說明 hook 本身失敗（路徑打錯、腳本崩潰、逾時）在多數事件上算非阻擋錯誤，動作照常進行，等於政策 hook 失效時全部放行；要改成失敗即阻擋，需在 `command`／`http` hook 設 `"onFailure": "block"`。另外 `Stop`／`TaskCompleted` 用 exit 2 送回 Claude 時，若 hook 自身跑不起來，Claude 也修不了它（[Hooks](https://code.claude.com/docs/en/hooks)）。
- **驗證點的測試可能是 Claude 自己寫的**。演講的驗證點設計預設測試本身可信，但若測試也由同一 session 產出，就有循環驗證問題，見下方「張力」。

## 怎麼落地

1. 先分「做錯能不能收回」：寫錯程式可交給模型；讀到金鑰、丟掉未提交修改、資料外送要寫成規則或由環境限制。
2. 本機長跑時開沙箱，加上金鑰路徑限制，並關閉沙箱外重試。WSL2 需要 `bubblewrap` 與 `socat`。
3. 需要離開本機環境時改用 cloud session，把外部 API 金鑰設成 network secret，網路維持最小範圍。
4. 用測試、build、截圖等可判定的驗證點約束過程。一定要跑的放 hook，腳本失敗時明確 `exit 2`，並把原因寫到 stderr。`Stop` hook 要檢查 `stop_hook_active`，避免卡在永遠無法滿足的條件。
5. CI 是所有 session 共用的最後關卡。Lydia 團隊的做法是由全新 context 的 Claude 先審 PR，再由另一組 agent 複查問題；文件類改動可不經人工，一般改動一人、高風險改動兩人。這是單一團隊經驗，不是通用標準。

## 個人工作流程照做步驟

以下針對單人、本機（含 WSL）為主、偶爾用雲端的情境，依演講順序排列；指令與設定名來自官方文件，未實跑。

**Claude Code**

1. **審指示檔**：在專案內跑 `/doctor prompt-audit`，它會一併審 `AGENTS.md`、rules 與 skills；逐條看報告再決定是否套用，不要一鍵全收。判準照演講：只留從程式碼看不出來的事。
2. **列出收不回的動作**，各寫成 deny：至少 `Read(./.env)` 這類金鑰檔、丟棄未提交修改的指令、force push。寫在 user 或 project 的 `permissions.deny`；要帶上單一 repo 的 cloud session 就 commit 進 repo 的 `.claude/settings.json`。
3. **本機開沙箱**：`sandbox.enabled: true`、`allowUnsandboxedCommands: false`，並用 `sandbox.credentials` 擋 `~/.ssh`、`~/.aws/credentials`，移除 `GITHUB_TOKEN` 等環境變數。WSL2 要先裝 `bubblewrap` 與 `socat`。
4. **信任範圍寫進個人 settings**：auto mode 老是擋你常用的 deploy repo 或 bucket 時，在 `~/.claude/settings.json` 的 `autoMode.environment` 用白話寫；寫在 repo 內的不會被分類器採用。
5. **完成閘門用 hook**：`PostToolUse` 改檔後跑 linter（只能回報，不能撤銷）；`TaskCompleted` 跑該任務相關測試；`Stop` 跑全套。失敗時 `exit 2` 並把原因寫 stderr，`Stop` 先檢查 `stop_hook_active` 防無限迴圈；政策型 hook 加 `"onFailure": "block"`。
6. **prompt 寫成驗收條件**：先寫「完成長什麼樣」，請它拆成各自有測試的任務，並要求貼出測試與 build 的實際輸出，而不是只說「通過了」。
7. **CI 當共同關卡**：先確認 CI 真的會擋你在意的問題，再考慮 auto-fix；auto-merge 只開給低風險類別，且 repo 要設 required checks。
8. **起手實驗**：挑一件比平常大的任務丟到 cloud session（先設好網路、network secret、setup script），記下它卡住或把你拉回來的地方，下一輪只處理那一點。

**Codex（對應做法，依 OpenAI 官方文件）**

- auto mode 的對應是 Auto-review：`approvals_reviewer = "auto_review"` 把需核准的請求交給審查 agent，政策拒絕 critical-risk 動作，審查失敗時 fail closed（[Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security)）。
- deny 的對應是 `~/.codex/rules/*.rules` 的前綴規則，`decision = "forbidden"` 直接拒絕，多條命中取最嚴格（[Rules](https://developers.openai.com/codex/rules)）。它比對的是指令前綴，與 Claude Code 一樣擋不到腳本內部的間接讀檔，所以還是要靠沙箱。
- 沙箱：預設 `workspace-write` 沙箱關閉網路，要開需 `sandbox_workspace_write.network_access = true`；比 Claude Code 本機沙箱預設更緊（[Agent approvals & security](https://developers.openai.com/codex/agent-approvals-security)）。
- 完成閘門：Codex 的 `Stop` hook 可用 `exit 2`＋stderr 或回傳 `{"decision":"block","reason":...}` 讓它繼續，也有 `stop_hook_active` 欄位；但 turn 內事件清單沒有 `TaskCompleted`，任務級閘門只能併進 `Stop`（[Hooks](https://developers.openai.com/codex/hooks)）。
- **不能直接搬的**：cloud session 的 network secret、Projects 的 coordinator／thread 分模型、Claude GitHub App 的 auto-fix 都是 Anthropic 產品功能，Codex 端要另找對應機制，本頁未查證。

## 勿引用

- 「auto mode 比人安全 6.5 倍」之類的倍數：13.6% 和 89% 來自單一植入指令的受控實驗，不能外推到所有專案與風險等級。
- 「開了沙箱就不會逃出去」：預設設定下仍可能走沙箱外重試。
- 「Anthropic 每天 3 萬個變更都是 Claude Code session 產出」：原文是 monorepo 每日合併的變更數，演講也只說「changes」。
- 「Anthropic 工程師同時跑幾十個 session、每個跑幾小時」當作普遍實況或量化數據：只是講者口述的內部使用描述，自報、無數字、無對照。
- 「exit 1 的 hook 一定會被忽略」：一般情況是非阻擋錯誤，但設了 `onFailure: "block"` 的 hook 失敗時會阻擋動作，要看實際設定。

## 張力與互補

- **與 Lauren Tan 互補**：[[Lauren-Tan-把糾正寫進程式庫]]主張把糾正寫進程式庫（API、架構、lint、型別），Lydia 主張把人放手後的職責交給 harness 與環境（deny、沙箱、hook、CI）。兩人共同反對靠散文指示當保證，差在落點：一個改程式碼本身，一個改執行環境；兩者可疊用。兩場都是同屆 vendor 講者的自報經驗。
- **驗證點的信任前提**：演講把測試當可信的 pass／fail 訊號，但[[用測試約束-AI-產碼]]指出 AI 依現有程式碼反推測試是循環論證，且 agent 可能用 `--no-verify`、改 workflow 等方式繞過護欄。實務上 hook 跑的測試最好由人或規格定義，deny 也該涵蓋改 hook、改 CI 設定的動作。
- **vendor 敘事的強度**：[[AI-自主工作流的實證檢驗]]的結論是長時自主 loop 與驗證迴路的流程描述可信，但「這樣做讓 agent 做得更好」的因果主張缺獨立實證。本場同樣只有流程與自家數字，沒有「開了這些機制後缺陷率或事故率如何」的資料。
- **跨工具對照**：[[四套-coding-agent-能力差異對照]]整理了 Codex 的沙箱、`rules` 與 Auto-review；本頁「個人工作流程照做步驟」的 Codex 段是把演講流程套到那些機制上的具體版本。

## 交叉引用

- 原始來源：[[AI-Engineer-Hallie-Rethinking-Claude-Code-Best-Practices]]——官方閱讀頁與完整機器逐字稿；本頁「演講脈絡」的時間碼與引述皆出自此。
- 同屆綜合：[[AI-Engineer-2026-演講精華-AI-工作流程]]——收錄同屆 28 場，本頁是其中 Lydia Hallie 一場的深讀版。
- 指令內容：[[Claude-5-世代的指示精簡原則]]——該頁處理 `CLAUDE.md` 該留什麼，本頁處理移除人工核准後由誰接手。
- Hook 能力：[[Claude-Code-Hook-能力邊界]]——該頁說明 hook 輸出契約，本頁的完成閘門是其「放行判斷」用途的具體案例。
- Review 分流：[[Matt-Pocock-的-PR-瓶頸解法]]——兩邊都按風險決定人工投入，但 Matt 以可逆性為軸，Lydia 團隊以改動類型與風險為軸。
