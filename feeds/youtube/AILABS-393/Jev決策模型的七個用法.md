---
title: 現在就該用的 Jev 實用案例
description: 介紹 TypeSafe 的 Jev 決策模型特性，以及接進 coding agent 的七個用法：compaction、文件規則檢查、skill 挑選、檔案搜尋、code review 分流、瀏覽器測試與規則強制
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=2nc_QMuNp18
published: 2026-09-28
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - ai-agent
  - token-optimization
  - workflow
---

> [!note] 字幕來源
> 取得的字幕為阿拉伯語配音軌，內容依該字幕翻譯整理。

影片宣稱 Jev 是目前最快的模型；最大的效益出現在把 Jev 接進日常使用的 coding agent。實測找出七個 Jev 影響最大的位置，不只讓 agent 更快更便宜，也解決 agent 一直存在的某些問題。

## Jev 是什麼

Jev 是 TypeSafe 公司開發的 AI 模型，屬於**決策模型**：

- 不像 Claude、GPT 以文字作答，而是從一組既定選項中挑一個——yes/no、一份清單、或對任何東西打分
- 選擇時附帶 **confidence value**，表示它對該選擇有多確定
- 速度快得多：Claude、GPT 逐 token 生成答案，Jev 一次回答所有問題，每個決策只需幾分之一秒
- 便宜得多：不產生 token，只付送進 Jev 的輸入費用，輸出完全免費
- 讓 Claude 自己做這類決策也行，但它得思考並寫出每個答案，多花時間與用量

限制：Jev 不是用來在 Claude Code 或 Codex 內取代既有模型的。它不寫文字，因此**不能寫程式、也不能讓模型使用工具**，只能在這類工具內當決策者。

## 取得 API key

- TypeSafe 平台本身目前因需求暴增暫停新註冊
- 也可透過 OpenRouter 或 Vercel AI Gateway 取得，兩者都是用單一 key 存取多家 AI 模型的平台
- 影片選 Vercel AI Gateway：到 Vercel dashboard 的 AI Gateway → API keys 頁建立 key。**key 只顯示一次**，要立刻複製
- 在 terminal 用 `export` 存成環境變數；在同一個 terminal 開 Claude，它就能讀到並使用

## 1. 更快的 compaction

一般 compaction 把整段對話送給模型，按一組指示要它摘要，可能很耗時。Jev 適合判斷某件事重不重要：讀完對話後挑出對話與模型回覆中真正重要的部分，取代模型預設的摘要。

- 現成 plugin：**fast Jev compaction**，用 Jev 的決策取代 compaction 摘要
- 該 repo 只支援 TypeSafe 自家平台，不支援 Vercel AI Gateway。影片把 plugin 複製進專案，請 Claude Code 小幅修改以支援 gateway
- plugin 用 hook 讓 Claude 不走一般 compaction 指令的流程
- 因為放在專案資料夾而非從 marketplace 安裝，需請 Claude 更新設定以辨識這個 plugin
- 裝好後照常執行 compact 指令，hook 接手取代原流程，通常不到一秒完成
- 門檻：session 用量低於 25% 時不呼叫 Jev，改走 Claude 模型的一般 compaction，確保只在效益大時才用 Jev API

## 2. 文件規則覆蓋檢查

專案有大量描述功能需求的文件，agent 很難全部追蹤；而且實作功能的就是預設模型本身，不能讓它自己當裁判。

影片建了一個 hook：Claude 每次修改控制 app 存取權限的檔案時觸發，問 Jev「文件中的每條規則是否都有對應測試」，找出寫在文件裡卻從未被測試的規則。

使用方式：請 Claude 檢查 app 的某個部分，它會載入 Jev skill 列出缺測試的規則，再依 Jev 的報告請 Claude 補寫測試。

## 3. skill picker

agent 只把 skill 的名稱與描述載入 context window，但專案用了很多 skill 時，模型得在 context 中考慮全部，再決定用哪個、不用哪個。這個選擇交給 Jev 快得多。

影片建的 **skill picker** hook：

- 像 Claude Code 一樣讀所有 skill 的名稱與描述
- 讀你的請求，挑出合適的 skill；請求不需要 skill 就不挑
- 每次送出請求時先跑，再告訴 Claude 該用哪個 skill，Claude 不必自己逐一推斷

實測每次請求後 hook 都會觸發，挑 skill 的速度比沒有 Jev 時快得多。

## 4. 更快的檔案搜尋

模型要在專案中找檔案時，會啟動名為 Explore 的 agent：在獨立 context window 中執行、精準回傳需要的檔案，避免無關檔案內容塞滿主 agent 的 context。Claude 原本預設用 Haiku 跑 Explore，後來改成與主 session 同一模型——若主 session 用 Opus，Explore 也跑 Opus，每次搜尋都更慢更貴。

做法：建一個 skill，讓 Claude 用 Jev 做 Explore 的工作。也可以建一個只在此專案取代 Explore 的 agent，但影片選 skill，因為 skill 可以存放所需的腳本等資源。

skill 分兩步：

1. 一般關鍵字搜尋，找出可能與問題相關的檔案
2. Jev 依各檔與問題的相符程度評分，每次 20 個檔，Claude 只開排名最前的少數幾個

實測 1.6 秒為 35 個檔案排序，正確的檔案排在第一。

## 5. code review 前置分流

實作功能的 agent 不該同時負責驗證，所以頻道總是讓另一個模型 review。問題是完整 review 很慢，因為 Claude 通常逐步進行。

做法：在 review 開始前加 Jev。它**不取代 Claude 當 reviewer**，只是額外的檢查步驟：

- Jev 讀變更，回答七個 yes/no 問題，例如這個變更是否真的符合規則允許、是否本來就是該改的東西
- 全部回答「否」→ reviewer 只跑一輪快速檢查
- 任一回答「是」或 Jev 不確定 → 照原本方式完整 review

效果：高風險變更被正確檢查，小變更快很多結束。

## 6. 瀏覽器測試

agent 開瀏覽器像真人一樣操作 app，能找出只有實際使用時才會出現的問題。給 Claude Code 瀏覽器工具後，模型會點各種按鈕、自己決定下一步點哪裡。這個「點哪裡」的決策可交給 Jev：最終判斷 app 是否正常仍由主模型負責，但 Jev 決定下一步更快。

影片請 Claude 建一個專用 skill：

1. 開啟 app，列出頁面上所有按鈕與連結
2. Jev 挑出最接近目標的元素並點擊
3. 從下一頁再列清單，重複直到 Jev 判定任務完成或頁面卡住

實測用它分別以 admin、manager、employee 登入，確認各角色只能存取被允許的頁面，再由 Claude 對照文件中的規則。之後要求在瀏覽器檢查 app 時就會載入此 skill，比一般方式省下大量時間。

## 7. 強制遵守規則

agent 有時會偏離事先在規格中規劃好的內容。`CLAUDE.md` 的規則只是指示，模型多數時候遵守，但不是每次。

做法：建 hook，因為 hook 每次都會執行、模型無法繞過。專案中有許多分屬 app 不同部分的規則檔：

- Claude 要修改檔案時，hook 把修改內容連同該檔的規則送給 Jev
- Jev 回答 yes/no：此修改是否違反任何規則
- Jev 至少 80% 確定違規時，修改被擋下，並告知 Claude 確切違反哪條規則以便修正

實測要求 Claude 建一個直接從瀏覽器讀取員工資料的檔案（違反其中一條規則），Jev 判定違規，檔案建立前就被擋下，Claude 也說明了是哪條規則。
