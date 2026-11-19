---
title: Harshul Jain 與 Parv Khatri 自架 LLM 要會說不
description: 自架 LLM 被 coding agent 灌爆時，在 ingress 先決定收、緩或拒，並以含拒絕數的 goodput 驗證，附 AdmitPerf 回查
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/ntVpbyDTYaQ-your-self-hosted-llm-needs-say-no
published: 2026-11-09
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - evaluation
  - coding-agent
---

# Harshul Jain 與 Parv Khatri 自架 LLM 要會說不

來源：AI Engineer 演講〈Your Self-Hosted LLM Needs to Say No〉的官方閱讀頁與完整機器逐字稿，落地於 [[AI-Engineer-Jain-Self-Hosted-LLM-Needs-to-Say-No]]（YouTube `ntVpbyDTYaQ`，約 52 分鐘，2026-11-09 上傳）。回查日期 2026-11-19。

**一句話主張**：自架 LLM 的 serving stack 裡，gateway、router、engine 各自做決定，卻沒有一層在「request 拿到 GPU 記憶體之前」問一句「現在還有空間嗎？」。coding agent 一個任務就送出 40–50 個呼叫，這一層必須補上：在 ingress 依 request 屬性和 engine 即時指標決定 admit、defer 或 reject，並回傳 agent 能照著做的錯誤碼；再用把被拒絕的 request 也算進分母的 goodput 證明這個 policy 真的有用。

## 講者與立場

- **Harshul Jain**：Audible 資深軟體工程師，負責部分 ML／AI 基礎設施。在寫開源 handbook《LLM Inference at Scale》（他說已超過 300 顆星），也維護 agent harness 框架 agentship。
- **Parv Khatri**：SAP 資深軟體開發者，做雲端應用與 LLM 基礎設施，寫過 LLM fine-tune 指南，也參與 agentship。
- **是否推自家產品**：沒有推雇主產品，但整場的後半段在介紹**他們自己的開源工具 AdmitPerf**（MIT 授權），研究綜述也出自 Jain 自己的 handbook。所以「現有論文都不適合 coding agent，你得自己做，而我們做了工具」這條敘事，有自家工具的利益在裡面。
- **適用對象**：自己架 vLLM、SGLang 這類 inference engine 的團隊（因為隱私或成本），不是只用託管 API 的人。

## 演講脈絡（依順序）

全場分四段：動機 → admission control 放哪裡、看什麼、回什麼 → 決策策略 → benchmark。

### 1. 動機：答案多長，request 進來時沒人知道（0:05–15:30）

**推論的基本事實**（2:00–4:00）：
- 模型一次寫一個 token，每個 token 都依賴前一個，所以無法一次寫完。
- 他要聽眾記住一件事：**模型寫到最後一個 token 才知道答案多長**。request 進來時能數輸入 token，卻不知道它最後要花多少 GPU 時間。

**request 經過的管線**（4:00–5:00）：app／agent → API gateway（驗 key、數請求數）→ router（挑一個 replica，也就是一份正在跑的模型）→ inference engine（vLLM、SGLang、TensorRT 等，把權重載進 GPU、把多個 request 組成 batch）。engine 會替每個 request 維護 **KV cache**，也就是 request 在生成過程中累積的記憶體；答案越長，KV cache 越大。

**容量上限來自三個互相拉扯的目標**（5:00–7:00）：品質（模型大小與精確度）、延遲（第一個 token 多快、之後每個 token 多快）、吞吐量（同時能服務多少 request）。像「好、快、便宜只能挑兩個」，每個產品只能挑兩個：
| 產品 | 優先 | 理由 |
|---|---|---|
| 互動式聊天 | 品質＋延遲 | 使用者對答案變差或等太久都很敏感 |
| 非同步 agent | 吞吐量＋品質 | 品質差就要重跑，背景任務重跑很貴 |
| autocomplete 這類高量即時系統 | 延遲＋吞吐量 | 不需要昂貴模型 |

不管放棄哪一角，都有一個在 SLO 內能扛的最大負載。假設是同時 8 個 request；**40 個 request 在 2 秒內湧入**會怎樣？

