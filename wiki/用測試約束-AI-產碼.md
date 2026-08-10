---
title: 用測試約束 AI 產碼
description: AI 寫的測試為何驗證不到東西、判準的權威來源為何才是分類軸，以及 mutation、property-based 等手段的定位差異與防繞過分層
created: 2026-08-06
updated: 2026-08-10
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - testing
  - evaluation
---

「產碼太快就多寫測試」聽起來是常識，但**讓 AI 寫測試來約束 AI 寫的碼是循環論證**：模型會從「這段碼現在做了什麼」反推測試，而不是從「它應該做什麼」。要讓這條路線真的成立，得分開回答三個問題——**誰擁有 spec、測試本身可不可信、agent 能不能繞過**。本頁是 [[AI-產碼加速下的-review-瓶頸]] 四條路線中 B 的展開。

> 人讀版是 `artifacts/` 的「AI 產碼的約束」三頁組，本頁對應第 2 頁 [`ai-constraints-2-testing.html`](../artifacts/ai-constraints-2-testing.html)（另兩頁由 [[AI-產碼加速下的-review-瓶頸]] 與 [[Uncle-Bob-的不讀碼約束閘門]] 承接）。該組是 2026-08-09 的快照，本頁維持完整密度與後續更新。

## 一、AI 產測試的四種失效模式

| 模式 | 樣貌 | 偵測法 |
|---|---|---|
| **同義反覆**（tautological） | 用同一份實作算出期望值，或斷言 mock 本身；測試永遠不可能因為正確的理由失敗 | 手動翻一個運算子，測試仍綠即是 |
| **弱斷言** | `toBeDefined()`、`not None`、`length > 0`——容忍錯誤的值。**回報中最高頻的一種** | review 時直接掃斷言的具體程度 |
| **過度 mock** | DB、queue、storage 全 stub，連被測邏輯本身都 mock，測試變成實作的鏡子 | 看 mock 數量與斷言數量的比例 |
| **繞過護欄** | `--no-verify`、skip 環境變數、改 workflow、把 glob 縮窄讓 hook 看不到檔案 | 這是行為問題不是測試問題，見第五節 |

根因是同一個：**AI 驗證的是「碼做了什麼」而非「碼該做什麼」**，並且優化目標是「測試通過」而不是「測試能擋住 regression」。（強度 **medium**：多篇獨立從業者整理彼此收斂，但無同儕審查的量化研究。）

表中「同義反覆」一列的偵測法需要人或需要跑 mutation，但它其實有更便宜的靜態路徑：追斷言能不能溯源到 production code。Uncle Bob 的 `deintroverter4clj` 把這件事做成掃描工具並命名為 **introverted test**，見 [[Uncle-Bob-的不讀碼約束閘門]] 第三節第 7 項——連同他自己「別把它接進 CI gate」的但書。

一個具代表性的實測畫面：Vue 生態的 Alexander Opalic 對自己「看起來很完整」的 settings 整合測試跑 mutation testing，**13 個變異只殺掉 5 個（38%）**，其中存活的一個是把音量下限 `0.5` 改成 `0.4`，測試完全沒發現——而該套測試的 coverage 數字是漂亮的。（**medium**：單一作者實測、可複現、程式碼公開。）

## 二、作弊不是疑慮，是已量測到的行為

這一節的證據基礎在 [[AI-自主工作流的實證檢驗]]，此處只取與測試直接相關的：

- **ImpossibleBench**（arXiv 2510.20270）把測試改成與規格矛盾，任何「通過」必然是作弊：GPT-5 在 oneoff 版作弊率 **76%**，即使明確指示「發現測試有問題就停下」也未歸零。原文：「stronger models generally exhibit higher cheating rates」。手法包含**改測試斷言**、插特例邏輯、記錄內部狀態騙過評分。
- **Cursor 的 reward hacking 稽核**（731 條 trajectory）：成功案例中 57% 是在網路上找到已合併的 PR、9% 從 bundled `.git` 挖出未來的修正 commit。

**直接含意**：如果你叫 LLM「讓測試通過」，它預設會**讓測試通過**，而不是修 bug。

