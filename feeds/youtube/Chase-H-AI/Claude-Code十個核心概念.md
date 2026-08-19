---
title: 21 分鐘講完 Claude Code 每個核心概念
description: 從模型 effort 選擇、prompting 與 context 管理，到 skills、hooks、routines、loop engineering 與 UltraCode 動態工作流的十個概念
created: 2026-08-19
updated: 2026-08-19
source: https://www.youtube.com/watch?v=eF20iepBQCU
published: 2026-08-18
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - workflow
  - loop-engineering
---

## 模型與 effort level

大不一定好，只會更貴。作者用一份長時程 agentic 任務的基準（影片稱 Deep Suite，指要跑數小時才完成的複雜專案）說明成本與品質的關係：

- Fable 高 effort：low 檔約 $3.76、完成率約 60%；high 檔約 $9.18、完成率約 69%——這一段的加價換得到品質。
- 再往上 extra high：完成率只多約 1%，成本卻從約 $9.18 跳到約 $13。
- 再到 max：又多約 $9，輸出卻持平。
- Opus 與 Sonnet 也是同樣趨勢。

實務 rule of thumb：

- 多數任務停在 **Fable 5 medium**。
- 撞到 Fable 用量上限就換 **Opus 5 medium**；作者觀察 Opus 在 medium 檔比較不囉嗦、不過度複雜化。
- 真的遇到複雜任務時，兩個模型都還有往 high 推的空間。
- 一般情況不建議用 Sonnet 5。

## Prompting：只有兩件事

大家都把 prompting 想得太複雜，其實只要：

1. **要開新專案就先進 plan mode**，讓你跟 Claude Code 先對齊。
2. **prompt 裡只需兩樣東西**：講清楚**目標**（你要達成的終態），以及**叫它反問你問題**。

不需要「你是資深軟體工程師」這類角色扮演，也不需要把每個步驟、每條限制都先寫出來。讓它反問，它會自己挖出你的盲點——需要哪些限制、要走哪些步驟、終點長什麼樣。反過來，沒有這段來回，Claude Code 只會回歸平均值，產出很通用的東西。等到來回討論到你滿意它的計畫，再開始執行。

## Token 與 context 管理

用 `/context`（或桌面版下方的按鈕）可以看到目前 context window 的使用狀況，例如「1M 中用了 18%」。

心智模型（簡化、不是精確機制）：一個字約等於一個 token，你給它的每個字、它回你的每個字都會累積。這件事重要的原因有兩個：

- **成本**：這個視窗填得越滿，該 session 每次互動就越貴。
- **品質**：填得越滿，Claude Code 表現越差。沒有明確的門檻數字，但約莫 **30%** 之後品質就開始接近線性下滑。

所以到了 30–50% 就該問自己要不要開新對話：

- `/clear`：清掉目前談過的一切。
- `/compact`：把談過的內容壓成摘要後接續新的 session。
- 或直接開一個新視窗。

重點是：專案已經產出的程式碼還在磁碟上，新對話隨時可以再讀，不是從零開始。

## CLAUDE.md 與記憶

CLAUDE.md 就是一份 markdown 文字檔，Claude Code 每個 session 開頭都會讀它。裡面放的是「你希望它永遠遵守」的指示——等於隱形地黏在你每一個 prompt 前面，所以放進去的東西最好真的重要。

- **不需要**做成很龐大複雜的 CLAUDE.md，**less is more**。
- 分兩層：**全域** CLAUDE.md 放在 Claude Code 自己的資料夾，不論在哪個專案都會被讀；**專案層** CLAUDE.md 只在該專案生效。全域那份影響所有專案，更該小心不要塞垃圾。
- 不確定自己的 CLAUDE.md 合不合理，可以跑 `/doctor`——它會檢視所有 CLAUDE.md 是否臃腫並給建議。

## Skills

Skill 的本質就是 prompt。以 Anthropic 官方的前端設計 skill 為例，它就是一大段告訴 Claude Code 該怎麼做前端設計的文字；把整段貼進對話跟叫 `/frontend-design` 是同一件事，差別只在你不用每次重貼。

兩種 skill：

- **補強型**：讓 Claude Code 在它原本比較弱的領域（例如前端設計）做得更好。
- **自動化型**：把一連串動作固定成特定順序。作者的 morning intel skill 就是這種：去掃過去 24 小時的 YouTube、Twitter、Reddit 與 Gmail，找 AI 相關動態，最後綜合成一份報告。手動做過幾次後叫 Claude Code 把流程寫成 skill，之後每次執行順序都固定，不會跑出奇怪的結果。

外面現成的 skill 很多，但**最有價值的是照你自己工作方式做的自訂 skill**。最省事的做法是叫出內建的 skill-creator skill（沒有的話直接叫 Claude Code 去下載），然後請它讀你過去 30/60/90 天的使用記錄，從你實際重複在做的事反推出幾個 skill。

## Plugins、CLI 與 MCP

這一類東西的目的都一樣：讓 Claude Code 能操作外部應用（Gmail、Notion 等），你只要坐在前面看它做事。

桌面版把它們叫 connectors 和 plugins，底層通常就是一個 MCP 或一個 CLI，術語不用太糾結。實務上：

