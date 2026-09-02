---
title: OpenClaw 與 Hermes Agent 比較
description: 兩套自架常駐 personal agent 的路線對照：OpenClaw 2.0 的 Gateway 分離架構與審查式 skill 演進，對上 Hermes 的單體架構與放手式自我進化
created: 2026-09-02
updated: 2026-09-02
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - skill
  - memory
---

# OpenClaw 與 Hermes Agent 比較

兩者同屬「**自架、常駐、會主動找你**」的 personal agent，與跑完即停的 Claude Code／Codex 不同類（分野見 [[Agent-Harness-Engineering-框架綜述]]）。它們的血緣早有紀錄——Hermes 的 `hermes claw migrate` 就是從 OpenClaw 匯入 persona／記憶／skill／API key，而 Claude Code 生態的 memsearch plugin 是把 OpenClaw 的記憶架構移植過去（見 [[Claude-Code-記憶系統六層比較]] Level 3）。本頁把兩者拉齊對照。

> **證據強度與時效**：OpenClaw 側以官方 release notes 為準（[[OpenClaw-2.0-Release-Notes]]，一手）；架構定性與競品評語出自 Decrypt 記者綜述（二手、未獨立查證，逐處標註）。Hermes 側沿用 [[Hermes-Agent]]，其資料為 **2026-07 快照**，本頁成稿時已兩個月未更新——Hermes 期間若有版本變動不在射程內，引用前宜回查官方文件。

## 定位與架構

| | OpenClaw | Hermes Agent |
|---|---|---|
| 出身 | Peter Steinberger（PSPDFKit 創辦人）個人專案，後移入 **OpenClaw Foundation** 非營利；作者 2026-02 加入 OpenAI 主持 personal-agent 方向，但**專案本身未併入 OpenAI**（OpenAI 只是夥伴之一，另有 Microsoft、GitHub、Nvidia、Atlassian、Tencent） | Nous Research 開源，MIT 授權 |
| 主軸 | 自架 personal agent：常駐本機、自有排程醒來，從 WhatsApp／Telegram／Discord／Signal 主動找你 | 自我進化 agent（coding + personal），標語 *The agent that grows with you* |
| 架構形狀 | **Gateway daemon 與 agent 分離**：Gateway 是通道橋接與安全邊界，agent 掛在其後 | **單體**：對話迴圈、工具派發、記憶收在同一個 agent class〔以上兩格出自 Decrypt 綜述，記者評語為「難擴展但好推理」〕 |
| 社群規模 | 極大：2.0 單次發布併入 16,977 個 PR | 小得多 |

貢獻者人數有**來源衝突**：官方 release notes 寫 **987 位**，Decrypt 與 InfoQ 寫 **933 位**（其中 569 位首次貢獻）。引用時擇一並標來源，勿當定論。

## OpenClaw 2.0（v2026.8.1）改了什麼

原訂只做「簡化安裝 + 重寫瀏覽器 App」兩件小事，因為兩者都動到同一批程式碼而滾成全面改版，官方自嘲為「accidentally」——這是團隊公開承認 scope creep，不是行銷話術。此前 230 天出過 106 個版本（幾乎每日），這次沉寂七週。

- **記憶換核心**：built-in Memory 接管搜尋與召回路徑，**QMD 退場**（`openclaw doctor --fix` 遷移）。代價明確：QMD 專屬的 reranking、query expansion、跨 agent transcript 搜尋**一併廢除**。同一 agent 的其他私人對話**預設可召回**，含 session reset 前那段；召回不跨群組、頻道、其他 agent，明確的 DM 隔離設定優先。另新增 `openclaw memory forget`，依 provenance 清除可歸因的衍生記憶（原始 transcript 與無血緣的舊筆記不受影響）。`MEMORY.md`／`USER.md`／Memory Wiki／LanceDB 仍各有角色。
- **session 進 SQLite**：可 rewind 到某則使用者訊息並 fork 分支切換。**rewind 只改 transcript 分支，不回溯檔案、已送出訊息或其他工具副作用**。降版會看不見遷移後建立的 session，升級前需備份。
- **Skill Workshop**：把提案、檢查、決策、套用歷史收進同一流程。自我學習產出的是**待審提案**，不直接改 live skill；有 plugin 提供的 scanner／benchmark／grader，**critical prompt-injection findings 會直接擋下套用**。模式分 `off`／`propose`／`auto`（新裝預設 `auto`，升級沿用原設定），但 `auto` 也只能建立或更新 **Workshop 自己擁有的** skill；使用者自寫與他人擁有的 skill，自動學習只能建議、不能自行改寫或刪除。
- **multiplayer 共享雲端 session**：同事可中途走進進行中的 session 而 context 不蒸發。Steinberger 稱自家團隊已改用共享環境，把本機 harness 叫作「relics of the past」——此為其公開表態，非中立評估。
- **Control UI 重寫**：以對話為中心（過去是獨立 Overview 頁），檔案、Git diff、PR 狀態、瀏覽器面板、終端機都圍著對話。

## 核心分歧：skill 複利的「放手程度」

兩者現在做的是同一件事——**把成功經驗萃取成可重用的 skill**——但把關形狀相反：

