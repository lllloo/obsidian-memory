---
title: Shopify 剛釋出史上最強的 AI coding 工作流程
description: 重建 Shopify 以 Helix 改寫 300 個畫面行動 app 的流程，用 checkpoint 拆分工作、四道 gate 把關，並以 orchestrator skill 串起整個 loop
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=bBMp5tLxShQ
published: 2026-09-24
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - loop-engineering
  - sub-agent
  - workflow
---

Shopify 用 AI coding agent 重建了主力行動 app（約 300 個畫面），但不是一次把整份工作丟給 agent，而是全程走結構化流程，讓 app 維持他們的標準。Shopify 只描述了方法、沒示範做法，影片依其描述重建同一套流程，並在 demo HR 系統（app 已建好、只是加新功能）上實測。

## Shopify 的 Helix 機制

Shopify 把 loop 背後的工具稱為 **Helix**，起因是要用不同於原本的方式改寫 app：

1. 從舊 app 取一個畫面，要求 agent 轉成新版
2. Helix 讀該畫面，拆成稱為 **checkpoint** 的小任務
3. 團隊成員先審查這些 checkpoint
4. 核可後，每個 checkpoint 必須通過四道嚴格檢查，Helix 才開始下一個

Helix 大部分工作交給 sub-agent，主因是**全新的 context window**：長任務全塞在同一個 context，agent 會被資訊量壓垮、遺忘中間的重要事項，品質下滑；sub-agent 讓每個任務有獨立 context。

整個 loop 圍繞兩件事：checkpoint（小塊工作）與 **gate**（工作必須通過的檢查，未通過就不能進下一個任務）。雖然 Shopify 用於 app 轉寫，這套流程也能用來建大型功能，同時確保符合 app 的標準與視覺品質。

Helix 仍是內部工具、無法取得，但 Shopify 公開了整體設定。

## Orchestrator skill：唯一需要下 prompt 的入口

逐步手動跑會需要大量人工介入，因此建了名為 **orchestrator** 的 skill，只需對它下 prompt，其餘部分由它自行處理。只在兩個時間點停下等你：

1. 規劃完 checkpoint 後，等你核可
2. 全部完成後，等你檢查 app、結束這一輪

## Checkpoint：由簡到繁的小塊工作

Shopify 的規則是**一個 checkpoint 正確完成前，下一個不能開始**，並依複雜度遞增排序：最小的任務先做，再做下一個更複雜的。因為每個 checkpoint 都建在前一個之上，早期決策若錯，能在還小、還便宜時修正。

**Checkpoint Planner agent**：把交給 orchestrator 的大功能拆成 checkpoint，寫成 JSON——結構對 agent 好理解、好查找。但 JSON 對人來說是一大塊難讀的結構化文字，所以另做了一個簡單的網頁 viewer 呈現 agent 的規劃。

流程：

1. 告訴 orchestrator 要加的功能，它啟動兩個 sub-agent：一個檢查 app 現況並確認可執行，另一個是 Checkpoint Planner（有疑問會先問你）
2. Planner 寫完所有 checkpoint，orchestrator 開 viewer 給你審：依序顯示每一步、哪些進行中、每個任務怎樣才算完成；並指示 Planner 用淺白語言
3. 同時 orchestrator 交派另一個 sub-agent 規劃測試，詳細寫下每個 checkpoint 如何測試，從一開始就全數文件化
4. 你要求修改或核可。**這一步要仔細審**，確保計畫沒漏功能，以免 agent 實作的時間白費

## Gate：規則只是建議，gate 是硬卡

prompt 或檔案中的規則只是建議，agent 工作時會忘、要一再提醒；gate 不通過就不讓 agent 進下一個任務。

實作方式：建一個在 agent **每次試圖停止時**執行的 hook，回傳 **exit code 2**。這裡的 exit code 2 不是表示出錯，而是提示 agent 繼續做——hook 告訴 agent 工作還沒完成，必須繼續直到通過 gate。概念借自 Ralph loop。

Shopify 的四道 gate：

| Gate | 檢查內容 |
|---|---|
| 1. behavior | 功能是否正常運作 |
| 2. UI | 畫面是否符合預期設計 |
| 3. code review | 底層程式碼品質 |
| 4. human review | 你的最終審查 |

