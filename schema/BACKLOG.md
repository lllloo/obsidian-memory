---
title: Vault Lint Backlog
created: 2026-07-13
updated: 2026-08-14
tags:
  - meta
  - lint
---

# Vault Lint Backlog

vault 健檢的**待處理清單**,由 `vault-lint` skill 每輪讀寫(手動或排程觸發皆同)。健檢發現由 agent **自主修補**(機械項與語意項皆然,2026-07-17 拍板取代原「語意項只報告」制);**只有真正需要使用者的決策**去重後留在此,解決即移除;你的決定(婉拒)留在此,約束 agent 之後的行為。

放 `schema/` 而非 `feeds/`:這不是「給人瀏覽的自動產物」,而是 **agent 每輪讀回來、用來約束自己行為的跨 session 操作狀態**——與 [`MEMORY.md`](MEMORY.md) 同層。`feeds/` 的規則是 agent 不讀,把行為約束放進去會自相矛盾,別的工具打開 vault 也看不到你的決定。

- 修得掉的不進本清單——agent 當輪直接修(需查證就自己查),review 面在呼叫端的 commit／PR diff。
- **真正需要使用者的決策**才進 `待你決定`:需你才有的資訊、正解動到 raw write-once／憲法檔／skill、或會推翻你已表態的方向。你退回的修法進 `已婉拒`,skill 之後不再重提。
- **agent 自己判維持現狀／待觸發的**進 `Agent 已判`——去重錨點,不每輪浮上來問你,除非依據的頁／基礎實際變動才重新評估。
- **頁面引用一律用反引號**(如 `` `wiki/某頁.md` ``),**不得用 wikilink**——`schema/` 在死連結掃描範圍內,用 wikilink 會被自己的 lint 掃成死連結。
- **沒有「上次執行」欄位,無發現的一輪本檔零變更**——那是排程器的營運狀態,不是 vault 的知識;記在這裡會讓每輪都產生 diff、天天開一個「今天沒事」的 PR。排程是否還活著,去排程器的執行紀錄看。

## 設定

- `semantic_days: 7` — 語意層只審近 N 天有 git 變動的 wiki 頁
- `semantic_page_cap: 10` — 語意層單次最多審幾頁;超過時依日期無狀態輪替批次
- `semantic_utc_offset: +08:00` — `semantic_days` 日曆窗口與每日輪替日期使用的 UTC offset

## 待你決定(真正需要使用者,其餘見 `Agent 已判`)

_(目前無項目)_

## Agent 已判(維持現狀／待觸發,不再每輪問)

**新頁候選——開不開由 agent 全權自行決定,不問使用者**(2026-07-17 使用者明示授權,先前的「先不開」意見一併撤回、不再構成約束):

判準沿用 wiki 全權與反過度工程:被再次引用、或有新料撐得起一頁時就**直接開,不報備**;仍嫌單薄就續留 inline。本節條目只是 agent 自己的錨點(防重複重議、防機械層洗版),不是待辦、更不是待批。

- NEWPAGE | OpenClaw | 記憶六層與 Hermes 頁點名「值得日後專門對照」,橫跨兩簇的樞紐;目前 inline 提及暫足夠
- NEWPAGE | SDD 工具橫向對照(Spec Kit／Kiro／Tessl／BMAD／OpenSpec) | AI-自主頁聚焦「效果證據」、對照頁聚焦「工具功能」切面不同,BMAD 當初刻意折進;非急件
- NEWPAGE | route B 記憶(Cline Memory Bank) | route A 有 `wiki/LLM-Wiki-生態實作比較.md` 撐,route B 與相鄰 Letta MemFS 只有 inline

**frontmatter／一致性——agent 判維持現狀**(動既有 raw 反違反 write-once;此註記為錨點,防機械層重複洗版):

- FRONTMATTER | `sha256`(白名單外,見兩個 `raw/fetched/` cookbook 檔)、fetched 檔 `tags: clippings`(語意與資料夾矛盾)、clippings 回連不對稱(6 clippings 僅 1 有 wiki 回連)——三者同受 raw write-once 約束,正解是接受現狀;唯 `sha256` 若要正式納 `CLAUDE.md` 白名單(當內容指紋)才需使用者動憲法檔,不納亦無妨

**其餘 agent 判斷不動**:

- LINT-RULE | 數值／日期跨頁一致性檢查 | 2026-07-21 提出後**當日自行撤回**,不新增 lint 規則。外部依據(WikiCollide:真實 wiki 矛盾 54.7% 為數值類、邏輯僅 17.5%)看似強,但**就地實測後判定優先度不可遷移**:日期漂移查無實例(散亂日期經比對皆為不同事件);數字確有跨頁重述(`90.2` 見 4 頁、`1,642` 見 3 頁、「25 條」見 6 頁)故機制成立,但零實際不一致。Wikipedia 的漂移機制是「同一事實被大量獨立條目各自重述」,本 vault 有交叉引用紀律、不走該模式。**重開條件**:實際出現 2 次以上跨頁數值不一致。詳見 `wiki/Agent-維護知識庫的已知失效模式.md` 第 3 條。**看到那份 54.7% 數據時勿再直接據以重提**

