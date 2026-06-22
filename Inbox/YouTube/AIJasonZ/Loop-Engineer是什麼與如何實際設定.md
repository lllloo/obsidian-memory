---
title: Loop Engineer 是什麼，以及如何實際設定
description: 解析從 prompt engineering 到 loop engineer 的演進，拆解自動觸發 agent 迴圈的核心元件：trigger、共享檔案結構、工具連接與可自主驗證的 codebase harness。
created: 2026-06-22
updated: 2026-06-22
source: https://www.youtube.com/watch?v=W6x-hb44C0c
published: 2026-06-18
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
---

## 從 prompt engineering 到 loop engineer 的演進

過去一年大量新名詞出現，每個其實都是針對 LLM 不同使用層級的技術叢集：

- **2023（GPT-3.5 / 4 API 初期）**：任務多半是單純的 task completion，給輸入、用模型輸出文字（抽結構化資料、寫文章）。因模型輸出不確定，**prompt engineering** 應運而生——調整 context 以引導行為（例如要求一律全大寫）。
- **2024 中（更聰明 + 更大 context window）**：context window 從約 4,000 跳到 128k 已是驚人進展，Google 再把標準拉到每個模型預設 1 million token。模型開始搭配 MCP 等工具自行決策，並把 tool call 與 tool response 納入對話迴圈，持續跑到任務完成。代價是 context 被愈吃愈快。
- **context 管理技術興起**：即使有 1M context，有效視窗約落在 128k–200k，能否把最相關資訊塞進去直接影響 agent 表現。於是出現一系列技術：system prompt 怎麼寫才能更好觸發 prompt cache、長對話的 compaction 策略，以及用 skill 擴充 agent 能力而不撐爆 context。
- **2025 末（更長更大的任務）**：one-shot 讓 Claude Code 完成 30 分鐘甚至 2 小時的工作變得常見，開始大量實驗 loop 與 workflow。最初是粗略的 while loop（同一 prompt 無限跑），後來演進到跨 session 的多 agent 協作——每個 session 處理一個任務並在迴圈中跑，需要一套跨 session 的狀態／檔案系統讓各 session 知道進度。

## Agent 的基本三件套

不論講得多進階，每個 agent 底層仍回到三件事：

- 程式語言寫的 agent loop
- memory layer（記憶層）
- tool access（工具存取）

## Harness 與 loop engineer 的定位

**harness** 概念最早由 LangChain 提出，定義很直接：**任何非模型的部分**。正因涵蓋太廣（prompt engineering、context 管理、orchestration 邏輯、hooks）才令人混淆。講者用兩層優化來區分：

- **內層（agent loop 本身）**：Claude Code、Codex 或自建 agent，所有優化都圍繞「給一個任務時能不能把它做好」。
- **外層（loop engineer）**：不只關注「把任務做好」，而是讓整個 agentic system 決定「該做什麼」。這層是觸發 agent runtime、追蹤 state 與 log、讓系統持續自我改進的環境。

外層的關鍵價值是**把人從親自 prompt agent 中解放**：agent 變得更自主，可由 cron job、另一個 agent、甚至伺服器 incident 的 webhook 觸發，在隨機時間被喚醒並交付有意義的成果。每次喚醒後 agent 通常做調查與行動，產出一份 backlog／ideas，主 agent 再排序、必要時指派給其他 agent。

## Loop 如何 compound（複利疊加）

關鍵在於**多個 loop 共讀共寫同一套共享資料夾**，形成複利效應。講者公司實際在跑的 loop：

- **support loop**：每 30 分鐘喚醒，處理所有 support ticket，自動回覆未處理的，並把 frictions 與 ideas 記進名為 **signals** 的資料夾。signal 是捕捉產品想法、發現的摩擦、可能錯過的機會的地方——例如某輪發現多人問如何匯出檔案，就建一個 export-file 的 signal MD 檔，記下哪些 user 遇到，之後同問題再出現就追加進同一檔。
- **SEO loop**：每天早上 9:00 拉資料、研究主題、發佈 SEO 頁面。分析資料時可能發現洞察（某頁點擊很多但轉換不足），就為該路由加一個 conversion gap 的 signal。
- **跨 loop 互通**：因為共享檔案系統，成長實驗的 loop 不只看自家 session 與分析，還會看其他 loop／部門識別出的所有 signal，據此排序——修被多次回報的 bug，或承接 marketing／SEO 在優化的機會。若 ads loop 發現某關鍵字點擊率高但沒有 organic content，這個 signal 也會回饋給 SEO loop 去優先產出該關鍵字的 organic content。

更強的版本：support loop 不只記 ideas 與 frictions，還直接觸發 coding agent 去實作部分想法，並監控成效、甚至回頭告知客戶修正已上線。兩種 loop 都有價值，後者更強大。

## 四個核心元件

1. **設定 triggers**：可以是多種觸發來源（cron、另一個 agent、webhook）。
2. **設計檔案結構**（最重要，見下節）。
3. **給 agent 工具與 connectors**，才能做有意義的工作。
4. **讓 codebase／環境支援平行且自主的工作**（很多人忽略的最重要一點）——多個 agent 能同時工作、各自驗證自己的成果。

## Codebase harness：legible、executable、verifiable

讓 agent 能自主在環境中工作，codebase 要具備三特性：

**Legible（可讀）**——agent 能輕易理解該改哪裡：

