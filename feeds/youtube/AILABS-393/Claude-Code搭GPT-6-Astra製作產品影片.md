---
title: Claude Code 加 GPT 6 Astra 終結 AI 影片剪輯
description: 透過 CLI Proxy API 在 Claude Code 用 Codex 訂閱驅動 GPT 6 Astra，按規劃、粗剪、精修、配樂製作產品影片
created: 2026-09-23
updated: 2026-09-23
source: https://www.youtube.com/watch?v=p565AqELA8M
published: 2026-09-16
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - multi-model
  - workflow
  - motion-design
---

## 為什麼要有流程

- 產品宣傳影片是讓人不必實際使用產品就注意到它的最快方式。
- 直接跳進製作通常品質不如預期，還浪費大量時間與 token；需要一套確保成品符合預期的完整流程。

## 為什麼在 Claude Code 裡跑 GPT 6 Astra

- Astra 是影片剪輯表現最好的模型之一，作者先前比較中其設計表現也勝過 Fable，設計方向較佳。
- 作者偏好 Claude Code 提供的工具，幾乎所有東西都用它做。
- 分工：Astra 負責影片的創意方向，Claude Code 負責執行工具產出影片。
- 不想用 Claude Code 也可直接用 Codex 或其他 coding agent；用 Codex 的人可跳過設定 Astra 的步驟，直接安裝影片工具。

## 在 Claude Code 設定 Astra

- 不建議直接付費接 OpenAI API：模型昂貴，做影片又很耗 token。
- 改用既有的 Codex 訂閱，透過 **CLI Proxy API**：在本機跑一個小 server，把 Claude Code 接到你已安裝的 coding agents，沿用既有訂閱而不另付 API 費用；支援許多 agent。
- 步驟：
  1. 用 `brew install` 安裝 CLI Proxy API。
  2. 需要調整部分設定並建立 API key——最簡單是請手邊的 agent 代為設定，並在 prompt 中註明要透過它使用哪個模型；完成後 agent 會給你一組 API key，留著連線用。
  3. 安裝後會自動啟動，不需額外指令。
  4. 這組 key 不是按 token 計費的一般 API key，只是讓你透過本機 server 使用已安裝的 coding agent，只在你自己的系統上有效。
  5. 執行 CLI Proxy API 的 login 指令連上 Codex 帳號：瀏覽器開啟後登入，工具會保存 Codex 登入狀態以使用你的方案。
  6. 啟動 Claude Code 時改設定 base URL，讓請求送往本機 server 而非 Anthropic；填入先前的 API key，模型指定為 GPT 6 Astra。
- 最後安裝影片製作工具：影片中列出工具清單，可截圖交給 agent 代為安裝；這些工具附帶 skill，告訴 agent 製作影片時如何使用。

## 階段一：規劃影片

- 範例產品：一個可搭配整套穿搭並購買的藝術風服飾店（用作者社群的 app template 建成）。
- 規劃很重要：製作可能花好幾小時，不先確認計畫就可能做出一支不要的影片。
- prompt 內容：
  - 商店執行中的網址，讓 agent 能打開商店並據此規劃。
  - 長度與版面：30 秒、16:9 橫式（產品 demo 常見）；短影音可改用直式。
  - 要配樂、不要旁白。
  - 請 agent 把計畫呈現在瀏覽器上，光看文字描述難以想像成片。
  - 要求計畫頁提供留言區，方便指出要改的地方。
  - 指定參考：Anthropic 與 Linear 的產品發表影片，讓 agent 理解你想要的樣貌與鏡頭運動（例如畫面如何滑過頁面、如何 zoom in 到按鈕）。
- agent 載入 Hyperframes（安裝的影片工具之一）附帶的 skill 來規劃鏡頭與整支影片，完成後在瀏覽器開啟計畫：逐秒列出畫面內容、鏡頭運動與網站上發生的事，並有留言區。
- 可留任意多則留言；審完請 agent 讀留言、更新計畫。
- 滿意後請 agent **鎖定計畫**，讓它知道這是最終方向，再進下一階段。

## 階段二：分鏡粗剪

- 先為每個鏡頭做基本版本，檢查鏡頭運動後再花時間精修。
- 分開製作的理由：某個鏡頭不滿意時只需改那一個，不必重做整支影片；也是檢查 zoom 與其他鏡頭指示是否正確的時機。
- prompt：開瀏覽器、以全螢幕解析度錄製每個鏡頭並各自轉成影片，以便檢查鏡頭運動。
- agent 先做第一個鏡頭就停下請你審核，避免同一個問題在整支影片重複出現；圖片與錄製片段會顯示在瀏覽器中。
- 第一個滿意後再讓它產生其餘鏡頭，最後在瀏覽器一起檢視。
- 作者遇到的問題：幾個片段莫名晃動、部分 zoom 與計畫描述不符，請 agent 修正；可一直要求修改到滿意。

## 階段三：合併與精修

- 請 Claude Code 優化鏡頭運動並把片段合併，讓鏡頭之間順暢銜接；prompt 中說明鏡頭如何移動、在哪裡 zoom in、何時出現打字動作。
- 合併耗時很長，產出的是尚無配樂的完整影片，存在 agent 的工作資料夾中。
- 有問題時要告訴 agent 發生在影片的哪個位置；作者遇到一個鏡頭偏右太多，請它移回原位。
- 修改完成後再請 agent 重新審查影片找殘留問題；安裝的工具內建小問題檢查，跑過後成片就不會帶著這些問題。

## 階段四：配樂

- 音樂讓觀眾在每個鏡頭間持續被吸引，大幅提升吸引力。
- 只叫 agent「加音樂」它會自己挑，但不一定合適，需要給方向。
- 作者寫了一個選曲 skill：
  - 從計畫中讀取產品風格。
  - 計算影片切換鏡頭的頻率，依此找節拍相符的音樂。
  - 到 Mixkit 搜尋 calm、piano 等分類的免費音樂。
- 建立方式：給 Claude Code 一段描述完整工作流程的 prompt，由它產生包含找音樂與加入影片所需一切的 skill；想要同樣 skill 可把該 prompt 交給自己的 agent 產生。
- 使用：輸入 `/` 加 skill 名稱，它會找音樂並加入，產出一個帶配樂的新版本影片。
