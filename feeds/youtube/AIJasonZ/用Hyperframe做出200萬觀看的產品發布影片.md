---
title: 我如何用 Hyperframe 讓產品獲得 200 萬以上觀看（逐步指南）
description: 以 HTML 表達影片時間軸的 Hyperframe 搭配 Codex 與 Astra 模型，從故事線、分鏡到逐 composition 微調做出高擬真產品發布影片的完整工作流
created: 2026-09-24
updated: 2026-09-24
source: https://www.youtube.com/watch?v=8pRe7kkPi6g
published: 2026-09-23
parent: "[[01.index]]"
tags:
  - youtube
  - workflow
  - motion-design
  - codex
  - ai-agent
---

> [!note] 本片為 HubSpot 贊助，講者順帶推廣其免費 Claude Code playbook（涵蓋 AGENTS.md／CLAUDE.md 結構、hooks、guardrails、task state、多 session 分層設定與降低 70% API 費用的做法）。字幕為自動產生，部分產品名稱依語境還原（如 Codex、Claude Code、GSAP、Remotion）；講者的產品名稱字幕記為 Track。

## 為什麼 AI 生成發布影片不再是「PowerPoint 動畫」

- 過去 AI 產出的發布影片多是簡報式投影片，乏味且沒有記憶點；講者認為自 Fable 系列模型推出、再到後續的 Astra 模型後，影片編輯能力大幅躍升。
- 講者的實測：把一段 YouTube 影片餵給 Astra + Hyperframe，一次 prompt、32 分鐘後就近乎像素級複製整支影片。
- 講者自己的產品發布影片全用 Fable／Astra + Hyperframe 生成，累計超過 100 萬觀看；最極端的案例是 Fable 5.1 發表當天早上看到公告，團隊在約 4 小時內做出高擬真影片加不像 vibe-coded 的 landing page，在 Twitter 拿到 10 萬以上觀看。
- 講者結論：對建構與推廣產品的人來說，熟練 Hyperframe 或 Remotion 這類工具已是必備技能。
- 能做到這點的前提是現代 harness（Codex、Claude Code）用 context、工具等包裝模型；只會單純下 prompt 的人與充分運用各種技巧的人之間，產出差距可達 10 倍。

## Hyperframe 的核心原理：用 HTML 表達影片時間軸

- 核心想法是用 HTML 做影片，因為 LLM 最擅長寫 HTML／CSS／JavaScript。
- 傳統做法（After Effects 等）是圖層、特效、關鍵影格的合成，自動化只能靠編輯軟體自己的 API，模型沒訓練過；更關鍵的是模型無法知道「1 分 3 秒時畫面長什麼樣」。
- Hyperframe 團隊最初嘗試用 JSON／XML 定義描述影片的資料結構，但模型難以視覺化每一影格，導致編修效率差；改走 HTML／CSS／JavaScript 路線後才突破。
- 運作方式：在 HTML 元素上加 composition ID、起始時間與持續時間等 data 屬性，把實際視覺內容包在 `div` 底下；模型照常輸出 HTML／CSS 設計，用 JavaScript 控制動畫（可沿用 GSAP 之類的動畫函式庫），只是把 DOM 元素綁到影片時間軸。
- 這讓模型能輕易擷取任意時間點的影格。Hyperframe 與 Remotion 的差別：Hyperframe 針對 HTML／CSS／JavaScript 最佳化，Remotion 針對 React 與 CSS；講者覺得模型在純 HTML 下設計更自由、更有創意。

## Hyperframe 的兩組 skills

- 安裝 Hyperframe skills 時數量很多、容易不知從何下手，講者歸納為兩組：
  - **核心組**：必裝的 `hyperframes-core`（講 Hyperframe 的基礎），以及相關的 Hyperframe CLI、animations、keyframes；另有 `hyperframes-registry`，讓 agent 在官方提供的大型 view 與動畫元件庫中搜尋。
  - **用途組**：依需求載入的 use-case skills，例如 product launch video、faceless explainer、music to video、PR to video、website to video。
- 講者用 website-to-video skill 指向 uber.com，一次 prompt、21 分鐘後得到一支以其核心 UI 元素與使用者旅程為主的無品牌動畫影片；但這種一 prompt 產出仍偏簡報感，要做出「像專業工作室」的品質需要後面的逐步流程。

## 從零開始的工作流：先定故事線

- 案例：為剛發布的 Codex plugin 做發布影片。開新 session，說明要做 Codex plugin 的發布影片，並刻意要求不要參考既有影片，模擬從零開始；模型選用 Astra 高階版本，講者認為它特別擅長影片製作。
- 第一步 agent 會先以文字提出故事線（Codex plugin 目錄、游標輸入搜尋、plugin 詳細頁與安裝狀態、在 Codex composer 中選用 plugin、以真實 UI 呈現進度與回應）。
- 講者接著修正故事線重點：
  - 以本週在 Twitter 爆紅的 people search 用例作 hero，並附上該次發布貼文作參考；agent 會自行到產品網站找對應頁面路由補 context（約 2 分鐘）。
  - 補進核心價值主張：不用訂閱、無合約，只按使用量付費（每次查詢幾美分）；支援 2,800 種資料與工具、要有一幕展現大量 vendor；在 people search benchmark 排名第一；可取得電話號碼（單價約 0.044）。
  - 結尾用 tagline「open router for data and tools」。
- 講者提醒影片製作是創意迭代，定好故事線後仍常會調整順序；Hyperframe 把一分鐘影片拆成多個 composition，因此重排順序很容易。

