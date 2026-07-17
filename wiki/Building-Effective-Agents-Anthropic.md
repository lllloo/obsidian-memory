---
title: Building Effective Agents（Anthropic）
description: Anthropic 建 agent 的基礎指南：workflows 與 agents 之分、augmented LLM 基石、五種 workflow 編排模式（含各自適用時機），與 ACI／工具 prompt engineering 實務、由簡入繁三原則
created: 2026-07-14
updated: 2026-07-17
source: "https://www.anthropic.com/engineering/building-effective-agents"
published: 2024-12-19
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - context-engineering
---

# Building Effective Agents（Anthropic）

Anthropic 2024 年底的基礎工程文章，是 [[Agent-Harness-Engineering-框架綜述]] 第 1 節的來源，也是 workflows／agents 二分法的原始出處。核心主張：與數十個團隊合作的觀察是，**最成功的實作不靠複雜框架或專用函式庫，而靠簡單、可組合的模式**——「由簡入繁，只在複雜度能實證改善結果時才加」。原文落地於 [[Anthropic-Building-Effective-Agents]]（raw）。（強度：全文為 vendor 觀察性經驗宣稱，非受控實證；架構定義部分已成術語共識，見文末。）

## workflows vs agents

Anthropic 把凡涉及 LLM 動態運作的系統統稱 **agentic systems**，但劃一條架構分界：

- **Workflows**：LLM 與工具經**預先定義的程式碼路徑**編排——路徑固定、可預測。
- **Agents**：LLM **動態指揮自身流程與工具使用**，對「如何完成任務」保有控制權。

此二分被 Spring AI 官方文件、Simon Willison 等廣泛採納，2026 年仍是標準分類（詳見綜述頁）。

## 何時該用（與不該用）

- 建議**先找最簡單的解**，只在需要時才加複雜度——很多時候根本不必建 agentic system。agentic system 常以延遲與成本換取更好的任務表現，要評估這個 trade-off 是否值得。
- 需要更多複雜度時：**workflow** 給定義明確的任務可預測性與一致性；**agent** 適合需要規模化的彈性與模型驅動決策。
- 但對許多應用，**單次 LLM 呼叫＋檢索＋in-context 範例**就夠了。

## 何時（與如何）用框架

點名 Claude Agent SDK、AWS Strands、Rivet、Vellum 等。框架簡化呼叫 LLM／定義解析工具／串接呼叫這類低階雜事，但**多疊一層抽象會遮蔽底層 prompt 與 response、更難 debug，也誘使人在該用簡單解時加複雜度**。建議：**先直接用 LLM API**（許多模式幾行程式就能實作）；若用框架，務必理解底層程式碼——對「引擎蓋下發生什麼」的錯誤假設是客戶出錯的常見來源。

## 基石：augmented LLM

agentic system 的基本建構塊是一個被 **retrieval、tools、memory** 增強的 LLM——模型能自己生成搜尋查詢、選工具、決定保留什麼資訊。兩個實作重點：**針對用例裁剪這些能力**，並**給 LLM 一個易用、文件完備的介面**。MCP（Model Context Protocol）是整合第三方工具生態的一種方式。後文假設每次 LLM 呼叫都具備這些增強能力。

## 五種 workflow 編排模式

由簡入繁，每種都附「何時用」：

