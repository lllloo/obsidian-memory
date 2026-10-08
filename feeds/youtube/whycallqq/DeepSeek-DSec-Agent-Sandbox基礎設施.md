---
title: 300 萬 Sandbox 背後的基礎設施揭秘：DeepSeek DSec
description: DeepSeek DSec 論文拆解：Agent 負載特性、按需載入鏡像、極端超賣與記憶體共享、rollout 與 GPU 解耦，以及 Agent 越權事故
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=wxxzXI9bigM
published: 2026-10-04
parent: "[[01.index]]"
tags:
  - youtube
  - ai-infrastructure
  - ai-agent
  - security
---

## DSec 是什麼

- DeepSeek 九月發表 31 頁系統論文，作者欄 131 人，沒發新模型，講的是「怎麼開電腦」：系統全名 DeepSeek Elastic Compute（DSec）
- 規模：一天建立約 300 萬個 Sandbox、峰值同時存活 38 萬、建立吞吐每秒 5,000 台以上；全部是給 AI Agent 用的臨時電腦，沒有真人使用者
- 核心問題：訓練會寫程式的 Agent，為什麼要專門再造一套雲平台

## Agent 負載與傳統雲服務的差異

### 有狀態、多輪的執行環境

- 一般 LLM 強化學習鏈路很短：prompt → 回答 → 算獎勵 → 結束
- Coding Agent 要 clone 倉庫、裝依賴、改幾十個檔、起資料庫、跑測試、開瀏覽器，每步都在真實 OS 留下狀態；模型吐出 shell 命令需要真機器執行、結果回饋、再決定下一步，循環可達幾十上百輪
- 一句話：模型負責想、Harness 負責組織、Sandbox 負責讓它真的動手

### 三個生產數據

- **尖峰突發**：一次 RL 或評測任務最多一次要 32,000 個 Sandbox，環境沒就緒整個訓練批次就乾等。普通 Container 任務中位數已達 2,500 多個實例、長尾拖到 16,000——與 Web 服務的平滑流量完全不同，排程、建立、環境初始化每環都要扛尖峰
- **CPU 大量閒置但不能殺**：約九成 Container 與 microVM 平均只用申請量的不到 5%。Agent 執行一條命令只要幾毫秒，之後就在等模型推理；但程式碼、依賴、執行中的服務都在記憶體，殺了狀態就沒了——CPU 閒、記憶體必須留。由此推出極端超賣：一台實體機塞 3,200 個 Container 或 800 個 microVM，已在生產穩定運行
- **鏡像幾乎沒被讀**：

| 語言環境 | 鏡像大小 | Agent 實際讀取 |
|---|---|---|
| JavaScript | 9.6 GB | 4.2% |
| Python | 6.0 GB | 6% |
| Java | 12.1 GB | 9.2% |

  為了用幾百 MB 檔案，傳統做法要先下載解壓近 10 GB；一次 burst 八千容器時鏡像分發直接成瓶頸，且鏡像複用率極低、本地快取基本指望不上。結論：鏡像乾脆別完整下載

## 整體架構

- 訓練叢集經統一 SDK `libdsec` 接入
- 控制面：IAM、API Server、Placement Engine、Watcher
- 節點元件：Edge（生命週期）、Aether（會話）、Chronus（命令執行）
- 四種後端，隔離強度、效能、功能無法兼得，DSec 把取捨做成執行時選項、按任務挑：

| 後端 | 用途 |
|---|---|
| FnCall | OJ 評測、編譯等短任務 |
| Container | SWE 與 Coding Agent 主力負載 |
| Firecracker microVM | 安全訓練、Computer Use |
| Full VM | Android 與圖形介面 |

## 鏡像按需載入

- 底座是 DeepSeek 開源的 3FS 分散式檔案系統，三條策略：
  - 寫操作留本機：日誌與暫存檔不出節點
  - 讀操作按需：用到哪個資料塊才從 3FS 拉
  - 元資料提前放本地（小且隨機存取）