- VERIFIER 誤報錨點 | 2026-07-21 該輪 verifier 曾誤報「54.7%／AUROC 75.1% 來源不明」,實為查錯論文(其出處 arXiv 2509.23233 不在其查核範圍),`wiki/Agent-維護知識庫的已知失效模式.md` 的引用不受影響,**勿據該誤報改動該頁**(該輪的另一半「內建品質評分第三題重跑」已於 2026-08-03 婉拒,見下節)
- STALE | `wiki/LLM-方案定價與-coding-agent-比較.md` | 孤立已修(補 2 條反鏈);定價數字仍為 2026-05~07 快照,頁面已標「回官網查」,agent 判**不值得例行 re-fetch**(11+ 廠商即時價、月月再過期)——要新快照再指示
- RAWGAP | `raw/fetched/OpenSpec-OPSX-Workflow.md` | opsx.md 已於 2026-07-21 消化進 `wiki/OpenSpec.md`(工作流／設定／schema 三節重寫,該頁第 23 行明載);機械層因該 wiki 頁 `source` 指主 repo 非 opsx.md 而續 flag,此為已消化錨點;首見 2026-07-22
- 維持現狀:無 in-vault 全文搜尋(21 頁 Grep 夠用)、evals 覆蓋不均(邊際價值低)

## 已修退場紀錄(精簡,細節見 git log)

- _(2026-07-18 deep-research 統計待回查項退場：保留有 commit 佐證的 2026-07-10「22 來源、25 主張」；2026-07-14 頁因現有 repo／commit 無法回查來源數、主張總數與確認數，已標「待考」，並保留頁面明列的 1 條否決主張。)_
- _(2026-07-16 全專案改進審視語意層 13 項——2 過時、9 交叉引用缺口、2 低優先群組——經「全都修」指示全數落地退場。)_
- _(2026-07-17「修問題」批次:全專案改進審視的 3 條 XREF、07-16 語意層的 3 矛盾 + 6 XREF + 4 過時、07-17 的 4 條低信心新發現,均已修補落地;`feeds/watch/` 漏登已補進 `schema/vault-map.md`、`schema/SYSTEM-DESIGN.md`;`published` 空值統一為 `""`。低信心「AI-自主 相關頁 pi-workflow 措辭」與「OpenSpec 31 工具」覆核後判定原敘述已足、退場。)_
- _(2026-07-17 逐件問診:MEMORY「貼 URL ingest 全流程」升級訊號候選經使用者核可退場(已於 `schema/MEMORY.md` 劃線註記);跨工具可攜縫補丁已落地——`AGENTS.md` 為 `CLAUDE.md` 的 symlink,故該句寫在 `CLAUDE.md` 的 `@import` 行旁。)_
- _(2026-07-17 治理改制:使用者拍板 vault-lint 語意項改**全面自動修**(不加對抗驗證),「語意項只報告」制退場;原「維持現狀:vault-lint 第二段刻意延遲」條目隨之結案。STALE `wiki/第二大腦方法論比較.md` 缺 Hermes Kanban 補充,依新制當場修補退場。)_
- _(2026-07-17 第二輪語意層(上輪欠審 9 頁＋第二大腦方法論比較):subagent 平行審出約 22 項獨立發現(1 高、8 中、13 低——指向錯誤、歸屬錯誤、方向倒置、措辭過寬、版本釘死、回連缺口等),全數當輪自主修補落地,動 12 個 wiki 頁;無新增待決項。)_
- _(2026-08-03 `vault-updates-daily` 整體退場:使用者拍板移除 skill、`feeds/updates/` 與全部文件引用。依據為近 7 篇日報實測——最大宗來源 GitHub Copilot 多為企業治理條目、OpenCode 多為版本 bump、主力工具 Claude Code 近 7 天 0 筆,且 08-03 兩筆全是 08-02 重報。此前的 starred 停用與雲端排程條目一併作廢,勿據以重開。)_
- _(2026-07-20 SKILL-STALE 退場:使用者核可動 skill,`.agents/skills/vault-lint/SKILL.md` 第 16 行「該 prompt 即使用者對 push 的明確同意」括號已刪——push 守門於 2026-07-20 移除後該依據不存在;「本 skill 不碰 git、由呼叫端決定 commit／PR」的設計本身不變。)_
- _(2026-07-18 語意層續審由 tracked carryover 改為日期驅動的無狀態輪替;避免無發現時游標不前進、相同頁面反覆占滿 cap,同時維持安靜輪零檔案變更。)_

## 已婉拒

- 2026-07-21 | `raw/` write-once 由文件約定升級為 git pre-commit hook 強制 | 使用者退回。原提案依據見 `wiki/Agent-維護知識庫的已知失效模式.md` 第 4 條（agent 破壞性刪除事故彙整）；該 hook 的實際保護面本就有限——它擋的是 write-once 違規進入 git 歷史，擋不住檔案系統層的刪除（未 commit 的刪除 `git restore` 即可救）。**不再提**
- 2026-08-03 | 主動提議消化 `raw/clippings/` 未消化剪藏 | 使用者退回（當時 5 篇無 wiki 回連）。clippings 維持憲法的「落地即止」——**由使用者明指才消化，agent 不主動列清單勸進**
- 2026-08-03 | 重跑「agent 知識庫專案的內建品質評分」第三題(13 個同類 repo 淺 clone＋grep,查是否有偵測式而非排序式的品質機制) | 使用者退回。該題兩輪 deep-research 零產出且證據鏈中從未讀過任何目標 repo,狀態是「未查到」非「已排除」;但 2026-07-22 `vault-page-score` 階段 0 實測已推翻前提——本 vault 22 頁由同一套寫入慣例產出、全過多輪 lint,方差太小,查到與否不改變任何決定。缺口狀態就地留在 `wiki/LLM-as-judge-知識庫頁面評分.md`。**不再提重跑**
- 2026-08-03 | 把 `topics/`／`cards/` 的工作知識納入 wiki 覆蓋（含「挑一個主題明指進 raw 試跑」的折衷版） | 使用者退回，界線不動。wiki 就定位為元層次研究庫，不追求覆蓋全部知識面；「wiki 只覆蓋三分之一知識面」不是缺口。**不再提**
