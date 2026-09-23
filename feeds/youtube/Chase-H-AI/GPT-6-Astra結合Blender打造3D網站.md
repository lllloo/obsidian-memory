---
title: GPT-6 Astra + Blender 打造驚豔 3D 網站
description: 不會 Blender 也能做互動 3D 網站：先用 Astra 生圖定調美學，再讓 Codex 腳本化建 Blender 模型、轉 Three.js 上頁，最後針對行動裝置與效能優化並部署
created: 2026-09-23
updated: 2026-09-23
source: https://www.youtube.com/watch?v=RhGiG-yZP-c
published: 2026-09-15
parent: "[[01.index]]"
tags:
  - youtube
  - web-design
  - codex
  - ai-image
  - frontend
  - workflow
---

## 成果概覽

- 示範網站的 hero 區塊不是預錄影片，而是用 Three.js 載入頁面的真實 3D 物件：會回應滑鼠移動、跟著游標、隨捲動移動，也能展開後再收回
- 3D 物件由 Blender 製作，而作者本人從沒用過 Blender
- 全程示範使用 Codex app 內的 GPT-6 Astra，但同樣流程在 Claude Code 也能做
- 作者提供 GitHub repo（連結在置頂留言），內含安裝說明、推薦 skill 與各步驟的範例 prompt

## 步驟 0：前置準備

- 需要：Codex 或 Claude Code、Blender（免費開源），以及配套 skill
- 推薦 skill：
  - **Blender Agent Studio**：作者在 GitHub 找到，只有約 20 顆星但實測好用
  - **Blender to web**：作者 repo 內附的 skill
- 把 Claude Code 或 Codex 指向該 repo，它會自行安裝 skill

## 步驟 1：設計——先用圖片定調

- 不要一開始就叫它進 Blender 建模；先讓 Astra 生成一批圖片，確定美學方向後，再拿選定的圖當 Blender 的參考
- 比起純文字描述（「我要一個無限迴圈造型、灰色帶點黃」），先生圖原型化快得多也容易得多；直接跳進 Blender 會很吃力
- 作者當時也不確定要什麼，只告訴 Codex：要一個可互動的 3D hero 物件（滑鼠移過、點擊會有反應），配色是黑色搭霓虹毒黃；請它產出多種選項
  - 產出的候選包括機器人臉、機械手臂、living fabric、另一隻機械手，以及最後選用的無限迴圈雕塑
- repo 內有範例 prompt，用法：丟進 Codex，說「以此為範本，但不要做虛構光學產品 Luma 的 3D hero，改做〈你的主題〉」
- 請它建一個概念圖庫，做 3 到 7 種 hero 變體——這是步驟 1 最快的迭代方式

## 步驟 2：進 Blender 建 3D 物件

- 只要告訴 Codex：「把我的設計在 Blender 中做成 3D 物件」
- 作者這次花了 12 分 40 秒；幾乎全透過腳本程式化完成，偶爾用 computer use 開啟 Blender 看畫面以驗證
- 使用者全程不用碰 Blender
- 不必滿足於一次產出：示範網站中流過整個結構的黃色脈衝光，第一版並沒有，是之後要求才加上的；此步驟就是不斷來回迭代直到滿意
- 物件只存在於 Blender 中時，可請它先做一個替代的 hero 區塊並轉成 Three.js，在網頁上預覽效果再定案

## 步驟 3：組建網站

- 示範是虛構公司 Aperture 的網站；Codex 把 Blender 物件轉成可互動的 Three.js 結構
- 物件不只放在 hero：會隨捲動講述產品故事，例如碎裂散開、再聚合，並切換到頁面另一側，整頁多處呼應該物件
- 網站本身也要先做 mockup：Codex 內建圖像生成工具，讓它先生圖而非直接寫 code
  - 作者這次一次到位：告訴它「這是我們做好的物件，我要從 hero 到頁尾有一個連貫的故事，怎麼整合？」
- 建議整頁都凸顯這個 3D 物件，因為它是最吸睛的元素
- repo 內有此步驟的範例 prompt，也有「請建好並在 Blender 內檢查最終成果」的範例 prompt
- 結尾同樣是持續迭代，最省力的方式是讓它盡量多產 mockup

## 步驟 4：優化與部署

- 要考慮的問題：行動裝置怎麼辦？是否很吃資源？非高階桌機的使用者怎麼辦？
- 行動版不跑複雜的 3D 物件，改成靜態圖片，避免老舊手機負荷不了
- repo 提供優化用 prompt，讓 Codex 檢查：
  - 行動裝置與不同硬體等級下都能正常運作、不拖垮使用者電腦
  - 量測物件的下載大小
  - 物件不在畫面內時暫停渲染
- 部署：Codex 有內建 hosting，在 Codex 中輸入 `@sites` 並指向已建好的網站即可自行上線，像內建的 Vercel
  - 作者不建議用於真正的 production，但要快速上線給別人看很方便

## 作者觀點

- 比起放 Seedance 生成的影片當背景，或把影片切成影格做捲動動畫，這種即時 3D 物件質感更高級
- 如同先前介紹 After Effects 的影片，這讓人能跨進原本沒時間或沒意願學的領域（例如 Blender），以相對簡單的方式做出很酷的網頁設計
