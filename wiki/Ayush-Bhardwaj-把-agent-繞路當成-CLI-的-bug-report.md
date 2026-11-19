---
title: Ayush Bhardwaj 把 agent 繞路當成 CLI 的 bug report
description: 深讀 Bhardwaj 演講並回查一手來源：從對話紀錄挖 agent 重複的 pipe 繞路來改 CLI，附照做步驟與數字強度
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-ayush-cli
published: 2026-11-12
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - evaluation
---

# Ayush Bhardwaj 把 agent 繞路當成 CLI 的 bug report

來源：AI Engineer CODE 2026 線上場〈Your Agent Hates Your CLI〉的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Bhardwaj-Your-Agent-Hates-Your-CLI]]（Day 2 直播 YouTube `y9JtCCZP2MQ`，1:46:46–1:59:04，約 12 分鐘）。2026-11-19 回查他引用的 Sanity、Infracost、DuckDB 文章、兩篇 arXiv 論文、Claude Code 官方文件與 issue，以及他自己的工具 repo。

**一句話**：agent 不會回報 CLI 難用，它會在你的指令外面再寫一小段程式（`| head`、`| grep`、`| python`）繞過去。偶一為之沒問題；同一種繞路反覆出現，就是一張沒人提的 bug report。對話紀錄就是你沒在看的產品分析資料。

## 講者與立場

Ayush Bhardwaj，所屬 Allos AI（演講標題的公司名，演講中沒有介紹）。他寫了 `chat-history`：讓 coding agent 搜尋自己在 Claude Code、Codex、Cursor 的歷史對話的 Rust CLI，附一份 skill 讓 agent 自己決定何時呼叫。演講的案例幾乎都來自改這個工具的過程，結尾也直接推薦它（「check out Chat History on Cargo or GitHub」）。

**立場**：有推自家工具，但這個工具是 MIT 開源、個人規模的專案（查詢當下 GitHub 十幾顆 star、crates.io 數百次下載），演講的方法本身不依賴它。要警覺的是：他所有關於「改 CLI 之後 agent 行為變好」的數字，都是在自己的工具、自己的對話紀錄上量的。

## 演講脈絡（依順序）

### 1. 開場：三個「剛好都對」的裁切（1:46:46–1:47:42）

都是他自己對話紀錄裡的真實呼叫：

- **Claude Code** 要查文件頁上的一個設定，下載整頁、grep、只留 40 行。這一次其實是 agent 在幫他 review 這場演講的稿子，「它還是忍不住」。
- **Codex** 要知道有幾個相依套件有漏洞，拿整份 JSON 報告、只留最後 40 行，因為這份報告把總數放在結尾。
- **Cursor** 跑測試、有一個失敗，只留最後 80 行。

三次都剛好留住了答案，但每一次都**把「答案在輸出的哪個位置」的假設寫死在指令裡**。這會把摩擦藏起來，工具作者看不到：一個 pipe 說明不了什麼，同一個 pipe 反覆寫，就指出工具缺了某個東西。

### 2. agent 不回報 bug（1:47:46–1:48:18）

Sanity 的 MCP server 上線以來有兩萬多個 agent、約三百萬次工具呼叫，卻沒收到 bug report。他們後來加了一個讓 agent 回報問題的工具（逐字稿辨識成「GIF feedback tool」，實際是 `give_feedback`），agent 有地方抱怨之後才開始說哪裡不對。他的轉折是：你不需要先做回報工具，回饋已經在你的對話紀錄裡。

### 3. 量化：pipe 有多常見，以及會出事的地方（1:48:23–1:49:45）

- 他從自己的對話紀錄抽出約 **20,000 次** agent 呼叫，涵蓋 14 個 CLI（git、GitHub CLI、cargo、curl、npm、docker 等）。
- 約**四分之一**把輸出接進 `head`、`grep`、`tail`、`python`、`sort`、`wc` 這類過濾器；讀取為主的指令超過一半，`git show` 和 `cargo test` 各 62%。
- harness 差異很大：Codex 讓 agent 每次呼叫自己設輸出上限，pipe 就少很多。
- **pipe 不只是砍雜訊**：bash 沒開 `pipefail` 時，pipeline 的退出碼是最後一個指令的。`cargo test | head` 可能在測試失敗時回報成功。投影片例子是「編譯錯誤＋綠點」：狀態錯了，但錯誤訊息還在畫面上，agent 仍讀得到。
- **更糟的是 pipe 把錯誤本身也切掉**：Claude Code 的 GitHub issue 裡，腳本拋 ReferenceError、非零退出，`tail` 只留下三行無害輸出，Claude 回報成功。錯誤從頭到尾沒進到模型。
- **建議：fail loudly**。工具失敗時，最後幾行固定放一段簡短摘要和完整 log 的路徑；就算 agent 只看 `tail`，也看得到失敗。

