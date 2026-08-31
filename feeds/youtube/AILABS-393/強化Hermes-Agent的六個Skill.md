---
title: 讓 Hermes Agent 更強大的 Agent Skills
description: 盤點六個外掛 skill/工具：計畫落檔、跨 agent 委派、終端輸出過濾、安全審查、受限站點抓取與 skill 描述動態檢索
created: 2026-08-31
updated: 2026-08-31
source: https://www.youtube.com/watch?v=WJgxX0Eib6k
published: 2026-08-30
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - workflow
  - token-optimization
  - security
---

## 為何還要外掛 skill

Hermes 內建九十多個 skill，也會把使用者對話中出現的工作流自動封裝成新 skill。但自動生成的 skill 只來自它從使用者身上學到的流程；外部 skill 則是別人已經解掉 Hermes 自己解不了的問題後封裝出來的成品。影片同時指出，這些 skill 大多不綁 Hermes，換到任何 AI coding agent 都能用。

## Planning with Files：把計畫從對話搬進檔案

**要解的問題**：長對話中 agent 會忘記早先講過的細節，必須重講一次；用 Opus 系列模型時更明顯。原因是 context window 中訊息太多，模型得同時關注全部，容易漏掉小細節。

**做法**：把計畫從對話搬進專案資料夾的三個檔案：

- `task plan.md`：把主任務拆成小任務，讓 agent 一次做一件
- `findings.md`：記錄 agent 遇到的每個問題與解法，同樣問題再出現時可直接沿用
- `progress.md`：記錄進度到哪裡

**與一般「把計畫寫成檔案」的差異**：這個 skill 用 **hook** 強制把三個檔案插進 context window，agent 沒有忽略的餘地。多數 agent 不支援 hook，Hermes 是少數支援的。作者自己的測試顯示，開 hook 後 agent 表現明顯較好，不會偏離被指派的任務。

安裝後 hook 會自動裝進 agent。實測時 agent 先建三個檔案、提問並由使用者回答，長 session 結束後定稿計畫並交出三個檔案。

## Delegate：跨 coding agent 的協調者

**要解的問題**：Hermes 已內建 Claude Code skill 與 Codex skill，可把任務直接送過去，但不主動使用——必須在 prompt 裡明講哪些任務給哪個 agent。

**做法**：`delegate setup` 是主 skill，負責協調；另附各 coding agent（Claude Code、Codex、Cursor）的專屬委派 skill。它會自動偵測系統上裝了哪些 coding 工具、判斷各任務適合哪一個，再分派下去。這些被叫起的 agent 以不詢問權限的模式執行，不會停下來等使用者逐項核准。

安裝時會列出 18 個 skill 供勾選對應自己系統上有的工具。使用時以 slash command 叫起 skill 並下 prompt：先辨識已安裝工具，接著給出完整分工地圖（含確切模型名稱與 effort level），使用者核可後才開跑，最後由 Hermes 匯總各 agent 回報成一份總結。

## RTK：在進 context 前過濾終端輸出

agent 跑的每個終端指令都會回傳輸出，而九成情況下 agent 只需要其中一小部分，其餘純粹灌爆 context。RTK 在輸出抵達 context window **之前**就先裁掉不需要的部分，它內建一份 agent 常用終端指令的資料庫，知道各指令的輸出該怎麼濾。例如跑測試時預設只留失敗的測試結果、丟掉通過的。

**注意它不是 skill**，而是裝在機器上、從終端執行的獨立工具。可以直接裝好再叫 agent 用它，但 agent 常會忘記；影片作者因此另外做了一個 skill，內含每個指令的參考說明，讓 agent 知道哪些指令可走 RTK、怎麼用，並要求所有指令改繞 RTK 而非照常直跑。（該 skill 放在其付費社群 AI Labs Pro。）

## Mantis：Google 的安全審查 skill 組

Mantis 是 Google 出的一組安全審查 skill，各自負責審查的不同面向，不分行動 app 或 web app 都適用。安裝指令列在 GitHub repo，執行時會讓你從眾多專門 skill 中挑選——建議全裝，因為它們是整套審查流程的各個環節。例如 `Mantis Plan` 負責在實際開始前規劃審查流程，`Mantis Reflect` 則回頭複查所有發現、確認失敗項有被妥善記錄。

**為什麼放在 Hermes**：app 上線後需要反覆做安全審查，而這不是人會記得主動做的事。Hermes 有 cron job（依排程自行執行的任務），可設定定期對已部署的 app 跑整套審查；因為 Hermes 常駐運行，發現問題時能透過 Slack 或其他已連接平台主動通知。影片作者自己的專案即以此方式運作：把專案交給 Hermes 並要它對程式碼跑整套，持續找出問題並套用修正。

## Agent Reach：存取受限站點

做研究時 agent 常被特定內容擋在門外，因為 Reddit 等許多站點不希望模型使用其內容；但這些站點正是研究價值最高的地方——上面是真人在談問題、觀點與經驗。Agent Reach 讓 Hermes 能存取這類通常被擋的站點，包括 Reddit、GitHub 等超過 15 個平台（含 Instagram、Facebook、Twitter），使用免費方法、不產生費用。影片提到它近期曾是 GitHub trending 第一名。裝好後可直接從 Hermes 對任一平台搜任一主題，它會跑自己的腳本找出相關資訊並回答。

## Skill Retriever：只送相關的 skill 描述進 context

**要解的問題**：skill 真正進 context window 的只有名稱與描述，且會**隨每則訊息一起送出**，好讓 agent 知道這些 skill 存在。單看一則名稱與描述佔比很小，但當 skill 累積到破百、Hermes 用了一段時間後，這些名稱與描述會吃掉 context window 相當大的一塊。

**做法**：Skill Retriever 在 Hermes 呼叫模型**之前**多插一步——把使用者訊息切成模型可理解的小塊，對每個 skill 也做同樣處理，然後把訊息與 skill 清單做比對，只送分數最高的那幾個 skill 描述進去，取代整份清單。

**官方文件宣稱的數字**：整份清單約用 11,000 token，改用後只需 2,300 token，宣稱每輪省下超過 9,000 token。（此為該專案自述數據，影片未獨立驗證。）

**兩層好處**：每則訊息進 context 的量大減，執行成本下降；agent 也不會被與當前提問無關的 skill 分散注意，答案品質更好。它以 plugin 形式提供，Skill Retriever 是其中一個 skill，裝好 plugin 後在 plugins 區啟用即可。
