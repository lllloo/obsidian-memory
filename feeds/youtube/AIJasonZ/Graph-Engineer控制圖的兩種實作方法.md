---
title: 我不再自己 prompt agent 了——Graph Engineer 的實作方法
description: 拆解網路上混談的三種 graph，聚焦控制圖（control graph），並示範 LLM as graph 與 code as graph 兩種落地方式與設計模式
created: 2026-08-31
updated: 2026-08-31
source: https://www.youtube.com/watch?v=_9OT25ZvrWs
published: 2026-08-25
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - claude-code
---

## 「graph engineer」其實混了三個不同概念

近期網路上 graph engineer 一詞爆紅，混淆主因是大家把三種完全不同的東西塞進同一個討論：

- **控制圖（control graph）**：LangGraph、dynamic workflow，或單純寫成文字的 SOP。多數 agentic 任務背後都有一套 SOP，控制圖是讓 agent 產出更可靠結果的手段。作者判斷 Peter 推文（「我們還在談 loop，還是已經轉向 graph 了？」）指的是這個——他描述的案例是「把一個變更 ship 進 codebase」的控制流程。
- **知識圖譜（knowledge graph）**：完全不相干的概念，只因為 Andrew Ng 剛好推出一小時的 agentic knowledge graph 課程而被連在一起。它是用來表達實體之間的關係，讓資料檢索更有效；agent memory 領域用 graph 已經好幾年了。
- **graph of loops**：假設未來公司由一堆 loop 在跑，如何確保這些 loop 都執行良好且持續改進。單一 loop 就已經很難，多個 loop 一起跑時錯誤與改進都會快速複利。這是全新且未被探索的領域，目前沒有真正的答案——多數團隊連一兩個 loop 都還沒成功建起來。

本片聚焦控制圖，因為以多數公司目前的位置來看，它的實用性最廣。

## 為什麼現在才需要控制圖

最大的轉變是：從「人 prompt agent」變成「某個東西代替人去 prompt agent」。目前最 AI native 的公司在試兩種模式：

- **Loops**：不再由人針對每個任務下 prompt，而是設好 trigger 去 prompt agent。trigger 可以是時間型（每天拉最新 GitHub issue 來修）、目標型（持續優化前端直到效能提升 200%）、或事件型（每封信進來就喚醒 agent）。每個 loop 最重要的設計，是界定哪些事 agent 可自理、哪些必須拉人進來。
- **Orchestrator 模式**：人不再對個別 agent 講話，而是對一個掌握全局 context 的 orchestrator agent 講話，由它開一組 agent 去實際執行並監控過程。Claude Code 作者 Boris 也提過，他現在大多是跟一個 Claude 講話、由它去跟其他 Claude 講話；任何時刻至少有幾個 agent 在跑，常常整夜跑上幾千個 agent 做複雜工作——這在三個月前還不可行。

兩種模式的共同點是**把人拉高一層**，不再逐步盯 executor agent 的每個 checkpoint。正因如此，可靠性變成敢不敢採用的關鍵，這也是作者一再強調至少要在 codebase 裡設一個 verifier 的原因（其 GitHub repo 有 setup verifier skill 可直接拿）。但 verifier 只是護欄的一小部分，不同業務流程需要注入不同的護欄與 SOP——控制圖就是在講這件事。

## 控制圖的三要素與「node 的意義變了」

graph-based workflow automation 已存在數十年，三個組件不變：

- **node**：要執行的動作
- **edge**：每個 node 之後接什麼
- **state**：在各步驟間被帶著走的資料

真正變的是 node 可以是什麼。傳統自動化裡 node 是跑一段 script 或做條件判斷；約三年前平台開始允許把 LLM 當成一個 node 以處理長尾情境；最近 node 本身可以是一個能做很多事的 agent。

幾個你其實已經在用的 graph 例子：

- **Claude Code / Codex 的 goal 功能**：接使用者 prompt → 跑 agent loop → 結束時由 LLM 判斷目標是否達成 → 達成就結束，未達成就回送新訊息給 agent。實作方式是 agent loop 加上 stop hook 系統。
- **Andrej Karpathy 的 auto research 專案**：把 agent 放進 for loop 持續改進語言模型。流程寫在一個 program 檔裡：指示 agent 用一個實驗性想法去改 `train.py`，跑實驗、評估結果，好就保留、不好就丟掉換下一個。state 就兩樣東西——被改動的 `train.py`，以及記錄所有嘗試的 `results.tsv`。有趣的是這個 graph 純粹靠 prompt 達成，沒有任何花俏機制，當時甚至還沒有 loop 或 goal 功能，就只是叫 agent 一直重複這個流程，它就做了。
- **Deep research**：接 prompt → orchestrator 規劃要涵蓋哪些主題 → fan out 一批 sub-agent 各自研究 → 收回後 review 資訊是否足夠 → 不夠就回上一步，夠了就產報告。

結論：**graph 的實作不一定要是程式碼**，可以只是一份寫下來的 SOP、一組預先定義的 script 與邊界。

## 兩種實作路線

- **code as graph**：Claude Code 的 dynamic workflow、Codex 的 code mode、LangGraph 等。
- **LLM as graph**：直接把 SOP 用文字、JSON 或 mermaid 圖寫出來塞進 context。現代模型已經相當能理解並照著這類 SOP 走，因此常常只要把設計好的 SOP 寫成文字、包成一個 skill 讓 agent 呼叫即可。

現代 harness 也已經提供不少原語：agent 能跑 bash（所以能執行你為確定性步驟寫的 script）、有 sub-agent 與 agent teams 的溝通協定（主 agent 可把 SOP 拆成步驟並喚起一組 agent）、需要真正確定性的檢查點時還可以用 hook 注入（goal 功能本身就是一例）。

