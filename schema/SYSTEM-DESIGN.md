---
title: Vault 運作模式
created: 2026-05-25
updated: 2026-07-08
tags:
  - vault
  - meta
---

# 運作模式 — Karpathy LLM Wiki

> 這份文件給人看，用來建立整體心智模型，逐節對齊 Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。
> 可執行規則不放這裡：agent 維護規則、Ingest/Query/Lint、寫入慣例、唯一守門看 [`CLAUDE.md`](../CLAUDE.md)；導航與 tag 查詢看 [`vault-map.md`](vault-map.md)。

一句話：**wiki 是腦的延伸，LLM 幫你維護；Cards/Topics 是你自己的抽屜。**

## 核心構想

多數人對「LLM + 文件」的體驗是 RAG：上傳一堆檔案，查詢時 LLM 即時檢索相關片段、生成答案。能用，但 **LLM 每次都從零重新發現知識**，什麼都沒累積。問一個需要綜合五份文件的細膩問題，它每次都得重新找、重新拼。NotebookLM、ChatGPT 上傳、多數 RAG 都是這樣。

這裡的做法相反：LLM **漸進地建立並維護一套持久的 wiki**——一批結構化、互相連結的 markdown，夾在你與原始來源之間。新來源進來，LLM 不只是索引它以備查詢，而是讀它、抽取重點、**整合進既有 wiki**：更新實體頁、改寫主題摘要、標記新資料與舊主張的矛盾、強化或挑戰演進中的綜合。知識被**編譯一次後持續保鮮**，不是每次查詢重推導。

關鍵差異：**wiki 是一份持久、複利的資產。** 交叉引用已經建好、矛盾已經標記、綜合已經反映你讀過的一切。每加一個來源、每問一個問題，wiki 都更豐富。

你（幾乎）從不親手寫 wiki——LLM 全權書寫與維護。你負責蒐集來源、探索、問對問題；LLM 做所有 grunt work：摘要、交叉引用、歸檔、簿記，這些才是讓知識庫長期真正有用的苦工。實作上一邊開 LLM、一邊開 Obsidian：LLM 依對話改動，你即時瀏覽——跟連結、看圖譜、讀更新後的頁。**Obsidian 是 IDE，LLM 是程式設計師，wiki 是 codebase。**

## 可以應用在哪

同一模式適用很多情境（原文舉例，供理解本 vault 可長成什麼樣）：

- **個人**：追蹤目標、健康、心理、自我成長——歸檔日記、文章、Podcast 筆記，逐步建出對自己的結構化圖像。
- **研究**：數週數月深挖一題——讀論文、報告，漸進建出帶演進論點的完整 wiki。
- **讀一本書**：邊讀邊歸檔每章，長出角色、主題、情節線與其關聯的頁，讀完得到一份豐富的伴讀 wiki（想像 fan wiki 那種上千互聯頁）。
- **團隊/商業**：由 LLM 維護、餵入 Slack 討論、會議記錄、專案文件的內部 wiki，人在迴路審更新。wiki 保持最新，因為沒人想做的維護由 LLM 做。
- **競品分析、盡職調查、行程規劃、課程筆記、興趣深挖**——任何「隨時間累積知識、想要有序而非散落」的場景。

本 vault 的實際落點偏 **coding agent / LLM 工具生態** 的個人研究知識庫（見 [`vault-map.md`](vault-map.md) 的 tag 地圖）。

## 架構：三層

原文是三層，本 vault 照搬：

1. **`raw/`（原始來源）** — 你精選的原料：文章、影片摘要、剪貼、資料。**不可變**，LLM 只讀不改，是事實來源。本 vault 分 `YouTube/`、`Clippings/`、`Archive/`、`Updates/`。
2. **`wiki/`（活知識庫）** — LLM 生成與維護的 markdown：摘要頁、實體頁、概念頁、比較頁、綜合頁。**LLM 完全掌管**——建頁、改頁、刪頁、交叉引用、維護 index，你只負責讀。
3. **schema** — 規範文件（[`CLAUDE.md`](../CLAUDE.md) / `AGENTS.md`），告訴 LLM wiki 怎麼組織、慣例是什麼、Ingest/Query/Lint 各走什麼流程。這是把 LLM 從通用聊天機器人變成**有紀律的 wiki 維護者**的關鍵設定，你與 LLM 隨時間共同演進它。

### 本 vault 的額外層：Cards/Topics（不在原文三層裡，系統不管）

