---
title: 平行 agent 產出的合併與 review
description: 多個 coding agent 平行產出後的整合面：衝突率實證、切分與合併順序、LLM 解衝突與 best-of-N 的上限、人工 review 變薄
created: 2026-09-16
updated: 2026-09-21
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - evaluation
---

本頁承接 [[平行跑多個-coding-agent-的工具選型]] 的結論「平行的瓶頸在 review 與合併」，回答下一個問題：**多個 agent 各自在 git worktree 分支上做完之後，產出怎麼合回主線、人怎麼 review**。

證據來源與強度：

- **deep-research 3 票對抗驗證**（2026-09-15～16），本輪通過的主張全數 3-0、無否決。
- **主 agent 回查**：各論文的標題、發表狀態與摘要數字，已從 arXiv 摘要頁逐篇核對。同儕審查的只有 AgenticFlict（AIware 2026）、2605.02273（EASE 2026）、2605.22534（MSR 2026），其餘為 preprint。
- **適用落差**：衝突率與 review 研究的對象都是 **GitHub 公開 PR**，不是本機平行 worktree。套到本機流程屬推論，下文不再逐句重複。
- **時效**：LLM 解衝突與 best-of-N 的絕對數字來自 2025 世代模型，會隨模型進步過期。可以沿用的是結構性結論：挑選與驗證是瓶頸、文字合併不保證語意正確。

## 一、衝突有多常見

