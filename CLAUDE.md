# CLAUDE.md

本檔是這個 vault 的 **schema**：告訴 agent 這套 Karpathy LLM Wiki 怎麼維護。系統全貌與心智模型見 [`SYSTEM-DESIGN.md`](schema/SYSTEM-DESIGN.md)，全局導航與 tag 查詢見 [`vault-map.md`](schema/vault-map.md)。

> 這個 vault 是 Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 實作：agent 漸進維護一套互聯的 markdown wiki，夾在你與原始資料之間。不是 RAG——知識被編譯一次後持續維護，是複利資產。

@schema/MEMORY.md

## 三層架構

| 層 | 角色 | agent 權限 |
|---|---|---|
| `raw/` | 原始來源（你精選的原料，事實來源），write-once | **可新增、不可修改**：可抓外部來源轉 markdown 落地新檔，寫入後即凍結，不回頭改任何既有 raw 檔 |
| `wiki/` | agent 完全掌管的活知識庫：摘要、實體、概念、比較、綜合 | **全權**：自由建頁、改頁、刪頁、交叉引用、維護 index |
| schema | 本檔（root）+ `schema/SYSTEM-DESIGN.md` + `schema/vault-map.md` + `schema/MEMORY.md` + `schema/BACKLOG.md`（規範 agent 行為 + 跨 session 操作記憶） | 依規則維護 |

`schema/BACKLOG.md` 是 `vault-lint` 的健檢待處理清單:agent **每輪讀回來約束自身行為**的操作狀態(去重、跳過已婉拒、判斷退場),與 `MEMORY.md` 同層,不是給人瀏覽的 feed 產物。**語意項只報告**,修補由使用者另行指示;使用者退回的修法記入「已婉拒」,agent 之後不再重提。寫入該檔時頁面引用一律用反引號、不得用 wikilink(`schema/` 在死連結掃描範圍內)。

**`cards/` 與 `topics/` 不屬於本系統。** 它們是使用者的私人資料夾，同時是 Quartz **唯一對外公開發佈**的層。agent 一律**不讀、不寫、不掃描、不維護、不索引** cards/topics——Ingest、Query、Lint 全部跳過它們。使用者自行從 wiki 手動撿選、複製想公開的內容進去；那是使用者的動作，不是系統的一環。

**`feeds/` 也不屬於三層系統。** 它集中存放只供使用者瀏覽的自動產物；除各自的產出 skill 外，agent 一律不讀、不寫、不掃描、不索引。`feeds/` 不參與 Ingest／Query／Lint，不得作為 `raw/` 或 `wiki/` 的來源；Quartz 只應發佈 cards/topics，`feeds/**` 不得公開。

- `feeds/youtube/`：`vault-youtube-sync` 的自動同步筆記。完整影片筆記寫入後凍結；draft 占位可由 skill 覆寫重試，頻道 index、Base 與 checkpoint 可由 skill 維護。
- `feeds/updates/`：`vault-updates-daily` 的消費性日報與來源設定。
（`vault-lint` 不再產 feeds 產物：健檢的待處理清單改放 `schema/BACKLOG.md`，見下方 schema 一節。）

## 唯一守門：git push

agent 自主維護 wiki（含改頁、刪頁），**不需逐步拍板**——這正是 Karpathy「維護成本趨近於零」的重點。唯一硬規則：

> **執行 `git push` 或任何遠端推送前，必須先取得使用者明確同意。**

`push` 會把 `raw/`、`wiki/` 與 `feeds/`（皆不應經 Quartz 發佈，但仍存在於 GitHub repo）一併推上遠端，該次 diff review 由使用者把關。除此之外沒有其他**硬**守門：不做 cards/topics 治理、不做品質 gate、不做敏感資料自檢 gate、不設「不自動刪」限制。（另有一個流程級確認點：單次 ingest 觸及超過 15 頁先問，見 Ingest 一節——那是確認節奏，不是守門。）

## CWD 契約

所有 repo-local vault skills 都要求 cwd 是 vault root，也就是本 repo 根目錄。哨兵檔用 `schema/vault-map.md`——幾乎每個專案根目錄都有 `CLAUDE.md`，拿它當 gate 對「跑錯 repo」無效；`schema/vault-map.md` 這個路徑只存在於本 vault。