| | OpenClaw 2.0 | Hermes |
|---|---|---|
| 觸發 | 大量工作與持久性糾正可產生改進提案；亦可顯式 `/learn` 或掃描過往工作 | 完成 5+ 次工具呼叫的複雜任務、解錯、被使用者糾正、發現非顯而易見流程 |
| 落地 | **提案 → 人工審查 → apply／reject／quarantine**，決策綁定當時審過的那個修訂版，後續修訂需重審 | **預設免人工核准即可寫入** |
| 治理 | 可選背景審查；週排程 job 回顧整批 skill、記錄使用與結果、保留專門化 skill、做可還原備份 | Autonomous Curator 評分、合併重疊、封存過時、保護 pinned skill、寫每輪報告 |

也就是說：**Hermes 自動化程度更高、把關更弱；OpenClaw 2.0 自動化較保守、把關更嚴**。OpenClaw 的「提案—審查—留痕」模型，與本 vault `vault-lint` 的做法（agent 自主修，但需使用者決策的進 `BACKLOG.md` 並保留去重錨點）同構；Hermes 那種放手模式在本 vault 早有標記的風險——背景 skill-review agent 曾產生非預期副作用，見 [[Hermes-Agent]] 的待查風險。

另一條 Hermes 獨有的軸是 **`llm-wiki` skill**：官方內建、逐字複刻 Karpathy 的 LLM Wiki pattern，也就是本 vault 的同一套方法論（見 [[LLM-Wiki-知識管理模式]]、[[LLM-Wiki-生態實作比較]]）。OpenClaw 的 Memory Wiki 是同名不同源的東西，2.0 之後定位為 built-in Memory 之外「保存人類筆記」的角色，**不宣稱採用 LLM Wiki pattern**——兩者不可混為一談。

## 安全：縮小但未關閉的差距

OpenClaw 的安全預設一直是它最被詬病之處（The Register 對 2.0 的評語直接是「在悶燒中的安全垃圾場上撒亮粉」）。2.0 補了不少：

- approval 綁定到確切的 request／command／session／人，第一個有效回答即定案，重連不能復活已結案的請求。
- 命令權限可綁定**確切參數與工作目錄**，script-backed 命令會重驗當初審過的位元組。
- 每個 session 可選 read-only／guarded／workspace／full，full 限管理員；per-turn 限制只能收緊不能放寬。
- team-scoped **Secret Store** 區分 Protected 與 agent-readable：受保護憑證可注入 Gateway 託管的 HTTPS 請求，而**不進入模型可見文字**。
- Docker／Podman 沙箱。

但兩個限制未變：**沙箱與 approvals 預設仍為關閉**（要人主動去開）；官方明講 **一個 Gateway = 一個信任域**，opt-in 的角色機制是「同一個受信任安裝內的協作限制」，不是互不信任者之間的隔離牆。真要租戶隔離得開多個 Gateway（稱為 cells）。Hermes 的差異化賣點之一正是「安全預設不假設只有你會碰這台機器」〔Decrypt 綜述，未獨立查證〕。

## 該選哪個

- **要生態、通道廣度、UI 成熟度、多人協作** → OpenClaw。ClawHub 有發布者／版本／安全稽核（Safe／Review／Blocked）契約，plugin 與 MCP 管理進了 Control UI。
- **要自我進化的深度、較保守的安全預設、內建 LLM Wiki 式知識庫** → Hermes。
- 一句話：**OpenClaw 贏在生態與廣度，Hermes 贏在自我進化與預設不外露**〔Decrypt 稱此為「全年流傳的普遍評價」，屬業界口耳而非測量結果〕。2.0 之後 OpenClaw 把 skill 自我改良補齊，但形狀是「有審查的建議系統」，不是 Hermes 那種放手讓 agent 自己長。

遷移成本不對稱值得一提：OpenClaw 2.0 的匯入路徑**可以從 Claude Code、Codex、Hermes 帶記憶進來**（僅記憶，不掃憑證、設定、skill 或任意供應商檔案），Hermes 則有 `hermes claw migrate` 反向匯入 OpenClaw。兩邊互通，鎖定風險低。

## 關聯

- 原始資料：[[OpenClaw-2.0-Release-Notes]]（一手）；Hermes 側見 [[Hermes-Agent-NousResearch]]、[[Hermes-Agent-Kanban]]
- 實體頁：[[Hermes-Agent]]——本頁的 Hermes 側全部取自該頁，機制細節不在此重述
- 記憶架構光譜：[[Claude-Code-記憶系統六層比較]]——OpenClaw 的記憶模式即該頁 Level 3 的來源；[[Agent-記憶兩大路線-知識庫與-memory-bank]] 提供「知識資產複利 vs. 工作記憶」的分軸，OpenClaw 的 built-in Memory 偏後者、Memory Wiki 偏前者
- 抽取式記憶的失效證詞：[[Mem0]] 頁記有一則 OpenClaw 圈內人棄用 Mem0、回到 markdown 與 prose 摘要的經驗——與本頁 OpenClaw 記憶走 markdown-first 的取向一致（該頁把該證人記為「OpenClaw 作者」，但 OpenClaw 的作者是 Peter Steinberger，身分歸屬待查，引用前回查 HN 原串）
- harness 框架脈絡：[[Agent-Harness-Engineering-框架綜述]]
