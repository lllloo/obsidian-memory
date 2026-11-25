---
title: Nikolay Petrov 量出 skill 裡模型已知的內容
description: 把 SKILL.md 拆成原子問答、有無 skill 對照量出模型已知內容；附 Dokimi 回查、數字強度與照做步驟
created: 2026-11-19
updated: 2026-11-25
source: https://ai.engineer/code/2026/talks/online-skills-knowledge
published: 2026-11-11
parent: "[[wiki/01.index]]"
tags:
  - skill
  - evaluation
  - context-engineering
  - coding-agent
---

# Nikolay Petrov 量出 skill 裡模型已知的內容

原料：[[AI-Engineer-Petrov-Skill-Already-Knows]]（官方閱讀頁＋官方機器逐字稿，Day 1 直播影片 `ZZ19zhYnDKY` 的 7:00:53–7:14:53，約 14 分鐘，Online Track 預錄）。逐字稿把工具名 Dokimi 辨識成「the document」，投影片內容是另外從影片截圖讀出的（14 張投影片看了 13 張）。回查以 `gh` 直讀 [intel/dokimi](https://github.com/intel/dokimi)、[mattpocock/skills issue #1384](https://github.com/mattpocock/skills/issues/1384) 與被引用的 skill 原文，2026-11-19 查。

**一句話**：「模型已經知道」不等於「這行可以刪」。把 skill 拆成一題一答的原子，分別在載入與不載入 skill 時問模型，就知道哪些句子在教新東西、哪些是重複、哪些反而害模型答錯。這只是找出值得實驗的地方，刪改後還是要重跑真實任務評測，分數不掉才算數。

## 講者與立場

Nikolay Petrov，Intel（GitHub `napetrov`，個人頁標 `@intel`）。整場的工具是他主導的開源專案 [Dokimi](https://github.com/intel/dokimi)（Apache-2.0，Intel 官方 org 下；changelog 檔名帶 `napetrov`），最後一張投影片就是 Dokimi 功能清單。**屬推自家開源工具**，但工具免費、方法本身可以不靠它手動做；他的實驗對象是 Anthropic、obra、Matt Pocock 三個熱門 skill repo，不是 Intel 自家產品。標題的 70% 其實來自 Dokimi 文件裡針對 Intel 自家 skills 的研究（見回查節）。

## 演講脈絡（依投影片順序）

### 1. Skill 有兩種：教知識的、規範流程的（投影片 3）

- **教知識**（teach）：模型猜不到的事實，例如你的格式、命名、門檻、專案規則。例子是 `grilling` skill 規定的確切一輪問答格式。
- **規範流程**（steer）：模型本來就懂、只是要它照順序做，例如「照循環走、不要跳步」。例子是 obra 的 `test-driven-development`，投影片標「96% 已被現行模型知道」。
- 本場只量**知識**。對流程型 skill，「模型已知」是正常的、沒問題：**知道規則不等於照規則做**。

### 2. 先用任務評測證明 skill 有用（投影片 4）

Skill 只是文字，要靠 eval 證明它改善了工作。他的例子：

- 任務：「Grill me on moving our CI to self-hosted runners」，先不載入 skill 跑一次，再載入跑一次。
- 檢查項就是 skill 承諾的行為，寫成 pass/fail：問題有編號嗎？每題有建議答案嗎？有等我回答嗎？檢查項可以自己寫，也可以讓模型從 skill 草擬、人再審。
- 5 個這類任務：不載入 3/5、載入 5/5，多解 2 題；另外看 trace 裡的 token 與時間。
- 評分方式三種：跑測試（pass/fail）、judge model 依 rubric 判、看 trace（呼叫了什麼工具、花多少 token 與時間）。

這只是示意例，不是正式實驗。

### 3. Skill 有用之後，怎麼改得更好（投影片 5）

四個問題：**Cut**（模型已知什麼）、**Keep**（什麼必須逐字保留）、**Fix**（什麼讓它混淆）、**Re-check**（新模型出來後它現在知道什麼）。

暴力法是一次刪一行、整套 eval 重跑：30 行就要 30 輪。而且行與行會互相影響：兩行講同一件事時，單刪哪一行都看不出變化。所以需要比整份文件小、又比任意換行有意義的分析單位。

### 4. 拆成原子：一個可檢查的事實（投影片 6）

概念借自 [FActScore](https://arxiv.org/abs/2305.14251)（Min et al., EMNLP 2023）：原論文是把模型的**輸出**拆成原子事實逐一查證，他反過來把 **skill** 拆開。以 `grilling/SKILL.md` 第 8 行為例，一句話拆成四個原子：

| 類型 | 問題 | 預期答案 |
|---|---|---|
| proposition（概念） | 決策樹以什麼單位進行？ | 以「輪」 |
| proposition | 什麼是 frontier？ | 前置條件都已決定的那些決策 |
| contract（確切規則） | 每輪問什麼、怎麼問？ | 全部一起問、編號、每題附建議 |
| contract | 下一輪之前要做什麼？ | 等使用者回答 |

**proposition** 是想法或建議；**contract** 是確切規則：格式、名稱、數字或順序。每個 skill 約取 25–30 個原子；mattpocock 的 repo 共 661 個原子，其中 367 個 proposition、245 個 contract。

### 5. 每個原子問兩次，交給評審（投影片 7）

- 不載入 skill：只給問題。載入 skill：`SKILL.md` + 問題。
- 評審看問題、答案鍵與一份回答，判定：完整、缺細節、部分正確、錯。可用一個模型或一組評審。
- **公平出題**：問題本身不能洩漏答案；不給工具，因為這裡測的是記憶不是搜尋，真實執行交給任務 eval。（逐字稿另說視情況也可以給 web access 之類的工具，測實務表現。）
- **公平評分**：每次呼叫重複跑以量測雜訊；評審最好用不同模型家族。

### 6. 四種結果（投影片 8）

| | 載入後答對 | 載入後答錯 |
|---|---|---|
| **不載入就答對** | 已知 → 可刪的候選 | **有害 → 先修** |
| **不載入答錯** | 新知 → 逐字保留 | 仍然缺 → 改寫 |

「仍然缺」是 skill 裡寫了，模型讀了還是答錯，代表寫法沒傳達到。

### 7. 有害條目很少，而且來自兩行互相衝突（投影片 9）

- 計數（Sonnet 5.5、嚴格評分）：anthropics 1/398、obra 0/478、mattpocock 0/661。他說較小、較不熱門的 skill 在他們的實驗裡有較多這類問題，但沒給數字。
- 唯一案例是 [anthropics/skills 的 `internal-comms`](https://github.com/anthropics/skills/blob/main/skills/internal-comms/SKILL.md)：第 26 行說「其他不符合上述的一律用 `examples/general-comms.md`」，第 29 行說「類型不符合任何既有 guideline 時，請使用者澄清」。問「請求不符合任何 guideline 怎麼辦？」，不載入時答「請使用者澄清」（正確），載入後答「檔案講了兩件事，無法判斷」。
- 修法：只改一處，讓第 29 行成為唯一的 fallback，刪掉第 26 行的 catch-all。

### 8. 把結果標回每一行（投影片 10）

每個原子都對應到原文的行或句子，所以可以把 `SKILL.md` 上色：綠色是新知（`grilling` 的輪次格式、編號、「回 yes 就是接受建議」的措辭），灰色是已知（一般的訪談建議）。他說示範是以行為單位，實際以原子為單位，同一行可能有不同顏色。

投影片同時列出成本與精度：

- **成本**：29 個 skill 花 **14 美元**、5,360 次呼叫；Sonnet 5.5 抽原子兼當評審，Haiku 5.5 與 Sonnet 5.5 作答。
- **精度**：單一 skill 25 個原子時，「60% 已知」的 95% 區間是 40–80%；整個 repo 661 個原子時約 ±4 個百分點。

### 9. 寬鬆與嚴格評分差很多（投影片 11）

- **寬鬆**：主旨對就算對，缺一個細節也算。**嚴格**：每個條件與細節都齊全才算。
- 例子是 `grilling` 第 28 行，答案鍵是「決策歸使用者：逐一交給他們，**並等待**」。模型答「使用者做決定，助理為每題提建議，但由使用者決定」，寬鬆判對，但沒有「等待」，嚴格判錯。少了「等待」這個行為契約就會失敗，即使評審認得出大原則。
- 不載入 skill 時的已知比例：Haiku 5.5 從 45%（寬鬆）掉到 18%（嚴格）；Opus 5.5 從 70% 掉到 22%（投影片註腳：Opus 數字出自「Dokimi paper」，Haiku 數字出自 mattpocock 研究）。contract 類原子裡，對兩個模型都是新知的比例從 50% 升到 77%。
- 他的解讀：較大的模型通常懂概念，但確切的 key、值、條件與步驟仍然要靠 skill 提供。**除這張投影片外，其餘數字都是寬鬆評分**。

### 10. 不同 repo 與模型差很多（投影片 12）

不載入 skill、寬鬆評分下答對的比例（60 個 skill、1,537 個原子，評審 Sonnet 5.5，**Sonnet 自評自己的答案**）：

| repo | Sonnet 5.5 | Haiku 5.5 |
|---|---|---|
| obra（superpowers） | 71% | 65% |
| anthropics | 64% | 54% |
| mattpocock | 53% | 45% |

小模型普遍知道得少；他預期隨模型進步已知比例會上升。各 skill 差很多，這不是壞事：流程型 skill 本來就會含很多已知內容；寫給小模型的知識型 skill，可能需要大模型自己就懂的解釋。**沒有一個脫離模型與任務的「最小 skill」**，理想上要在更多模型上跑。

### 11. 新穎度只是一個訊號，最後還是要跑 eval（投影片 13）

測驗看得到的：問 Haiku 不載入 skill「下一輪之前要做什麼？」，它答「等回答」，判為已知。**測驗看不到的**：真實 session 裡沒有 skill 時，agent 會不會真的停下來等，還是一次問完就往下做。

流程：已知的行列為刪除候選 → 拿掉它們在同一批任務上跑 eval → 分數不變就刪；變差就保留，並註明為什麼要保留。目的是用證據引導要做哪些實驗，取代暴力嘗試與猜測。

### 12. Dokimi（投影片 14）

把 `SKILL.md` 當程式碼測試的工具：Novelty map、有無 skill 的 A/B eval（品質、token、時間）、context impact、routing（agent 會不會選到你的 skill）、成本預估、縮短、Evolve（用 GEPA 改寫 skill，由封存的 eval set 把關）、merge or split、沙箱執行的 runtime security、judge panel。結尾一句：「去寫更好的 skill。」

## 回查結果

| 演講說法 | 查證結果 | 依據 |
|---|---|---|
| 原子概念來自 FActScore | **成立**：Min 等人 2023，把長文生成拆成原子事實，計算有可靠知識來源支持的比例；Petrov 把方向反過來用在 skill 上 | [arXiv 2305.14251](https://arxiv.org/abs/2305.14251) |
| Dokimi 是開源框架 | **成立**：`intel/dokimi`，2026-10 建立、Apache-2.0、持續有提交；README 說每張功能卡都會寫明「現在能做什麼、在哪裡停」，部分功能是開放中的 PR 或研究方向。**投影片 14 的功能未逐項確認是否已發布** | [README](https://github.com/intel/dokimi) |
| 29 個 skill 花 14 美元 | **成立**：mattpocock 報告寫 metered spend **$13.96 for 29 skills**，triage 等級、每 skill 25 個原子、跳過 paraphrase 與 reversal | [issue #1384](https://github.com/mattpocock/skills/issues/1384) |
| Haiku 45% → 18%、Sonnet 53% | **成立**：同一份報告寫 Haiku 寬鬆 0.45、嚴格 0.18，Sonnet 0.53；245 個 contract 中 122 個（50%）對兩個模型都是新知 | 同上 |
| mattpocock 0/661 有害 | **成立**：報告說唯一候選就是 `grilling` 第 28 行，只在嚴格評分出現，判定為評審雜訊而排除 | 同上 |
| `grilling` 第 8、28 行原文 | **成立**：現行 `SKILL.md` 第 8 行是「Work the tree in rounds…」，第 28 行結尾是「The _decisions_ are the user's: put each to them and wait.」 | [grilling/SKILL.md](https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md) |
| `internal-comms` 第 26、29 行衝突 | **成立，至今未修**：兩行原文與投影片一致，該檔最後一次修改早於演講 | [internal-comms/SKILL.md](https://github.com/anthropics/skills/blob/main/skills/internal-comms/SKILL.md) |
| Opus 5.5 已知 70% → 22% | **模型標籤對不上**：Dokimi 文件的對應數字是 `claude-opus-5` 寬鬆「already knew」0.700、嚴格 0.216，研究對象是 Intel 自家 `intel/skills` 的 33 個 skill，不是三個熱門 repo。文件裡沒找到 Opus 5.5 的同組數字 | [skill-novelty-evidence.md §3](https://github.com/intel/dokimi/blob/main/dokimi/docs/skill-novelty-evidence.md) |
| 評審最好用不同家族 | **他自己的研究沒做到**：mattpocock 研究與投影片 12 都由 Sonnet 5.5 評 Sonnet 5.5 的答案；報告自己承認這會灌高 Sonnet 的已知比例 | issue #1384 第 6 節 |

## Dokimi 文件裡、演講沒講的限制

以下出自 Dokimi 自家文件（同一作者、單一研究、LLM 評審；文件說人工標註的 gold subset **尚未填完**，所以所有絕對水準都建立在 LLM 評審上）。

- **兩個評審意見不一致**：2,143 份雙評回答，在六級判定上完全一致只有 66.4%，收成「大致正確／錯」二分時 85.2%。文件結論：相信正負號與排名，不要相信小數點後第二位；**`added` 差異小於 0.15 的不要引用**。
- **新穎度能比同一 skill 下的模型，不能比不同 skill**：嚴格 `added` 在同一 skill 內排模型時與任務分數 ρ 為 0.625（重跑後 +0.875）；拿來排不同 skill 時 ρ 為 −0.446。所以「A skill 新知比 B 多，A 比較好」**不成立**。寬鬆評分的 `added` 與任務結果幾乎無關（同 skill 內 0.000），**做決策用嚴格評分**。
- **「段落多餘」不能當結論**：沒有任何 skill 在嚴格評分下所有原子結果一致；以標題為單位時一致率只有 0.39–0.44，約四分之一原子與所屬段落的多數結果不同。
- **知識分數看不到安全條款被刪**：一個只保留 21% token 的縮短版，知識保留分數 0.916，保護分數只有 0.158。否定句、版本限制、順序限制這類句子單看資訊量低，貪婪選取會先丟掉它們，但它們防的是特定失敗。
- **縮短的實測結果**：強模型上沒有縮短版比完整版掉超過 0.08；超過 0.08 的損失都發生在最小的模型（−0.10、−0.15、−0.19）。有的 skill 幾乎每段都受保護（`xpu-system-setup` 最多只能縮到 94%），問題在內容不在長度。
- **寫法本身會害模型**：`performance-patterns` 的 `SKILL.md` 用漸進揭露的語氣（「我會先去查某份清單」），grok-4.6 只載入 `SKILL.md` 時 8 題有 6 題延後作答，分數 0.047，不載入 skill 反而 0.537。
- **無關內容會傷小模型**：用等長的不相干文字當 placebo，Haiku 4.5 從 0.340 掉到 0.130、grok 從 0.352 掉到 0.104；Opus 5 與 gpt-5.6-luna 則幾乎不受影響。
- **強模型最容易被錯誤前提帶走**：反轉題（故意埋相反說法）的抵抗率，強模型 0.787–0.811 反而低於最弱的 0.890。skill 裡若有過時或寫反的句子，最受害的是最好的模型。skill 內植入錯值時，模型照說的比例是 0.846–0.942，只有 3% 會指出。
- **Routing 常是更大的問題**：33 個 skill 裡有 6 個 routing 正確率低於 0.50，最低 0.146。描述沒選中，內容再好也沒用；所以 Dokimi 的 walkthrough 把 routing 檢查排在第一步。
- **數字會過期**：文件說研究用的兩個模型已無法呼叫，新穎度數字只有附上模型名與日期才能引用。

另有一處說法不一致：Dokimi 的四種結果表把「已知」寫成「delete it, for this model tier」，但 README 與演講都說「已知不代表可以安全刪除」。**以後者為準**，刪之前一定要跑任務 eval。

## 搬到個人 Claude Code／Codex 工作流程

### 能照做的：手動版（不必裝工具）

適合自己寫、常用的知識型 skill 或 `CLAUDE.md` 段落。

1. **先分類**：這份 skill 是在教知識，還是在規範流程？流程型（TDD、review 步驟、何時停下來問人）就跳過下面的刪減，只做第 6 步的行為 eval，因為「知道」不等於「做到」。
2. **先查會不會被選到**：用 5–10 句使用者實際會說的話（不要照 skill 的標題寫），看 agent 會不會選到這個 skill。選不到就先改 `description`，內容先不要動。
3. **列原子**：挑 15–25 個可檢查的點寫成問答，優先挑 contract：確切格式、檔名、門檻、順序、否定句（「不要…」）、版本或條件限制。問題不能帶出答案。
4. **在乾淨環境問兩次**：一次不載入 skill（直接呼叫 API，或在沒裝這個 skill 的目錄開新 session），一次把 `SKILL.md` 貼進 context。用另一家模型當評審，或自己判；**一律用嚴格標準**，缺一個條件就算錯。
5. **處理順序**：(a) 載入後反而答錯的先修，通常是兩行互相衝突，留一條或寫清楚適用條件；(b) 兩邊都答錯的改寫或移到更顯眼的位置；(c) 兩邊都答對的才列為刪除候選；(d) 只有載入才答對的逐字保留。否定句、順序與版本限制即使看起來已知也先保留。
6. **刪完跑任務 eval**：拿 3–5 個真實任務，寫成 pass/fail 檢查項（例如「每題有編號」「有等我回答才繼續」），新舊版本**各跑 3 次**看雜訊。分數持平才刪；變差就放回，並在旁邊註明為什麼要保留。
7. **換模型時重測**：同一 skill 在 Haiku 與 Sonnet 間已知比例差 10 個百分點以上的情況很常見（mattpocock 29 個 skill 中有 15 個），換主力模型或小模型 subagent 時要重量。

### 能照做的：用 Dokimi

依 README 與 walkthrough（**本次未實跑**；README 用 `dokimi ...`，部分文件用 `python cli.py ...`，以安裝後的 CLI 說明為準）：

1. 免費靜態檢查：`dokimi catalog check --root <skills 目錄> --kind skills`。
2. 先估價不花錢：`skill novelty analyze ... --estimate-only`；實跑時每一步都加 `--max-usd` 上限。
3. 從 `triage` 等級開始（25 個原子）。文件的實測：一份 19k token 的 skill，triage 約 103 次呼叫、約 1.8 美元；`study` 等級約 1,901 次呼叫、約 14.5 美元。估價會低估，文件說保留樣本最多少算 33%。
4. 需要 API 金鑰或已登入的 harness；執行型任務還要 container 環境。

### 不建議照做的

- **看到「模型已知 70%」就把 skill 砍掉七成**：70% 是寬鬆評分、特定模型、特定 skill 集合；嚴格評分只剩約兩成。
- **對 25 個原子的單一 skill 下結論**：區間約 ±20 個百分點，只能看出很大的差距。
- **拿新穎度比較不同 skill 好壞**：Dokimi 自己的資料顯示這樣排序是錯的。
- **用新穎度判斷流程型 skill 能不能刪**：它只量知識，看不到 agent 會不會照做。

本 vault 的 `vault-lint` 屬流程型 skill，第 1 步就會被排除；若要套用任何刪改，依 AGENTS.md 屬於改 skill，要先問使用者。

## 證據強度與限制

- **所有數字都是自報**，出自講者自己的工具與實驗，沒有獨立重現；作者自己的 gold set 人工標註尚未完成。
- **評審有偏差**：mattpocock 與三 repo 的比較由 Sonnet 評 Sonnet，與他自己的建議相違；Sonnet 與 Haiku 的差距有一部分是自評造成的。
- **樣本**：三 repo 比較 60 個 skill、1,537 個原子；mattpocock 單一 repo 661 個原子；Opus 數字的來源是 Intel 自家 33 個 skill。投影片 10 的「29 個 skill」與投影片 12 的「60 個 skill」是不同批實驗。
- **只量 `SKILL.md`**：mattpocock 報告明說沒有納入 `references/` 等資源；有 3 個 skill 因預算沒跑。
- **知識 ≠ 行為**：講者與報告都明講。
- **開場 3/5 → 5/5 是示意例**，不是實驗結果。
- **有害條目稀少**的結論只來自三個熱門 repo；「小眾 skill 有害較多」沒有給數字。

## 勿引用

- **「SKILL.md 有 70% 是模型已知的」當通則**：70% 是 Dokimi 研究中 `claude-opus-5`、寬鬆評分、Intel 自家 33 個 skill 的結果。三個熱門 repo 在寬鬆評分下是 45–71%；嚴格評分只查到 mattpocock 的 Haiku 18%，Intel 自家 skill 集上 `claude-opus-5` 為 22%。引用時要附模型、評分方式與 skill 集合。
- **「Opus 5.5 已知 70% → 22%」**：投影片標 Opus 5.5，但它引用的 Dokimi 文件寫的是 `claude-opus-5`，沒找到 Opus 5.5 的同組數字。要引用請寫 `claude-opus-5`（0.700 → 0.216），並註明來源是 Dokimi 文件。
- **「已知內容可以刪」**：Dokimi 四種結果表的「delete it」字樣與 README、演講本身都矛盾，以「刪前要跑 eval」為準。

## 與其他頁的張力與互補

- **與 [[Claude-5-世代的指示精簡原則]] 互補也有張力**：該頁整理「CLAUDE.md 只寫 Claude 猜不到的事」，Petrov 提供量測「猜不猜得到」的方法。張力在於：該頁傾向刪掉模型已知的叮嚀，Petrov 的嚴格評分顯示模型多半只懂大概，確切條件仍要寫。兩頁都同意改完要用自己的任務驗收。
- **支持 [[Lauren-Tan-把糾正寫進程式庫]] 的排序**：Petrov 承認測驗看不到 agent 會不會真的「停下來等」，等於承認散文層管不住行為。Lauren Tan 把散文放在信任金字塔下層，主張重要規則改成 lint、型別或驗證。
- **與 [[Roey-Ben-Chaim-讀-skill-看不出它會做什麼]] 互補**：兩人都說光讀 `SKILL.md` 判斷不了效果。Ben Chaim 談安全，要在沙箱實跑看行程與網路；Petrov 談有效性，要有無 skill 對照加任務 eval。Dokimi 也列了沙箱 runtime security，但本次未確認是否已發布。
- **[[Superpowers]] 的實測**：obra 的 skill 是三個 repo 中已知比例最高的（Sonnet 71%），其中 `test-driven-development` 達 96%。這符合它以流程型 skill 為主的定位，不代表可以精簡。
- **[[Matt-Pocock-的-PR-瓶頸解法]] 的 skill 被量過**：mattpocock/skills 已知比例最低（Haiku 45%），報告建議保留 122 個兩個模型都不知道的 contract，並附一組 `grilling` 的行為 eval 範例；該 issue 截至 2026-11-19 仍開著、沒有回覆。
- 這場演講在 [[AI-Engineer-2026-演講精華-AI-工作流程]] 的「skill 設計」主題中被摘要過；本頁是完整版，並修正了該處「任務評測只有 5 題」的說法：5 題是示意例，正式量測是原子問答。