驗證方式用 harness-native `Read schema/vault-map.md`（不經 shell、跨平台）——讀得到即在 vault root，讀不到就停止並請使用者 cd 過來。不要用 shell 的檔案存在檢查（在 Windows 預設 PowerShell 會翻車）。

從其他專案呼叫本 repo skill 前，先 cd 到 vault root：`~/code/obsidian-memory`（三平台一致；cmd.exe 不認 `~`，改用 `%USERPROFILE%\code\obsidian-memory`）。

## 三個動作：Ingest / Query / Lint

wiki 的維護就是這三個動作，只在 `raw/` + `wiki/` 上進行；不碰 cards/topics 或 feeds。

### Ingest（擷取）

新來源進 `raw/` → agent 讀 → 直接在 `wiki/` 寫入或更新頁面，**不需要先開一輪討論才動筆**。

進料管道（raw 為 write-once，落地後不改）：

- **使用者貼 URL**：先 Grep `raw/` 的 `source:` 查同 URL 是否已落地。**已存在**：不重複建檔，直接更新對應 wiki 頁（重讀來源、與現有 wiki 內容對照，實質變了就在頁面就地更新——來源過時靠此處人眼＋lint 語意層兜底，不做雜湊比對）。**未存在**才抓內容（優先 defuddle）轉 markdown，按 frontmatter 慣例（含 `source`、`published`）存 `raw/fetched/`，再往下 ingest。抓到的內容明顯殘缺（登入牆、付費牆、重 JS 頁）時**不落地 raw**——write-once 塞進殘件即凍結——改請使用者用 Web Clipper 剪藏。
- **Web Clipper 剪藏**、**使用者手動放檔**：存入 `raw/clippings/`。
- **YouTube 自動同步**：`vault-youtube-sync` 只寫入 `feeds/youtube/`，不進 raw 或 wiki。

流程：

1. 寫一頁摘要（或更新既有摘要）。
2. 更新相關的實體頁 / 概念頁：整合新資訊、改寫舊摘要、**新資料與舊主張衝突時就地標記矛盾**。
3. 更新 `wiki/01.index.md`（新頁登錄、一行摘要）；**順手維護頂部「最近更新」區塊：加一筆本輪動到的頁（頁 wikilink＋一句），滾動保留最近 5 筆、超出刪最舊**——滾出的舊筆不另存、也不擴充筆數，要回溯更久之前的變更一律走 `git log`。這是給消費端的輕量近期入口（有界、不當完整歷史）；完整時序真相在 git。不建獨立熱檔（取捨見 [`wiki/LLM-Wiki-生態實作比較.md`](wiki/LLM-Wiki-生態實作比較.md)）。
4. 補交叉引用：新頁至少連 1–2 個相關既有頁，避免孤立。
5. **收尾輕量 lint（只檢當輪動到的頁，不掃全庫）**：交叉引用是否雙向、有無與既有主張矛盾、有無因新頁產生的孤立頁。當輪頁本就在 context 裡，成本趨近於零；這是擋「漂移」（頁面 ingest 時未同步交叉引用而無聲過時）的主要防線，全庫成長掃描仍不做。

單一來源可牽動多頁（典型 10–15 頁，屬正常，見 [`SYSTEM-DESIGN.md`](schema/SYSTEM-DESIGN.md)）。agent 自主寫，不逐頁拍板；使用者在旁讀、隨時導引重點即可。可一次一源慢慢做，也可批次 ingest。**例外閘門：單次 ingest 預計觸及（建/改/刪）超過 15 頁時，先列頁面清單問過使用者再動筆**——閘門刻意訂在典型範圍之上，只攔真正異常的大面積改動；15 頁以內照常全自主。

### Query（查詢）

向 wiki 提問 → agent 先讀 `wiki/01.index.md` 找相關頁 → 讀頁 → **附引用**綜合答案。Query 一律不掃 feeds。

