---
title: 第一名的 Claude Code 設計 Skill 迎來大升級
description: Impeccable 4.0 以 64 種 AI slop 反模式檢測、177 種 worlds 風格與 live 視覺化迭代，把前端設計的控制權交回使用者手上
created: 2026-08-17
updated: 2026-08-17
source: https://www.youtube.com/watch?v=RVeCbPg0liw
published: 2026-08-03
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - web-design
  - workflow
---

宣稱能解決 Claude 前端設計問題的 skill 與 plugin 多如牛毛，作者說自己實測過數百個，只有一個明顯高出一截，而它剛剛大幅升級——**Impeccable 4.0**。

本片是專門針對這個工具的深度解析。作者明說前一支關於「如何把品味注入網頁設計流程、擺脫通用 AI slop 產出」的影片是前置基礎，這裡不重複那些基本功。

## Impeccable 是什麼

- **免費開源的 skill**，GitHub 約 5 萬顆星；GitHub 官方喜歡到把它整合進自家 AI 工具。
- 核心命題是**辨識 AI slop 的模式再置換掉**。作者先說約 40 種（紫色漸層、藍色漸層那類），後來更正為官方文件列的 **64 種**「暴露 AI 預設值與生產缺陷」的模式。文件裡也能看到這些模式隨年代的變化——早期 ChatGPT 時代那種痕跡，跟現在的 AI slop 長相已經不同，但都是要遠離的東西。
- 它是**一個 skill 但內含 23 個指令**，各自對應設計光譜的不同環節：塑形（shape）、打磨（polish）、變安靜（quieter）、動畫、onboarding、配色、字體排版等等。官網 impeccable.style 上每一個指令都有「Claude Code 版 vs. Impeccable 版」的視覺對照可看。

## 4.0 的兩個主要改動

### Live mode

2.0 時期還在 alpha 的功能，現在完整成形，明顯更順、更即時。價值在於**把迭代帶出終端機、變成視覺化操作**，設計流程因此簡單很多。

### Worlds（177 種設計世界）

官方說法是加入了 177 個高評價的 worlds，實際上就是 **177 種設計模板／美學風格**，可在從零建站時挑選。運作方式是它先給你它的第一個設計構想，再給出幾個差異極大的選項——等於把前一支影片裡手動做的事自動化了。

官方另有文章說明他們怎麼確保這些不會每次都是垃圾產出，影片沒有展開。

配合 **Higgsfield MCP** 使用時，可以直接看到**自己的網站在各種風格下長什麼樣**，而不是看通用模板。

作者認為這兩項都不是小改動，因為它們的共同主題是**迭代與提供選項**。

## 安裝

- Impeccable 本身：`npx impeccable install`。覺得指令太難的話，把 GitHub 網址複製貼進 Claude Code，說「幫我安裝 impeccable」即可。
- **Higgsfield MCP**（worlds 功能要用到，本質是幾乎所有 AI 圖像／影片生成器的聚合器）：去 higgsfield.ai，點上方的 MCP and CLI，選 Claude Code，複製那段 prompt 貼進去，它會帶你走完授權流程。

## 實作流程

### 初始化

在新資料夾裡跑 `/impeccable init`，它會開始問問題：

1. **要建什麼**——作者回答「一個真實的 landing page」。
2. **要用什麼技術堆疊**——不知道的話可以直接回「你決定」。
3. **證據（evidence）**——你希望網站上放什麼內容。有截圖就給，有真實數字最好；什麼都沒有就叫它自己編。作者選了讓它產生假資料，之後再改。

回答完後它呼叫 Higgsfield MCP 生成各種 worlds，**在 localhost 上開起來讓你實際看**，第一個是它自己的構想（示範中是 Pathfinder 的 hero section），後面是其他選項。不喜歡可以按右下角 re-roll 重擲，也可以給**可選的引導**（例如「我比較喜歡第三個，多做幾個那個方向的變體」）。

