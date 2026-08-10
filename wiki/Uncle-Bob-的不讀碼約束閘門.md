---
title: Uncle Bob 的不讀碼約束閘門
description: 逐項解剖「不讀 agent 產碼、改用測試與度量包圍它」這套主張——每道閘門實際擋住什麼、他自己寫的工具怎麼實作、以及這套方案撐不住的三個地方
created: 2026-08-09
updated: 2026-08-10
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - testing
  - evaluation
---

Robert C. Martin 在 2026-07-23 的[推文](https://x.com/unclebobmartin/status/2080257779395154409)（5M views）宣告：**不讀 agent 寫的任何程式碼**，改用「極端約束」包圍 agent——「unit tests、gherkin tests、QA procedures、quality metrics、mutation testing、test coverage，以及其他一堆」，跑完這串 gauntlet 之後對產出有「very high confidence」。（推文串原文與同作者一個月前的相關前串已落地 [[Uncle-Bob-用約束取代讀-AI-產碼]]。）

這則推文值得逐項研究，原因不是它有名，而是**他把每一道閘門都自己寫成了工具、公開在 GitHub 上**。這讓「他到底在做什麼」從意見變成可檢驗的事實——本頁的一手依據幾乎全部來自那些 repo 的原始碼、角色 prompt 與 CI 設定，而不是轉述文章。

> **兩個結論在第二輪查證時被推翻，值得先講**（2026-08-09）：（1）第一輪判定「護欄全在 prompt 層、沒有機械強制」是**錯的**——漏看了 `.github/workflows/`，實際上驗收規格與 parser 被 CI 鎖死；（2）推文字面的「沒有人讀碼」也不成立——`swarm-forge` 的 `adversaries` 分支派了一個**對抗式 reviewer agent 專門讀碼**。真正的命題不是「測試取代 review」，而是「review 的判準可以被寫下來交給 agent 執行」。本頁是 [[用測試約束-AI-產碼]] 的一個具體人物案例：那頁回答「哪些手段有證據」，本頁回答「一個把這條路線推到極致的人，實際搭出來的東西長什麼樣、哪裡撐不住」。

> 人讀版是 `artifacts/` 的「AI 產碼的約束」三頁組，本頁對應第 3 頁 [`ai-constraints-3-uncle-bob.html`](../artifacts/ai-constraints-3-uncle-bob.html)（另兩頁由 [[AI-產碼加速下的-review-瓶頸]] 與 [[用測試約束-AI-產碼]] 承接）。該組是 2026-08-09 的快照，本頁維持完整密度與後續更新。

## 一、先清掉兩個流傳的誤讀

**誤讀一：「Lots of times I just use unit tests and crap.」** 這句被多篇二手文章當成他自嘲隨便測測。回讀他 2026-07-02 的[前串](https://x.com/unclebobmartin/status/2072736888478175413)，原文是：

> Lots of times I just use unit tests and **crap evaluation**. That seems to work pretty well.

`crap` 是 **CRAP（Change Risk Anti-Patterns）度量**，不是形容詞。斷句斷在 `crap` 後面，意思從「我用 CRAP 度量」反轉成「我隨便測測」。佐證是決定性的：他自己有 [`crap4java`](https://github.com/unclebob/crap4java)（★277）、`crap4clj`、`crap4go` 三個 repo。

**誤讀二：「七道閘門是他的標準做法」。** 同一則前串裡他自己就打了折：

> I've been pushing very hard on overloading with tests. […] But just because we can do them doesn't mean we actually should. […] For larger projects I can imagine that gherkin testing is pretty useful and so is QA testing. I'm checking that now.

他的編排工具 `swarm-forge` 也把這件事寫死進設計：`two-pack` 分支明文是「不含 Gherkin 與驗收測試的開銷」的快速流程。**閘門數量隨專案規模調整，不是一套鐵板清單。**

## 二、他實際建了什麼

七項約束對應到一組他親手寫、且**三個語言各做一套**的工具。這是本頁最硬的事實層（2026-08-09 經 GitHub API 逐一驗證存在）：

| 約束 | Clojure | Go | Java |
|---|---|---|---|
| Mutation testing | `clj-mutate` | `mutate4go` | `mutate4java` |
| Quality metric（CRAP） | `crap4clj` | `crap4go` | `crap4java` |
| 重複偵測（DRY） | `dry4clj` | `dry4go` | `dry4java` |

外加幾個只有 Clojure 版的：`dependency-checker`（元件邊界與依賴方向）、`deintroverter4clj`（見第三節第 7 項）、`speclj-structure-check`。跨語言的則是 [`Acceptance-Pipeline-Specification`](https://github.com/unclebob/Acceptance-Pipeline-Specification)（★168，Go/Babashka），以及編排層 [`swarm-forge`](https://github.com/unclebob/swarm-forge)（★1982）。

**這些不是散落的玩具，有一份憲法把它們接起來。** `swarm-forge` 的 `constitution/articles/engineering.prompt` 開頭就是工具採購指令：

> On startup, procure the latest version of each required CRAP, mutation, and DRY tool for the project language directly from the listed `github.com/unclebob/...` repositories and get each one ready to run.

`swarm-forge` 提供三種編制，直接對應閘門的取捨光譜：

| 編制 | 角色 | 什麼時候用 |
|---|---|---|
| `two-pack` | coder → cleaner | 小任務，**跳過 Gherkin 與驗收測試**，保留 CRAP／DRY／重構 |
| `four-pack` | specifier → coder → refactorer → architect | 中型，要 Gherkin 規格但不把每道閘門拆成獨立 agent |
| `six-pack` | specifier → coder → cleaner → architect → hardender → QA | 大型，每道品質閘門各有專責 agent |
| `adversaries` | coder ↔ reviewer | **對抗式雙人組**，見第四節前的專節——這個編制推翻了「沒人讀碼」的字面理解 |
| `squad` | squad-leader（＋動態生成的隱形 agent） | 實驗中：常駐一個可見的 leader，其餘 agent 由後續切片動態產生 |

（分支清單與角色檔為 2026-08-09 經 GitHub API 直讀，`squad` 分支只有 leader 一個角色檔，屬未完成的實驗。）

而 @rfleury 在串裡問的「你到底用這套做了什麼」，答案是 [`empire-2025`](https://github.com/unclebob/empire-2025)——經典戰棋遊戲 Empire 的 Clojure 重製版（★87，約 6 MB，100×60 地圖、九種兵種、電腦 AI）。這個答案很重要，第四節會回來談。

## 三、逐項研究

### 1. Unit tests

agent 寫、他不讀。這一項本身沒有新意，但**與既有證據有一處張力值得標出來**。

[[用測試約束-AI-產碼]] 第三節的收斂結論是：有效的不是「叫 agent 遵循 TDD」（TDAD 測到程序性指示反而讓 regression 升到 9.94%），而是**測試先於程式碼存在**這個結構事實。Uncle Bob 的 `empire-2025/AGENTS.md` 通篇沒有 TDD 指令；但 `swarm-forge` 的角色設計把它放回去了——`coder` 角色的職責明文是「implements requested behavior **with TDD** and unit tests」。

而 `coder.prompt` 的原文比「with TDD」四個字精確得多，其中一句直接對著假測試problem 開槍：

> Use TDD to specify behavior before implementation. First write focused unit tests that express the requested observable behavior and **would fail for a plausible wrong implementation**. Then write only enough production code to pass those tests.

「**會因為一個合理的錯誤實作而失敗**」——這就是 mutation testing 的判準，被寫成寫測試當下的自我檢查。用 prompt 要求 agent 自己滿足這個判準當然不如機械變異可靠（所以後面才有 hardender 真的跑 mutation），但它把正確的目標講清楚了，而不是含糊的「寫好測試」。

同一份檔案還有一條防止閘門互相稀釋的規則：

> **Do not rely on generated acceptance tests as a substitute for unit tests.**

換句話說，他把 TDD 從「寫在規則檔裡的口號」搬成**角色的定義**，並且用另一個角色（`specifier`）先把規格固定下來、經人核准才交手。這恰好落在證據支持的那一邊：先固定驗證標的，而不是下流程命令。（**medium-high**：角色檔為一手且措辭明確；但「這個設計是有意識地回應『TDD 指示無效』這個發現」仍是本頁推論，非他本人陳述。）

### 2. Gherkin tests——真正的創新在 gherkin mutation

Gherkin 本身是老東西（Given/When/Then 驗收規格）。他做的新東西叫 **acceptance mutation**，`Acceptance-Pipeline-Specification` 的 README 定義得很清楚：

> Acceptance mutation means mutating Gherkin example values in the specification-derived JSON IR. **It does not mean conventional mutation testing of application source code.**

管線是這樣的：

```
feature 檔 → gherkin parser → JSON IR → 驗收進入點產生器 → 專案測試 runner
                                  ↓
                            gherkin mutator（變異 example 值）→ mutation 報告
```

> The normal run proves that the project satisfies the feature. **The mutation run checks whether the acceptance tests fail when important example values change.**

**這是把 mutation 的思路搬上驗收層，用來抓一種特定的假測試**：Gherkin 場景寫得漂漂亮亮、也綠了，但 step definition 根本沒把 example 表格裡的值接到系統上——換掉數字，測試照樣綠。這正是 [[用測試約束-AI-產碼]] 第一節「同義反覆」與「弱斷言」在驗收層的化身，而該頁原本沒有對應的偵測手段（那頁的 mutation 只談原始碼層）。**這一項是本次研究對既有頁的實質補充。**

`mutator-spec.md` 定義的變異規則是**型別推斷式的值擾動**，刻意不含領域語意（「The portable mutator must not define command, enum, or domain-specific swaps」），且對固定路徑與原值為決定性偽隨機：

| 值型別 | 變異方式 | 例 |
|---|---|---|
| 整數 | 加一個非零隨機差 | `20 → 27` |
| 浮點 | 加一個非零隨機差 | `3.14 → 2.89` |
| 布林 | 取反 | `true → false` |
| null／nil／none | 換成非空字串 | — |
| ISO-8601 日期時間 | 依精度移動非零量 | `2026-05-13 → 2026-05-15` |
| 逗號分隔清單 | 隨機挑一項遞迴變異 | `2, 5, 8 → 2, 11, 8` |
| 其他字串 | dither（插入／刪除／置換／相鄰交換／改大小寫） | `accepted → accfpted` |

**兩條防「為了分數而作弊」的規則寫在角色檔裡，值得單獨抄。** `specifier.prompt`：

> Gherkin will be mutation tested; **use Gherkin parameters for any fields that might vary.** Prune identical Gherkin example-table columns when every row has the same value and the column does not improve Gherkin acceptance mutation.

`hardender.prompt` 講得更直白：

> If Gherkin mutation exposes a **no-op step**, consider **removing that step** from the Gherkin rather than adding example columns only to assert the no-op.

也就是說：變異存活代表這個步驟根本沒在驗任何東西，正確的反應是**刪掉那個假步驟**，而不是硬加一欄斷言把分數補回來。這與 [[用測試約束-AI-產碼]] 第六節「mutation 是體檢不是門禁、當成 gate 會誘發為了分數寫測試」是同一個警覺，只是他把對策直接寫進了 agent 的行為規則。

成本控制走的是差分：`--level` 有 `full`／`hard`／`soft` 三檔，決定什麼情況可以沿用上次結果——`full` 全跑，`hard`（預設）要 feature 內容、scenario、background **與實作雜湊**全部相符才沿用，`soft` 則**不看實作雜湊**。⚠️ `hardender` 的最終驗證序列用的是 `--level soft`，意味著**規格沒變、只有實作變了的 scenario 會沿用舊的「全殺光」結論而不重跑**。這是明確的成本取捨，但也是這套設定裡一個結構性的盲區。（**medium-high**：三檔定義從 `mutator-spec.md` 直讀、`--level soft` 從 `hardender.prompt` 直讀；「因此可能沿用過期結論」是依定義推導，非實測。）

`empire-2025` 的實作是同一管線的專案版：`.txt`（Given/When/Then）→ parser → `.edn` → generator → Speclj spec → 執行。

**但實際的驗收檔不是標準 Gherkin，是一套自製 DSL**——關鍵在於它用 ASCII 地圖直接當作初始狀態：

```
;===============================================================
; Army wakes near hostile city with reason.
;===============================================================
GIVEN game map
  A#+
A's target is +

WHEN a new round starts and A is waiting for input.

THEN the error message contains :army-found-city.
```

`A#+` 就是「陸軍、陸地、城市」三格相鄰的盤面。這解釋了他為什麼要自己寫 parser 而不用 Cucumber：**標準 Gherkin 的 example table 表達不了這種二維空間狀態**，而在戰棋領域，盤面就是規格最自然的寫法。可搬性的教訓是：Gherkin 的價值不在 Given/When/Then 這三個字，而在「規格用領域自己的語彙寫、且可執行」；照抄關鍵字卻用錯記法，反而會得到 Andy Knight 說的那種 UI 腳本式假規格。

`AGENTS.md` 對 agent 的規則裡有兩條特別值得抄：

> - Never modify an acceptance test `.txt` file without explicit permission.
> - If an acceptance test cannot be translated to a spec, report which test and why to the user. **Still generate the spec as a failing test documenting the desired behavior.**

第二條是好設計：翻譯不了的規格不會消失成沉默的缺口，而是變成一個紅燈。

**必須並列的反對意見**：測試自動化顧問 Zhimin Zhan 在[回應文](https://agileway.substack.com/p/reflections-on-robert-c-martins-popular)裡同意「不讀碼、靠自動化測試」的主張，卻**單獨反對 Gherkin 這一項**，理由是 Cucumber／SpecFlow 路線在商業上的失敗史。不過他本人銷售競品測試工具，且該文的失敗率宣稱沒有可查證的一手依據。（**low**：單一具利益關係的從業者主張，僅記錄存在對立意見，不作為論據。）

### 3. QA procedures——「不讀碼」的真正邊界在這裡

這一項最容易被忽略，卻是理解整套主張的關鍵——**人的閘門在這裡，而且是硬的**。

QA 在 `six-pack` 裡是一條完整的鏈，兩份角色檔講得很明白。`specifier.prompt` 定義 QA 套件的性質，「端到端」的定義嚴格得值得抄：

> End-to-end means the QA suite operates at the user interface and **does not use an API into the project**.

`QA.prompt` 負責把它變成可執行的東西：

> Convert the QA procedures written by the specifier into executable scripts […] Run the end-to-end QA suite through the user interface only; do not use an API into the project for end-to-end verification.

這條規則順帶解釋了一個先前看不懂的細節：`empire-2025` 的 `--headless=N`、`--seed=N`、`--log`、`--debug-dump` 不是隨手加的除錯旗標，而是**刻意設計的可測性 affordance**——`QA.prompt` 明文允許「新增命令列參數或 UI 指令來曝露難測的邏輯，只要那些 affordance 位於使用者介面、且不構成給 QA 的私有 API」。

**人的閘門在規格邊界，不在程式碼邊界。** `specifier.prompt` 的六階段工作流最後一步與交手規則寫死了這件事：

> 6. **Ask the user for approval to hand off to the coder.**
>
> Do not commit or notify coder **until the user explicitly approves the handoff**. […] When QA notifies you that the job is complete, merge the changes and **ask the user for the next feature**.

所以整條流水線的人工控制點有兩個：**開頭核准規格、結尾決定下一個功能**，中間全自動。這把先前只有二手轉述的說法（他 review Gherkin 與 QA procedures、不 review 單元測試）換成了一手依據——不是他在推特上怎麼講，而是他的系統實際上留了哪些洞給人。

**「不讀 AI 產的程式碼」這個標題是準確的，但推論成「他不看 agent 的產出」是錯的。** 他把人類注意力從**實作層**整個搬到**規格層**：Gherkin 他核准，QA 程序他核准，成品他親手玩。省下來的是讀函式本體的時間，不是驗證的時間。這與 [[AI-產碼加速下的-review-瓶頸]] 的四條路線是同一件事的兩種說法——他選了「約束前移」而非「改善 review」，而前移到的位置精確地說就是**規格**。

`QA.prompt` 裡還有一條規則直接對應 reward hacking 的防線：

> **If the QA suite contradicts the Gherkin or unit tests, stop and ask for clarification before changing behavior.**

這正是 ImpossibleBench 測出模型做不到的那件事（規格與測試矛盾時該停下而非作弊）。他把它寫成了角色規則——仍是 prompt 層，但至少矛盾被明確指定為「上報」而不是「自行解決」。

### 4. Quality metrics——CRAP 是複雜度上限偽裝成測試度量

他點名的 quality metric 就是 CRAP。公式由 Alberto Savoia 與 Bob Evans 於 2007 提出，我**直接從 `crap4clj/src/crap4clj/crap.cljc` 原始碼確認**他的實作是教科書版本：

```clojure
(defn crap-score [complexity coverage-pct]
  (let [cc (double complexity)
        uncov (- 1.0 (/ coverage-pct 100.0))]
    (+ (* cc cc uncov uncov uncov) cc)))
```

也就是 `CRAP(m) = CC² × (1 − 覆蓋率)³ + CC`。

⚠️ **`crap4clj` README 的範例輸出不可當參考**：那一列寫 `CC=12、Cov=45.0% → CRAP=130.2`，但用上面的公式算出來是 **≈36.0**。README 的示範數字是手寫的、與實作不一致（2026-08-09 實測）。要引用 CRAP 值請自己算或實跑。

**這個公式的性質比它的數值更重要。** 業界慣例門檻是 30，而指數的設計讓覆蓋率的效果三次方衰減：CC=10 的函式覆蓋 42% 就能壓到門檻以下，CC=25 要 80%，而 **CC 超過 30 時，無論覆蓋率多高都不可能低於門檻**——因為公式尾巴那個 `+ cc` 是保底項。

所以 CRAP 名義上是「測試品質度量」，實際運作起來是**一條硬性的複雜度上限**：你不能用寫測試的方式贖回一個過度複雜的函式。這與他推文裡「I constrain the hell out of function size and complexity」是同一件事的兩種表述。（**high**：公式從原始碼直接驗證；門檻 30 為工具生態的一致慣例，屬約定非實證。）

另外兩個度量工具的機制也值得記：`dry4clj` 不比對文字，而是把每個 top-level form 正規化成語法指紋集合，用 **Jaccard 相似度**（預設門檻 0.82）找結構重複——所以改名字、換述詞躲不掉。`dependency-checker` 則檢查元件邊界與依賴方向。

### 5. Mutation testing

原始碼層的 mutation 在 [[用測試約束-AI-產碼]] 已有完整證據盤點（Thoughtworks Radar Vol.34 唯一押注的一項、Meta ACH 的生產規模一手、以及待測碼本身可能有 bug 時 MSI 不適用的方法論缺口），此處只記他的增量。

他的 `clj-mutate` 用一個**差分機制**解成本問題：原始碼檔尾嵌一份 manifest，預設**只變異上次執行後改動過的 top-level form**，並支援 `--lines` 只重測上一輪的存活者。這與 Meta ACH「不做全量變異」的方向一致，但手段不同——ACH 靠「只產與特定關注議題相關的 fault」縮範圍，他靠「只測改動過的部分」縮範圍。前者需要人先指定關注議題，後者不需要，代價是不會回頭複驗舊碼。

一個小細節透露了紀律：`crap.cljc` 的檔頭是 `;; mutation-tested: 2026-03-04`——工具自己也跑過自己。

### 6. Test coverage——單獨當閘門，證據並不支持

這是七項裡**外部證據最不利**的一項，而 Uncle Bob 的用法恰好繞開了問題。

軟體工程領域關於覆蓋率的經典研究是 Inozemtseva 與 Holmes 的 [Coverage Is Not Strongly Correlated with Test Suite Effectiveness](https://dl.acm.org/doi/10.1145/2568225.2568271)（ICSE 2014）。他們為五個系統（最大 724,000 行）生成 **31,000 組測試套件**，結論是：

> ……a **low to moderate** correlation between coverage and effectiveness **when the number of test cases in the suite is controlled for**.

也就是說，覆蓋率與抓 bug 能力看似相關，很大一部分只是「測試寫得多」這個共同因子造成的假象；把測試數量控制住之後，相關性掉到低至中等。更強形式的覆蓋率（分支、路徑）也沒有帶來更多洞見。

**但這正是 CRAP 存在的理由**：覆蓋率單獨看沒有意義，放進複雜度的脈絡裡才有——同樣是 60% 覆蓋率，CC=3 的函式無所謂，CC=20 的函式是紅燈。他不用覆蓋率當閘門，他用覆蓋率當 CRAP 的一個輸入。這個用法沒有被上面那份研究否定。（**high**：ICSE 同儕審查、規模明確；本段引用的是論文摘要，完整 PDF 因編碼問題未能逐段核對。）

### 7. 「a plethora of others」——最有意思的一項在這裡

清單的省略號可以從他的 repo 補完，而其中最值得抄的是 [`deintroverter4clj`](https://github.com/unclebob/deintroverter4clj)。它做靜態分析，把每個測試分類成 **extroverted／likely-extroverted／introverted／questionable**：

> An **introverted test** passes but does not ground its assertions in SUT behavior — for example, asserting on literals, test-local data, or `clojure.core` helpers without calling production code.

**這是把 [[用測試約束-AI-產碼]] 的「同義反覆」失效模式機械化成可掃描的檢查。** 那頁原本給的偵測法是「手動翻一個運算子，測試仍綠即是」——需要人或需要跑 mutation。deintroverter 走靜態路徑：追斷言能不能溯源到 production code，不用執行、不用變異，因此便宜得多。對 AI 產測試場景這是很對口的一項，因為「斷言的是 mock 或字面值」正是最高頻的病徵。

⚠️ **但他自己的 README 明文反對把它當閘門**：

> Use it **manually**: point it at paths, read the report, and follow up in the editor. **It is not meant to be wired into CI gates**, release checks, or other automated verification or hardening pipelines. Verdicts are heuristic […] treat them as guidance for human judgment, **not pass/fail criteria**.

一個宣稱「不讀碼、只靠 gauntlet」的人，他最貼近 AI 測試病徵的工具卻要求人去讀報告、回編輯器跟進。這不是矛盾，是誠實——但它精準地標出了 gauntlet 的邊界在哪裡。

## 三之二、他不讀碼，但他派了 agent 去讀

推文的字面讀法是「程式碼沒有人讀」。`swarm-forge` 的 `adversaries` 分支推翻了這個讀法：那是一個只有兩個角色的編制，`coder` 與 `reviewer`，而 **reviewer 的職責就是讀碼**。

> Review **the code**, tests, commit history, handoff state, and relevant project behavior.
>
> Also review **low-level code quality: names, control flow, duplication, error handling, edge cases, and local readability**.
>
> Be **adversarial** but concrete: every recommendation must name the issue, the risk, and the expected change.

它的四個審查階段就是 Clean Architecture 的條目本身：**UI/Core 分離、依賴規則（高層模組不得依賴靠近 IO 的低層模組）、資訊隱藏與封裝、局部程式碼品質**。

**這一項是本頁最重要的修正**：Uncle Bob 沒有放棄 code review，他放棄的是**由人做 code review**。他把自己畢生主張的那套架構判準寫成 prompt，交給另一個 agent 去執行。所以正確的命題不是「測試可以取代 review」，而是「**review 的判準可以被寫下來、交給 agent 反覆執行**」——這是個弱得多、但也可信得多的主張。

三個設計細節值得單獨記：

- **寫入範圍受限**：「Do not modify production code, test code, build scripts, or project behavior. The only files you may change are review artifacts under `review/`。」reviewer 只能寫評審產物，改不了被評的東西。且 `swarmforge.conf` 給它獨立的 git worktree（`window reviewer codex reviewer`），所以**隔離是機械的**（worktree），檔案範圍限制才是 prompt 層的。
- **它驗證的是「閘門有沒有被跑」，不只是碼本身**：「Check that the coder used TDD where evidence is available」「Check that coder **ran language mutation testing or explicitly justified any omission**」。這是對 gauntlet 本身的後設查核——正好回應了第四節第 1 點指出的「驗證由 agent 自己回報」那個缺口，雖然查核者仍是 agent。
- **職責切乾淨**：「**Do not run language mutation testing**」——reviewer 自己不跑 mutation，只確認 coder 跑了。避免評審者變成執行者。

收斂條件也是明確的：不滿意就寫 `review/recommendations/NNN-recommendations.md`（序號遞增、每項須寫明問題、風險、預期變更）交還 coder；滿意才寫 `review/approval.md` 並停止。**評審歷程留成 git 裡的檔案**，這比對話紀錄可回溯得多。

## 四、這套方案撐不住的三個地方

### 1. 護欄大半在 prompt 層——但關鍵那一道是真的機械化了

@repojournal 在串裡問：

> If we cannot trust the outcome of what AI makes […] what gives us the confidence that it will stay within the guardrails of our constraints just because we asked it to?

大部分護欄確實只是請求。`engineering.prompt` 的 Guardrails 一節：

> Do not edit mutation testing or Gherkin acceptance mutation manifests by hand […]

`AGENTS.md` 的「Never modify an acceptance test `.txt` file without explicit permission」同樣如此。對照 [[用測試約束-AI-產碼]] 第五節引的 ImpossibleBench 量測——**GPT-5 在測試與規格矛盾時作弊率 76%，即使明確指示「發現測試有問題就停下」也未歸零**——這類指示的可靠度不該被高估。

**但有一道護欄他真的工程化了，而且正好是最該工程化的那一道。** `empire-2025` 唯一的 GitHub Actions workflow 叫 `acceptance-boundary-guard.yml`，在 `pull_request` 與 `push` 都跑，執行 `scripts/check-acceptance-boundary.sh`。腳本的核心是：

```bash
# Fails if a change set touches locked acceptance scenarios or parser sources.
blocked="$(printf '%s\n' "$changed" \
  | rg '^(acceptanceTests/|src/empire/acceptance/parser/)' \
  | rg -v '^acceptanceTests/README\.md$' \
  | rg -v '^acceptanceTests/transport\.txt$' \
  … )"
[[ -n "${blocked}" ]] && exit 1
```

**驗收規格與 parser 原始碼被鎖死，改到就紅。** 這正是 [[用測試約束-AI-產碼]] 第五節的第 4 層（保護護欄本身），而且做法比 CODEOWNERS 更直接。設計上還有一個細節值得抄：鎖是**預設鎖住、逐項解鎖**——排除清單裡那十來個 `transport-*.txt` 是當時正在規格化的檔案，做完就會收回鎖定。這對應該節列的最陰險手法（「不是 `--no-verify`，是弱化規則本身」）：agent 想讓失敗變通過，最省事的路徑就是改驗收規格，而這條路被機械擋住了。

修正後的分層盤點：

| 防繞過層 | 他有沒有 |
|---|---|
| 1. 明文寫進規則檔 | ✅ `engineering.prompt`、`AGENTS.md` |
| 2. 執行前 deny（PreToolUse） | ❌ 未見 |
| 3. CI 鏡像本地檢查 | ⚠️ **只鏡像了邊界檢查**——CI 不跑測試、mutation、CRAP、DRY，那些全在本地指令鏈 |
| 4. 保護護欄本身 | ✅ boundary guard，且預設鎖定 |

所以 @GeoffreyHuntley 那句「we need to engineer the constraint's」，他至少對**規格不可竄改**這一項做到了。真正的缺口在第 3 層：**驗證本身沒有權威副本**。所有測試、mutation、CRAP 都由 agent 在本地跑、由 agent 回報結果，沒有任何一個獨立於 agent 的地方重跑一次。agent 說「全綠」與「真的全綠」之間，在這套設定裡沒有機械上的區別。

### 2. empire-2025 的領域，是測試最有優勢的領域

「very high confidence」這個結論的外推範圍受限於它的樣本。`empire-2025` 是：單機遊戲、單一開發者、無使用者資料、無認證與權限、無外部系統整合、無並行使用者、無資料庫遷移、無合規要求，而且他刻意建了 `--seed=N`（固定亂數）與 `--headless=N`（無 UI 跑完整迴圈）讓行為可決定性重現。`AGENTS.md` 甚至要求「Mock the random number generator for tests with random/non-deterministic conditions」。

**這是一個「正確性幾乎可以被測試完整指定」的領域**——遊戲規則就是規格，而且規格是封閉的。相對地，[[專案測試流程]] 那類系統的核心風險（前端等 `total`、後端回 `total_amount` 這種跨邊界契約漂移、資料遷移、權限邊界、第三方 API 行為變更）在 Empire 裡根本不存在。

**這不否定他的方法，但否定直接外推。** 他證明的是「在規格封閉、行為可決定的領域，約束陣可以取代讀碼」；他沒有證明、也沒有宣稱在有真實使用者與資料的系統上成立。（**high**：專案性質從 README 與 AGENTS.md 直接可讀。）

### 3. 沒有外部量測

「very high confidence」是自評，全串與全部 repo 都沒有缺陷逃逸率、生產事故、或與對照組的比較。這與 [[用測試約束-AI-產碼]] 第六節的判準直接衝突——那頁說**唯一該用的成效判準是「有沒有抓到真 bug」**，而這裡能拿到的只有「閘門都綠了」。

值得公平地說：他是在推特上回一個問題，不是發表研究。但引用這套方案時得誠實標明它的證據等級是**單一資深從業者的實作示範**，而不是效果實證。

## 五、對 Vue + Laravel 專案的可搬性

他的工具全是 Clojure／Go／Java，本 vault 關心的 [[專案測試流程-前端-Vue]] 與 [[專案測試流程-後端-Laravel]] 一個都用不到。逐項對照現成程度：

| 閘門 | Vue／Laravel 的現成程度 |
|---|---|
| Unit tests | ✅ Vitest／PHPUnit，已在 [[專案測試流程]] 展開 |
| Mutation testing | ✅ Stryker（JS/TS）、Pest `--mutate`／Infection（PHP），既有頁已記邊界 |
| Test coverage | ✅ 兩端內建；但依第 6 項，別單獨當閘門 |
| **CRAP 度量** | ⚠️ **無現成整合**。兩端都能取得 CC 與行覆蓋率（PHPMD／`phpunit --coverage-clover`；ESLint complexity／Vitest coverage），公式只有一行，**自己算是划算的**——這是本頁最可直接落地的一項 |
| DRY 偵測 | ⚠️ 有 `jscpd`（跨語言 token 級）但非 Jaccard 語法指紋；PHP 有 PHPMD 的 CPD |
| 依賴方向檢查 | ✅ 前端有 dependency-cruiser／Madge（[[AI-生成流程圖與架構圖]] 已收）；PHP 有 Deptrac |
| **Introverted test 偵測** | ❌ **找不到對應工具**。概念可搬（斷言是否溯源到 production code），實作得自己寫 |
| Gherkin + acceptance mutation | ❌ Gherkin 有 Behat（PHP）／Cucumber.js，但 **example 值變異這一層沒有現成品** |
| QA procedures | ⚠️ 人的流程，與語言無關，可直接抄 |
| **鎖住規格檔的 CI guard** | ✅ **與語言完全無關、當天可做**：一個 workflow 跑 `git diff --name-only` 比對受保護路徑即可，見第四節第 1 點的腳本。這是本頁性價比最高的一項 |
| **對抗式 reviewer agent** | ✅ 概念可直接搬：獨立 worktree、只能寫 `review/`、審查判準寫成固定清單、產出序號遞增的 recommendations 檔 |

**建議的採用順序**（沿用 [[用測試約束-AI-產碼]] 第六節的「先量基線」原則）：**鎖住規格檔的 CI guard 先做**（成本一小時、與語言無關、擋掉最陰險的那類繞過）→ CRAP 一行公式算一次找出最該補測試的函式 → 已排定的 mutation 基線 → 若那時仍覺得測試在說謊，再考慮手寫 introverted test 偵測。Gherkin 那一整套除非專案規模到了他說的「larger projects」，否則按他自己的話就是 overloading。

## 證據強度總表

| 主張 | 強度 |
|---|---|
| 他為每項約束都寫了工具，Clojure／Go／Java 各一套 | **high**：2026-08-09 經 GitHub API 逐一驗證 repo 存在、可讀 README 與原始碼 |
| `crap4clj` 實作的是教科書 CRAP 公式 `CC²×(1−cov)³+CC` | **high**：直接讀 `src/crap4clj/crap.cljc` 原始碼 |
| CRAP 實質上是複雜度上限（CC>30 無法靠測試贖回） | **high**：公式的數學性質，可自行驗算 |
| 「crap evaluation」指 CRAP 度量而非自嘲 | **high**：前串原文＋他自有三個 crap4* repo |
| 閘門數隨專案規模調整，非固定清單 | **high**：他本人推文＋`swarm-forge` 的 two/four/six-pack 分支設計 |
| gherkin mutation ＝變異 Gherkin example 值、非變異原始碼 | **high**：`Acceptance-Pipeline-Specification` README 明文定義 |
| 覆蓋率控制測試數量後只與有效性低至中度相關 | **high**：ICSE 2014 同儕審查、31,000 組測試套件；本頁引用的是摘要，未逐段核對全文 |
| 驗收規格與 parser 被 CI 機械鎖定，agent 改不了 | **high**：`acceptance-boundary-guard.yml` 與 `scripts/check-acceptance-boundary.sh` 全文可讀，`pull_request` 與 `push` 皆觸發 |
| 驗證本身（測試／mutation／CRAP）沒有獨立於 agent 的權威副本 | **medium-high**：`empire-2025` 唯一的 workflow 只做邊界檢查，其餘為本地指令鏈；無法排除未公開的本地機制 |
| ~~護欄僅存在於 prompt 層，無機械強制~~ | **已於 2026-08-09 第二輪查證推翻**：初判漏看 `.github/workflows/`，實際上第 4 層（保護護欄本身）已機械化。原判定不成立，保留此列作為紀錄 |
| 他派了一個對抗式 reviewer agent 去讀碼，判準是 Clean Architecture 四項 | **high**：`swarm-forge` `adversaries` 分支 `reviewer.prompt` 全文可讀 |
| gherkin mutator 的變異規則為型別推斷式值擾動、不含領域語意 | **high**：`mutator-spec.md` 直讀，含規則順序與範例 |
| `--level soft` 可能沿用實作已變更之 scenario 的舊結論 | **medium-high**：三檔定義與 hardender 用法皆直讀，此推論依定義導出、未實測 |
| empire-2025 屬規格封閉、行為可決定的領域 | **high**：README 與 AGENTS.md 直接可讀 |
| 人的閘門在規格邊界（核准 Gherkin 與 QA 程序），不在程式碼邊界 | **high**：`specifier.prompt` 明文「Ask the user for approval to hand off to the coder」「Do not commit or notify coder until the user explicitly approves」。**2026-08-09 第二輪從 low-medium 的二手轉述升為一手**——依據不再是他推特上怎麼說，而是他的系統留了哪些控制點給人 |
| 「他把 TDD 從規則檔搬成角色定義是有意識回應 TDD 指示無效」 | **low**：本頁推論，非他本人陳述；角色檔只支持「coder 明寫 TDD 且要求測試須能因合理錯誤實作而失敗」這個事實 |
| 這套方案能給出 very high confidence | **不可引用為效果證據**：自評，無缺陷逃逸率、無對照組、無外部量測 |

**勿引用**：

- **「AI 產碼的問題比人寫的多 1.7 倍、安全漏洞多 2.7 倍」**——追到源頭是 **CodeRabbit 的自家報告**（2025-12，n=470 個 GitHub PR，320 個標為 AI 共同撰寫），而**問題的分類用的是 CodeRabbit 自己的 review taxonomy**。賣 AI code review 的廠商，用自家工具的判準，量測「AI 產碼問題比較多」——與本 vault 既有的「各家 AI 測試／review 工具自評抓 bug 率」屬同一類利益衝突。**不得作為論據使用。**
- **`crap4clj` README 範例輸出的 `CRAP=130.2`**——與該 repo 自己的公式實作不符（正確值 ≈36.0），是手寫的示範數字。
- **「99+% 的團隊導入 Gherkin E2E 測試失敗」「SmartBear 與 Tricentis 因此虧損放棄」**——出自銷售競品測試工具的從業者部落格，無可查證一手依據。可記錄為存在對立意見，不可當事實。

## 關聯

- [[用測試約束-AI-產碼]] — 本頁是該頁的**人物案例層**：該頁盤點「哪些手段有多少證據」，本頁盤點「一個把這條路線推到極致的人實際搭了什麼」。兩處實質互補：本頁第 2 項的 **gherkin acceptance mutation** 補上該頁沒有的驗收層假測試偵測，第 7 項的 **introverted test 靜態偵測**則把該頁「同義反覆」失效模式從人工偵測法升級成可掃描的檢查。反過來，該頁第五節的五層防繞過正是本頁第四節判定這套方案漏洞所用的尺。
- [[AI-產碼加速下的-review-瓶頸]] — 本頁是該頁四條路線中「**約束前移**」的極端案例：Uncle Bob 不是改善 review，而是整條廢掉 review 換成前移的閘門。該頁引 DORA 的「投資測試自動化的 ROI 可能高於優化人工 review」，本頁是那句話被推到底之後的樣子。
- [[專案測試流程]] — 一個意外的收斂：`engineering.prompt` 要求「Separate testable modules from environmentally unsuitable modules that open GUIs […] Maximize testable code and minimize the unsuitable boundary」，與該頁「第一個動作不是寫測試而是把判斷抽離框架」是同一條紀律，只是他講的是 GUI、該頁講的是 Vue 元件與 Laravel Controller。第五節的可搬性表則是本頁對該頁的具體回饋。
- [[AI-自主工作流的實證檢驗]] — 本頁第四節第 1 點的證據基礎（ImpossibleBench 的 76% 作弊率）出自該頁；該頁「驗證迴路必要但不充分，因為測試本身可被 agent 篡改」正是本頁判定 prompt 層護欄不足的依據。
- [[不讀碼時該看哪些圖]] — 同一處境（不讀 agent 產碼）的另一組答案，且與本頁在**機制上同形**：本頁最高性價比的結論是把驗收規格檔用 CI guard 機械鎖死，該頁則是把架構邊界寫成 CI 上會 fail 的依賴規則——都不是靠人記得檢查，而是把判準外移成機械閘門。差別在射程：本頁的閘門管「行為對不對」，該頁的管「東西有沒有放對地方」，兩者都不可替代對方。
- [[Agent-工作流-Pattern-藍本庫]] — `swarm-forge` 的 two/four/six-pack 是該頁「複雜度為最後手段、單 agent 優先」選用 gate 的一個實例：同一個人針對任務規模提供三種編制，而不是永遠派六個 agent。
