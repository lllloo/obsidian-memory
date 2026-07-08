---
title: 讓 Fable 5 成本降低 80% 的五個使用技巧
description: 整理五個降低 Claude Fable 5 token 與成本的技巧：調降 effort level、讓 Fable 當架構師分派模型、引入節省 token 的 skills、用 Opus 先做研究、以及 advisor mode。
created: 2026-07-06
updated: 2026-07-06
source: https://www.youtube.com/watch?v=p8ypBeNXQ8E
published: 2026-07-03
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - token-optimization
---

影片背景：Fable 5 再過幾天就要從 Pro / Max 方案下架、改吃 API 價格，且有每週用量上限，因此重點是如何在不犧牲模型能力的前提下壓低 token 與成本。以下五招由影片作者實測整理。

## 技巧一：調降 effort level

門檻最低、槓桿最高的一招——用 `/effort` 把預設的 high 降下來。作者引用兩組 benchmark 佐證：

- **Deep SWE（長時程 agentic 任務）**：max effort 每題平均約 $22，但相較 extra high 的 pass 率提升有限；降到 low 只要 $3.76，成本降幅超過 80%。而 Fable 5 在 low（60%）仍勝過 Opus 4.8 在 max（59%，約 $13）。medium 約 65%、high 約 69%、extra high 約 70%。
- **Anthropic 官方 frontier code accuracy vs cost**：Fable 5 在 low 約 $5 出頭、分數約 11%，與 Opus 4.8 在 max（約 $11）同分但半價；升到 medium 已勝過 Opus 4.8，且仍比 extra high 便宜。

結論：任務越不複雜（例如 web design）越該用 medium 或 low，複雜任務才需要更高 effort。作者最想讀者實驗的就是這招。

## 技巧二：讓 Fable 當架構師，分派工作給合適模型

不要用 Fable 同時做規劃與執行。讓 Fable 5 當 architect 產出 plan，再依複雜度把工作分派給合適模型（Opus、Sonnet，或 GPT 5.5、本地模型）。Fable 夠聰明能在 plan 裡明確指定哪部分用哪個模型。

- 進階做法：搭配 Claude Code 內的 Codex plugin（含 Codex rescue function），把部分 feature 交給 GPT 5.5。
- 簡化做法：直接用 plan mode 讓 Fable 產出一份 markdown plan，再另開一個 Opus session 執行該 plan。

重點是避免 Fable 把 token 燒在低階任務上。

## 技巧三：引入節省 token 的外部工具 / skills

例如 Ponytail：給 Claude 一組準則，讓它在維持輸出品質的前提下寫更少程式碼、用更少 token。

- 官方 benchmark 只在 Haiku 4.5 上測過；作者自己在 Opus 4.8 上實測，數字甚至更好（寫更少 code、耗更少 token、更快）。
- 作者在 Fable 5（medium setting）上實測 Ponytail：整體輸出 token 更少，換算成本約便宜 22%，比官方對 Haiku 宣稱的還好。

類似工具還有 Caveman。大方向：Fable 是昂貴模型，任何能帶來約 20% 節省的工具都值得實驗，別因存疑就直接排除。

## 技巧四：讓 Opus 先做研究，再交給 Fable 規劃

表面上與技巧二相反：這裡改由 Opus 為 Fable 準備。因為 plan 通常需要研究，而研究不需要 Fable 等級的高階推理。

- 用 `/deep-research`（Claude Code 內建 dynamic workflow）做研究。作者為這支影片跑 deep research 時噴出 109 個 sub-agents——若每個都用 Fable 5 會直接爆用量上限。
- 做法：用較低階模型（Opus / Sonnet）上網蒐集資訊、做基本 adversarial 查證，再把整理好的 context 交給 Fable 5 產出 plan。

讓 Fable 專注在高階架構思考，把蒐集 context 這類雜活留給便宜模型。

## 技巧五：Advisor mode

最初以 Opus + Sonnet 搭配示範：聰明模型當 advisor / planner，低階模型當 executor 負責讀寫與呼叫工具；executor 一卡住就把 context 分享給 advisor 問下一步該怎麼做。

要讓 Fable 5 當 advisor：

- 你設定的 model 就是 executor（實際寫 code 的那個），所以要把 model 設成 Opus。
- 執行 `/advisor fable`，讓 Fable 5 負責指揮 Opus。

Anthropic 尚未公布 Fable 當 advisor 的官方數字，但作者以 Opus + Sonnet 4.6 的 advisor mode 圖表推測：executor 會表現更好且更便宜。適合想讓 Fable 純粹當架構師 / 指揮者的人。