### 4. 他自己的工具：pipe tax（1:49:45–1:51:45）

- 10 月他對自己的工具做了一次稽核，記錄約 **1,000 次**呼叫，是一個小型個案。方法適用任何 agent 會呼叫的東西：**看 agent 呼叫完之後立刻做了什麼**。
- **80%**（五次有四次）用他的工具打開舊 session 時，輸出直接被接進 `grep`、`sed`、`head`、`tail` 或 `python`。他把這叫做 pipe tax（逐字稿辨識成「pipe text」，依上下文判斷應為 tax）。pipe 把垃圾擋在 context 外沒有錯，問題是 agent **每次都手寫同一個裁切指令**，每一次都是在猜答案在哪裡。
- **合理的反對意見**（來自 Hacker News 一串「為 agent 設計 CLI」的討論）：讓 agent 自己決定讀多少就好，它很會用 `grep`、`head`。他的回答：一次性的情境本來就該這樣；但在那些日常 CLI 上，**83%** 的 pipe 屬於「同一個 CLI 子指令＋同一個 pipe 工具出現至少 10 次」的重複模式。參數可以不同，agent 要的是同一件事。
- **輸出為什麼大**：同一個長 session，整份打開是 **120 萬字元**，只取搜尋命中周圍約 **3,000 字元**。harness 會限制輸出大小，但**大小上限不會挑出相關的訊息**；選擇型旗標才能讓 agent 告訴工具它要哪一段。

### 5. 三個例子：左欄是 bug report，右欄是修法（1:51:45–1:52:47）

| agent 的繞路 | 它其實在說 | 他在 `chat-history` 的修法 |
|---|---|---|
| 用 `rg`、`sed` 過濾 session 內容 | 讓我挑我要的那段 | `view` 可以只回命中周圍、只回命中的訊息，或最後幾則加大小上限 |
| 用 Python 處理 JSON | 給我少一點欄位 | `search` 加 compact 模式：一筆一行，約為 JSON 的六分之一大，結果相同 |
| 用 for 迴圈逐一 `inspect` 多個 session（約三分之一的 inspect 呼叫是這樣來的） | 讓我一次問好幾個 | `inspect` 一次接受多個 session ID |

「我的 roadmap 就在我的指令周圍的那些指令裡。」

**旁證 Infracost**：這家雲端成本工具 5 月也寫了同樣的發現。agent 在 JSON dump 上寫 `jq` 和 Python pipeline，他們把過濾搬進 CLI、加 compact 格式和教 agent 用的 skill。沒有這些的 Claude 在困難題答對 0/6，有了之後 6/6，整份 benchmark 成本降 41%。他也引用該文作者在 HN 上說的：讀這些 agent log 就像在看 usability test。

### 6. 文件是介面的一部分（1:53:19–1:54:22）

- 把功能做進 CLI 之後，要用 skill 檔或 `--help` 告訴 agent。「這聽起來很理所當然」，但 **agent 把你教的東西當字面照做**。
- 他的實驗：某次改動讓 `--deep` 旗標變成 no-op，他刻意讓 skill 繼續叫 agent 用它，看 agent 會不會自己發現。結果 **95 次搜尋裡 95 次都還帶著這個旗標**。之後有兩個 session 載入了改寫過、不再提它的 skill：這兩個 session 的搜尋都沒帶 `--deep`，而且第一次讀取就試用了新旗標。
- 結論：`SKILL.md`、help 文字、錯誤訊息**就是介面**；過時的文件就是 bug，因為 agent 會一直照著做。
- 新旗標傳到 agent 之後：幾乎每次搜尋都用 compact 輸出，幾乎每次讀取都用新旗標；**被 pipe 的讀取從 82% 降到約四分之一**。

### 7. 用對話紀錄當測試集（1:54:22–1:55:06）

- agent 實際跑過的指令就是測試案例，agent **緊接著做了什麼**是粗略的答案。
- 把這些指令分別丟進舊版和新版重播：
  - 改了排序：確認 agent 後來實際採用的那筆結果還在最前面。
  - 改了輸出格式：確認沒有東西不見。
  - 改了預設值：看哪些指令的行為因此改變。
  - agent 立刻用不同參數重打同一個呼叫：多半是找到一個失敗案例。