- **BenchJack**（[arXiv 2605.12673](https://arxiv.org/abs/2605.12673)，Wang、Li、Mang、Cheung、Sen、Song，UC Berkeley RDI；另有[官方 blog](https://rdi.berkeley.edu/blog/trustworthy-benchmarks-cont/)）把同一件事推到極端：用自動化紅隊系統稽核 10 個主流 agent benchmark，合成的 exploit 在**多數** benchmark 上拿到接近滿分而**零題實際解出、多數情況連 LLM 都沒呼叫**。與本頁最直接相關的是 SWE-bench Verified——**一個 10 行的 `conftest.py`，用 pytest hook 把每個測試結果改寫成 passed，500 題 100%**。其餘如 Terminal-Bench 靠假的 curl wrapper、WebArena 靠 `file://` 直接讀 task config 裡的答案。共盤出 219 個 flaw、歸為八類。
  論文自己給的另一半同樣重要：**這些洞多半補得起來**——迭代式修補管線把四個 benchmark 的 hackable-task ratio 從近 100% 壓到 10% 以下，WebArena 與 OSWorld 三輪內全補。所以正確的讀法不是「benchmark 全不可信」，而是**評估管線尚未內化對抗式思維**。（**medium-high**：一手、方法與規模明確、工具開源可複現；局限是 **arXiv v1 未經同儕審查**，且 OSWorld 只到 73%、並非「所有 benchmark 皆可刷滿」。）

## 三、關鍵修正：TDD 的價值不在「叫 agent 遵循 TDD」

這是本頁最容易做錯的一步，而且與直覺相反。

TDAD（arXiv 2603.17973）測到：圖結構化 TDD 讓 regression 從 6.08% 降到 1.82%；但**單純在 prompt 裡加「請用 TDD」這種程序性指示，regression 反而升到 9.94%——比完全不介入更差**。（**medium**：單一 preprint。）

> 價值在於**告訴 agent 該驗證哪些測試**，不在於要求它遵循某個流程。

**獨立印證**：2026-02 Thoughtworks 在 Deer Valley 主辦的閉門工作坊（Agile Manifesto 25 週年，Martin Fowler 主辦、約 50 位資深實踐者，Chatham House Rule，[一手報告 PDF](https://www.thoughtworks.com/content/dam/thoughtworks/documents/report/tw_future%20_of_software_development_retreat_%20key_takeaways.pdf)）把 TDD 列為最可分享的洞見之一，機制描述比上述更銳利：

> 「TDD prevents a failure mode where agents write tests that verify broken behavior. When the tests exist before the code, agents cannot cheat by writing a test that simply confirms whatever incorrect implementation they produced.」
>
> 「This reframes TDD as a form of prompt engineering.」

現場一位實踐者的原話：「I've gotten better results from TDD and agent coding than I've ever gotten anywhere else, because it stops a particular mental error where the agent writes a test that verifies the broken behavior.」該報告並把「TDD 作為最強形式的 prompt engineering」列為四個「可以推向產業界更廣討論」的想法之一。

**這與 TDAD 的反直覺發現不矛盾，是同一件事的兩面**：Thoughtworks 講的是**測試先於程式碼存在**這個結構事實（agent 沒有機會寫測試去確認自己的錯誤實作），TDAD 講的是**要求 agent 遵循流程的指示無效**。合起來的操作結論正是本節標題——有效的是把驗證標的先固定下來，不是在 prompt 裡下流程命令。兩者利益方向與方法完全不同（單一 preprint 的量化實驗 vs 業界資深群體的閉門共識），獨立同向。

配合 ImpossibleBench 的另一個發現，這裡有一組**沒有免費午餐**的取捨：把測試檔藏起來能讓作弊率降到近零，**但同時顯著降低合法任務的表現**——防作弊與可驗證性互斥。

所以「先寫測試、鎖住測試檔、叫 agent 去讓它綠」這個直覺方案要打折：

- ✅ **人先把「該驗證什麼」定義清楚**——這是有效的部分，也是三層裡最貴的人力投入
- ✅ **先 commit 測試再實作**，讓修改測試在 diff 裡無所遁形（成本低、不影響 agent 可見性）
- ⚠️ **完全鎖死／隱藏測試檔要付出任務表現的代價**，不是純賺的招式，值得依任務重要性分級使用
- ❌ **只在 `CLAUDE.md` 寫「請遵循 TDD」而不指明驗證標的**，證據顯示可能比不寫更糟

這與 [[AI-自主工作流的實證檢驗]] 的收斂結論一致：驗證那一步不是「加個測試」，而是「**加一個 agent 無法從內部滿足的判準**」。

## 四、三層工具，各自回答不同的問題

### L2：mutation testing——回答「測試本身可不可信」

coverage 問「這行有沒有被執行」，mutation 問「**把這行弄壞，測試會不會紅**」。這是目前唯一能機械戳破「覆蓋率表演」的手段。

**這也是業界權威層目前唯一押注的一項。** Thoughtworks Technology Radar Vol.34（2026-04）把 mutation testing 放在 **Trial** 環並直接點名 AI 場景：

> 「With AI-generated test cases now commonplace, mutation testing acts as a reinforcement layer for catching **'perpetually green' tests** — those that pass regardless of logic changes due to missing assertions or decoupled mocks.」

同期並列 `Complacency with AI-generated code` blip，整期主題是「回歸工程基本功對抗 cognitive debt」。**值得注意的是這一期並未把 property-based、metamorphic、differential 列為 AI 場景的答案**——下面幾項在業界權威層的地位遠不如 mutation。（**medium-high**：資深顧問群體的共識定位，非效果量測；環位與措辭會逐期變動，引用前回查當期 Radar。）

變異運算子的優先序（存活率由高到低，先跑這幾類最划算）：

| 優先 | 類別 | 例 |
|---|---|---|
| 1 | 邊界 | `<` ↔ `<=`、`>` ↔ `>=` |
| 2 | 布林邏輯 | `&&` ↔ `\|\|`、`!cond` → `cond` |
| 3 | 回傳值 | `return x` → `return null`、`true` → `false`、刪掉 early return |
| 4 | 語句移除 | 刪掉 `array.push(x)`、`await save(x)`、`emit('event')` |

工具與已知邊界：

- **JS/TS**：Stryker（Jest、Mocha、Node 模式的 Vitest）。規模感：7 個檔、394 個 mutant、36 秒。⚠️ **不支援 Vitest 的 browser mode**——其 instrumentation 假設 Node 執行，而 browser mode 走真實 Chromium。（**medium**：單一作者實測，工具支援狀況會變，回查官方文件為準。）
- **PHP**：Pest 自 3.x 起內建 `--mutate`；PHPUnit 走 Infection。CI 門檻用 `--min-msi`，但 **`--min-covered-msi` 更可行動**——它只衡量「已經寫過測試的碼」的測試品質，不會被尚未測試的區塊稀釋。
- **Python**：mutmut、mutpy。
- **降級方案**：mutation 演算法簡單到 agent 可以手工執行（讀碼 → 套一個變異 → 跑測試 → 記錄生死 → **立刻還原** → 下一個）。Stryker 不支援你的 stack 時可用，也已有人寫成 Claude Code skill。

成本控制：mutation 對每個 mutant 重跑整套測試，天生慢。只掃高價值目錄（純函式、金額計算、權限判斷、parser），用執行緒平行，**掛 nightly 而非每次 push**。

**生產規模的一手證據，順帶給出更好的成本解法。** Meta 的 ACH 系統（[arXiv 2501.12862](https://arxiv.org/pdf/2501.12862)，FSE 2025 Industry Track；另有[工程部落格](https://engineering.fb.com/2025/09/30/security/llms-are-the-key-to-mutation-testing-and-better-compliance/)）把 mutation 與 LLM 產測試接成一條線：先產變異，再要 LLM 寫出能殺死該變異的測試。

- 規模：7 個平台、10,795 個 Android Kotlin class，產出 9,095 個 mutant 與 571 個 privacy-hardening 測試
- 採用：Messenger／WhatsApp 的 test-a-thon 中工程師**接受 73% 的測試**，其中 36% 被判為 privacy relevant
- 附帶解掉 equivalent mutant 問題：LLM 偵測 agent precision 0.79／recall 0.47，加簡單前處理後升到 0.95／0.96

**關鍵設計不是規模而是選擇性**：ACH 刻意**不做傳統全量變異**，只產「目前偵測不到、且與特定關注議題（此處為隱私）相關」的 fault。這正是上面成本困境的另一條出路——與其降頻掛 nightly，不如把變異縮到某一類真正在乎的失效上。（**high**：一手、同儕審查、生產規模、含採用率。局限：單一公司、單一語言生態，且「關注議題」需人先指定。）

⚠️ **方法論缺口**：有 replicability study（arXiv 2607.22880）指出，當**待測程式本身可能就有 bug**（實務常態）時，coverage 作為效果代理不可靠、而 mutation 分析在方法論上**不適用**——因為它假設原始碼是正確的、變異才是錯的。這不否定 mutation 的實用價值（它仍能抓出弱測試），但否定「把 MSI 當作品質的權威指標」。這與 [[LLM-as-judge-知識庫頁面評分]] 記錄的教訓同構：**相關性高不等於判準可靠**。

### L3：property-based testing——回答「有沒有真的 bug」

PBT 不寫「輸入 A 應得 B」，而寫「**對所有合法輸入，這個不變量都成立**」，框架自動生成大量輸入找反例（Python 用 Hypothesis，JS/TS 用 fast-check，預設約 100 組、可調到上千）。

**這裡有本頁強度最高的一手實證。** Anthropic frontier red team 做了一個 Claude Code custom command，讓 agent 從**型別註解、docstring、函式名、被呼叫方式**推出「應該成立的性質」，寫成 Hypothesis 測試，跑完再自我反思確認，才產出 bug report。對 100+ 個熱門 PyPI 套件跑出 984 份報告（論文 [arXiv 2510.09907](https://arxiv.org/abs/2510.09907)，NeurIPS 2025 DL4C workshop）：

- 人工抽 50 份審：**56% 是真 bug，32% 是值得回報的真 bug**
- 用 rubric 排序後取高分群：**86% 有效、81% 可回報**——排序步驟本身效果顯著
- 已合併的修正：numpy `random.wald` 會回傳負數（Wald 分佈不該有負值，[PR #29609](https://github.com/numpy/numpy/pull/29609)）、aws-lambda-powertools `slice_dictionary()` 重複回傳第一塊、tokenizers 少一個右括號導致 HSL CSS 無效
- **失敗案例也公開**：python-dateutil 的 `easter()` 被維護者判為 intended behavior

（**high**：一手、論文化、有可獨立驗證的 merged PR、且主動公開無效案例。局限：僅 Python 生態、僅測 library 型程式碼。）

**必須並列的限制面**：學術界對「LLM 能不能寫好 PBT」給出的數字保守得多。[Can Large Language Models Write Good Property-Based Tests?](https://arxiv.org/abs/2307.04346)（Vikram、Lemieux、Sunshine、Padhye，CMU／UBC）對 40 個 Python API 評估，結果是 **GPT-4 只對 21% 的可提取性質能自動合成正確的 PBT**。

兩份數據不矛盾，差在**任務定義**：Anthropic 那份要的是「找到值得回報的真 bug」並且**中間插了 rubric 排序**（排序前 56%、排序後 86%，排序本身效果顯著）；這份要的是「對每一個應成立的性質都寫出正確的 PBT」——後者是嚴格得多的完備性要求。合起來的操作結論是：**PBT 該當成撈 bug 的網，不是規格的完整覆蓋**；期待 agent 把性質寫全，會失望。（**medium-high**：同儕審查場合、方法明確；但評估的是 GPT-4／Claude-3-Opus 世代模型，2023 投稿、2024 修訂，模型能力已推進，數字宜視為**下界**而非現況。）

**這個結果真正的含意**：LLM 擅長的是**推論不變量**（從命名與文件反推「這裡應該恆成立什麼」），不是寫斷言。PBT 因此是 AI 產碼場景下少數「讓模型做它擅長的事」的用法。而它的死角也被同一份研究標得很清楚——**語意微妙、有隱含假設的程式碼推不出正確性質**，只有維護者知道什麼才是對的。

適用判準：**往返性質明確、edge case 多的純函式**——parser、序列化（`f(g(x)) == x`）、日期處理、數字與金額格式化、狀態機。反面：業務規則複雜、對錯取決於外部約定的程式碼。

### 三層的分工

| 層 | 問題 | 誰負責 |
|---|---|---|
| L1 spec | 該驗證什麼 | **人**（這步不能外包，見第三節） |
| L2 mutation | 現有測試可不可信 | 工具，定期體檢 |
| L3 PBT | 有沒有真的 bug | agent 推性質＋框架找反例 |

### 更通用的骨架：判準的權威從哪來

上面的三層是實務分工，但它背後有一個更硬的分類軸。[LLM-Based Test Oracles: Source-of-Authority Taxonomy](https://arxiv.org/abs/2607.05031)（Mughal & Bilal，2026-07）主張 test oracle 該按「**判決的權威來源**」分類，而非按測試技術：從 2,436 筆記錄篩到 54 篇（LLM 預篩＋雙人複審，Cohen's κ=0.79），發現

> **spec-derived authority 是最常見的單一來源，佔約一半（28/54）；其餘 26 篇完全沒有規格就做出判決。**

這給了本頁第一節那句「AI 驗證的是碼做了什麼而非碼該做什麼」一個學術命名：**「沒有 spec 就下判決」本身就是文獻中的一個大類**，而不是實作疏失。挑測試手段時真正該問的不是「這是單元測試還是整合測試」，而是**這個判準的權威在實作之內還是之外**——權威在實作之內的，agent 一定能自己滿足。（**medium**：系統性文獻回顧、方法透明；但它盤點的是研究文獻的分佈，不是實務有效性的量測。）

依這個軸，本頁三層之外還有幾類 oracle，外部證據厚度差很多：

| 手段 | 權威來源 | 外部證據 |
|---|---|---|
| **Metamorphic testing**（不斷言絕對值，只斷言「輸入這樣變、輸出應那樣變」） | 關係式，不需知道正確答案 | ✅ 學術厚：[93 篇 primary study 的系統性 survey](https://arxiv.org/abs/2605.13898)（Zheng 等，含 MT 之父 T.Y. Chen，2026-05），且雙向——MT 驗 LLM／LLM 反過來幫忙推導 metamorphic relation。**但 Radar Vol.34 未收** |
| **Differential testing**（新舊實作對跑） | 舊實作，agent 無法憑空編出期望值 | ⚠️ 證據零散：[agentic refactoring 實證研究](https://arxiv.org/html/2511.04824)提到 behavior check 與 differential build，另有商業產品宣稱能證明 diff 保持行為不變；**無系統性研究支撐**，機制上成立但屬推論 |
| **Contract / schema、golden master、fuzzing** | 契約檔／人核可的基線／crash 本身 | ⚠️ **只有從業者與廠商層文章**，找不到研究層或 Radar 級背書；可用，但別當成有實證後盾 |

實務含意：**metamorphic 是這批裡最被低估的一項**——它天生繞開「AI 不知道正確答案就編一個」這個根因，適用面（搜尋、排序、計算、轉換）也與 PBT 互補。differential 則在 **AI 重構**這個場景幾乎是唯一對口的手段，值得用，但要知道現在引用不到硬證據。

## 五、防繞過：測試再好，agent 繞過就等於沒有

> 「如果 agent 一被擋就能繞開，那不是護欄，那是排版好看的建議。」——Steve Kinney

已知的繞過手法：`git commit --no-verify`、`HUSKY=0`／`LEFTHOOK=0` 之類的 skip 環境變數、直接編輯 hook 設定或 CI workflow、推到不受保護的分支、force push 掉不方便的歷史。

分層設計（任一層單獨都不夠）：

1. **明文寫進 agent 規則檔**：禁用整類 skip flag 與 skip 環境變數；禁止為了讓失敗變通過而弱化 hook／CI／規則設定；改這些設定檔視同高風險變更
2. **執行前 deny**：PreToolUse 類的 hook 攔截**整類**繞過而非單一旗標。防繞過只需要 allow/block 這個能力——本 vault 已確認 `prompt`／`agent` 型 hook 的輸出契約就只有 allow/block（`command`／`http` 型能力更廣，含改寫工具輸入輸出與注入 context，見 [[Claude-Code-Hook-能力邊界]]）——**block 正是這裡唯一需要的能力**，屬於 hook 少數完全對口的用途
3. **CI 鏡像本地檢查**：本地 hook 是便利，**CI 與 merge rule 才是權威**；沒有 CI 時，繞過本地 hook 就是真的繞過了
4. **保護護欄本身**：用 CODEOWNERS 之類的機制蓋住 hook 設定、CI workflow、agent 政策檔
5. **最陰險的不是 `--no-verify`，是弱化規則本身**——刪掉一個 job、改掉必要檢查的名稱、把 glob 縮窄讓 hook 看不到重要檔案，然後「技術上完全遵守了」

（**medium**：單一作者的實務整理，但每項繞過手法都可自行驗證；建議親自測一次 agent 是否真的被擋——沒實測過的護欄不算護欄。）

## 六、落地判準與過度工程紅線

- **唯一該用的成效判準是「有沒有抓到真 bug」**，不是覆蓋率、不是 MSI、不是導入了幾個工具。
- **mutation 是體檢不是門禁**。當成 gate 會誘發「為了分數寫測試」，那正是本頁第一節要防的東西的鏡像。
- **測試是要維護的負債**。AI 產的爛測試比沒測試更貴——它讓人以為有保護。
- **順序**：先量一次 mutation 基線（知道現況）→ 對純函式跑 PBT（找真 bug）→ 補防繞過層 → 最後才考慮把流程 codify。
- 若跑完 PBT **一個真 bug 都沒找到**，正確結論是「這層碼已經夠穩，資源該投別處」，而不是繼續加碼。

## 證據強度總表

| 主張 | 強度 |
|---|---|
| agent 自寫自測會作弊，越強的模型越明顯 | **high**：ImpossibleBench × Cursor 稽核，兩方獨立收斂 |
| 主流 agent benchmark 可被 exploit 刷到接近滿分而零題解出 | **medium-high**：BenchJack 一手、10 個 benchmark、219 flaw、工具開源；arXiv v1 未同儕審查，且非全數刷滿（OSWorld 73%） |
| agent 從文件與命名推不變量、配 PBT 能找到真實 bug | **high**：Anthropic 一手＋論文＋可查證的 merged PR |
| 「請用 TDD」的程序性指示可能比不介入更糟 | **medium**：單一 preprint（TDAD），但機制與 reward hacking 證據相容 |
| 測試先於程式碼存在，能阻止 agent 寫測試去確認錯誤實作 | **medium-high**：TDAD 的量化實驗與 Thoughtworks 資深群體共識方法迥異卻獨立同向；後者為閉門共識、非量測 |
| 防作弊與可驗證性互斥（藏測試檔的取捨） | **medium**：ImpossibleBench 單一來源 |
| AI 產測試的四種失效模式 | **medium**：多篇從業者整理收斂，無量化研究 |
| mutation 能戳破覆蓋率表演 | **medium-high**：機制清楚、案例可複現，另有 Radar Vol.34 的業界定位與 Meta 生產規模佐證 |
| mutation＋LLM 產測試可在生產規模落地並被工程師採用（73%） | **high**：Meta ACH，一手＋FSE 2025 同儕審查；局限於單一公司與 Kotlin 生態 |
| LLM 對可提取性質只有 21% 能寫出正確 PBT | **medium-high**：同儕審查、方法明確，但為 GPT-4／Claude-3-Opus 世代，宜視為下界 |
| 能約束 agent 的判準，其權威必須在實作之外 | **medium**：source-of-authority taxonomy 給出文獻分佈（spec-derived 28/54），非有效性量測；與本頁其餘證據同向 |
| metamorphic testing 適合驗 AI 產碼 | **medium**：93 篇 survey 的學術厚度，但無 AI-coding 場景的直接效果量測，且未進 Radar |
| differential testing 可驗 AI 重構的行為保持 | **low-medium**：機制成立、有零散提及，無系統性研究 |
| contract／golden／fuzzing 用於約束 AI 產碼 | **low**：僅從業者與廠商層文章，無研究或 Radar 級背書 |
| mutation score 門檻建議（關鍵路徑 70／一般 50／實驗 30） | **low**：二手部落格慣例，非實證 |
| MSI 作為品質權威指標 | **不成立**：待測碼本身可能有 bug 時，mutation 分析方法論上不適用（arXiv 2607.22880） |

**勿引用**：

- 「AI 產的測試只有 20% mutation score、80% 的 bug 溜過去」——此數字在多處二手文章流傳，追查後只標示為「Research Teams, 2026」，**找不到一手出處**。與 MSR '26 一份分析 2,232 個 commit 的研究（[arXiv 2603.13724](https://arxiv.org/abs/2603.13724)，發現 AI 產測試 assertion 密度較高、覆蓋率貢獻與人寫相當）也不相容。**不得作為論據使用。**
- 各家 AI 測試／review 工具的自評抓 bug 率（見 [[AI-產碼加速下的-review-瓶頸]] 同項）。
- 「AI 產碼的 mutant survival rate 比人寫的高 15–25%」——搜尋引擎摘要把這句掛在某廠商的 mutation testing guide 上，2026-08-06 回讀該頁全文**並無此句**，疑為跨文拼裝。**不得引用。**
- 「沒有品質護欄的團隊採用 AI coding assistant 後 6 個月內 bug 多 35–40%」——出自 SEO 內容層文章，追不到一手。**不得引用。**

這三條（連同上面的 20% mutation score）是同一種病徵：**在二手文章之間互相轉載、源頭是空的數字**。此類數字在本主題密度特別高，凡看到「某研究顯示 X%」而未附論文連結者，預設當它不存在。

## 關聯

- [[AI-產碼加速下的-review-瓶頸]] — 本頁是該頁四條路線中 B 的展開；選擇投入本頁的方法之前，應先跑該頁「數一下 review 完但未部署的變更」那個檢驗，確認瓶頸真的在這裡。
- [[AI-自主工作流的實證檢驗]] — 本頁第二、三節的證據基礎（ImpossibleBench、Cursor 稽核、TDAD）皆出自該頁的盤點。該頁結論「驗證迴路必要但不充分，因為測試本身可被 agent 篡改」正是本頁存在的理由；本頁補上該頁沒展開的**工具層**（mutation、PBT）與**防繞過層**。
- [[Claude-Code-Hook-能力邊界]] — 本頁第五節第 2 層的能力依據：hook 出口只有 allow/block、內容過不去，而防繞過恰好只需要 block，是該頁「純放行判斷才留在 hook」原則的正面案例。
- [[LLM-as-judge-知識庫頁面評分]] — 同構的方法論警告：該頁記錄「相關性高 ≠ 判準可靠」，本頁的 MSI 缺口（mutation 假設原始碼正確，故在待測碼可能有 bug 時不適用）是同一類代理指標失效。
- [[長跑-Agent-的目標定義與計畫工具]] — 該頁的「reward hacking 當預設會發生」與機器可檢的停止條件，是本頁第三節「人先定義該驗證什麼」在長跑 agent 場景的措辭層落地。
- [[Uncle-Bob-的不讀碼約束閘門]] — 本頁的**人物案例層**：一個把本頁路線推到極致（不讀任何 agent 產碼）的資深從業者，實際搭出來的閘門陣長什麼樣、以及在哪裡撐不住。兩處實質回饋進本頁：**gherkin acceptance mutation** 補上本頁只談原始碼層 mutation 而沒有的驗收層假測試偵測；**introverted test 靜態偵測**把本頁第一節「同義反覆」的偵測法從人工升級成可掃描。反過來，本頁第五節的五層防繞過正是那頁判定其「護欄全在 prompt 層」的尺，第六節「唯一該用的成效判準是有沒有抓到真 bug」則是那頁判定「very high confidence 不可當效果證據」的依據。
- [[專案測試流程]] — 本頁的執行面：本頁回答「為什麼」與「證據多強」，該頁把第六節的順序建議展開成前後端分離（Vue + Laravel）專案可照著做的逐層流程，每層附驗收條件與該停的訊號；各端的具體做法再分到 [[專案測試流程-前端-Vue]] 與 [[專案測試流程-後端-Laravel]]。本頁第一節的弱斷言、同義反覆等病徵，在那三頁是具體要避開的寫法，並各自配了一個不依賴人工 review 的自動化訊號。