## 分鏡（storyboard）階段：先看版面與文案

- 故事線確認後，agent 產出分鏡；此階段不需在意細部視覺，只專注兩件事：**畫面整體版面**與**文案**。
- 可對每一格逐一給回饋，再按按鈕複製 prompt 貼回；回饋會記錄在 `hyperframe/frame-commands.json`，agent 讀該檔即可套用（講者的一輪回饋約花 13 分鐘重建多數頁面）。
- 講者強調這裡正是創辦人／行銷人員的價值所在：即便是 Astra，預設仍傾向做簡報式影片，給對 context 與引導才能做出好東西。
- 講者的實際回饋範例：
  - 不要簡報式版面；拿掉「find your next customers」這種把產品錨定在單一用例的文案。
  - 先從 Codex Mac app UI 搜尋 plugin 開始，片頭與片尾之後再想——先把故事線的主幹做好。
  - 要求 UI 必須與真實 Codex Mac app 像素級一致（分鏡工具目前不能貼圖，講者改在 chat 貼截圖）。
  - 整支影片應維持在同一個真實 Codex session 裡，看起來像真實 demo，可用鏡頭 zoom in／out。
  - 縮短畫面文字——觀眾注意力極短，講者總是要求 agent 簡化畫面內容。
  - 補進 waterfall matching 的展示：agent 收到 prompt 後列出所有有對應 endpoint 的 vendor 與價格，掃描後選出正確 vendor。
  - 用「center big text → 換行 → 拉遠鏡頭顯示 vendor 與價格；左邊是 vendor 價格、右邊是 Track 價格；用美元而非美分拉開對比」這種鏡頭語言描述需求，講者認為很有效。
- 講者習慣一次不給太多回饋，分幾輪往返；版面大致到位後，用「approve the storyboard sketch and continue to animation」按鈕或直接說 I approve 進入動畫階段。

## 逐 composition 微調：先把前兩幕做到標準

- 進入動畫階段後，會得到依線框動起來的第一版影片；此時 UI 可能還不像真實 app，這階段的目的是確認**動畫節奏**是否正確。
- 講者的做法：每一幕都已是獨立 composition，因此逐幕請 Codex 修改，把 token 與注意力集中在單一幕上，品質通常更高。
- 先修 `01 discovery` 與 `02 install`，要求 100% 像素級複製 Codex app UI（含 plugin UI），並附截圖；agent 能把截圖轉成幾乎一模一樣的 UI。
- 再要求加背景，讓 Codex app 看起來像 Screen Studio 錄影。
- 鏡頭語言的回饋：點擊 plugin、輸入搜尋、點擊時都應 zoom in 讓焦點清楚；若出現「先拉遠再拉近」的多餘動作，直接說「keep the same zoom scale、只移動鏡頭位置」——「zooming scale」是有效的關鍵詞。
- 講者強調前一兩幕要先磨到位，作為後續所有幕的標準與風格。

## 把標準套用到後續幕

- 前兩幕定調後，只需說「apply the same UI treatment」到下一幕。
- `03`（people search）的回饋細節：
  - 結尾多餘的 zoom 動畫拿掉，最後一幀停留短一點。
  - 加大 prompt 輸入框的縮放讓文字更大；移除上方 toolbar 與「full access」等視覺雜訊。
  - 送出後鏡頭上移、新訊息浮出、Track 工具呼叫以更細的動畫浮出。
  - 每個 vendor 顯示真實 logo；分步驟呈現：Track 先出現 loading 狀態 → vendor 逐一浮出 → 選定 vendor 後鏡頭移向右側顯示聯絡人浮出，每位聯絡人加真實頭像。
  - 加入 Google Sheet 的 action card（與 chat 內同款卡片），先顯示 loading 表示正在抓取並存入 Google Sheet，再把鏡頭移到右側顯示結果。
  - 結果浮出時先顯示姓名、真實公司、職稱，工作 email 欄位則以不同 vendor 分批填入，讓觀眾看出 waterfall 驗證 email 是對每位聯絡人同時進行的。
- 講者指出模型加 Hyperframe 現在已能做很高品質的東西，影片品質主要取決於製作者對細節的注意——那些小細節才真正呈現產品的核心價值。
- `04` 沿用相同品質與 UI treatment 後幾乎一次到位，因為 01–03 已建立所有 pattern。
- Benchmark proof 這幕的回饋：開場以居中大標題搭配 Apple／Nike 廣告式的動態與鏡頭運動，先聚焦「most accurate people finder for agents」，接著展示 Codex、Claude Code、OpenClaw 等 logo（指向 LobeHub 的開源 logo 套件），再過場到 B2B prospecting 的 people search bench：Claude 先顯示 43% 長條圖，Claude + Track 到 78%、近乎翻倍，最後展示四個類別的圖表。
- 整體往返約 1.5 小時後得到講者滿意的版本：動畫流暢、故事線正確、呈現了連接多系統與 waterfall 路由取得最便宜資料的核心功能。

## 可重用性與收尾

- 所有過去的發布影片都只是資料夾：每支影片有 `compositions/` 資料夾，內含每一幕的 HTML 檔，每個 HTML 即一段影片片段；日後可直接指向舊影格要 agent 重用，本片示範刻意不這麼做。
- 最後加配樂：直接 prompt「next I want to choose some music」，Hyperframe 內建相當大的音樂庫（字幕於此處中止）。
