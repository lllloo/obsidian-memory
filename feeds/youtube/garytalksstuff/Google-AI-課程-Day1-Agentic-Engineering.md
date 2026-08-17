---
title: 15 分鐘看完 Google Vibe Coding / Agentic Engineering 開發課 Day 1
description: 從 vibe coding 到 agentic engineering 的光譜、context 六型與 Agent = Model + Harness 拆解
created: 2026-08-17
updated: 2026-08-17
source: https://www.youtube.com/watch?v=GzHfE50N8x4
published: 2026-07-10
parent: "[[01.index]]"
tags:
  - youtube
  - ai-engineering
  - context-engineering
  - harness
  - token-optimization
  - best-practices
---

背景數據：85% 的專業開發者在用 AI coding agent，41% 的新 code 是 AI 寫的。Google 上線了一套五天的 AI 開發課程，第一天講義就有 51 頁，把業界正在收斂的共識寫成正式框架。

## Vibe Coding 與 Agentic Engineering 是一條光譜

2025 年 2 月 Karpathy 貼文描述 vibe coding：完全順著感覺走，用自然語言描述需求、不看任何 code，遇錯就把錯誤訊息複製給 AI 自己修。這個詞爆紅後被濫用到什麼都能講，反而什麼都說不清楚，所以 2026 年初 Karpathy 又補了 agentic engineering 來描述有紀律的那一端。

課程的第一個核心主張：這兩者不是二選一的開關，而是一條光譜，上面有三個位置——vibe coding、structured AI-assisted coding、agentic engineering。判斷標準不是你用不用 AI，而是 **AI 的輸出周圍有多少結構、驗證與人類判斷**。

| 面向 | Vibe Coding | Agentic Engineering |
|---|---|---|
| Intent 規格化程度 | 隨口的自然語言 prompt | 正式 spec、架構文件、memory files |
| 驗證方式 | 看起來會動 | 自動化測試、CI/CD gates、LLM judges |
| 錯誤處理 | 貼錯誤訊息回去叫 AI 修 | agent 在定義好的邊界內自我診斷，人只處理架構層級問題 |

站在光譜哪個位置沒有對錯，看使用場景與出錯風險：週末做 prototype 純 vibe coding 完全合理，跑壞就重來；處理金流的 production API 就必須走 agentic engineering。

兩端最大的分水嶺是**驗證**，而驗證有兩種：

- **Tests**：驗證確定性的部分——這個 function 給這個輸入就該吐這個輸出。
- **Evals**：驗證非確定性的部分——agent 走的路徑對不對、工具選得對不對、產出有沒有到品質標準。

Google 講得很死：沒有這兩樣東西，不管 prompt 寫得多精緻，你做的都還是 vibe coding。

## Context Engineering：比 Prompt Engineering 更關鍵

想往 agentic engineering 移動，練的不是把 prompt 寫得更漂亮，而是 context engineering。可以想成幫新員工做入職簡報——你不會只丟一句「幫我把功能做出來」，而會說明任務、專案背景與公司規範。關鍵提問是：一個新加入團隊的工程師需要知道什麼才能有效貢獻？我又要怎麼把這些知識編成 AI 能用的形式？

Context 分六種：

- **Instructions**：定義 agent 的角色與邊界
- **Knowledge**：領域知識
- **Memory**：短期與長期狀態
- **Examples**：行為示範
- **Tools**：可呼叫的工具定義
- **Guardrails**：硬性約束

這六種又分為兩類：

**Static context**——每次一定載入，如系統指令、`AGENTS.md` / `CLAUDE.md` 這類 rule files。優點是可靠，agent 不用自己去找；缺點是貴，不管什麼問題都要載入、載入就燒 token。

**Dynamic context**——按需載入，如 skills、RAG 撈回的文件、工具執行結果。優點是便宜、可擴展，需要才付錢；風險是該去抓的時候沒去抓。

哪些放 static、哪些放 dynamic，這條邊界本身就是關鍵的架構決策，要像 code 一樣被 review、被版控。

**管理 dynamic context 最強的 pattern 是 Agent Skills**。與其把所有專業知識塞進 system prompt，不如讓 agent 平常保持通用型、需要時再讀取 skill 變成特定任務專家。這個機制叫 **progressive disclosure**：啟動時只看到每個 skill 的一行 metadata，任務匹配才載入完整指令，需要深層參考資料才去拉。結果是一個 agent 可以帶著幾十種專業能力，但只為正在用的那一個付 token。

