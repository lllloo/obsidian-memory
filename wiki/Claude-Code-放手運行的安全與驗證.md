---
title: Claude Code 放手運行的安全與驗證
description: 查證 Lydia Hallie 演講與 AI懶人報 EP474，整理 auto mode、deny、沙箱、cloud、hook 與 CI 的分工及缺口
created: 2026-11-19
updated: 2026-11-19
source: https://www.youtube.com/watch?v=-m3yj9YLmxs
published: 2026-11-15
parent: "[[wiki/01.index]]"
tags:
  - claude-code
  - coding-agent
  - ai-agent
  - testing
---

2026-11-19 研究 [AI懶人報 EP474](https://www.youtube.com/watch?v=-m3yj9YLmxs) 的回存。影片整理 Anthropic Claude Code 團隊 Lydia Hallie 的演講〈[Rethinking Claude Code Best Practices](https://www.youtube.com/watch?v=vlfCjWuv4es)〉，本頁逐項回查演講與官方文件。**證據強度**：功能行為來自官方文件；安全數字是 Anthropic 自測；演講只讀 YouTube 機器字幕；指令與設定都未實跑。功能變動快，引用前請回查文件。

**一句話**：人退出迴圈後，方向交給模型、核准交給 auto mode、硬限制交給 deny 規則與執行環境、結果交給測試、hook 與 CI。影片的分工正確，但有兩個缺口要補：沙箱有「失敗後改到沙箱外重試」的出口，Projects 的 cloud thread 不套用 repo 裡的權限規則與 hook。

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

## 影片沒講清楚的缺口

- **沙箱有逃生口**。指令在沙箱內失敗時，Claude 可用 `dangerouslyDisableSandbox` 改到沙箱外重試。auto mode 下由分類器判斷，符合 allow 規則的指令則會直接放行。要當硬邊界，應設 `"allowUnsandboxedCommands": false`。
- **Projects 的 cloud thread 不吃 repo 的權限規則與 hook**。Lydia 說可把 deny 規則 commit 進 repo 帶上雲端，這適用於單一 repo 的 cloud session。Projects 的 cloud thread 只載入 `CLAUDE.md`，`.claude/settings.json` 的權限規則與 hook 都不套用。此時能依靠的是 auto mode、cloud environment 和 CI；需要 hook 就把 thread 放回自己電腦跑。
- **cloud 不是零風險**。機器可丟棄，但 push、connector 訊息和 network secret 對應的 API 呼叫都會留下後果。無論網路層級怎麼設，GitHub、已啟用的 MCP connector 與 network secret 的 host 都仍可連到。
- **auto mode 不能取代高風險審查**。部落格的受控實驗有利於 auto mode，但 Anthropic 較早的[工程文](https://www.anthropic.com/engineering/claude-code-auto-mode)在真實越權動作資料集上回報 17% 漏判，並說它不能直接取代高風險基礎設施的仔細人工審查。兩者資料集不同，數字不可相減。
- **無人值守也可能停下**。分類器連續擋 3 次或累計擋 20 次，auto mode 會暫停並改回詢問。
- **Auto-fix 有副作用**。它需要安裝 Claude GitHub App，回覆會以你的帳號發出並標示來自 Claude Code，可能觸發靠留言驅動的自動化；base branch 前進造成的衝突也不會自動處理。

## 怎麼落地

1. 先分「做錯能不能收回」：寫錯程式可交給模型；讀到金鑰、丟掉未提交修改、資料外送要寫成規則或由環境限制。
2. 本機長跑時開沙箱，加上金鑰路徑限制，並關閉沙箱外重試。WSL2 需要 `bubblewrap` 與 `socat`。
3. 需要離開本機環境時改用 cloud session，把外部 API 金鑰設成 network secret，網路維持最小範圍。
4. 用測試、build、截圖等可判定的驗證點約束過程。一定要跑的放 hook，腳本失敗時明確 `exit 2`，並把原因寫到 stderr。`Stop` hook 要檢查 `stop_hook_active`，避免卡在永遠無法滿足的條件。
5. CI 是所有 session 共用的最後關卡。Lydia 團隊的做法是由全新 context 的 Claude 先審 PR，再由另一組 agent 複查問題；文件類改動可不經人工，一般改動一人、高風險改動兩人。這是單一團隊經驗，不是通用標準。

## 勿引用

- 「auto mode 比人安全 6.5 倍」之類的倍數：13.6% 和 89% 來自單一植入指令的受控實驗，不能外推到所有專案與風險等級。
- 「開了沙箱就不會逃出去」：預設設定下仍可能走沙箱外重試。

## 交叉引用

- 指令內容：[[Claude-5-世代的指示精簡原則]]——該頁處理 `CLAUDE.md` 該留什麼，本頁處理移除人工核准後由誰接手。
- Hook 能力：[[Claude-Code-Hook-能力邊界]]——該頁說明 hook 輸出契約，本頁的完成閘門是其「放行判斷」用途的具體案例。
- Review 分流：[[Matt-Pocock-的-PR-瓶頸解法]]——兩邊都按風險決定人工投入，但 Matt 以可逆性為軸，Lydia 團隊以改動類型與風險為軸。
