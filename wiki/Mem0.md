---
title: Mem0
description: AI agent 記憶層工具的整合路徑（plugin／MCP／CLI）、hook 實測消耗與失效模式證據，含本 vault 採 MCP-only 的拍板理由
created: 2026-07-20
updated: 2026-07-20
source: https://github.com/mem0ai/mem0
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - memory
  - mcp
  - claude-code
  - coding-agent
---

# Mem0

雲端 AI agent 記憶層，把對話抽取成「原子事實」存進向量庫，供跨 session／跨工具召回。Apache 2.0 開源＋託管 Platform 的 open-core 模式。本頁是 2026-07-20 多輪查證（deep-research＋5 輪定向補查＋本機 CLI 驗證）的回存，重點在**整合路徑的實際差異**與**失效模式的證據強度**，不是功能介紹。

在 [[Claude-Code-記憶系統六層比較]] 的座標裡它屬 Level 6（跨工具單一大腦）。該頁原稱其「等於租」——**此描述需分層**：軟體本身是真 Apache 2.0、可完全自架（raw LICENSE 檔實查，無 Commons Clause／BUSL 附加）；但**官方整合路徑全部綁雲端**，實際採用體驗確實是租。

## 三條整合路徑

差別**不在能力，在誰觸發記憶**——工具集幾乎一樣。

| | Plugin | MCP-only | CLI |
|---|---|---|---|
| 9 個記憶工具 | ✅ | ✅ | ✅（13 子指令） |
| Lifecycle hooks | ✅ | ❌ | ❌（原始碼無 hook 機制） |
| 觸發 | 自動捕捉 | 全手動 | agent 須主動叫 |
| 後端 | 雲端 only | 雲端 only | 雲端 only |

〔官方文件逐字〕MCP-only 的官方警語是「MCP-only installs require manual memory operations」。**Plugin 與 MCP 不可並用**——plugin manifest 會自動註冊 MCP server，兩邊都加會 tool collision。

CLI（`@mem0/cli`）**不是替代品**：原始碼 `cli/node/src/plugin-sync.ts` 註解寫明設計假設是兩者同裝（CLI 管認證、MCP 管 agent 呼叫）。其 `src/backend/` 工廠函式無條件回傳 `PlatformBackend`，`MEM0_BASE_URL` 可改主機但改不了協定，**無法指向自架後端**〔repo 原始碼〕。

## Plugin hook 的實際消耗（原始碼實測）

官方文件把 hooks 描述成「session start／compaction／task completion／session end」四個觸發點。**原始碼是 7 個事件、9 個 handler**〔`integrations/mem0-plugin/hooks/hooks.json`〕，文件嚴重簡化：

| 事件 | 時機 | 消耗 |
|---|---|---|
| `Stop` | **每個 assistant turn 結束**（非 session 結束） | 1 add（`infer:true`） |
| `UserPromptSubmit` | 每則 ≥20 字元訊息 | 1 search；每 3 則 +1 add |
| `PreToolUse`/`Read` | **每次讀 ≥1.5KB 檔案** | 1 search |
| `PostToolUse`/`Bash` | 輸出含錯誤時 | 2 search |
| `SessionStart` | 啟動／resume／compact 後 | 1 count＋背景 import＋誘發 agent 2 次 search |
| `PreCompact` | 壓縮前 | 1 add |

**「task completion」＝ `Stop`，即每輪回應**，不是粗粒度的任務完成。綁死額度的是 retrieval（免費層 1,000/月）而非 add（10,000/月），因為 agent 讀檔頻率遠高於使用者發話。可關的旋鈕只有 `MEM0_AUTO_SAVE=false`、`MEM0_PREFETCH=false`；**Read 與 Bash 兩條無開關**，只能改 `hooks.json`。

另注意：`/mem0:onboard` 會「Detects and imports project files (`CLAUDE.md`, `AGENTS.md`, `.cursorrules`)」，且**在新專案首次 session 自動觸發**，不是只有手動才跑。Codex 的 hooks 則不會自動生效，需另跑 `install_codex_hooks.py` 並開 `[features] codex_hooks = true`〔repo README 逐字〕。