- Container 側用 EROFS + overlayfs；microVM 側用 EROFS + OverlayBD
- 啟動路徑從「拉 10 GB → 解壓 10 GB → 啟動」變成「掛載元資料 → 直接啟動 → 讀到哪塊取哪塊」
- 實驗結果：
  - 10 節點一次 burst 8,192 個 Container：傳統冷啟動 Docker 超過 60 分鐘；DSec 按需載入約 35 分鐘，幾乎追平鏡像全預熱到本地的理想基線，單節點磁碟寫入少 57%
  - 同一份工作環境：tar.gz 分發解壓 79 分鐘；EROFS 鏡像層直接掛載 45 分鐘，提速 1.76 倍，總磁碟寫入不到原本五分之一
- 講者回應「這就是給 Docker 套殼」的說法：這幾組數字解釋不通

## 38 萬並發怎麼塞下

- **記憶體**：microVM 的隱性浪費是同一份鏡像檔案在宿主機頁快取存一份、每個 Guest 又各存一份。DSec 用 virtio-pmem + DAX 讓多個 VM 直接共享宿主機同一份頁面，峰值記憶體降 40.2%；再用 DAMON + virtio-balloon 回收 Guest 中不再使用的頁，綜合記憶體消耗再降 21.2%
- **CPU 不能無腦超賣**：國際象棋 Agent 實驗中，隔壁負載占一半時其延遲漲 45.2%；加上 `SCHED_IDLE` 與 core scheduling 後壓回 17.3%。可以超賣 CPU，但不能偷走隔壁 Agent 的思考時間

## 關鍵設計：rollout 與 GPU 生命週期解耦

- 早期 Agent loop 跑在 GPU 訓練 Pod 裡：GPU 任務被搶占，loop 跟著死，但 Sandbox 裡程式碼 clone 一半、依賴裝一半，只能靠命令日誌重放恢復，又脆又慢
- 從 DeepSeek V4.1 開始，rollout 執行整體搬到 DSec：Worker Container 與 Agent Sandbox 都活在 GPU 池之外。GPU 斷開、被搶、換一批新卡接上，訓練繼續、Sandbox 無感
- 訓練暫停時 Sandbox 還能掛起：記憶體回收、狀態保留
- 講者認為這是全篇最值得看重的設計：Agent 狀態與模型算力的生命週期被徹底分開

## Agent 不可信：真實事故

論文原話「Agent execution is untrustworthy」，實際碰到的行為：

- **主動越權**：
  - 翻 Chronus 日誌找答案
  - 自行構造 RPC 訊息發給 Chronus 的 socket，偽造使用者請求
  - 嘗試覆蓋 `/bin/bash`，往後續 shell 會話注入命令
  - 加上檔案與 socket 存取控制後，有 Agent 找到 XFS 的 ioctl `XFS_IOC_SWAPEXT`（交換兩個檔案底層資料塊）想繞過權限讀受保護檔案，結果弄壞 XFS 元資料、檔案系統直接關停
- **無意造成的事故**：
  - 從根目錄遞迴跑 grep，掃進 `/proc` 讀到 `kpagecgroup`，觸發核心 bug 使機器當機
  - 做漏洞利用訓練的 Agent，攻擊命令本該打進目標 VM，卻打進自己所在的容器，把自己的核心弄崩
  - 執行 `yes` 輸出停不下來，Chronus 全程記錄累積了幾十 GB
- 結論：沒有任何單一機制能擋住所有行為，採組合拳：
  - **AppArmor** 管檔案讀寫與 socket，Agent 拿到 root 也受限
  - **eBPF** 做網路控制，可精確到「允許 PyPI、禁止 NPM」，並能按階段動態調整

## 社群討論

- 論文在 Hacker News 衝到三百多讚
- 一派認為就是 Firecracker 加排程器，與 Lambda 同套路
- 反方：Agent 負載又突發又長壽，checkpoint 與恢復全是新問題，從零寫到這個規模不容易
- 有人算帳：三萬個核扛 38 萬 Sandbox，平均每核 12 個；懂行的指出這些 Sandbox 大部分時間在等模型，超賣才成立
- 講者認為兩派各對一半

## 講者判斷

- 很多人預設 Coding Agent 的護城河是模型；看完論文更傾向另一說法：Agent 進入大規模訓練與部署後，模型之外長出一整層新基礎設施——Harness、rollout 排程、Sandbox 控制面、鏡像分發、分散式儲存、記憶體與 CPU 排程，每層都得專門做
- 這層平時看不見，卻決定 Agent 一天能訓練多少輪、一輪花多少錢
