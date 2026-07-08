# CLAUDE.md

本檔是這個 vault 的 **schema**：告訴 agent 這套 Karpathy LLM Wiki 怎麼維護。系統全貌與心智模型見 [`SYSTEM-DESIGN.md`](SYSTEM-DESIGN.md)，全局導航與 tag 查詢見 [`vault-map.md`](vault-map.md)。

> 這個 vault 是 Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 實作：agent 漸進維護一套互聯的 markdown wiki，夾在你與原始資料之間。不是 RAG——知識被編譯一次後持續維護，是複利資產。

## 三層架構

| 層 | 角色 | agent 權限 |
|---|---|---|
| `raw/` | 不可變原始來源（你精選的原料，事實來源） | **只讀不改** |
| `wiki/` | agent 完全掌管的活知識庫：摘要、實體、概念、比較、綜合 | **全權**：自由建頁、改頁、刪頁、交叉引用、維護 index |
| schema | 本檔 + `SYSTEM-DESIGN.md` + `vault-map.md`（規範 agent 行為） | 依規則維護 |

**`Cards/` 與 `Topics/` 不屬於本系統。** 它們是使用者的私人資料夾，同時是 Quartz **唯一對外公開發佈**的層。agent 一律**不讀、不寫、不掃描、不維護、不索引** Cards/Topics——Ingest、Query、Lint 全部跳過它們。使用者自行從 wiki 手動撿選、複製想公開的內容進去；那是使用者的動作，不是系統的一環。

## 唯一守門：git push

agent 自主維護 wiki（含改頁、刪頁），**不需逐步拍板**——這正是 Karpathy「維護成本趨近於零」的重點。唯一硬規則：

> **執行 `git push` 或任何遠端推送前，必須先取得使用者明確同意。**

`push` 會把 `raw/` 與 `wiki/`（皆不經 Quartz 發佈，但仍存在於 GitHub repo）一併推上遠端，該次 diff review 由使用者把關。除此之外沒有其他 agent 守門：不做 Cards/Topics 治理、不做品質 gate、不做敏感資料自檢 gate、不設「不自動刪」限制。

## CWD 契約

所有 repo-local vault skills 都要求 cwd 是 vault root，也就是本 repo 根目錄，底下直接有 `vault-map.md`。

驗證方式用 harness-native `Read vault-map.md`（不經 shell、跨平台）——讀得到即在 vault root，讀不到就停止並請使用者 cd 過來。不要用 `[ -f vault-map.md ]` 之類 shell gate（在 Windows 預設 PowerShell 會翻車）。

從其他專案呼叫本 repo skill 前，先 cd 到 vault root：`~/code/obsidian-memory`（三平台一致；cmd.exe 不認 `~`，改用 `%USERPROFILE%\code\obsidian-memory`）。

## 三個動作：Ingest / Query / Lint

wiki 的維護就是這三個動作，全部只在 `raw/` + `wiki/` 上進行，不碰 Cards/Topics。

### Ingest（擷取）

新來源進 `raw/` → agent 讀 → **與使用者討論重點** → 在 `wiki/` 寫入或更新頁面：

1. 寫一頁摘要（或更新既有摘要）。
2. 更新相關的實體頁 / 概念頁：整合新資訊、改寫舊摘要、**新資料與舊主張衝突時就地標記矛盾**。
3. 更新 `wiki/01.index.md`（新頁登錄、一行摘要）。
4. 補交叉引用：新頁至少連 1–2 個相關既有頁，避免孤立。

單一來源可牽動多頁。agent 自主寫，不逐頁拍板；使用者在旁讀、隨時導引重點即可。可一次一源慢慢做，也可批次 ingest。

### Query（查詢）

向 wiki 提問 → agent 先讀 `wiki/01.index.md` 找相關頁 → 讀頁 → **附引用**綜合答案。

好答案（比較表、綜合分析、發現的關聯）**可回存成新 wiki 頁**，讓探索跟來源一樣複利累積，不要消失在對話裡。回存只在 wiki 內，不寫進 Cards/Topics。

### Lint（健檢）

定期掃 wiki（+ raw 索引）：矛盾、被新來源取代的過時主張、孤立頁、被提到卻沒專屬頁的概念、缺交叉引用、可用查證補的資料空缺。產出修補與新探究建議。由 `vault-lint` 承載，只掃 raw/wiki，不碰 Cards/Topics。

## wiki 頁面與索引

- **頁面類型**：摘要頁、實體頁（人/工具/組織）、概念頁、比較頁、綜合頁。
- **`wiki/01.index.md`**：內容目錄——每頁一行摘要 + wikilink，按類別分組，每次 ingest 更新。查詢時先讀它再鑽細節（省 token，也避免重複建頁）。
- **交叉引用是核心紀律**：wiki 的價值在互聯成網，不在單頁品質。

## 寫入慣例（只約束 `raw/` + `wiki/`）

這些是「怎麼寫」的品質慣例，**不是守門煞車**（不需拍板、不擋流程）。只適用 agent 會寫的 raw/wiki，碰不到使用者私有的 Cards/Topics。

### 1. 語言

正文一律繁體中文，技術名詞／品牌名／工具名保留英文。

### 2. Tag 沿用既有

寫入前先用 Grep 工具搜 `^tags:`（glob `*.md`，加 5 行上下文）查現有 tags，優先沿用，避免同義異寫。真無合適才建新 tag；新 tag 使用小寫、`-` 連接。

### 3. 命名

