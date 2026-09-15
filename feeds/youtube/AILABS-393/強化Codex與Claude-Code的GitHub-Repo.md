---
title: 讓 Codex 與 Claude Code 設定效率翻十倍的 GitHub Repo
description: 盤點八個補足 coding agent 盲點的 repo，涵蓋圖片轉 3D、瀏覽器驗收、精簡回覆、設計技能庫、規格訪談、SwiftUI、skill 評測與反壞模式檢查
created: 2026-09-15
updated: 2026-09-15
source: https://www.youtube.com/watch?v=Ua0APTMVcb8
published: 2026-09-14
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - ai-agent
  - skill
  - evaluation
  - token-optimization
  - frontend
---

## 背景

- Agent 能完成大部分要求，但仍有自己補不了的缺口；社群已做出不少工具填補，影片挑出實測站得住的八個 repo，其中兩個曾登上 GitHub trending。

## Image to 3JS：圖片轉程式碼 3D 模型

- 從圖片中擷取物件，轉成**完全由程式碼組成**的 3D 模型（Three.js），可放進 landing page、加動畫並讓訪客互動——就是近來常見的滾動式產品頁效果。
- 因為模型是程式碼，可直接請 agent 改顏色、調光線，不需要專業 3D 動畫軟體。
- 用法：把圖片交給 agent，要求用 image to 3js 轉成 3D 模型。agent 分階段建模，每階段與原圖比對，發現差異先修正再加細節。
- 缺點：非常耗 token、耗時；第一次成果常不夠細，需要針對特定部位反覆要求改進。

## Reticle：瀏覽器端的真實驗收

- 痛點：agent 常在功能沒完成時就宣稱完成，通常只確認 app 能載入、設計有套上，背後仍可能出錯。
- Reticle 讓 agent 能追蹤 app 執行時內部發生什麼，找出不運作的原因。
- 安裝後，只要請 agent 建 app，即使 prompt 沒提也會自動使用：自動開瀏覽器、像使用者一樣操作 app 驗證。
- 每個受測部分給出三種結論之一：**成功／失敗／資訊不足無法判定**；失敗時說明原因，讓 agent 修正後重試。
- 自己打開 app 時角落會出現 Reticle 浮動面板，可回看先前的檢查紀錄、看出錯與修復過程。

## Chisel：精簡回覆與工具輸出

- 痛點：模型回覆（尤其工作結束時的總結）越來越長，Claude 系列更明顯，且結構凌亂難讀。
- Chisel 要求 agent 少用字、不寫任務不需要的程式碼，降低花在多餘說明與程式碼上的 token。
- 作者公布的測試：改搜尋框行為的任務，無 Chisel 約 1,500 tokens 回覆，有 Chisel 約 600；與 Caveman、Ponytail 等同類工具比較，Chisel 總 token 也較少。
- 以 Claude Code plugin 安裝，含四個 skill 與三個 hook：session 開始時、送出 prompt 時、agent 使用工具後。
- Claude Code 額外好處：工具回傳資訊時，先移除重複或不必要的文字再給 agent 讀，減少 context 被塞滿、降低成本。
- 輸出結構固定：先講大致做了什麼 → 關鍵改動 → 跳過了什麼。

## UI Skills：設計 skill 的搜尋庫

- 痛點：設計 skill 很多、各有設計原則，要挑出符合風格的那個很費工。
- UI Skills 是收錄多位作者設計 skill 的函式庫，agent 會搜尋並取用最適合的 skill。
- 提供 MCP 與終端機工具兩種形式：
  - MCP：工具常駐在 agent session 中（影片選用此方式）。
  - 終端機：需在 prompt 或專案指示中告訴 agent 何時使用。
- 流程：agent 先依 prompt 搜尋符合的 skill → 篩出相關者 → 取其指示用於建站；不必事先自己挑選、安裝每個設計 skill。

## Ouroboros：先釐清規格、再建構與驗收

- 痛點：沒講清楚 app 要怎麼運作時，agent 會自己決定細節。
- 安裝：依所用 agent 跟著 setup 指令做；它提供一個終端機指令，setup 會把指令接到 agent 上，由 agent 代跑工作流。
- 用法：描述想建的 app，要求 agent 使用 Ouroboros。
- **自我訪談**：針對需求自動產生問題，並用你已描述的內容與專案現況作答；只有「之後容易改、且不超出需求範圍」的小細節才自行補上，會改變 app 本質的決策則暫停問你。所有假設都會記錄下來。
- 答案形成規格計畫；建構前先審查計畫並處理問題，通過後才開始建。
- 建完後檢查是否符合計畫；**建構指示中不包含檢查方式與預期結果**。不符之處交回 agent 修，保留已成功部分，並重跑檢查確認沒弄壞其他東西。
- 提供 dashboard 即時追蹤 agent 進度；若 agent 停滯或達到嘗試上限，會說明停止原因。

## SwiftUI Skills：iOS 原生外觀

- 痛點：專注 iPhone app 外觀與行為的設計 skill 很少；agent 模仿 Liquid Glass（Apple 按鈕、選單的玻璃質感）時只會堆模糊與背景，做出來比較像透明按鈕，還宣稱一樣，也跟不上 Apple 的功能性變更。
- repo 提供以 SwiftUI 正確建構畫面的指示，並持續跟進 Apple 最新變更。內含兩個 skill：
  - Liquid Glass skill：如何在 iOS 26 使用 Apple 內建按鈕與選單、常見錯誤。
  - 針對 Apple 新推出的 iPhone Duo 較寬尺寸的內容排版。
- 裝好後要求 agent 依 skill 指示建 app，會套用 Apple 實際的設計模式，比 agent 自己做更接近原生。

## Caliper：驗證 skill 是否真的有用

- 痛點：skill 一多就難判斷哪些仍有幫助；模型更新後新模型可能本來就會做 skill 教的事，舊 skill 只增加 token 成本。
- Claude Code 的 skill doctor 指令只顯示各 skill 佔多少 context token、哪些沒被用到，無法回答「skill 是否讓成果更好」。
- Caliper 在終端機執行，測試 skill 是否達成設計目的，並比較**有／無 skill** 的 agent 成果。
- repo 附兩個 skill：
  - grill skill：訪談你這個 skill 該做什麼，讓測試反映真實意圖。
  - evaluate skill：協助 agent 建立並執行測試（evals）。每個測試含一個 prompt 與預期結果描述。
- 測試存放在 skill 旁邊，執行紀錄存在 `.caliper` 資料夾供事後查閱。
- 流程：要求 agent 對某 skill 使用 Caliper → 先呼叫 evaluate skill 準備測試，卡住才呼叫 grill skill 訪談 → 以不同 prompt 分別跑有 skill 與無 skill 的多次 run → 產出報告，說明哪些任務 skill 處理穩定、哪些仍需改進，以及改善幅度是否值得多花的 token。
- 同樣的比較也適用 MCP server 與設定中的其他指示。

## Antislop：清除 agent 常見壞寫法

- 依作者撰寫的規則集檢查程式碼，找出 agent 常犯的特定錯誤並回報給 agent 修正，不必自己讀程式碼。
- 規則有些抓會拖慢 app 的多餘工作，有些則反映作者個人偏好的寫法。
- 依 repo 說明在專案中設定；安裝 skill 後，每次交任務 agent 都會跑這些檢查並修掉問題，也可在完成工作後要求做一次最終 review。
