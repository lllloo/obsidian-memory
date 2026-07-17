---
name: vault-lint
description: vault 健檢:掃 wiki+raw 的死連結、孤立頁、frontmatter 缺欄、tag 漂移、raw 消化缺口(機械層),加近期變動頁的矛盾／過時／交叉引用缺口審查(語意層)。機械項與語意項一律由 agent 自主修補(語意修補需要查證就自己查);只有真正需要使用者的決策(需使用者才有的資訊、動 raw write-once、動憲法檔／skill)才進 schema/BACKLOG.md,同一問題不重複洗版。可隨時手動跑,也可掛排程;兩者行為完全一致、不需參數。使用時機:使用者要求「vault 健檢」「lint 報告」「掃一下 wiki」「檢查 vault 健康」「跑一下健檢」,或直接呼叫 /vault-lint。
---

# Vault Lint

健檢即整理:掃出的問題**由 agent 自主修補**——機械項照規則修,語意項(矛盾／過時／引用缺口)與 Ingest 同權限,有把握就直接修、需要查證就自己查證再修;`raw/` 維持零寫入(write-once)。只有**真正需要使用者的決策**才寫進待處理清單 `schema/BACKLOG.md`(2026-07-17 使用者拍板,取代原「語意項只報告」制):

- 需要使用者才有的資訊(原始記錄、當時意圖)才能核實的項;
- 正解會動到 `raw/` write-once、schema 憲法檔(`CLAUDE.md`／`SYSTEM-DESIGN.md`)或 skill 本身的項;
- 使用者曾表態過方向、再動會推翻其決定的項。

清單放 `schema/`(agent 每輪讀回來約束自身行為的操作狀態),不放 `feeds/`(agent 不讀區)。

**手動與排程共用同一條流程,無模式分支、無參數差異。** 本 skill **不執行任何 git 動作**(不 commit、不 push、不開 PR),因此無人值守時不會卡在需要人拍板的守門上。跑完只留檔案變更;要不要落成 commit／PR 由呼叫端決定——手動時由使用者指示,排程時寫進該排程自己的 prompt(**該 prompt 即使用者對 push 的明確同意**,不由本 skill 代行)。

## 產出

- 待處理清單 + 設定:`schema/BACKLOG.md`(單一持久檔,去重後留未解決項,解決即移除)。**不產快照報告檔,不寫入 `feeds/`。**

`BACKLOG.md` 結構:

- `## 設定` — `semantic_days`、`semantic_page_cap`。
- `## 待你決定` — **只收真正需要使用者的決策項**(判準見上),逐條一行(帶頁面、一句話、首見日)。可自主修的項不進此節——直接修掉。
- `## Agent 已判` — agent 自主判斷**維持現狀／待觸發**的項(反過度工程判斷暫不開頁、動既有 `raw/` 違反 write-once、不值得例行動作等)。這節是**去重錨點**,不是待辦:去重時視為既有項、不重洗回 `待你決定`,只有該項所依據的頁／基礎實際變動才重新評估。注意「修得掉但還沒修」不屬此節——那種當輪就修。
- `## 已婉拒` — 使用者退回的項;每條記所在段落錨,之後不重提。
- `## 本輪語意層截斷` — 語意層的 **carryover 狀態**:記本輪 cap 截斷未審的 `CHANGED` 頁,供下輪優先續審(見主流程第 7 步)。**更新時機**:本輪實際跑了語意審查、且整輪另有檔案寫入時,改寫為本輪狀態;整輪無其他寫入則保留原節不動——安靜的一輪連這節也不碰,零變更契約優先於紀錄新鮮度。

**沒有心跳／執行狀態區,且無發現時本檔零變更。** 「上次何時跑過」是呼叫端的營運狀態(排程器的執行紀錄),不是 vault 的知識狀態,寫進來只會讓每輪都產生 diff——**安靜的一輪必須安靜到檔案層級**,呼叫端才能靠「有無變更」判斷要不要開 PR。掃描異常(`scan-error`)不靠心跳欄位傳達,改為進 `待你決定`(見主流程第 4 步),它本來就是該讓人看到的「有事」。

**寫入本檔時,頁面引用一律用反引號**(如 `` `wiki/某頁.md` ``)**,不得用 wikilink**——`schema/` 在死連結掃描範圍內,wikilink 會被自己掃成死連結。

## 主流程

1. 用 harness-native `Read schema/vault-map.md` 確認 cwd 是 vault root;讀不到就停止,請使用者 cd 到 vault root(`~/code/obsidian-memory`;cmd.exe 用 `%USERPROFILE%\code\obsidian-memory`)。
2. `Read schema/BACKLOG.md` 取設定(`semantic_days`、`semantic_page_cap`;讀不到用預設 7 天、10 頁)與既有清單(含 `已婉拒`)。
3. 執行機械層掃描:

```
python3 .agents/skills/vault-lint/scripts/lint_scan.py --days <semantic_days>
```