**兩個公開事故**（7:00–8:50）：
- 2023-11-08 OpenAI：流量異常大的一天，routing server 記憶體耗盡、health check 開始失敗；加了 replica 又撤回，最後是切斷進來的流量、再慢慢放回。
- 2026-01-21 Anthropic：Sonnet 4.5 這一層先變慢，接著在約 90 分鐘內回錯誤，原因是算力不夠應付需求。
- 兩家的後續行動都**不是**「要更快的 engine」：OpenAI 是 graceful load shedding，Anthropic 是更早偵測容量上限。他說這是同一個意思：**更早決定讓哪個 request 進來**。兩個事故都指向「前門」。

**缺的那一步：admission**（9:00–10:00）：管線補成 client → admit 層 → queue／router → engine。admission 是 **request 拿到任何 GPU 記憶體之前**做的決定，只有三種答案：現在開始（admit）、收下但等一下（defer）、現在不行（reject，可回 429 等錯誤）。

**為什麼一定要在 engine 之前**（10:00–12:30）：
- 一旦 admit，engine 就進入兩個階段：**prefill**（讀整個 prompt、建立 KV cache）和 **decode**（一次寫一個 token，每個 token 讓 cache 再長一點）。記憶體一直被占到 request 結束。所以「yes 不是一個瞬間，是延續整個 request 生命週期的承諾」。
- 例子：先 admit 短答案的 A，再 admit 長答案的 B；這時短答案的 C 進來，C 自己需要的工作很少，卻可能因為 B 還在記憶體裡、而且 cache 還在長，照樣錯過延遲目標。**對 C 的決定，有一部分取決於 engine 先前對 B 的承諾。**
- 記憶體滿了，engine 只有三招：丟掉 cache 之後重算（evict）、把 request 換到 CPU 或磁碟等待（swap）、或做到一半回錯誤（preempt）。三招都造成延遲、錯過 SLO，還浪費已花的記憶體。

**為什麼這是「我們的」問題**（12:30–15:30）：
- 託管服務的問題由 OpenAI、Anthropic 自己處理；但為了隱私或成本自架模型的團隊，連同 GPU 一起接下這些決定。
- 流量型態變了：以前是一個人聊天，一次一個 request，中間有幾秒在讀回覆；現在 coding agent 把那幾秒拿去送呼叫、重試、再開更多工作。
- 例子：請 agent 修一個失敗的測試，它可能讀約 **14 個檔案**、跑約 **10 個測試**，整個任務加上工具使用與後續推理產生 **40–50 個呼叫**，有的很快、有的很久。在叢集看來，一個使用者的任務變成一串彼此相關、成本不一的突發請求。

### 2. Admission control：放哪裡、看什麼、回什麼（15:30–27:30，Khatri 主講）

**每一層都看不到全貌**（16:00–17:00）：問每一層「還有空間給這個 request 嗎？」——agent 說不是我的事；gateway 說我看不到；router 說不是我的事；engine 說「我要先說 yes 之後才知道」。

**放在哪裡**（17:00–18:30）有三個時機：
1. **ingress**（engine 正前方）：看得到 request 本身，加上 engine 匯出的指標。只需要一個 proxy 或 gateway，engine 完全不用改。
2. **queue boundary**：在 engine scheduler 挑下一個 batch 時決定。
3. **decode 期間**：scheduler 在答案寫到一半時暫停 request 或收回它的 cache。

後兩者看得更多，但要改 scheduler，等於永遠維護一份自己修改過的 vLLM 或 SGLang fork、每次上游更新都要跟。**ingress 是唯一能搭配原版 engine 的位置**，所以整場都以 ingress 為準。

**policy 是一個函式**（18:30–20:30）：輸入「request 的資訊＋系統現況」，輸出三種答案之一。在 policy 說 admit 之前，request 不占任何 GPU 記憶體。它需要兩邊同時的資訊：

| 來自 request | 來自 engine |
|---|---|
| 輸入長度 | KV cache 用量 |
| 哪個 client／tenant | 佇列裡最舊的 request 等了多久（queue age） |
| 屬於哪個 agent session | prompt 已被 cache 的比例（cache hit） |
| deadline（有的話） | 各 replica pool 的負載 |

