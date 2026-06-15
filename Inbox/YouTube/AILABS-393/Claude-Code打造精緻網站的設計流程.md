---
title: 用 Claude Code 打造精緻網站的四種設計流程
description: 拆解 marketing UI 與 functional UI 兩條設計路線，從 design skill、prompting guide、design.md、HTML mock-up 到 ShadCN 與 UI clone 的完整 harness 做法。
created: 2026-06-15
updated: 2026-06-15
source: https://www.youtube.com/watch?v=HqD5a2Cae60
published: 2026-06-13
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - frontend
  - ui-design
  - ai-agent
---

影片核心論點：模型大家都能用，差異在於圍繞模型建立的 harness（流程）。模型會持續演進，三個月前建好的 harness 很快過時，因此重點是讓 harness 能跟著任何模型一起進化。設計工作要分成兩條完全不同的路線：marketing UI（行銷頁）與 functional UI（功能介面 / dashboard），兩者的做法、動畫策略與工具鏈都不同。

## 模型會收斂到「平均設計」

模型傾向產出最安全、最平均的設計版本，Anthropic 稱之為「converging on the distribution」——模型會蓋出它看過上千次的東西。即使是被宣傳得很強的新模型也沒解決這問題。

- 實測：要求建一個 plantation 網站的 landing page，並提示「盡量有創意、別太在意內容」、刻意關閉所有 skill。產出不算差，但有對比度問題、部分圖片載入失敗，談不上最佳。
- 套用 Anthropic 官方 front-end design skill 後（skill 內沒有任何 reference 或外部資源，純粹就是一段 prompt），設計明顯更精緻、有細膩動畫與更多細節。

## 用 prompting guide 讓 skill 跟著模型進化

每出一個新模型，AI 公司會發新的 prompting guide。可把通用 design prompt 與該模型的 prompting guide 一起貼進 Claude，請它依新 guide 改寫出更新版 skill。

- 用 Fable 5 的 guide 改寫 design skill 後，產出結構更好、把元素轉成 card 排版，連 CTA 區塊都變成貼著郵票的明信片——這些小細節讓成品看起來更有創意。
- prompting guide 的另一用途是修模型的行為問題。Opus 4.8 推出時，Anthropic 指出該模型會預設某種設計風格，建議的修法是「先請模型給多個設計方向，再讓你挑」。
- Fable 5 的 guide 已不再提這問題，但實測該模型仍會回退到同樣風格——大約三分之二的產出仍是相似 styling，等於沒真正修好。因此值得回頭看舊模型的 docs，常有沒被收進最新 guide 的有用內容。

## design.md：品牌語言，但時機很重要

design.md 檔案內含品牌語言（顏色、間距、字體、元件、整體 styling），可直接套到頁面上。Get design.md 是不錯的來源，能取得許多品牌的檔案。

- 關鍵：**在模型已產出 landing page 之後**才套 design.md，且這只適用於 landing page。
- 原因：design.md 會把一切鎖死，連字體都鎖。而字體正是讓那些範例看起來更有創意的重要因素，太早套會扼殺創意空間。
- 在 functional UI（如 dashboard）上套 design skill 會讓它變好看，但會變得難用——marketing 與 functional 的設計策略必須分開。

## 動畫：marketing 用 GSAP，effort 拉高

加動畫分兩個層級：marketing UI 與 functional UI。

- marketing skill 預設讓模型加 CSS 動畫，但 GSAP 動畫效果好得多。
- effort 是現在控制模型的主要槓桿：簡單任務維持 low~medium 即可；加動畫這類任務用 X high 效果明顯更好、重試次數更少。
- 作者的 marketing UI skill 內有規則：符合特定條件時自動載入 GSAP skill。實測在 landing page 上即使規劃有限，仍能正確把螢幕動畫放進明信片內、讓四季依序轉場。

## Functional UI：先做 HTML mock-up，再轉應用

functional UI 流程與 marketing 完全不同，planning 是第一步且很關鍵。有了 plan 後，不要直接叫 Claude 建 app，而是**先用 HTML 建 mock-up**。

- 流程從 design.md 開始（沒有也可以略過）。作者自家社群平台「外部」與「內部」設計完全不同，內部都先用 HTML mock-up 規劃；他們先做一份部分靈感來自 Notion 的 design.md，用它把所有畫面做成 mock-up，驗證定稿後才轉成真正的應用。

## 用實驗探索不確定的設計方向

functional UI 還有一個重點是「實驗」。

- 早期做法：用 task list 開多個 agent 並行，各自產出不同 UI 變體來比較哪個最好。後來改用 sub-agent；但有了百萬 token context 後，用 primary agent 也能做，做法已不那麼重要。
- 自建 gallery viewer：產多份 HTML mock-up 時，自動把它們一起開在單一畫面中並排比較，避免淹沒在一堆檔案裡。
- 案例：做社群平台時不確定「社群互動空間」該長怎樣，於是讓 agent 產出多個 community channel UI 的 HTML mock-up 放進 gallery viewer 比較。
- 沒提供 design.md 時，產出的 mock-up 視覺不一致；有 design.md 時，模型會把它當顏色、間距、字體、元件、styling 的 source of truth，讓所有 mock-up 保持視覺一致，同時仍能探索不同 UX 方向。
- 動畫提醒：functional UI 不要過度加動畫，乍看驚豔但會讓以生產力為主的介面變得分散注意力。

## ShadCN skill：HTML markup 一鍵還原成元件

定稿設計後，下一步用 ShadCN skill。作者已把 functional UI skill 連到 ShadCN skill，多數流程自動完成。

- 過去流程複雜：要為 ShadCN MCP 產詳細實作 plan，再依 plan 建整個介面，雖可行但很繁瑣。
- 現在只需「最終 HTML markup + ShadCN skill」。ShadCN skill 由 ShadCN 創作者打包，內含大量 context 與實作知識，能把定稿 HTML markup 幾乎一比一還原成實際 ShadCN 元件，不必再做複雜的轉換 plan。

## 自我驗證與專案 context

- prompting guide 要求把 self-verification 寫明確：可在 Claude.md 放一段 prompt 要 agent 驗證輸出。驗證時不要用主 agent，改用 sub-agent，並讓它指向 design.md 作為比對基準。
- 模型在有任務 context 時表現更好。設計上需要知道產品實際是什麼；有些框架另設 product.md，但作者認為設好 Claude.md 已能讓模型理解專案。
- functional UI skill 每接到新任務就讓模型一併讀 Claude.md，並含一個 mocks 資料夾（放所有 HTML 檔）供新增元件時參考，再加上 design.md。

## Clone 現有 UI 的兩種模式

很多 SaaS app 可被輕易 clone，新模型理解圖片的能力大幅提升，使這流程變簡單。clone 分兩種模式：

- **Mode B（marketing UI）**：用 single file CLI 這個工具，可擷取一個頁面包含 HTML、CSS 與圖片；若站點有多頁，可抓 sitemap.xml 當網站地圖，讓模型據此發現並抓取其他頁面。
- **登入牆問題**：對 Notion 這種需登入的站，直接指向網址只會拿到 landing page，拿不到登入後的應用介面。此時 screenshot 是最佳選擇——要仔細擷取介面的不同狀態（hover、互動造成的版面變化、可分兩欄的版面等），務必提供模型所需的完整 context。
- **Mode A（用 screenshot）**：截好圖後不要直接貼進 prompt，而是把圖**拖**進 Claude，讓系統取得圖片路徑。Mode A 會蒐集所有 screenshot、放進 clone 資料夾當參考素材，作為 clone 的基礎；接著產出介面的初版 HTML，再進到建最終應用。
