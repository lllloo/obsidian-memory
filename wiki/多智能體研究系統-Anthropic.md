---
title: 多智能體研究系統（Anthropic）
description: Anthropic Research 功能的 orchestrator-worker 多 agent 架構解剖：subagent 平行動態搜尋、CitationAgent 引用歸屬、prompt 工程八原則、LLM-as-judge 評測與生產可靠性
created: 2026-07-14
updated: 2026-07-14
source: "https://www.anthropic.com/engineering/multi-agent-research-system"
published: 2025-06-13
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - context-engineering
---

# 多智能體研究系統（Anthropic）

Anthropic 官方工程文章，拆解 Claude 的 **Research 功能**如何從原型走到生產。核心是一套 **orchestrator-worker（協調者—工作者）多 agent 架構**：一個 lead agent 規劃並拆解任務，spawn 多個 subagent 平行搜尋，最後由 CitationAgent 補上引用。是第一方（vendor 自陳）的方法論來源，原文落地於 `raw/fetched/Anthropic-Multi-Agent-Research-System.md`。

> 使用者問的「CitationAgent 關於搜尋的方法」其實橫跨兩件事：**搜尋由 subagent 執行**（見〈搜尋方法〉），**CitationAgent 不搜尋、只做引用歸屬**（見〈CitationAgent〉）。本頁兩者都收。

## 架構：orchestrator-worker

1. **LeadResearcher**（用 Claude Opus 4）分析查詢、擬定策略，並**先把計畫存進 Memory**——因為 context window 一旦超過 20 萬 token 會被截斷，計畫必須持久化以免遺失。
2. Lead 依查詢**建立數個 Subagent**（用 Claude Sonnet 4），各帶明確子任務，**平行**探索不同面向。
3. 每個 Subagent 獨立跑 web 搜尋、用 **interleaved thinking** 評估工具結果，把發現回傳給 lead。
4. Lead 綜合結果，判斷是否需要更多研究——需要就再建 subagent 或調整策略，形成**迭代 loop**。
5. 資訊足夠後退出 loop，把所有發現交給 **CitationAgent** 處理引用，最終帶引用的結果回傳使用者。

對比傳統 **RAG 的靜態檢索**（取與查詢最相似的 chunk 一次生成），此架構是**動態多步搜尋**：邊找邊調整、依新發現轉向、分析後才形成高品質答案。

## 搜尋方法（核心）

搜尋是 subagent 的職責，原文歸納出幾條可攜的 heuristic（策略取向而非硬規則）：

- **搜尋的本質是壓縮**：subagent 各自擁有獨立 context window，平行探索問題的不同面向，再把最重要的 token 濃縮回傳給 lead。這種 separation of concerns（各自的工具、prompt、探索軌跡）降低 path dependency，換得更徹底的獨立調查。
- **先廣後窄（start wide, then narrow）**：模仿專家做研究——先鋪陳全景再鑽細節。agent 天生傾向用**過長、過窄的查詢**，結果返回稀少；因此在 prompt 裡要求先下**短而廣**的查詢、評估可得資訊、再逐步聚焦。
- **平行化大幅提速**：兩層平行——(1) lead 一次 spin up 3–5 個 subagent 而非序列；(2) subagent 一次用 3+ 個工具。複雜查詢的研究時間最多**降 90%**。
- **依查詢複雜度調配努力**：把 scaling 規則寫進 prompt——簡單事實查找 1 個 agent、3–10 次工具呼叫；直接比較 2–4 個 subagent、各 10–15 次；複雜研究 10+ 個 subagent 分工。防止對簡單查詢過度投入（早期常見失效模式：對簡單查詢 spawn 50 個 subagent）。
- **interleaved thinking 精煉查詢**：subagent 在拿到工具結果後用交錯思考評估品質、辨識缺口、修正下一次查詢，使其能適應任務。
- **工具選擇是成敗關鍵**：給 agent 明確 heuristic——先檢視所有可用工具、把用途對應使用者意圖、廣泛外部探索用 web、專用工具優先於通用工具。工具描述品質差會把 agent 帶往完全錯誤的路徑。
- **來源品質**：早期 agent 偏好 SEO 最佳化的**內容農場**，勝過權威但排名較低的來源（學術 PDF、個人 blog）；補上來源品質 heuristic 才修正。搜尋結果只是**候選**，agent 仍須讀原頁、保留引用，不能把檢索排序當事實依據。