gateway 有左邊、engine 有右邊，**沒有人兩邊都有**，所以 admission 必須是獨立的一層。

**八個訊號變成規則**（20:30–22:00），每個訊號和門檻比較，越過就推向某個結果：
- 輸入大到放不進目前的記憶體餘裕 → defer。
- client／tenant 超過自己的配額 → reject（429）。
- 某個 agent session 同時在跑的呼叫太多 → defer。
- 排隊會讓 request 反正趕不上 deadline → reject。
- KV cache 低於高水位 → admit。
- 最舊的 request 等太久 → defer。
- prompt 已被 cache → 優先 admit，因為服務它很便宜。
- 所有 pool 都滿 → reject（529）。

**經驗法則**：挑以秒為單位變化的訊號（例如 queue age），不要用一分鐘平均。coding agent 2 秒送 40 個呼叫，一分鐘平均根本不會察覺。

**三種回應，server 與 agent 各該做什麼**（22:00–27:30）：

**Admit → 200**。engine 為整個 prompt 承諾 KV cache、request 加入正在跑的 batch、每一步和其他 request 一起 decode 一個 token，記憶體一直占到結束或 client 斷線。所以 admission 決定必須在 200 **之前**。agent 端三件事：
1. **timeout 從第一個 token 到達時開始算**，不是從送出 request 算；高負載下光 prefill 就可能花幾秒。
2. **放棄就真的關掉連線**。server 只在 request 完成或 client 斷線時才釋放 KV cache；本地 timeout 但連線還開著的 agent，仍在占 GPU 記憶體。
3. **stream 可能中途斷掉**，而且沒有狀態碼可看；你手上是半個答案，要決定續寫還是重試。
一句話：「200 是開始的承諾，不是完成的承諾。」

**Defer → 503＋`Retry-After`**。header 告訴 client 等幾秒，數字由 policy 根據 engine 估計，例如正在跑的 batch 多久會釋放足夠的 cache。適用條件是**突發而非趨勢**：queue age 在升但系統還沒飽和、容量很快會回來。如果容量短期回不來，defer 只是把問題往後踢，應該直接誠實 reject。agent 端：睡 `Retry-After` 的秒數再加一點隨機 **jitter**，然後重試。沒有 `Retry-After` 時，每個 agent 自己挑延遲，通常是 0，於是 10 個重試同時回來；一次突發裡每個呼叫重試一次，**40 個呼叫就變 80 個**。

**Reject → 429 或 529**，兩個碼代表兩種原因：
- **429 Too Many Requests**：是這個 client 或 agent session 用超過它的份（per-client 負載、併發呼叫數、配額）。問題在呼叫端。agent 應該**降低自己的負載，限制同時在飛的呼叫數**。
- **529（他說 Anthropic 用這個碼）**：provider 過載，所有 replica 都滿，誰都進不來。問題在 pool。重試得更猛只會更糟；應該**等更久、換模型或換 provider，或把任務先擱著**。
- 兩種都要有 **retry budget**：用 exponential backoff 加 jitter，幾次之後**告訴使用者發生什麼事**。全速重試的 reject，正是開場那種事故的成因。

### 3. 決策策略（27:30–38:30，Jain 主講）

**數請求數不夠：count 不是 cost**（28:00–29:30）：
- gateway rate limit 給每個 API key 固定配額：能讓 tenant 之間公平，但**不隨 GPU 負載變化**，保護不了 GPU。
- proxy 對每個 replica 限制同時在飛的 request 數：更接近硬體，但一個快速查詢和一個長規劃呼叫都只算一個位子。實務上大多變成排隊，最後是 **client 的 timeout 在替你拒絕**。
- 成本導向的 policy 用 engine 的即時狀態，估計每個 request 會花多少 KV 記憶體與 token，在它占記憶體之前說不。

