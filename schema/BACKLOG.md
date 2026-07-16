---
title: Vault Lint Backlog
created: 2026-07-13
updated: 2026-07-16
tags:
  - meta
  - lint
---

# Vault Lint Backlog

vault 健檢的**待處理清單**,由 `vault-lint` skill 每輪讀寫(手動或排程觸發皆同)。findings 去重後留在此,解決即移除;你的決定(婉拒)留在此,約束 agent 之後的行為。

放 `schema/` 而非 `feeds/`:這不是「給人瀏覽的自動產物」,而是 **agent 每輪讀回來、用來約束自己行為的跨 session 操作狀態**——與 [`MEMORY.md`](MEMORY.md) 同層。`feeds/` 的規則是 agent 不讀,把行為約束放進去會自相矛盾,別的工具打開 vault 也看不到你的決定。

- 機械可修項(路徑錯的死連結、缺欄位、有 `description` 的 index 漏登)由 skill **自動修**,不進本清單。
- 需判斷 / 語意項進 `待你決定`;你退回的修法進 `已婉拒`,skill 之後不再重提。
- **頁面引用一律用反引號**(如 `` `wiki/某頁.md` ``),**不得用 wikilink**——`schema/` 在死連結掃描範圍內,用 wikilink 會被自己的 lint 掃成死連結。
- **沒有「上次執行」欄位,無發現的一輪本檔零變更**——那是排程器的營運狀態,不是 vault 的知識;記在這裡會讓每輪都產生 diff、天天開一個「今天沒事」的 PR。排程是否還活著,去排程器的執行紀錄看。

## 設定

- `semantic_days: 7` — 語意層只審近 N 天有 git 變動的 wiki 頁
- `semantic_page_cap: 10` — 語意層單次最多審幾頁,超過取最近變動者並標注截斷

## 待你決定

- [低] RAWGAP | `raw/clippings/` | **現存 clippings 全數判定已消化,無待 ingest**(機械層仍會逐篇 flag,因未加 wikilink;此註記為判斷錨點,防重複洗版)。2026-07-16 結清最後 2 篇:`Claude-Code-Best-Practice-—-Threads-Carousel-Cards`(82 條操作最佳實務)判定**不 ingest**——純操作 cheatsheet、大量版本專屬易過期內容與 wiki 時間抗性相斥,概念層已由 harness/記憶/多-agent/實證四側面 5–7 頁涵蓋,屬使用者自撿進 topics 公開層的料;`The-Official-BMad-Method-Masterclass`(BMAD IDE 工作流示範逐字稿)行銷示範品質撐不起一手實體頁,已將其角色鏈(Analyst→…→QA)＋advanced elicitation＋doc sharding 最小增補進 `wiki/AI-自主工作流的實證檢驗.md` spec-driven 節,不建專頁。原項首見 2026-07-13

### 2026-07-16 全專案改進審視(本地三層,未跑網路搜尋;使用者「先紀錄再考慮」)

**wiki 織網缺口(語意層,主線抽查已坐實)**

- [中] STALE+ORPHAN | `wiki/LLM-方案定價與-coding-agent-比較.md` | 全庫唯一近孤立頁(內文反鏈僅 `wiki/Claude-Code-記憶系統六層比較.md` 1 條),且唯一停在 `updated: 2026-07-09`(其餘 20 頁滾到 07-14~07-16)。定價是最易過期內容卻最久沒回查。建議:重讀來源更新快照 + 補連 `wiki/AI-自主工作流的實證檢驗.md`、`wiki/Context-優先與多-agent-的適用邊界.md`(「選哪個 agent／花多少錢」決策軸)
- [中] XREF | `wiki/跨專案第二大腦整合模式.md`↔`wiki/OKF-與本-vault-的相容性.md` | 前者第 89 行整段講 OKF 選擇性匯出卻只用外部 URL、沒連 OKF 拍板頁;兩頁是同一件事的兩半。補雙向 wikilink(OKF 頁內文反鏈亦僅 1 條)
- [低] XREF | `wiki/OpenSpec.md`↔`wiki/Agent-Harness-Engineering-框架綜述.md` | OpenSpec 第 159 行連了 Agent-Harness,後者相關頁區未回指;OpenSpec 為 07-16 新頁、反鏈僅 1 條。補回指(框架↔實體)
- [低] XREF | `wiki/設計品質的可量化檢測.md`↔`wiki/AI-生成流程圖與架構圖.md` | 兩頁都自我定位為「AI 生成物需外部判準」的領域落地、都連 `wiki/AI-自主工作流的實證檢驗.md` 卻不彼此連。補互連