- 這份答案只是猜測 agent 想要什麼，所以**留一部分案例不看，用來給修法打分**。

### 8. 重來一次會先做什麼（1:55:06–1:56:05）

- 在 20,000 次呼叫裡，**55%** 的 pipeline 下游只有 `head`、`tail` 或 `sed`，代表需求是「更小的切片」。所以**先做範圍與上限**，別先做花俏功能。
- **旗標要 agent 願意用才有用**：GitHub CLI 的 list 指令有 `--limit`，agent 有 81% 的時候會用；反例是 cargo，`cargo test` 的 quiet 模式每個測試印一個字元、仍會回報失敗，但 agent 大約十次只用一次，其餘都用 pipe。所以要在 help 和 skill 裡教。
- **大輸出預設少印，並說怎麼拿更多**：例如結尾寫「showing 20 of 300, add `--offset 20` for the next page」。

### 9. Agent mode 與「省 token 不等於變好」（1:56:05–1:57:00）

- 一次做完上述幾項的方法是 **agent mode**：CLI 偵測到是 agent 在呼叫就換一種輸出。Claude Code 這類 agent 會在它開的 shell 設環境變數，工具可以據此判斷。
- **DuckDB** 做了一個：終端機上是畫線表格，agent 拿到的是純表格，並註明省略幾列、怎麼拿；超大查詢會提早停下並說明；錯誤以 JSON 回傳。模型讀到的輸出少了 **59%**，但省下的 token 只佔模型總讀取量約 **0.5%**，成本和執行時間都沒有改善。
- 對比 Infracost：那邊是 agent 從答錯變答對；DuckDB 的案例 agent 本來就答對了。所以**要量 turn 數和答對率，不要只量 token**。

### 10. 為什麼不能直接叫 agent 做這件事（1:57:00–1:58:08）

- agent 現在還不擅長一次就設計好。叫它「做一個給 agent 用的工具」，它多半先想像一個人類使用者，再把 agent 支援硬接上去；它會照抄最常見的模式，而那些模式多半很差。
- 佐證：一份研究發現多數官方 MCP server 只是包一層既有 API；另一份檢查真實 MCP server 的工具描述，97% 有問題。文件也一樣：ETH Zurich 測了 agent 寫的 context 檔，對任務成功沒幫助、成本更高、比人寫的差。
- **但 agent 擅長另一半**：給它一份對話紀錄和一個能跑的測試，它能找出問題並改進工具，有時超過人手寫的版本；Anthropic 在自己的內部工具上也回報過這點。
- 分工：**人決定工具應該是什麼樣子，agent 對照實際發生的事去檢查**。

### 11. 怎麼開始（1:58:18–1:59:04）

1. **先備份對話紀錄**，因為 Claude Code 會在 30 天後刪除不活躍的紀錄。
2. 搜尋「工具名後面接 pipe」之類的模式。
3. 如果你發布 MCP server：找 agent **立刻用不同參數再呼叫一次**的情況。
4. 收尾：「如果你在為 agent 做工具，agent 的對話紀錄就是你大概沒在看的產品分析。繞路就是 bug report，去讀你的對話紀錄。」

## 回查結果（2026-11-19）

