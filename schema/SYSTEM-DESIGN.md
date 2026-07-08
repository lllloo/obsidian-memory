---
title: Vault 運作模式
created: 2026-05-25
updated: 2026-07-08
tags:
  - vault
  - meta
---

# 運作模式 — Karpathy LLM Wiki

> 這份文件給人看，用來建立整體心智模型。
> 可執行規則不放這裡：agent 維護規則、Ingest/Query/Lint、寫入慣例、唯一守門看 [`CLAUDE.md`](../CLAUDE.md)；導航與 tag 查詢看 [`vault-map.md`](vault-map.md)。

一句話：**wiki 是腦的延伸，LLM 幫你維護；Cards/Topics 是你自己的抽屜。**

## 這是 Karpathy 的 LLM Wiki

這個 vault 是 Karpathy [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 的實作。核心不是 RAG——RAG 每次查詢都從原始文件重新擷取、什麼都不累積；LLM Wiki 相反：**知識被編譯一次後由 LLM 持續維護**，交叉引用已建好、矛盾已標記、綜合已反映讀過的一切。wiki 是複利資產，每加一個來源、每問一個問題都讓它更豐富。

繁瑣的不是讀或想，是**書目整理**——更新交叉引用、保持摘要最新、維護數十頁一致。人類放棄 wiki 是因為維護負擔長得比價值快；LLM 不會無聊、不會忘記更新、可一次動十幾個檔，維護成本趨近於零，wiki 才得以持續存活。

## 三層架構

原文是三層，本 vault 照搬：

1. **`raw/`（原始來源）** — 你精選的原料，**不可變**。LLM 只讀不改，是事實來源。（YouTube 摘要、Clippings、Archive、Updates 及任何 raw 項。）
2. **`wiki/`（活知識庫）** — LLM 生成與維護的 markdown：摘要、實體、概念、比較、綜合。**LLM 完全掌管**——建頁、改頁、刪頁、交叉引用、維護 index，你只負責讀。
3. **schema** — 規範文件（[`CLAUDE.md`](../CLAUDE.md) / `AGENTS.md`），把 LLM 從通用聊天機器人變成「有紀律的 wiki 維護者」。

`index.md`（內容目錄）是 wiki 層內的特殊檔案，不是獨立層級。

## Cards/Topics 是使用者私人區，系統不管

`Cards/` 與 `Topics/` **不在上面三層裡**。它們是：

- **你的私人抽屜**：你自己愛放什麼放什麼，agent 完全不讀、不寫、不掃、不維護、不索引。
- **唯一對外公開層**：Quartz 只發佈 Cards/Topics。你從 wiki 讀到覺得不錯的內容，**手動**撿選、複製進去對外發表。

也就是說：wiki 是 LLM 幫你養的活知識庫（私有、只給你讀）；Cards/Topics 是你親手策展、決定對世界公開的成品。策展與公開與否完全在你手上，不是 agent 的職責。

這也回應 Karpathy 的反指標「**結構化垃圾場**」：AI 生一堆沒人讀、不拿來決策的精美 wiki 就只是垃圾。這裡的守門不是攔在 wiki 生成前（那會拖垮維護成本），而是攔在「你決定公開什麼」——wiki 讓 LLM 自由累積，你用「撿進 Cards/Topics」這個動作表達「這個我讀過、覺得值得對外」。

## 三個動作

- **Ingest（擷取）** — 新來源進 raw → LLM 讀 → 與你討論重點 → 寫/更新 wiki 頁、更新 index、更新相關實體/概念頁、標矛盾。單一來源可牽動多頁。
- **Query（查詢）** — 向 wiki 提問，LLM 讀 index → 找頁 → 綜合附引用的答案。好答案回存成新 wiki 頁，讓探索跟來源一樣複利。
- **Lint（健檢）** — 定期掃矛盾、過時主張、孤立頁、缺專屬頁的概念、缺交叉引用、資料空缺，產出修補與新探究建議。

規則見 [`CLAUDE.md`](../CLAUDE.md)。三動作的模型仍是本 vault 架構；目前只有「外部原料進 raw」有專屬 skill，其餘（wiki 綜合、查詢、健檢）由 agent 手動執行，核心 skill 待按需重建：

| 操作 | 做什麼 | 承載 |
|---|---|---|
| Ingest | 外部原料進 raw | `vault-youtube-sync`、`vault-updates-daily` |
| Ingest | 綜合維護進 wiki | 手動（原 `ob-write`／`vault-wiki-build` 已移除） |
| Query | 問 wiki，附引用綜合；好答案回存 wiki | 手動（原 `ob-read` 已移除） |
| Lint | 掃 wiki 孤立頁、死連結、矛盾、缺欄位等 | 手動（原 `vault-lint` 已移除） |

## 人 / AI 分工

- **你**：蒐集來源、提出問題、判斷價值、從 wiki 撿選公開進 Cards/Topics、拍板 `git push`。
- **AI**：讀、摘要、整理、交叉引用、歸檔、維護 wiki 一致性、結構健檢。

AI 承擔重複、瑣碎、容易被延後的維護工作，自主維護 wiki（含刪頁）不需逐步拍板。唯一硬守門是 `git push` 前要你同意（見 [`CLAUDE.md`](../CLAUDE.md)）。

## 版本抗性

把精確版本號釘死進 wiki 正文，下一版就過期，「校對過時資訊」變成永遠追不完的循環。wiki 正文留「行為怎麼變」的理解版本，易變細節（確切版本切換點）交給官方 changelog 由讀者回查。程式類 raw 會隨 API/framework 迭代而過期，但留著仍有回查價值——真正要防過期的是 wiki 正文。具體寫入規則見 [`CLAUDE.md`](../CLAUDE.md)。

## 刻意不做

這些不是缺功能，而是設計選擇：

- **不管 Cards/Topics**：它們是使用者私人抽屜兼唯一公開層，策展與公開完全交給人；agent 的 Ingest/Query/Lint 一律跳過。
- **不做自動成長掃描**：概念缺口、該連沒連這類成長面觀察，只在討論中浮現、只提議，不背景掃全 vault。可機械驗證的結構問題（孤立頁、死連結、tag 漂移、缺欄位）才交給 Lint 健檢（原 `vault-lint` 已移除，目前由 agent 手動執行）。
- **不寫 `log.md`**：Karpathy 建議的時序簿記檔，本 vault 暫不採用——操作時間軸靠 git log 與 commit 訊息即可，不另立一個需要人工同步、容易漂移的簿記檔。之後想要再補。
- **不上搜尋引擎（qmd 等）**：目前規模用 `rg` / harness-native Grep 夠用。等搜尋真的變痛再升級。

## 細節在哪

| 要找 | 看 |
|---|---|
| Agent 維護規則、Ingest/Query/Lint、寫入慣例、唯一守門 | [`CLAUDE.md`](../CLAUDE.md) |
| 全域導航與 tag 查詢地圖 | [`vault-map.md`](vault-map.md) |
| 通用 LLM Wiki 概念 | [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) |
