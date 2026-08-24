---
title: 用 Seedance 2.5 三步驟把 Claude 變成網頁設計天才
description: 從 Landbook、Twitter 找靈感，用 siteclone skill 逐像素重建當底稿，再以 Higgsfield MCP 生成 hero 影片並跑 remix 變體迭代。
created: 2026-08-24
updated: 2026-08-24
source: https://www.youtube.com/watch?v=NUK_TBz46dM
published: 2026-08-22
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - web-design
  - ai-image
  - workflow
---

## 核心循環：靈感 → skill → 迭代

整支影片圍繞一個三步驟循環，反覆套用在不同尺度上：

1. **找靈感**——決定整體 vibe 與美學方向。
2. **叫出對的 skill**——確保 Claude Code 真的執行得出想要的東西。
3. **迭代**——看到結果再調整。

這個循環同時作用於大尺度（整個網站要長什麼樣、設計方向是什麼）與小尺度（這個 component 要怎麼運作、有沒有參考、有沒有對應的 skill）。作者認為最該帶走的就是這個循環本身，其餘都是工具細節。

## 步驟一：找靈感與建立品味庫

作者列出三個找設計參考的來源：

- **Twitter**
- **Pinterest**
- **Landbook**——特別推薦，因為它通常會直接連到網站本體，拿得到真實 URL。

影片中的兩個範例：從 Landbook 找到 finn.com（動畫效果不錯），從 Twitter 找到一個 hero section 有雕像造型加 parallax 的網站（Plinth）。

**建議建立自己的品味庫（taste library / taste vault）。** 找到喜歡的網站不該用過一次就消失，之後還可以回頭調用、或至少用來啟動思路。作法很簡單：把截圖或連結收集起來，丟給 Claude Code 說「幫我做一個 library」，五分鐘就能建好。作者自己就有一個存在本機的 taste vault。

## 步驟二：用 siteclone 取得可用的底稿

一般作法是丟一堆截圖給 Claude Code 當參考，這可行，但可以做得更好。

**前提是要有真實 URL**（純截圖不適用）。有 URL 就能看底層的 code，交給 Claude Code 幾乎能逐像素重建，包含所有動畫。

作者做了一個叫 **siteclone** 的 skill，安裝後直接叫用並指向 URL：

```
/siteclone <URL>
```

它會拆解整個網站（含動畫）並產出逐像素的重建版本。影片示範本機 dev server 跑出來的結果與原站幾乎沒有差別。

**定位說明**：目的不是把別人的網站當自己的作品，而是拿到一個好用的骨架來大幅改造。與其把截圖丟給 Claude Code 賭它能從願景直接做出成品，不如先有一個可以動手改的基礎，省下大量時間。

## 步驟三：用 AI 影片做 hero section

若要 hero section 有真實動態（不只是靜圖或 parallax），就得引入 Claude Code 以外的工具。作者用的是 **Seedance 2.5**。

### 標準流程：先圖後影片

不要讓影片生成器單靠 prompt 從零生成，而是先做一張**參考圖當作影片的第一幀**。生圖可用 Nano Banana Pro、Seedream 或 GPT Image。影片中用的是 **Seedream 5**。

### 透過 Higgsfield MCP 在 Claude Code 內完成

作者的生圖與生影片全部在 Claude Code 內經由 **Higgsfield MCP** 完成，不必手動去網站上操作。安裝方式：到 higgsfield.ai 的 MCP and CLI 區段，複製 prompt 貼進 Claude Code，它會自動安裝 MCP 與相關 skills。

### 構圖要留白

生成參考圖時要先想好 hero section 的版面配置。影片的例子是文字放左側，所以圖的**右側要留大量 dead space**，主體（雕像）推到右邊。若換成文字在上、banner 在下的配置，主體就放中間、同樣要留白。

**留白是關鍵**——動畫只是點綴，不能喧賓奪主。

### 生成影片的指令與原則

給 Claude Code 的指示大意是：用 Seed Dance 2.5，拿剛才生成的參考圖為 landing page 生一支影片，接著描述想要的動態。

影片例子：雕像手持一顆類似 palantir 的球體，讓球體緩慢脈動、微微發光。

**原則是動態越含蓄越好**，動作太大會分散注意力。

## 合併與迭代：remix site skill

把重建的網站與生成的影片合在一起後，作者的 GitHub 另外提供 **remix site** skill 承接迭代。

### 先修文案再 remix

第一次合併的結果問題很多：整站還是 Plinth 的文案、影片被 header 蓋住、影片切到 body 的接縫太硬。作者先用一段 prompt 把 hero 與 body 的文案、名稱、主題整批改成自己網站的定位（示範情境是一家虛構的 AI analytics 公司），再進 remix 階段。

### 呼叫與兩個提問

```
/remix-site
```

skill 會問兩個問題：

- **Amplitude（幅度）**：三個變體要跟原版差多少。
- **Anchors（錨點）**：有沒有具體的美學參照。**沒給錨點的話變化會很保守**，大概只動顏色、字體、間距與 hero 的少許細節，不會有劇烈差異。

作者的答法是幅度拉到最大，錨點指向自己的 taste library 讓它挑三個差異很大的方向，並允許它呼叫 Higgsfield MCP 生成額外素材（例如用 GPT Image 為 body 補圖）。

### 變體檢視

三個變體會呈現在同一頁上，可點進去各自捲動瀏覽。影片中的三個是 Monolith（明顯更暗、加了 dither mono 風格的新素材）、Clima（綠色系配雲與橘色）與第三個（graph 背景加新素材）。作者選了 Monolith。

**變體數量不限三個**，錨點也可以放很多、幅度可以自己調。重點是逼出腦力激盪，看到不同方向再收斂——對沒有設計背景的人來說，光靠想像很難生出這些變化，得先看到才知道要什麼。

### tweaks 面板

選定變體後右側會出現 **tweaks 面板**，可對個別 component 做很細的調整。作者認為這比 Claude 桌面版原生提供的還深入。示範可調的項目包括：

- 影片本身的 grain（顆粒感）
- 黑色漸層的覆蓋範圍（雕像的顯露程度）
- 影片亮度
- 全部隨機 shuffle
- 預設集：pitch black、soft studio、loud watermark
- page spacing
- reveal stagger（進場時各元素的錯開節奏）

同時**隨時都還能直接 prompt Claude**，要做大範圍改動時那仍是最快的方式。

## 其他要點

- **skill 不限用於專案開頭**：impeccable、taste skill 這類前端設計 skill，在已經迭代很久的既有專案上一樣可以隨時套用。
- **動態的性價比在進場動作**：作者認為 motion 最划算的地方是元素怎麼進入頁面——有重量感、從上方或側邊帶進來的那種，而不是畫面裡有多少東西在動。
- **行動裝置不要播影片**：偵測到 mobile user 就改給靜態圖，避免舊手機吃不消。
