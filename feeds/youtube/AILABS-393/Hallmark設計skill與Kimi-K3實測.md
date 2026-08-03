---
title: Hallmark 設計 skill 與 Kimi K3 實測
description: 每個模型都有固定的設計慣性，Hallmark 以四個動詞與 58 項檢查把 agent 推離預設樣板；含在 Claude Code 內跑 Kimi K3 的接法與三模型對照
created: 2026-08-03
updated: 2026-08-03
source: https://www.youtube.com/watch?v=EwTOiqWWqEc
published: 2026-07-25
parent: "[[01.index]]"
tags:
  - youtube
  - frontend
  - design-system
  - claude-code
  - best-practices
---

核心論點：每個 AI 模型都有自己的設計慣性，用久了才會發現。新模型發布時大家都說它前端最強，前幾個網站確實不錯，但同一套模式會反覆出現在它產出的每個設計裡——不管是 Sonnet 4.5 還是 GPT 5.6。所以不論用哪個模型，都需要有東西把它推離預設，這正是好設計師在做的事。影片以 Hallmark 這個 skill 為例，並順帶實測 Kimi K3。

## Kimi K3 的定位

以下數字為影片引用 Artificial Analysis 與 LM Arena 的說法：

- Moonshot AI 的旗艦模型，加入百萬 token context window 陣營。
- 智慧面明顯領先 Opus 4.8 與新版 Gemini 3.6，略遜於 Fable 5 與 GPT 5.6，但差距小到基本屬同一級距。
- 前端設計面（LM Arena，同 prompt 對打並依真實使用者評價排名）甚至勝過那兩者。
- 表現好的一個原因是內建的 vision in the loop：多數模型只看程式碼推測網站長相，Kimi 會對自己做出來的東西截圖、檢視結果再調整。間距與版面因此更平衡、更像有意圖的安排。
- 價格是真正的優勢——每百萬 token 輸入 3 美元、輸出 15 美元；GPT 5.6 為 5／30，Fable 5 為 10／50。同級表現、三者中最低價。

## 為什麼不用 Kimi Code

Kimi 隨 K2.5 推出自家 terminal coding agent「Kimi Code」，但影片作者實測後不推薦：

- **慢**：Claude Code 或 Codex 約 3 分鐘的任務，Kimi Code 要接近 10 分鐘。原因一是權重尚未開放，模型只由 Kimi 自家伺服器託管，所有請求都得回到那裡，伺服器過載就都變慢；原因二是 harness 本身粗糙，Kimi 官方文件也承認它並非為發揮 K3 全部潛力而設計。
- **切模型會掉 context**：Codex 與 Claude Code 依任務頻繁換模型時都能保住脈絡，Kimi Code 的對話脈絡在換模型時會崩掉。
- **sub-agent 數量不透明**：執行時看起來開了非常多 sub-agent，事後詢問卻說只開了五個處理該任務。

## 在 Claude Code 裡跑 Kimi K3

直接走 Kimi API 會按讀寫字數計費、用量一大就很貴。較划算的做法是把已經在付的 Kimi 訂閱轉成本機 API：

1. 用 `brew install` 安裝 CLI proxy API——它把你已登入的 coding 工具轉成在本機執行的 API。
2. 執行 Kimi 登入指令，開啟登入頁完成登入。
3. 啟動 server 讓 Kimi 連線保持活著。
4. 為這個本機設定產生一組 API key（可以直接請 Claude Code 或你用的 agent 幫你設定），複製備用。
5. 啟動 Claude Code 時把請求的 URL 從 Claude 官方位址改指向本機 localhost，把上一步的 key 當作 Anthropic auth token 貼入，模型設為 Kimi K3，再執行 `claude`。

這些設定只存在於該終端 session，不是永久的；關掉後在新終端執行 `claude` 就回到原本的訂閱用法。

**注意**：Kimi 搭 Claude Code 時 auto compaction 不會執行。context window 填滿後它不會停下來，但回答會開始偏離指令、變得空泛，所以要自己管理 context。此外 skill 的自動觸發也不可靠——自動觸發是圍繞 Claude 自家模型調校的，Kimi 不是預設模型。用 slash command 手動叫起 skill 比較保險，確保它在開始建置前確實載入。

## Hallmark 的四個動詞

Hallmark 是一個 anti-AI-slop 的 agent 設計 skill，透過四個動詞使用：

- **預設**：直接告訴 agent 你要建什麼，它依 skill 指示中的工作流做出新 UI。
- **audit**：拿你的程式碼對照已知的反模式檢查，確認站上沒有這些問題。
- **redesign**：丟掉現有設計，往完全不同的方向重做一版。
- **study**：給它一個你喜歡的網站，它抽取該站的風格並朝那個方向做。

