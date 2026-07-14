---
title: 如何設計真正能運作的 Agent Loop
description: 拆解生產環境 agent loop 的四大構件——loop contract、state/log、trigger 類型與 verifier，並介紹 evolve loop 讓 agent 自我優化的做法。
created: 2026-07-14
updated: 2026-07-14
source: https://www.youtube.com/watch?v=JQ_We_ztxrI
published: 2026-07-13
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - claude-code
---

作者分享其公司 Super Divine 過去數月在生產環境跑 agent loop 的實戰經驗：agent 每 30 分鐘自動醒來掃描 codebase、找出改進與錯誤、檢查 server log 並開 PR；每個 PR 由 verify agent 完整測試並附上證據供人審查，低風險修正甚至可直接 merge。此外還有 CRM 生命週期 agent 掃描用戶分群做觸達、支援工單自動處理。重點是「從你 prompt agent 做事，轉向設計一套讓 agent 自行決定該做什麼、執行、驗證並隨時間自我改進的系統」——這就是 Loop Engineering。

真正的難處不在把 loop 拼出來（用 Copilot 或 Codex 誰都做得到，那是簡單的 5%），而在**設計能讓你放心走開的 guardrail**——loop 要能持續安全地交付、並隨時間自我改進。

## Loop 的整體結構

每個內部 loop 都是同一套結構：

- 一份 markdown 檔，同時持有 **loop contract** 與 **state/log**，是 loop 自身的活文件。
- **trigger 層**：真正喚醒 agent 開工。
- **實際執行的 agent**：找工作、做工作、驗證做得對不對，並持續更新文件，讓下一輪更聰明。

## Loop Contract（loop 的憲法）

markdown 檔的核心，三件事最關鍵：

- **Goal（目標）**：贏的樣子長怎樣？是否存在終點線？
- **Boundaries（邊界）**：明確界定哪些 agent 可自行決定、哪些必須升級交給人。
- **SOP**：若有特定 workflow 或原則要求 agent 每次都遵守。

## State 與 Log

讓 agent 記住試過什麼、學到什麼，拆成兩部分：

- **State**：耐久的當前快照——目前假設是什麼、有哪些 backlog、哪些已 ship 但需追蹤。這部分要**刻意保持很小**。
- **Log**：逐輪的 append-only 紀錄。少了它，每天早上 loop 都會重新發現同一批噪音錯誤，浪費 token 追已試過的線索。

小型 loop 大多可把 contract 與 state/log 塞進**同一個檔案**。目錄結構是每個 loop 一個資料夾，內含一份 readme，其他 artifact 也存在該資料夾並在 readme 中被引用。

## Trigger 的四種類型

選對 trigger 類型對降低成本影響很大。current loop 之所以讓人覺得混亂，正是因為 trigger 類型不同。

**1. 連續 for-loop**：Codex／Claude Code 的 `go` 指令，背後就是 while loop——在目標未滿足前（或設定最大來回輪數、token budget）持續「看 contract、做下一步」。適合能拿到即時回饋的場景，如 bug 修復、或 spec 定義明確的複雜軟體實作。

**2. Cron job**：如 Codex automation、Claude Code loop 或排程指令，固定間隔喚醒 agent。loop 與 schedule 的唯一差別是一個跑在雲端、一個跑在同一個 session。

**3. Event-based（事件驅動）**：對特定事件反應，如收到新 email 就喚醒 agent 處理、server 發生事故就立刻叫 agent 去修，適合需即時處理的事。但 Claude Code 與 Codex 都不原生支援——需自架 local daemon process 對外 expose 一個 URL 供 webhook 送通知（例如在 Render 建 webhook 指向本機 daemon 接收失敗事件）。

**4. Combo／workflow（最實用）**：ticker 仍以固定間隔跑，但不立即喚醒 agent，而是先跑一段 script 從資料源程式化檢查是否真有新工作。例如支援收件匣分流 loop 用一段 JavaScript 從 Intercom 撈過去 30 分鐘的更新——有真更新才觸發 agent，沒有就跳過這輪。好處是能把一批工作批次交給 agent、只在真有事時喚醒，成本與 token 效率高得多。

