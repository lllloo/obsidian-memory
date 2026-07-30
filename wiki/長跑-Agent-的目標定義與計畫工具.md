---
title: 長跑 Agent 的目標定義與計畫工具
description: 讓自主迭代 agent 持續推進而不走偏的目標檔機制（分層、驗收判準、停止條件、防漂移措辭）與 SDD 工具生態的採用度實據
created: 2026-07-30
updated: 2026-07-30
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - coding-agent
  - agent-framework
---

# 長跑 Agent 的目標定義與計畫工具

「怎麼給長跑／自主迭代型 coding agent 定目標，讓它能持續推進又不走歪」的兩個層面：**機制層**（目標檔怎麼寫，有哪些可直接抄的措辭）與**工具層**（現成能裝的是哪些、誰真的被採用）。

與 [[AI-自主工作流的實證檢驗]] 的分工：該頁記錄「這些做法有多少效果證據」（答案是幾乎沒有，反面證據紮實得多），本頁記錄「**具體怎麼寫**」與「**現在該裝哪個**」。該頁的核心警告在本頁全部成立，採用前請先讀。

本頁基礎來自 deep-research（2026-07-30，5 路搜尋、25 來源、125 條抽出主張、25 條進 3 票對抗式查證，14 條確認／11 條否決），工具採用度另以 `gh` 直查 GitHub API 核實。

## 最重要的前提：沒有一條是效果實證

14 條確認主張**沒有任何一條**是「這個機制有效」。全部是對一手 artifact（範本檔、prompt 檔、shell／TypeScript 原始碼、官方文件）內容的**描述性**核實——即「某工具規定了什麼」，不是「這樣規定能減少 drift」。引用時一律標「工具慣例／單一作者或單一廠商設計主張」。

樣本另有偏斜：憲法檔與 Complexity Tracking 兩個機制**只有 spec-kit 一個來源**，不足以支撐跨生態通則。

## 機制層：可直接抄的措辭

### 目標要分層落盤（3-0，廠商設計主張）

spec-kit 與 Kiro 是彼此獨立的生態，結構同構：

| 層 | 內容 | 前例 |
|---|---|---|
| 憲法／原則 | 不可協商的長期規則 | spec-kit `.specify/memory/constitution.md` |
| 需求／規格 | what ＋驗收判準（**權威定義在此層**） | `spec.md`／Kiro `requirements.md`、`bugfix.md` |
| 設計／計畫 | how，且「grounded by the constitution」 | `plan.md`／`design.md` |
| 任務 | 離散可追蹤項，獨立者標 `[P]` 可平行 | `tasks.md` |

**抄用注意**：寫成「三個固定分層」而非固定檔名——spec-kit 現行有 7 個 core command（`constitution`／`specify`／`clarify`／`plan`／`tasks`／`analyze`／`implement` 之外還有 `checklist`、`converge`、`taskstoissues`），Kiro 第一層檔名隨模式變。

⚠️ **這一層有生態內反證**：spec-kit 社群把三份 artifact 描述為**會互相分歧的 peers**（artifact drift），提議 `/speckit.reconcile`（issue #1063）與 constitution-aware 的最終 gate（#1323）。對長跑 agent 而言，**多一層文件就是多一個漂移源**。

### 驗收判準用結構化記法 ＋ 機器可掃描的未決標記（3-0）

Kiro 的 EARS 記法，自述目的是「Unambiguous and testable / Easy to translate into test cases」：

```
WHEN [condition] THE SYSTEM SHALL [behavior]
```

spec-kit 則用固定字串逼出未知，不讓 agent 靜默臆測補齊：

```
System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
```

並把「No [NEEDS CLARIFICATION] markers remain」當 checklist gate。

⚠️ **此機制的執行面已被觀察到失效**：有使用者回報 checklist 勾了「無殘留標記」但 `spec.md` 正文標記仍在——**假完工**。