- **agent PR 約四分之一以上會有文字衝突**：[AgenticFlict](https://arxiv.org/abs/2604.03551)（AIware 2026 接受，ACM DOI `10.1145/3805760.3814923`）收集 142K+ 個 agent PR，其中 107K+ 個跑完確定性合併模擬，29K+ 個有衝突，衝突率 **27.67%**，各 agent 之間差異明顯。強度：同儕審查的資料集論文，但只算文字衝突，而且是重新模擬合併，不是開發者實際遇到的衝突。
- **跨 agent 撞車的機率約是同 agent 的兩倍**：[2607.04697](https://arxiv.org/abs/2607.04697)（preprint）使用 AIDev-pop 資料集（33,596 個 PR）。只算時間真正重疊時，40.2% 的 repo 有同時活躍的 agent PR 對。這些 PR 對當中，同一 agent 產出的衝突率約 **19.8%**，不同 agent 之間約 **41.7%**，兩者的 95% 信賴區間不重疊。強度：跨 agent 的 PR 對只有 115 對，樣本小。
- **worktree 只隔離檔案系統，擋不住語意衝突**：例如 A 分支改了函式名，B 分支新增呼叫舊名的地方。兩支各自都綠，合併時也沒有文字衝突，合併後卻會壞。這是 git 逐行合併的基本行為，也就是傳統的 semantic merge conflict，不依賴來源（[Grass 部落格](https://codeongrass.com/blog/parallel-worktrees-conflict-prediction/)，廠商文）的可信度。**推論**：合併後要重跑涵蓋整合邊界的測試，衝突率數字只是下限。

對本機流程的意涵（推論）：Claude Code、Codex、agy 混用正好落在「跨 agent」那一格。兩個 agent 要碰同一片程式碼時，比讓同一個 agent 開兩支更容易撞。

## 二、事前：切分降低衝突

- **依依賴結構切分**：[Co-Coder](https://arxiv.org/abs/2606.00953)（preprint，作者自評、未同儕審查）把多 agent 編排當成圖分割問題。做法是用靜態分析建依賴圖、把 hub 檔案單獨處理、以 community detection 分群，再依依賴關係排程。在 28 個任務上，通過率最多提升 14.0%、wall-clock 最多加速 2.10 倍、API 成本最多降 35%，比較對象包含 Claude Code agent teams。強度：數字都是「最多」，提升最大的是依賴最密的專案；提升來自整套系統，不單是切分。
- **經驗法則**（[Zylos](https://zylos.ai/research/2026-05-21-stacked-prs-ai-agent-collaboration/) 廠商研究部落格，無數據，屬從業者慣例而非實證）：
  - 先定好檔案歸屬；
  - 會碰同一批檔案的任務**依序做、不平行做**；
  - 每個 stack 層保持小而自成一體（約 200 行、只做一件事）。

這與舊頁 HN 串的「任務原子化、盡快合併，掛著的 worktree 太多會變惡夢」、kevinsync「很少讓 Claude 與 Codex 做真正不同的任務」方向一致（見 [[平行跑多個-coding-agent-的工具選型]]），也呼應 [[Context-優先與多-agent-的適用邊界]]：互相依賴的改動不適合平行。

## 三、合併：順序、預測與工具

**衝突預測**（單一廠商部落格 Grass，無數據，**做法可抄但效果未證**）：

- 比對各分支相對共同 base 的變更檔案（`git diff --name-only base...branch`）。檔案重疊只當黃燈，hunk 或 symbol 重疊才是強訊號；原文也沒證明後者較準。
- 時機是開 draft PR、每次 push、merge queue 失敗時。
- 有重疊時**指定先合一支，另一支 rebase 後重跑相關測試**。
- 警告分 low、medium、high 標籤，不一律擋下。長壽的 agent 分支要常 rebase。

**stacked PR 工具**（功能描述，verifier 已回查 [Graphite merge queue](https://graphite.com/docs/graphite-merge-queue) 與 GitHub stacked PR 官方文件；**不是成效證據**）：

- Graphite 的 stack-aware merge queue 可以把整個 stack 平行批次驗證。
- stack 部分合併後，Graphite 會自動 rebase 上層分支。
- `gh stack sync` 會串接 rebase 剩下的分支，並以 `--force-with-lease` 推送。
- 已知問題：gh-stack issue #118（推送失敗）、#354（每次 rebase 會破壞 review 歷史）。

**讓 LLM 自動解衝突：約五到六成與開發者一致，不能免驗**：

- [Merge-Bench](https://arxiv.org/abs/2605.25890)（preprint）Java 結果：
  - Gemini 2.5 Pro 正規化後一致 62.5%（逐字 54.7%）；
  - Claude Opus 4 為 51.2%（逐字 44.4%，另有 21.2% 未解）。
  - 限制：zero-shot、一次一個 hunk、不給工具與測試；排除超過 20 行或 512 token 的 hunk；作者自承整體表現可能被高估。
- [2607.27674](https://arxiv.org/abs/2607.27674)（preprint，單一作者，只測 Java）：generate-validate-retry agent 跑 ConflictBench，約 55% 與開發者一致，比 AutoMerge 的 36.7% 高。但領先主要來自覆蓋率（傳統工具常直接放棄），不是單題準確率。另外，它的 LLM judge 會放行未通過結構檢查的結果。
- **讀法**：「與開發者一致」是正確性的**下限**，不一致不等於錯，開發者自己也可能解錯，所以**不可**讀成「四到六成是錯的」。兩篇都不是 agent 在 worktree 內能跑測試、讀 repo 時自己解衝突的情境，那種情境的成效目前沒有實證。

## 四、review：人工變薄是觀測到的事實

- **產量與 reviewer 的剪刀差**：[2607.01904〈AI Writes Faster Than Humans Can Review〉](https://arxiv.org/abs/2607.01904)（preprint，單一企業觀察研究，因果推論有限）追蹤一家中型企業的「2x」要求，涵蓋 802 名開發者、196,212 件 PR：
  - 摘要一手：人均吞吐量到 2026-04 達基準的 2.09 倍。
  - 內文數字經 verifier 讀 PDF 3-0 確認、主 agent 未親核：PR 量增 3.1 倍，reviewer 只增 1.5 倍。
  - 缺口主要由 AI review 吸收：有人工 review 的 PR 從 89% 降到 68%，有 AI review 的從約 19% 升到約 84%。
  - 人工 review 也變薄：有人寫留言的 review 從約 39% 降到約 21%，無留言核准約翻倍。
  - 論文另指出 merge 率與 revert 率大致穩定，所以 review 變薄**沒有**反映在這些粗略品質指標上。
- **公開 GitHub 的 agent PR 常沒有實質人工 review**（同儕審查兩篇）：
  - [2605.02273](https://arxiv.org/abs/2605.02273)（EASE 2026）：約 61.38% 的 agent PR 沒有任何 review 紀錄；在同時有人類 PR 的 repo 降到 28.92%。agent PR 的 review 留言 71.58% 由 agent 寫。人類 review agent PR 時，25.92% 的留言是在對 agent 下指令，不是獨立評估（人類 PR 只有 1.63%）。
  - [2605.22534](https://arxiv.org/abs/2605.22534)（MSR 2026）：已合併的 agent PR 抽樣 364 件，只有 15.4% 需要 reviewer 明確介入。
  - 限制：「沒有紀錄」不等於沒人看過；下指令由 regex 分類（`@coderabbit review` 也算）；抽樣以 Codex 為主（167 件），Claude Code 只有 8 件。

這組觀測把 [[AI-產碼加速下的-review-瓶頸]] 的「認知說瓶頸在 review」補上一個具體機制：**瓶頸沒有被解掉，而是被 AI review 接手、人工 review 退化成放行**。它也是 [[Agent-維護知識庫的已知失效模式]] 所記 automation bias 在程式碼 review 上的實地樣本（推論，兩篇研究都沒有量測品質後果）。

## 五、best-of-N：產生容易，挑選才難

同一任務讓多個 agent 平行做再挑最好的，瓶頸在挑選：

- [CodeMonkeys](https://arxiv.org/abs/2501.14723)（preprint）在 SWE-bench Verified 上：
  - 候選中至少一個正確的比例是 69.8%，隨機挑約 45.8%。
  - 用「模型自產測試投票＋專做挑選的多輪 trajectory」得到 57.4%，整個 benchmark 總成本約 2,300 美元。
  - 約補回隨機與理想挑選之間**一半**的差距。
- [R2E-Gym](https://arxiv.org/abs/2504.07164)（preprint）26 次 rollout：
  - 任一候選正確的上限有 64.4%。
  - 只用跑測試、或只用 LLM 評分的 verifier 都停在約 43%（43.7%、42.8%）。
  - **兩者混合**（先用 LLM 分數取前幾名，再加測試分數）可達 51%。
  - 限制：測試由 agent 自產；LLM 評分用的是微調過的 verifier，不是通用 judge；只測單一 32B 模型。

**推論到人工挑選本機多份產出**：不要只看「測試綠了」，也不要只憑讀 diff 的印象，兩種訊號要疊用。先用測試過濾，再比 diff，順序合理但**沒有實證**。這與 [[AI-自主工作流的實證檢驗]]「agent 自驗不可信」一致：單一訊號的 verifier 天花板很低。

## 對本機流程的可行做法（綜合，非實證）

以下由上面各節組合而成，屬推論，每條的強度回看對應節：

1. **派工前**先劃檔案歸屬，碰同一批檔案的任務排成依序，不要平行。跨 agent（Claude 對 Codex）的任務更要分開（第一、二節）。
2. **合併前**用 `git diff --name-only` 比對各分支重疊，有重疊就指定先合哪支（第三節）。
3. **合併後**另一支 rebase 並重跑整合邊界測試，因為沒有文字衝突不代表沒壞（第一節）。
4. LLM 或 agent 解出的衝突**一律跑測試再收**，不當成已解決（第三節）。
5. AI review 可以當第一關，但要意識到人工 review 會自然退化成放行（第四節）。跨模型互審的方向性見 [[Multica-與-agent-看板的用法與適用邊界]]（單篇小樣本）。
6. best-of-N 挑選疊用測試與閱讀兩種訊號（第五節）。

## 勿引用與強度警示

- **本輪沒有否決主張**，但研究問題第 (4) 項（Simon Willison、HN、Claude Squad、Conductor 作者的第一手經驗）與「agent 自我 review、跨模型互審、CI gate 先擋的成效」**零條通過驗證**。這些面向的空白是「未查到」，不是「已排除」。第一手經驗改看 [[平行跑多個-coding-agent-的工具選型]] 由主 agent 核對過的那一節。
- Emdash「把 diff review、PR、CI checks、merge 集中在同一介面」只是 [README](https://github.com/generalaction/emdash) 自述，沒有成效證據。
- 「stack 每層約 200 行」「hunk 或 symbol 重疊比檔案重疊準」都是廠商部落格的經驗值，不可當數據引用。

## 未解問題

- agent 在 worktree 內能跑測試、讀 repo 時自己解衝突，成效比 zero-shot 逐 hunk 的 benchmark 高多少？
- agent 自我 review、跨模型互審，能不能實際降低缺陷或人工負擔？企業研究只量到 AI review 的覆蓋率，沒量品質。
- 本機平行 worktree 的衝突率與切分效果，和 GitHub 公開 PR 資料有沒有差異？
- 人工比較 best-of-N 多份產出時，實務上怎麼分批排序最有效？缺從業者一手紀錄。

## 交叉引用

- 上游：[[平行跑多個-coding-agent-的工具選型]]。該頁選工具並給出「瓶頸在 review 與合併」的判斷，本頁接手這個瓶頸本身。
- review 地景：[[AI-產碼加速下的-review-瓶頸]]。該頁是單 agent 下的四條約束路線，本頁第四節的企業研究是它「認知與觀測互斥」的新觀測。
- 驗證路線：[[用測試約束-AI-產碼]]。第一節「合併後重跑整合測試」與第五節「測試是挑選訊號之一」都依賴測試本身可信，這正是該頁處理的問題。
- 適用邊界：[[Context-優先與多-agent-的適用邊界]]。第二節「互相依賴的任務依序做」是它在合併層的落地。
- 互審方向性：[[Multica-與-agent-看板的用法與適用邊界]]。
