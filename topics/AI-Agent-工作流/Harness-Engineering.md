---
title: Harness Engineering
created: 2026-04-21
updated: 2026-06-30
tags:
  - claude-code
  - ai-agent
  - harness
---

**Harness Engineering** 是設計、建置、迭代 agent harness 的工程實踐，跟 Prompt Engineering / Context Engineering 並列。

Agent = Model + Harness。Harness 是 prompt 之外、把 instructions、tools、runtime guardrails、互動方式組裝成「agent 失敗時有外部機制把它拉回正軌」的系統——重點不是 prompt 多神，而是失敗 recovery 機制。

> 命名：OpenAI 用 **Harness Engineering**，Anthropic 用 **harness design**。兩者在同一個問題域，但重心不同：前者偏 agent-first engineering discipline，後者偏長任務 app development 的具體 harness 設計。

## 代表性架構：Planner / Generator / Evaluator

Anthropic 的 long-running app development harness 把複雜任務拆成三個主要角色，適合拿來理解「生成」與「評估」為什麼要分離：

| 角色 | 職責 | 重點 |
|---|---|---|
| Planner | 規劃 | 定義目標、範圍、驗收標準（產品層，非技術細節） |
| Generator | 實作 | 根據 plan 交付，跟 git / tests / runtime 整合 |
| Evaluator | 驗證 | 站在對立面找 bug、找缺口；不跟 generator 共用自我評價 |

## 長任務 loop 的最低構件

長任務 harness 不是「讓 agent 一直跑」而已，而是把人原本在每輪之間做的檢查、修正、記錄外部化。最低構件有六個：

- **可觀察的 oracle**：開工前先定義什麼證據能代表完成。測試綠燈、browser walkthrough、截圖比對、benchmark、人工審核紀錄都可以；重點是 agent 不靠自我感覺收工。
- **外部 state**：用 progress 文件、task graph、`state.yaml`、ticket 或 commit 保存目前做到哪裡，避免 chat context / compaction 成為唯一真相。
- **安全切片**：任務切分不是越小越好，而是每片都要可獨立執行、可驗證、失敗時可回滾或隔離。
- **角色權限分離**：讀現況的 scout、做高風險判斷的 judge、唯一可編輯的 worker、負責標記完成的 PM 不應混成同一個全能 agent。這比多開幾個 subagent 更重要。
- **feedback quality**：測試輸出、錯誤 log、瀏覽器截圖、使用者回饋要能進入下一輪決策；低品質或被截斷的 feedback 會讓 loop 只是在重試同樣錯誤。
- **停止條件與錯誤處理**：明確寫出什麼情況算完成、什麼情況要停下找人、tool call 失敗時怎麼清理狀態。沒這層，loop 不是太早宣告成功，就是空轉燒 token。

Deterministic loop 適合測試、編譯、健康檢查這類 done 清楚的任務；non-deterministic loop 適合 UI、產品判斷、內容品質，但必須把主觀判斷轉成可檢查 artifact，例如設計 rubric、截圖走查、對抗式 reviewer。

Workflow 與 goal 的差別可用任務形狀判斷：**wide 用 workflow，deep 用 goal**。workflow 適合拆成多個互相獨立的 sub-task 平行跑，例如研究、審查、遷移盤點；goal / loop 適合一步步深入、下一步依賴上一輪回饋的任務。任務不夠大、不值得交叉驗證、或其實需要 agent 自行摸索時，硬開多 agent workflow 只是燒 token。

## 立場

- **Generator 不要自評**：LLM 對自己輸出過度自信，主觀任務（UI / 產品完成度）尤其明顯——把評估獨立出來品質才會穩
- **通用工具比客製 JSON schema 工具穩**：LLM 對 `grep` / `git` / `npm` 這類通用 CLI 有更豐富訓練先驗，自訂工具 schema 越多越脆；但前提是資料本身已經結構化、命名一致、可被檔案系統與 CLI 讀懂（Vercel 在 text-to-SQL agent 拿掉 80% 工具後速度 / token / 成功率都改善）。延伸手法是**用型別系統當 guardrail**：與其讓 LLM 直接猜 raw JSON，不如讓它產出能編譯的程式碼再轉換——n8n 官方 MCP 讓模型寫 TypeScript、經 type-check / 編譯驗證後才轉成 workflow JSON，型別系統先過濾掉大量結構錯誤
- **大型 codebase 用 file system 導航勝過 RAG**：把整個 codebase embedding 後 semantic search，容易拿到過期或相似但錯誤的檔案、central index 與實際檔案系統不同步、agent 據此幻覺出不存在的 module / symbol；改用 file system + shell + 精準讀檔逐步縮小範圍（與 agentic RAG 的 `list/grep/read` 骨架同理）更穩、更省 context——這是「通用工具勝過客製抽象」在 code navigation 上的體現
- **狀態外部化才能續跑**：progress 文件、feature checklist、task graph、git commits——把「只存在對話裡」的資訊拉回 repo；compaction 可以降低重開 session 的頻率，但長任務仍需要 handoff artifacts、必要時 reset，以及可被下一輪 agent 接手的外部狀態
- **依賴變更也是 runtime guardrail**：讓 agent「必須先證明 dependency 值得加入」而非自由安裝，把套件變更變成可審核事件
- **背景自動化要分層喚醒**：不是每個 cron 都該叫 LLM。健康檢查、TLS、成本監控這類 deterministic 檢查可先用便宜腳本跑；只有事件異常或需要判斷時才喚醒 agent。PRD、健康檢查規則、競品監控這類會演化的上下文適合做成 skill，而不是每輪把整份文件塞進 context。
- **高權限自跑要有隔離與回滾**：自動核准、yolo、背景修復這類設定只適合在 sandbox、測試、checkpoint、可回滾工作區都到位時開。否則它只是把人工確認移除，沒有補上對等的安全機制。