## CitationAgent（引用歸屬，非搜尋）

研究 loop 結束後，系統把**所有蒐集到的 documents 與 research report** 交給 CitationAgent。它的職責是**找出報告中每個需要引用的具體位置（identify specific locations for citations）**，確保所有主張都正確歸屬到來源，最後把帶引用的結果回傳使用者。

換言之，CitationAgent 是 pipeline 的**專職最後一步**：它不做 web 搜尋、不蒐集資訊，只做**引用歸屬（citation attribution）**。這與評測 rubric 中的 **citation accuracy**（引用的來源是否確實支持主張）直接呼應——把「找資料」與「掛引用」拆成不同 agent，讓引用正確性成為可獨立評測、獨立優化的關卡。

## Prompt 工程八原則

1. **像你的 agent 一樣思考**：用 Console 以真實 prompt/工具模擬，逐步觀察 agent，才能建立準確心智模型、看出失效模式。
2. **教會協調者如何委派**：每個 subagent 需要目標、輸出格式、工具與來源指引、清楚的任務邊界；指令含糊會導致重工或漏洞。
3. **依查詢複雜度調配努力**（同上搜尋節）。
4. **工具設計與選擇至關重要**：agent-工具介面等同人機介面；壞的工具描述會誤導 agent。他們甚至做了會自我改寫工具描述的 tool-testing agent，讓後續 agent 任務完成時間**降 40%**。
5. **讓 agent 自我改進**：Claude 4 能當稱職的 prompt engineer，給它 prompt 與失效模式就能診斷並提出改進。
6. **先廣後窄**（同上搜尋節）。
7. **引導思考過程**：extended thinking 當可控 scratchpad，lead 用它規劃；subagent 用 interleaved thinking 在工具結果後評估與精煉。
8. **平行工具呼叫**（同上搜尋節）。

整體策略是灌輸好的 heuristic 而非死板規則，並設 guardrail 防 agent 失控。

## 評測

- **立刻用小樣本開始**：早期改動效果巨大（成功率可能 30%→80%），約 **20 個代表真實用法的查詢**就能看出變化；別等湊滿數百案例才建 eval。
- **LLM-as-judge 做得好就能規模化**：研究輸出是自由文本、少有單一正解。用一個 LLM judge 依 rubric 評——factual accuracy、citation accuracy、completeness、source quality、tool efficiency。實測發現**單次 LLM 呼叫、單一 prompt、輸出 0.0–1.0 分數加 pass/fail** 最一致、最貼近人判。
- **人評補自動化漏洞**：人測抓到自動化漏掉的邊角（幻覺、系統故障、來源選擇偏見，如前述內容農場問題）。

## 生產可靠性

- **agent 有狀態、錯誤會複利**：長時運行跨多次工具呼叫維持狀態；用 resume（從出錯處續跑，不從頭重啟）+ retry + 定期 checkpoint，並讓模型在工具失敗時自行調適。
- **debug 需新方法**：agent 非決定性，靠 **full production tracing** 與監控決策模式（不看對話內容以保隱私）診斷根因。
- **部署要謹慎協調**：用 **rainbow deployment** 漸進切流量，避免更新中斷運行中的 agent。
- **同步執行造成瓶頸**：目前 lead 同步等待 subagent 完成，簡化協調但阻塞資訊流；非同步可增平行度但帶來狀態一致性與錯誤傳播難題。

## 附錄要點

- **end-state 評測**：對會變更持久狀態的 agent，評「最終狀態是否正確」而非逐步驟，容許不同有效路徑。
- **long-horizon 對話管理**：completed 階段摘要後存外部記憶；近 context 上限時 spawn 乾淨 context 的新 subagent，靠 handoff 維持連續；可從記憶取回研究計畫而非遺失。
- **subagent 直接寫檔案，減少「傳話遊戲」**：subagent 把成果存外部系統、只回傳輕量 reference，避免多階段處理的資訊流失與 token 開銷（尤其結構化輸出如程式碼、報告、視覺化）。

