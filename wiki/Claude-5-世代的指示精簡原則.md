---
title: Claude 5 世代的指示精簡原則
description: 查證 AI懶人報 EP478 的 CLAUDE.md 精簡建議，整理該刪的指示、effort、subagent 與驗收做法，並標出證據限制
created: 2026-11-19
updated: 2026-11-19
source: https://www.youtube.com/watch?v=K_0UezrjoKo
published: 2026-11-17
parent: "[[wiki/01.index]]"
tags:
  - claude-code
  - context-engineering
  - coding-agent
  - evaluation
---

2026-11-19 研究 [AI懶人報 EP478](https://www.youtube.com/watch?v=K_0UezrjoKo) 的回存，影片主張逐項回查它引用的 Anthropic 原文。**證據強度**：官方文件與 Anthropic 部落格為一手來源，但效果數字都是廠商自測；Lance Martin 演講只讀 YouTube 機器字幕，數字與措辭可能有辨識誤差。影片畫面與 `/doctor` 輸出未核對，指令也未實跑。

**一句話**：影片的做法大致站得住，核心是「CLAUDE.md 只寫 Claude 猜不到的事，長流程改成按需載入」。但目前沒有公開數字證明精簡 CLAUDE.md 能省多少 Claude Code 額度，刪完仍要用自己的任務驗收。

## 影片主張的查證結果

| 影片主張 | 查證結果 | 依據 |
|---|---|---|
| Claude Code system prompt 砍掉超過八成，coding 測試沒退步 | **成立，有適用範圍**：原文限「Opus 5、Fable 5 這類模型」與內部 coding eval；部分內容是搬進 skill 與延遲載入工具，不是全部刪除 | [Thariq Shihipar](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) |
| 砍法有三個方向 | **簡化**：原文列六組舊做法與新做法，影片取其中三組 | 同上 |
| 不用再叫 Opus 5.5 想，拿掉 think carefully 回覆較快、品質無明顯下降 | **成立**：測試場景是聊天產品；官方另建議從 prompt 與常駐指示移除同類句子 | [Prompting Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)、[Addy Osmani](https://claude.dev/blog/getting-the-most-out-of-opus-5-5) |
| 舊式提示會增加成本、有時更差 | **成立但證據偏窄**：演講的實驗是約 50 張客服工單的合成評測，刻意注入反模式後取平均，不是 Claude Code 的 CLAUDE.md 實測 | [Lance Martin 演講](https://www.youtube.com/watch?v=ys6YQ2yfBpM) 約 3:30–5:00 |
| `/checkup` 是 `/doctor` 別名，`prompt-audit` 先報告、確認才改 | **成立**：預設涵蓋 `CLAUDE.md`、`CLAUDE.local.md`、`AGENTS.md`，以及 `.claude/` 與 `~/.claude/` 下的 rules、skills、commands、subagents、output styles；需要較新版本，確切版本見官方文件 | [Commands](https://code.claude.com/docs/en/commands)、[Memory](https://code.claude.com/docs/en/memory) |
| Opus 5.5 預設 `medium`，追平或超過 Opus 5 `high` | **成立**：這是 Anthropic 自測；同一等級下 Opus 5.5 每輪想得更多，不要沿用舊設定 | [Prompting Opus 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)、[Model config](https://code.claude.com/docs/en/model-config) |
| 工單測試第一步換 Opus 5.5 low，成本砍半 | **順序與歸因不精確**：第一步其實是 prompt audit；省下的錢也有一部分來自 Opus 5.5 單價較低 | [Lance Martin 部落格](https://claude.dev/blog/automating-eval-design-and-hillclimbing) |
| 最終成本約五分之一，未看過題目答對率 79% → 90% | **成立，樣本小**：holdout 只有 14 張工單（78.6% → 90.5%），最終設定是 Sonnet 5 low 加上改良 prompt | 同上 |
| subagent 只在三種情況保留 | **條件正確，情境被延伸**：原文談企業在 Claude Platform 上建的 agent，不是個人 Claude Code 的 subagent 配置 | [Applied AI 文章](https://www.claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop) |
| 快取讀取約一般輸入的十分之一，Opus 5.5、Sonnet 5.5 更便宜 | **成立**：多數模型 0.1 倍，這兩款 0.05 倍 | [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) |
| 把快取用對，成本最多降 72% | **成立但是上限**：演講說部分內部 harness 原本沒用好快取，已用好的專案不會有這種幅度 | Lance Martin 演講約 7:30–8:00（機器字幕） |

## 怎麼精簡 CLAUDE.md

**刪或改**：

- 叫模型思考的句子，例如「一步一步想」，直接刪。想調整思考量就改 effort。
- 空泛叮嚀，例如「務必詳盡」「再檢查一遍」。真的要檢查就改成可驗證的要求，例如「改完跑測試，列出失敗項」。
- 互相衝突的規則，只留一條，或寫清楚各自的適用條件。Thariq 的說法是衝突會讓 Claude 多花心力判斷；Lance 則說前沿模型常被矛盾規則搞混。
- 看 repo 就知道的事，例如框架與目錄位置。

**搬走**：長的驗證、部署步驟做成 skill，CLAUDE.md 只留一句指向它。

**留下或補上**：程式碼看不出來的地雷、完成條件，以及何時該停下來問人。[Addy Osmani 的指南](https://claude.dev/blog/getting-the-most-out-of-opus-5-5)建議把「只有無法繼續或要做破壞性操作才停」這類規則寫進 CLAUDE.md。

這和 [[Context-優先與多-agent-的適用邊界]] 的判準一致：缺知識就補 context，不是多建 agent。各工具怎麼載入這些指示檔，見 [[Coding-agent-指示檔與規則載入機制對照]]。

## 影片沒講清楚的限制

- **刪驗證句和降 effort 會疊加**。演講說新模型會自然驗證，但 [Thariq 的 effort 測試](https://claude.dev/blog/spending-your-effort/)發現 effort 正是在調節驗證與邊界測試的多寡，low 的失敗案例常是沒充分檢查。重要工作要保留可驗證的完成條件，驗證階段用 `high`。
- **精簡不等於規則越少越好**。上述工單案例的最後一步是**加上**路由規則與退款上限的對照，搜尋集分數從 88.9% 升到 98.9%。該加的是模型猜不到的領域規則。
- **從 Opus 5 升級不必急著重寫**。官方指南說既有 Opus 5 prompt 應可照常運作，可以先測再改。
- **要求把思考過程寫進回覆可能被拒**。Opus 5.5 對這類 prompt 可能回 `reasoning_extraction` 拒絕，API 應改讀 summarized thinking。這比「浪費 token」更具體，影片沒提。
- **API 端調 effort 會影響快取**。請求之間改頂層 `effort` 會讓快取的 messages 失效，對話中途要改應使用 per-message effort（目前為 beta）。
- **額度問題要先量再改**。`/context` 可看 context 被什麼佔用，`/doctor` 在訂閱方案下也會依近 7 天用量提出建議。影片把額度問題歸到 CLAUDE.md，但沒有提供節省幅度。

## 改完怎麼驗收

影片的做法可用：保留舊設定，挑約 10 個真實任務，每次只改一項，新舊並排比較。[Applied AI 文章](https://www.claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop)也說 10 個 golden examples 足以起步。

有兩點要比影片嚴格：

- **每個任務跑不只一次**。影片說新舊各跑一次，但同一篇文章要求重複執行，因為它的案例有個退化只在兩次中出現一次。比較時也要看哪些任務由過變不過，不能只看總分。
- **題目要包含真正難的案例**。[評測設計文](https://claude.dev/blog/automating-eval-design-and-hillclimbing)反對只收某模型答錯的題目，但也提醒只取日常流量會偏簡單，應納入人判斷為困難、能說出難在哪的案例。

主觀品質適合兩兩比較，Lance 在問答中說這比打分數容易。

## effort 怎麼選

依 [Thariq 的個人經驗法則](https://claude.dev/blog/spending-your-effort/)，屬單一工程師經驗，官方 [Model config](https://code.claude.com/docs/en/model-config) 對 `medium`、`high` 的描述與其相近：

| 等級 | 適用 |
|---|---|
| `low` | 腦力激盪、草稿、簡單修改，人還在迴圈內 |
| `medium` | 多數日常開發，例如範圍清楚的新功能 |
| `high` | 重視驗證或邊界情況，例如修舊專案的 bug |
| `max` | 要它完全自主處理的困難任務 |

「較強模型配較低 effort，常比較弱模型配高 effort 便宜又好」是 Lance 的經驗法則，不是定律。他的工單案例最後反而降到較便宜的 Sonnet 5，仍要靠 eval 決定。

## 勿引用

- 「Hillclimb 省下 90% 成本」：演講機器字幕出現此數字，部落格寫的是約五分之一成本（約省 80%）。**勿引用 90%**，以部落格為準。
- 「精簡 CLAUDE.md 能省 X% 額度」：本次查到的來源沒有這個數字。72% 是 API 快取，80% 是 system prompt 字數，都不能套用。

## 交叉引用

- 判準來源：[[Context-優先與多-agent-的適用邊界]]——本頁的 subagent 收斂建議補上 Anthropic 較新的單一 agent 加 skill 論點，適用情境仍以企業 agent 為主。
- 載入機制：[[Coding-agent-指示檔與規則載入機制對照]]——該頁說明指示檔怎麼載入，本頁說明裡面該寫什麼。
