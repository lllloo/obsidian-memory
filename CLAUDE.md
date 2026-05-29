# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

# Obsidian Memory Vault — Agent 操作規格

本檔只放 agent 必須遵守的執行規則。Vault 心智模型看 [`vault-model.md`](vault-model.md)；Cards -> Topics 升級門檻看 [`topics-review.md`](topics-review.md)；導航與 tag 查詢看 [`vault-map.md`](vault-map.md)。

## 基本原則

- Vault 是「吸收型卡片盒」：筆記寫成已內化的理解版本，不保存整篇原料。
- 「已內化」以使用者本人讀過／看過為準。AI 代為摘要、但使用者尚未親自消化的外部原料，**不主動升 Card**——摘要留 Inbox 當「待讀佇列」，待本人消化再內化。已誤升成 Card 的，**搬回 Inbox**，不用 `draft` 等標記在 Cards 充當待讀狀態。
- 不主動擴大 scope：不自動回存筆記、不自動結構搬移或升 Topic。
- `Inbox/Clippings/` 例外：agent **不主動掃描、消化或刪除** Clippings 內容。使用者剪藏的網頁原料留作參考，只在使用者明確指名（如「消化 Clippings/X.md」、「處理 Clippings」）才處理。「整理 Inbox」這類掃描動作預設**跳過 Clippings**。
- 刪除筆記（Inbox／Cards／Topics）需使用者拍板；唯 skill（如 `ob`、`vault-youtube-sync`）流程內定義的消化刪原篇依各 skill 流程，不在此限。
- 執行 `git push` 或任何遠端推送前，必須先取得使用者明確同意。

## CWD 契約

所有 repo-local vault skills 都要求 cwd 是 vault root，也就是本 repo 根目錄，底下直接有 `vault-map.md`。

```bash
[ -f "vault-map.md" ] || { echo "ERROR: cwd 不在 vault root"; exit 1; }
```

從其他專案呼叫本 repo skill 前，先 `cd C:\code\obsidian-memory`。

## 寫入前 Checklist

任何 agent 在寫入 `.md` 前都必須自檢。Vault 內容會公開發佈，敏感資料零容忍。

### 1. 敏感資料

正文與 frontmatter 不得包含：

- Token / Key：`sk-`、`sk-ant-`、`ghp_`、`gho_`、`AKIA`、`AIza`、`xox[baprs]-`、`eyJ`（JWT）
- Private key header：`-----BEGIN ... PRIVATE KEY-----`
- 自然語言密碼：「密碼是 ...」、「password: ...」後接明文
- 客戶 / 公司內部資訊、個資：身分證、私人電話、地址、內部 IP / 網址

命中時依情境處置：

- **本次寫入命中**：剔除敏感片段後再寫入；整篇無法拆解則中止寫入並告知使用者。
- **既有筆記命中**：停手、回報檔案與行號給使用者，待拍板後才移除——不自動改既有筆記（與基本原則「不主動擴大 scope」一致）。

### 2. Tag 沿用既有

寫入前先查現有 tags，優先沿用，避免同義異寫。

```bash
rg -A5 '^tags:' . -g '*.md'
```

真無合適才建新 tag；新 tag 使用小寫、`-` 連接。

### 3. 命名

- 檔名不含空格；空格一律改為 `-`。
- Wikilink 必須對應實際存在的檔案名稱。
- `title:` 用主題名，不加日期前綴。

### 4. Frontmatter schema

`.md` frontmatter 欄位採白名單與固定順序；新增欄位前先確認既有筆記是否已使用。

欄位語意與固定順序（即下表列序）：

| 欄位 | 用途 / 何時用 | 值格式 |
|---|---|---|
| `title` | 主題名，可含空格與中文；不加日期前綴（SKILL 範本可例外，如 `vault-updates-daily` 日報 `"<YYYY-MM-DD> Daily Updates"`） | 字串（檔名為其無空格、`-` 連接版） |
| `description` | 一句話自我介紹，給 Obsidian Bases、Quartz SEO、AI 查詢用。**適用**：Topics `index.md`、Inbox/YouTube 影片摘要、Inbox/Clippings 網頁剪藏（Web Clipper 自動帶 `{{description}}`）；其餘筆記不加（書籤型第一段已是定位段，判斷型靠第一段帶頭） | 字串，30–80 字；不重複 title，避免「這篇 / 本文」自我指涉 |
| `created` | 進 vault 日期 | `YYYY-MM-DD` |
| `updated` | 最後修改日期 | `YYYY-MM-DD` |
| `source` | 來源 URL（網頁／影片連結；YouTube `index` 為頻道 URL）；回查用，非證據本體 | URL |
| `published` | 原始內容發佈／上傳日，與 `created`（進 vault 日）區分；不明可留空 | `YYYY-MM-DD` 或空 |
| `parent` | Obsidian 圖譜用 wikilink，讓筆記出現在圖譜 | `"[[01.index]]"` |
| `last_sync_id` | youtube-sync 增量同步 checkpoint，僅存於頻道 `01.index.md` | YouTube videoId |
| `draft` | `true` = 不發佈到 Quartz 公開站（未定稿／含敏感脈絡，或 youtube transcript 抓取失敗的占位待重抓） | `true`（省略 = 已發佈） |
| `extracted_to` | 多主題 Inbox 筆記內化某切角後指回整合頁（半消化狀態） | `"[[<整合頁名>]]"` |
| `tags` | 主題分類 + 必要的功能性 tag | YAML list |

