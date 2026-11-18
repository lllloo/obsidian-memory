---
title: Matt Pocock 的 PR 瓶頸解法
description: 查證 Matt Pocock 演講與 AI懶人報 EP412，整理自動檢查、AI review、人工 review 三層做法，並對照其 skills 實作差異
created: 2026-11-19
updated: 2026-11-19
source: https://www.youtube.com/watch?v=T-5FW3KRpgI
published: 2026-10-02
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - testing
  - skill
---

2026-11-19 研究 [AI懶人報 EP412](https://www.youtube.com/watch?v=T-5FW3KRpgI) 的回存。影片整理 Matt Pocock 在 AI Engineer Paris 2026 的演講〈[Fixing the PR Bottleneck](https://www.youtube.com/watch?v=LlgiOCmFG_w)〉，本頁回查演講與 [mattpocock/skills](https://github.com/mattpocock/skills) 當日內容。**證據強度**：這是單一實踐者的方法論，演講沒有提供前後對照數據，他的依據是「對我非常有效」；GitHub 星數只代表受歡迎程度。演講只讀 YouTube 機器字幕，skill 未實跑。

**一句話**：先用自動檢查和 AI review 提高 PR 品質，人只把注意力放在難以回復的改動上，再把重複出現的 review 意見變成檢查或規範。方向實用，但影片說「直接裝來用」不夠精確：現行 `code-review` skill 只回報問題，不會自己 commit。

## 影片主張的查證結果

| 影片主張 | 查證結果 | 依據 |
|---|---|---|
| 三層煞車：自動檢查、AI review、人工 review | **成立**：目標是用前兩層讓人工 review 變快 | 演講約 3:00–4:00 |
| 測試會說謊，例子是把實作再寫一次 | **成立但影片只講一種**：演講另有讀原始碼判斷 UI 順序的結構敏感測試，以及 mock 後不可能失敗的測試 | 演講約 5:00–8:00 |
| 深模組讓測試集中在小介面 | **成立**：概念來自 John Ousterhout；`tdd` skill 也要求透過公開介面驗證行為 | 演講約 8:30–9:30、[`tdd`](https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md) |
| `improve-codebase-architecture` 找可加深的模組 | **成立**：產生視覺報告，再針對選定項目追問 | [skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md) |
| 規範放 `coding-standards.md`，只交給 review agent | **主張成立，檔名要更新**：現行 skill 指名 `CODING_STANDARDS.md`，也會搜尋其他規範文件 | [`code-review`](https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md) |
| review agent 預設直接 commit，skill 可直接裝來用 | **演講主張成立，現行 skill 不是這樣**：`code-review` 用兩個 subagent 回報 Standards 與 Spec 問題；`implement-spec` 再把問題交給新的 implementer subagent 修 | 同上、[`implement-spec`](https://github.com/mattpocock/skills/blob/main/skills/engineering/implement-spec/SKILL.md) |
| PR 標單向門、雙向門與 blast radius | **成立**：`pr` skill 的 `Merge Danger` 區塊有這兩項，另要求摘要圖與前後證據 | [`pr`](https://github.com/mattpocock/skills/blob/main/skills/engineering/pr/SKILL.md) |
| `retro` 把重複問題變成檢查或規範 | **成立**：機械性違規優先做確定性檢查；它提出候選項，由人決定，需手動呼叫 | [`retro`](https://github.com/mattpocock/skills/blob/main/skills/engineering/retro/SKILL.md) |
| skills repo 今年 2 月建立、27 萬多星 | **成立**：建立於 2026-02-03；2026-11-19 查詢時約 32.7 萬星，影片數字是當時快照 | GitHub API |

## 可直接採用的做法

1. 列出 PR 實際經過哪些層，先補空著的自動檢查。檢查不花 token，最適合先加。
2. 測試從公開介面驗行為。看到重述常數、讀原始碼字串、或 mock 到不可能失敗的測試，就改寫或刪除。
3. 第二次寫同一句 review 意見時停下來：機械性問題做成 lint、型別或 CI；需要判斷的才寫進規範。這與 [[Lauren-Tan-把糾正寫進程式庫]] 的優先序一致。
4. 每個 PR 寫明能否回復與影響範圍。寄信、資料遺失、昂貴遷移都算單向門，即使 diff 很小。

## 影片沒講清楚的限制

- **`code-review` 不是完整的 AI review 層**。[官方說明](https://github.com/mattpocock/skills/blob/main/docs/engineering/code-review.md)指出，要找 null path、race、off-by-one 等 bug，應使用 Claude Code 內建 review，不是這個 skill。它查的是規範和 Spec 是否符合。
- **「review 很輕」和「review 要 commit」有張力**。演講用 reviewer 不必實作、除錯來說明 context 較空，接著又主張 reviewer 預設要改碼並 commit。現行 skill 把修復交給另一個 implementer，反而較符合前一個前提。
- **規範全搬出 `AGENTS.md` 是取捨，不是定論**。Anthropic 的 [Best practices](https://code.claude.com/docs/en/best-practices) 範例仍把影響寫法的少量慣例放在 `CLAUDE.md`。本頁判讀：能機械檢查的進 lint；寫錯就會走錯方向的少量慣例留在常駐指示或 path-scoped rules；風格與品味再交給 review，避免 implementer 先照錯的方向做完才返工。
- **雙向門可能被標錯**。`pr` skill 由寫 PR 的 agent 填寫，而演講的「改一點卻寄信給 6 萬人」正是作者容易漏看的情況。涉及資料寫入、對外通知、權限與遷移的路徑，宜用規則強制列為高風險，不只靠自評。
- **自動 commit 後要重跑檢查**。reviewer 改完的版本才是人要審的版本，CI 必須針對最新 commit 再跑一次。
- **先確認瓶頸真的在 review**。[[AI-產碼加速下的-review-瓶頸]] 記錄了另一種觀點：若通過 review 的變更仍排隊等部署，加快 review 只會把壓力往下游推。

## 演講有、影片略過的重點

Matt 建議不要把自動 review 完全外包，因為通用工具不是太泛而誤報，就是太專而不適用；團隊應逐步累積自己的規範。`pr` skill 也強調用虛擬碼、呼叫樹或 Mermaid 讓人快速看懂改動，不只標風險。

## 交叉引用

- 測試品質：[[用測試約束-AI-產碼]]——該頁用 mutation testing 等手段檢驗測試是否可信，本頁提供從模組設計減少壞測試的做法。
- 同型做法：[[Lauren-Tan-把糾正寫進程式庫]]——兩者都把重複糾正變成環境約束；Tan 更強調 API 與架構，Matt 更聚焦 PR 流程。
- 瓶頸判斷：[[AI-產碼加速下的-review-瓶頸]]——該頁檢驗「瓶頸在 review」這個前提，本頁是前提成立時的一套流程。
- 放手運行：[[Claude-Code-放手運行的安全與驗證]]——該頁說明 session 無人值守時的安全與驗證層，本頁處理 PR 產出後的 review 分流。
- 指示精簡：[[Claude-5-世代的指示精簡原則]]——兩頁都主張縮小常駐指示，但對專案慣例該留多少有不同取捨。