4. **熔斷檢查**:掃描輸出**有任何 `ERROR:` 行、或缺 `SCAN:complete` 行** → 本輪視為掃描異常:**不修補、只新增、不退場**(不依壞輸出動 wiki,也不移除 BACKLOG 既有項),在 `待你決定` 補一條高嚴重度項「機械掃描異常,本輪不修補不退場」(附錯誤摘要與首見日;去重規則同其他項,已在清單就不重複加)後結束本輪。異常排除後該項照常退場。正常則往下。
5. 機械層修補(agent 自主判斷並修,逐項記錄):
   - `DEADLINK`:目標檔存在、可**唯一對應**(漏資料夾限定、大小寫差異)→ 直接修(wikilink 或 markdown 式路徑,依原文語法修)。多候選 → 讀上下文判斷正確目標再修。目標不存在 → 依內容處置:改外部 URL、改純文字,或值得建頁就建(建頁屬語意修補,照第 8 步紀律)。目標在 `feeds/` 等範圍外(wiki 不得引用 feeds)→ 移除或改寫該引用。
   - `INDEXGAP`:有 `description` 直接複製登錄 `wiki/01.index.md`;無 `description` → 讀頁寫一行摘要登錄,順手補該頁 `description`。
   - `ORPHAN`:讀頁找 1–2 個相關既有頁補雙向引用;真的無處可連才記 `Agent 已判` 錨點。
   - `FM`:缺欄可補值者直接補(如缺 `updated` 取 git 最後變動日)。
   - `TAG`:同義異寫漂移由主 agent 判讀後直接正規化(沿用既有 tag,改少數就多數)。
   - `RAWGAP`:`raw/clippings/` 彙總檢視、`raw/fetched/` 逐條檢視;值得消化的走 Ingest 流程;判定不值得的記 `Agent 已判` 錨點。
   - 修補動到的頁同步 `updated` 為今日。
6. **對 BACKLOG 做 reconcile**(去重 + 退場):
   - **去重**:新掃出的每一項,跟 BACKLOG 既有項比對(同頁 + 同目標/同議題)→ 已在清單就不重複加。比對用讀進 context 的兩份短文本判斷,不算 hash。
   - **退場**(熔斷未觸發時):BACKLOG 既有項本輪已修掉或掃描不再輸出 → 移除。語意項僅當**該頁本輪在 `CHANGED` 內被重審且未重現**才移除;該頁未變動 → 保留。
   - **已婉拒 / Agent 已判**:兩節的項本輪一律**跳過不重提、不重修**——本輪掃出的項若已對應到其中任一節的錨點(如 `Agent 已判` 的 RAWGAP clippings 彙總),視為既有;唯該項所依據的頁／基礎實際變動時才重新評估。
7. 語意層審查:取 `CHANGED` 清單,超過 `semantic_page_cap` 時**先取 BACKLOG「本輪語意層截斷」節所列且仍在 `CHANGED` 內的頁(上輪欠審優先,防同一批最近變動頁輪輪擠掉其他頁),再依最近變動補足**,並標注截斷。每頁備妥「目標頁全文 + 鄰接頁全文(wikilink 指到的頁與連入它的頁,各至多 5 頁)」**加上該頁在 BACKLOG 的既有語意項**(供去重)。可用 `Agent` 工具時以 `subagent_type: "general-purpose"` 平行審查,prompt = `references/semantic-review.md` 全文 + 該頁與鄰接頁內容 + 既有語意項(不要叫 subagent 自己讀檔);無 Agent 工具時主 agent 直接照該 reference 逐頁審查。subagent 只審不改;發現去重後交下一步處置。
8. 語意修補(主 agent 執行,不交 subagent 改檔):逐條處置語意發現——
   - **有把握就直接修**:矛盾就地改正或標記、過時主張更新、引用缺口補雙向 wikilink 並以相鄰文字說明關係。
   - **需要查證就自己查**(WebFetch 官方來源、回讀 `raw/`)再修;查證產出就地標證據強度與限制。
   - 符合「真正需要使用者」判準(見開頭)的才進 `待你決定`;判維持現狀的記 `Agent 已判` 錨點。
   - 修補動到的頁同步 `updated`,收尾對當輪動到的頁做輕量 lint(交叉引用雙向、無新矛盾、無新孤立頁——同 Ingest 收尾)。
9. **只在內容真的變了才寫回** `schema/BACKLOG.md`(待決項有增減、既有項內容有改、或依「產出」節時機更新截斷節)。有寫回才同步 frontmatter `updated` 為今日。**本輪無任何增減 → 完全不碰該檔**(連 `updated` 也不動),讓檔案層級維持零變更。
10. **止於檔案變更**:不 commit、不 push、不開 PR、不建分支。跑完照下方「固定回覆」報告即可,git 交由呼叫端處理。**無發現的一輪應留下零檔案變更**——呼叫端(排程 prompt)就是靠「有無變更」決定要不要開 PR,任何無謂的寫入都會變成每日雜訊 PR。修補全數自主,但 review 面不消失:全部變更留在 working tree,由呼叫端的 commit／PR diff 給使用者把關。

## 資源

- `references/semantic-review.md`:語意層審查 prompt(含去重指示)。傳給 subagent 時貼全文。
- `scripts/lint_scan.py`:機械層掃描,輸出 machine-readable lines + `SCAN:complete`(格式見腳本 docstring)。

## 固定回覆

完成後回覆:

- 本輪:自主修 N 機械項、M 語意項,新增待決 K 項、退場 J 項,BACKLOG 現存 open 數。
- 本輪狀態(`ok` / `scan-error` / `no-op`)——**只在回覆裡講,不寫進任何檔案**。
- `待你決定` 前 3 條(高嚴重度優先)。
- 語意層有截斷時明講掃了幾頁、略過幾頁。
- **本輪實際寫入的檔案清單**(未 commit);零變更時明講「無檔案變更」。本 skill 不開 PR,這份清單就是使用者的 review 入口,也是呼叫端判斷要不要開 PR 的依據。