精確措辭：驗收判準的**權威定義**放需求層、實作計畫另檔並回連，**不可**寫成「測試內容完全不出現在 design/tasks」（Kiro `design.md` 含 Testing strategy、spec-kit `tasks.md` 亦帶 per-task acceptance criteria）。

### 停止條件寫成機器可檢的式子（3-0，單一作者慣例）

goal-md 範本逐字要求「List concrete, machine-checkable conditions — **not vibes**」，五類形式：

```
Stop and report when ANY of:
- score >= 90                                    # 分數閾值
- 5 consecutive iterations with no improvement   # 無進展偵測
- [max iterations] iterations completed          # 迭代上限
- [external dependency] becomes unavailable      # 外部依賴失效
- test suite takes > 60s                         # 成本／延遲天花板
```

前提是先選運作模式，模式決定要不要寫這節：`Converge`（達標即停）／`Continuous`（跑到人類中斷）／`Supervised`（在關卡暫停等核可）。

具體上限的前例：Ralph `MAX_ITERATIONS=10`、Pi auto-continue 上限 3、goal-md 建議 N=5。**這些預設值來源皆未說明依據**，別當調校過的數字引用。

### 完工判定外部化，但必須同時防卡死（medium）

**正面**：Ralph 全 story `passes: true` 才輸出 `<promise>COMPLETE</promise>`，外層 shell `grep` 到才 break。⚠️ 此條查證 **1-2 未過**——sentinel 仍由 agent 自己吐，只是把判定搬到外層，**不等於獨立驗證**。

**更值得抄的是反面**：planning-with-files 的 Stop gate 刻意設計成「只有全部條件同時成立才 block」，避免未完成的計畫把 session 永久困住：

```
The gate is OFF unless ALL of these hold:
1. .mode exists and contains "gate"           # 顯式 opt-in
2. an in_progress phase exists                # 只有 pending 不 block（程式註解引 issue #178 lesson）
4. block counter < PWF_GATE_CAP (default 20)
5. the ledger advanced since the last block   # stall → allow stop
```

另有 **SHA-256 attestation** 防 agent 自行改目標：篡改時注入內容換成 `[PLAN TAMPERED — injection blocked]`，v3 模式無 attestation 時拒絕注入計畫本體。這是全部來源裡唯一把「目標不可被 agent 竄改」做成機制而非宣告的實作——與 [[AI-自主工作流的實證檢驗]] 記載的 Anthropic「選 JSON 而非 Markdown 存進度」同一問題意識。

### 閉環 ＋ append-only 日誌（2-1）

goal-md 的 Improvement Loop：

```
0. Read iterations.jsonl if it exists — note what's been tried and what worked
1. [measure command] > /tmp/before.json
...
6. [measure command] > /tmp/after.json
7. Compare: if improved without regression, commit
8. If regressed or unchanged, revert
9. Append to iterations.jsonl: before/after scores, action taken, result, one-sentence note
```

原則「Every iteration leaves the repo better or unchanged, never worse」＋「Atomic commits — one improvement each, so reverts are clean」；commit 格式 `[S:NN→NN] component: what you did`。

**價值主要在「下一輪不重跑已失敗的實驗」**，不在「防漂移」（後者無證據）。兩點限定：Iteration Log 在範本中標 **Optional**、step 0 是條件式「if it exists」，不是無條件義務；唯一效果數據是單則軼事（「Went to bed. Woke up to 12 commits… 47 → 83」）——**單一作者經驗值**。

⚠️ **內在張力**：goal-md 同時主張「用 scalar 分數驅動 keep/revert」與「reward hacking 預設會發生」——**前者正是後者的溫床**。整條防線靠「計分腳本標不可編輯」撐著，一旦 agent 能改測試，收斂信號即失效。這正是 [[AI-自主工作流的實證檢驗]] 中 ImpossibleBench 與 Cursor 稽核所測到的行為。

### 防範圍膨脹：舉證責任反轉 ＋ 明寫不該變的東西（3-0）

spec-kit `plan-template.md` 逐字：