## Benchmark 宣稱：不可引用

官方數字（LoCoMo 92.5、LongMemEval 94.4、p95 延遲 -91%、token -90%）**全部是廠商自報、未同儕審查**，作者五人皆 Mem0 團隊，baseline 由作者自行實作。README 自承免責：「Scores reflect Mem0's managed platform, which includes proprietary optimizations not available in the open-source SDK」，其自家 benchmark repo 實測 OSS 比託管低 3.4–5.8 個百分點。

**獨立反證方向一致——「不如直接塞完整歷史」**：

- HN `cpluss` 在 MemBench 跑 4,000 案例（harness 開源）：記憶系統「14–77× more expensive... and 31–33% less accurate at recalling facts than just passing the full history」〔獨立第三方 benchmark，單一模型／單一 benchmark〕
- Zep 的重算指 full-context baseline ~73% vs mem0 ~68%〔**競品廠商，利益相關**〕
- [issue #2800](https://github.com/mem0ai/mem0/issues/2800)：多位研究者本地跑 LoCoMo 分數遠低於論文，**連用平台版也拿不到**
- Penfield Labs 稽核 LoCoMo：6.4% 答案 key 有誤、LLM judge 接受最多 63% 的刻意錯誤答案

⚠️ **勿引用**：「p95 延遲降 91%」「token 省 90%」至今零獨立複現。「LongMemEval 63.8% vs 49.0%」在內容農場流傳但追不到原始出處。雙方唯一共識是 **LoCoMo 不足以支撐任何 SOTA 宣稱**。

## 失效模式：核心設計層級，非成熟度問題

最強的一筆是 [issue #4573](https://github.com/mem0ai/mem0/issues/4573)——生產環境 32 天後全量拉出 10,134 筆逐筆審查〔**單一部署 n=1，早期用 gemma2:2b 抽取屬不合理配置，不可外推成普遍比率**〕：

> 224 entries survived... That's 97.8% junk... Only 38 entries were clean enough to keep as-is.

垃圾來源：**system prompt／boot file 反覆重抽 52.7%**、cron/heartbeat 噪音 11.5%、系統架構 dump 8.2%、暫時任務狀態 7.4%、幻覺使用者輪廓 5.2%、隱私外洩 2.1%。**這批分佈是 coding／ops agent 特有的**，聊天機器人場景不會出現。

兩個**機制性**發現不依賴其配置，是本頁最該記的部分：

1. **換更強的模型救不了**——「A better model follows the extraction prompt more faithfully, which means it extracts more indiscriminately. **The extraction prompt is the bottleneck, not the model.**」
2. **幻覺會自我複製**——召回的記憶被當成新輸入再抽一次，形成放大迴圈：808 筆「User prefers Vim」（191 筆逐字重複），系統裡沒人用 Vim，源頭是一次幻覺。「Any hallucination that gets stored once will be re-extracted indefinitely.」

其他結構性缺陷〔GitHub issue 實證〕：[#4956](https://github.com/mem0ai/mem0/issues/4956) v3 變 ADD-only 不再發 UPDATE/DELETE，矛盾事實共存且檢索不含 recency；[#5330](https://github.com/mem0ai/mem0/issues/5330) 原生無 TTL／decay（2024 Show HN 就有人問，至今無解）；[#4926](https://github.com/mem0ai/mem0/issues/4926) 必須永遠生效的約束走 cosine 排名可能擠不進 top_k，那些該進 system prompt；[#3695](https://github.com/mem0ai/mem0/issues/3695) **託管版** `delete_all()` 從 dashboard 移除但 search 仍撈得到；[#2813](https://github.com/mem0ai/mem0/issues/2813) 每次 add 都等 LLM 抽取，20 秒以上是設計非 bug。

唯一乾淨的棄用證詞是 OpenClaw 作者 `endymi0n`〔[HN](https://news.ycombinator.com/item?id=47770220)，單一開發者經驗、非實證〕：「stopped using it very soon... after the third injected wrong fact I went back to QMD and prose / summarization」。其失敗模式對「只記簡單內容」的用法特別重要——**內容簡單不等於抽取不出錯**：反諷被字面抽取（跟胖朋友開六塊肌玩笑 →「interested in achieving an athletic form」）、連抽一個明確日期都常錯。

## 資訊生態污染警告

搜「mem0 best practices」第一頁幾乎全是廠商內容（`mem0.ai/blog`、`mem0.ai/compare/*` 整批 SEO 對打頁）與 AI 生成內容農場，互抄同一組數字、敘事結構雷同、無可驗證的第一手部署細節。**有價值的獨立來源只有三處：GitHub issues、Hacker News、少數個人 blog。** 查 mem0 相關主張時直接去這三處，別信搜尋結果第一頁。

同理，**官方文件本身也不可盡信**：整合索引頁漏列 Claude Code／Codex（頁面實際存在，見 `llms.txt`）、`codex mcp add` 是否支援 HTTP 兩頁互相打臉（本機 `--help` 證實**支援**，文件那句「only supports stdio」是錯的）、hook 數量文件說 4 個原始碼是 9 個。**優先信 CLI `--help` 與 repo 原始碼。**

## 本 vault 的拍板（2026-07-20）

採 **MCP-only、不裝 plugin**，定位為**全域隨手記的收件匣**（跨機器、簡單紀錄），嚴謹知識仍走本 vault。理由：

- Plugin 的自動捕捉正是 #4573 垃圾來源前三名（system prompt／cron／架構 dump）的成因；MCP-only 手動叫則不產生這三類
- 兩者不爭權威，層級不同——有內容值得長期保存再手動搬進 wiki，同 cards/topics 的人工撿選模式
- 現有 `ask-vault` 已解決「跨專案查詢累積知識」且已 cross-CLI；mem0 補的真缺口只有兩個：**寫入**（ask-vault 唯讀）與**沒有 vault 的機器**

已接受的代價：`infer:true` 的抽取可能扭曲原文（見上 `endymi0n` 條）。因屬隨手記、vault 才是權威，此代價可接受。

`--scope user` 為跨專案必要（`claude mcp add` 預設 `local`）；header 用單引號讓 `${MEM0_API_KEY}` 存為變數參照而非明文烤進設定檔。

⚠️ **一個類別錯置的釐清**：[[OpenSpec]] 不是 mem0 的整合對象。它不是 agent host（不跑 MCP／不裝 plugin），而是**裝進** host 的 workflow 框架（`docs/supported-tools.md` 逐字：「Codex is skills-only: OpenSpec installs `.codex/skills/openspec-*/SKILL.md`」）。兩者若同在一個 host，是**爭同一個位置**——OpenSpec 用 checked-in 可 review 的 spec 檔決定 agent 該遵守什麼，mem0 用雲端不可 review 的記憶做同件事，權威來源會分裂。查無任何 mem0×OpenSpec／spec-kit 的 prior art。

## 相關頁

- [[Claude-Code-記憶系統六層比較]] — mem0 在儲存／召回光譜上的 Level 6 定位；本頁是該頁那格的展開與證據補強
- [[Agent-記憶兩大路線-知識庫與-memory-bank]] — 本頁「隨手記 vs 嚴謹知識」的分工，正是該頁 A／B 兩路線分野在單一工具上的落地
- [[LLM-Wiki-生態實作比較]] — mem0 自家 repo 的 [discussion #4051](https://github.com/mem0ai/mem0/discussions/4051) 有人（自稱 mem0 fan）推薦 `MEMORY.md`＋git 作輕量替代，與本 vault `schema/MEMORY.md` 近乎同構；其自劃界線值得記：該路在「大量語意檢索」會斷，在「agent 接上進度」剛好
- [[OpenSpec]] — 上述類別錯置的另一方
