# AGENTS.md

本檔是這個 vault 的 **schema**：告訴 agent 這套 Karpathy LLM Wiki 怎麼維護。系統全貌與心智模型見 [`SYSTEM-DESIGN.md`](schema/SYSTEM-DESIGN.md)，全局導航與 tag 查詢見 [`vault-map.md`](schema/vault-map.md)。

> 這個 vault 是 Karpathy 的 [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 實作：agent 漸進維護一套互聯的 markdown wiki，夾在你與原始資料之間。不是 RAG——知識被編譯一次後持續維護，是複利資產。

@schema/MEMORY.md

> **非 Claude Code 工具**（Codex／Cursor／opencode 等）：上面那行 `@` 匯入是 Claude Code 專屬語法，你的工具不會解析。請**手動 Read `schema/MEMORY.md` 與 `schema/BACKLOG.md`**——那是 agent 跨 session 的操作記憶與待處理清單（含使用者已拍板、勿重複提議的項目），漏讀會重提已婉拒的修法。

> **本檔是本 repo 唯一的規範檔，不要建立 `CLAUDE.md`。** Claude Code 自 v2.1.277 起在專案沒有 `CLAUDE.md` 時原生讀取 `AGENTS.md`；反過來，只要本目錄或**任何上層目錄**出現 `CLAUDE.md`／`CLAUDE.local.md`，它就改讀那個、完全不看本檔，等於整份規範無聲失效。`/init` 之類會產生 `CLAUDE.md` 的動作在本 repo 一律不跑（2026-09-21 使用者拍板，原 `AGENTS.md`→`CLAUDE.md` symlink 同時移除）。

## 三層架構

| 層 | 角色 | agent 權限 |
|---|---|---|
| `raw/` | 原始來源（你精選的原料，事實來源），write-once | **可新增、不可修改**：可抓外部來源轉 markdown 落地新檔，寫入後即凍結，不回頭改任何既有 raw 檔 |
| `wiki/` | agent 完全掌管的活知識庫：摘要、實體、概念、比較、綜合 | **全權**：自由建頁、改頁、刪頁、交叉引用、維護 index |
| schema | 本檔（root）+ `schema/SYSTEM-DESIGN.md` + `schema/vault-map.md` + `schema/MEMORY.md` + `schema/BACKLOG.md`（規範 agent 行為 + 跨 session 操作記憶） | 依規則維護 |

`schema/BACKLOG.md` 是 `vault-lint` 的健檢待處理清單:agent **每輪讀回來約束自身行為**的操作狀態(去重、跳過已婉拒、判斷退場),與 `MEMORY.md` 同層,不是給人瀏覽的 feed 產物。lint 發現由 agent 自主修補;**只有真正需要使用者的決策**(需使用者才有的資訊、動 raw write-once、動憲法檔／skill)才進「待你決定」,agent 判定維持現狀／待觸發者則進「Agent 已判」作去重錨點;使用者退回的修法記入「已婉拒」,agent 之後不再重提。寫入該檔時頁面引用一律用反引號、不得用 wikilink(`schema/` 在死連結掃描範圍內)。

**私人筆記已移至 Notion。** 不重建 `topics/`、`cards/`；私人筆記不納入 Ingest／Query／Lint，也不作為 `raw/`／`wiki/` 的來源。外部入口見 `schema/vault-map.md`。

**Notion 操作邊界（2026-10-13 使用者拍板）**：本 repo 的日常維護與技術查詢只使用本地核心知識庫與規範，不自動連線查讀或修改 Notion。文件中的 Notion 連結是供使用者回看的外部入口，不代表 agent 可自行存取。只有使用者重新明確指定 Notion 任務時，才在該任務授權範圍內操作；既往遷移的授權不延伸為後續操作許可。

**本 repo 只供 AI 執行核心流程（2026-10-13 使用者拍板）**：保留 raw／wiki、規範、`vault-lint` 與必要設定；不重建真人入口 `index.md`、架構讀本或 PR 合併 Discord 通知。公開發佈由外部 repo 管理。本地已移除自動產物與 HTML 呈現層；未經使用者重新指定，不重建 `feeds/`、`docs/architecture/`、`vault-youtube-sync`、`vault-watch`、`vault-page`。歷史快照入口集中於 `schema/vault-map.md`。

## 守門：無

agent 自主維護 wiki（含改頁、刪頁），**不需逐步拍板**——這正是 Karpathy「維護成本趨近於零」的重點。**`git push` 亦可自主執行，不需事先徵求同意**（2026-07-20 使用者拍板移除原「push 前須明確同意」守門；此即本 repo 對 push 的常設明確授權，涵蓋 main 分支，優先於全域保護分支規則），review 由使用者事後看 GitHub diff 把關。force push 不在此授權內，仍需明確要求。

沒有任何硬守門：不做 Notion 私人筆記治理、不做品質 gate、不做敏感資料自檢 gate、不設「不自動刪」限制。（另有一個流程級確認點：單次 ingest 觸及超過 15 頁先問，見 Ingest 一節——那是確認節奏，不是守門。）

## CWD 契約

所有 repo-local vault skills 都要求 cwd 是 vault root，也就是本 repo 根目錄。哨兵檔用 `schema/vault-map.md`——幾乎每個專案根目錄都有 `CLAUDE.md`／`AGENTS.md`，拿它當 gate 對「跑錯 repo」無效；`schema/vault-map.md` 這個路徑只存在於本 vault。

驗證方式用 harness-native `Read schema/vault-map.md`（不經 shell、跨平台）——讀得到即在 vault root，讀不到就停止並請使用者 cd 過來。不要用 shell 的檔案存在檢查（在 Windows 預設 PowerShell 會翻車）。

從其他專案呼叫本 repo skill 前，先 cd 到 vault root：`~/code/obsidian-memory`（三平台一致；cmd.exe 不認 `~`，改用 `%USERPROFILE%\code\obsidian-memory`）。

## 三個動作：Ingest / Query / Lint

wiki 的維護就是這三個動作，只在 `raw/` + `wiki/` 上進行；不涵蓋 Notion 私人筆記。

### Ingest（擷取）

新來源進 `raw/` → agent 讀 → 直接在 `wiki/` 寫入或更新頁面，**不需要先開一輪討論才動筆**。

進料管道（raw 為 write-once，落地後不改）：

- **使用者貼 URL**：先 Grep `raw/` 的 `source:` 查同 URL 是否已落地。**已存在**：不重複建檔，直接更新對應 wiki 頁（重讀來源、與現有 wiki 內容對照，實質變了就在頁面就地更新——來源過時靠此處人眼＋lint 語意層兜底，不做雜湊比對）。**未存在**才抓內容（優先 defuddle）轉 markdown，按 frontmatter 慣例（含 `source`、`published`）存 `raw/fetched/`，再往下 ingest。抓到的內容明顯殘缺（登入牆、付費牆、重 JS 頁）時**不落地 raw**——write-once 塞進殘件即凍結——改請使用者用 Web Clipper 剪藏。
- **Web Clipper 剪藏**、**使用者手動放檔**：存入 `raw/clippings/`，**落地即止、不自動往下 ingest**——這是使用者隨手剪存的原料，要不要進 wiki 由使用者明指。故 lint 的 raw 消化缺口掃描（`RAWGAP`）不涵蓋 `clippings/`，只掃 `fetched/`；clippings 未被 wiki 引用是正常狀態，不是缺口。

流程：

1. 寫一頁摘要（或更新既有摘要）。
2. 更新相關的實體頁 / 概念頁：整合新資訊、改寫舊摘要、**新資料與舊主張衝突時就地標記矛盾**。
3. 更新 `wiki/01.index.md`（新頁登錄、一行摘要）；**順手維護頂部「最近更新」區塊：加一筆本輪動到的頁（頁 wikilink＋一句），滾動保留最近 5 筆、超出刪最舊**——滾出的舊筆不另存、也不擴充筆數，要回溯更久之前的變更一律走 `git log`。這是給消費端的輕量近期入口（有界、不當完整歷史）；完整時序真相在 git。不建獨立熱檔（取捨見 [`wiki/LLM-Wiki-生態實作比較.md`](wiki/LLM-Wiki-生態實作比較.md)）。
4. 補交叉引用：新頁至少連 1–2 個相關既有頁，避免孤立。
5. **收尾輕量 lint（只檢當輪動到的頁，不掃全庫）**：交叉引用是否雙向、有無與既有主張矛盾、有無因新頁產生的孤立頁。當輪頁本就在 context 裡，成本趨近於零；這是擋「漂移」（頁面 ingest 時未同步交叉引用而無聲過時）的主要防線，全庫成長掃描仍不做。

單一來源可牽動多頁（典型 10–15 頁，屬正常，見 [`SYSTEM-DESIGN.md`](schema/SYSTEM-DESIGN.md)）。agent 自主寫，不逐頁拍板；使用者在旁讀、隨時導引重點即可。可一次一源慢慢做，也可批次 ingest。**例外閘門：單次 ingest 預計觸及（建/改/刪）超過 15 頁時，先列頁面清單問過使用者再動筆**——閘門刻意訂在典型範圍之上，只攔真正異常的大面積改動；15 頁以內照常全自主。

### Query（查詢）

向 wiki 提問 → agent 先讀 `wiki/01.index.md` 找相關頁 → 讀頁 → **附引用**綜合答案。Query 只查本地核心知識庫。

好答案（比較表、綜合分析、發現的關聯）**可回存成新 wiki 頁**，讓探索跟來源一樣複利累積，不要消失在對話裡。回存只在 wiki 內，不自動寫進 Notion 私人筆記。

### Lint（健檢）

定期健檢只掃 raw/wiki/schema，不掃 Notion 私人筆記。機械層檢查死連結、孤立頁、frontmatter、tag 漂移、raw 消化與索引缺口；語意層依日期輪替審查近期變動 wiki 頁的**矛盾與明確事實錯誤**。**語意層只抓「真的壞了」、不抓「能更好」**（2026-07-22 使用者拍板）：交叉引用缺口（含單向斷鏈）、過時主張（除非構成矛盾）、可改可不改的措辭一律**不報**——這些「能更好」的項任何頁都找得到，報了就永遠改不完，正是使用者要避免的吹毛求疵。交叉引用是核心紀律，但它在 **ingest 新頁時建立**（見上 Ingest 流程第 4、5 步，成本趨近於零的時機），例行健檢不再回頭挖缺口。掃描由 `vault-lint` skill 承載，可手動跑亦可掛排程，行為一致且 skill 本身不碰 git。**健檢即整理：機械項與語意項一律由 agent 自主修補**（與 wiki 全權一致；需要查證就自己查，2026-07-17 拍板取代原「語意項只報告」制）。`schema/BACKLOG.md` 的「待你決定」**只收真正需要使用者決策的項目**——包括需使用者才有的資訊、動 raw write-once／憲法檔／skill，或會推翻使用者已表態方向的項；該節去重維護、解決即移除。「Agent 已判」保留自主判斷的去重錨點，只有所依據的頁／基礎實際變動時才重新評估；使用者退回的修法記入「已婉拒」不再重提。不產快照報告。死連結列機械層之首有實證依據：LLM wiki 的頭號結構錯誤，見 [`LLM-Wiki-生態實作比較`](wiki/LLM-Wiki-生態實作比較.md)。

## wiki 頁面與索引

- **頁面類型**：摘要頁、實體頁（人/工具/組織）、概念頁、比較頁、綜合頁。
- **`wiki/01.index.md`**：內容目錄——每頁一行摘要 + wikilink，按類別分組，每次 ingest 更新。查詢時先讀它再鑽細節（省 token，也避免重複建頁）。
- **交叉引用是核心紀律**：wiki 的價值在互聯成網，不在單頁品質。

## 寫入慣例（`raw/` + `wiki/`）

這些是「怎麼寫」的品質慣例，**不是守門煞車**（不需拍板、不擋流程）。適用 agent 會寫的 raw/wiki。不涵蓋 Notion 私人筆記。

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
| `title` | 主題名，可含空格與中文；不加日期前綴 | 字串（檔名為其無空格、`-` 連接版） |
| `description` | 一句話自我介紹，給 Obsidian Bases、AI 查詢用。**適用**：wiki 頁、raw 網頁剪藏；其餘筆記可省 | 字串，30–80 字；不重複 title，避免「這篇／本文」自我指涉 |
| `created` | 進 vault 日期 | `YYYY-MM-DD` |
| `updated` | 最後修改日期 | `YYYY-MM-DD` |
| `source` | 來源 URL（網頁／影片連結）；回查用，非證據本體 | URL |
| `published` | 原始內容發佈／上傳日，與 `created`（進 vault 日）區分；不明可留空 | `YYYY-MM-DD` 或空 |
| `parent` | Obsidian 圖譜用 wikilink，讓筆記出現在圖譜 | `"[[01.index]]"`；vault 內多個資料夾各有同名 `01.index.md`，重名歧義時用路徑限定（如 wiki 頁 `"[[wiki/01.index]]"`） |
| `tags` | 主題分類 + 必要的功能性 tag | YAML list |

一般筆記需有 `title`、`created`、`updated`、`tags`。`tags` 一律用 YAML list，不用 inline array 或字串。Clippings 中 **Web Clipper 產出**的 `description` 為自動帶入的外站文案，豁免 30–80 字與風格要求，agent 不回頭修；**agent 貼 URL 落地**的 `fetched/` 來源則照正常 `description` 規則寫。

修改 `.md` 內容時盡量同步 `updated` 為今日日期（`YYYY-MM-DD`），但不為此中斷流程。

### 5. Wikilink 與 Obsidian 語法

- 寫入 wikilink 前確認目標檔案存在；不存在就改用外部 URL，不留死連結。
- 在正文使用 wikilink 時，盡量以相鄰文字說明關係（例如支持、反例、延伸或應用），不只堆疊「關聯」連結；純目錄／索引條目除外。
- `.base` wikilink 必須加副檔名：`[[02.影片清單.base]]`；embed 同理 `![[02.影片清單.base]]`。
- `.base` 內容不會在圖譜產生連結；要讓筆記出現在圖譜中，需在筆記 frontmatter 加 `parent: "[[01.index]]"`。
- `#` 開頭的內容會被 Obsidian 解讀為 tag；hex 色碼必須用反引號包住，例如 `` `#57F287` ``。
- 來源連結放置：單一主來源放 frontmatter `source`；正文需就地引用多個外部連結時用 inline 超連結（`[文字](URL)`）。

### 6. 查證產出的強度標註

deep-research 或其他對抗式查證的結果回存 wiki 時：每條主張就地標**證據強度與限制**（如「單一 preprint、未同儕審查」「單一作者經驗值、非實證」）；被查證**否決**的主張明列並標「勿引用」，不無聲丟棄；拍板結果附日期記進頁面。防查證結論被後續引用時失去強度資訊。

同理，日後新證據**推翻**頁面既有主張時，不默默改寫或刪除：原句就地改標「已被取代（YYYY-MM-DD）：新結論見某節／某頁」並保留，讓翻案本身留痕——被翻過案的主張正是「引用前再確認」的訊號。只有「推翻」才標；日常補充、細化、改寫不觸發，也不回頭挖舊頁補標（2026-08-11 拍板）。

## 可用 Skills

本 repo 在 `.agents/skills/` 提供 repo-local skills；`.claude/skills` 是 symlink。

| Skill | 用途 |
|---|---|
| `vault-lint` | wiki+raw 健檢，機械項與語意項皆由 agent 自主修補；真需使用者決策的才進「待你決定」，「Agent 已判」與「已婉拒」保留去重約束；手動／排程共用同一流程，本身不執行 git 動作 |

`vault-lint` 只在 vault 內執行、需 cwd 在 vault root，適用上節 CWD 契約。**目前沒有任何跨專案入口**——別的專案要取本 vault 的知識，只能由使用者自行開 session 進來查。

優先使用 skill，不新增平行流程。新增或修改 skill 時，盡量遵循 [Agent Skills](https://agentskills.io) 開放標準，讓內容可跨工具移植。

不重建已退場的 `ob-write`、`ob-read`、`vault-wiki-build`、`ask-vault` 或其輕量版；Ingest／Query 依本檔流程執行，Lint 使用現行 `vault-lint`。

### 新增 / 修改 skill 的本 repo 約束

**新增或修改 skill（含既有 skill 的 bug 修正、一致性調整）一律先問過使用者再動手，不比照 wiki 全權自主。** skill 改的是 agent 之後怎麼行動，影響範圍比一頁 wiki 內容大，值得每次都讓你點頭。

**怎麼問**：一次一題、走決策樹逐一解依賴，每題附上推薦答案；事實能查（filesystem／既有 skill／工具）就自己查，只把**決策**擺給使用者；未達共識不動筆。

- subagent 一律 `Agent` + `subagent_type: "general-purpose"`，prompt = `references/*.md` 全文 + 本次需求（不要叫 subagent 自己 Read）
- 工具限制等規則寫在 references 正文，自包含、不引用命名 agent
- 補 fallback 條款：「無 Agent 工具時主 agent 直接 Read references 跑同一流程」
- SKILL.md 主流程不寫憲法級規則（通用 wikilink/frontmatter 慣例等）——這些在本檔 `AGENTS.md`，不重述也不寫「見 AGENTS.md」指回
- 但 subagent 經 `references/*.md` 執行時要遵守的寫作規則（繁中、時間抗性等）必須在該 prompt 內可達（inline 或叫它先讀 AGENTS.md），不能只靠 AGENTS.md

## 時間抗性

Notion 私人筆記交給使用者，但 agent 寫的 wiki 頁仍要防過期：描述行為怎麼變、別把精確版本號釘死進正文，確切切換版本指向官方 changelog 由讀者回查；版本號只在它是行為關鍵分水嶺、讀者必須知道時才留並標來源。與版本耦合度低的行為約束（如某功能需特定 model / API）仍要留。程式類 raw 會隨工具迭代而過期，但留著仍有回查價值——真正要防過期的是 wiki 正文。
