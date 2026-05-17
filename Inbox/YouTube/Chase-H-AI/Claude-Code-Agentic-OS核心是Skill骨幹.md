---
title: Claude Code Agentic OS 核心是 Skill 骨幹
created: 2026-05-15
updated: 2026-05-15
source: https://www.youtube.com/watch?v=d86VCtQ_dN8
published: 2026-05-14
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - agentic-os
  - skill
  - automation
  - obsidian
  - dashboard
---

## 核心論點：價值在 Skill 不在 Dashboard

社群上瘋傳的 Claude Code「command center / dashboard」其實是表象。真正驅動 agentic OS 價值的是底下那層 **skill 與 automation 骨幹**——把你日常工作流程編碼成 skill，再把適合的轉成 automation。Dashboard 只是把骨幹的能力暴露出來給沒法進 terminal 的人用，沒有底層骨幹的 dashboard 是「fancy nonsense」。

## Agentic OS 的三層架構

1. **Skill 與 Automation 骨幹（核心）**：把日常 workflow 編碼成 Claude Code skill，必要時轉成 automation
2. **Memory 層**：context engineering，可以做完整 knowledge graph（LightRAG 等），但 Obsidian 已是 80% 解，多數人夠用
3. **Dashboard / Command Center（最後才做）**：上述兩層鎖好才有意義

## 為什麼要把 workflow 編碼成 Skill

多數人用 Claude Code 的方式是「開 terminal，描述任務」，本質上就是稍微好一點的 ChatGPT。把重複任務編碼成 skill 帶來：

- **方便**：原本要一整段話描述的任務，現在一個單字觸發
- **可測試**：用 `skill-creator` skill 對「有 skill vs 沒 skill」做 A/B 測試，確認 skill 是否真的提升效果
- **降低隨機性**：LLM 本質非確定性，把日常任務 codify 能讓系統輸出更接近 deterministic

## Skill 創建流程

1. 開 terminal、開新 Claude Code session、開麥克風
2. 對 Claude 講：「這是我的 daily plan、我做這些事，幫我從中抽出 skill」
3. Claude 把 workflow 切成 skill candidates，用 skill-creator skill 落地
4. 測試 skill、走下一個 domain（business、team、personal life）

關鍵心態：**skill 應該客製化給「你」**，不要在 awesome-claude-skills 這種 mega-repo 大海撈針。Claude Code 最強的地方是極易客製，要系統化地用這個優勢。

## Workflow Skill（高階組合 Skill）

可以把多個小任務組合成一個 workflow skill。範例：作者的 `content-cascade` skill 做以下事——

- 下載 transcript
- 生成 blog post / LinkedIn post / Twitter post
- 啟動 Playwright 自動發文

九個獨立任務變一個 skill 觸發，生產力提升顯著。

## Productivity 通用建議：Google Ecosystem

幾乎每個人都能受益的一個 skill 類別：把 Google 生態接進來。

- **進階做法**：GWS CLI，能控制整個 Google ecosystem（email triage、Drive 操作、Calendar 等）
- **基礎做法**：用 claw.ai 內建的 Gmail / Calendar / Drive MCP connector
  - 限制：MCP 版不能直接寄信，但可以建 draft，多數人覺得夠用（反正本來就不想自動寄）
  - 設定耗時：30 秒，幾乎沒人做卻是巨大 productivity 升級

## Automation Decision Tree

每個 skill 都要問：on-demand 還是 routine？分兩種 routine：

- **Local automation**：跑在自己電腦上，要 Claude Code 開著；不確定就選這個
- **Cloud automation**：跑在 Anthropic server，有配額限制、看不到本機 CLI / skill / 檔案

實務上多數情況選 local。

## Memory 層：Obsidian 的真實角色

破除迷思：**Obsidian 不是 RAG，不做 embedding，沒 vector DB**。它只是一個「組織層」——讓人類能在大量 markdown 檔之間瀏覽、連結，不會改變記憶機制。

但「組織得好」在 scale（數千份文件）後變很重要，不只對人，也對 Claude Code 的 token efficiency（找東西不浪費 token）。

### Karpathy RAG 結構（基準參考）

- `raw/` — unstructured 原料
- `wikis/` — 把原料整理成 reports / articles
- `outputs/` — 交付成品（slide deck、deliverable）

範例流程：研究 AI agents → 進 `raw/` → 整理進 `wikis/AI-agents/` → 做成 slide deck 進 `outputs/`。

**不需要照抄**這個結構，重點是：自己看得懂、Claude Code 在十萬份檔案下也能爬。

### Index 檔案（最重要的 takeaway）

Karpathy 結構真正的核心是 **index 檔**：每個資料夾都放一個 index 當 table of contents。

- Vault 根 → 列出所有頂層資料夾說明
- 每個子資料夾 → 列出該層所有文件 / 子資料夾

從 vault 進 `wikis/` 看 index 知道有 `agents/`、`rag-systems/`、`content/`；進 `agents/` 又有 index 列裡面文件。一層層遞進。沒有 index 等到累積 5000 份文件就找不到東西了。

作者實際結構：`archive/`、`content/`、`notes/`、`dashboard/`、`inbox/`、`ops/`、`project/`、`systems/`、`wiki/`，每層都有 index。

## Dashboard 的兩條路：Obsidian-forward vs Streamlit Web App

兩種實作，trade-off 不同：

### Obsidian-forward Dashboard

- 內建在 Obsidian 裡，本身就是 custom plugin
- 優勢：**ergonomics 與 power**，可內嵌 terminal、Google Calendar 網頁、各種 tab（audience metrics、research、headlines、GitHub trending、Hacker News、content opportunities）
- 劣勢：**分發難**——要 clone → 進 Obsidian → 啟用 plugin → 移動 panel → 各種手動設定，沒法給非技術人員
- 適合：solo operator、要 all-in-one workspace

### Streamlit Web App Dashboard

- 純 local web app，本質上就是一堆按鈕對應 skill
- 優勢：**分發極快**，丟 GitHub repo 給 client 幾秒就跑起來；非技術人員一鍵執行 skill
- 劣勢：少了 Obsidian 那種無限客製
- 適合：要包成產品給 team / client

## Engine 可替換：Claude Code → Codex

整套架構是「chassis」，Claude Code 只是 engine。可以隨時換成 Codex CLI——

- 用 Claude Code 直接 refactor dashboard 程式碼指向 codex CLI，幾分鐘搞定
- 可在 dashboard 加 toggle button 切換 engine

## 成本問題：Headless `-p` Mode

Anthropic 對 `claude -p` headless 模式有負面態度：給 200 美元 / 月 plan 但限制只能用在 API cost。整套 OS 在底層跑 headless，會不會出問題？

- 多數人（99.99%）不會踩到 quota
- 真的踩到 → 把 engine 切成 Codex CLI，沒這個限制、性價比更好

## 結論：先做 Skill 骨幹，再談其他

- 看到 fancy dashboard 不要先羨慕，那只是 facade
- Skill 骨幹是 90% 的價值，dashboard 是 10%
- Solo operator：Obsidian-forward 路線最適合
- 包產品給 client / team：Streamlit web app 路線
- 反 agentic OS 的人通常只批 dashboard 空殼——他們講的是對的，但骨幹才是重點