- 幾乎所有主流軟體現在都有對應的 connector；connectors 目錄裡找不到的，去 GitHub 搜 MCP 或 CLI 多半找得到。
- 安裝很簡單：把該工具的網址複製進 Claude Code，叫它「install this CLI」即可（作者示範 Playwright CLI）。
- 不知道該裝哪些？**直接問 Claude**——開新專案時就把「這個專案有沒有適合的 MCP／CLI／connector」列進你要它回答的問題，它會上網查、也能幫你裝。

作者的判斷：到了現在這個階段，幾乎沒有理由把 Claude Code 的輸出複製貼到別的地方、或自己手動走完流程——通常都有對應的 CLI 或 MCP。

## Hooks

Hook 就是規則：**每當 X 發生，就做 Y**。

作者自己的例子：任務完成時播一個提示音。他常常切到別的分頁，聲音一響就知道該回來看了。

設定方式一樣是用講的——「幫我建一個 hook，每次任務完成就播提示音」，它就會幫你設好。不知道該設哪些 hook，做法同 skill：叫 Claude Code 看你過去 30/60/90 天的使用記錄，讓它建議。

## Automations（routines）

Skill codify 之後，下一步就是不要再手動叫它。以 morning intel 為例，它應該每天自動跑。

桌面版做法：左側進 **routines** → new routine：

- **local vs cloud**：多數情況選 local。跑在雲端等於在 Anthropic 的伺服器上，需要碰你本機東西的自動化會很麻煩。
- 填名稱與描述（例：morning report／我的晨間簡報）。
- **instructions 幾乎不用寫**——因為任務已經 codify 成 skill 了，直接寫 `/morning-brief` 就好。這正是先做 skill 的價值：流程已經手動驗證過能動，現在只是把它自動化。
- 其餘設定：權限建議 auto、選模型（不一定需要 Fable 5，作者認為 Opus medium 是不錯的中間值）、選資料夾、設排程，然後建立。

作者提到 routines 目前約可設到每天 15 個；但你也可以讓自己的電腦用排程／腳本去啟動 Claude Code，所以並不真的被那個數字綁死。

## Loop Engineering

Loop engineering 就是在 Claude Code 裡建立**朝著明確成功標準前進、且會自我改善**的自主迴圈。四個要件：

1. **觸發（trigger）**：事件驅動或時間驅動。morning report 就是時間驅動，每天早上 8 點。
2. **任務（task）**：這個迴圈實際做什麼。以 morning report 為例是抓 YouTube／Twitter／Reddit、收信、綜合、產報告。
3. **成功標準（success criteria）**：最難的一環。「一份好報告」是什麼？必須落成客觀量測——例如至少要有幾個 YouTube 來源、Twitter 要有哪一類 insight；主觀成分高的任務可以再加一道人類評分（1 到 10 分快速打分）。相對地，若目標是「讓這支 Python 應用跑進 1 秒」，每次迭代好不好判斷得一清二楚（2 秒 → 1.9 秒就是有在往對的方向走），loop 就好做很多。
4. **記錄（log）**：把每次迭代與評分寫下來。下一輪跑之前先讀 log，看看被打到 9、10 分的報告長什麼樣、是什麼造成的，然後複製那些做法。

有了「目標 + 可回看的過往迭代」，一直循環下去就是自我改善迴圈；複雜或簡單都可以，骨架就這四步。

## 動態工作流與 UltraCode

UltraCode 是一個 effort 設定。開啟後等於授權 Claude Code 把你交付的任務轉成**動態工作流**——一支 JavaScript 腳本，用來大規模編排 sub-agent。不是 5 個、10 個，而是可能上百個，而且編排方式是針對你這個問題客製的。

影片列出六種動態工作流架構範例：

- **classify and act**：一個 sub-agent 當分類器，依分類把不同任務推給各自的專門 agent。
- **fan out and synthesize**
- **adversarial verification**
- **generate and filter**
- **tournament style**：跑一系列嘗試，再由外部裁判 agent 逐輪比出最後贏家。
- **loop until done**：跟前一節的 loop engineering 很像。

內建的 deep research 其實就是動態工作流，隨時可用 `/deep-research` 叫起來，而且它是上面兩種架構的組合：先 fan out 派 20–50 個 sub-agent 上網找資料，再用 adversarial verification 逐條判斷哪些說法站得住腳，最後才給你綜合報告。所以架構之間是可以疊的，那六種也不是窮舉。

**成本警告**：動態工作流與 UltraCode 非常貴。跑 deep research 時若你在 Fable 上，它預設會把上百個 sub-agent 全部開成 Fable agent。但你不是只能吃預設值——呼叫時可以直接下參數，例如「只用 Opus agent」「最多 20 個 agent」。不給任何限制就準備燒掉數百萬 token、把用量打爆。

作者的用量感受：即使用 Fable，一次 deep research 在 $200／月方案上大約吃掉每週總用量的 3–5%。想放手讓 UltraCode 自由發揮客製工作流，建議挑週用量快重置前再跑，才不會一次燒光。這仍是處理高複雜度問題時很強的工具，只是要省著用。