```
## Complexity Tracking
> Fill ONLY if Constitution Check has violations that must be justified
| Violation | Why Needed | Simpler Alternative Rejected Because |
```

設計意圖是 spec-kit 自己的話：「These gates prevent over-engineering by **making the LLM explicitly justify** any complexity… creating accountability for architectural decisions」。由 agent 而非人填。

配套是 Kiro bugfix spec 的 `Unchanged Behavior (Regression Prevention)` 欄位：

```
WHEN [condition] THEN the system SHALL CONTINUE TO [existing behavior]
```

**Kiro 會把它編譯成 property-based tests**——這是全部來源裡唯一把散文約束變成可執行 oracle 的前例，其餘一律停在宣告。

三點措辭精確度：① 範本從未用「scope creep」字眼，用的是 over-engineering／unjustified complexity；② 這是「**有紀錄的例外**」型 gate，填表 justify 即可通行，非零例外；③ `unchanged behavior` 是**行為不變量**，不是 diff／路徑白名單，要後者得另立欄位。

### 人類 checkpoint 只有一個位置站得住（3-0，單一廠商）

spec-kit 憲法第三條「Article III: Test-First Imperative」逐字：

> This is NON-NEGOTIABLE: All implementation MUST follow strict Test-Driven Development. No implementation code shall be written before: 1. Unit tests are written 2. Tests are **validated and approved by the user** 3. Tests are confirmed to FAIL (Red phase)

即驗收判準先固化成失敗的測試，agent 才有可自主收斂的目標函數。⚠️ 另一種常見說法「checkpoint 擺在 tasks 拆完之後」查證 **1-2 未過**，勿引用。

### 單一任務原則要落成狀態機（3-0）

Ralph `prd.json` 每個 user story 帶 JSON 布林 `passes` ＋整數 `priority` ＋ per-story `acceptanceCriteria`：

```
L10  Pick the highest priority user story where `passes: false`
L11  Implement that single user story
L15  Update the PRD to set `passes: true`
L105 Work on ONE story per iteration
```

旗標集合同時充當停止條件——一個機制兼任防漂移（壓縮每輪 diff 面積）、進度檔與終止判定。精確度：「一件事」＝一個 story，同輪仍含品質檢查、commit、append `progress.txt`、更新 `AGENTS.md`。

### reward hacking 當預設會發生（3-0，單一作者）

goal-md 最關鍵的一句：

> **Without constraints the agent will absolutely find creative ways to make the number go up that you did not intend.**

三道可抄防線：

1. **Constraints 節寫成硬規則**（範本註明「hard rules the agent must never break — **not suggestions**」）：`Never fabricate test results — they come from the test runner only`／`Never modify credentials`／`score must not decrease`／`Atomic commits`
2. **File Map 逐檔標 Editable?**（`Yes / No / Written by [tool] only`），並「Mark scoring scripts and config as "No" so the agent does not game the metric」
3. **Metric Mutability 三檔**：`Locked`（不可改計分碼）／`Split`（可改量測工具、不可改成功定義）／`Open`（含成功標準皆可改）

作者的框架是「Goodhart's Law applies to silicon as much as carbon.」

## 工具層：誰真的被採用

GitHub star 數，2026-07-30 以 `gh api`／`gh search` 直查核實（**star 是採用度／人氣代理指標，不等於品質或效果**）：

| stars | repo | 最後推送 | 定位 |
|---|---|---|---|
| 263,351 | `obra/superpowers` | 2026-07-28 | agentic skills framework ＋開發方法論 |
| 124,508 | `github/spec-kit` | 2026-07-29 | 純 SDD 工具，需 Python CLI |
| 64,798 | `gsd-build/get-shit-done` | **2026-05-31** | GSD 本體，自稱 BMAD 的輕量替代 |
| 63,099 | `Fission-AI/OpenSpec` | 2026-07-30 | 見 [[OpenSpec]] 專屬頁 |
| 51,261 | `bmad-code-org/BMAD-METHOD` | 2026-07-30 | 最重、多角色鏈 |
| 25,839 | `OthmanAdi/planning-with-files` | 2026-07-24 | 計畫落盤＋每 turn 重新注入＋完工 gate |
| 21,318 | `snarktank/ralph` | — | Ralph loop 的 `prd.json` 狀態機實作 |