## LLM as graph 的四個設計模式

1. **知道何時該把 agent node 切開**。技術上可以把整套 SOP 塞進單一 agent，模型越強越可能一次做完，但要理解模型的邊界：再強的模型都不擅長驗證自己的產出，所以 verifier 通常是獨立的 node；依 OpenAI 與 Anthropic 的研究，複雜任務通常也需要一個專責研究、推理、想清楚的 planner agent。同時思考哪些步驟可以平行、哪些適合用更強或更弱的模型。
2. **該用程式碼的地方就用程式碼**，這是提高可靠性、加快速度、減少無謂錯誤的好方法。適用情境：複雜的資料抓取（與其讓 agent 呼叫多個 API 再自己拼資料，不如寫成 script）、常見的資料分析、把 dev server 拉起來（免得 agent 跟它纏鬥）、以及評估結果或跑 end-to-end 測試。
3. **每個 agent node 都定義好輸入與輸出**，讓邊界與產出期待明確。
4. **設計 state**。不論走哪條路線，都需要讓不同 agent 能快速掌握目前工作狀態。最簡單的做法是一份記錄最新狀態的 markdown 檔，外加每個 agent／每次執行寫入的 append-only log。

一般流程：對任何想讓 agent 重複、可靠執行的任務，先把 SOP 攤開想過所有步驟，再依上述模式把東西歸成 node 與 edge，最後定義一份記錄 state 的 artifact 文件。兩條路線都適用，差別只在輸出物——LLM as graph 產出的是一個可被 loop、被排程或臨時喚起的 skill；code as graph 產出的是可執行的 JavaScript。

## 實例一：每日壞設計 triage（LLM as graph）

作者團隊做的 Superdesign 是讓人設計 UI 的 vibe design 平台，並在業務各處跑多條 loop。他們另開一個叫 superdesign AGI 的 repo，作為全業務的狀態追蹤與知識庫——每一次做過的事、處理過的 support ticket、ship 過的工程票都在裡面。現在要改 codebase 時，他大多不是進實際的產品 repo，而是在這個 repo 起 agent；repo 底部是 artifact 存放區，頂部則放各種 skill，其中一些本身就是用 skill 搭出來的小型 graph。

每日壞設計 triage 的目的：每天使用者在平台上產生大量設計，要撈出 agent 做壞的、或使用者抱怨的案例，持續累積可用來改進 agent 的資料集。graph 流程：

1. 每天一次，agent 依既有的啟發式指標從資料庫拉出可能是壞設計的候選清單；沒有結果就直接結束。
2. 有候選時，先跑一支 script 表面化可被機械判定的問題（有錯誤、版面整個壞掉、不 responsive、script 跑不起來等），這類直接進清單。
3. 其餘設計則 fan out 一批 sub-agent，每個處理一批：截圖該設計、與使用者的原始需求比對、輸出評估結果（各 agent 有約定好的 output schema）。
4. 主 agent 彙整資訊後排名所有壞設計，發佈成當日清單（repo 裡的一個檔案）。團隊可據此加進評估資料集，或針對各問題再開一組 agent 去改進 agent 本身。

實作方式就是一個 skill 加上幾支 script：skill 裡記錄程序——該跑哪支 script 取得候選、接著跑哪些確定性檢查、何時 fan out 視覺判斷的 sub-agent、各 agent 的 output schema、整個 loop 的 output contract 與護欄。每天只要起一個 loop、把 agent 指向這些 skill 與 script 即可。這是相當複雜的流程，但靠注入 skill 加 script 就能得到很好的產出。

## 實例二：ship change workflow（code as graph）

dynamic workflow 的做法是讓 agent 直接寫 JavaScript，因為它被賦予了幾個專為 agent 設計的原語與 API：可以呼叫函式開出 agent、組 pipeline（各階段有依賴關係）、以及 parallel（fan out 一批 agent）。有了這些，agent 可以寫出任意 JavaScript 來搭出它想要的任何 graph。

團隊的 ship change workflow 在每次已有明確 scope 與計畫後觸發，分三階段：setup 與實作 → 驗證 → 驗證通過後簡化並開 PR。JavaScript 檔裡會為各階段定義 schema：起一個 agent session 時給定 prompt、模型與 schema，session 結束時就會依該 schema 輸出結果，等同每個 agent node 的 state 輸出，下一個 node 便能帶著上一段的重要 context 與細節組 prompt。

以寫文章為例的最小示範：階段一「產大綱」，schema 含標題與各段落的重點條列；階段二「依大綱寫文章」，prompt 直接引用前一段 agent session 的輸出，最後函式回傳完整結果。另有一個開源專案以開源方式實作了 dynamic workflow，其中每個 agent node 可以是 Claude、Codex 或任何 agent library；作者在其 AI builder 社群放了幾個程式碼範例。

**最關鍵的提醒**：光把任務這樣拆開是不會work的，一定要給 agent 能好好測試的工具。這是作者看到最多人漏掉、又納悶自己的 loop 為何跑不起來的一步。他公開 repo 裡有 verifier setup skill 可直接拿去用。

## 兩種方法怎麼選

兩者都有效、輸出物不同。作者多數情況選 LLM as graph，因為 dynamic workflow 或 Codex code 目前每次都是開一個全新 agent session、無法接續前一段對話，用起來較惱人；但若任務規模極大，code as graph 是很好的方法。

作者預告下一支影片要談 graph of loops：當公司裡有大量 loop 同時在跑，如何確保它們產生複利效果。
