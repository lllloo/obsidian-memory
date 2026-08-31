---
title: Claude Code 的 design skill 與三步驟前端設計流程
description: 新的 /design 把 Claude Design 網頁版的 artboard 與屬性面板搬進 Claude Code，可疊加 impeccable 等 skill；配合靈感、疊 skill、tweaks 迭代三步驟使用
created: 2026-08-31
updated: 2026-08-31
source: https://www.youtube.com/watch?v=nSfEL1Y-nUk
published: 2026-08-28
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - web-design
  - workflow
---

Claude Code 迎來近期最大的前端設計能力升級：新的 `/design` skill 把獨立的 Claude Design 網頁 App 的核心體驗搬進 Claude Code 本身，不必再在兩個應用之間來回搬運設計稿。

## 這個 skill 解決什麼

- 過去流程：在 Claude Design 網頁版做完整份設計 → 匯出成 zip → 丟進資料夾 → 再指給 Claude Code，中間步驟繁瑣。
- 現在：直接在 Claude Code 內產出 artboard，滿意後叫 Claude Code 把它寫成程式碼。
- **最大加值是能疊加 skill**：在 Claude Design 網頁版無法呼叫 impeccable 或 taste 之類的 skill，在 Claude Code 內可以，成品品質因此更好。

作者認為它針對的族群很明確：慣用 Claude Code、也喜歡 Claude Design 網頁版，但覺得兩者切換很彆扭的人。

## 怎麼用

指令就是 `/design` 加上你想做的東西的描述。

- **桌面 App**：結果出現在側邊面板，所有東西都在同一個地方，作者偏好這種方式。
- **終端**：會產生一個 artifact，在瀏覽器開啟；便利性略遜，但操作一樣簡單。

產出的 artboard 具備：

- 一次產生多個版本／變體。
- 右側屬性列：點選任一元件即可調整幾乎所有屬性，可縮放放大細看。
- 右上的 **tweaks** 區塊，初始為空，需另外要求 Claude 生成。

## 三步驟工作流

作者建議每次用 Claude Code 做前端設計都照這三步走。

### 步驟一：先給靈感，不要只給 prompt

不要只丟「給我三個不同版本」，而是先餵**參考圖**：截圖你喜歡的海報、設計風格，然後說「做出同一調性的東西」。此原則同樣適用於 landing page、hero section 等。

找靈感的地方：

- Pinterest（例如搜「Instagram infographic」）
- Landbook（偏 web design 與 hero section）
- Dribbble

作者建議**自己累積一個設計素材庫**，之後要設計時直接取用，不必每次重跑找靈感這一步。

### 步驟二：疊加額外 skill 與 MCP

在同一段 prompt 裡明確要求呼叫其他 skill 與工具，這正是網頁版做不到的部分。作者示範的 prompt 大意：

> 我們用 `/design` 重做這三則貼文，我放了三張截圖當設計靈感，請針對每張截圖各產一個版本。請呼叫 impeccable design skill。另外你可以用 Higgsfield MCP，如果覺得需要生成外部素材來做海報就去做，交給你判斷。

- **impeccable**：免費開源的前端設計 skill，主打辨識並清除 AI slop、套用更好的設計原則。
- **外部素材生成**：Higgsfield MCP，或其他影像生成服務。非必要，不想用外部圖片也可以。

重點是：因為身處 Claude Code 內，任何工具都能拉進設計流程。

### 步驟三：用 tweaks 面板迭代

初始 artboard 沒有可調控制項，畫面會提示「describe what you want to adjust and Claude will add a tweaks panel for it」。回到終端要求即可，作者示範的說法是要 tweaks **盡量激進**，能編輯的東西越多越好。

生成後右側出現 tweaks 列，可以調整紙張顏色、文字外觀、字級、字重、行距等等；面板本身也常常給出調整方向的靈感。

大改動仍走 prompt。作者示範針對三個版本中的第二個下指令：只保留這一個、其餘忽略，改掉內容走 infographic 方向解釋 `/design` 帶來什麼，並要求先做 web search 確認 `/design` 實際功能再重做。產出的新版海報資訊量明顯增加，而且因為在 `/design` 裡，文字位置與內容都能直接手動微調。

## 為何值得

視覺化即時迭代取代了「下 prompt → 等生成 → 看喜不喜歡 → 再下 prompt」的迴圈，速度差距明顯。選定喜歡的版本後，就告訴 Claude Code 只針對它迭代，直到滿意為止。