`Cards/` 與 `Topics/` 是本 vault 疊在三層之上的擴充，**不屬於 Karpathy 模型**：

- **你的私人抽屜**：你愛放什麼放什麼，agent 完全不讀、不寫、不掃、不維護、不索引。
- **唯一對外公開層**：Quartz 只發佈 Cards/Topics。你從 wiki 讀到覺得不錯的內容，**手動**撿選、複製進去對外發表。

wiki 是 LLM 幫你養的活知識庫（私有、只給你讀）；Cards/Topics 是你親手策展、決定對世界公開的成品。這也回應 Karpathy 的反指標「**結構化垃圾場**」：AI 生一堆沒人讀、不拿來決策的精美 wiki 就只是垃圾。守門不攔在 wiki 生成前（那會拖垮維護成本），而攔在「你決定公開什麼」——用「撿進 Cards/Topics」這個人為動作表達「這個我讀過、值得對外」。

## 三個動作（Operations）

- **Ingest（擷取）** — 你把新來源丟進 raw、叫 LLM 處理。典型流程：LLM 讀來源 → 與你討論重點 → 寫一頁摘要 → 更新 index → 更新橫跨 wiki 的相關實體頁/概念頁 → 標矛盾。**單一來源可牽動 10–15 頁。** 可一次一源、你在旁導引，也可較少監督地批次 ingest；發展出適合自己的節奏並寫進 schema。
- **Query（查詢）** — 向 wiki 提問，LLM 先讀 index → 找相關頁 → 讀頁 → **附引用**綜合答案。答案形式依問題而定（markdown 頁、比較表、投影片、圖表、canvas）。關鍵洞見：**好答案可回存成新 wiki 頁**——你要的比較、分析、發現的關聯很有價值，不該消失在對話裡；這樣探索跟來源一樣複利累積。
- **Lint（健檢）** — 定期請 LLM 體檢 wiki：矛盾、被新來源取代的過時主張、無入連的孤立頁、被提到卻缺專屬頁的概念、缺交叉引用、可用 web 搜尋補的資料空缺。LLM 也擅長提議「該再查的問題」與「該找的來源」，讓 wiki 隨成長保持健康。

三動作的模型是本 vault 架構；目前只有「外部原料進 raw」有專屬 skill，其餘（wiki 綜合、查詢、健檢）由 agent 手動執行，核心 skill 待按需重建：

| 操作 | 做什麼 | 承載 |
|---|---|---|
| Ingest | 外部原料進 raw | `vault-youtube-sync`、`vault-updates-daily` |
| Ingest | 綜合維護進 wiki | 手動（原 `ob-write`／`vault-wiki-build` 已移除） |
| Query | 問 wiki，附引用綜合；好答案回存 wiki | 手動（原 `ob-read` 已移除） |
| Lint | 掃 wiki 孤立頁、死連結、矛盾、缺欄位等 | 手動（原 `vault-lint` 已移除） |

## 索引與日誌

原文用兩個特殊檔幫你在 wiki 長大時導航，用途不同：

- **`index.md`（內容導向）** — wiki 內容的目錄：每頁一行摘要 + 連結，按類別（實體、概念、來源…）分組，**每次 ingest 更新**。查詢時先讀 index 找相關頁，再鑽細節。在中等規模（約 100 來源、數百頁）很好用，省去 embedding-based RAG 基建。本 vault 落在 [`wiki/01.index.md`](../wiki/01.index.md)。
- **`log.md`（時序導向）** — 原文建議的 append-only 記錄：ingest / query / lint 何時發生什麼。若每條用固定前綴（如 `## [2026-04-02] ingest | 標題`），用 `grep "^## \[" log.md | tail -5` 就能看最近幾筆。**本 vault 目前不採用**——操作時間軸靠 git log 與 commit 訊息即可，不另立一個需人工同步、容易漂移的簿記檔。之後想要再補。

## 選配：CLI 工具