**GSD 生態有分裂訊號**：本體 `gsd-build/get-shit-done`（64,798）已兩個月未推送，另有 `gsd-build/gsd-2`（7,752、2026-05-22）與 `open-gsd/gsd-pi`（977、2026-07-28）分頭活動。押上去前先確認哪個是活的。

### 選擇判準

- **要「先問清楚你要幹嘛、再幫你寫 spec 與計畫、然後照計畫不偏離地做完」** → `superpowers`。star 是第二名的兩倍，Claude Code 一行裝（`/plugin install superpowers@claude-plugins-official`，亦在官方 marketplace），skills 自動觸發不需記指令，支援 11 種 harness。README 描述的流程：不直接寫碼而是「steps back and asks you what you're really trying to do」→ 從對話中萃出 spec 並分段給你確認 → 你簽核設計後產出實作計畫 → subagent-driven development 逐項執行並互審，自稱「not uncommon for your agent to work autonomously for a couple hours at a time without deviating from the plan」。內建 red/green TDD、YAGNI、DRY 作為防膨脹紀律。
  ⚠️ **本頁對 superpowers 只做了 README 直讀（前 70 行），未跑對抗式查證、未核實機制實作**。「連續自主數小時不偏離計畫」是**廠商／作者自述**。它另有商業服務（`sales@primeradiant.com`），非純社群專案。
- **要最貼近 spec-kit 但更輕** → OpenSpec（見 [[OpenSpec]]，本 vault 已有逐節查證的專屬頁）。
- **要分數驅動的收斂迴圈** → 上述工具皆不涵蓋，需自行加 goal-md 那套（並承擔上述 scalar 分數的張力）。
- **已在用 BMAD** → 它就是同一類的重量級版本；嫌重的輕量替代是 GSD（明確自稱如此）或 OpenSpec。

## 勿引用清單

依 CLAUDE.md 寫入慣例第 6 條，被查證否決者明列，不無聲丟棄。

| 主張 | 票數 | 裁決 |
|---|---|---|
| planning-with-files 的「context window = RAM、filesystem = disk」類比、「三檔案 gitignored、不放其他 runtime state」 | 0-3 | **勿引用**（見下方更正：三檔案與 hook 注入本身為真，被否決的是這些周邊細節） |
| 「lifecycle hook 數量為 Claude Code 5／Codex 7／Pi 8」、「goal drift 歸因於 50+ tool calls 後目標被擠出 attention window」 | 0-3 | **勿引用** |
| spec-kit「單一階段只准動自己那層檔案」屬 diff 範圍限制 | 0-3 | **勿引用** |
| 「同一份規格同時生成實作與測試」 | 1-2 | **勿引用** |
| 「三道可勾 phase gate：Simplicity ≤3 projects／Anti-Abstraction／Integration-First」 | 1-2 | **勿引用**——本輪查明原因：**該內容已從現行 `plan-template.md` 移出** |
| 「`tasks.md` 兼作即時進度檔、狀態即時標 in-progress／completed」 | 0-3 | **勿引用** |
| 「人類 checkpoint 擺在 tasks 拆解完成之後」 | 1-2 | **勿引用** |
| 「goal-md 的 GOAL.md 全部欄位皆必填」 | 1-2 | **勿引用**（Iteration Log 等節標 Optional） |
| 二手比較文引的 star 數（Superpowers 166k、spec-kit ~90k） | — | **勿引用**：2026-07-30 實查為 263,351／124,508，**二手比較文的數字系統性偏低** |

## 兩條方法論教訓

### 對抗式查證會過度否決