## 關鍵數據與強度標註

- 多 agent（Opus 4 lead + Sonnet 4 subagents）比單一 Opus 4 在內部研究評測**高 90.2%**，優勢集中於可平行的廣度型查詢。（強度：**第一方內部評測、未經獨立複現**，勿當通用結論引用。）
- **token 經濟性**：agent 約耗 chat 4 倍 token，多 agent 系統約 **15 倍**；只在「任務價值夠高」時划算。多數 coding 任務可平行性低，未必適合。（強度：Anthropic 生產遙測、屬自陳成本承認，被多方轉引無爭議。）
- BrowseComp 分析中三因素解釋 95% 表現變異，**單是 token 用量就解釋 80%**，其餘為工具呼叫數與模型選擇。（強度：第一方分析，佐證「多 agent 靠分散 context 擴充平行推理容量」的架構主張。）

## 實作層 prompt（cookbook）

官方 [anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook) 的 `patterns/agents/prompts/` 公開了這套系統的三個實際 prompt，補足部落格未寫的實作細節（逐字內容落地 `raw/fetched/Anthropic-Cookbook-Research-Prompts.md`）。（強度：官方 cookbook 範例 prompt，可能與生產版本有出入，但為第一方公開的實作參考。）

**research_lead_agent（協調者）**——先判 query 類型再定計畫：
- **query 三分類**：depth-first（單一問題多視角，平行探不同觀點／方法）、breadth-first（可拆成獨立子問題，平行各研究一塊）、straightforward（單一聚焦調查即可）。
- depth-first 定 3–5 種方法論視角；breadth-first 列出所有可獨立研究的子任務並劃清邊界防重疊；**預設 3 個 subagent**，依複雜度增減。

**research_subagent（搜尋工作者）**——即〈搜尋方法〉的實作：
- **research budget**：規劃時先估工具呼叫預算，依複雜度分級（簡單 <5、中 ~5、難 ~10、極難 ≤15），超支觸限。
- **OODA loop**（observe–orient–decide–act）迭代；**最少 5 次、至多 10 次**工具呼叫。
- 查詢啟發式：**廣優於窄、每則查詢 <5 字**、太少再放寬／太多再收窄；核心迴圈 `web_search`（拿 snippet）→ `web_fetch`（取全文）；絕不重複相同查詢。
- source quality：要求標註推測語氣（could／may、未來式）、辨識聚合站 vs 原始來源、衝突資訊帶回 lead 裁決。
- **硬上限**：20 次工具呼叫、~100 來源，逼近就 `complete_task`。

**citations_agent（引用歸屬）**——CitationAgent 的真正機制：
- 輸入 `<synthesized_text>`（已綜合但未附引用的報告）＋來源文件；輸出 `<exact_text_with_citation>`。
- **逐字不改**：內容 100% 相同、連空白都不增減——輸出去掉引用標記後與原文**逐字比對，不一致整份 reject**。
- 引用準則：只在來源直接支持處加、引用「完整語意單元」而非片段、優先句尾、同句同源只標一次。
- 印證了架構把「找資料」（subagent）與「掛引用」（citations agent）**拆成可獨立評測的關卡**，對應評測 rubric 的 citation accuracy。

## 交叉引用

- 綜述定位：[[Agent-Harness-Engineering-框架綜述]]——該頁已把本文的 token 經濟性與 long-horizon 技術納入 harness 工程主軸；本頁補上此文**完整的搜尋方法論與 agent 分工細節**。
- 實證對照：[[AI-自主工作流的實證檢驗]]——本文的 resume/checkpoint、end-state 評測正屬其「驗證迴路／狀態持久化」的盤點範疇，可比對 vendor 敘事與獨立實證的落差。
- 檢索範式對照：[[LLM-Wiki-知識管理模式]]——本文「動態多步搜尋 vs 靜態 RAG」與該頁「知識編譯一次持續維護 vs 每次查詢重檢索」是同一組張力的不同切面。
- 記憶機制對照：[[Claude-Code-記憶系統六層比較]]——本文的 external memory／乾淨 context 新 subagent handoff，可對應其記憶分層。