- 檔名不含空格；空格一律改為 `-`。
- Wikilink 必須對應實際存在的檔案名稱。
- `title:` 用主題名，不加日期前綴。

### 4. Frontmatter schema

`.md` frontmatter 欄位採白名單與固定順序；新增欄位前先確認既有筆記是否已使用。

| 欄位 | 用途 / 何時用 | 值格式 |
|---|---|---|
| `title` | 主題名，可含空格與中文；不加日期前綴（SKILL 範本可例外，如 `vault-updates-daily` 日報 `"<YYYY-MM-DD> Daily Updates"`） | 字串（檔名為其無空格、`-` 連接版） |
| `description` | 一句話自我介紹，給 Obsidian Bases、AI 查詢用。**適用**：wiki 頁、raw/YouTube 影片摘要、raw/Clippings 網頁剪藏；其餘筆記可省 | 字串，30–80 字；不重複 title，避免「這篇／本文」自我指涉 |
| `created` | 進 vault 日期 | `YYYY-MM-DD` |
| `updated` | 最後修改日期 | `YYYY-MM-DD` |
| `source` | 來源 URL（網頁／影片連結；YouTube `index` 為頻道 URL）；回查用，非證據本體 | URL |
| `published` | 原始內容發佈／上傳日，與 `created`（進 vault 日）區分；不明可留空 | `YYYY-MM-DD` 或空 |
| `parent` | Obsidian 圖譜用 wikilink，讓筆記出現在圖譜 | `"[[01.index]]"` |
| `last_sync_id` | youtube-sync 增量同步 checkpoint，僅存於頻道 `01.index.md` | YouTube videoId |
| `draft` | youtube-sync transcript 抓取失敗的占位待重抓標記；正常筆記不用 | `true`（省略 = 正常） |
| `tags` | 主題分類 + 必要的功能性 tag | YAML list |

一般筆記需有 `title`、`created`、`updated`、`tags`。`tags` 一律用 YAML list，不用 inline array 或字串。Clippings 的 `description` 為 Web Clipper 自動帶入的外站文案，豁免 30–80 字與風格要求，agent 不回頭修。

修改 `.md` 內容時盡量同步 `updated` 為今日日期（`YYYY-MM-DD`），但不為此中斷流程。

### 5. Wikilink 與 Obsidian 語法

- 寫入 wikilink 前確認目標檔案存在；不存在就改用外部 URL，不留死連結。
- `.base` wikilink 必須加副檔名：`[[02.影片清單.base]]`；embed 同理 `![[02.影片清單.base]]`。
- `.base` 內容不會在圖譜產生連結；要讓筆記出現在圖譜中，需在筆記 frontmatter 加 `parent: "[[01.index]]"`。
- `#` 開頭的內容會被 Obsidian 解讀為 tag；hex 色碼必須用反引號包住，例如 `` `#57F287` ``。
- 來源連結放置：單一主來源放 frontmatter `source`；正文需就地引用多個外部連結時用 inline 超連結（`[文字](URL)`）；自動化日報沿用既有的標題側連結格式。

## 可用 Skills

本 repo 在 `.agents/skills/` 提供 repo-local skills；`.claude/skills` 是 symlink。

| Skill | 用途 |
|---|---|
| `ob-write` | 寫入筆記到 raw/wiki（global，任何專案可呼叫；cwd=vault root 不限工具，跨專案走定位鏈直寫本機 clone） |
| `ob-read` | wiki 查詢（global，任何專案可呼叫；cwd=vault root 本地直搜，跨專案定位鏈定位後唯讀搜尋） |
| `vault-youtube-sync` | YouTube 影片摘要同步至 `raw/` |
| `vault-updates-daily` | 日常更新彙整至 `raw/Updates/` |
| `vault-wiki-build` | Ingest：讀散落 raw → 綜合維護 wiki 頁 → 更新 index |
| `vault-lint` | wiki 結構健檢（掃 raw/wiki，不碰 Cards/Topics） |

優先使用 skill，不新增平行流程。新增或修改 skill 時，盡量遵循 [Agent Skills](https://agentskills.io) 開放標準，讓內容可跨工具移植。

### 新增 / 修改 skill 的本 repo 約束

- subagent 一律 `Agent` + `subagent_type: "general-purpose"`，prompt = `references/*.md` 全文 + 本次需求（不要叫 subagent 自己 Read）
- 工具限制等規則寫在 references 正文，自包含、不引用命名 agent
- 補 fallback 條款：「無 Agent 工具時主 agent 直接 Read references 跑同一流程」
- SKILL.md 主流程不寫憲法級規則（唯一守門 git push、通用 wikilink/frontmatter 慣例等）——這些在本檔 `CLAUDE.md`，不重述也不寫「見 CLAUDE.md」指回
- 但 subagent 經 `references/*.md` 執行時要遵守的寫作規則（繁中、時間抗性等）必須在該 prompt 內可達（inline 或叫它先讀 AGENTS.md），不能只靠 AGENTS.md

## 時間抗性

Cards/Topics 交給使用者，但 agent 寫的 wiki 頁仍要防過期：描述行為怎麼變、別把精確版本號釘死進正文，確切切換版本指向官方 changelog 由讀者回查；版本號只在它是行為關鍵分水嶺、讀者必須知道時才留並標來源。與版本耦合度低的行為約束（如某功能需特定 model / API）仍要留。程式類 raw 會隨工具迭代而過期，但留著仍有回查價值——真正要防過期的是 wiki 正文。
