---
title: 這個新開源工具修好了你的 Claude Code 工作流
description: Agit 把 git 的 repo、branch、commit 套到 agent 對話，支援對話回退、挑訊息、Claude Code 與 Codex 互轉及分享
created: 2026-09-23
updated: 2026-09-23
source: https://www.youtube.com/watch?v=CHHEjuNBxoQ
published: 2026-09-22
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - context-engineering
  - security
---

## 問題：多 session 之間難以共享 context

- session 綁在同一個 agent、同一個資料夾；要換 session 或交給別人，只能請 agent 把 context 寫成檔案。
- 寫出來的交接檔通常只留重點、漏掉細節。
- Agit（agent git）解決的就是這件事：管理單一 agent 內的 session、在不同 agent 之間搬移對話，並能分享給他人接續討論。

## 概念：把 git 套用到對話上

- git 回顧：commit 是一次存檔版本、branch 是可隨時丟棄的實驗分支、push 是上傳到 GitHub 等遠端讓隊友取用、pull request 是請求合併回主線。
- Agit 的對應關係：
  - **repo**：存的是 agent 對話，以及 agent 的記憶（memory）與 skills，而不是程式碼。
  - **branch**：每個 session 一個 branch，同一專案的多段對話彼此獨立。
  - **commit**：存下訊息與 agent 的回應動作，形成可回溯的對話紀錄。
- 關鍵限制：在對話裡「回到過去」**不會還原 app 的程式碼變更**，改變的只是 agent 看到的對話內容。

## 分享與權限

- 需要建立 profile（類似 GitHub 個人頁），用來標示 session 屬於誰、控制誰能存取。
- 本機存的 session 不會出現在 profile 上，要 push 之後才會出現。
- repo 預設 private，其他人看不到；private repo 的對話總儲存量上限 1 GB。
- 可轉為 public：Agit 會先跑多項檢查再請你確認；轉公開後他人可複製歷史，**且無法再改回 private**。
- 分享給特定人的兩種方式：
  - **加為 collaborator**：在 settings 面板加入；對方可接續對話，再以 pull request 把自己的成果送回你的 repo。
  - **唯讀連結**：對方只能讀不能改；可設定連結可開啟次數，用完即失效。

## 安裝與初始化

- GitHub repo 提供兩種安裝指令：一鍵安裝器（`create agit` 類指令，同時完成安裝與 coding 工具設定），以及透過 npm 的替代安裝；兩者都是全機安裝。影片作者因一鍵安裝器失敗改用 npm。
- 用 version 指令確認版本。
- 全機安裝**不代表會自動記錄所有專案**，只在你指定的地方記錄。
- 登入流程：先到官網註冊帳號 → 終端執行 login 指令 → 選 browser login 並在開啟的頁面核准 → 用 `whoami` 類指令確認登入帳號與 email。
- 在專案資料夾執行 init 指令，會開啟互動介面：
  - 設定 repo 名稱（預設 unnamed）。
  - 確認專案資料夾正確。
  - 可檢視要儲存的 instructions 與 skills。
  - **auto push**：開啟後 agent 會自動 push 對話；關閉則可之後手動 push。
  - 選擇寫入指示的檔案：`AGENTS.md`（Codex 等工具用）或 `CLAUDE.md`（Claude Code 用）；兩個工具都用就兩個都選，兩檔都會寫入 agent 使用 Agit 所需的指示。
- Agit 另在家目錄的 Agit 資料夾內為每個 repo 建立獨立資料夾，存放對話、memory（事實與決策）、skills（agent 建立、供未來 session 使用的 skill）。
- init 後正常下 prompt 即可，每回合結束 Agit 會在本機存下對話。

## 對話回退（revert）

- 和多數 agent 內建的 rewind 不同之處：不只能回退自己的對話，**別人分享給你的對話也能回退**；同樣只改對話、不改 app。
- 流程：
  1. 先執行 log 指令列出 sessions，選一個 session 後會顯示每個 prompt 與 agent 的回應，旁邊的編號代表每個 turn（一個 prompt 加一次回應）。
  2. 用 revert 指令，格式為 session 名稱後接 `#` 加編號。
  3. 注意：填的**不是要回到的那個 turn 編號**，而是從最後一個往回數、要移除的那些 turn 編號，可在同一指令列出多個。
- 被移除的 turn 仍留在 log 紀錄中，只是 agent 不再看得到。
- 用 resume 指令接續該對話；若要同步更新 profile 上的版本，再執行 push。

## 跨 session 挑訊息（cherry-pick）

- 可把另一段對話的某則訊息帶進目前 session，agent 的回應與動作紀錄會一起帶過來。
- 流程：先用 log 找到來源 session 的訊息編號 → 用 cherrypick 指令指定 session 名稱與訊息編號，加到目前 session 的尾端；可一次列多個編號。
- 同樣只複製對話歷史，**不會套用那些訊息中做過或描述的 app 變更**。

## 跨 agent 接續對話（fork）

- 各 coding agent 預設都不支援把對話交給另一個 agent 接續。
- 過去作法：請 Claude Code 寫下已完成的事與 Codex 需要知道的內容，再請 Codex 讀它後接手。
- Agit 作法：用 fork 指令並選擇 Codex，會從既有對話建立新 session、轉成 Codex 可讀的格式並在 Codex 開啟；原對話保留。
- 可請目前的 agent 幫你組好指令（省得記參數），但要**自己在終端執行**，才能在另一個終端接續對話。

## 機密資料遮蔽與補強 skill

- agent 常經手 API key、密碼，一旦讀到就成為對話的一部分，push 時可能一併外洩。
- Agit 在存對話時會掃描機密，把辨識出的 key 換成 placeholder（標示位置但不含值）；push 前會再檢查一次。影片以假造的 API key 測試，存下的歷史確實已被替換。
- 限制：API key 通常有固定開頭、固定長度等可辨識模式；由一般單字組成的密碼沒有這些特徵，**即使對話明說「這是密碼」Agit 也可能漏掉**。
- 作者的補強：寫了一個 skill，在對話存檔前向 Agit 註冊密碼——先註冊專案中既有的機密，並要求 agent 在收到新密碼時先註冊再繼續；註冊後 Agit 存檔時就會替換成 placeholder。
- 必須在 session 開始時就加入此 skill：密碼一旦已被存入歷史，事後加 skill 也移不掉；就算刪除該訊息，密碼仍留在歷史中。