**設計 policy 的四個選擇**（29:30–31:00），彼此牽制：
1. **unit**：admit 的單位是單一 request、agent session，還是 tenant。
2. **signal**：policy 觀察什麼（KV 壓力、queue 深度、deadline slack……）。**系統變忙時它必須真的會動**。
3. **rule**：怎麼把訊號變成決定，從耗時微秒的門檻到耗時數秒的最佳化器。
4. **action**：決定之後對 client 做什麼（上一段的 admit／defer／reject）。
例：deadline 類訊號只在 request 真的帶 deadline 時才有用。

**unit 選 session 的理由**（31:00–32:30）：兩個 agent 任務各 20 個呼叫，容量只夠約一半。逐 request 平分：每個任務各進約 10 個，但兩個都卡在沒進來的呼叫上，**容量用光、完成 0 個任務**。逐 session：A 全部進來、完成；B 得到一個清楚的「晚點再來」。數成功呼叫數看不出「0 個任務完成」和「1 個任務完成」的差別。他承認這張圖是示意，但「我們的 40 個呼叫就是一個 session；coding agent 送的是 session，而大多數已發表的 policy 只 admit 單一 request」。

**訊號依你要防的失效來選**（32:30–34:00）：

| 要防的事 | 看的訊號 | 失效條件 |
|---|---|---|
| cache 溢出 | KV 壓力 | cache 根本不會填滿時（第 4 段會回來咬人） |
| 浪費的重算 | KV 用量＋cache hit rate | 一個滿的 cache 只要在被重用就沒問題 |
| 等待變長 | queue depth | — |
| 趕上延遲目標 | deadline slack | request 沒帶 deadline |
| 為長答案做規劃 | 預測輸出長度 | — |

**四種把訊號變決定的方式**，由便宜到昂貴（34:00–36:30）：

| 方式 | 例子（他引用的論文） | 決策耗時 | 他報的結果 |
|---|---|---|---|
| 單一門檻 | 逐字稿辨識成「clued weight／fluid weight」的 2026 policy，對 KV 用量設門檻、逐 request admit | 數十微秒 | 10–25% 改善 |
| 雙閘門（兩個訊號同意才動作） | Concur：KV 用量＋cache hit、admit 整個 agent | 低於 100 微秒 | SGLang 吞吐量約 4 倍，但**只做離線測試** |
| 全叢集最佳化器 | QLM：一次對所有佇列解規劃問題 | 約 5 秒 | 40–90% 增益 |
| 形式化 deadline 上界 | 逐字稿辨識成「Kronos」：算最壞情況下是否還能達成 TTFT deadline | 微秒級 | deadline miss 從 99% 降到 0 |

- 拿成本欄對照 agent：2 秒送 40 個呼叫，**5 秒才做完的決定在整波突發結束後才出來**。
- 各論文用不同模型、engine、工作負載，**不能當排行榜讀**。
- 他把論文放在兩軸上：優化 deadline 還是吞吐量；admit 單一 request 還是整個 session。coding agent 需要的是「admit 整個 session、對即時流量線上運作、搭配沒 fork 的 engine」，**沒有一篇乾淨地落在那裡**。Concur 不需要 fork，最接近，但只測過離線。結論：挑最接近的，自己做。

**決策樹**（37:00–38:30）：
1. request 有沒有 deadline？有 → 用形式化 deadline 上界（微秒級）。
2. 沒有 → 尖峰負載時 KV cache 會不會填滿？會 → KV 門檻；prefix 重用影響成本時改用雙閘門（KV＋cache hit）。
3. 不會 → 用 **queue 門檻**。
先觀察部署在尖峰時落在哪一支，再花時間調門檻。

### 4. Benchmark：怎麼證明 policy 有用（38:30–50:00，Khatri 主講）

**四樣東西**（39:00–40:30）：
1. **cluster**：先在**完全不開 admission control** 時量出 replica 能撐的負載，當作 1× 容量；之後的負載都寫成它的倍數。
2. **policy**：讀哪些訊號、用什麼門檻、說不的時候做什麼。
3. **trace**：真實流量紀錄，回放 coding agent 流量，從 0.5× 容量一路拉到 2×。
4. **score**：同一份 trace 跑兩次，一次開 policy、一次不開，比較結果。

