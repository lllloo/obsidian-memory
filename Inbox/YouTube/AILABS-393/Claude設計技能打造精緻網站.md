---
title: 用 Claude 設計技能打造精緻網站
description: 盤點一整套設計用 skill：從前端設計方向、shadcn 元件、GSAP 動畫到行動端 Material 3 與 SwiftUI，各自解決 AI 生成設計同質化的不同環節。
created: 2026-06-24
updated: 2026-06-24
source: https://www.youtube.com/watch?v=Ot582-E61ac
published: 2026-06-23
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - frontend
  - ui-design
  - ai-agent
---

AI 生成的設計愈來愈好，但也愈來愈像——模型從大量同質資料學習，遇到設計決策就反射性挑「最常見」的選項，於是所有 landing page 都漂向同一種安全、通用的樣子。這支影片盤點一整套以 skill 形式打包的設計工作流，每個 skill 針對這個同質化問題的不同環節。skill 的好處是只在需要時才載入，不像 MCP 永遠佔著 context window。

## 設計方向：打破預設

Anthropic 的 front-end design skill 是許多設計 skill 的基礎，負責替網站定調。它的做法是強迫模型在動筆寫程式前先承諾一個明確的設計方向並保持一致，藉此跳脫安全、通用的選擇。skill.md（skill 的指令表）裡直接點名要避開常見的 AI slop——過度使用的字體、白底紫色漸層。

適用時機：landing page、作品集等「設計本身就是產品一部分」的頁面。

AI Labs 自己的設計系統把這支 skill 改寫成 marketing UI skill 裡一個叫 break the default 的 prompt。改寫原因是原版對較新的模型已稍微過時——Opus 4.8 與 Fable 5 都附了 prompting guide，說明 Claude 的變化以及指令該怎麼跟著調，他們把這部分折進了自己的系統。

## 功能型 UI：shadcn

Anthropic 的設計 skill 不適合功能型 UI。一旦開始做實際產品（dashboard、後台），問題就從「好不好看」變成「能不能當作有大量元件、且每個都要正確運作的產品來運轉」。

shadcn 的價值在於：dashboard 常用的元件早就由真人以專業水準建好，模型不必從零生成元件、自己配動畫，直接從 registry（現成元件的大型函式庫）拉來用。成果像真正的產品，因為起點就是「已經做到可上線」的零件，而不是粗糙初稿慢慢修。

shadcn 的搭配有兩部分：

- **skill**：規則手冊。shadcn 有一套正確的建構方式，skill 收錄這些規則，同時參照你專案的設定，確保產出既符合 shadcn 規範又貼合你既有專案結構。好處是第一次就拿到乾淨輸出，不用反覆修同樣的錯。
- **shadcn MCP**：與 registry 的即時連線，讓模型瀏覽並把真實元件直接拉進專案。

兩者一起用：MCP 提供元件，skill 提供規則、模式與專案脈絡，加起來才讓模型有「正確使用元件」的判斷力。為何有 MCP 還要 skill？因為 skill 只在需要時載入，不像 MCP 永遠在 context 裡。

## dashboard 的排版問題

一般 app 一次堆一個元件就行，但 dashboard 的核心難題不同——重點不在元件一致性，而在資訊如何排在螢幕上：怎麼分組資料、一個畫面塞多少才不會太擠。

因此有另一支由其他開發者（非 shadcn）做的 dashboard skill，專門讓模型先推理出排版安排再動手，成果才像真正的分析工具而非雜亂堆疊。

## UI UX Pro Max：先跑引擎再寫程式

這支 skill 的運作方式和其他都不同。多數 skill 給模型一些設計原則就信任它去套用，導致一切漂向同一種「好設計」。它的做法是先跑一個引擎：

- 在它自己 GitHub 上的開源資料庫同時發出五個搜尋
- 從 161 個產業類別拉出適合你產品的風格
- 從中挑出色票、字體配對與頁面排版
- 過濾掉對該類產品會顯得不對勁的選項
- 把量身打造的設計系統（完整規則手冊）交給模型依循

差異在於：其他 skill 給模型更好的品味，這支則在動工前就給出一個針對你實際產品類型推理出來的決策。

## 動畫：GSAP

靜態頁面只能走到一定程度，動畫能改善使用體驗、拉長停留時間。但動畫正是 AI 生成程式最容易崩的地方——叫模型加動畫，它幾乎只會做「往下捲動時元素滑入」這一招，而這在半數 AI 網站上都一樣，遠不及真正動態設計的能耐。

GSAP 是許多專業網站採用的動畫函式庫，這支 skill 直接來自打造 GSAP 的團隊，讓模型依正確模式工作，涵蓋基本位移到大型捲動動畫。它也處理常被低估的效能面：AI 動畫卡頓的主因是模型用改變尺寸或位置來移動元素，迫使瀏覽器每一幀都重建整頁；skill 引導模型改用瀏覽器容易處理的位移方式，光這個習慣就讓動畫順暢。

最適合 landing page 與捲動敘事。AI Labs 的 marketing UI skill 明確指定需要動畫時就用 GSAP skill 來實作。

## 品味預設（taste presets）

這組 skill 不是完整系統，而是直接丟進去把模型推向某種特定風格的預設。不要一次全疊，挑一個符合你要的氛圍即可：

- **minimalist UI**：留白、簡潔，適合報導、部落格等要讓內容呼吸的網站
- **industrial brutalist UI**：粗獷厚重的反企業風格
- **front-end UI/UX**：全能型，提供穩健預設；產品或商務 landing page 想乾淨專業時的安全選擇
- **premium front-end UI**：做出精品時尚品牌般的 landing page

## 視覺素材：Higgs Field

專業級網站需要真實的圖片與影片，但模型自己多半只抓網路上的 stock 圖，且常不符需求。Higgs Field 把圖片與影片生成接進你的 agent，不離開終端機就能要 hero image 或背景影片。它不綁單一模型，內建多數優秀的圖片與影片模型；做影片時 See Dance（Seedance）是目前最佳的選擇之一。

## 行動端 skill

很多 AI 生成的行動 UI 會悄悄出問題，因為模型把手機當成縮小的網站。但行動端有自己的規則：握持方式、拇指可及範圍、導航方式，每個平台還有自己的設計語言。

- **mobile app UI design**（原則層）：把好的行動設計規則直接內建，涵蓋拇指區（主要按鈕放在拇指可及處）、一致間距、精簡而非十種大小的字級——這些正是 Airbnb、Duolingo、Spotify 等熱門 app 背後的規則。
- **Material 3**：等於 web 端 shadcn 在行動端的對應，給模型 Google 的實際設計系統（多數 Android 與 Pixel app 採用）。風格大膽、色彩鮮明、大圓角、彈性動態。給一個顏色它就建出整套配色主題，還會檢查 app 對 Google 指南的貼合程度。
- **SwiftUI skills**：原生 iPhone 用。Apple 設計與 Google 相反，較克制、偏向半透明的玻璃質感（現稱 liquid glass）。skill 直接從你 Mac 上 Xcode 抽出 Apple 官方文件交給模型當規則，產出真正像原生的 app。
- **官方 Expo skill**：同時做 iPhone 與 Android。Expo 是讓一份 app 同時跑兩平台的框架，skill 涵蓋導航、樣式到平台功能。