### 兩層收斂

挑定一種風格後指令回傳終端機開始建原型，而**建的過程中它會再給你那個風格底下的多個變體**（示範中是 constellation、dossier split、find the Y 三種）。也就是：先在多種風格間挑一種，再在該風格的多個變體間挑一個，每一步都能下引導。

作者特別欣賞這一點，並拿它跟另一類 skill 對比：

> 那種一招鮮的 skill（隨便從某個 GitHub repo 抓來的）做出來的網站確實好看，**但它只會做那一種網站**。Impeccable 很通用，代表**它的下限比較低**——你出錯的空間更大——但客製化程度高得多，願意投入的話最終產品更好。

### 自動審查

第一輪迭代結束時，它會啟動一個叫 **Impeccable Finish Reviewer** 的 subagent，**用全新的 context window** 重跑一遍檢查，確保建置過程中沒有不小心自己引入 AI slop 模式。相當於第二雙眼睛，確認做出來的跟原本要做的一致。

示範結果：作者只說了「這是一家叫 Pathfinder 的虛構 AI 分析公司，內容你自己編」，沒給參考圖、連 CTA 都沒指定，產出跟同樣 prompt 交給一般 frontend design skill 的結果天差地遠——關鍵是它不像那種一眼看穿的通用產出。

作者順帶提出一個態度上的提醒：**做任何 AI 創意工作都該擺脫「必須一次到位」的期待**，它本來就是迭代過程。

## Impeccable Live 的用法

指令是 `/impeccable live`，網站會開起來、下方多一條工具列。

- **pick element**（最常用）：點選任一元件後開啟 prompt 視窗，可以打字或用麥克風，並選擇要生成 1 到 4 個變體。
- 也可以**指定要套用哪個領域的指令**（bolder、quieter、polish、typeset 等）——這些就是前面說的 23 個 Impeccable 指令，忘記某個指令做什麼就回官網查。
- 示範中作者只選了 bolder、要三個變體、**連 prompt 都沒打**就送出。回到終端機能看到指令傳過去了，因為**當前 session 會持續輪詢 live mode 事件**。
- 產出的三個變體**各自還能再微調**（傾斜角度、印章邊框開關等）。作者說他非常喜歡這點，因為替代方案是自己去要求 Claude Code 生一個微調介面出來。
- 滿意後按 **accept**，資訊就送回終端機。
- **detect** 按鈕會檢測 AI slop 反模式。從零建站時建置過程已經做過了，這顆按鈕主要是給「拿 Impeccable Live 去改既有網站」的情境用的。
- **design.md**：完整的設計檔案，所有顏色、元件、按鈕規格都在裡面（作者類比為 Google Stitch 與 Claude 設計功能裡的同類東西），也能看原始檔。
- 另有 insert 功能與一個 prompt 視窗，效果等同直接在終端機下指令調整整頁。

## 分工原則：大改動走終端機，微調走 Live

作者給了明確的分界：

| 情境 | 工具 |
|---|---|
| 元件層級的微調與變體 | Impeccable Live |
| 大幅版面調整、整個方向重來 | 終端機 |

方向要重來時的做法就是設計流程的常規動作——**餵它不同的參考**。作者維護了一個自己的**靈感庫（taste vault）**，收集看過喜歡的 hero page 與各種設計。示範中他把一張 ASCII 風格的參考圖貼進去，說明參考圖在哪、目前站台跑在哪個 localhost 埠、想往這個方向走一個新變體，並提醒它 Higgsfield MCP 還在、需要背景素材可以自己生。

產出的第二版跟第一版差異極大、確實是 ASCII 主題，但**仍然是 Impeccable 的產物**——一樣跑過 Impeccable reviewer 確認沒有 slop，等於兩邊的好處都拿到。

作者最後補充可以再對每個區塊跑 animate，讓頁面不那麼靜態。整體心法一句話：**大處交給 Claude Code，小處用 Impeccable 收拾**。
