---
title: 讓 Jev 搭配 Claude Code 發揮到頂尖水準的工具
description: 實測八個以 Jev 決策模型為核心的工具，涵蓋危險指令攔截、規則檢查、瀏覽器測試、完成度驗證、訊息分流與 SEO 報告
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=jlEMo6Dsh9E
published: 2026-10-07
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - ai-agent
  - workflow
  - security
---

影片測試市面上所有找得到的 Jev 工具，留下八個真正能改善工作流程的。Jev 是 TypeSafe AI 的決策模型，專門回答 yes/no 類判斷；這些工具的共同模式是把「該不該做」的判斷交給 Jev，Claude 負責實際執行。Jev 本身是什麼、怎麼設定不在本片範圍。

API key 方面，多數工具可用 TypeSafe 自家 key，也支援 OpenRouter、Vercel AI Gateway 等提供 Jev 的供應商；預設只吃 TypeSafe key 的工具，可請 Claude 改寫成支援自選供應商。

## Toolgate：比 auto mode 更嚴格的動作攔截

Claude Code 內建的 auto mode 會擋危險指令、放行安全指令。Toolgate 做同樣的事但更嚴：Claude 每次採取行動前，Toolgate 都先問 Jev 是否允許，Jev 說否就擋下。

攔截範圍：

- 任何無法復原的變更
- prompt injection 攻擊
- 下載來的工具試圖把資料送往外部伺服器
- Claude 使用你未授予的權限（例如切到能改動整台電腦的 admin 模式）
- 超出你所交代任務範圍的動作
- 你說要自己決定的事，Claude 必須留給你

安裝步驟：

1. 複製 repo 的安裝指令在 terminal 執行
2. 用 key 指令加入 API key；用 TypeSafe key 可直接執行，其他供應商需從 repo 複製正確的供應商名稱
3. 執行 `toolgate init`：把 Toolgate 接上 Claude Code，並把攔截規則與 API key 存進資料夾，下次開 Claude Code 時讀取
4. 開 Claude Code 給任何任務即開始運作

實測：要求 Claude 刪掉一個資料夾並把檔案搬到另一個資料夾。Claude 沒先複製內容就開始刪，Toolgate 給出 77% 的破壞性風險分數。這種分數通常會要求你確認，但因為跑在 bypass permissions 模式（不問任何權限），Toolgate 直接擋下；之後 Claude 先把檔案複製到安全處才完成任務。

缺點：連真的需要刪除的東西也不讓 agent 刪，這部分得自己處理。

## Abide：逐次檢查編輯是否違反專案規則

Abide 把 Claude 的每次編輯拿去對照你的規則，違規就要 Claude 修。支援 Codex、Claude Code 等多數 coding agent。

它會先把 `AGENTS.md`、`CLAUDE.md` 轉成獨立的規則檔，稱為 **rubric**，供 Jev 閱讀。

安裝與設定：

1. 執行 login 指令，會問兩個問題：用哪種 key（影片選 Vercel AI Gateway）、裝在全部專案或僅此專案（影片選僅此專案）
2. 執行 init 指令：接上 Claude Code，並加入教 Claude 如何配合 Abide 的檔案
3. 新專案還沒有 rubric，需在 Claude Code session 內請 Claude 建立

Claude 建立的 `.abide` 資料夾內含：

- rubric：所有規則的細節
- compile skill：Claude 把指令檔轉成 rubric 時遵循的步驟
- 一份記錄每個轉換步驟的檔案

rubric 會把每條規則轉成 yes/no 問題，因為 Jev 就是回答這類問題的決策模型。影片的 rubric 有 49 條規則，其中 33 條需要 Jev 在執行前判斷。rubric 就緒後，Abide 會標出 Claude 違規之處，Claude 必須修完所有標記才能結束任務。

## Jev Browser：Claude 測、Jev 判斷的瀏覽器測試

Jev Browser 是頻道前一部影片所介紹工具的開源版。運作方式：請 Claude Code 測某功能，Claude 用 Jev Browser 讀取畫面內容，Jev Browser 再把讀到的回傳給 Claude 繼續跑測試。

安裝注意：

- 官方有一行包含所有設定步驟的安裝指令，但實測裝到舊版（Jev Browser 更新頻繁），建議改請 Claude 安裝最新版並直接設定好
- 預設只支援 TypeSafe key，沒有的話請 Claude 修改工具以接自選供應商
- 裝好後在 Claude 中以 MCP 形式提供，所有工具可用

使用時在 prompt 中明示「用 Jev Browser 的工具」，Claude 會多次呼叫它，最後產出列出所有 bug 的報告。實測任務約 2 分鐘完成，不用此工具會久得多。

## Jev Belay：防止 Claude 謊報完成

