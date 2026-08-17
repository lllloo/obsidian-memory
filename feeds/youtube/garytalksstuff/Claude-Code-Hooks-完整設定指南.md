---
title: 精通 Claude Code Hooks：必備設定完整指南
description: 拆解 Hook 的 Event、Matcher、Handler 三層架構，說明它與 CLAUDE.md 的強制性差異，並示範金鑰攔截與文章審查兩個實例
created: 2026-08-17
updated: 2026-08-17
source: https://www.youtube.com/watch?v=rLNGSDYkK-w
published: 2026-08-16
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - hooks
  - automation
  - workflow
  - security
---

## Hook 與 CLAUDE.md 的根本差別

CLAUDE.md 是給模型看的提醒紙條：它提供指示，模型會盡力遵守，但不保證每次照做。所以就算寫了「改完程式一定要跑測試」「執行危險 Git 指令前要先停下來」，模型仍常忘記。

Hook 則是 deterministic 的強制機制，由 Claude Code 這套軟體在背後掌控。設定的時機一到，軟體直接介入執行，不經模型判斷。比喻是便利商店的自動門——有人走進感應區，門就開，沒有商量空間。

三者的分工判準：

- 一次性任務 → 對話中直接講
- 專案通用規則與大方向 → 寫進 CLAUDE.md 當參考
- 特定時機到就絕對必須執行、不能承受被忘記的風險 → 做成 Hook

Hook 的原理在 Claude Code 與 Codex 之間通用，判斷方式可互相沿用。

## 設定檔的三層架構

Hook 就是 JSON 格式的設定，通常放在專案資料夾的 `.claude/settings.json`。不需死背，只要理解三層：

| 層 | 回答的問題 | 語法檢查範例 |
|---|---|---|
| Event | 什麼時候發生 | `PostToolUse`（工具剛調用完的瞬間） |
| Matcher | 具體要攔截哪個操作 | 只鎖定修改程式碼的動作 |
| Handler | 最後要做什麼動作 | 呼叫本機的語法檢查腳本 |

## 十個核心 Event

Claude Code 目前有多達 31 種 Event，但按系統工作階段分類，抓十個核心的就夠。

第一階段：系統啟動與接收指令

- **SessionStart**：開啟對話的瞬間觸發，不論是開新對話、接續舊紀錄或輸入 clear 清空畫面。GitHub 熱門專案 Superpowers 就用它強制在每次對話載入 Skill，對付 AI 載入 Skill 的隨機性。
- **UserPromptSubmit**：按下 Enter 送出 prompt 的那一刻觸發。開源專案 Claude-Mem 用它攔截提問，在背後呼叫 worker-service 從資料庫撈出相關記憶再塞回給 Claude Code，解決跨對話失憶問題。

第二階段：工具即將被調用（適合安全防呆）

- **PreToolUse**：工具正準備被調用前觸發。Matt Pocock 的 Skills 用它檢查 tool call 內容，發現 `git reset --hard` 這類會洗掉程式碼的指令或危險的 git push，就當場中斷並告知沒有權限。

第三階段：工具執行完畢（適合快速驗收）

- **PostToolUse**：工具成功執行後觸發。前端設計 Skill Impeccable 在此把關，Claude 一改完 UI 檔案就掃描揪錯——例如圖片標籤的連結是空的，或字體顏色太淡（直接計算文字與背景的數學對比值），不符標準就自動要求修正。

第四階段：任務結束與特殊狀況

- **Stop**：這一回合對話完全結束時觸發。Impeccable 刻意把排版節奏、配色和諧度這類深度美感檢查留到 Stop，因為它會把整個工作階段改過的檔案統整起來做一次總體檢；每改一行就跑深度檢查會嚴重拖慢開發。cross model review 的做法也是用 Stop 在 Claude 寫完 plan 時呼叫 Codex 做 peer review。
- **Notification**：通知提醒，可設成桌面通知或提示音，讓 Claude 在背景工作時不必一直守著螢幕，需要確認權限或回答問題時才被叫回來。
- **SubagentStart / SubagentStop**：主 Claude 派 subagent 開工與交回結果時觸發，適合在開始前補上任務規則與品質要求、做完後檢查產出有沒有達標。
- **PreCompact**：對話太長、Claude 自動濃縮前觸發。若每次濃縮都漏掉關鍵決策、目前進度或不能更動的規則，可用它在濃縮前先把重要資訊整理保存下來。

第一次接觸只要先記住四個：SessionStart、PreToolUse、PostToolUse、Stop。

## Matcher 的篩選與收斂

Matcher 從所有可能出現的動作裡挑出這個 Hook 真正要處理的目標。例如 Matcher 設為 `Edit` 和 `Write`，代表只關心修改檔案的動作，讀取檔案、搜尋資料或執行其他工具都不會往下跑。

需要更細的話，下面還能再加 if 條件，例如只檢查副檔名 `.ts` 的程式碼。條件全符合才交給 Handler。

## 五種 Handler

Handler 決定條件符合後實際要做什麼，目前有五種類型。

