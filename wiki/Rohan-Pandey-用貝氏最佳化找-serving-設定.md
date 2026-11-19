---
title: Rohan Pandey 用貝氏最佳化找 serving 設定
description: DigitalOcean 線上場示範：依流量組合與 goodput 目標讓 Optuna 迴圈找自架模型 serving 設定，附回查與證據限制
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/code/2026/talks/online-rohan-optimization
published: 2026-11-12
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - evaluation
  - automation
---

# Rohan Pandey 用貝氏最佳化找 serving 設定

來源：AI Engineer CODE 2026 線上場〈Stop Shipping LLM Settings That Only Win on Paper〉的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Pandey-Model-Serving-Recipe-Optimization]]（YouTube `y9JtCCZP2MQ`，Day 2 直播 2:13:37–2:19:04，約 5 分半）。回查日期 2026-11-19。

**一句話**：模型權重附的預設 serving 設定，不保證適合你的機器和流量。與其手動試參數，不如先定義流量組合和評分目標，讓貝氏最佳化迴圈在背景跑有限次數的 trial，最後交出**可部署的 YAML** 和**證明它為何勝出的 HTML 報告**。

## 講者與立場

- **Rohan Pandey**：大會議程頁列為 DigitalOcean 的 Software Engineer II。整場只有他一人發言。
- **Balaji Varadarajan**：只出現在演講標題，議程頁講者列與逐字稿都沒有他。他在這場的角色不明。
- **是否推自家產品**：示範跑在 DigitalOcean 的 droplet（雲端主機）上，但沒有推銷付費功能，也沒給 repo 或產品名。回查找不到這個 tuner 的公開 repo 或官方公告（見下方回查），所以它目前看起來是**內部工具的示範**，聽眾拿不到程式碼。
- **標題和內容的落差**：標題說「別上線只在紙上贏的設定」，但演講本身沒有討論「紙上」與「實際」的差別，也沒有示範上線後的驗證。標題的承諾比內容大。

## 演講脈絡（依順序）

### 1. 問題：預設 recipe 不是最佳 recipe（2:13:37–2:14:28）

目標是做一個 agent，替任何模型找出最好的 serving 設定（逐字稿寫成「VLM serving config／recipe」）。手動找最佳設定很花時間；如果能自動化、在背景跑，agent 找參數比人快，就能省下大量時間。

**「VLM」指的是什麼**：逐字稿同一個詞先後被辨識成 VLM、VLN、BLM，搭配「serving recipe」「ISL／OSL」「ITL」「goodput」這些用語，最可能是 serving 引擎 **vLLM**（vLLM 官方的模型部署指南就叫 Recipes）。這是推論，演講沒有在畫面以外講清楚，閱讀頁也只寫「serving configuration」。

### 2. 搜尋策略：貝氏最佳化＋Optuna（2:14:31–2:15:39）

- 策略叫**貝氏最佳化**：用數學方法縮小搜尋空間，不必窮舉所有組合，所以找參數的時間變短。
- **Optuna** 是執行這個策略的工具。流程：餵入起始 recipe → 跑一個 trial → 評分 → 用策略改 recipe → 再跑，直到 trial 數用完。
- 閱讀頁補了一句重點：迴圈搜尋再有效率，如果分數不代表你真正要的服務品質，它只會很有效率地改善錯的東西。**目標函數才是關鍵**。

### 3. 流量組合（2:15:45–2:16:18）

- 示範機器是一台已載入 **GPT-OSS 120B** 的 droplet。
- 起始 recipe 裡定義四種流量情境（regime）：**短聊天、長聊天、RAG、批次分類**，各有自己的輸入長度（ISL）與輸出長度（OSL）。這些可以依需要改。
- 起始 recipe 就是「下載模型權重時拿到的設定」。
- 含意：找到的最佳設定是**以這組流量和這台硬體為條件**，不是這個模型的通用最佳值。

### 4. 啟動一次實驗（2:16:26–2:17:28）

指令做三件事：指定權重位置、啟動虛擬環境、跑 `tuner.py`。必填的輸入有四個：

| 輸入 | 作用 |
|---|---|
| study 名稱 | 識別這次實驗 |
| 起始 YAML | 搜尋起點，就是上面那份預設 recipe |
| 硬體規格 | 結果綁定的機器 |
| trial 數 | 搜尋預算；畫面上的例子是 24 |

時間成本：他說這類實驗**通常要跑好幾個小時**，GPT-OSS 那次約四到五小時，另一個模型也要幾小時。閱讀頁特別提醒：自動化省的是重複的手動調參，不是讓 benchmark 變免費。

### 5. 產出：YAML＋HTML 報告（2:17:32–2:18:57）

