---
title: 全新 Astra 網頁設計工作流
description: 用 GPT-6 Astra 內建圖像生成做前端設計的流程：建立 taste vault 參考庫、跨設計家族產出多版本、比較 skill 效果、以 tweaks 面板微調，最後用 Sites 部署分享
created: 2026-09-15
updated: 2026-09-15
source: https://www.youtube.com/watch?v=XK6S1hbYv7I
published: 2026-09-09
parent: "[[01.index]]"
tags:
  - youtube
  - web-design
  - codex
  - ai-image
  - workflow
---

## 為何 Astra 適合前端設計

- GPT-6 Astra 內建圖像生成工具，且剛加入 GPT Images 2.5，不需另外串接、免費使用
- 前端設計是高度迭代的過程，常需自製素材與圖像；對比 Fable 模型需接 fal、Higgsfield 等外部工具並按次付費，內建生成讓迭代又快又便宜
- 講者需要親眼看過多個版本才能定案，因此能跨多個設計家族快速產出版本是關鍵

## 步驟零與一：確定產品並蒐集參考

- 步驟零：先想清楚要做什麼網站、產品是什麼
- 步驟一：找靈感，不從零開始。來源包含 Pinterest、Twitter、Landbook、Dribbble（搜尋如「SaaS 前端設計」「某類產品 landing page」）
- 長期做法是建立自己的設計參考庫，講者稱為 **taste vault**：
  - 把喜歡的截圖丟給 Astra（最初在 Fable），由它整理到同一處並依設計家族分類
  - 分類例：monumental editorial、product-led minimalism、technical systems、futurism、print tech paper、dither mono、vast quiet cinematic 等
- 有了參考庫後可以這樣下指令：
  - 「用 technical systems 家族示範這個網站的樣子」，並給整個分類要它萃取設計模式
  - 「我很喜歡這一個，先完全重現再改成我們的」
  - 同時要求 print tech paper、dither mono、vast quiet cinematic 等多個家族的變體
- 重點是給實際範例，而不是「讓它更吸睛、更乾淨、更極簡」這類空泛描述
- 應持續累積：看到喜歡的網站就截圖丟給 Astra，說「加進我的 taste vault」
- 講者在置頂留言提供 taste vault 副本與影片中所有 prompt

## 步驟二：多版本產出與 skill 選擇

- 若已確定風格可直接指定；多數人還不確定時，不要說「用這個風格做一個 landing page」，而是「做多個 landing page，每個對應一種設計家族」
- 要思考讓 Astra 使用哪些前端設計 skill：
  - **Impeccable**：講者最常談的前端設計 skill，約 66,000 stars，主打消除 AI slop
  - **Taste skill**：約 86,000 stars
  - Anthropic 的 **frontend-design skill** 也能帶進 Astra 使用
- 需要自己實驗感受哪個適合

## 步驟三：迭代

- 範例產品是虛構的 **Vantage**：給個人投資者的金融市場 AI 分析工具
- 講者要求五個設計家族（luminous futurism、print tech paper、quiet cinematic、technical systems、product minimalism），各四種變體：無 skill、Anthropic frontend-design、Impeccable、Taste skill，共 20 版，全在 Codex desktop app 內切換預覽
- 觀察：
  - Impeccable 與 Taste skill 是目前最主要、且不過度規範的外部前端設計 skill；很多 skill 只會產出單一特效（如捲動動畫），不實用
  - 部分版本加 skill 後較好，但**無 skill 的 baseline Astra 表現已很扎實**，並非「有 Impeccable 很驚艷、沒 skill 就是 AI slop」
  - 顯示模型基礎能力提升，需要的鷹架越來越少
- 主視覺圖由 Astra 自行生成：只給了參考，它便依故事脈絡想出雲與天文台的意象
- 迭代循環：
  1. 先在設計家族層級比較，選一個家族（講者選 technical systems 的無 skill 版）
  2. 要求「保留此美學，在這個方向內做三個不同變體」，得到 Original、Field of View（主視覺佔更大版面、整體偏綠）、Research Bureau（圖片較小）
  3. 選定一版（講者選 Original，乾淨又有個性）後進入微調
- 範例中的儀表板雖是虛構資料，但可互動切換不同 ticker

## 微調：tweaks 面板

- 讓 Codex 做一個類似 Claude Design 的 **tweaks 面板**，用滑桿即時調整多項設定，免去逐條 prompt「標題大一點、小一點」
- 面板可完全自訂，範例內容包含：
  - 動態預設：original（無動畫）、expressive（重播入場動畫、捲動時有份量感，更有質感）
  - 標題字重、行高、字距
  - 圖片亮度、對比、縮放
  - 格線圖樣（如點狀）、強調色
  - footer 選項：原版、大型浮水印、帶動態的線框城市（可調線寬、窗戶、是否動畫）
  - 儲存與重設設定、與原版比較、回到精修版或開原始版
- 產生面板的 prompt 同樣放在講者 GitHub

## 元件與部署

- 另一種微調是加入自訂或網路上找到的元件；講者最愛 **21st.dev**：在 Components 可瀏覽邊框、marquee、文字、testimonials、卡片、日曆、按鈕等大量範例
- 非設計背景者的難處是不知道自己不知道什麼，花 5～10 分鐘瀏覽參考，可避免被推向 Astra 的中位數輸出（雖然中位數已不錯）
- 看到喜歡的元件，點選後按 copy prompt 貼進 Codex；從單一元件（例如某張卡片的排法）就能把美學擴展到整個網站
- 部署：在 Codex 內用 `@sites` 說「套用這些新設定，把網站放上 Sites」即可上線
  - 類似簡化版的「推到 GitHub 再部署到 Vercel」，由 OpenAI／ChatGPT 代管
  - 不建議用於正式環境，適合分享給他人取得回饋
  - 可用 share 輸入對方 email，或開放任何人檢視；私人網站需登入才能看

## 結語

- Astra 讓跨設計風格、跨同風格版本的迭代又快又省，內建圖像生成讓素材製作便宜
- 不用任何 skill 的 baseline GPT-6 也能產出扎實成果；不需要只會給單一風格的高度規範 skill，關鍵是找出自己的風格，因此建立參考庫（taste vault）最重要