wiki 長大後可能想要能更有效操作它的小工具，最明顯的是 **wiki 頁全文搜尋**。小規模時 index 檔就夠；長大後想要正經搜尋（如 [qmd](https://github.com/tobi/qmd)，本地 markdown 混合 BM25/vector 搜尋，含 CLI 與 MCP），也可自己 vibe-code 一支簡單搜尋腳本。**本 vault 目前規模用 `rg` / harness-native Grep 夠用**，等搜尋真的變痛再升級。

## 訣竅（Tips）

原文的實用招式與本 vault 對應現況：

- **Obsidian Web Clipper**：瀏覽器擴充，把網頁轉 markdown 快速進 raw。本 vault 已用（`.clipper/`，產出進 `raw/Clippings/`）。
- **本地下載圖片**：把附件路徑設成固定資料夾（如 `raw/assets/`）、綁快捷鍵下載，讓 LLM 能直接看圖而非依賴會失效的 URL（LLM 無法一次讀含內嵌圖的 markdown，須先讀文字、再分開看圖）。**本 vault 以文字為主，尚未採用**；來源含關鍵視覺時再開 `raw/assets/`。
- **圖譜視圖（graph view）**：看 wiki 形狀的最佳方式——什麼連什麼、哪些是樞紐、哪些是孤島。要讓筆記進圖譜，frontmatter 加 `parent: "[[01.index]]"`。
- **Marp**：markdown 投影片格式，Obsidian 有 plugin，可從 wiki 內容直接生簡報。本 vault 目前未用。
- **Dataview / Bases**：對 frontmatter 跑查詢生動態表。本 vault 用 Obsidian **Bases**（`.base`）取代 Dataview，如各索引頁的 `清單.base`／`02.影片清單.base`。
- **git repo**：wiki 就是一個 markdown 的 git repo——版本歷史、分支、協作免費得到。本 vault 即是。

## 為何有效

維護知識庫的苦不在讀或想，而在**簿記**：更新交叉引用、保持摘要最新、標記新舊矛盾、維護數十頁一致。人類放棄 wiki，是因為維護負擔長得比價值快。**LLM 不會無聊、不會忘記更新某條交叉引用、可一次動 15 個檔**——維護成本趨近於零，wiki 才得以持續存活。人的工作是策劃來源、導引分析、問好問題、思考這一切的意義；其餘全交給 LLM。

思想上與 Vannevar Bush 的 **Memex（1945）** 一脈：私有、主動策劃、文件間的關聯與文件本身一樣有價值的個人知識庫。Bush 沒解決的是「誰來維護」——這由 LLM 補上。

## 人 / AI 分工與唯一守門

- **你**：蒐集來源、提出問題、判斷價值、從 wiki 撿選公開進 Cards/Topics、拍板 `git push`。
- **AI**：讀、摘要、整理、交叉引用、歸檔、維護 wiki 一致性、結構健檢。

AI 承擔重複、瑣碎、容易被延後的維護工作，自主維護 wiki（含刪頁）不需逐步拍板——這正是「維護成本趨近於零」的重點。唯一硬守門是 **`git push` 前要你同意**（見 [`CLAUDE.md`](../CLAUDE.md)）。

## 版本抗性

把精確版本號釘死進 wiki 正文，下一版就過期，「校對過時資訊」變成永遠追不完的循環。wiki 正文留「行為怎麼變」的理解版本，易變細節（確切版本切換點）交給官方 changelog 由讀者回查。程式類 raw 會隨 API/framework 迭代而過期，但留著仍有回查價值——真正要防過期的是 wiki 正文。具體寫入規則見 [`CLAUDE.md`](../CLAUDE.md)。

## 刻意不做

這些不是缺功能，而是設計選擇（原文皆為「optional / 建議」，本 vault 按需取捨）：

- **不管 Cards/Topics**：使用者私人抽屜兼唯一公開層，策展與公開完全交給人；agent 的 Ingest/Query/Lint 一律跳過。
- **不做自動成長掃描**：概念缺口、該連沒連這類成長面觀察，只在討論中浮現、只提議，不背景掃全 vault。可機械驗證的結構問題（孤立頁、死連結、tag 漂移、缺欄位）才交給 Lint。
- **暫不寫 `log.md`**：見上「索引與日誌」，用 git log 代替。
- **暫不上搜尋引擎（qmd 等）**：見上「選配」，現階段 Grep 夠用。
- **暫不做圖片/assets 下載、Marp 簡報**：文字為主，需要時再開。

## 細節在哪

| 要找 | 看 |
|---|---|
| Agent 維護規則、Ingest/Query/Lint、寫入慣例、唯一守門 | [`CLAUDE.md`](../CLAUDE.md) |
| 全域導航與 tag 查詢地圖 | [`vault-map.md`](vault-map.md) |
| 通用 LLM Wiki 概念（原文） | [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) |
