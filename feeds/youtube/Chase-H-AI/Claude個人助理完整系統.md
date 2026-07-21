---
title: 如何把 Claude 變成個人助理——完整系統
description: 用 email 分流、每日研究簡報與內容再利用三類 skill 自動化雜務，並以 Obsidian 索引結構與 dashboard 收束成可觀測的系統
created: 2026-07-21
updated: 2026-07-21
source: https://www.youtube.com/watch?v=gUv7VqcRzok
published: 2026-07-14
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - automation
  - workflow
  - obsidian
  - second-brain
  - skill
---

## 出發點：先問要自動化什麼

過去談 Claude OS 多半在講系統設計——skill 架構怎麼排、Obsidian vault 怎麼建。這次反過來看實際在跑的設定。

第一個要確立的不是架構，而是：**哪些是無聊、重複、不太需要決策的雜活**。作者把自己的工作切成三桶：

- 生產力／銷售（AI agency 業務）
- 研究
- 內容

其中內容以外的部分，多數人都能對應——只要你在銷售或行銷環境裡，就會有客戶資訊進來要回、有每天要追的動態。

## 生產力／銷售

### Email 分流自動化

每天早上 8:00 讀 Gmail（透過 Claude connector），把過去 24 小時的信分成幾桶：leads、urgent、warm、sponsors、meetings、noise。之後依桶別分頭處理：

- **sponsors**：自動草擬回覆，帶上罐頭內容與 media kit 連結（含報價）。
- **leads**：流程較深。網站上每個 lead 都會填表單留下預算、需求、時程；Claude Code 在分流時一併讀進來。若判斷是真實詢問（信件合理、認真填寫、預算對得上、非亂填），就自動發動 web search 調查對方公司背景，讓你進 discovery call 前先有底。接著給出建議「這是他們想做的事，該不該往下走」——**要不要推進仍由人決定**。點頭後才產出草稿信，附上行事曆連結讓對方預約。
- **urgent**：附上草擬回覆。
- 其餘：只做標記。

最後產出一份 markdown 報告寫進 Obsidian vault，一眼可讀，連不在意的 noise 也列出來。

要自己改寫這套，核心問題是：你平常收哪些類型的信？該怎麼分桶？分完之後你希望 Claude 拿這些資訊做什麼？

### 提案與追蹤

discovery call 之後走 Calendly，會自動寄來含所有討論重點的 recap。把 recap 交給 Claude Code，它產出一份品牌化 PDF：交付內容、工作範圍、報價、簽署欄位，結構是 engagement／timeline／investment 加底部簽名區。同時產生 drive 連結，連同草稿信一併送出。人仍會過目，但省下手工寫提案的時間。

## 研究

關鍵前提是**知道自己的資訊源頭在哪**。以 AI 領域來說就是 Twitter、GitHub，偶爾議題會先在 YouTube 冒出來——大致就這三個。換一個領域來源不同，但架設方式相同。

### 每日簡報（daily brief）

- **GitHub**：用 GitHub API 抓熱門 AI repo，分成幾類——本週新建的 top 10、近 30 天內建立的 top 5、過去 24 小時與過去 30 天成長最快的。前者看什麼是新的，後者看什麼是既有但正在竄升。這塊人工做最痛苦，自動化收益最大。
- **YouTube**：抓趨勢影片，重點是**同時顯示創作者的觀看數與訂閱數**——百萬訂閱拿一萬觀看不值得注意，兩千訂閱拿一萬觀看就代表講中了大家在意的事。
- **Twitter** 與一般 web search：抓大標題。
- 附帶的「內容機會分析」作者評價是 hit or miss；真正有價值的是它撈回來的原始資料。

email 分流簡報與研究簡報**合併成單一的 morning automation**，設定為 Claude Code 內的 local routine，只要電腦開著就會自動觸發。

### X pulse

自建、部署在 Railway 上的應用，24／7 運作，每小時左右透過 Telegram 推送 AI 圈當下最熱的推文，並綁定主要創作者（包含 Claude dev team 與 OpenAI 團隊的人）。有大事發生時立刻知道，不必一直刷 Twitter。

### 隨選研究（on demand）