1. **Prompt chaining**：把任務拆成一連串步驟，每次 LLM 呼叫處理前一次的輸出；可在中間步插入程式化 **gate**（檢查點）確保仍在軌道上。**何時用**：任務能乾淨拆成固定子任務時；用延遲換更高準確度（每次呼叫更簡單）。例：先寫行銷文案再翻譯；先寫大綱、檢查大綱達標、再依大綱寫全文。
2. **Routing**：分類輸入並導向專門的後續任務，達成關注點分離、建更專門的 prompt。**何時用**：有明確類別、各自分開處理更好、且分類能被準確執行時。例：客服分流（一般問題／退款／技術支援）；簡單常見問題導向便宜小模型、困難罕見問題導向更強模型。
3. **Parallelization**：LLM 同時處理任務、輸出以程式聚合，兩變體——**Sectioning**（拆成獨立子任務平行跑）、**Voting**（同任務多次跑取多元輸出）。**何時用**：子任務可平行加速，或需多視角／多次嘗試提高信心時。例（sectioning）：一個實例處理查詢、另一個篩不當內容；一次評測跑多個面向。例（voting）：多個 prompt 各查程式漏洞；不同投票門檻平衡誤報漏報。
4. **Orchestrator-workers**：中央 LLM 動態拆解任務、委派給 worker LLM、綜合其結果。**與 parallelization 的關鍵差異**：子任務**非預先定義**，而由 orchestrator 依具體輸入決定。**何時用**：無法預測需要哪些子任務時（如 coding：要改幾個檔、各檔怎麼改視任務而定）。例：對多檔做複雜變更的 coding 產品；多來源蒐集分析的搜尋任務。
5. **Evaluator-optimizer**：一個 LLM 生成回應、另一個在 loop 中評估並給回饋（即 generator-evaluator 迴路原型）。**何時用**：有明確評測準則、且迭代精煉帶來可衡量價值時——徵兆是「人能articulate回饋讓回應變好」且「LLM 能給這種回饋」。例：文學翻譯的細膩度；需多輪搜尋分析的複雜檢索（由 evaluator 決定是否再搜）。

## Agents

agent 通常就是**在 loop 中依環境回饋使用工具的 LLM**：從人的指令或互動討論起步，任務明確後自主規劃與運作，必要時回頭找人；執行中每步都要從環境取「ground truth」（工具結果、程式執行）評估進度，可在 checkpoint 或遇阻時暫停等人回饋。**何時用**：開放式問題、難以預測所需步數、無法寫死固定路徑、且你對其決策有一定信任時；autonomy 適合在**受信任環境**中規模化任務。代價是**更高成本與錯誤複利**，故建議在 sandbox 充分測試並加適當 guardrail。例：解 SWE-bench 任務的 coding agent、computer use 參考實作。

> **設計哲學**：這些建構塊不是規範，是可塑可組合的常見模式。成功關鍵是量測表現並迭代——**只在複雜度能實證改善結果時才加**。

## 三個核心原則

實作 agent 時遵循：

1. 保持設計的**簡單性（simplicity）**。
2. 優先**透明性（transparency）**——明確顯示 agent 的規劃步驟。
3. 用完善的工具文件與測試，精心打造 **agent-computer interface（ACI）**。

## 應用域（附錄一）

兩個特別有價值的應用，共同點是**同時需要對話與行動、有明確成功準則、能形成回饋迴路、且有意義的人類監督**：

- **客服**：對話流天生契合開放式 agent；工具拉取客戶資料／訂單／知識庫，退款／改單可程式化執行，成功可由「使用者定義的解決」明確衡量。已有公司採「僅對成功解決收費」的用量計價，顯示對成效的信心。
- **coding agent**：程式解可由**自動測試驗證**、agent 能以測試結果為回饋迭代、問題空間結構良好、輸出品質可客觀衡量。Anthropic 自家實作已能僅憑 PR 描述解 SWE-bench Verified 的真實 GitHub issue；但自動測試驗功能之餘，**人審對「解是否合乎更廣系統需求」仍關鍵**。（強度但書：SWE-bench Verified 這條「輸出可客觀衡量」的佐證本身有雜訊——OpenAI 後來審計發現該 benchmark 59.4% 題目有實質缺陷、35.5% 測試過嚴，見 [[AI-自主工作流的實證檢驗]]；「可客觀衡量」在原則上成立，但不宜把單一 benchmark 分數當效果鐵證。）

## ACI：為工具做 prompt engineering（附錄二）

無論建哪種 agentic system，工具多半是要角。核心類比：**投入多少心力在人機介面（HCI），就該投入多少在 agent-computer interface（ACI）**——工具定義與規格值得跟整體 prompt 一樣多的 prompt engineering。