- **GPT-OSS 120B**：報告顯示 50 個 trial 中哪一個最好。最佳化後的 YAML 包含所有 recipe 參數，他舉例「找到 256 是最佳值」，但沒說是哪個參數。評分依據是 **goodput tokens**（他口誤說成「accuracy」）。相對起始設定，tokens generated 提升 **17.5%**。
- **DeepSeek R1 distill 模型**：9 個 trial，第 9 個最好。token throughput **翻倍**，ITL（inter-token latency，相鄰 token 間的延遲）**幾乎減半**。沒說是哪個 distill 尺寸。
- 結論：你會拿到一份 HTML 報告（每個 trial 的表現）和一份 YAML（最佳 recipe）。閱讀頁的整理是：兩者都留，才能分清楚「可部署的結果」和「選它的理由」。

**數字對不上的地方**：指令範例寫 24 個 trial，GPT-OSS 報告是 50 個，DeepSeek 是 9 個。閱讀頁的解釋是：畫面上的指令只是示範怎麼啟動，報告來自另一次已完成的實驗。

## 回查結果（2026-11-19）

| 項目 | 結果 |
|---|---|
| tuner 本身的 repo／文件 | **找不到**。GitHub 上 DigitalOcean 組織沒有對應的 vLLM tuner repo，網路搜尋也沒找到官方公告，只找到 StartupHub.ai 依演講改寫的報導，同樣沒附 repo |
| 議程頁 | [ai.engineer/code/2026](https://ai.engineer/code/2026) 列為 11 月 12 日線上場，議程上的題目是「Searching for a better model-serving recipe」，講者只列 Rohan Pandey |
| Optuna 用貝氏最佳化 | **對得上**。Optuna 原始碼 `Study.__init__` 在未指定 sampler 時用 `TPESampler()`，`optimize` 文件寫「the default choice for the sampler is TPE」（[study.py](https://github.com/optuna/optuna/blob/master/optuna/study/study.py)）。TPE 是一種以機率模型挑下一組參數的貝氏方法；另有明寫「Gaussian process-based Bayesian optimization」的 `GPSampler`（[samplers 文件](https://optuna.readthedocs.io/en/stable/reference/samplers/index.html)）。演講沒說他用哪個 sampler |
| goodput 的定義 | 演講只說「goodput tokens」，沒給 SLO 門檻。一手定義來自 DistServe：在**符合指定 SLO**（如 TTFT、TPOT 的 P90 門檻）下系統能撐住的最大請求率（[DistServe blog](https://haoailab.com/blogs/distserve/)）。vLLM 的 `vllm bench serve --goodput` 用 `ttft`、`tpot`、`e2el` 三種 SLO 以毫秒指定（[文件](https://docs.vllm.ai/en/latest/cli/bench/serve.html)）。所以「17.5% goodput 提升」**沒交代 SLO 是什麼**，無法判斷意義 |
| 兩個模型 | 都存在：[openai/gpt-oss-120b](https://huggingface.co/openai/gpt-oss-120b)、DeepSeek R1 distill 系列（如 [DeepSeek-R1-Distill-Llama-70B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B)） |
| vLLM 自帶的同類工具 | **已經有官方替代品**。vLLM repo 的 [`benchmarks/auto_tune`](https://github.com/vllm-project/vllm/tree/main/benchmarks/auto_tune) 對 `max-num-seqs` 與 `max-num-batched-tokens` 做網格搜尋，可加 P99 端到端延遲上限與 prefix cache 命中率條件，README 也建議放在 tmux 裡跑。[`vllm bench sweep`](https://docs.vllm.ai/en/latest/benchmarking/sweeps.html) 對 serve 參數與 bench 參數做笛卡兒積掃描，每組預設跑 3 次，還能畫 Pareto 前緣。兩者都是網格搜尋，不是貝氏最佳化 |
| 開源的貝氏版本 | [Anurag-Deo/InferTune](https://github.com/Anurag-Deo/InferTune) 做的事幾乎一樣（Optuna TPE 搜 vLLM 參數、輸出可執行的 `vllm serve` 設定），而且多做了三件演講沒做的事：勝出設定**從頭重跑**確認、對 baseline 算 **bootstrap 信賴區間**、改變數值精度（如 fp8 KV cache）時用 lm-eval-harness **確認準確度沒掉**。查詢當下只有 1 顆星，屬個人專案、自報數字 |
| 學術對照 | [SLO-Guard（arXiv 2604.17627）](https://arxiv.org/abs/2604.17627)：單一作者 preprint，在小模型、單張 A100、五個 seed 下比較，**貝氏（暖啟動 TPE）與隨機搜尋找到的最佳延遲統計上打平**；作者明說優勢不是找到更好的設定，而是在固定預算內更穩定。它還指出這個搜尋空間裡很多看似合理的設定會直接 crash 或 OOM，所以把 crash 當成觀測資料 |

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| GPT-OSS 120B goodput 提升 17.5%（50 trial、4–5 小時） | **講者自報、單一實驗**。沒給 SLO 門檻、流量組合比例、硬體型號、重跑次數 |
| DeepSeek R1 distill throughput 翻倍、ITL 減半（9 trial） | **講者自報、單一實驗**。沒說模型尺寸與硬體；「翻倍」也可能代表起始設定特別差，不代表 tuner 特別好 |
| 貝氏最佳化比窮舉省時間 | 一般原理成立，但演講**沒有和網格或隨機搜尋比較**。SLO-Guard 的小規模實驗反而顯示最佳結果與隨機搜尋打平（單一 preprint、未同儕審查） |
| 最佳化不影響模型品質 | 演講**沒有驗證**。閱讀頁明說 17.5% 不是語言模型的準確度提升。若搜尋空間包含量化或 KV cache 精度，品質要另外測 |
| 結果能搬到別的部署 | 閱讀頁明說錄影無法證明這些增益能搬到不同部署 |

**勿引用**：

- 「這個 agent 找到的設定提升了準確度」：逐字稿說「the way that it's getting the accuracy is the amount of goodput tokens」，這是把分數口誤成 accuracy，不是模型準確度。
- 「17.5% 是 GPT-OSS 120B 的通用 serving 增益」：結果綁定這組流量、這台機器和未公開的起始設定。

## 能不能搬到個人 Claude Code／Codex 工作流程

**多數人用不到**：只用 Claude、OpenAI 等託管 API 的話，serving 參數由供應商決定，沒有東西可調。這場和日常 coding agent 工作流程關係不大，[[AI-Engineer-2026-演講精華-AI-工作流程]] 的來源清單也標為「個人開發者適用度低」。

**自架模型（vLLM）時可以照做**，讓 Claude Code 幫你寫腳本、在背景跑：

1. **從真實流量定義情境**：從 log 統計輸入與輸出長度分布，切成幾個 regime（像演講的短聊天、長聊天、RAG、批次分類），寫明比例。沒有真實流量就照用途估，並把這個假設寫進報告。
2. **先寫目標，再寫搜尋**：用 `vllm bench serve --goodput` 指定 SLO（例如 TTFT、TPOT 的毫秒上限），把「達到 SLO 的 goodput」當分數，不要只看原始 throughput。
3. **先用官方網格工具**：參數少（例如只調 `max-num-seqs`、`max-num-batched-tokens`）時，直接用 vLLM 的 `auto_tune.sh` 或 `vllm bench sweep`，不必自己寫。參數多、單次 trial 很貴時，才換 Optuna 的 TPE；也可以參考 InferTune。
4. **把 crash 當結果記下來**：OOM 或啟動失敗的設定給最差分並記錄原因，不要讓迴圈中斷。
5. **勝出設定要重跑並對照 baseline**：至少重跑兩次看變異；搜尋空間有改數值精度時，跑一次固定 seed 的準確度評測。
6. **YAML 和報告一起留**：最佳設定、所有 trial 紀錄、流量假設、硬體、日期放在同一個目錄進版控。換模型、換硬體、流量組合變了就重跑。
7. **長時間任務放 tmux**：實驗動輒數小時，放 tmux 或背景程序跑，agent 只負責寫腳本、啟動和最後讀報告，不要讓 agent 一直開著等。

## 與既有頁的關係與張力

- **它其實不太是「LLM agent」**：從逐字稿看，迴圈每一步都是 Optuna 決定下一組參數，沒有提到 LLM 參與。這反而印證同屆 Raymond Weitekamp〈[Your Agent Doesn't Need an LLM for Every Decision](https://ai.engineer/talks/hFNbPmzzcEs-your-agent-doesnt-need-llm-every-decision)〉的主張：目標可量化、搜尋空間是數值時，傳統最佳化器比 LLM 更適合。[[Jev-與-System-One-模型]] 也是「決策不一定要生成文字」這條路線，可對照。
- **是 evaluator-optimizer 迴圈的非 LLM 版本**：[[Building-Effective-Agents-Anthropic]] 的 evaluator-optimizer 要求「有明確評測準則、迭代能帶來可衡量的價值」。這場的 benchmark 分數就是可執行、客觀的 evaluator，和 [[設計品質的可量化檢測]] 用自動檢測撐起閉環是同一形狀。差別是這裡的 optimizer 是 TPE，不是 LLM。
- **和「附證據」的主題一致**：[[AI-Engineer-2026-演講精華-AI-工作流程]] 第 2 節主張產出要附驗證證據。這場的「YAML 配 HTML 報告」是同一個原則在 serving 調參上的版本；但它自己的證據（單次實驗、無重跑、無品質檢查）還不夠強。
- **分數設計的風險**：閱讀頁「optimizer 會很有效率地改善錯的東西」這句話，和 [[LLM-as-judge-知識庫頁面評分]] 的結論同向：評分規則決定結果可信度。這裡的對應問題是 goodput 的 SLO 門檻與流量比例選錯，找到的設定就只在測試流量上贏，正是標題說的「only win on paper」。
