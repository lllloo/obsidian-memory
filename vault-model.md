# 運作模式 — 吸收型卡片盒

> 這份文件給人看，用來建立整體心智模型。  
> 可執行規則不放這裡：agent 寫入規則看 [`CLAUDE.md`](CLAUDE.md)，升 Topic 門檻看 [`topics-review.md`](topics-review.md)，導航與 tag 查詢看 [`master-index.md`](master-index.md)。

一句話：**Vault 是腦的延伸，不是倉庫。**

## 來源脈絡

這個 vault 是三層東西疊起來：

- **卡片盒筆記法（Zettelkasten）**：底層方法。把知識拆成獨立可讀、彼此連結的卡片。
- **Karpathy 的 LLM Wiki 變體**：在 markdown wiki 上加一層 LLM 維護能力，讓摘要、交叉引用、歸檔這些維護工作成本大幅下降。原始概念見 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。
- **本 vault 的吸收型調整**：消化完就刪原始資料，只留下可覆寫、可更新的理解版本。

這不是 RAG。RAG 是查詢時臨時從原始資料重抓、重拼；這個 vault 則是讓 LLM 漸進維護一套相互連結的 markdown，作為你和外部資料之間的複利知識層。

## 為什麼不保留原始資料

三條原則合起來，形成這個 vault 對原始資料的處理方式：

- 吸收並內化
- 不留原始資料，只留參考資料
- Card 可覆寫、永不定稿

重點是：**消化後「我理解的版本」才是價值本體，原始資料可以丟。**

這也是本 vault 和通用 LLM Wiki 最大的分歧。LLM Wiki 傾向保留不可變 raw sources，方便日後重新提煉；本 vault 選擇消化完直接刪 Inbox。只要 Card 自足、不靠原文也讀得懂，來源連結就只是回查用。連結死了也沒關係。

這點對程式筆記特別重要。API、framework、工具限制、best practice 都會隨時間迭代；過期 clipping 會增加判斷成本，甚至把舊資訊偽裝成仍可參考的知識。因此這裡不追求保存完整原始資料，而是保留當下已內化、之後可更新的理解版本。

## 工作流

Vault 分三層成熟度：

| 層級 | 角色 | 生命週期 |
|---|---|---|
| `Inbox/` | 外部原始資料暫存 | 消化完刪除 |
| `Cards/` | 未歸屬的完整概念 Card | 累積同主題後批次升 Topic |
| `Topics/<主題>/` | 已歸檔的主題知識 | 長期維護，持續覆寫 |

這三層不是單純分類資料夾，而是成熟度流動：未消化 → 待歸類 → 已歸檔。防爆量靠流動，不靠紀律：Inbox 消化完刪、Cards 成批搬走、Topics 第一層不跨主題聚合。

## 三層流動細節

### Inbox → Cards（消化）

Inbox 有三條清空路徑：

- A. 寫新 Card（放 `Cards/`）：真有新啟發，少數。
- B. 強化既有 Card / Topic 內容：呼應舊想法，多數。
- C. 直接刪除：沒學到新東西或品質差，多數。

三條都以「刪除 Inbox 原篇」作結。Inbox 空 = 無積欠。

路徑 A、B 寫 Card 時，按既有慣例附上來源連結，來源只是回查用，不作為證據本體。

多主題例外：若 Inbox 筆記同時涵蓋多個主題，而本次只內化其中一個切角，可以從原筆記移除已內化段落、保留剩餘段落，並在 frontmatter 加 `extracted_to: "[[<MOC 名>]]"` 指回 MOC。半消化筆記仍是 Inbox 的待消化狀態，鼓勵下次同主題整理時再處理剩餘內容。

### Cards → Topics（歸檔）

Card 是完整概念：獨立可讀，不需搭配其他筆記或原文就能理解，不是零碎斷句。

批次歸檔有兩種觸發：

- 同主題累積：多張同主題 Cards 一起搬。
- Card 裂變：單張 Card 長大後拆成多張，同時搬。

歸檔動作（須先經使用者拍板，見 [`CLAUDE.md`](CLAUDE.md) 升級限制）：

1. 找到或建立 `Topics/<主題>/` 資料夾，並確保有 `index.md` 作為主題入口頁。
2. 一次 `git mv` 整組 Cards 到 `Topics/<主題>/`，內容不動。
3. 在 `index.md` 補上 wikilink 清單。

跨主題靠 `tags` 串連。`Topics/` 第一層不做跨主題巢套；不要建「AI-工具/Claude-Code/」這種群組。單一主題內 Cards 過多時，才考慮在 `Topics/<主題>/` 底下再分子資料夾。

升 Topic 前的品質門檻與退回 Cards 的反指標看 [`topics-review.md`](topics-review.md)。已升 Topic 重看時若命中反指標，可退回 Cards，但仍需使用者拍板。

主要操作由 skills 承載：

| 操作 | 做什麼 | 承載 |
|---|---|---|
| 擷取 / 消化 | 外部原始資料進 Inbox，內化進 Cards 或 Topics 後刪原篇 | `ob`、`vault-youtube-sync`、`vault-updates-daily` |
| 查詢 / 回存 | 問 vault；若答案有複利價值，只提議回存，等你拍板 | `ob`、`CLAUDE.md` 查詢回存規則 |
| 主題整合 | 多篇相關筆記整合成 MOC 或 Topic 入口 | `vault-distill` |
| 結構健檢 | 掃孤立頁、死連結、tag 漂移、缺欄位等結構問題 | `vault-lint` |

## 人 / AI 分工

- **你**：蒐集來源、提出問題、判斷價值、拍板是否回存、刪除或升 Topic。
- **AI**：消化、摘要、整理、交叉引用、歸檔、結構健檢。

AI 可以承擔重複、瑣碎、容易被延後的維護工作；但不自主決定知識是否值得留下。回存、刪除、升 Topic 都要你拍板。

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
| Cards → Topics 升級門檻與反指標 | [`topics-review.md`](topics-review.md) |
| 全域導航與 tag 查詢地圖 | [`master-index.md`](master-index.md) |
| 專案結構、安裝方式、skill 清單 | [`README.md`](README.md) |
| 通用 LLM Wiki 概念 | [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) |
