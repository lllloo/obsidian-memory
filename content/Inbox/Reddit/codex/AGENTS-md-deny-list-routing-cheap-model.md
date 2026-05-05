---
title: AGENTS.md trick that stopped Codex from doing dumb work at premium rates
created: 2026-05-05
updated: 2026-05-05
source: https://www.reddit.com/r/codex/comments/1t3ffxe/agentsmd_trick_that_stopped_codex_from_doing_dumb/
published: 2026-05-04
tags:
  - reddit
  - codex
  - workflow
  - mcp
  - best-practices
---

> **繁中摘要**：用 AGENTS.md 寫「**deny-list**」（do NOT use Codex for…）比正向「請用便宜模型」更能讓 Codex 把瑣碎任務（reformatting、單欄擷取、待人工複審的分類）路由到便宜的 worker model（透過 MCP server，預設 DeepSeek V4 Flash，可換任何 OpenAI-compatible endpoint），實測一週 184/520 calls 被 offload，省下約 $5–9 Codex spend。

---

## 原文重點

**問題**：作者週日稽核 Codex token 消耗，發現一半的 call 是 "rename these 12 fields"、"format this csv as markdown table"、"extract the dates from this changelog" 這類 janitor work，gpt-5.5 用 architect 費率做這些事。

**核心做法：deny-list framing**

- 正向規則「use the cheap model for X」常被 Codex 忽略
- 負向規則「do NOT use Codex for: bulk reformatting, single-field extraction, classification you'll review anyway」明顯比較黏
- 作者觀察：Codex 對 negative rules 的遵守度高於 positive suggestions

**Setup**

- 一台 MCP server，提供單一 tool
- Codex 透過 `~/.codex/config.toml` 標準 MCP config 呼叫
- 預設 worker：DeepSeek V4 Flash（選它的理由是 1M context window + 價格）
- `base_url` 一行就能改，任何 OpenAI-compatible endpoint 皆可（ollama / vllm / lm studio …）
- Repo（含 AGENTS.md template 與 `config.toml` snippet）：<https://github.com/arizen-dev/deepseek-mcp>

**一週實測（單一專案）**

- 184 calls offloaded out of ~520 total
- worker 側成本：`$0.34`
- 估算避免掉的 Codex spend：`$5 ~ $9`（依 token mix）

**路由判準**

- 路由給 worker：bounded 任務、會 skim 後才採信的、「思考」其實只是套模板的
- 留在 Codex：planning、會出貨的程式碼、碰到不熟 repo 區塊、錯了會在 review 漏掉的

**Caveats**

- 它是 worker 不是 agent，**沒有 tool calls**
- worker 側 latency 約 3–25s，連續鏈式小 call 會累加
- 仍需人工 review 輸出

## 社群討論亮點

- 有人質疑為何 Codex 不預設用 gpt5.4 mini / 5.3 spark 做這類 routing，並詢問品質損失情況（作者貼文未直接回應品質量化）
- 另一位用戶分享現行替代法：在 plan mode 結束後關掉 plan mode，貼入自寫的 agent rule set，由該 rule set 指定不同任務用哪個 model；不需 MCP server 也能達到部分 routing 效果
- 顧慮：把品質較差的 cheap model 產出引入由 5.5 維護的 repo 是風險，但「capitalize this letter 卻啟動整顆 GPU」也明顯不合理，trade-off 需自己拿捏
