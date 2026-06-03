---
title: Vault 運作模式
created: 2026-05-25
updated: 2026-06-03
tags:
  - vault
  - meta
---

# 運作模式 — 半自動卡片盒

> 這份文件給人看，用來建立整體心智模型。  
> 可執行規則不放這裡：agent 寫入規則與 Cards -> Topics 升級門檻看 [`CLAUDE.md`](CLAUDE.md)，單張 Card 品質標準看 [`card-quality.md`](card-quality.md)，導航與 tag 查詢看 [`vault-map.md`](vault-map.md)。
> 執行邊界（刪除筆記需使用者拍板、`git push` 須明確同意、`Inbox/Clippings/` 不主動消化、`extracted_to` 半消化原篇留 Inbox 的合法性）均以 [`CLAUDE.md`](CLAUDE.md) 的基本原則、frontmatter 與整合流程規則為準，本文不重述。

一句話：**Vault 是腦的延伸，不是倉庫。**

## 來源脈絡

這個 vault 是三層東西疊起來：

- **卡片盒筆記法（Zettelkasten）**：底層方法。把知識拆成獨立可讀、彼此連結的卡片。
- **Karpathy 的 LLM Wiki 變體**：在 markdown wiki 上加一層 LLM 維護能力，讓摘要、交叉引用、歸檔這些維護工作成本大幅下降。原始概念見 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。
- **本 vault 的半自動策展調整**：整理與升級分類由 agent 協助、人工拍板；消化完就刪原始資料，只留下可覆寫、可更新的理解版本。

這不是 RAG。RAG 是查詢時臨時從原始資料重抓、重拼；這個 vault 則是讓 LLM 漸進維護一套相互連結的 markdown，作為你和外部資料之間的複利知識層。

## 為什麼不保留原始資料

三條原則合起來，形成這個 vault 對原始資料的處理方式：

- 吸收並內化
- 不留原始資料，只留參考資料
- Card 可覆寫、永不定稿

重點是：**消化後「我理解的版本」才是價值本體，原始資料可以丟**——前提是已內化；使用者尚未親自讀過的原料不適用。

這也是本 vault 和通用 LLM Wiki 最大的分歧。LLM Wiki 傾向保留不可變 raw sources，方便日後重新提煉；本 vault 選擇消化完直接刪 Inbox。只要 Card 自足、不靠原文也讀得懂，來源連結就只是回查用。連結死了也沒關係。

這點對程式筆記特別重要。API、framework、工具限制、best practice 都會隨時間迭代；過期 clipping 會增加判斷成本，甚至把舊資訊偽裝成仍可參考的知識。因此這裡不追求保存完整原始資料，而是保留當下已內化、之後可更新的理解版本。

### 版本抗性

同樣的時間迭代問題也會反過來咬筆記正文：把精確版本號釘死進 Cards / Topics，下一版就過期，於是「校對過時資訊」變成永遠追不完的循環。道理同上：筆記留「我理解的、之後可更新的版本」，易變細節交給官方文件。具體寫入規則（哪些版本號該留、行為約束別淡化）見 [`CLAUDE.md`](CLAUDE.md)。

## 工作流

Vault 分三層成熟度：

| 層級 | 角色 | 生命週期 |
|---|---|---|
| `Inbox/` | 外部原始資料暫存 | 消化完刪除 |
| `Cards/` | 未歸屬的完整概念 Card | 累積同主題後批次升 Topic |
| `Topics/<主題>/` | 已歸檔的主題知識 | 長期維護，持續覆寫 |

這三層不是單純分類資料夾，而是成熟度流動：未消化 → 待歸類 → 已歸檔。防爆量靠流動，不靠紀律。

**Inbox → Cards（消化）**：一份原料消化後有三種去向——內化成新 Card、強化既有 Card / Topic、或沒學到東西就直接刪；三者都以清空 Inbox 原篇作結，Inbox 空 = 無積欠（這裡的「空」指 agent 職責內的待消化佇列；`Inbox/Clippings/` 是使用者剪藏的參考原料，不在 agent 主動消化職責內、不計入積欠，見 [`CLAUDE.md`](CLAUDE.md)）。前提是使用者本人已讀過／看過；AI 代摘要但本人尚未消化的原料不算內化，留 Inbox 當待讀佇列。