## Gate 1：behavior

涵蓋所有不需要瀏覽器的測試：agent 不靠點擊 app 檢查，而是寫小段程式碼像真人一樣使用該功能，即 test。先規劃測試（前面 viewer 中已看到），agent 才有明確標準驗證功能是否如預期；測試盡量涵蓋各種情況，確認不同輸入下底層流程都正確。

- 把頻道先前的 TDD planner skill 改成適合此流程的版本：為交付的功能規劃並撰寫測試，確保所有不需瀏覽器就能驗證的東西在此階段都測到。例如「主管能否核准某人的請假」用一段程式碼就能直接驗證，不必按按鈕看結果
- 先前規劃測試的 sub-agent 就是依這個 skill 運作

執行順序（核可 checkpoint 後從 checkpoint 1 開始）：

1. orchestrator 啟動數個 sub-agent 撰寫 gate 1 所需的測試；功能尚未實作，測試起初全部失敗
2. 另一個 sub-agent 撰寫此 checkpoint 的程式碼
3. 再一個 sub-agent 執行測試，確認全部通過
4. 全數通過即標記 checkpoint 1 的 gate 1 通過

## Gate 2：UI

直接影響使用者體驗，是最重要的 gate 之一。Shopify 是轉寫 app，設計必須完全一致，因此用 Gemini 模型當完美主義的設計 reviewer——測試發現 Gemini 的空間感很好，能判斷畫面上元素的位置與大小，抓出兩個畫面間細微的間距與尺寸差異。

自己的專案或接案通常沒有可對照的基準，因此先做 HTML prototype：快速展示視覺、嘗試不同方向而不影響主專案，也是拿給客戶核可的依據。

- **prototype skill**：把整個 prototype 做成一個可開啟、可點擊的單檔，並遵循專案自身的指引，例如 design file（列出所有設計細節的結構化檔案；影片用頻道社群的 design.md planner skill 產出）。有了它，prototype 在 UI 實作前就先建好
- **比對 skill**：比對 prototype 與實作的 app，確認視覺相符、互動行為也一致。比對前先確認兩者處於相同狀態（例如表單送出前與送出後是不同狀態）
- 比對不用 Gemini，而是由 skill 從當前 session 啟動新的 Claude session 來做

不是每個 checkpoint 都需要此 gate，因為 gate 1 已在不用瀏覽器的情況下測了大部分東西，viewer 上有些 checkpoint 就沒有這道 gate。需要時 orchestrator 並行啟動兩個 Claude sub-agent：

- 一個審畫面外觀，另一個審互動行為
- **兩者都看不到專案指示**，只依 prototype 與 design file 評判
- 各自回傳差異審查，orchestrator 合併後決定此 gate 通過與否

## Gate 3：對抗式 code review

功能能用、外觀也符合 prototype，但底層程式碼仍可能一團亂。

Shopify 的做法：兩個對抗式 agent 依照 Shopify 寫下的標準檢查程式碼，找到的問題都必須修正，兩個 agent 都核可才算通過。

影片改成一個批評、一個修正的對抗 loop：

- **adversarial agent**：預設程式碼有錯，設法找出問題
- **fixer agent**：修正 adversarial agent 找到的問題
- **adversarial loop skill**：協調兩者之間的溝通

流程：gate 1 與 gate 2 通過後，orchestrator 啟動 adversarial agent 等它審查；沒問題就標記完成，否則啟動 fixer 修正，再讓 adversarial agent 重審，來回直到 adversarial agent 核可為止。

## Gate 4：人工審查

即使 agent 有標準與可對照的基準，也無法從人的角度審查。所有 checkpoint 完成後，你要實際測試功能是否如預期運作，也檢查有沒有哪裡能更好用或更好看，提出小幅修改。

提出修改時，orchestrator 會：

- 把修改轉成新的 checkpoint，同樣走完所有 gate
- 把你的回饋寫進 **learnings 檔**，每個 agent 開工前都會先讀

## 核心原則

agent 過程中可以出錯，但 gate 絕不放行未完成的工作。Shopify 的說法是：一次嘗試可以是錯的，但在不再錯之前不准出貨。

整套流程可自行請 Claude 依描述建成 skill。