好答案（比較表、綜合分析、發現的關聯）**可回存成新 wiki 頁**，讓探索跟來源一樣複利累積，不要消失在對話裡。回存只在 wiki 內，不寫進 cards/topics。

### Lint（健檢）

定期掃 wiki（+ raw 索引）：矛盾、被新來源取代的過時主張、孤立頁、被提到卻沒專屬頁的概念、缺交叉引用、可用查證補的資料空缺。產出修補與新探究建議。只掃 raw/wiki/schema，不碰 feeds/cards/topics。掃描由 `vault-lint` skill 承載（findings 去重後維護在 `schema/BACKLOG.md`，解決即移除，不產快照報告；可手動跑亦可掛排程，行為一致且不碰 git）：**機械可修項自動修、語意項只報告**（依據：死連結是 LLM wiki 實證的頭號結構錯誤，見 [`LLM-Wiki-生態實作比較`](wiki/LLM-Wiki-生態實作比較.md)），語意修補在使用者點頭後由 agent 執行；使用者退回的修法記入「已婉拒」不再重提。

## wiki 頁面與索引

- **頁面類型**：摘要頁、實體頁（人/工具/組織）、概念頁、比較頁、綜合頁。
- **`wiki/01.index.md`**：內容目錄——每頁一行摘要 + wikilink，按類別分組，每次 ingest 更新。查詢時先讀它再鑽細節（省 token，也避免重複建頁）。
- **交叉引用是核心紀律**：wiki 的價值在互聯成網，不在單頁品質。

## 寫入慣例（`raw/` + `wiki/`，以及各 skill 指定的 feeds 筆記）

這些是「怎麼寫」的品質慣例，**不是守門煞車**（不需拍板、不擋流程）。適用 agent 會寫的 raw/wiki；feeds 筆記只由各自 skill 依自包含規則維護。碰不到使用者私有的 cards/topics。

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
| `description` | 一句話自我介紹，給 Obsidian Bases、AI 查詢用。**適用**：wiki 頁、feeds/youtube 影片摘要、raw 網頁剪藏；其餘筆記可省 | 字串，30–80 字；不重複 title，避免「這篇／本文」自我指涉 |
| `created` | 進 vault 日期 | `YYYY-MM-DD` |
| `updated` | 最後修改日期 | `YYYY-MM-DD` |
| `source` | 來源 URL（網頁／影片連結；YouTube `index` 為頻道 URL）；回查用，非證據本體 | URL |
| `published` | 原始內容發佈／上傳日，與 `created`（進 vault 日）區分；不明可留空 | `YYYY-MM-DD` 或空 |
| `parent` | Obsidian 圖譜用 wikilink，讓筆記出現在圖譜 | `"[[01.index]]"`；vault 內多個資料夾各有同名 `01.index.md`，重名歧義時用路徑限定（如 wiki 頁 `"[[wiki/01.index]]"`） |
| `last_sync_id` | youtube-sync 增量同步 checkpoint，僅存於頻道 `01.index.md` | YouTube videoId |
| `draft` | youtube-sync transcript 抓取失敗的占位待重抓標記；正常筆記不用 | `true`（省略 = 正常） |
| `tags` | 主題分類 + 必要的功能性 tag | YAML list |

一般筆記需有 `title`、`created`、`updated`、`tags`。`tags` 一律用 YAML list，不用 inline array 或字串。Clippings 中 **Web Clipper 產出**的 `description` 為自動帶入的外站文案，豁免 30–80 字與風格要求，agent 不回頭修；**agent 貼 URL 落地**的 `fetched/` 來源則照正常 `description` 規則寫。

修改 `.md` 內容時盡量同步 `updated` 為今日日期（`YYYY-MM-DD`），但不為此中斷流程。

### 5. Wikilink 與 Obsidian 語法