**Cards → Topics（歸檔）**：Card 是完整概念，獨立可讀、不靠原文就能懂。同主題累積成群、或單張裂變成多張時，成批搬進 `Topics/<主題>/`。跨主題靠 `tags` 串連，`Topics/` 第一層不做跨主題巢套（不建「AI-工具/Claude-Code/」這種群組）。

具體操作步驟（三條清空路徑、`extracted_to` 半消化例外、`Inbox/Clippings/` 不主動消化、`git mv` 歸檔與補 `index.md` wikilink）均見 [`CLAUDE.md`](CLAUDE.md)；升 Topic 門檻見 CLAUDE「Cards -> Topics 升級限制」，單張卡品質與反指標見 [`card-quality.md`](card-quality.md)。已升 Topic 重看若命中反指標可退回 Cards，仍須使用者拍板。

主要操作由 skills 承載：

| 操作 | 做什麼 | 承載 |
|---|---|---|
| 擷取 / 消化 | skill 把外部原始資料帶進 Inbox（`ob-write` 亦可依使用者指示直接回存 Cards）；內化與刪原篇由使用者執行 | `ob-write`、`vault-youtube-sync`、`vault-updates-daily` |
| 查詢 / 回存 | 問 vault；若答案有複利價值，只提議回存，等你拍板 | `ob-read`（查）、`ob-write`（回存）、`CLAUDE.md` 查詢回存規則 |
| 主題整合 | 多篇相關筆記整合成整合頁或 Topic 入口 | 當前 agent 依 `CLAUDE.md` 多筆記整合規則執行 |
| 結構健檢 | 掃孤立頁、死連結、tag 漂移、缺欄位等結構問題 | `vault-lint` |

## 人 / AI 分工

- **你**：蒐集來源、提出問題、判斷價值、拍板是否回存、刪除或升 Topic。
- **AI**：消化、摘要、整理、交叉引用、歸檔、結構健檢。

AI 可以承擔重複、瑣碎、容易被延後的維護工作；但不自主決定知識是否值得留下。回存、刪除、升 Topic 都要你拍板。維護動作（如建立新 Card 時順手在 1–2 篇最相關既有筆記補入站 wikilink，避免新卡一建立就孤立）屬已授權任務的合理組成，不需逐次拍板，與「決定知識去留」的拍板權分屬兩件事；具體見 [`CLAUDE.md`](CLAUDE.md)。

## 刻意不做

這些不是缺功能，而是設計選擇：

- **不保留原始資料**：程式筆記會快速過期；保留 raw clipping 不一定更安全，反而可能增加判斷成本。
- **不做自動成長掃描**：概念缺口、該連沒連、資料空缺這類成長面觀察，只在討論中浮現、只提議、不背景掃全 vault。結構問題才交給 `vault-lint` 主動掃。這是刻意的界線——成長判斷需讀正文語意、帶不確定性，拖進 lint 會拖慢結構快掃、也難以 deterministic 化；lint 只做可機械驗證的結構問題（孤立頁、死連結、tag 漂移、缺欄位）。
- **不寫 `log.md`**：操作時間軸靠 git log 與 commit 訊息即可，不另立一個需要人工同步、容易漂移的簿記檔。
- **不上搜尋引擎（qmd 等）**：目前規模用 `rg` + Obsidian CLI 夠用。等搜尋真的變痛再升級。

## 細節在哪

| 要找 | 看 |
|---|---|
| Agent 寫入規則、寫入前 checklist、frontmatter、tag / 命名 | [`CLAUDE.md`](CLAUDE.md) |
| Cards → Topics 升級門檻（決策準則 + 執行流程） | [`CLAUDE.md`](CLAUDE.md) |
| 單張 Card 品質標準與反指標 | [`card-quality.md`](card-quality.md) |
| 全域導航與 tag 查詢地圖 | [`vault-map.md`](vault-map.md) |
| 通用 LLM Wiki 概念 | [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) |
