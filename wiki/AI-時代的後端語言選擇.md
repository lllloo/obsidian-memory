---
title: AI 時代的後端語言選擇
description: PHP、Go、Node/TypeScript、Python 在產品接 AI 與讓 coding agent 寫後端兩面的證據盤點：生態差異明確，產碼品質的語言排名互相矛盾
created: 2026-09-23
updated: 2026-09-23
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - coding-agent
  - agent-framework
  - evaluation
  - laravel
  - mcp
---

# AI 時代的後端語言選擇

「AI 時代該用哪個後端語言」其實是兩個問題，證據狀態完全不同：

- **(A) 在產品裡接 AI**（呼叫 LLM、串流、agent、RAG）：各語言的**生態差異明確、可查證**。
- **(B) 讓 coding agent 寫後端**：**沒有證據支持「某語言讓 AI 產碼明顯更好」**。跨語言評測的排名互相矛盾，論文作者自承語言與 repo／題目難度混淆；站得住的只有具名從業者的經驗談。

2026-09-23 以 deep-research 對抗式查證（5 角度、21 來源、25 條主張驗證、5 條否決），另由主 agent 回讀 Armin Ronacher 原文補上研究漏抓的經驗談。以下每條標證據強度。

## 一、產品接 AI：差異在生態與並發模型，不在執行速度

LLM 呼叫的瓶頸是模型回應延遲，語言本身跑多快幾乎無關；真正分出高下的是**新框架／SDK 先支援誰**與**長連線怎麼扛**。

| 語言 | 現況 | 證據強度 |
|---|---|---|
| **Python** | AI/ML 生態深度與廣度無對手，CrewAI、LlamaIndex、DSPy 等 agent／RAG 框架多以 Python 為先 | 中：主來源為廠商部落格（Blaxel，兩語言都託管、立場相對中立），「框架較多」屬定性共識非計量 |
| **TypeScript** | OpenAI、Anthropic、Google 三家都有積極維護的官方 TS SDK；Vercel AI SDK、Mastra、LangGraph.js 已可上生產；串流與長連線是本行 | 中：SDK 部分有 npm 一手發版紀錄佐證 |
| **Go** | Anthropic、OpenAI 都有**官方 Go client SDK**；微軟 Agent Framework for Go 2026-07 進 public preview（tool-calling、MCP、多 agent）。但 **Claude Agent SDK 與 OpenAI Agents SDK 都沒有官方 Go 版**，只有社群請求與非官方移植 | 高：微軟 devblog 一手公告＋ `gh api` 列 repo 核實。勿誤讀成「Go 沒有官方 LLM SDK」 |
| **PHP（Laravel）** | 官方 `laravel/ai` 提供跨供應商統一 API（文字、圖像、音訊、embeddings），`stream` 走 SSE、`queue()` 丟背景，provider 受限流時自動 failover。PHP 有**官方 MCP SDK**（PHP Foundation × Symfony） | Laravel AI SDK：高（官方文件＋部落格互證），但屬廠商自述、只證明功能存在、不證明生產效能。MCP SDK：中，見下 |

**PHP MCP SDK 的「GA」要兩者並陳**：MCP 官方部落格（2025-09）稱 generally available，首版只能建 server；repo 自述在 1.0 前屬 experimental，查證時仍在 0.x、README 已列 client。所以「GA」應理解成「已公開釋出」，**不可寫成「PHP 有穩定的官方 MCP SDK」**。

### PHP-FPM 的核心限制

PHP-FPM 一個 worker 同時只處理一個同步請求，LLM 呼叫期間 worker 整段被佔住——串流更久，但**非串流呼叫一樣會佔**，阻塞來自同步 I/O 本身。常見緩解：

1. Octane（Swoole／RoadRunner／FrankenPHP）常駐 worker
2. Horizon／queue 把生成丟背景，再用廣播推前端
3. 另掛 Node.js sidecar 專門處理串流

強度：中。機制是 FPM 的基本架構事實（3-0），但主來源是單一技術部落格，另有 Sevalla、Medium、php-fpm-ng issues 的獨立佐證。「每請求佔 3–30 秒」是部落客估計非實測。**三種緩解的實際並發效果本輪未驗證**。

## 二、AI 寫後端：評測排名互相矛盾

### 跨語言 agentic 評測

| 評測 | 各語言結果 | 限制 |
|---|---|---|
| SWE-bench Multilingual（SWE-agent＋Claude 3.7 Sonnet） | Rust 58.1%、Java 53.5%、**PHP 48.8%**、Ruby 43.2%、JS/TS 34.9%、**Go 31.0%**、C/C++ 28.6% | 每語言約 43 題，1 題約 2.3 個百分點；頁面自承難以判斷哪些因素最重要 |
| SWE-Bench Pro 公開集（Scale AI，2025-09） | **Go 與 Python 普遍較高**，JS/TS 依模型從近 0% 到 30%+ | 只含 Python/JS/TS/Go，無 PHP；語言分析只用 50 回合、每題 $2 上限的軌跡；某些 repo 所有模型都低於 10% |
| Multi-SWE-bench（2025-04，1,632 題） | 模型在 Python 強、難以泛化到其他語言 | 無 PHP；Python 分數取自另一資料集（SWE-bench Verified）；其他語言中難題比例較高；三種受測 agent 原本都為 Python 最佳化 |

數字本身強度高（3-0、逐項對過一手）。但 **Go 在一份倒數第二、在另一份名列前茅**，本身就說明語言與 repo、題目難度分不開——high 只代表「評測得出這些數字」，不代表「語言 X 更適合 AI coding」。

