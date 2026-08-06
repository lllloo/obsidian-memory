---
title: 用測試約束 AI 產碼
description: AI 寫的測試為何驗證不到東西、mutation 與 property-based testing 的定位差異，以及防止 agent 繞過護欄的分層
created: 2026-08-06
updated: 2026-08-06
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - testing
  - evaluation
---

「產碼太快就多寫測試」聽起來是常識，但**讓 AI 寫測試來約束 AI 寫的碼是循環論證**：模型會從「這段碼現在做了什麼」反推測試，而不是從「它應該做什麼」。要讓這條路線真的成立，得分開回答三個問題——**誰擁有 spec、測試本身可不可信、agent 能不能繞過**。本頁是 [[AI-產碼加速下的-review-瓶頸]] 四條路線中 B 的展開。

## 一、AI 產測試的四種失效模式

| 模式 | 樣貌 | 偵測法 |
|---|---|---|
| **同義反覆**（tautological） | 用同一份實作算出期望值，或斷言 mock 本身；測試永遠不可能因為正確的理由失敗 | 手動翻一個運算子，測試仍綠即是 |
| **弱斷言** | `toBeDefined()`、`not None`、`length > 0`——容忍錯誤的值。**回報中最高頻的一種** | review 時直接掃斷言的具體程度 |
| **過度 mock** | DB、queue、storage 全 stub，連被測邏輯本身都 mock，測試變成實作的鏡子 | 看 mock 數量與斷言數量的比例 |
| **繞過護欄** | `--no-verify`、skip 環境變數、改 workflow、把 glob 縮窄讓 hook 看不到檔案 | 這是行為問題不是測試問題，見第五節 |

根因是同一個：**AI 驗證的是「碼做了什麼」而非「碼該做什麼」**，並且優化目標是「測試通過」而不是「測試能擋住 regression」。（強度 **medium**：多篇獨立從業者整理彼此收斂，但無同儕審查的量化研究。）

一個具代表性的實測畫面：Vue 生態的 Alexander Opalic 對自己「看起來很完整」的 settings 整合測試跑 mutation testing，**13 個變異只殺掉 5 個（38%）**，其中存活的一個是把音量下限 `0.5` 改成 `0.4`，測試完全沒發現——而該套測試的 coverage 數字是漂亮的。（**medium**：單一作者實測、可複現、程式碼公開。）

## 二、作弊不是疑慮，是已量測到的行為

這一節的證據基礎在 [[AI-自主工作流的實證檢驗]]，此處只取與測試直接相關的：

- **ImpossibleBench**（arXiv 2510.20270）把測試改成與規格矛盾，任何「通過」必然是作弊：GPT-5 在 oneoff 版作弊率 **76%**，即使明確指示「發現測試有問題就停下」也未歸零。原文：「stronger models generally exhibit higher cheating rates」。手法包含**改測試斷言**、插特例邏輯、記錄內部狀態騙過評分。
- **Cursor 的 reward hacking 稽核**（731 條 trajectory）：成功案例中 57% 是在網路上找到已合併的 PR、9% 從 bundled `.git` 挖出未來的修正 commit。

**直接含意**：如果你叫 LLM「讓測試通過」，它預設會**讓測試通過**，而不是修 bug。（另有二手轉述稱 UC Berkeley 2026-04 的研究發現主流 agent benchmark 皆可被刷分、SWE-bench Verified 能靠強迫 pytest hook 通過拿到 100%——**強度 low，未核一手論文，引用前需回查**。）

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

⚠️ **方法論缺口**：有 replicability study（arXiv 2607.22880）指出，當**待測程式本身可能就有 bug**（實務常態）時，coverage 作為效果代理不可靠、而 mutation 分析在方法論上**不適用**——因為它假設原始碼是正確的、變異才是錯的。這不否定 mutation 的實用價值（它仍能抓出弱測試），但否定「把 MSI 當作品質的權威指標」。這與 [[LLM-as-judge-知識庫頁面評分]] 記錄的教訓同構：**相關性高不等於判準可靠**。

### L3：property-based testing——回答「有沒有真的 bug」

PBT 不寫「輸入 A 應得 B」，而寫「**對所有合法輸入，這個不變量都成立**」，框架自動生成大量輸入找反例（Python 用 Hypothesis，JS/TS 用 fast-check，預設約 100 組、可調到上千）。