agent 常在任務其實沒做完時宣稱完成。Jev Belay 這個 plugin 讓 Claude 在真正完成前無法結束，概念類似 Ralph Loop，差別是由 Jev 判斷是否真的完成。

運作流程：

1. Claude 宣稱完成時，Jev Belay 讀取整段對話，找證明任務已完成的證據
2. 找不到就要求 Claude 證明
3. Claude 證明不了，就 re-prompt 要它完成任務

安裝：

1. 複製新增 marketplace 的指令（同時會重載 plugins）
2. 執行 plugin install 指令
3. 回答設定問題：安裝範圍（影片選僅此專案）、TypeSafe API key（沒有可比照 Jev Browser 請 Claude 接自己的供應商）
4. 設定 **threshold**：Jev 要多有把握任務已完成才允許 Claude 停下，影片設 75%
5. 可選開啟 decision log 查看 Jev 的判斷；另有一個選項顯示「若此工具沒介入會發生什麼」，用來比較有無工具的差異

## Jev Steer or Queue：任務中途插話的分流

情境：送出 prompt 後想到漏講的事，於是在 Claude 工作中追加訊息。Claude Code 預設會暫存該訊息，等目前這一步做完就交給 Claude。問題是若新訊息其實可以等整個任務做完，Claude 仍在半途收到，會分心同時做兩件事。

此 plugin 讓 Jev 判斷新訊息該怎麼處理，三種選擇：

| 選擇 | 行為 |
|---|---|
| steer | 目前這一步做完後交給 Claude（即 Claude Code 預設行為） |
| queue | 關於另一個任務、可以等的訊息，暫存到 Claude 做完所有工作後，作為新請求送出 |
| interrupt | 緊急訊息，Claude 立即停下，不等目前步驟結束 |

- 只在 Jev 至少 90% 確定時才依其判斷行動，不確定就不改變 Claude 的行為
- 同時支援 Codex 與 Claude Code
- 安裝方式同一般 plugin，加入 API key 即可；裝好後所有新 session 都會啟用

實測：Claude 建 landing page 時要求改色彩主題，判定比頁面本身更急，直接送進去；不急的訊息則延後。

## Compact Advisor：判斷何時 compact

長 session 必然要 compact，但時機不對會丟掉 Claude 之後需要的細節。Compact Advisor 用 Jev 判斷現在是否適合 compact：看 session 進行到哪、能否在不丟失重要 context 的情況下壓縮。

- 安裝：執行 GitHub repo 上的指令，裝完會開新 session
- 首次執行會問設定問題，例如 API key 與 minimum context
- 之後每次回覆後都會告訴你是否適合 compact

實測觀察：

- agent 回覆結尾有提問時，不會建議 compact
- 沒有待辦問題、已用約 100,000 tokens、且 session 沒有可接續的新內容時，才建議 compact
- compact 品質明顯較好，session 中提過的細節都有保留

## Quicksilver：讓 Jev 代為篩選檔案

Claude 有很大一部分工作是讀大量檔案只為找到少數需要的那幾個。Quicksilver 把 Jev 放在 agent 與檔案之間當決策層：把搜尋轉成快速的 yes/no 判斷交給 Jev，Jev 讀檔並列出候選清單，Claude 只讀清單上的檔案。

- 好處：省 token、Claude 專注在更重要的工作；搜尋由 Jev 處理，Claude 的 context window 保持乾淨
- 安裝：terminal 執行單一指令，之後可在任何任務要求 Claude 使用 Quicksilver

實測：在自家 app 上要 Claude 用 Quicksilver 找出哪些部分沒有遵循共用色彩設定。Jev 約 2 秒檢查 37 個檔案，Claude 省下約 67,000 tokens 的閱讀量。

## Jev SEO：網站搜尋排名分析報告

給 Jev SEO 一個網址，它產出 SEO 報告，呈現 Google 等搜尋引擎找到你網站的難易度。

報告產生方式：

1. 沿連結造訪所有找得到的頁面
2. 跑一組固定檢查，抓 broken link、sitemap 問題等
3. 對每頁問 Jev 同一組問題（例如頁面是否有幫助、標題是否貼合內容），用來評估內容品質

產出：

- PDF 報告，各領域分別評分
- Excel tracker：可逐項打勾的修正待辦清單

Jev SEO 是 skill，照指令安裝後執行 `/jev-seo <網址>`（指令名依影片口述，確切寫法以官方 repo 為準）。完成後給出總分，影片測試的網站約 76 分；報告列出最重要的行動項、指出哪些部分空泛無用，並評估網站是否已準備好被 AI 搜尋收錄、什麼在阻礙網站表現。每次改善網站後可重跑比較。