### 歷史基準：MultiPL-E（2022，同儕審查）

- 產碼表現與語言熱門度相關，但 Lua 等冷門語言也可以表現一樣好。
- Codex 的 HumanEval pass@1 超過 40% 的語言含 **PHP**、TypeScript、Java、C++ 等，Go 不在其中。
- **靜態型別整體無顯著效果**（HumanEval p=0.33）；但把 TypeScript 型別全改 `any` 後表現掉 2.5%（p<0.001）——在型別註記是常規的語言裡，有資訊量的型別有用。

強度：中。只有 Codex 做了統計檢定；受測是 2022 年模型、函式級一次生成、**無編譯回饋**，不能外推到 Claude Code／Codex 這類 agentic 迴圈。有「靜態型別語言表現較好」的反向線索（arXiv 2512.18131、GitHub Blog 引述「LLM 產碼編譯錯誤 94% 是型別錯誤」），但只見於搜尋摘要、未讀原文，**勿引用**。

### 具名從業者經驗談

**Armin Ronacher（Flask 作者，2025-06「Agentic Coding Recommendations」）**：「I strongly recommend Go for new backend projects.」理由是：

- 測試直接、可增量執行，縮短 agent 迴圈
- 語言簡單、structural interface，LLM 容易「理解」
- 生態重視向後相容與明確升版，減少 API 漂移
- 明確傳遞的 context 取代隱式執行期狀態

同時點名 Python 不利：agent 常被 pytest fixture injection 這類「魔法」與 async 事件迴圈問題絆倒，且直譯器啟動慢拖慢迴圈。

強度：低（單一作者經驗、非評測），但一手原文已由主 agent 回讀核對。注意他比的是 Go 與 Python，**沒有評論 PHP**；和上面 SWE-bench Multilingual 中 Go 墊底的結果並存，兩者談的是不同東西（迴圈手感 vs 單次解題率）。

**Taylor Otwell 與 Laravel 官方文件**：重慣例、目錄固定的框架讓 agent 少猜、產碼更準。強度：低——廠商有利益、無數據，頁面同時在推 Laravel Boost。

**Laravel Boost Benchmarks（廠商自辦）**：17 個 Laravel 任務、315 個 Pest 測試、6 個模型。開 Boost 時前段模型達 313/315，關掉時約 298–299。強度：低——官方自承每項只跑一次、只能當方向訊號，重跑有翻盤；**無跨語言對照**，不能拿來比 Go/TS/Python。

## 三、判讀

1. **不構成「為了 AI coding 換語言」的理由**：評測排名矛盾且混淆，經驗談彼此談的不是同一件事。比起語言，**有型別檢查、有測試、跑得快的回饋迴圈**才是 agent 產碼品質的著力點——這條與 [[用測試約束-AI-產碼]] 的主張一致；PHP 端可用 PHPStan／Larastan 把型別閘門補上。
2. **產品接 AI 的真正決策是並發模型**：Laravel 專案的一般 AI 功能留在 Laravel（`laravel/ai` 已涵蓋）；串流並發量大時在 Octane／FrankenPHP、queue＋廣播、sidecar 三者間選；重 agent／RAG pipeline 才值得開 Python 或 TS sidecar 吃主流生態；高併發 AI gateway 才輪到 Go。這三條緩解的實測比較目前**沒有證據**，是本頁最大缺口。

## 查證否決（勿引用）

以下主張在對抗式驗證中被否決。依過往經驗 verifier 會過度否決，否決不等於事實為假，但**未經一手回查前一律勿引用**：

- 「Octane＋Swoole 單一 worker 可用 coroutine 同時持有多條 LLM 連線」（0-3）
- 「Multi-SWE-bench 呈 Python > Java > Go/Rust > C/C++、TS/JS 墊底並歸因於非同步範式」（0-3）
- 「Boost 評測證明慣例＋官方 MCP 能明顯改善 AI 寫後端品質」（0-3，推論超出證據）
- 「Laravel Boost 提供超過 15 個專用工具」（0-3，細節未回查）
- 「SWE-bench Multilingual 作者不把差異歸因於語言」（1-2，措辭問題）

## 開放問題

- 2026 年前沿模型搭配實際 harness，在同難度任務上同時比較 PHP／Go／TS／Python 的公開評測是否存在？
- agentic 迴圈（有編譯器、型別檢查、測試回饋）下，靜態型別是否提升成功率？
- Laravel 在 Octane／FrankenPHP 下扛大量並發 LLM 串流的實測，與 queue＋廣播、sidecar 相比何時該選哪個？

## 關聯

- [[用測試約束-AI-產碼]] — 本頁第二節「語言不是關鍵、回饋迴圈才是」的延伸：該頁講這個回饋迴圈本身怎麼被 agent 繞過、怎麼加固，是本頁判讀第 1 條的具體做法。
- [[專案測試流程-後端-Laravel]] — 留在 Laravel 時的落地面：那套分層測試就是讓 agent 在 PHP 端也有快速回饋的閘門。
- [[MCP-無狀態化-2026-07-28]] — 本頁 PHP MCP SDK 的背景：協議本身剛經歷無狀態化改版（移除 `initialize` 握手）。0.x SDK 是否已跟上該版，本輪未查證，採用前應先確認。
- [[四套-coding-agent-能力差異對照]] — 本頁第二節談的「agentic 迴圈」在各家 harness 上的實際能力差異。