## 命名史與爭議

詞很新、業界尚無嚴格定義，公認起點是 2026-02-05 Mitchell Hashimoto《My AI Adoption Journey》——他自陳「不知道業界有沒有公認叫法，姑且叫它 Harness Engineering」，核心理念是 agent 一犯錯就改造系統讓它絕不再犯。隨後 OpenAI 那篇標題帶 Harness Engineering 的文章正文其實只提了一次 Harness，被推測是受 Hashimoto 啟發後才把詞放進標題；LangChain《The Anatomy of an Agent Harness》則把公式定調為 `Agent = Model + Harness`（「If you're not the model, you're the harness」），與本文開頭一致。

**是不是噱頭**：它用到的技術沒一個是新的——linter、任務拆解規劃、品質評估機制早就存在，Harness Engineering 只是把它們重組到一個新詞下，提供的是系統思維框架而非顛覆性新技術。懷疑論的兩個攻擊點：(1) 新瓶裝舊酒還造詞宣傳；(2) 隨模型能力增強，今天的 Harness 設計遲早被模型自身吸收而不再需要。

合理立場：**不是噱頭，但也不是終局**，而是過渡期的關鍵技術。模型仍會犯錯、幻覺、在複雜任務偏離軌道，在此現實下誰把 Harness 搭得更穩，誰就更早把模型能力轉成生產力。

## 框架實作

- [[GAN-Style-Harness]] — Planner / Generator / Evaluator 三角的具體實作
- [[bookmark-Superpowers-Agent開發框架|Superpowers]] — 偏 TDD / implementation gates 的流派
- [[bookmark-GStack-Agent開發框架|GStack]] — 偏規劃 / design / QA 的 workflow pack
- [[bookmark-BMAD-Agent開發框架|BMAD]] — 偏 agile lifecycle / 多軟體角色 persona 接力
- [[bookmark-Spec-Kit-Spec驅動開發框架|Spec-Kit]] — 偏 Spec-Driven Development，以 spec 為 first-class artifact 驅動 code 生成

多 agent 協作機制（Subagent / Agent Teams / Forked subagent / worktrees）見 [[Claude-Code-多-Agent-協作]]；再往上一層的協作拓撲（人管 ticket、agent 在 ticket 層工作回報，「狀態外部化」推進成 ticket 系統即 state machine）見 [[Ticket-驅動的-Agent-協作]]。

## 來源

- [Harness engineering: leveraging Codex in an agent-first world (OpenAI)](https://openai.com/index/harness-engineering/)
- [Harness design for long-running application development (Anthropic)](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [We removed 80% of our agent's tools (Vercel)](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)
- [My AI Adoption Journey (Mitchell Hashimoto)](https://mitchellh.com/writing/my-ai-adoption-journey) — 詞源
- [The Anatomy of an Agent Harness (LangChain)](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness) — 定調 `Agent = Model + Harness`
- [Goal Buddy 修復長任務 Agent（AI Labs）](https://www.youtube.com/watch?v=q7Am0pV6FjQ)
- [Loop Engineering 強化 Hermes Agent（AI Labs）](https://www.youtube.com/watch?v=AQRDjI5owZI)
- [Hermes Agent 與 Claude Code 自動化案例（AI Labs）](https://www.youtube.com/watch?v=Sb96po6S67k)
- [Hermes Agent 進階用法（AI Labs）](https://www.youtube.com/watch?v=qMEm1bgxnUM)
- [Hermes Agent 隱藏設定（AI Labs）](https://www.youtube.com/watch?v=nN6DZi_fiSo)
- [Claude Code 完整作業系統藍圖（AI Labs）](https://www.youtube.com/watch?v=5LnwJyi1il4)
