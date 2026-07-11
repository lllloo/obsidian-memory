---
title: 比 90% 的人更會用 Claude Fable 5
description: 軟體團隊實測 Fable 5 的使用守則：effort 設定停在 high 以下省一半用量、大模型規劃小模型實作、Ponytail 配 TDD 減少代碼量、主打 security 與 code review。
created: 2026-07-10
updated: 2026-07-10
source: https://www.youtube.com/watch?v=GM7-ei-4Xc8
published: 2026-07-06
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - token-optimization
  - best-practices
  - security
  - workflow
---

## Effort 設定的陷阱

- Effort 是模型回答前思考多深的設定；在 Fable 5 上把它調高是個大陷阱。
- 作者實測：**xhigh 與 max 的輸出跟 high 完全一樣**，不只他們、其他人也有同樣經驗；調上去只會重擊你的用量。
- Ultra code 只是疊在 effort level 上的一個 Claude Code skill，作者認為從未產出過有價值的東西，只是 Anthropic 讓你多花錢的方式之一。
- 結論：**effort 保持在 low 到 high 之間，永遠不要超過**；low 與 medium 在 Fable 上的表現會讓你意外地好。此一調整就能把用量砍半而品質不減。
- 背景：Fable 5 即將從方案中下架，但 Anthropic 已公告計劃讓它回歸，不是永久消失。Anthropic 的官方 prompting guide 只針對「在 app 內用模型」，不涵蓋個人工作流的用法。

## 大模型規劃、小模型實作

- AI 圈每逢「大模型＋更小但夠聰明的模型」同時存在，就會流行「大模型做 planning、小模型做實作」——老生常談但不是壞建議。例如 ingest 文件、讀大型 PDF 這類工作不該用大模型（作者在 AI Labs second brain 攝取競品內容做研究時就是這樣做）。
- 最簡單的工作流：用 Fable 等大模型產出 PRD 規劃，功能不大就交給小模型實作。作者的 community 專案在 `docs` 資料夾下有實作新功能專用的子資料夾，每個新功能都有一份基於固定範本的 PRD；範本針對專案客製（例如每次都會問：會不會新增使用者？需不需要 data model migration 改資料庫？），所以不能直接照抄別人的。
- Subagent 的模型路由：Theo 公開了他 `CLAUDE.md` 的相關段落——主 orchestrator 應持有一張依 **cost、intelligence、taste** 排名的 model graph 來派工。作者未把它寫進 `CLAUDE.md`，但手動照這個思路在不同模型間路由，並認為 Theo 的排名大致準確。
- Codex 模型原本只能經 CLI 使用，但 OpenAI 已為 Claude Code 做了 plugin（用 slash command 安裝，需先裝 Codex CLI），提供一組可用指令。作者已大量使用 Codex，**專門用於 review 工作**——他們認為 Codex 模型更擅長審查其他模型的產出（尚未與 Fable 5 正面比較過）。

## 用 Ponytail 讓 Fable 寫更少代碼

- 例外情境：Fable 5 **特別擅長為困難問題找出有創意的解法**，所以偶爾直接拿它寫 code 也很好用——但成本太高的問題仍在。
- 解法是 Ponytail：一組讓 AI coding agent **寫更少代碼**的規則集（本質是一串老派 coding 規則，沒有新東西），對 refactoring 特別強。
- 前提：app 已有使用者時直接讓它砍代碼很可能改壞東西，**必須先有 TDD 結構**才能安全使用。
- Ponytail 是 Claude Code plugin，附帶 skills 等內容物，但你只需要它 `skill.md` 裡的 prompt——貼進主 `CLAUDE.md`，或在用 Fable 5 寫 code 前當 prompt 貼上即可。
- 有測試護欄後，Ponytail 重構出來的任何代碼只要測試通過就可信任，可以持續改動代碼、持續蓋功能。

## TDD：測試先行、由獨立 agent 撰寫

- 每個新功能先依 PRD 寫測試，agent 再寫 code。unit test 針對單一單元（例：dashboard 的設定按鈕點了要開選單，測試保證這件事持續成立），整個 app 都有對應測試，任何改動後都跑一遍。
- 關鍵原則：**測試不能由實作的同一個 agent 寫**——同一個 agent 常會寫出「剛好讓自己的錯誤代碼通過」的測試。作者用獨立的 TDD test author subagent 負責寫測試。
- Repo 依此結構化、永遠測試先行之後，不管模型怎麼寫 code，都能確知結果可用。

## Security 與 Code Review 才是主場

- 有一個流傳的 benchmark 聲稱 Fable 變笨、要求它寫 code 會 route 到 Opus。作者認為不實：只有這一個 benchmark 這樣說，且它把 Sonnet 5 排成 reasoning 第一名（明顯不對）；作者長期使用只在「要求解釋 reasoning」時見過改路由，coding 任務沒有，不必恐慌。
- 多數人忘了 Anthropic 釋出此模型的初衷：他們表示 Mythos 太強大，測試顯示它能找到其他模型找不到的安全漏洞（也因此有 jailbreak 能力）。所以應該**把 code review agent 與 security review agent 端出來，特別聚焦 security**。
- 作者的 verification loop 實例（community 平台加新功能與大改版時）：
  - **Code review expert** subagent：建在 Cursor 的 thermonuclear code quality review skill 之上，檢查代碼架構、確保 codebase 在持續加功能時方向正確；實測回報一個必要修改與兩個小問題，已修補。
  - **Security reviewer** subagent：基於 Claude Code security review 這個 GitHub Action（push 代碼到 GitHub 時自動跑的審查）。把該 repo 連結丟給 Claude Code、請它轉成 agent 即可。
  - 對整個平台跑 security review 時，它把平台拆成多個部分、**平行啟動六個基於 Fable 5 的 security reviewer agent**，成果豐碩——挖出大量 bug，均已修補。

## Mockup 先行與合併前 quiz

- Anthropic 的 Tarik 發表了 Fable field guide，記錄他使用 Fable 5 的經驗，並做了說明用的 artifacts（比文章本身清楚）。多數步驟你用舊模型時大概已在做，不必深究；值得採用的兩點：
- **先做 mockup**：作者 repo 有 `design/mocks` 資料夾，放整個網站的 1:1 HTML prototype clone；每個新功能都先加在這個 mock-up 上視覺化，確認後才動工。
- **合併前 quiz**：很多人不看 agent 實作了什麼就 merge。Tarik 提供的 prompt 讓 Fable 在 merge 前主動來考你這些變更——不是逐行讀 code，而是至少掌握 agent 怎麼做到的摘要。
- 作者強烈推薦：不管用 goal 還是 loop，它終會結束，之後要加功能、改專案；**對 codebase 沒有 context 就無法駕馭 agent**，到時一定反咬你。
