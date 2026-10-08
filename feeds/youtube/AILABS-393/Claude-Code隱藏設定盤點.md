---
title: Claude Code 設定中值得開啟的隱藏設定
description: 盤點 init 改版、設定匯入、prompt 稽核、skill 用量、auto mode 調校、context 釋放、plan mode、多 session 協作與快捷鍵等鮮為人知的功能
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=i6Q7bXnWGlM
published: 2026-10-05
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - best-practices
  - workflow
  - token-optimization
---

> [!note] 設定名稱來自影片口述
> 下列環境變數、settings 鍵名與指令名是依字幕還原的寫法，大小寫與確切拼法以 Claude Code 官方文件為準。

## 改良版 init：先訪談再寫 `CLAUDE.md`

原本的 `/init` 會讀整個專案，把學到的全寫進 `CLAUDE.md`。問題是 `CLAUDE.md` 只該放 agent 隨時都要記得的事；讀程式碼就能知道的東西不該進去。

Claude Code 團隊自己在用的修法：啟動前在 terminal 設定環境變數 `CLAUDE_CODE_NEW_INIT=1`，必須放在 `claude` 指令之前，session 才讀得到。

開啟後 `/init` 不再直接寫檔，而是先問你的工作方式：

- 要改善現有設定還是從頭開始
- 是否要建立 skills 與 hooks
- 怎麼使用 Git、打算怎麼部署 app

依回答擬一份小計畫等你確認，核可後才動筆。產出的 `CLAUDE.md` 帶有你的工作方式，並附上 skills 與 hooks 作為更好的起點。

## 從其他 agent 匯入設定

從 Codex、Cursor 等轉來時，不必從零開始。執行 import 指令並帶上原 agent 名稱，Claude Code 會列出可複製的項目（該 agent 的指令檔、已連接的 MCP 等），等你勾選後，建一個含複製步驟的 skill，再用它把選定項目搬進 Claude Code。

## 定期稽核指令檔：prompt audit

模型持續進步，為舊模型寫的指令對新模型不再有幫助，反而塞滿 context、讓回答變差。一份份手改太耗時，可用 `/claude-api` 指令後接 `prompt audit`：

- 讀取整套設定，用 sub-agent 分別檢查各部分
- 產出問題清單與建議修法
- 請 Claude 套用後，只留下仍有幫助的指令

最需要跑的時機是**新模型剛推出時**，那時過時的指令最多。

## 清理沒在用的 skill：skill doctor

多數 skill 很少被用到，卻一直占著 context。`/skill-doctor` 會列出：

- 每個 skill 的使用頻率與最後使用時間
- 每個 skill 在 context window 中占用的 token 數

據此請 Claude 刪掉不用的 skill。另外 `/skills` 會列出所有 skill，按 `T` 可依 token 占用由小到大排序。

## 讓 auto mode 學會你的習慣

不帶參數啟動 Claude Code 時進入 auto mode，Claude 會自行放行安全的指令。但 auto mode 不知道你平常放行哪些指令。

- **auto mode setup 指令**：讀專案與過去的 session 紀錄，把 auto mode 規則調成符合你常放行的指令；顯示新設定等你核可後才更新
- **`/fewer-permission-prompts`**：若不想改 auto mode 本身的設定，改用這個。它搜尋過去 session 中最常用的指令與工具，只挑**唯讀、不改動任何東西**的，加進 allow list，存在當前專案的 settings 檔。長任務可放心讓它跑，不用擔心改到不想改的東西

## 釋放開場就被占用的 context

長任務需要盡量多的空閒 context，但有一部分在你打字前就被占了。

- **Claude app 的 connectors**：Notion、Slack 等在 Claude app 加的 connector 會載入每個 Claude Code session，即使從沒用過。在 `~/.claude/settings.json` 設 `disableClaudeAiConnectors: true`，對所有 session 生效，Claude app 的 MCP server 不再出現。不必自己開檔，請 Claude Code 代改即可
- **artifacts**：做設計時 Claude 會先產 artifact 在瀏覽器開頁面確認方向，但產 artifact 的工具同樣常駐每個 session。不需要時在同檔設 `enableArtifact: false`，之後無論怎麼要求都不會產 artifact

## 為使用 AI 的 app 建 eval

`/claude-api` 另有兩個子指令：

- **build eval**：建立一組測試，檢查 app 在不同情境下的表現。測試只寫一次，之後每個新版本都跑同一組
- **hill climb**：反覆修改 app、每次改完跑測試並評分，只保留分數比前一次高的修改