- **deep research**：Claude Code 內建的 `/deep-research`，是預載的動態工作流。放開跑可以派出上百個 sub agent 做對抗式資訊蒐集——上網找資料、互相驗證正確性、再做綜合。相對於一般 web search 只派幾個 sub agent 瀏覽網頁，這是強化版，但**極吃 token**。
- **YT pipeline skill**：先搜尋與主題相關的 YouTube 影片，把所有 URL 送進 NotebookLM，由 NotebookLM 處理 transcript、做綜合再回傳。透過 notebooklm-py CLI 取得非官方 API。好處是綜合運算在 Google 伺服器上完成，**不消耗自己的 token**。目的是不必看十支影片，而是拿到「共同結論是什麼、哪裡彼此不一致、為何值得在意」。

作者估計光研究這一塊就省下每週 5 到 10 小時。生產力與研究兩側最好合併看待——你回的信、你做的東西，通常都建立在某些研究之上。

## 內容

- **腳本、hook 與大綱**：單一的隨選 skill。作者用 Callaway 的影片訓練出 hook 與轉場的寫法。他本人不寫逐字稿，這比較像腦力激盪工具——重點是 AI 已被特定 skill 校準過，不會只吐通用垃圾，來回幾輪之後想法會在**人**這邊成形。
- **包裝（標題、縮圖）**：縮圖自己做；標題用同樣的心法，讓 AI 看哪些標題表現好、為什麼，但仍是來回討論。純靠自己與一張白紙會很辛苦，把創意全外包給 AI 也不行——這類需要「品味」的事 AI 並不擅長，混合式最有效。
- **內容再利用（content cascade）**：每天中午與晚上 8:00 檢查是否有新影片發布，有的話抓 transcript，改寫成 blog、LinkedIn 貼文與推文。

### 怎麼調出「你的聲音」

這個 skill 最花時間的就是語氣。作者給的做法是一個明確的循環：

1. 給 Claude 一批**完全出自你本人**的寫作範例。
2. 要它把這些轉成 skill。
3. 讓 skill 跑出一個範例。
4. **狠狠地批評它**——逐點指出哪裡錯、哪裡對、你會怎麼改。
5. 把修正後的版本回饋給它，它更新 skill，再產新範例，再批評。

重複約十次，之後在實際使用中繼續重複，才會磨出真正堪用的 skill。**不要相信「一次成形、自我改進」的說法**——凡涉及個人語氣的寫作，human in the loop 是必要的。

## 收束成系統：Obsidian 與 dashboard

### 為什麼要 Obsidian

Obsidian 本身**並不改變 Claude Code 的運作方式**，知識圖譜也只是漂亮的視覺化。它的實際作用是把個人系統產出的東西組織起來，長出一張交給 Claude Code 的地圖，讓提問能被快速且正確地回答。

### Karpathy method 的資料夾結構

把所有東西單純想成資料夾：

- 最上層是 **vault**。
- 底下分 **raw**（未經整理的原始資料，例如研究倒出來的一堆東西）、**wiki**（把 raw 綜合成報告）、**output**（把報告再變成簡報之類的成品）。
- 每層底下再依用途細分子資料夾。

關鍵在於**每個資料夾都放一份 index 文件**，等同該層的目錄，說明裡面有什麼、各在哪裡。這樣 Claude Code 往下鑽時永遠知道該去哪。

所謂「迷路」不是真的迷路，而是**成本問題**：什麼都靠 grep 並不高效，檔案結構愈大，沒有組織就會推高 token 成本，同時降低準確度。這套結構本質上是給 Claude Code 的檔案櫃，檔案櫃與地圖才是價值所在，知識圖譜只是副產品。

### Dashboard 的角色

skill 抓了信、做了研究、產了內容——資訊去哪了？能不能一個地方全看到？終端不適合承擔這件事，Claude Code 桌面應用也不是為此設計。因此才有 command center／web dashboard：

- Obsidian Base 版面：各項 metrics、token burn、所有自動化列表（可一鍵執行）、audience 區塊（morning report 的另一種切法）。
- web app 版本內容一致：metrics、skills，下方可直接開啟報告文件，與 Obsidian vault 內的是同一份。

三者分工是：**dashboard 給你可觀測性，Obsidian 負責組織，skill 與 automation 才是真正在替你做事的部分**。

## 核心結論

這套設定是高度個人化的——作者辨識出自己不想花時間的事，好把時間留給更高槓桿的工作。只有你能辨識出你的版本。辨識出來之後的步驟是固定的：**把它變成 skill、確認它能跑、把它自動化**，重複幾次，每週就能省下 5 到 10 小時。
