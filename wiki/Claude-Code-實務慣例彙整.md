---
title: Claude Code 實務慣例彙整
description: MUKI 整理 82 條 Claude Code 使用心法：計畫紀律、context 管理、CLAUDE.md／Skill／Command 分層、工作流收斂模式
created: 2026-07-27
updated: 2026-07-27
source: https://mukiwu.github.io/claude-code-tips/claude-code-best-practice-cards.html
published: 2026-04-20
parent: "[[wiki/01.index]]"
tags:
  - claude-code
  - agent-framework
  - context-engineering
  - coding-agent
---

# Claude Code 實務慣例彙整

來源是 MUKI 整理自 Anthropic 團隊（Boris Cherny、Thariq、Cat Wu 等）與社群發言的 82 條 Claude Code 使用心法（原 17 張 Threads carousel 卡片）。**單一二手彙整、非本 vault 對抗式查證**——具體指令與百分比引用時仍應回官方 changelog／文件核實；本頁只留跨時間仍站得住的方法論層，原文逐條清單見 [[Claude-Code-Best-Practice-—-Threads-Carousel-Cards]]。

## 計畫與委任紀律

- **先計畫、後動手**：開 Plan Mode 讓 Claude 先想架構；模糊需求用工具反問（如 AskUserQuestion）寫成詳細 spec 再開新 session 執行；審查計畫可用第二個 Claude 扮演審查角色，或 cross-model 對照。
- **給方向不給步驟**：交付目標與驗收標準（如「diff 你的 branch 證明它動」），別逐步微管理怎麼做——模型會自己找路徑，過度規定步驟反而限制它找到更好的解法。
- **Prototype 優先於 PRD**：建造成本低時，直接做多個版本比寫規格書更快收斂到對的方向。

## Context 管理紀律

- **context rot 有臨界區間**：token 數過大時回憶準確度下降（原文標約 300–400K，確切數字隨模型迭代會變，見 [[Agent-Harness-Engineering-框架綜述]] 的 context engineering 節，「context rot」一詞出自 Chroma 獨立研究、非 Anthropic 自創）；高智力需求的工作別拖到那個階段。
- **每輪對話是分支點**：一輪結束後主動選 continue／壓縮／清空／換 subagent，而非放任 context 累積雜訊；壓縮前先請 Claude 寫交接摘要，是比壓縮本身更可控的做法。
- **subagent 隔離雜訊**：把大量檔案讀取／搜尋的中間過程留在子 agent，只把結論帶回主 context——與 [[Agent-Harness-Engineering-框架綜述]] 的 sub-agent 隔離技術同一原理，本 vault 的 `Agent` 工具使用慣例即此模式的具體落地。
- **新功能開新 session**，別讓不相關任務共用 context 拖累判斷。

## CLAUDE.md／Skill／Command／Hook 四層封裝

依「多常用、多需要動態判斷」分層，而非哪個功能更強：

| 層 | 適合放什麼 | 限制 |
|---|---|---|
| CLAUDE.md | 持續生效的專案規則、跨檔案慣例 | 檔案過長（原文抓 200 行量級）模型會開始忽略指令；行為規範（如「別加 Co-Authored-By」）宜放 `settings.json` 用機制強制，而非寫成 CLAUDE.md 的軟性建議 |
| Command（`.claude/commands/`） | 一天用多次、不需額外 context 隔離的固定流程 | 注入現有 context，比開 subagent 輕量 |
| Skill | 需要自主判斷「何時觸發」、可分階段揭露的知識包 | `description` 要寫觸發時機而非內容摘要；正文只寫會把 Claude 推離預設行為的內容，別寫它本來就會做的事——本 vault 的 skill 撰寫慣例（見 `CLAUDE.md`「新增/修改 skill」一節）與此同向 |
| Hook | 不需要模型介入判斷、事件觸發即執行的自動化 | 跑在 agentic loop 之外，如 PostToolUse 自動格式化、Stop 時提醒繼續或驗證 |

CLAUDE.md 本身也「不保證任何事」——它是建議不是合約，模型仍可能不遵守；某項規則反覆被忽略時，該檢討的是規則設計（是否夠具體、是否該挪到 settings.json 之類的機制層），而不是預期模型必然照辦。

## 工作流收斂模式

多數場景收斂到 Research → Plan → Execute → Review → Ship 的同一模式；簡單任務不必套框架，直接對話往往更快。長 session 建議規劃與寫碼分工（規劃用高階模型、執行用效率模型），並視情況調整思考強度而非固定拉滿。

## PR 與 Debug 紀律

- **小 PR 優於大 PR**：一個功能一個 PR，方便 review 也方便 revert；配合頻繁 commit（原文引用 Boris Cherny 個人數據：p50 僅 118 行/PR，屬單一從業者自陳，非普適基準）。
- **squash merge 保持線性歷史**，一 commit 對一功能，利於 `git bisect`。
- **Debug 給 Claude 看得到的證據**（截圖、console、log），比純文字描述問題更快收斂；不同模型互相 QA（cross-model review）能抓到單一模型的盲點。
- **agentic search（glob/grep）優於向量 RAG**：原文提及 Claude Code 曾嘗試向量資料庫後放棄，改用選擇性檢索——與本 vault Query 動作「先讀 index 再鑽細節」而非全文向量檢索同一立場，見 [[LLM-Wiki-知識管理模式]]。

## 相關頁

- [[Agent-Harness-Engineering-框架綜述]] — 本頁的 context 管理、subagent 隔離對應該頁「long-horizon 三類技術」的官方版本；該頁是第一方工程文章的對抗式查證彙整，權威性高於本頁這份二手 tips 彙整，衝突時以該頁為準。
- [[Claude-Code-記憶系統六層比較]] — 本頁 CLAUDE.md 分層一節是該頁 Level 1（CLAUDE.md 原生記憶）在操作層的實務補充。
- [[LLM-Wiki-知識管理模式]] — 本頁「agentic search 優於 RAG」呼應該頁的核心設計立場。