兩者每次執行都會花真實 API 費用（每個測試都呼叫模型）。若 app 本身不呼叫任何模型，build eval 仍有用：它會走過 app、規劃測試，不使用 API。

## Plan mode 的兩個修正

**找回「清除 context 再實作」選項**：plan mode 寫完計畫後會請你選 permission mode 開始實作，以前還有清除 context 的選項，現在不顯示了。清掉的好處是規劃階段的來回不會留在實作時的 context，Claude 只帶著計畫開工。在 `~/.claude/settings.json` 設 `showClearContextOnPlanAccept: true` 即恢復。

**計畫存放位置**：清掉 context 後計畫不會消失，而是存到 `~/.claude/plans/`，不論在哪個專案都集中在這。若想放在專案內方便與協作者分享，在 settings 加 `plansDirectory`，值設為專案內的資料夾名稱。

## Output style

`/output-style` 列出可選風格，共五種：

| 風格 | 行為 |
|---|---|
| default | 未改動時的預設 |
| proactive | 先動手而非先規劃 |
| concise | 回答比平常更短 |
| explanatory | 多解釋自己在做什麼 |
| learning | 要求你自己寫部分內容，邊做邊學 |

指令後接風格名稱即可切換。

## 顯示 thinking 摘要

以前按 `Ctrl+O` 可看推理摘要，現在預設不顯示。在 `~/.claude/settings.json` 設 `showThinkingSummaries: true` 恢復。

## Focus mode：長任務後免捲動

Claude Code 平常會顯示每一步的每個變更，長任務後要往上捲很久才找得到 prompt 與答案。focus mode 只顯示你的 prompt、Claude 的答案與簡短的工作摘要。

1. 執行 `/tui` 設為 full screen（focus mode 只在全螢幕模式運作）
2. 執行 `/focus`

執行中仍看得到 Claude 在做什麼、讀哪些檔，但完成後那些步驟會從畫面消失。

## 支線任務：branch、fork、subtask

| 指令 | 行為 |
|---|---|
| `/branch` | 複製當前對話並開成新 session，在副本試新想法、原 session 保留進度；仍需自己下 prompt |
| fork | 類似 branch，但在背景啟動副本並直接交付任務；主 session 照常使用，任務完成後背景 session 自行結束；一定會開新 session |
| subtask | 在當前 session 內交給 sub-agent，且該 sub-agent **帶完整 context**（一般 sub-agent 是全新 context，只拿到主 agent 給的 prompt） |

## 多 session 協作

**session 間互相傳訊**：同一專案開多個 session 時，各自只知道自己的對話。執行 list agents 指令可看到能聯繫的 session。例如 A session 需要 B 已經查明的資訊，直接請 A 傳訊息問 B，即使 B 還在工作也能拿到答案並繼續。

**提問逾時自動作答**：Claude 提問時會停下等回覆，沒盯著那個 session 就不知道它卡住了。在 `~/.claude/settings.json` 加 ask user question timeout 設定，設 60 秒或任意時間，時間到 Claude 自選建議答案繼續做。但只在不需要你也能前進時才這樣做；若必須由你回答才能繼續，它會一直等。

**通知**：`/config` 往下找 local notifications，選擇通知方式（影片選 terminal bell），Claude 完成或需要回答時會通知你。

## 模型分派

- **opusplan**：`/model opusplan` 讓 plan mode 用 Opus、其餘用 Sonnet。強模型負責規劃、實作跑 Sonnet；Sonnet 吃的額度比 Opus 少，對 Pro 方案（較快撞上限）最有意義
- **統一 sub-agent 模型**：sub-agent 預設用 session 同一模型或由 Claude Code 挑選。設 `CLAUDE_CODE_SUBAGENT_MODEL` 為想用的小模型，再設 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`——少了後者，sub-agent 自己的定義檔仍可指定別的模型；若想保留這彈性就不設。兩者都放 `~/.claude/settings.json`，Claude Code 啟動時讀取，下個 session 起生效

## 快捷鍵

| 快捷鍵 | 作用 |
|---|---|
| `Ctrl+S` | prompt stashing：暫存寫到一半的 prompt 並清空輸入框，送出另一則後原 prompt 自動回來 |
| `Ctrl+Y` | 誤清整段 prompt 時還原被刪的文字 |
| `Ctrl+_` | 復原上一次對 prompt 的修改 |

## Powerup：內建互動教學

`/powerup` 在 Claude Code 內提供短課程，每課以動畫 demo 展示一項功能，邊用邊學。
