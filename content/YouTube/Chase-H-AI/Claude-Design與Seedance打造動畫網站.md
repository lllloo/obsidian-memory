---
title: Claude Design 結合 Seedance 2.0 打造動畫網站
tags:
  - youtube
created: 2026-04-22
updated: 2026-04-22
published: 2026-04-20
source: https://www.youtube.com/watch?v=7uW1SKmx-Ic
parent: "[[01.index]]"
---

## 整體工作流

結合 Claude Design 與 Seedance 2.0 建立帶動畫 hero 的 landing page，步驟固定為：

1. 在 Higgsfield 上用 Nano Banana Pro 產出 **靜態起始圖**（決定整張版面構圖）
2. 把圖與 prompt 丟進 **Claude Design**，先做桌面版靜態網站的設計迭代
3. 用 Seedance 2.0 把同一張圖轉成 **15 秒 hero 背景影片**
4. 把 MP4 上傳回 Claude Design 替換 hero 背景
5. 從 Claude Design **hand off 到 Claude Code** 收尾，部署至 GitHub / Vercel

關鍵原則：在 Claude Design 做到 90%、不追求 100%；剩下的微調留給 Claude Code，因為 Claude Design 的 usage 很貴。

## 構圖先行：Nano Banana Pro

prompt 不是重點，**構圖（composition）才是**。下 prompt 前先決定：

- hero 圖要放左、中、右，哪邊留空給文字
- 是否要有上方 navbar、CTA 按鈕、底部 ticker
- 文字（tagline / hero text）預計佔哪塊 dead space

沒有靈感時去 Dribbble 搜 `landing page SaaS`，拆解現有網站的 hero 與版面安排，至少先備 2–3 個方向再回 Nano Banana Pro。prompt 本身可以直接叫 Claude 幫你寫。

示範用的是一張左側留白、右側為 Prometheus 風格人物的圖，對應一個假想的市場情報 SaaS「Olympus」。

## Claude Design 操作

### 建立專案

- 左側進入 **Prototype**，輸入專案名（例：`SD2`）
- Design System 可暫不填；選 **High fidelity**，按 Create
- 進到專案後，在左下上傳剛才的靜態圖當作 context
- 有 Dribbble 參考圖就一起丟進去，多張 screenshot 都可

### Prompt 與 Plan Mode

在 prompt 結尾加一句 `Ask me any questions before you begin.`，Claude Design 會進入類似 Claude Code 的 **plan mode**，反問你一連串細節（typography、色盤、copy voice、hero composition、section order、social proof、tweaks 等），即使原本 prompt 很粗糙，也能靠 Q&A 補到相對完整。

建議：

- 選項不清楚時直接選 `decide for me`
- 遇到 tweaks 問題一律盡量多開，後續還可以再加

### Usage 注意

Claude Design 的用量與 Claude Pro / Max 5 / Max 20 **額度分開計算**，且非常吃資源。作者整個流程跑下來的額外費用約 **$5 美元**。因此要集中火力讓 Claude Design 做設計決策，細節修改交給 Claude Code。

### Tweaks 面板

右側 **Tweaks** 是 Claude Design 最有價值的地方，可即時改：

- accents、theme（light / dark）
- headline、logo mark、pricing names
- 任何 motion 設定
- 字型（body font / mono font / type scale）
- CTA、overlay darkness、emberglow 等細節

面板之外還有：

- 右上 **Edit** → 點任何元件直接改顏色、字型、padding、opacity
- 點元件可以 **留 comment** 或直接在畫布上畫註解，送給 Claude 讓它依註解調整位置／樣式
- 右上 **Share** → 匯出 HTML、Canva、PowerPoint、PDF，或邀請協作者

## 兩段式迭代：先巨觀變體、再微觀 tweaks

這是 Claude Design 比 Claude Code 強的地方——**視覺化的版面 A/B 迭代**非常快。

### Step 1：產生巨觀變體

不要只看第一版，用 prompt 讓 Claude Design 產兩個以上**完全不同版面**：

> Can you create two additional layout variants for our web page that I can click through in addition to this current one, suggest some new designs we could include.

示範中得到三個版本：cinematic（原版）、archive、terminal，hero 到 footer 整體風格都不同。選定一個方向後再往下。

### Step 2：針對選中版本狂開 tweaks

鎖定後，請 Claude Design 把 tweaks 盡量加好加滿：

> Let's stick with the cinematic, you can remove the other two, and also aggressively increase the number of tweaks available.

tweak 數量可從 ~5 擴到 ~15，然後反覆切換直到畫面滿意。

## hero 背景影片：Seedance 2.0

保留靜態背景而不是整張換成影片的原因：**手機使用者不要被大影片拖慢**，mobile 版只顯示靜態圖。

在 Higgsfield 進 Seedance 2.0：

- 把前面那張靜態圖直接拖進起始幀
- Prompt 要求**動作極小**，範例：
  > Keep the motion extremely slow, clouds barely moving, embers from the fire, and his hands slowly drifting.
- 風格要像 low-key GIF，不是電玩等級的動畫，避免喧賓奪主

設定建議：

- 長度：約 **15 秒**，夠長到使用者停留閱讀期間不會看到跳接
- 比例：**16:9**
- 解析度：**≥ 1080p**
- **不要開 enhance prompt**，要完整控制 prompt
- 產出不會一次到位，通常要 **4–5 次**才抽到堪用版本

替代模型：Kling 3.0、VO 3.1；目前 Seedance 2.0 是最好的選擇。

## 把影片接回 Claude Design

下載 MP4 後回到 Claude Design：

- 在 prompt 輸入框下方直接上傳 MP4
- 下 prompt：
  > Can we swap the still image for the video I just uploaded for the hero background?

就這麼簡單，hero 就會自動換成動畫背景。至此 Claude Design 端基本收工。

## 交給 Claude Code 收尾

hand off 流程：

1. 右上 **Share → Hand off to Claude Code**
2. 因為包含 MP4，用 `copy` 可能抓不下來 → 改選 **Download zip**
3. 本機解壓縮整個資料夾
4. 把解壓後的資料夾拖進 Claude Code，下 prompt：
   > Extract all these files for the web page we are building, and then spin up a dev server.

Claude Code 會展開檔案並啟動 dev server，接下來做細節微調、推 GitHub、部署 Vercel 即可。

## 要點整理

- 先構圖再下 prompt，構圖決定 hero 空間如何切
- 進 Claude Design 前備 2–3 個版面方向，截 Dribbble 範例一起丟
- 用 `Ask me any questions before you begin.` 觸發 Claude Design 的 plan mode
- Claude Design usage 單獨計費、很貴，集中做設計決策
- 迭代流程：**巨觀變體 → 鎖定一版 → aggressively 開 tweaks**
- hero 背景影片：極小動作、15 秒、16:9、1080p、關掉 enhance prompt、預期重抽 4–5 次
- 桌面用影片、手機用靜態圖，避免 mobile 體驗崩盤
- 90% 完成度就 hand off 到 Claude Code，用 Download zip 避免 MP4 下載失敗