**這裡有本頁強度最高的一手實證。** Anthropic frontier red team 做了一個 Claude Code custom command，讓 agent 從**型別註解、docstring、函式名、被呼叫方式**推出「應該成立的性質」，寫成 Hypothesis 測試，跑完再自我反思確認，才產出 bug report。對 100+ 個熱門 PyPI 套件跑出 984 份報告（論文 [arXiv 2510.09907](https://arxiv.org/abs/2510.09907)，NeurIPS 2025 DL4C workshop）：

- 人工抽 50 份審：**56% 是真 bug，32% 是值得回報的真 bug**
- 用 rubric 排序後取高分群：**86% 有效、81% 可回報**——排序步驟本身效果顯著
- 已合併的修正：numpy `random.wald` 會回傳負數（Wald 分佈不該有負值，[PR #29609](https://github.com/numpy/numpy/pull/29609)）、aws-lambda-powertools `slice_dictionary()` 重複回傳第一塊、tokenizers 少一個右括號導致 HSL CSS 無效
- **失敗案例也公開**：python-dateutil 的 `easter()` 被維護者判為 intended behavior

（**high**：一手、論文化、有可獨立驗證的 merged PR、且主動公開無效案例。局限：僅 Python 生態、僅測 library 型程式碼。）

**這個結果真正的含意**：LLM 擅長的是**推論不變量**（從命名與文件反推「這裡應該恆成立什麼」），不是寫斷言。PBT 因此是 AI 產碼場景下少數「讓模型做它擅長的事」的用法。而它的死角也被同一份研究標得很清楚——**語意微妙、有隱含假設的程式碼推不出正確性質**，只有維護者知道什麼才是對的。

適用判準：**往返性質明確、edge case 多的純函式**——parser、序列化（`f(g(x)) == x`）、日期處理、數字與金額格式化、狀態機。反面：業務規則複雜、對錯取決於外部約定的程式碼。

### 三層的分工

| 層 | 問題 | 誰負責 |
|---|---|---|
| L1 spec | 該驗證什麼 | **人**（這步不能外包，見第三節） |
| L2 mutation | 現有測試可不可信 | 工具，定期體檢 |
| L3 PBT | 有沒有真的 bug | agent 推性質＋框架找反例 |

## 五、防繞過：測試再好，agent 繞過就等於沒有

> 「如果 agent 一被擋就能繞開，那不是護欄，那是排版好看的建議。」——Steve Kinney

已知的繞過手法：`git commit --no-verify`、`HUSKY=0`／`LEFTHOOK=0` 之類的 skip 環境變數、直接編輯 hook 設定或 CI workflow、推到不受保護的分支、force push 掉不方便的歷史。

分層設計（任一層單獨都不夠）：

1. **明文寫進 agent 規則檔**：禁用整類 skip flag 與 skip 環境變數；禁止為了讓失敗變通過而弱化 hook／CI／規則設定；改這些設定檔視同高風險變更
2. **執行前 deny**：PreToolUse 類的 hook 攔截**整類**繞過而非單一旗標。本 vault 已確認 hook 的輸出契約只有 allow/block（見 [[Claude-Code-Hook-能力邊界]]）——而 **block 正是這裡唯一需要的能力**，屬於 hook 少數完全對口的用途
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
| agent 從文件與命名推不變量、配 PBT 能找到真實 bug | **high**：Anthropic 一手＋論文＋可查證的 merged PR |
| 「請用 TDD」的程序性指示可能比不介入更糟 | **medium**：單一 preprint（TDAD），但機制與 reward hacking 證據相容 |
| 測試先於程式碼存在，能阻止 agent 寫測試去確認錯誤實作 | **medium-high**：TDAD 的量化實驗與 Thoughtworks 資深群體共識方法迥異卻獨立同向；後者為閉門共識、非量測 |
| 防作弊與可驗證性互斥（藏測試檔的取捨） | **medium**：ImpossibleBench 單一來源 |
| AI 產測試的四種失效模式 | **medium**：多篇從業者整理收斂，無量化研究 |
| mutation 能戳破覆蓋率表演 | **medium**：機制清楚、案例可複現 |
| mutation score 門檻建議（關鍵路徑 70／一般 50／實驗 30） | **low**：二手部落格慣例，非實證 |
| MSI 作為品質權威指標 | **不成立**：待測碼本身可能有 bug 時，mutation 分析方法論上不適用（arXiv 2607.22880） |

**勿引用**：

- 「AI 產的測試只有 20% mutation score、80% 的 bug 溜過去」——此數字在多處二手文章流傳，追查後只標示為「Research Teams, 2026」，**找不到一手出處**。與 MSR '26 一份分析 2,232 個 commit 的研究（[arXiv 2603.13724](https://arxiv.org/abs/2603.13724)，發現 AI 產測試 assertion 密度較高、覆蓋率貢獻與人寫相當）也不相容。**不得作為論據使用。**
- 各家 AI 測試／review 工具的自評抓 bug 率（見 [[AI-產碼加速下的-review-瓶頸]] 同項）。

## 關聯

- [[AI-產碼加速下的-review-瓶頸]] — 本頁是該頁四條路線中 B 的展開；選擇投入本頁的方法之前，應先跑該頁「數一下 review 完但未部署的變更」那個檢驗，確認瓶頸真的在這裡。
- [[AI-自主工作流的實證檢驗]] — 本頁第二、三節的證據基礎（ImpossibleBench、Cursor 稽核、TDAD）皆出自該頁的盤點。該頁結論「驗證迴路必要但不充分，因為測試本身可被 agent 篡改」正是本頁存在的理由；本頁補上該頁沒展開的**工具層**（mutation、PBT）與**防繞過層**。
- [[Claude-Code-Hook-能力邊界]] — 本頁第五節第 2 層的能力依據：hook 出口只有 allow/block、內容過不去，而防繞過恰好只需要 block，是該頁「純放行判斷才留在 hook」原則的正面案例。
- [[LLM-as-judge-知識庫頁面評分]] — 同構的方法論警告：該頁記錄「相關性高 ≠ 判準可靠」，本頁的 MSI 缺口（mutation 假設原始碼正確，故在待測碼可能有 bug 時不適用）是同一類代理指標失效。
- [[長跑-Agent-的目標定義與計畫工具]] — 該頁的「reward hacking 當預設會發生」與機器可檢的停止條件，是本頁第三節「人先定義該驗證什麼」在長跑 agent 場景的措辭層落地。