作者補充兩點：

1. **Skills 有複利效應**：做一個每天用得到的 skill，發現產出不如預期就回頭改，一個月後會比一開始好用非常多。不要想著一步到位。
2. **要寫得 agent 友善、人類可維護**：一個任務可能調用好幾份 skill，產出走歪時你要有能力找出是哪一份把 agent 帶偏。不要寫一份一萬行的 skill，你連看都看不完。

## SDLC 被壓縮，以及工廠模型

軟體開發生命週期（需求、設計、實作、測試、部署、維護）因 AI 被壓縮，但壓得很不均勻：實作從幾週變幾小時，需求訪談、架構決策、驗證品質大多仍是人的速度。所以不是舊流程被加速，而是誕生了新流程——階段之間邊界變模糊、迭代週期從週變分鐘、**spec 的品質變成新的瓶頸**。

- **需求階段**：從文件在部門間傳遞變成人跟 AI 的對話。訪談仍要人談，但談完 AI 幾分鐘就能生出 spec 與初版 prototype。
- **架構階段**：最頑固的人類階段。架構決策本質是 trade-off（一致性還是可用性、自己做還是買現成），依賴商業脈絡，AI 抓不到全貌。AI 擅長的是架構定案後的執行。
- **實作階段**：業界調查說生產力提升 25–39%，但 METR 有研究發現資深工程師用 AI 做某些任務反而慢了 19%，因為時間都花在驗證與修正 AI 產出。兩個數據不衝突：AI 不是消滅實作工作，而是把實作從「寫」變成「review、引導、驗證」。
- **維護階段**：最被低估。以前那種沒人敢動的 legacy code，現在 agent 可以讀懂整個 codebase、理解 pattern、在尊重既有架構下動手改。框架遷移、更新過時 API、現代化測試這些以前風險太高的事，現在可以著手翻修。

Google 給的心智模型是 **factory model（工廠模型）**：把開發流程想成一座工廠，你是工廠經理。經理不親手組裝零件，而是設計產線、把關品質。**開發者的主要產出不再是程式碼，而是產出程式碼的系統**——包含 spec 與 context、負責實作的 agents、驗證正確性的測試與品質關卡、把失敗導回修正的 feedback loops、約束行為的 guardrails。你給 agent 的是 success criteria，不是 step-by-step 指令。

## Agent = Model + Harness

很多人把 model 當成系統本身：新 model 出來就覺得 agent 變聰明，用舊 model 就覺得變笨。這個觀念是錯的，而且會讓你把時間投資在錯的地方。

一顆 raw model 不是 agent。它要有 harness 給它狀態、給它執行工具的能力、給它 feedback loop、給它可執行的約束，才變成 agent。你用 Claude Code、Cursor、Codex 感受到的行為差異，很大一部分是 harness 決定的。

如果 context engineering 是新員工的入職簡報，harness engineering 就是整間公司的運作方式——IT 基礎設施、工作流程規範、門禁、績效評估系統，入職簡報只是其中一環。

**Harness 六大件**：

1. **Rule files**：定義 agent 是誰、在乎什麼、什麼絕對不能做
2. **Tools**：可呼叫的 function、MCP servers，以及什麼時候該用哪個的說明
3. **Sandbox**：code 在哪裡跑，能摸到什麼、摸不到什麼
4. **Orchestration**：sub-agent 調度、model 之間的路由、專家之間的交接規則
5. **Hooks**：在生命週期固定點跑的確定性 code，例如 commit 前自動擋掉硬編碼的密碼。放的是那些 agent 不該忘卻常常忘的事
6. **Observability**：logs、traces、evals、成本監控。沒有這層，你不知道 agent 是做得好還是在偷偷浪費你的錢

**兩個佐證案例**：Terminal Bench 2.0 這個硬派 coding agent benchmark，有團隊完全不換 model、只改 harness，成績從 30 名以外拉進前 5 名；LangChain 的實驗則是同一顆 model，只調 system prompt、tools 與 middleware 就加了 13.7 分。

**大部分 agent 失敗都是 configuration 問題**。出包時第一反應是怪 model、打開排行榜想換一顆，但真正原因通常是缺一個工具、一條規則寫得太模糊、少一個 guardrail，或 context 塞滿雜訊。