**覆蓋缺口 / 可延伸新頁(需先確認不觸犯反過度工程)**

- [中] NEWPAGE | OpenClaw | `wiki/Claude-Code-記憶系統六層比較.md` 第 52 行自我點名「Hermes 與 OpenClaw 同血緣,值得日後專門對照」;OpenClaw 另在 memsearch 移植、`hermes claw migrate` 多次被提卻無實體頁。橫跨記憶六層與 Hermes 兩簇的樞紐
- [低] NEWPAGE | SDD 工具橫向對照 | Spec Kit／Kiro／Tessl／BMAD／OpenSpec 散在 `wiki/AI-自主工作流的實證檢驗.md` 第 54 行 prose + 獨立 OpenSpec 頁,而平行的 wiki 工具簇已有 `wiki/LLM-Wiki-生態實作比較.md` 對照表。**權衡**:AI-自主聚焦「效果證據」、對照頁聚焦「工具功能」,切面不同不算重複,但 BMAD 當初刻意折進而非開頁——非急件
- [低] NEWPAGE | route B 記憶實作 | `wiki/Agent-記憶兩大路線-知識庫與-memory-bank.md` 的 route A 有 `wiki/LLM-Wiki-生態實作比較.md` 撐實作細節,route B(Cline Memory Bank)與相鄰 Letta MemFS 只有 inline 描述、無對等實作頁。可待再被引用時再開

**skill／系統層(改 agent 行為,依 repo 規則須逐項拍板)**

- [中] SKILL | `vault-updates-daily` 雲端 routine 未排 | 該 skill 的 `starred-repos.txt` snapshot fallback 存在的唯一理由就是雲端 token-free 排程跑,基建做好卻只有 vault-lint 一支 routine。前置:須先本機 `--snapshot-starred` 一次並授權推送
- [中] SKILL | MEMORY「貼 URL ingest 全流程」候選計數失效 | 手動 ingest 無具名入口累積次數,結構上永遠踩不到「滿 3 次」門檻、無限期卡在 0 次;fetch 段已被全域 `defuddle` 覆蓋。建議做決策:退場 or 改用「時間／成長」訊號
- [低] SKILL | 跨工具可攜縫 | `schema/MEMORY.md` 自稱唯一跨工具可攜操作記憶,但靠 `CLAUDE.md` 的 `@schema/MEMORY.md` 自動載入,而 `@import` 為 Claude Code 專屬;Codex／Cursor／opencode 讀 `AGENTS.md` 不解析。可在 `AGENTS.md` 正文加一句「非 Claude Code 工具請先 Read `schema/MEMORY.md`、`schema/BACKLOG.md`」
- [低] SKILL | `ask-vault` 缺 `OBSIDIAN_VAULT` 逃生口說明 | 腳本支援該環境變數覆寫 vault 路徑,但 `SKILL.md` 沒提;非預設路徑時 agent 只會拿到「工具未就緒」。補一行
- [低] SCHEMA | `schema/vault-map.md`、`schema/SYSTEM-DESIGN.md` 漏登 `feeds/watch/` | 兩檔 feeds 子樹只列 youtube／updates,但 watch 實際存在、`CLAUDE.md` 已列;vault-map 自稱「單一權威清單」卻缺一項(vault-watch 後加時同步漏)

**frontmatter／一致性(注意 `raw/` write-once 約束)**

