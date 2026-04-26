---
title: Claude Code 指令速查
created: 2026-04-24
updated: 2026-04-26
tags:
  - claude-code
  - cli
---

Claude Code session 層指令，依使用頻率分三梯隊。

## 第一梯隊（幾乎每天用）

- **`/clear`**（別名 `/reset`、`/new`）— 重置 context，開新對話。換任務前必用，前次對話仍可用 `/resume` 找回
- **`/compact [instructions]`** — 壓縮對話保留主線。可加指令：`/compact 保留修改的檔案清單`
- **`/btw <問題>`** — 側邊提問，不進 history、不打斷主任務、無 tool access。問「為什麼選這個方法？」之類的快速確認
- **`/rewind`**（別名 `/checkpoint`、`/undo`；或 `Esc+Esc`）— 回到任一 checkpoint，可還原 conversation / code / 兩者都還原。試了不好直接復原，零風險

## 第二梯隊（常用）

- **`/context`** — 以色塊視覺化 context 用量，顯示哪些工具最耗 token，也給出優化建議，判斷該不該 `/compact`
- **`/model`** — 切換模型（Opus / Sonnet / Haiku 等），左右鍵同時調整 effort
- **`/usage`** — 查 token 額度與 session 費用，別名 `/cost`、`/stats`
- **`/config`** — 開設定介面（theme、thinking mode、recaps 等），別名 `/settings`
- **`/fast [on|off]`** — 切換 fast mode（Opus 4.6 加速輸出）
- **`/copy [N]`** — 複製最後 N 個回應到剪貼簿；有 code block 時彈選擇器；SSH 下按 `w` 改存檔
- **`/voice`** — 語音輸入，支援 hold / tap / off 三種模式
- **`/statusline`** — 設定常駐狀態列。自然語言描述想看的資訊（model、context %、git branch、cost），設一次長期用
- **`/rename [名稱]`** — 為 session 命名。跑多個 session 時必用，不命名根本分不清哪個是哪個
- **`/color <顏色>`** — 設 prompt bar 顏色（red / blue / green / yellow / purple / orange / pink / cyan）。搭配 `/rename` 視覺區分 session
- **`/skills`** — 列出可用 skills，按 `t` 按 token 排序，確認哪些 skill 已載入

## 第三梯隊（依場景用）

- **`/plan [描述]`** — 進入 plan mode，Claude 只提計畫不動程式碼。可直接帶描述：`/plan fix the auth bug`
- **`/ultraplan <prompt>`** — 在 ultraplan session 起草複雜計畫，瀏覽器確認後遠端或本地執行。適合大型架構規劃
- **`/branch [名稱]`**（別名 `/fork`）— 從當前對話開分支，原對話保留，可用 `/resume` 切回。想試不確定的方向時用
- **`/effort [level]`** — 調整推理深度（low / medium / high / xhigh / max）。簡單任務設 low 省 token
- **`/loop [interval] [prompt]`**（別名 `/proactive`）— 本地定期重複執行。`/loop 5m check if the deploy finished`
- **`/schedule`**（別名 `/routines`）— 雲端排程任務，電腦關了也會執行，搭配 `/loop` 本地版使用
- **`/focus`** — 只顯示最後 prompt、tool call 摘要與最終結果，隱藏過程；再次執行切回。需 fullscreen 渲染（`/tui fullscreen`）
- **`/resume [session]`**（別名 `/continue`）— 恢復指定 session。`claude --continue` 接最近一次，`claude --resume` 開選單
- **`/diff`** — 互動式 diff 檢視器，左右切換 git diff 與每個 Claude turn 的變更
- **`/batch <指令>`** — 大規模平行改動，自動拆成 5–30 個獨立單元各跑一個 worktree agent
- **`/autofix-pr`** — 監控當前 PR，CI 失敗或 reviewer 留言時自動推修復（需 `gh` CLI）

## 偶發使用

- **`/ultrareview`** — 深度多 agent 程式碼審查，跑在雲端 sandbox
- **`/review [PR]`** — 本地 session 審查 PR，深度審查用 `/ultrareview`
- **`/security-review`** — 分析當前分支待提交變更，掃安全漏洞
- **`/simplify [focus]`** — 審查最近改動的檔案，三個 review agent 平行找重用與效率問題後修
- **`/debug [description]`** — 啟用 debug logging，可帶問題描述聚焦分析；mid-session 啟用從當下開始捕捉
- **`/export [filename]`** — 匯出當前對話為純文字；無 filename 彈對話框選擇
- **`/tasks`**（別名 `/bashes`）— 列表與管理背景任務
- **`/status`** — 查版本、模型、帳號、連線狀態；可在 Claude 回應中執行，不必等回應完成
- **`/doctor`** — 診斷安裝、認證、設定問題，按 `f` 讓 Claude 自動修復
- **`/sandbox`** — 開啟 / 關閉檔案 + 網路隔離沙箱，減少權限提示
- **`/permissions`**（別名 `/allowed-tools`）— 管理工具權限白名單，支援 wildcard 語法（如 `Bash(npm run *)`）
- **`/fewer-permission-prompts`** — 掃描 session 歷史，找安全但一直跳確認的指令，產出建議白名單
- **`/memory`** — 編輯 CLAUDE.md / 啟用或停用 auto-memory
- **`/init`** — 互動式初始化專案 CLAUDE.md；設 `CLAUDE_CODE_NEW_INIT=1` 也引導建立 skills / hooks / memory
- **`/add-dir <path>`** — 在當前 session 加入額外工作目錄供 Claude 讀寫
- **`/tui [default|fullscreen]`** — 切換 terminal UI 渲染器；`fullscreen` = 無閃爍 alt-screen，含 `/focus` 支援
- **`/team-onboarding`** — 分析近 30 天 session，產出團隊上手指南
- **`/insights`** — 分析歷史 sessions，整理互動模式與 friction points，適合週期性回顧
- **`/recap`** — 手動產生當前 session 一行摘要（離開 3 分鐘後也會自動產生）
- **`/hooks`** — 查看目前載入的 hook 配置

## 來源

- [Commands](https://code.claude.com/docs/en/commands)
- [Interactive mode](https://code.claude.com/docs/en/interactive-mode)
- [Statusline](https://code.claude.com/docs/en/statusline)
- [Checkpointing](https://code.claude.com/docs/en/checkpointing)