前兩種 trigger 是 Claude Code 與 Codex 開箱即用；後兩種需自建 local script 與 daemon service。

## 執行的 Agent

被喚醒後通常走三個階段：

1. **蒐集訊號**：找出並排序工作。
2. **執行任務**。
3. **驗證**：高風險、高複雜度的任務（如工程工單）在宣稱完成前先由 verifier 把關品質。

簡單任務可由單一 agent 一手包辦三件事；複雜任務則拆成三種角色：

- **Orchestrator**：接 prompt，做研究與規劃。
- **Executor（sub-agent）**：各自在隔離的 worktree 工作，任務可平行跑。
- **Verifier**：測試結果並把證據附到 PR 上，讓人審查更容易。

所有更新都寫回 loop contract 文件。

## Verifier 是高風險 loop 的前提

任何交付高風險工作（真實 production 程式碼變更、對真實客戶發訊）的 loop，verifier 都是前提。要點是讓流程容易、且產出人能輕鬆審查的證據——給 agent 一個能**token 高效地驗證自己工作**的環境。作者提過的做法包括用 Playwright CLI 讓 agent 測試並錄下影片／截圖證據、用 Crabbox 架遠端 sandbox 環境跑測試（不受本機能同時開幾個 dev server 的限制）。作者把這些打包成一個叫 verifier setup 的 skill，可直接丟給 Claude Code 或 Codex 在自己 codebase 建好驗證系統。

## Evolve Loop（自我優化層）

剛起步的 loop 多半不完美，有很多可優化空間（trigger 怎麼設計更省成本、哪些重複的 SOP 可轉成 script）。這些改進很多能由 LLM 自己完成——只要把 agent 的既有設定、過去 run 的 state/log、以及原始對話歷史都交給它去檢視。

做法：每跑 5～10 輪 loop 後，觸發一次專屬的 evolve session，把既有設定與歷史 log 交給 agent，讓它排序並執行改動——可以是 loop contract 本身、過時的 state、或為重複動作新建的 trigger script。前述支援 loop 的「程式化 trigger（只在必要時喚醒）」正是在一次 evolve run 中被自動設定出來的。

## 實例

- **React doctor checks**：用 open source CLI 工具 react-doctor 每天掃 codebase、找出最關鍵的問題自動修。contract 含 scope、boundary（在隔離 worktree 用 sub-agent 修、需跑驗證流程、哪些可自 merge 哪些需人審）、SOP 與 state。自建 dashboard 追蹤 PR 與 health score 變化。
- **CRM 生命週期 loop**：每天監控 DAU，分群為小型 influencer（拉聯盟／分發）、明顯受挫用戶（依 LLM log 判斷）、活躍但未升級者；依優先級與風險，agent 可自動觸達或草擬訊息等人核可。已跑近一個月，文件每輪持續更新。
- **文件維護 loop（documentation maintainer）**：每天喚醒 agent 檢查過去 24 小時 ship 了什麼、diff 是什麼，比對 readme／setup guide／範例／run book，逐處驗證何者真的過時，沒事就結束 session，有事才做小修正並開 PR。contract 有一條關鍵規則 **never rewrite accurate doc to look busy**——因為 agent 的預設傾向是就算沒必要也硬要做點什麼，這條規則能確保它只產出有用的結果。

## Loopery（開源工具）

作者團隊自建並已開源的內部工具，供團隊集中管理所有 loop 的 contract、state、log 與 trigger：可定義前述的程式化 trigger、依最佳實踐建立 contract、儲存原始 run log 供 agent 自我修正，並內建 evolve loop 行為（每幾輪後跳出一個藍點代表一次 evolve run）。附有 dashboard 追蹤開啟中的待辦與效能變化，也可一鍵把某 loop 的所有脈絡複製到本機與 agent 對話優化。內建多個模板（doc maintainer、react doctor loop、定期清理技術債等），複製 prompt 貼進 repo 即會自動建立 loop 資料夾與對應設定。可免費使用，GitHub 連結在影片說明欄。