- 維護一個概略索引的 `agents.md`（OpenAI 的做法），指向各種文件系統，讓 agent 漸進式探索資訊。
- 設定 **custom lint**：不能完全依賴 agent 自己找到相關資訊，可把規則注入程式化的 lint 檢查，agent 做錯時自動浮現警告。例如複雜的 monorepo 不想讓 agent 用某些 legacy 資料夾，agent 一 import 就報錯。核心是替 agent 做 context engineering，不總是靠它自己找資訊。

**Executable（可執行）**——agent 應在 dev server 已跑起來的狀態開始工作，理想上不花 token 或認知負荷：

- 寫一個 `dev.local` 之類的腳本，agent 跑一行就把 dev server 拉起。
- 讓 codebase **work tree friendly**：五個平行 agent 各自在自己的 work tree，仍能各自起 dev server 測試而不互相衝突。
- 設定便利腳本讓 agent 跳到特定狀態（例如某種 seed 狀態）以測試特定情境，替 agent 驗證成果提供捷徑。

**Verifiable（可驗證）**——給 agent 對的工具去測試與記錄結果：

- 講者最推 **Playwright CLI**：讓 agent 有效操作瀏覽器，還能錄影片附到 GitHub PR，方便人類審閱是否正常。
- 為關鍵流程寫少量 end-to-end 測試，確保永不壞掉（如 upgrade flow、sign up flow）。
- 提供 **PR skill**，定義 agent 提 PR 前必做的步驟清單。
- **不要讓 agent 自我驗證自己的工作**——通常效果不好。PR skill 裡一律要求 agent **spawn 一個 read-only 的 verifier agent**，並給它詳細 spec。

## 檔案與 logging 系統的最佳實踐

講者認為三種檔案是好的抽象層級：

**1. Artifacts（產出物）**——每個 agent 工作或發現的輸出，是共享知識層。類型多元：docs、signals、tasks，甚至 campaign（跑 ads 時用來追蹤成效）。講者的設定有 SEO loop、ads loop、跑在定價上的 product growth loop 等：

- 每種 artifact 有自己的資料夾，資料夾內放一份 README，清楚說明什麼該放／不該放、新增項目的流程、以及該 artifact 的 schema。
- 每個 artifact 檔有 metadata frontmatter + 主體內容 + 一段 timeline 記錄變更。
- signals（產品回饋、想法、任何 loop 觀察到的東西）同理，可連到不同來源（原始客戶回饋或 support ticket artifact）。artifact 的目的是成為任何 loop 都能讀寫的共享 library。
- 可再建小型 mini app 來檢視各種 artifact，方便 human-in-the-loop 追蹤需要自己注意的事項。

**2. Loop contract（迴圈契約）**——每個 loop 定義一份契約，包含：loop 的 goal、該遵循的 workflow 與邊界、outstanding task backlog（下次 loop 挑最重要的接手或重新排序）、timeline（記住之前做過什麼）。講者每個 loop 資料夾放一份簡單 README 作為契約。loop 被觸發時先讀契約，理解 goal、workflow、之前發生的事，再採取行動。這份契約極其有用。

**3. Logs（日誌）**——為何已有 timeline 還需要 log：講者的一天混合了「審閱 loop 產出」與「以 copilot 狀態跟 agent 做困難或創意工作」，需要讓 agent 快速理解跨 domain 發生了什麼、並捕捉臨時資訊。做法是一個**全域 work log MD 檔**：每個 agent 完成一大塊工作就寫入此檔；開工前也會讀最後 5–10 筆。

## 實際搭一個 support loop

以較簡單的 support loop 示範（每 30 分鐘拉近期 support ticket、有資訊就草擬或直接回覆、記錄 frictions 與 ideas）：

1. **先建 skills**：support 人員需要的存取——Intercom（抓 ticket）、Stripe（查訂閱／付款）、Supabase（debug 付款資訊）、render（抓 backend log），加上 triage support ticket 的 skill。這部分依自家業務客製。workflow 定為：抓過去 X 小時有更新的所有 ticket、調查 user 提到的問題、建立 tickets artifact 記錄處理過的、建立 engineer ticket 記錄回饋想法、最後記下做了什麼。
2. **建 `claude.md`**：讓 agent 理解業務。可 prompt Claude Code／Codex 研究你的業務並存進此檔，內含所有業務 context，以及回應 agent、engineer 工作的規則（解釋有哪些 repo、要求每次走 git work tree 並含管理 work tree 的契約，這些跨任何 loop 適用）。
3. **`architecture.md`**：在 `claude.md` 中被引用，是基於既定結構的通用指令——定義 agent 該建立哪些 artifact 類型與 loop domain、以及 log 的慣例。指向此檔說「幫我設定相關 artifacts」，agent 會讀 architecture 檔並 scaffold 出 docs、signal（feedback／idea／observation）、tickets 等 artifact 類型，以及空的 log MD 檔，再建 `domain/support` 資料夾。
4. **先手動跑一次測試**：通常先手動跟 agent 跑一次（fetch 過去一小時 ticket、分析、審閱、草擬回覆、存 ticket、為產品想法／user friction 存 signal、明確 bug 直接 spawn agent 修並建 engineer ticket）。先 test run，觀察 agent 處理幾個 ticket、各自建 artifact、識別潛在回饋／friction、記錄 bug，藉此校準 workflow。
5. **設定 loop**：workflow 對了之後，請 agent「先建一份 README 作為契約（含 goal、workflow、timeline），再把 loop 設到 session」——產出契約 README 並設定每小時觸發該 session 的 loop。

講者提到建了一個 `loop engineer setup` 的 repo template，封裝團隊設 loop 的最佳實踐，可複製其資料夾結構來設定 artifact 與開新 loop。