- **格式選擇有實質差異**：同一動作常有多種表達（改檔用 diff vs 重寫整檔；結構化輸出用 markdown vs JSON），對人是外觀差異、對 LLM 難度天差地別——寫 diff 要先知道 chunk header 的行數變化；JSON 內寫程式要多做換行與引號跳脫。準則：給模型足夠 token「思考」再落筆、格式貼近網路上自然出現的樣子、避免格式「開銷」（如精確計算數千行、跳脫字串）。
- **把工具當給 junior 開發者的 docstring 寫**：設身處地想「光看描述與參數，用法明顯嗎」；好的工具定義含用法範例、邊角案例、輸入格式要求、與其他工具的清楚界線。用 workbench 跑大量範例看模型犯什麼錯再迭代；**poka-yoke**（防呆）你的工具——改參數讓犯錯更難。
- **實證**：建 SWE-bench agent 時，**優化工具花的時間比優化整體 prompt 還多**。例：agent 移出 root 目錄後用相對路徑會出錯，改成**強制絕對路徑**後模型使用完美無瑕。

## 強度標註

- 全文為 **vendor 第一方觀察性經驗宣稱**（「與數十個團隊合作」），非受控實證、無量化 benchmark；作為方法論指引與術語定義適格，作為「效果有多大」的證據不適格。
- **workflows/agents 二分與五種模式的命名**已成產業術語共識（Spring AI、Simon Willison 等轉引），這部分穩定度高。
- **時效風險**：文中點名的具體模型（Haiku 4.5／Sonnet 4.5）與框架清單（Claude Agent SDK、AWS Strands 等）是 Anthropic 於後續改版時更新的內容，非 2024-12 原文原貌；模式本身與版本耦合度低，模型與框架名僅為示意，勿當固定事實。

## 交叉引用

- 挑選視角：[[Agent-工作流-Pattern-藍本庫]]——該頁把本文五模式當**骨架**（並據原文「These building blocks aren't prescriptive」明確標為非完整分類法），補上本文沒有的 CSIRO Data61 18-pattern catalogue、OpenAI 的 Manager/Decentralized 二分與 ReAct／Reflexion／Self-Refine 的論文出處；設計新 skill 要挑 pattern 時讀該頁，要本文完整原貌讀本頁。
- 綜述定位：[[Agent-Harness-Engineering-框架綜述]]——該頁第 1 節簡述本文的二分法與五模式並置於 harness 工程時間線最前端；本頁補上綜述未收的 **augmented LLM 基石、各模式適用時機、兩個應用域、ACI／工具 prompt engineering** 完整內容。
- 模式的規模化實例：[[多智能體研究系統-Anthropic]]——該系統正是本文 **orchestrator-workers** 模式的生產級落地（lead 動態拆解、平行 subagent、綜合結果），可對照「模式原型」與「實作細節」兩層。
- 實證對照：[[AI-自主工作流的實證檢驗]]——本文「只在複雜度能實證改善時才加」「用測試結果當回饋迭代」的主張，該頁以獨立證據檢驗其邊界（測試本身可被 agent 篡改，驗證迴路必要但不充分）。
- 記憶／context 對照：[[Claude-Code-記憶系統六層比較]]——本文 augmented LLM 的 memory 增強，是該頁記憶分層的最小前身。
- 判準延伸：[[Context-優先與多-agent-的適用邊界]]——把本文「由簡入繁」原則落成可操作的決策清單，並補上「加複雜度（多 agent）實測會怎麼壞」的獨立證據（Cognition、MAST）。
- evaluator-optimizer 落地：[[設計品質的可量化檢測]]——該頁把本文 **evaluator-optimizer** 的「生成→評估→回饋」迴路落到設計品質領域，用可執行、客觀的 evaluator（自動化檢測）撐起「報告→修正→重跑」閉環，是本文抽象模式在特定領域的具體落地案例。
- 二分法定位引用：[[pi-workflow-編排-harness-與本-vault-分野]]——該頁以本文 workflows／agents 二分法與五種編排模式，把 pi-workflow 定位為路徑固定的 **workflow**（`foreach`＋`reduce` 屬 parallelization），對照 orchestrator-workers 的子任務動態委派。