**評分：goodput under admission**（40:30–41:30）：分子是**達成 SLO** 的 request 數（答案準時開始、token 之間沒停頓太久）；分母是**所有到達的 request，包括被拒絕的**。試算：拒絕 95% 流量、把剩下 5% 服務得完美。只算 admit 的，SLO 達成率 100%；goodput under admission 是 5%。「只算留下的 request，拒絕看起來就是免費的。其實不是。」

**工作負載要像真的**（41:30–42:30）：回放保留 fan-out、重試、session 關係的 agent trace，不要用均勻隨機到達。負載寫成實測容量的倍數，從一半掃到兩倍。deadline 寫成「無負載延遲的倍數」。**從沒超過容量的 benchmark 等於沒測到 policy，因為 policy 從來不必說不。**

**每個 admission 結果都該揭露的七件事**（42:30–43:50）：
1. 負載：實測容量的倍數。
2. deadline：相對於無負載延遲。
3. **signal liveness**：policy 看的指標在壓力下有沒有真的動（他說沒有一篇論文報告這項）。
4. 變異：重跑幾次、結果差多少，不是一次幸運的 run。
5. 參數：哪些值在這個環境調過、從別處借來、或用預設。
6. 分母：被拒絕的 request 有沒有算進 goodput 分母。
7. 設定：模型、engine 與版本、硬體、工作負載、SLO、baseline。
他強調這不要求別人改評估方法，只要求說清楚做了什麼；可當讀論文和做自己 benchmark 的檢查清單。

**AdmitPerf**（43:50–47:00）：
- 一個 repo 兩種用途：production 端是放在 vLLM／SGLang 前面的 library，對每個 request 決定 admit／defer／reject；benchmark 端是在真實 GPU 上跑任何 policy 的 harness。**兩邊呼叫同一個 decide 函式**，所以測過的 policy 就是部署的 policy，不必重寫。
- 動機：他們比較的 **16 篇論文**裡，沒有兩篇的 baseline、engine、工作負載、SLO 組合相同。
- 演講展示五個指令：起 GPU 上的 engine、smoke test 確認在服務、每個 policy 跑數次、比較誰贏多少、關掉基礎設施停止計費。**provisioning 和 benchmark 刻意分開**：載入模型要幾分鐘，每次換 policy 都重建會改變當作對照組的部署本身。「部署是常數，policy 是變數。」
- **policy 必須宣告它讀哪個訊號**：KV 門檻 policy 宣告需要 KV 使用比例；engine 給不出來，run 在啟動時就報錯停下。否則缺值會被讀成 0，KV 門檻永遠看到 0、admit 一切，**悄悄變成不做 admission 的 baseline，結果卻看起來完全正常**。「看不到訊號的 policy 應該大聲失敗。」
- 每個決定連同當時看到的狀態一起記錄；每次 run 留下 manifest、summary、decisions、outcomes 四個 JSON。

**A10 上的結果：queue 在長，KV cache 卻很空**（47:00–49:30）：
- 設定：Qwen2.5 約 0.5B 參數的小模型、一張 A10、engine 上限同時 4 個 sequence、每秒 14 個 request、重跑 2 次。
- 不開 admission：p95 TTFT（time to first token）約 2.5 秒，上下浮動約 700 毫秒。
- queue 上限 policy（最多 2 個 request 在等）：admit 約 63%、拒絕約 37%，p95 TTFT 降到約 1 秒（他說「好 2.5 倍」），goodput 持平。
- 他最喜歡的結果：同一次 run，**KV cache 用量最高只有 0.5%**，queue 卻深到 24 個。小模型、4 個短 sequence，KV cache 相對巨大、永遠填不滿，壓力全在 queue。**等 KV 壓力的 policy 會看到一條平線、admit 一切**——正是第 3 段表格第一列的失效條件。

**筆電就能試**（49:30–50:00）：附一個會在負載下變忙、提供 harness 所需三個 endpoint 的假 engine，可以在筆電上試整套流程；自己寫的 policy 包成獨立套件，AdmitPerf 會自動發現。歡迎貢獻 policy、工作負載、engine adapter、指標。

### 收尾（50:00–52:00）

