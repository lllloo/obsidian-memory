---
title: 用 Claude Code 做出真正會轉換的 Carousel 混合工作流
description: 純 HTML 做的社群 carousel 千篇一律、零互動；改用封面圖交給 AI 影像模型、內頁交給 Claude Code HTML 的混合三步法，兼顧視覺與可規模化重複產出。
created: 2026-06-03
updated: 2026-06-03
source: https://www.youtube.com/watch?v=7taGazHQkMg
published: 2026-06-02
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - social-media
  - ai-image
---

社群媒體（尤其 AI 圈）充斥用 Claude Code 純 HTML 產的 carousel，外觀千篇一律、互動率近零。Carousel 是目前轉換率最高的社群內容形式之一，要脫穎而出得跳脫這個趨勢。作者主張用「混合工作流」：封面圖交給外部 AI 影像模型，內頁交給 Claude Code 的 HTML，兼顧視覺衝擊與可規模化的重複產出。

## 核心原則：封面 vs 內頁分工

- **封面（cover image）**：使用者滑動時第一眼看到的東西，必須最具視覺衝擊力。這一張才值得動用外部 AI 影像生成（GPT Image 2、Nano Banana Pro 等）。
- **內頁／價值頁（body slides）**：封面已經把人勾進來，內頁重點是給實際價值，不需要每張都驚艷。用 Claude Code 自己產的 HTML asset 就夠。
- 動機是平衡速度與品質：用 AI 影像模型產圖既慢又花錢（每張都付費），一個 carousel 可能多達 10 張，全部用影像模型不切實際。封面用影像模型、其餘走 HTML，才能快速、便宜、可重複地系統化產出。

## 三步流程

### Step 0：找靈感、建素材庫

- 動手前先做研究，看別的領域什麼 carousel 格式有效，當作起點；從白紙開始會很痛苦又費時。
- 到 Instagram、TikTok 搜「carousel」往下滑，看什麼視覺抓住你的眼球。喜歡的就截兩張圖：封面一張、內頁一張。
- 第一次做建議至少花 20–30 分鐘，開始累積一個視覺靈感素材庫。刻意去看自己利基（niche）以外的領域，把外部風格帶進自己的領域才會與眾不同——不是抄，是取靈感。
- 為當次製作鎖定一個想參考／套版的範本。

### Step 1：安裝 Higsfield CLI

- 作者用 Higsfield CLI 透過 terminal 存取各種 AI 影像生成工具（Nano Banana、GPT Image 2 或下週新出的任何模型），不綁單一工具。也有 MCP 版，但作者偏好 CLI。
- 流程：到 Higsfield.ai → MCP and CLI 分頁 → CLI → 用指令安裝 → 跑 `higsfield login` 登入帳號 → 可再加入相關 skills。
- 先建一個 carousel 資料夾（作者命名 `Chase AI carousels`，名稱隨意）。長期目的是累積自己表現好的 carousel 素材庫，之後可直接叫 Claude Code「去做 carousel 第 10 版、換成這個主題」。

### Step 2：用 AI 影像模型做封面

- 把選定的參考封面截圖丟進 Claude Code，prompt 大致是：這是我要當靈感的圖、用 Higsfield CLI、用指定影像模型（如 GPT Image 2），接著說明要跟原圖有何不同。
- 範例需求（主題為「六月份 Claude Code 前五大 plugins」）：保留原圖整體美學，但把中間的女性雕像換成男性；把 Photoshop 圖示換成 GitHub／Anthropic 圖示；換掉文字；指定 GPT Image 2、長寬比盡量接近 4:5、高品質 2K、一次產四張。
- 若不確定某影像模型需要哪些輸入參數，Claude Code 具備對應 skill 與 CLI 知識，可直接問它建議。關鍵是把 prompt 講清楚要改什麼。
- 這是一個迭代式創作過程，很少一次到位（one-shot），通常要來回幾次微調。正因如此才只對封面這麼搞——若每張內頁都這樣做太花時間。
- 加文字的兩種做法：把選定的圖餵回 Claude Code，叫它「其他都不要動，只在上方加文字」；或把圖帶進 Canva 之類工具自己手動加。作者示範前者，並要求文字部分套用如雕像眼睛那種彩虹漸層（rainbow gradient）效果，一樣產四個版本挑一個。

### Step 3：用 Claude Code HTML 做內頁

- 內頁＝封面之後的所有頁。空間有限：一張圖、一個標題、一兩行文字。當成 PowerPoint 投影片來經營，不要塞滿文字，講求 economy of action（精簡）。
- 幾乎全部由 Claude Code 用 HTML 產，唯一例外是作者手動提供的截圖；但 Claude Code 也能自己產（例如示意 terminal 的圖就是它自己畫的）。
- prompt 思路：先說「封面已鎖定，現在做內頁，要純 HTML、能在瀏覽器打開、能做微調」。給它一張自己舊 carousel 截圖當內頁範本（喜歡其文字風格、背景等）。要求能在瀏覽器移動元素、改字級、改文字內容；若改動需把 JSON 複製回來也接受，但要盡量簡單。
- 範例：要五張內頁對應六月五個 plugins，指定其中三個為 caveman、codex plugin、Impeccable，其餘兩個讓 Claude Code 自己研究 GitHub 後補上文案——作者完全沒給文案，由它自行研究產出。
- 這些 raw prompt 全都可以再 codify 成 skills。作者有自己一整套 skills 與 carousel 範例（放在其付費社群）。

## Tweak Loop：瀏覽器即時微調

- Claude Code 會連同 HTML 一起建出一個「tweak」介面，靈感來自 Claude design 的 tweak mode。
- 可即時調整 headline 大小、body 字級、背景透明度、卡片傾斜等，所有屬性都能調。
- 改完後底部有 export tweaks（輸出成 JSON）。把 JSON 貼回 Claude Code，它就會自行套用更新。可同時對多張投影片改，再一次匯出。

## 強化內頁：換真實截圖／網路找圖

- 內頁最能加分的是換上真實截圖。例如 caveman mode 那頁，去 caveman 的 GitHub 截圖，貼進 Claude Code 說「把這張當 caveman 圖換掉你生的那張」，再逐張重複此流程。
- 也可叫 Claude Code 上網替各項目找合適圖片，不限 HTML 或手動截圖，發揮空間大。

## 總結與心法

- 三步法（找靈感 → 外部 AI 影像模型做封面 → HTML 做內頁）給出可持續、可重複的流程，兼得兩邊好處：AI 影像的創意與視覺，HTML 當骨幹且夠易執行、能規模化，不用每天枯坐電腦數小時。
- 累積到第 20 個 carousel 時，已有預建範本，不必再重跑找靈感、微調那套，只要換文案即可。
- 別掉進「只要 Claude Code 裡一個 skill 就夠」的陷阱；多做一點點（建立 foundation）就能明顯勝過市面上千篇一律的成品。