- **command**（最常用）：直接執行電腦上的指令或腳本。例如改完程式碼自動跑 lint、用 Prettier 整理格式，或在執行指令前先跑檢查程式擋下危險操作。
- **http**：把 Hook 收到的資料傳到外部服務，例如工具執行失敗時自動把錯誤訊息送到 Slack。
- **mcp_tool**：直接使用已連線的 MCP 工具，例如每次開工自動從 Jira 抓回今天的任務當背景資訊。
- **prompt**：把事件資料連同事先寫好的檢查條件交給另一個 AI 模型判斷。這個 AI 只根據收到的資料回答，不會自己開檔案或搜尋。適合檢查 commit 訊息是否符合團隊格式這類判斷。
- **agent**：叫起一個 subagent，並交給它事件資料與驗收條件。subagent 可以先讀檔案、搜尋程式碼、執行測試，查清實際狀況後再回傳結果。適合在 Claude 宣稱完成時，對照原始需求實際跑測試驗收。

prompt 與 agent 的差別在於：prompt 拿現有資料直接回答，agent 可以先動手查清楚再回答。

注意每個 Event 支援的 Handler 類型不同——有些可用 prompt 和 agent，有些只能用 command、http 或 mcp_tool。設定前先請 AI 查官方文件確認搭配。

## 實例一：Git commit 金鑰攔截（command handler）

需求講給 AI 聽時只要交代兩件事：什麼時候啟動、啟動後做什麼。

> 請幫我在全域設定裡建立一個 Hook：每當你準備執行 git commit 時，先檢查這次要提交的內容，如果包含 .env 檔案或疑似 API 金鑰就把提交擋下來並告訴我是哪個檔案有問題；沒發現就讓提交正常繼續。完成後請測試「有敏感資料會擋下」與「沒有敏感資料會放行」兩種情況。

產出的設定：

- Event：`PreToolUse`
- Matcher：`Bash`（只有準備執行終端機指令時才叫起檢查程式）
- Handler：command，執行名為 Git Commit Secret Guard 的檢查程式

放在使用者層級的 `.claude/settings.json`，所以不論在哪個專案，Claude 準備 git commit 都會經過這道檢查。雖然 Matcher 會在每個 Bash 指令前叫起它，但程式會先判斷這次是不是 git commit，無關就安靜結束；真要提交時才檢查 `.env` 檔案、私鑰、憑證或疑似 API 金鑰。

## 實例二：文章 AI 味把關（需要質化判斷）

金鑰與 `.env` 有明確判斷規則，用程式比對就夠。但像「文章有沒有 AI 腔」這種質化判斷，做法是：

> 請建立一個 Hook：每當你寫完一篇 blog 文章、準備結束工作時，啟動一個 agent 讀取剛產出的文章，呼叫去除 AI 寫作痕跡的 Humanizer Skill 檢查有沒有 AI 味。發現問題就把有問題的段落和原因交回給你繼續修改，檢查通過才能結束工作。

產出的設定：Event 用 `Stop`，Handler 仍是 command，執行一支 Humanizer Gate 檢查程式。這支程式本身不判斷 AI 味，它負責找出這次修改過、還沒通過檢查的文章，再要求 Claude 開 agent 呼叫 Skill 審查。文章若之後又被修改，原本的通過紀錄會失效，下次結束前要重新檢查。

## 建好之後必檢查的兩件事

**觸發範圍夠不夠精確**：範圍設太大會在許多無關操作中被叫起，浪費時間又打斷工作。做法是 Matcher 先縮小範圍、Handler 裡再檢查更細的條件——就像上面用 Matcher 鎖定 Bash，再由檢查程式判斷是不是 git commit。

**Stop Hook 有沒有設定結束條件**：Stop Hook 每次阻止 Claude 結束都會要求它繼續工作，修改完再次準備結束時同一支 Hook 又啟動。沒有明確通過條件就可能一直退回、修改、重檢查。Humanizer Gate 的做法是記錄目前版本是否已通過，通過後只要文章沒再被修改下次就直接放行；連續三輪還是沒過就停止退回，交給人工確認。

## 搬到 Codex 的兩個差異

Claude Code 的設定不能直接複製到 Codex，但判斷方式（先講什麼時候啟動、再講啟動後做什麼）通用。

- **Event 數量**：Claude Code 目前 31 種，Codex 11 種。`PreToolUse` 和 `Stop` 兩邊都支援，所以 `.env` 檢查與 Humanizer Gate 的基本做法都能搬過去。實際建立時不用背 Event 名稱，講清楚時機讓 Codex 自己判斷能不能做到即可。
- **Handler 類型**：Claude Code 支援 command、http、mcp_tool、prompt、agent；Codex 目前真正會執行的只有 command。但這不代表 Codex 做不了需要 AI 判斷的流程——Humanizer Gate 本身就是 command handler 先跑檢查程式，再要求主 agent 呼叫 Skill 完成審查，同一個需求通常仍做得到，只是串接方式不同。

做法建議是把想解決的問題直接告訴 Codex，請它按目前支援的格式重新建立，而不是複製貼上 Claude Code 的設定。

## 起步建議

先找出一件你經常提醒 AI、而且每次都發生在固定時機的事情，把「什麼時候啟動」和「啟動後做什麼」講清楚讓 AI 建第一版，再確認觸發範圍與結束條件。可以從很小的問題開始，例如提交程式碼前檢查金鑰——只要這件事會重複發生、適合在固定時機自動處理，就值得做成 Hook。