- [低] FRONTMATTER | `sha256` 為白名單外欄位 | 只在 `raw/fetched/Anthropic-Cookbook-Research-Prompts.md`、`raw/fetched/Anthropic-Multi-Agent-Research-System.md` 出現,同資料夾其餘 3 檔沒有。**注意**:移除會改既有 raw、違反 write-once;現實解是納入 CLAUDE.md 白名單(當內容指紋)或接受現狀
- [低] FRONTMATTER | fetched 檔全掛 `tags: clippings` | 語意與資料夾矛盾(fetched 是 agent 貼 URL、clippings 是 Web Clipper);跨資料夾 tag 查詢會混淆。同受 raw write-once 約束,傾向接受或改慣例、不回改既有檔
- [低] FRONTMATTER | clippings 回連紀律不對稱 | 6 個 fetched 全有 wiki 回連,6 個 clippings 僅 1 個有——正是機械層每輪 flag clippings 的根因。立慣例「clipping 種子某 wiki 頁時在該頁補 `[[clipping]]` 回連」可讓 linter 自動消 flag
- [低] FRONTMATTER | `published` 空值寫法不一 | `wiki/OpenSpec.md` 用尾隨空白、`wiki/pi-workflow-編排-harness-與本-vault-分野.md` 用 `""`;下次 lint 順手統一

**審視後判斷維持現狀(不動)**:vault-lint 第二段語意自動修(刻意延遲、重開條件明確)、無 in-vault 全文搜尋(21 頁 Grep 夠用)、evals 覆蓋不均(機械掃描與外部 API 相依 skill 補 eval 邊際價值低)。

_(2026-07-16 語意層 13 項——2 過時、9 交叉引用缺口、2 低優先群組——經使用者「全都修」指示已全數修補落地,退場。)_

### 2026-07-16 語意層例行審查(排程,近 10 頁)

**矛盾**

- [高] 矛盾 | `wiki/多智能體研究系統-Anthropic.md` | 交叉引用區描述 `wiki/pi-workflow-編排-harness-與本-vault-分野.md` 為「foreach/reduce 對照 orchestrator-worker」,但該頁本文主張其較貼近 `dynamic` pattern(子任務非預先定義、動態委派),兩頁對同一技術判斷描述相反。建議修正本頁交叉引用敘述以符合對方實際主張
- [中] 矛盾 | `wiki/第二大腦整合的現成工具與做法.md` | 第33行將 MCP 工具接入 vault 框定為「若採用」的條件式,第47行卻斷言本 vault 已有「MCP 可達(直連層)」,與現況(僅 `ask-vault` headless 查詢、非 MCP protocol)不符。建議統一條件語氣或註明尚未落地
- [中] 矛盾 | `wiki/設計品質的可量化檢測.md` | 第17/36行將「AI agent 模擬使用者」與其餘三項純工具量測並列為「非 LLM 自評」,但該項本質仍是 LLM 判斷,未呼應鄰接頁 `wiki/AI-自主工作流的實證檢驗.md` 對 LLM-as-judge self-preference bias 的提醒。建議補說明規避同源偏袒風險或收斂措辭

**引用缺口**

- [中] XREF | `wiki/LLM-Wiki-知識管理模式.md` | 「關聯」節未回連 `wiki/第二大腦整合的現成工具與做法.md`(引用本頁定義三層架構原型)與 `wiki/多智能體研究系統-Anthropic.md`(引用本頁比較檢索範式),兩處皆單向
- [中] XREF | `wiki/AI-自主工作流的實證檢驗.md` | 第 48、132 行「五步迴圈」一詞全文未定義、無其他頁連結說明所指。建議補定義或連到 `wiki/Agent-Harness-Engineering-框架綜述.md` 對應迴圈(需核對步數是否吻合)
- [中] XREF | `wiki/Building-Effective-Agents-Anthropic.md` | `wiki/pi-workflow-編排-harness-與本-vault-分野.md` 兩處引用本頁定位其 workflows/agents 二分法框架,但本頁「交叉引用」清單未回連該頁
- [低] XREF | `wiki/Agent-Harness-Engineering-框架綜述.md` | 「相關頁」清單未回連 `wiki/pi-workflow-編排-harness-與本-vault-分野.md`(該頁引用本頁作編排職能定位依據)
- [低][低信心] XREF | `wiki/AI-自主工作流的實證檢驗.md` | 「相關頁」對 pi-workflow 頁的摘述用詞與該頁實際引用語境略有落差,建議覆核措辭精準度
- [低][低信心] XREF | `wiki/第二大腦方法論比較.md` | 「侷限與存疑」未解問題句與 `wiki/第二大腦整合的現成工具與做法.md` 證據強度小節實質為同一問題最新印證,但未互相點出