實務習慣建議：agent 出包時不要修完 bug 就走，多花五分鐘回頭問「我的 rules、workflows、skills 哪裡可以改，讓這種錯誤不再發生」，把答案寫回 harness。每跑一輪系統就更可靠一點，錯誤從成本變成資產。**model 你控制不了，harness 是你唯一能控制也最值得投資的地方。**

## 人的角色：Conductor 與 Orchestrator

Google 認為人會在這兩種模式間來回切換：

**Conductor（指揮家）**：在 IDE 裡看著 code 一行行出現，隨時下指令、隨時修正，每一步都在掌控裡。適合複雜邏輯、棘手 debug、不熟的 codebase——這些情境你需要理解每一個改動。

**Orchestrator**：定義目標後指派任務給 agents，它們在背景平行跑、可能同時處理 codebase 不同部分，你隔段時間回來 review 給方向。適合定義明確的任務、bug fix、照既有 pattern 做的功能、codebase 遷移、測試生成。

Orchestrator 模式需要四項技能：**specification**（把任務定義到 agent 不會誤解）、**decomposition**（拆成 agent 一個 session 能消化的大小）、**evaluation**（快速判斷產出過不過關）、**system design**（設計約束、測試、feedback loop）。

## Token 經濟學：CapEx 與 OpEx

課程用前期投資與營運成本兩個財務概念回答「建 harness、寫 evals 的時間成本值不值得」。

**Vibe coding** 看起來超便宜，前期投資趨近於零，但藏著三個會複利成長的營運成本：

1. **Token 燃燒率**：沒整理過的 context 整包倒進去，然後反覆叫 model 修它自己沒被驗證過的錯，這個低成功率的迴圈每輪都在燒 API 費用。
2. **維護稅**：沒有結構一致性的 AI code，半年後出 bug 要花好幾天逆向工程。
3. **資安補救**：code 生得快漏洞也多，production 環境修一個資安漏洞的成本是設計階段抓到的好幾倍。

**Agentic engineering** 把這套帳反過來：前期要投工程時間設計 API schema、建測試套件、整理 context，CapEx 高，但每個功能的邊際成本大幅下降，因為 AI 是在一座治理好的工廠裡跑，產出天生結構就對、預先測過、符合公司標準。

**Context engineering 不只是技術，它是財務槓桿。** LLM 按送進去的每個 token 收費，把 10 萬 token 的 repo 整包塞進每個 prompt 從 token 效率來說很不友善；一份精準的文件或提示詞會直接拉高 first-pass 成功率，第一次就做對等於省掉整條 trial-and-error 的錢。你不能決定模型費用，但可以用比較少的 token 完成一樣的任務。

## 行動建議

**個人開發者**：

1. 開始建立並維護自己的 `AGENTS.md` 或 `CLAUDE.md`，十行就可以開始（技術棧、慣例、硬規則、workflow）；agent 每做一次你不想再看到的事就加一條規則。
2. 測試跟 evals 在生 code 之前寫——它們是你跟 AI 之間的合約，一份好的測試套件比任何自然語言 prompt 都更能精確傳達意圖。
3. 要上線的 code 每一行都要 review，對「看起來很聰明」的東西保持懷疑，檢查 import 的套件是不是真的存在。
4. 基本功不能忘：debug 方法、系統設計原則都要留著，AI 是放大這些專業，不是替代它。

**帶團隊或規劃公司 AI 轉型**：

1. 把 AI 開發當成工程投資，不是生產力功能。導入 coding agent 卻不配套 evals、observability 與架構標準，只會產出有速度沒品質的 code，技術債堆得比誰都快。
2. 把 harness 當成團隊共用資產：system prompt、skill 庫、eval 套件都要像 code 一樣被版控、被 review、有人維護。建一次之後每個專案都在複利。
3. 人跟 agent 的混合團隊會是常態：人訂方向，agent 負責實作。招募與培養人才的重心會從實作能力移到判斷力——會寫最多 code 的工程師不再是最有價值的，能把 agent 指揮得好的才是。

講義最後一句：Generation is solved; verification, judgment, and direction are the new craft。程式碼產出的效率問題已被解決，驗證、判斷、方向才是新的手藝活。

Model 每幾個月換一代永遠追不完，但你為自己工作流打造的 harness（rules、skills、evals）存在 version control 裡、會複利，model 越換越強你的系統跟著水漲船高。

## 課程其餘四天

- Day 2：agent 工具、MCP 與 A2A
- Day 3：skills、記憶與 context 優化
- Day 4：security 與 evaluation
- Day 5：spec-driven 的 production level 開發