- 寫入 wikilink 前確認目標檔案存在；不存在就改用外部 URL，不留死連結。
- 在正文使用 wikilink 時，盡量以相鄰文字說明關係（例如支持、反例、延伸或應用），不只堆疊「關聯」連結；純目錄／索引條目除外。
- `.base` wikilink 必須加副檔名：`[[02.影片清單.base]]`；embed 同理 `![[02.影片清單.base]]`。
- `.base` 內容不會在圖譜產生連結；要讓筆記出現在圖譜中，需在筆記 frontmatter 加 `parent: "[[01.index]]"`。
- `#` 開頭的內容會被 Obsidian 解讀為 tag；hex 色碼必須用反引號包住，例如 `` `#57F287` ``。
- 來源連結放置：單一主來源放 frontmatter `source`；正文需就地引用多個外部連結時用 inline 超連結（`[文字](URL)`）；自動化日報沿用既有的標題側連結格式。

### 6. 查證產出的強度標註

deep-research 或其他對抗式查證的結果回存 wiki 時：每條主張就地標**證據強度與限制**（如「單一 preprint、未同儕審查」「單一作者經驗值、非實證」）；被查證**否決**的主張明列並標「勿引用」，不無聲丟棄；拍板結果附日期記進頁面。防查證結論被後續引用時失去強度資訊。

## 可用 Skills

本 repo 在 `.agents/skills/` 提供 repo-local skills；`.claude/skills` 是 symlink。

| Skill | 用途 |
|---|---|
| `vault-youtube-sync` | YouTube 影片摘要同步至 `feeds/youtube/` |
| `vault-updates-daily` | 日常更新彙整至 `feeds/updates/` |
| `vault-lint` | wiki+raw 健檢，findings 維護於 `schema/BACKLOG.md`（機械可修項自動修、語意項只報告）；手動／排程共用同一流程，本身不執行 git 動作 |

優先使用 skill，不新增平行流程。新增或修改 skill 時，盡量遵循 [Agent Skills](https://agentskills.io) 開放標準，讓內容可跨工具移植。

> **已移除的核心 skill**：`ob-write`、`ob-read`、`vault-wiki-build`、舊版 `vault-lint`（含 `ob-write`／`ob-read` 兩個全域 symlink）已於重整時移除。三動作（Ingest／Query／Lint）的模型仍是本 vault 的架構；其中 Lint 的掃描面已按需重建為報告制的 skill（2026-07-10 以 `vault-lint-daily` 之名重建，2026-07-13 改名回 `vault-lint`——它不專為排程而生，手動隨時可跑，「daily」是誤導）。與同名的舊版無血緣，是重寫的另一套。其餘（wiki 綜合、查詢、修補）仍由 agent 手動執行。

### 新增 / 修改 skill 的本 repo 約束

**新增或修改 skill（含既有 skill 的 bug 修正、一致性調整）一律先問過使用者再動手，不比照 wiki 全權自主。** skill 改的是 agent 之後怎麼行動，影響範圍比一頁 wiki 內容大，值得每次都讓你點頭。

**怎麼問**：一次一題、走決策樹逐一解依賴，每題附上推薦答案；事實能查（filesystem／既有 skill／工具）就自己查，只把**決策**擺給使用者；未達共識不動筆。

- subagent 一律 `Agent` + `subagent_type: "general-purpose"`，prompt = `references/*.md` 全文 + 本次需求（不要叫 subagent 自己 Read）
- 工具限制等規則寫在 references 正文，自包含、不引用命名 agent
- 補 fallback 條款：「無 Agent 工具時主 agent 直接 Read references 跑同一流程」
- SKILL.md 主流程不寫憲法級規則（唯一守門 git push、通用 wikilink/frontmatter 慣例等）——這些在本檔 `CLAUDE.md`，不重述也不寫「見 CLAUDE.md」指回
- 但 subagent 經 `references/*.md` 執行時要遵守的寫作規則（繁中、時間抗性等）必須在該 prompt 內可達（inline 或叫它先讀 AGENTS.md），不能只靠 AGENTS.md

## 時間抗性

cards/topics 交給使用者，但 agent 寫的 wiki 頁仍要防過期：描述行為怎麼變、別把精確版本號釘死進正文，確切切換版本指向官方 changelog 由讀者回查；版本號只在它是行為關鍵分水嶺、讀者必須知道時才留並標來源。與版本耦合度低的行為約束（如某功能需特定 model / API）仍要留。程式類 raw 會隨工具迭代而過期，但留著仍有回查價值——真正要防過期的是 wiki 正文。