**study 的關鍵差異**：沒有 Hallmark 時，叫任何 agent 去研究一個網站，結果就是直接複製風格；Hallmark 明確阻止這件事，把該網站當作設計參考而非答案，所以產出仍然是原創的。

Hallmark 另附一個豐富的設計風格庫可供取用，官網有以各風格做成的 landing page 可視覺瀏覽，文件中的 `recipe.md` 則列出 prompt 最佳實務。

## 安裝

從 GitHub repo 複製安裝指令貼進終端即開始安裝。過程會問要裝給哪個 agent：

- 用 Kimi Code 或 Codex：不改任何選項直接繼續，裝進 `.agents` 資料夾（含這兩者在內許多 agent 用它放設定）。
- 在 Claude Code 裡跑 Kimi：要另外從清單中勾選 Claude Code，才會裝進 Claude 設定所在的 `.claude` 資料夾。

安裝後專案下 `.agents` 與 `.claude` 兩處都會有這個 skill。`SKILL.md` 記錄使用方式、如何被叫起與運作所需的一切。它勝過同類的地方在於帶了一百多份 references，涵蓋各種面向包含 AI slop 模式；交付成果前會跑 58 道檢查，確保網站沒有 slop 痕跡，另有元件與上述動詞的 references。

## 實測

### Kimi K3

- Kimi 本身也已長出自己的模式。因為中國模型常以蒸餾（拿另一個模型的輸出來訓練）Claude 系列模型的方式訓練，Opus 4.8 的風格在 Kimi 產出中很常見：hero 區塊後方放圖、大字 hero 文案偏移到一側、不論深淺色都往暖橘與棕色調色盤靠。
- 作者喜歡的一點是 Kimi 的文案不像 Opus 那樣塞滿行銷術語，讀起來每個東西都像是有意放在那裡。
- 執行 skill 後會先跑 **pre-flight**：檢視既有的設計風格相關檔案，判斷哪些可留、哪些要改。因為測試用的是剛開的 Next.js 樣板，它鎖定 Next.js 為框架、其餘丟棄。接著問三件事——受眾是誰、網站用途、語調。在 prompt 裡先講是最佳實務，但省略它也會自己問，不是硬性要求。回答後它從 references 拉出主題與其餘設定並建站，完成時確認 58 項 slop 檢測全數通過。
- 下 redesign 動詞會辨識該動詞、載入 redesign protocol、重問一次問題、跑同一套工作流，往與第一版完全不同的方向整個重建。
- audit 模式會重新載入 skill、依那些模式產出報告並標出每個發現，由你決定套用哪些修正。實測 audit 後 Kimi 執行了幾項修正：移除讓設計顯得像 AI slop 的字體、把圖片從 Unsplash 換到另一個圖庫 Pixum（因為幾乎每個模型都預設抓 Unsplash）、修好行動裝置 responsiveness，整體提升。

### Opus 4.8

- 先不裝 skill 跑一次：約 6 分鐘完成，成果是重度 AI slop，從配色、背景漸層到偏好的圓角方塊，全都是典型 Opus。
- 用作者團隊的 AI slop detector skill 掃描，標出大量問題，特別點名漸層文字。
- 再跑 Hallmark：載入 skill、跑 pre-flight、記錄模式、問同樣的問題、走完整個工作流。耗時遠比不用 skill 那次長，但成果更有創意、更像刻意設計，按鈕互動性明顯較好，來自模型對產品理解更深。
- 它預設不放佔位圖，因為抓 Unsplash 素材是規則裡的 slop 模式之一；定位是給產品開發者用，所以要求你自備圖片，而非退回 AI 生成或圖庫素材。
- 整體成果明顯優於 Kimi 那次。作者判斷這個 skill 目前搭 Claude 效果較好——它還沒有對 Kimi 的設計特性建立深度認識，只是拿其他模型的已知模式在標記。

### Codex

- Codex 的預設風格是綠白配（如同 Opus 預設橘、奶油與棕），設計偏重大量 SVG，字級相對螢幕偏小。成果在同儕中不差，但那些預設模式終究會浮現。
- 測試把 skill 裝在 `.agents` 資料夾，用 Codex app（內建 browser use 等能力），prompt 只說要建什麼。它跑完 pre-flight、問了受眾／用途／語調，接著編輯多個檔案、跑既有測試與一次互動式瀏覽器測試——它有瀏覽器能力且擅長這類事，就實際用上了。
- 成果比預設好很多。藍白組合仍略帶 AI 生成感，但在這裡讀起來像刻意選擇而非 slop，因為這組顏色與技術類網站調性相符；所有元素都不同於 Codex 的預設做法。hero 區塊的圖有些問題（選取分頁的視覺沒做對），但屬事後可修的層級。
- 跑 Hallmark audit 產出報告：整體結構良好，只剩少數問題，包含第一版常漏掉的 responsiveness。
