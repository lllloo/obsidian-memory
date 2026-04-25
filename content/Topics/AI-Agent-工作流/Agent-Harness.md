---
title: Agent Harness
created: 2026-04-21
updated: 2026-04-25
tags:
  - claude-code
  - ai-agent
  - harness
  - moc
---

涵蓋 harness 定義、planner / generator / evaluator 三角、狀態外部化、context 管理演進、多 agent 協作拓撲、評估機制與常見陷阱。

## 是什麼

**Agent harness** 是 prompt 之外的外部執行殼層：把 instructions、tools、runtime guardrails、使用者互動方式組裝成一套能讓 agent **跑得久、跑得穩、能協作** 的系統。

三個基本面：

- **Instructions**：system prompt、規則、工作協議
- **Tools**：讀檔、改檔、終端、測試、瀏覽器、review 管線
- **Interaction model**：如何下 prompt、何時切新 session、如何驗收與回報

重點不是「prompt 要多神」，而是 **agent 失敗時，有沒有外部機制把它拉回正軌**。

## 三角核心：Planner / Generator / Evaluator

Anthropic 在 long-running application harness 文章裡，把複雜系統拆到最後，發現最關鍵的結構通常只剩三個角色：

| 角色 | 職責 | 重點 |
|---|---|---|
| Planner | 規劃 | 定義目標、範圍、驗收標準；偏產品層，不是技術碎任務 |
| Generator | 實作 | 根據 plan 交付功能，和 git / tests / runtime 整合 |
| Evaluator | 驗證 | 站在對立面找 bug、找缺口、打分，不跟 generator 共用自我評價 |

**核心原則：Generator 不要自評。**

LLM 很容易對自己的輸出過度自信，尤其在 UI、產品完成度、細節品質這類主觀任務上更明顯。把評估獨立出來，品質才會穩。

## 狀態外部化：讓長任務能續跑

長任務最常見的兩種失敗：

- **one-shot 衝太快**：什麼都想一次做完，結果 context 用盡後無法接續
- **過早宣稱完成**：其實還有缺口，但 agent 已經自我感覺良好

比較可靠的解法是把狀態外部化到檔案系統：

- `progress.txt` / `state.json` / task graph
- 明確的 feature checklist 或 eval rubric
- git commits 作為可回退的里程碑
- project docs / architecture notes 作為長期記憶

`AGENTS.md`、`CLAUDE.md`、設計文件索引、任務圖 JSON，本質上都在做同一件事：**把「只存在對話裡」的資訊拉回 repo。**

## Context 管理：焦慮減輕了，但沒消失

較新一代的 Claude / Opus 模型加上 compaction，確實讓「context 焦慮」比舊時代小很多；但它不是魔法。

更穩的原則仍然是：

- 讓 agent 用搜尋工具找片段，不要動不動手動 attach 大檔
- 每個邏輯工作單元結束後就切乾淨 session 或子代理
- 把可重讀的知識放文件，不要要求 agent 在超長對話裡硬記住一切

換句話說：**compaction 減少了頻繁重開 session 的必要，但沒有取消狀態外部化的價值。**

## 多 Agent 協作拓撲

> 這一章混合了 **Claude Code 官方內建能力**（subagents / agent teams / worktrees）與**社群工具/模式**（Claude Tasks、Agent Chatter、Antigravity 等）。看筆記時要分清楚哪個是平台內建，哪個是外掛或 workflow pattern。

| 拓撲 | 機制 | 典型場景 |
|---|---|---|
| Subagents | 主 agent 分派獨立 context 的子任務 | 搜索、審查、單點研究 |
| Agent Teams | 多個 teammate 共享 mailbox / task list | 平行 code review、長任務分工 |
| Task graph / swarm | 任務帶 `blocks / blocked_by` 依賴圖 | 複數工作流協同、長時間執行 |
| Cross-CLI chatter | 不同 agent host 透過共享頻道協調 | Claude + Gemini + Codex 交叉工作 |

### 官方內建的穩定組合

- **Subagents**：適合局部研究與隔離輸出
- **Agent Teams**：適合多人分工與彼此傳訊
- **Git worktrees**：適合避免多 agent 互踩檔案

### 社群常見延伸

- **Claude Tasks**：用 task graph JSON 讓長任務有外部狀態
- **Agent Chatter / 類似工具**：讓不同 CLI agent 共用 chat channel
- **Antigravity 類模式**：共享工作區 + 獨立分支 / worktree

## Evaluation：怎樣才算真的完成

主觀任務（UI / DX / 產品細節）最怕「看起來差不多」。這時 Evaluator 需要**明確 rubric**。

Anthropic 在前端評估裡常用的四個面向：

1. **Design quality**
2. **Originality**
3. **Craft**
4. **Functionality**

另一種更工程導向的 evaluator 是 **TDD**：

1. 先寫測試（暫不實作）
2. 全 fail
3. commit 測試
4. 再讓 agent 實作
5. 直到全部通過

這也是為什麼 [[Superpowers框架]] 會把 TDD gate 放在框架核心。

## 工具與規則：通用工具通常比客製 JSON 工具穩

Vercel 在 text-to-SQL agent 的案例裡，把一堆特化工具收斂成更通用的執行路徑後，速度、token、成功率都改善。這個 pattern 很值得記：

- LLM 對 `grep`、`git`、`npm` 這類通用 CLI 有更豐富訓練先驗
- 自訂 JSON schema 越多，越容易把 agent 綁死在脆弱工具呼叫上

Skills / rules 的用途則是補另一層：

- **rules / CLAUDE.md**：告訴 agent 這個 repo 的不變量
- **skills**：把可重用流程打包成可延遲載入的工作模組

## 常見陷阱

**徵兆：agent 太早說 done**
- 原因：缺獨立 evaluator
- 解法：加 rubric、測試、review 或對抗式 evaluator

**徵兆：新 session 接不上舊任務**
- 原因：狀態只留在對話裡
- 解法：外部化到 docs / checklist / task graph / commits

**徵兆：多 agent 互踩檔案**
- 原因：共享工作區但沒隔離
- 解法：worktree、分支與明確 file ownership

**徵兆：工具越加越多，結果更脆**
- 原因：過度依賴客製工具 schema
- 解法：能用通用 CLI / 標準工具就不要先發明新輪子

## 相關

- [[GAN-Style-Harness]] — 三角架構的具體實作案例
- [[GSD框架]] — 偏 orchestration / fresh session 的流派
- [[GStack框架]] — 偏規劃 / design / QA 的 workflow pack
- [[Superpowers框架]] — 偏 TDD / implementation gates 的流派

## 來源

- [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps)
- [We removed 80% of our agent's tools](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)
- AILABS-393、AIJasonZ 等多支影片摘要（作為社群延伸脈絡）