**過時／時間脆弱**

- [低] STALE | `wiki/AI-自主工作流的實證檢驗.md` | 第 54 行稱 OpenSpec 為「完整五步」,但 `wiki/OpenSpec.md` 明確標 explore 為可選,措辭易誤導為五步皆必經
- [低] STALE | `wiki/跨專案第二大腦整合模式.md` | 第45行「不建獨立熱檔」決定敘述未標日期,鄰接頁(`wiki/LLM-Wiki-生態實作比較.md`、`wiki/第二大腦整合的現成工具與做法.md`)皆標「2026-07-15 拍板」
- [低] STALE | `wiki/多智能體研究系統-Anthropic.md` | 第23行 200K token 上限數字未標時間前提;同頁模型配置已做「2025-06 快照」時間抗性標註,唯此數字未同等處理
- [中][低信心編輯判斷] STALE | `wiki/Building-Effective-Agents-Anthropic.md` | SWE-bench Verified 佐證「輸出品質可客觀衡量」缺對 OpenAI 審計缺陷率(59.4% 有實質缺陷、SWE-bench-Live 成功率腰斬)的強度標註呼應,依 CLAUDE.md 寫入慣例第 6 條可能需就地補註
- [低][低信心] STALE | `wiki/OpenSpec.md` | 第132行「31 個工具中 28 個」為快照數字,頁面已標「30+ 為下界」部分緩解,殘留風險低
- [低][低信心] STALE | `wiki/pi-workflow-編排-harness-與本-vault-分野.md` | 「6 種 stage pattern」「4 個內建命名流程」等功能計數未標查核時間
- [低][低信心] STALE | `wiki/第二大腦方法論比較.md` | Hermes 雙軸類比(2026-07-09 驗證)未提及該頁 2026-07-14 新增的 Kanban board 任務佇列子系統
- [低][低信心] STALE/疑慮 | `wiki/第二大腦整合的現成工具與做法.md`↔`wiki/LLM-Wiki-生態實作比較.md` | 兩輪日期主題皆不同的 deep-research,統計數字(22 來源、25 條主張)完全相同,不排除巧合,亦可能複製前次框架未更新;建議之後回查原始記錄核實
- [低][低信心] STALE | `wiki/多智能體研究系統-Anthropic.md` | 「一次 spin up 3–5 個 subagent」與分級表「複雜研究 10+ 個」數字用語有張力,可能非真矛盾,屬一般情境 vs 上限情境的措辭問題

本輪已重審並確認**仍開啟、內容不變**:`wiki/跨專案第二大腦整合模式.md`↔`wiki/OKF-與本-vault-的相容性.md` XREF、`wiki/OpenSpec.md`↔`wiki/Agent-Harness-Engineering-框架綜述.md` XREF、`wiki/設計品質的可量化檢測.md`↔`wiki/AI-生成流程圖與架構圖.md` XREF(三者皆列於本節上方「wiki 織網缺口」段落)。

本輪截斷:20 頁 `CHANGED`(7 天內有 git 變動)依 `semantic_page_cap: 10` 只審最近變動的 10 頁;略過 10 頁(`wiki/第二大腦實踐與本-vault-優化.md`、`wiki/Context-優先與多-agent-的適用邊界.md`、`wiki/Agent-Harness-Engineering-框架綜述.md`、`wiki/Hermes-Agent.md`、`wiki/OKF-與本-vault-的相容性.md`、`wiki/LLM-方案定價與-coding-agent-比較.md`、`wiki/LLM-Wiki-知識管理模式.md`、`wiki/LLM-Wiki-生態實作比較.md`、`wiki/Claude-Code-記憶系統六層比較.md`、`wiki/Agent-記憶兩大路線-知識庫與-memory-bank.md`)留待下輪。

## 已婉拒

_(目前無項目)_