| 主張 | 結果 | 來源 |
|---|---|---|
| Sanity：兩萬多個 agent、約三百萬次呼叫，加了回報工具後開始收到回饋 | **成立**：原文寫「Over 20,000 agents have made three million tool calls … since it went GA in December 2025」，工具叫 `give_feedback`，後改名 `give_sanity_feedback`；回報常附乾淨的重現步驟，一例揭露 `deploy_schema` 輸入格式從沒寫進文件。文章 2026-06-18 發布，與演講說的「6 月」相符。「一份 bug report 都沒有」這句措辭本次沒逐字核到 | [Sanity 部落格](https://sanity.io/blog/how-to-get-product-feedback-from-agents) |
| Infracost：0/6 → 6/6、成本降 41% | **成立，但要知道條件**：2026-05-18 文章，16 題（11 題可計分，其中困難 6 題）、3 個 Terraform 專案共 1,171 個資源、Opus、每題重複 5 次。困難題 bare Claude 0/6 花 $7.61，用 skill 6/6 花 $2.48；總成本 $16.41 → $9.63（41%，文中自稱是下限）。文章標題的 79% 是困難題的輸出 token 降幅，不是成本。新增的是 `--missing-tag` 等謂詞旗標與 `--llm`（TOON 格式）。廠商自測、無獨立重現。「像看 usability test」那句不在文章內，是 HN 留言，本次未核 | [Infracost 部落格](https://www.infracost.io/blog/we-cut-claude-s-token-usage-79-by-redesigning-our-cli-for-agents) |
| DuckDB agent mode：輸出少 59%、只佔總量約 0.5%、成本與時間沒改善 | **成立**：DuckDB 團隊 2026-10-09 文章，Claude Code 回答 22 題 TPC-H（SF100），開／關 agent mode 各跑 3 次；DuckDB 輸出 123.6k → 50.8k token；132 次全部答對；agent mode 反而多一點 turn（237 對 224）。偵測條件是有已知 agent 環境變數（含 `CLAUDECODE`、Codex、Cursor、Gemini、Copilot 的變數）、stdout 不是終端機、沒指定輸出格式；可用 `-agent`／`-no-agent` 強制。超過上限時印前後各 20 列，註腳寫明總列數與怎麼拿全部 | [DuckDB 部落格](https://duckdb.org/2026/10/09/agent-mode) |
| Claude Code 會在它開的 shell 設環境變數 | **成立**：官方文件說 `CLAUDECODE=1` 會設在 Bash 工具、hook、status line、stdio MCP server 等子行程；IDE 整合終端機也會設，所以要分辨「是不是 Claude 直接開的」要看 `CLAUDE_CODE_CHILD_SESSION` | [Claude Code 環境變數](https://code.claude.com/docs/en/env-vars) |
| Claude Code issue：`tail` 切掉 ReferenceError，Claude 回報成功 | **成立**：anthropics/claude-code #39945「Claude pipes Bash output through tail/head, discarding errors before reading them」，2026-03 開、2026-06 關閉 | [GitHub issue #39945](https://github.com/anthropics/claude-code/issues/39945) |
| Claude Code 30 天後刪除紀錄 | **成立**：`cleanupPeriodDays` 預設 30，背景清理、不顯示訊息，被刪的 session 也不會出現在 `/resume` | [Settings reference](https://code.claude.com/docs/en/settings-reference#cleanupperioddays) |
| 97% 的 MCP 工具描述有問題 | **成立**：arXiv 2602.14878，856 個工具、103 個 server，97.1% 至少有一個 smell，56% 沒講清楚用途。補充演講沒講的：把描述補齊，任務成功率中位數只升 5.85 個百分點，執行步數卻增加 67.46%，且 16.67% 的情況變差。這份檢查是用 LLM 掃描器打分，不是人工標註 | [arXiv 2602.14878](https://arxiv.org/abs/2602.14878) |
| ETH Zurich：agent 寫的 context 檔沒幫助、更貴、比人寫的差 | **方向對，最後一點要保留**：arXiv 2602.11988（ETH 團隊）最新版摘要說 context 檔整體**沒有**提升任務成功率、推論成本平均增加 20% 以上，而且 LLM 生成的與開發者寫的**都**是如此；人寫的只有小幅增益是早期報導的說法。preprint | [arXiv 2602.11988](https://arxiv.org/abs/2602.11988) |
| Anthropic 回報 agent 改進內部工具可超過人寫的 | **成立**：〈Writing effective tools for agents — with agents〉（2025-09）以內部 Slack 工具的 held-out 測試集比較人寫與 Claude 最佳化版本。同文也建議大輸出要有分頁、截斷與合理預設，並提供 concise／detailed 回應格式 | [Anthropic 工程部落格](https://www.anthropic.com/engineering/writing-tools-for-agents) |
| 「多數官方 MCP server 只是包一層 API」的研究 | **未查到出處**，演講沒給名字 | — |
| 他的工具 `chat-history` | **存在且與演講描述一致**：[ay-bh/chat-history](https://github.com/ay-bh/chat-history)，Cargo.toml 作者即 Ayush Bhardwaj，MIT。README 的旗標對得上演講：`view --around／--grep／--tail／--role／--max-chars`、`search --compact`（「About a sixth the size of `--json`」）、`inspect <id> <id> --brief`。首次執行會自動把 skill 裝到 `~/.claude/skills/` 與 `~/.agents/skills/`；README 沒有提到演講中的 `--deep` 旗標（已被淘汰，與演講一致） | [crates.io](https://crates.io/crates/chat-history) |

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| 約 20,000 次呼叫、14 個 CLI、四分之一被 pipe、`git show`／`cargo test` 62%、83% 屬重複模式、55% 只接 head/tail/sed | **單一使用者自報**：全是講者自己的對話紀錄，抽取方法與 pipe 的判定規則沒公開；閱讀頁也說這是他常用工具與流程的證據，不是所有 agent 行為的普查 |
| `gh` 的 `--limit` 用了 81%、`cargo test -q` 約十次一次 | 同上，自報；沒說分母 |
| 自家工具 pipe 讀取 80%／82% → 約四分之一 | **自報、無對照**：前後兩個數字（80% 與 82%）在演講中不一致；改版前後的模型與任務也不同 |
| `--deep` 失效後 95/95 仍使用；改寫 skill 後 2 個 session 不再用 | 95 次這半邊有說服力；「改 skill 後就改過來」只有 **2 個 session**，是軼聞級 |
| compact 模式約 JSON 的六分之一 | 講者自報，README 也這樣寫，沒附量測方法 |
| 1.2M 字元 vs 3,000 字元 | 單一 session 的單次比較 |
| Infracost 0/6 → 6/6、成本 -41% | 已核原文；**廠商自測**、小題數（困難題 6 題）、無獨立重現 |
| DuckDB 59%／0.5%／成本沒改善 | 已核原文；廠商自測，但結果對自己不利（沒省到錢），反而可信度較高 |
| 97% 工具描述有 smell | 已核摘要；preprint，評分用 LLM 掃描器 |
| ETH context 檔研究 | 已核摘要；preprint，且最新版結論比演講轉述更廣（人寫的也沒普遍幫助） |

**勿引用**

- 「ETH 研究證明 agent 寫的 context 檔比人寫的差」作為該研究的主結論：最新版摘要的結論是兩者整體都沒有提升成功率，請直接引摘要。
- 「Infracost 把 token 用量砍 79%」當成成本數字：79% 是困難題的輸出 token，成本降幅是 41%。
- 「多數官方 MCP server 只是包 API」：本次查無出處。

## 可以搬到個人 Claude Code／Codex 工作流程的做法

前提：這場演講是寫給**工具作者**的。你不寫 CLI，能直接搬的是第 1、2、4 步；你有自己的腳本、CLI、skill 或 MCP server，才用得到第 3、5、6 步。

1. **先把對話紀錄留住**。Claude Code 預設 30 天清掉不活躍的紀錄，而且不提示。要做這種分析，先在 `~/.claude/settings.json` 把 `cleanupPeriodDays` 調大，或定期把 `~/.claude/projects/` 備份出去。
2. **挖出重複的 pipe**。Claude Code 的紀錄是 `~/.claude/projects/<專案>/<session>.jsonl`，每行一個 JSON；`type` 為 `assistant` 的那行，`message.content[]` 裡 `type: "tool_use"`、`name: "Bash"` 的項目，`input.command` 就是 agent 下的指令（2026-11-19 在本機紀錄上用 Python 試跑過，結構相符）。做法：抽出所有指令 → 用 regex 找 `| (head|tail|grep|sed|wc|python|jq)` → 依「pipe 前的指令＋子指令」與「接的過濾工具」分組計數 → 看出現 10 次以上的組合。注意 `cd 路徑; …` 開頭的指令要先剝掉前綴才分得準。本機粗跑時，大量 pipe 其實是 `grep`／`sed` 讀檔再接 `head`，這類是 agent 在讀檔，不是某個 CLI 缺旗標，不在本演講的射程內。
3. **自己的 CLI 或腳本，依序補這幾樣**（他說先做最便宜的）：
   1. 範圍與上限旗標（`--limit`、`--offset`、`--tail N`、`--around`）。
   2. 大輸出預設只印一部分，結尾寫「顯示 20／300 筆，加 `--offset 20` 看下一頁」。
   3. 精簡輸出模式（一筆一行、只留必要欄位），取代讓 agent 自己寫 Python 削 JSON。
   4. 接受多個 ID 的批次查詢，取代 for 迴圈。
   5. 失敗時最後幾行固定是錯誤摘要＋完整 log 路徑，並保留非零退出碼。
   6. 要做 agent mode 的話，偵測 `CLAUDECODE` 等環境變數＋stdout 不是終端機，並保留強制開關（照 DuckDB 的做法）。
4. **自己跑測試與腳本時不讓 pipe 吃掉失敗**。hook 與腳本開頭加 `set -o pipefail`；要 agent 跑長輸出的測試時，在 `CLAUDE.md`／`AGENTS.md` 寫「輸出先寫進檔案，再讀檔尾與錯誤段」，不要只寫「跑測試」。第三方 CLI 已有精簡旗標的（如 `cargo test -q`），把旗標直接寫進指示檔，因為他的數據顯示 agent 不會自己去找。
5. **改旗標就同時改 skill**。刪除或停用旗標的同一個 commit 裡，`grep` 所有 `SKILL.md`、`AGENTS.md`、help 文字，把提到舊旗標的地方一起改掉。他的實驗顯示只要 skill 還在叫 agent 用，agent 就會一直用。
6. **改完用舊紀錄重播驗收**。從步驟 2 抽出的真實指令挑一批當測試，舊版、新版各跑一次，依第 7 節的四條規則比對，並留一部分不看來打分。量 turn 數與答對率，不只量輸出大小。

**不能照搬的部分**：

- agent mode 和輸出格式只有工具作者能改；對第三方 CLI 你只能用指示檔教旗標。
- 他的工具就是「搜尋對話紀錄」，所以分析自己的紀錄剛好是它的用途，這個方法在他那裡特別順。一般 CLI 要另外寫抽取腳本。
- Codex 讓 agent 每次呼叫自設輸出上限，pipe 本來就少，同樣的分析在 Codex 紀錄上可能看不出東西。

## 與既有頁的關係

- 和 [[Lauren-Tan-把糾正寫進程式庫]] **部分衝突**：Tan 把 skill、rules 這類散文放在信任倒金字塔的低層，主張能改成確定性檢查就不要寫散文；Bhardwaj 則說 skill 和 help 文字**就是介面**，實驗也顯示 agent 會照字面執行。兩者並不矛盾：Tan 說的是「不要把約束只寫在散文裡」，Bhardwaj 說的是「散文一旦寫了就會被照做，所以過時的散文是 bug」。合起來的結論是：散文要少，但寫了就要和程式同步維護。
- 為 [[Claude-5-世代的指示精簡原則]] 提供一個**機制面的佐證**：那頁主張刪掉過時、多餘的指示；Bhardwaj 的 `--deep` 實驗（95/95 照舊用）具體示範了過時指示會持續造成錯誤呼叫。
- [[Claude-Code-放手運行的安全與驗證]] 談人退出迴圈後由 hook、CI 接手驗證；本頁的 pipe 吃掉退出碼與錯誤訊息，正是這類自動驗證會被騙過的一個具體路徑，hook 腳本應開 `pipefail`。
- [[AI-Engineer-2026-演講精華-AI-工作流程]] 第 3 節引用了本場的 `--deep` 與 DuckDB 兩例；本頁是完整版與回查結果。
- [[Agent-Harness-Engineering-框架綜述]] 從 harness 的角度談 context 管理；本頁補上「工具輸出本身」這一層：harness 能做的是大小上限，挑出哪一段只能靠工具提供選擇型旗標。

## 張力與限制

- **「讓 agent 自己 pipe」的反方並沒有被駁倒**，只是被限縮：他承認一次性情境本來就該 pipe。真正的主張是「重複 10 次以上的模式」才值得做進工具。沒有重複模式的工具，不用為 agent 加一堆旗標。
- **省 token 不是改 CLI 的理由，答錯才是**。DuckDB 的案例清楚顯示：agent 本來就答對時，輸出少 59% 也幾乎省不到錢（系統提示與對話歷史才是大頭）。值得投資的是 Infracost 那種「agent 拿不到答案、在 JSON 上自己寫解析器」的情況。
- **他主張的「人設計、agent 檢查」與他引用的 Anthropic 文章不完全一致**：Anthropic 那篇讓 Claude 從評測結果直接改寫工具，而且在 held-out 測試上勝過人寫版本。Bhardwaj 的保留在於「從零設計」這一步，不是「改進」這一步。
- **用 agent 下一步行動當答案有偏差**：agent 接下來用的結果不一定是對的結果。他自己也說這是粗略答案，所以要留 held-out 案例。

## 交叉引用

- [[Lauren-Tan-把糾正寫進程式庫]]
- [[Claude-5-世代的指示精簡原則]]
- [[Claude-Code-放手運行的安全與驗證]]
- [[AI-Engineer-2026-演講精華-AI-工作流程]]
- [[Agent-Harness-Engineering-框架綜述]]
