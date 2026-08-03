---
title: 三步驟擺脫 AI slop：把個人品味注入 AI 網頁設計
description: 先建立設計靈感庫養出品味，再裝 impeccable、Taste Skill、Higgsfield MCP 等外部工具，最後用四要素 prompt 一次生五版再收斂迭代。
created: 2026-08-03
updated: 2026-08-03
source: https://www.youtube.com/watch?v=7FU98O0JLHs
published: 2026-07-23
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - web-design
  - prompt-engineering
  - workflow
---

## 問題不是技術，是通用

AI slop 一直在變形：早期是配 Inter 字體、藍紫漸層的通用 SaaS 樣板；現在的版本好看多了，但仍然一眼看得出是 AI 產的——固定的配色、固定的字體、一種一望即知「兩三個 prompt 生出來」的風格。

關鍵論點：這不是技術問題，是**通用**問題。模型明天強十倍也只是改變「什麼算通用」的定義而已。唯一的解法是把使用者自己的品味注入設計流程——那是主觀且獨一無二的，所以產出才會獨特。

## 步驟一：養出品味，建立靈感庫

先大量曝光高水準的網頁設計，再把喜歡的東西收成一個庫，之後拿它當所有設計的基底，而不是讓 AI 從零產出「回歸平均值」的東西。

找靈感的地方：

- **Dribbble**：搜 web design、切 popular，看大量 landing page。
- **Pinterest**：同樣搜 web design，能看到跟 Claude 預設產出很不一樣的 hero page。
- **Twitter**：作者最偏好的一個，因為圈內有很多創作者在做別處看不到的設計與 UI 實驗。

做法就是逛、看到喜歡的就截圖存下來，有網址就連網址一起存。截圖可以就放在一個資料夾，作者則是讓 Claude Code 做了一個簡單的 web app 當靈感庫：

- 把素材集中在一處，並依**設計類型**自動分組。
- 讓 AI 解釋這個設計是什麼、代表什麼、對應的設計詞彙是什麼（例如「Voxel 渲染風景」這類關鍵詞）。
- 每張圖提供兩個按鈕：**copy image prompt**（拿去生 hero 背景圖）與 **copy brief**（拿去生整個網站）。

重點在於剛起步時腦中還長不出東西，需要先找到「確實有效、而且你喜歡」的東西當基底。

## 步驟二：給 Claude Code 外部工具

### impeccable

作者認為目前最強的前端設計 skill，開源、GitHub 上將近 50,000 星，已被納為 GitHub AI 工具的官方一部分。

- 是**一個** skill，但內含 23 個指令，各自從不同角度改造網站或元件：批評問題、加細節打磨、`bolder`（把安全的設計往有衝擊力推、但不至於失控）、`overdrive`、`clarify`（把冗長警告壓縮成好讀的版本）等。
- 官網 impeccable.style 左側列出全部 23 個指令，每個都有「Claude Code 標準輸出 vs. 加了 impeccable」的對照圖，是理解它們差別最快的方式。
- 本質是在七個面向辨識並清除 slop：typography、色彩、空間設計、responsiveness、互動、動效、UX 文案。官網有一整區專講 slop，拆成 46 種模式。
- 附 CLI：可以掃過整個專案指出哪裡是 AI slop，並在 dev server 上視覺化呈現。另有 live mode，能開著網站逐元件點選、即時調整——補上純終端機拿不到的視覺維度。
- 安裝提供三種方式；搞不清楚就把網址貼給 Claude Code 讓它幫你裝。

### Taste Skill

替代選項，GitHub 星數略低於 66,000，v2 剛釋出但仍屬 experimental。同樣是抓 AI slop 的尾巴，改善版面、typography、動效與間距，目標是產出獨特而非樣板感的 UI。

作者認為 impeccable 與 Taste Skill 明顯優於 Anthropic 內建的 front-end design，也優於 UIUX Pro Max 這類熱門 repo。

### Higgsfield MCP

補上 Claude Code 原生沒有的能力：**圖片生成與影片生成**。它接通幾乎所有主流 AI 圖片／影片生成器；作者圖片多用 GPT Images 2，影片則隨市場變動（當時最好的是 SeaDance）。到 higgsfield.ai 的 MCP and CLI 頁複製指令貼進 Claude Code，跟著跑完認證即可，另有一些 skill 可加裝。裝好後要做 hero 背景圖或客製素材時，Claude Code 會自動呼叫它生成。

### 21st.dev

不是 skill 也不是 MCP，比較接近步驟一的品味範疇，但層級更低——專講**元件**。左側可挑 buttons、cards、pricing section、border、background、call to action 等，點進任一元件可 copy prompt，貼進 Claude Code 就會生出那個樣子的元件。價值在於逼自己去看平常根本不會想到的細節（例如 pagination 有哪些做法）。

### 工具的陷阱

不要掉進「再裝一個 skill 就能解決所有設計問題」的兔子洞。網路上很多很酷的 skill 能產出很酷的網站，但它們**範圍窄、極度規範性（prescriptive）**，通常只吐得出一種風格的東西。推薦 impeccable、Taste Skill、Higgsfield 正因為它們彈性大、可以往很多方向走；代價是它們不會自動給你好結果——結果好壞取決於你的 prompt 與品味注入。

## 步驟三：不要一次到位，撒網再收斂

核心心法：**放棄 one-shot**。一開始就撒大網。

作者的實作是替一家虛構 AI 公司 Argus 做網站，一次生五個不同風格的版本，而且左半用 impeccable、右半用 Taste Skill 做對照。

收斂節奏：

1. 先看五種風格 → 大致確定要走的方向（例如 print tech 紙感風）。
2. 對選中的風格再做三個變體 → 從三個裡挑一個。
3. 挑定後才進入微調。
4. 風格定了才引入 Higgsfield MCP 生 hero 圖與各種素材。

這樣做的理由是：所有選項要能**同時攤在一個畫面上**比較。窩在終端機裡一次試一個、再試下一個，很難知道自己到底想往哪走。

### prompt 的四個要素

刻意不做那種一萬頁的 `design.md`——別人給你的那種東西每次都產出一樣的結果、範圍極窄。作者每次只傳四樣東西：

- **Aesthetic（美學）**：這個網站大致屬於哪個設計家族。
- **Reference image（參考圖）**：從品味庫拿一張或多張。目標是**match the feel**，不是抄內容或抄設計。不必只用截圖，直接丟喜歡的網站 URL 也可以。
- **Intent（意圖）**：在做什麼、為什麼做。是 SaaS 產品還是活動頁？目標受眾是誰？希望他們讀完就好、點進某處，還是填表單？這會決定網站其他部分長什麼樣。
- **Guardrails（護欄）**：永遠要做什麼、永遠不要做什麼。這裡正好處理 AI slop——例如「絕不要紫色漸層」「絕不要 Inter 字體」。

如果已經建好品味庫，可以直接說「看一下我的庫，挑五個美學家族生五個網站」；沒有庫就明確說「我要五個不同風格的版本」，一樣可行。

### 實際示範

作者的 prompt 大意是：替 Kestrel（服務小型新創的 AI 分析平台）做 landing page，意圖是讓訪客預約 demo；護欄是所有 hero 頁都要有一張紀念碑級的大圖、絕不出現紫色漸層與 3D SaaS blob 那類 AI slop；要求生五個版本，並逐版指定美學方向、附上品味庫來的參考圖、說明 hero 區大概長什麼樣。

產出的五版中，print tech 紙感版把資料本身當成材質使用；所有圖像素材都是 Claude Code 生的，沒有靠 HTML／CSS 去刻圖形。