本輪 verifier 把 planning-with-files 的「三檔案 ＋ hook 每 turn 重新注入」整條判 **0-3 否決**，但該 repo README 逐字寫著 `task_plan.md`／`findings.md`／`progress.md` 與「re-injects them every turn」、注入格式為 `===BEGIN PLAN DATA===`、由 `UserPromptSubmit` hook 寫入。**真正不可靠的只有周邊細節**（各家 hook 數量、attention window 的歸因），verifier 連同核心一起殺掉。

含意：**3 票制的否決不等於「該事實為假」，只表示「該條主張的表述無法整體成立」**。回存時應把可核實的核心與未經核實的細節拆開判，不要整條丟棄——這是本 vault 使用 deep-research 產出時的已知偏誤方向（與 [[Agent-維護知識庫的已知失效模式]] 的壓縮丟限定詞屬同族問題：一個丟限定詞、一個因限定詞為假而丟主體）。

### 二手比較文的數字不可信

本輪同時取得二手比較文與 `gh` API 實查，兩者對同一批 repo 的 star 數落差達 1.6–1.9 倍且方向一致偏低。**工具採用度一律直查 API 並標日期**，不引用聚合文章的數字。

## 開放問題

- **尺規隔離只有宣告、沒有機制**：測試／計分腳本與被改的程式碼同 repo 時，五個來源全部只做到「在 goal 檔標成不可編輯」，無一實作強制隔離（獨立 repo／唯讀 mount／分離 CI 身分）。這是整個機制群最大的單點失效。
- **分層 goal 檔自身的漂移如何對帳**：spec-kit 生態自承缺實作後複檢（issue #1063、#1323），而長跑 agent 最需要這一段。現行 `/speckit.analyze` 與 `/speckit.converge` 是否真能對帳未經核實。
- **「連續 N 輪無改善即停」的 N 該取多少**、多維度指標下「無進展」如何定義？goal-md 的 5、Ralph 的 10、Pi 的 3 皆為未調校預設。
- **散文約束在什麼條件下能自動編譯成可執行 oracle**？Kiro 為 unchanged behavior 生成 property-based tests 是唯一前例，其可靠性、覆蓋率與失效模式無任何來源說明；而 AgentSpec（[arXiv 2503.18666](https://arxiv.org/abs/2503.18666)）發現文字約束**累積後表現退化**，暗示純文字路線有上限。
- superpowers、GSD 的實際機制均未核實（僅 README 層），與本頁機制清單的對應關係不明。

## 相關頁

- [[AI-自主工作流的實證檢驗]] — 本頁的效果證據基礎：spec-driven／長時 loop 的獨立實證幾乎不存在，而 reward hacking（ImpossibleBench 76%、Cursor 稽核）與長任務可靠度崩落（METR）是硬證據。本頁「reward hacking 當預設會發生」的設計前提，正是該頁「規格越模糊，agent 越容易轉向讓測試通過」的操作化；本頁補上該頁 spec-driven 節缺的**可抄措辭層**。
- [[OpenSpec]] — 本頁工具表中唯一已逐節對抗查證的一手工具頁；該頁的 delta spec、artifact DAG、`config.yaml` 脈絡注入可視為本頁「分層落盤」的一種具體 schema 化。
- [[Agent-工作流-Pattern-藍本庫]] — 該頁自陳「只涵蓋 agent 工作流編排，軟體開發概念型流程待補」；本頁的機制清單即該缺口的軟體開發側補充（目標定義與收斂控制，非 agent 編排）。
- [[Agent-維護知識庫的已知失效模式]] — 本頁「對抗式查證會過度否決」與該頁「壓縮系統性丟限定詞」是同一族失效：都讓經過處理的知識比原始來源更不準確，且方向不隨機。
- [[Agent-Harness-Engineering-框架綜述]] — 該頁記載業界主張該怎麼設計 harness；本頁的停止條件、完工 gate、進度落盤是那些主張在具體工具裡的落地形態。