如果只記一張投影片：在 inference 叢集收 request 時，**要有機制及早說不**，在 ingress、在說 yes 之前、在 request 進 GPU 占記憶體之前。並且處理好 admission policy 回傳的錯誤碼。AdmitPerf 起源於寫 handbook 時做的調查發現了缺口。

## 回查結果（2026-11-19）

| 項目 | 結果 |
|---|---|
| AdmitPerf repo | **存在**：[harshuljain13/AdmitPerf](https://github.com/harshuljain13/AdmitPerf)，MIT，回查時 3 顆星、2026-09 建立、已發 0.0.x 版。內建 `kv_threshold`、`queue_depth`、`dual_gate`、`no_admission` 四個 policy |
| AdmitPerf 現況與演講**不同** | 2026-10-04 起 repo 合併了「retire-harness」，10-07 改成「package-only，cluster 移出」。README 現在明寫「It does not provision, serve, scrape, or generate load」。演講展示的起 GPU／smoke／bench／compare／關機五指令，現況變成 `make up`／`make smoke`（Helm chart，不屬於套件）加 `admitperf watch／report／compare／demo`。「同一個 decide 函式用在 gateway 與 benchmark」與「缺值不當 0」（README：「Absence is never zero」）仍在 |
| A10 實測數字 | **作者自己撤下了真實硬體數字**。README「On real hardware: not yet measured」一節寫：現有數字來自模擬 engine，「Earlier figures from real runs were removed rather than carried forward, because they could not be reproduced」。README 沒指名是哪一組，但演講裡唯一的真實 GPU 結果就是 A10 這組 |
| 狀態碼對應 | 演講說 pool 全滿回 **529**；AdmitPerf 現行 `reasons.py` 把容量類原因（kv_pressure、queue_depth、deadline_infeasible 等）一律對應 **503**，只有 tenant 配額與 rate limit 回 429，沒有 529。README 的說法是「503 means the server cannot serve anyone right now. 429 means this caller is asking for too much」 |
| signal liveness 沒人報 | AdmitPerf README 說 16 篇 admission 論文、七個報告項目中，signal liveness 一篇都沒報。這是**作者自己的調查**，調查本身回查時沒找到公開全文（handbook repo 裡沒有對應章節） |
| README 的另一個 liveness 例子 | A100-40GB 跑 Qwen2.5-7B、`max_num_seqs=64`、2,168-token request 時，`kv_used_fraction` 算術上不會超過約 0.35，門檻設 0.90 的 policy 在任何到達率下都不會觸發。和演講 A10 的論點同方向，但同樣是作者自己的算術 |
| handbook | [harshuljain13/llm-inference-at-scale](https://github.com/harshuljain13/llm-inference-at-scale) 存在，回查時 **280 顆星**，與演講說的「300+」對不上 |
| OpenAI 2023-11-08 事故 | **大致對得上，但成因更具體**。[官方事故頁](https://status.openai.com/incidents/00fpy0yxrx1q)：5:42–7:16 PT 大量 502／503；routing layer 節點撞到記憶體上限、readiness check 失敗；當天 completion 量創新高是臨界點，但慢性根因是程式碼在迴圈裡不斷配置新的 response buffer。處置是限制流量、重新部署、逐步放回；後續包含「Added rate limit controls for more graceful load shedding」。演講說的「加 replica 又撤回」在回查摘要裡沒看到，**未證實** |
| Anthropic 2026-01-21 事故 | **對得上**。[官方事故頁](https://status.claude.com/incidents/yrxt885v63jw)：約 14:00–15:26 UTC，部分 API 使用者在 Sonnet 4.5 遇到錯誤率升高與變慢；原因「insufficient compute capacity allocated to meet demand」；後續「implement monitoring improvements to detect capacity constraints earlier」 |
| 529 的意義 | **對得上**。[Claude API errors 文件](https://platform.claude.com/docs/en/api/errors)：529 `overloaded_error` 是 API 暫時過載，「can occur when the API experiences high traffic across all users」；429 `rate_limit_error` 是組織撞到 rate limit 或支出上限。官方 SDK 會對 rate limit 與 5xx 以 exponential backoff 自動重試（預設兩次）、有 `retry-after` 時遵守。文件也寫 streaming 在回 200 之後仍可能出錯，與演講「200 不保證完成」一致 |
| QLM | **存在**：[arXiv 2407.00047](https://arxiv.org/abs/2407.00047)〈Queue Management for SLO-Oriented Large Language Model Serving〉，摘要報 SLO 達成率提升 40–90%、吞吐量 20–400%。演講的「40–90%」對得上；「每個決定約 5 秒」本次沒在論文中核對到 |
| Concur | **存在**：[arXiv 2601.22705](https://arxiv.org/abs/2601.22705)，ICML 2026（[PMLR 頁](https://proceedings.mlr.press/v306/chen26fs.html)）。admit 整個 agent 的 middleware，AIMD 式、cache-aware 的 admission 演算法；agentic **batch** inference 吞吐量在 Qwen3-32B 最多 4.09 倍、DeepSeek-V3 1.90 倍。「4 倍」只對 Qwen3-32B 成立；「雙閘門」是演講的分類說法，論文自稱的是 congestion control 式演算法 |
| 「Fluid wait」與「Kronos」 | **沒查到**。逐字稿辨識不清，閱讀頁也沒寫論文名；搜尋找不到「TTFT deadline miss 99%→0」的形式化上界論文。這兩列數字無法核對 |

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| admission 應在 ingress、request 拿到 KV cache 之前決定 | 設計論證，邏輯完整（engine 要 admit 之後才知道成本），兩家 provider 的事後行動方向一致；但不是「ingress 優於 scheduler 內決策」的實證，只是「不必維護 fork」的取捨 |
| coding agent 一個任務 40–50 個呼叫、14 檔、10 測試 | **講者舉例、非量測**，沒給 trace |
| session 為單位比 request 好 | **他自己承認是示意圖**，沒有實測。Concur 是逐 agent admit 的一手例子，但它是離線 batch 情境 |
| 四篇論文的數字（10–25%、4 倍、40–90%、99%→0） | 各自是論文**自報**、不同模型與工作負載，講者自己說不能排名。其中兩篇查不到 |
| A10：p95 TTFT 約 2.5 秒 → 約 1 秒、admit 63%、goodput 持平、KV 峰值 0.5% | **單一小模型、單一 GPU、重跑 2 次、自報**；作者 repo 已撤下真實硬體數字並說無法重現。只能當「訊號可能不動」的示意 |
| 16 篇論文沒有兩篇設定相同、沒有一篇報 signal liveness | **作者自己的調查**，全文沒公開，無法核對 |

**勿引用**：
- 「AdmitPerf 在 A10 上把 p95 TTFT 降 2.5 倍且 goodput 不變」作為已驗證結果：作者 repo 現寫「On real hardware: not yet measured」，且說先前真實 run 的數字無法重現而移除。
- 「Concur 讓 SGLang 吞吐量變 4 倍」作為通用結論：論文只有 Qwen3-32B 達 4.09 倍、DeepSeek-V3 是 1.90 倍，而且是離線 batch 推論。
- 「OpenAI 2023-11 事故只是流量太大」：官方根因含一個 response buffer 重複配置的程式 bug，流量創新高是臨界點。
- 「AdmitPerf 有 infra up／bench run 等五個指令」：演講時的 harness 已在 2026-10 被移出套件。
- 以 529 當容量拒絕的通用標準碼：529 是 Anthropic API 自訂的過載碼，不是 HTTP 標準；AdmitPerf 自己現在用 503。

## 能搬到個人 Claude Code／Codex 工作流程的做法

**伺服器端那一半，多數人用不到**：只用 Claude、OpenAI 託管 API 的話，admission 是 provider 的事。只有在本機或團隊自架 vLLM／SGLang（例如讓 Codex 或其他 agent 接本地模型）時才需要。

**client 端那一半，人人用得到**。你寫的批次腳本、平行跑多個 `claude -p` 或 sub-agent 的 orchestrator，就是演講裡那個「2 秒送 40 個呼叫」的 agent：

1. **分清 429 和 529／503**：429 表示你送太多，降低自己同時在飛的呼叫數；529／503 表示對方整體過載，拉長等待、換模型或把任務擱著，不要更用力重試。
2. **遵守 `Retry-After`，再加 jitter**：等它給的秒數加一段隨機延遲。平行開的多個 worker 尤其要加，否則同時醒來又是一波尖峰。
3. **設 retry budget**：exponential backoff 加 jitter、重試有上限；用完就停下來回報，不要無限迴圈。官方 SDK 已內建有上限的重試，自己再包一層重試時要算進總次數，避免重試疊重試。
4. **限制 fan-out**：自己寫的平行派工設固定併發上限（例如同時最多 N 個），收到 429 就調降。這和 [[Girish-Konda-把-sub-agent-當分散式系統]] 的「讀到 rate limit 應降低後續派工」是同一件事。
5. **streaming timeout 從第一個 token 開始算**，並在放棄時真的關掉連線或終止子程序，不要留著背景請求。
6. **處理 200 之後中斷**：stream 斷在一半時，判斷能否從部分輸出續做，還是要整個重來；有副作用的步驟重來前先確認狀態。

**自架模型時可以照做**：
1. 先不加任何 policy，用 `admitperf watch <engine 的 /metrics URL>` 錄一段尖峰時的指標，看 KV 壓力、queue depth 哪一個真的會動。AdmitPerf README 把這步列為第一步，而且不需要改 gateway。
2. 依決策樹選 policy：有 deadline 用 deadline 類；KV 會滿用 KV 門檻；KV 不會滿就用 queue 門檻。
3. 用 AdmitPerf 的 `enforce` 參數或 shadow mode 先只記錄不擋，比較開與不開的 goodput（分母用所有到達的 request）。
4. 負載從 0.5× 掃到 2× 實測容量，至少重跑幾次看變異，並把七項揭露寫進結果。
5. AdmitPerf README 另外補了演講沒講的 benchmark 細節（用 `vllm bench serve` 時加 `--ignore-eos`、輸入要夠長 KV 才會先成為瓶頸）；照抄前先讀現行版本，因為這個 repo 變動很快。

## 與既有頁的關係與張力

- **補 [[Rohan-Pandey-用貝氏最佳化找-serving-設定]] 的另一半**：Pandey 調的是 engine 本身的設定、用 goodput 當目標；這場處理 engine 前面「該不該讓 request 進來」。兩場都用 goodput，但這場把**被拒絕的 request 算進分母**，正好回答 Pandey 頁指出的「goodput 沒交代 SLO 就無法判斷意義」：分母怎麼定同樣要揭露。兩頁的調參結果都要以「這組流量與硬體」為條件。
- **和 [[Girish-Konda-把-sub-agent-當分散式系統]] 是同一個問題的兩端**：Konda 從 orchestrator 端說「無界 fan-out 時下游用 429／503 推回，但 orchestrator 看不到推回」；這場從 server 端說「要回 agent 能照做的錯誤碼」。合起來是一個完整的 backpressure 迴圈：server 要回清楚的碼，client 要讀懂並減速。Konda 頁「容量必須在非同步啟動之前預留」也和這場「在 admit 之前決定」同構。
- **和 [[Joey-Wang-agent-量放大後壞掉的周邊系統]] 互相印證**：Wang 說 agent 量放大後壞的是周邊系統（叢集容量、佇列），Harvey 用每人併發上限與保留互動名額處理；那是在 agent 平台層做 admission，這場是在 inference 層做。兩者都主張「以 session／人為單位限制併發」比單純數請求更有用，但都是單一團隊的經驗。
- **「看得到的指標不一定會動」與 [[LLM-as-judge-知識庫頁面評分]] 同類**：一個量測若在你的條件下永遠不變，報出來的結果看起來正常其實沒意義；這場的 signal liveness 與那頁「評分規則決定結果可信度」是同一種警覺。
- **一個張力**：講者用「沒有一篇論文適合 coding agent」來導出「自己做、用我們的工具」，但 AdmitPerf 自己後來撤下了唯一的真實硬體數字、也把 benchmark harness 移出套件。演講提出的方法論（goodput 分母、七項揭露、signal liveness）比工具本身更站得住。