一般筆記需有 `title`、`created`、`updated`、`tags`。根 `index.md`（Quartz 公開首頁）可不加 `tags`。`tags` 一律用 YAML list，不用 inline array 或字串。下列三類需有 `description`：Topics `index.md`、Inbox/Clippings 網頁剪藏（Web Clipper 自動帶）、Inbox/YouTube 影片摘要（vault-youtube-sync skill 範本帶）。

Topics 的 `index.md` 是主題入口；Cards/筆記也可以是整合頁。不要用額外 tag 標記這類結構角色，辨識時依路徑（如 `Topics/*/index.md`）與內容判斷。

修改 `.md` 內容時盡量同步 `updated` 為今日日期（`YYYY-MM-DD`），但不為此中斷流程。

## Wikilink 與 Obsidian 語法

- 寫入 wikilink 前確認目標檔案存在；不存在就改用外部 URL，不留死連結。
- `.base` wikilink 必須加副檔名：`[[02.影片清單.base]]`。
- `.base` embed 同理：`![[02.影片清單.base]]`。
- `.base` 內容不會在圖譜產生連結；要讓筆記出現在圖譜中，需在筆記 frontmatter 加：

  ```yaml
  parent: "[[01.index]]"
  ```

- `#` 開頭的內容會被 Obsidian 解讀為 tag；hex 色碼必須用反引號包住，例如 `` `#57F287` ``。
- 建立新 Card 時，除了 Card 內的出站連結，順手在 1–2 個最相關的既有筆記補一條入站 wikilink——避免新 Card 一建立就是孤立頁（事後才靠 lint 補連結）。
- 清空或大幅改動某資料夾後，回查 `vault-map.md` 是否有指向該路徑的條目（資料夾索引、tag 查詢指南），避免留下死指向。

## 查詢規則

查詢方式看 `vault-map.md`（資料夾索引、tag 查詢指南）。

若查詢或討論**整合了 ≥2 篇既有筆記、且產生原文沒有的綜合結論**，可提議「要不要回存成 Card?」，不得自動寫入。未達此門檻不主動提。

## 多筆記整合 / 整合頁

使用者要求「整合筆記」、「合併同主題筆記」、「建立整合頁」或類似任務時，由當前 agent 直接依本檔規則主導，不另走獨立 skill。

整合流程：

1. 先讀 `vault-map.md`，再用 tag、路徑、正文關鍵字搜尋 `Inbox/`、`Cards/`、`Topics/`。
2. 列出候選筆記與共同主題；排除既有整合頁（例如 `Topics/*/index.md` 或內容明確為整合頁），避免整合頁套整合頁。
3. 只有整合了 ≥2 篇既有筆記、且產生原文沒有的綜合結論時，才建立或改寫整合頁。
4. 整合頁預設寫入 `Cards/<主題>.md`；不自動升入 `Topics/`，升 Topic 仍依 `topics-review.md` 等使用者拍板。
5. 整合頁 frontmatter 必須含主題 tag，不新增結構角色 tag，並遵守本檔寫入前 Checklist。
6. 原筆記處置只提出建議，不自動刪除或搬移。可選處置為：保留並用 wikilink 連回、整篇刪除、部分抽取並加 `extracted_to`。

整合頁內容應聚焦長期有效的概念、判斷框架與筆記間的共識 / 差異；避免把版本清單、工具流水帳或可由官方文件快速取代的細節塞進主體。精確版本號的處理（淡化易變版本、保留行為約束）見 [`vault-model.md`](vault-model.md) 的「版本抗性」，此原則適用所有 Topics / Cards，不限整合頁。

## 可用 Skills

本 repo 在 `.agents/skills/` 提供 repo-local skills；`.claude/skills` 是 symlink。

| Skill | 用途 |
|---|---|
| `ob` | 筆記建立 / 查詢分派入口 |
| `vault-youtube-sync` | YouTube 影片摘要同步至 Inbox |
| `vault-updates-daily` | 日常更新彙整 |
| `vault-lint` | Vault 結構健檢 |

優先使用 skill，不新增平行流程——現有 skill 能覆蓋的操作一律走 skill，只有 skill 無對應流程時才手動直接操作（即下一段情境）。新增或修改 skill 時，盡量遵循 Agent Skills 開放標準，讓內容可跨工具移植。

未透過 skill 直接操作 Inbox 或 Cards 時，先讀 [`vault-model.md`](vault-model.md) 的「三層流動細節」確認流程（三條清空路徑、`extracted_to` 例外、git mv 步驟）。

## YouTube 筆記

所有 YouTube 影片筆記正文一律以繁體中文撰寫。

- 技術名詞、品牌名、工具名保留英文。
- 若 defuddle 取得英文 transcript，需翻譯整理為繁體中文後再寫入筆記。

## Cards -> Topics 升級限制

升 Topic 不由 agent 自主執行。流程：

1. 列出候選 Cards。
2. 對照 `topics-review.md` 的 5 條保留條件與反指標。
3. 給出傾向與理由。
4. 等使用者拍板後才執行 `git mv`。

改寫優於直接決定；改寫後必須重跑審核再決定。

## 成長觀察

討論 vault 內容時，若**明確看到具體的結構缺口**（某概念散在多頁卻沒專屬 Card、兩篇主題相關卻沒互連、某主題有明顯資料空缺），可順手點出。

只提議，不自動執行；不要背景掃描整個 vault 找成長面問題。結構問題交給 `vault-lint`。

成長觀察與查詢規則的「回存提議」同屬討論衍生提議，**單次回應至多提一項**，避免變成噪音。
