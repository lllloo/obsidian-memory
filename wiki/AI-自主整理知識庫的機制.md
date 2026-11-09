---
title: AI 自主整理知識庫的機制
description: 具名系統讓 AI 自行去重、拆頁、補缺口的做法與防失真設計，附反覆固化的反面實證與本 vault 適用評估
created: 2026-11-09
updated: 2026-11-09
parent: "[[wiki/01.index]]"
tags:
  - wiki
  - knowledge-graph
  - ai-agent
  - memory
---

# AI 自主整理知識庫的機制

本頁回答：除了 ingest 當輪的局部維護，現行（2026 下半年）AI 知識庫與 agent 記憶系統怎麼讓 AI **自己整理結構**（去重、拆頁、改名、導覽頁、固化），以及**主動補缺口**（找出單薄區域、自行研究補頁），還有這些做法會怎麼壞。來源是 2026-11-09 一輪 deep-research（22 個來源，25 條主張經三票對抗查證），加上主 agent 回讀一手原文，補核未驗證和被否決的主張。

**結論先講**：

- 生態收斂成同一種分工：**偵測交給 AI 自動跑，動作依歧義程度分級**。答案唯一的結構修補全自動，例如重生索引、補登孤立頁、把死連結改指到既有頁。合併、拆分、改名這類有歧義的動作，先產生候選，再由 LLM 讀全文裁決或交人拍板。
- 讓 AI 多整理，主要風險不在單次動作，而在**反覆改寫**。多份 2026 研究顯示，LLM 持續固化記憶會讓原本有用的記憶變壞，甚至比不用記憶還差（見下「反面證據」）。所以要加碼自主，該加的是**偵測器與觸發點**，不是提高改寫頻率。
- 「主動上網補缺口」證據最薄。沒有任何系統對「AI 自選題、自己研究、自己寫頁」做過效果評估。現成做法多半是 AI 偵測缺口，由使用者給題，再跑有界的研究。

## 共同模式：偵測自動、動作分級

| 動作類型 | 生態做法 | 代表 |
|---|---|---|
| 答案唯一的結構修補 | 寫入後自動修，乾淨時不出聲 | nvk Structural Guardian、Anthropic dreaming 的死連結改指 |
| 有歧義的合併／拆分／改名 | 先產候選，再由 LLM 讀全文裁決或人拍板；裁決留紀錄防翻案 | obsidian-wiki `wiki-dedup`、Synto |
| 內容固化（多筆整理成摘要） | 增量處理加上限，以原始層當 ground truth | ReMe Auto Dream、Anthropic dreaming、Letta Dreaming |
| 缺口偵測 | 只報候選（品質訊號、共現、核心頁過時） | Hermes `llm-wiki`、obsidian-wiki `wiki-synthesize`／`wiki-status`、nvk Librarian |
| 缺口補寫（上網研究） | 使用者給題、輪數有上限、來源先落地 | obsidian-wiki `wiki-research`、jackwener `research`、nvk `--min-time` |

## 結構自整理

### nvk/llm-wiki：Structural Guardian

[nvk/llm-wiki](https://github.com/nvk/llm-wiki) 的規格寫明，每次寫入後自動跑輕量檢查，原文是「Silent when clean. Auto-fix trivial issues. Warn on structural problems. Never block the user.」自動修只限兩種情況：索引列數和實際檔案數不符時，重生該目錄的索引；孤立檔則補登進索引。有歧義的 wikilink、footnote、coverage 都不自動修，hub 層內容也不自動刪。內容層的維護工具 Librarian 只產出分數報告（staleness 與 quality 各 0–100）；`fix <id>` 標為「not yet implemented」，dedup 和 coherence 兩個 pass 列在 future。

- 證據強度：clone 一手規格（2026-10-25 HEAD）逐字核對。Guardian 只存在於 prompt 層，沒有程式邏輯，也沒有效果實證。repo 內 Librarian 的品質分數算法有兩處寫法不一致：AGENTS.md 寫四個面向各 25 分、低於 40 標記；`references/librarian.md` 寫各面向 1–5 分、平均後乘 20、門檻 70。
- 對照本 vault：ingest 收尾的輕量 lint 和 `vault-lint` 機械層已經涵蓋孤立頁與索引缺口，功能相當。

### obsidian-wiki：兩段式去重 `wiki-dedup`

[Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki)（約 3,700 stars，2026-11 仍活躍；本 vault 先前未收錄）的 [`wiki-dedup`](https://github.com/Ar9av/obsidian-wiki/blob/main/skills/wiki-dedup/SKILL.md) 把去重拆成兩段，藉此控制成本：

1. **找候選只看 frontmatter 和標題**：標題相似度取 Jaccard、正規化編輯距離、子字串包含三者的最大值，再加上 alias 交叉比對，同目錄或共享 tag 另外加分。合成分數 ≥0.75 列為候選，≥0.90 為高信心。
2. **只對候選讀全文**：LLM 給出 merge／keep-separate／needs-review 三種裁決，各附一句理由。規格明確警告「不同版本不是重複」。

預設只報告。`--auto` 只合併「高信心且裁決為 merge」的配對，寫入前先記 git snapshot。被合併的頁會改寫成帶 `redirects_to:` 的 stub，並全庫改寫指向它的 wikilink。少於 10 頁的 vault 直接跳過。

- 證據強度：一手規格逐字核對。分數由 LLM 判斷估算（規格原文「You don't need exact arithmetic」），不是程式算出來的；沒有準確率實證。標題相似度是為英文標題設計的，套在中文標題上的召回率與誤報率未經檢驗。

### Synto：偵測自動、拍板保留，裁決防翻案

[Synto](https://github.com/kytmanov/synto)（單人維護，約 267 stars）會在 `doctor`／`concept inspect` 提出 merge candidate，但不會自行合併。人工拆掉的錯誤 alias 會留下 **denial tombstone**，下一輪 ingest 不得再接回去。rename 保留舊名當 alias，避免重新 ingest 時把舊概念建回來。由人下指令的 `concept merge／split／unmerge／rename` 都會記 log、支援 dry-run，並自動 commit。

**可逆性陷阱**：概念身分存在被 gitignore 的 `state.db`，所以 `synto undo` 遇到這類操作會拒絕撤回，只能改下反向指令。`unmerge` 也只是 best-effort：只能以空 stub 重建，合併時共享的來源和連結都不會還原。

- 證據強度：CHANGELOG、程式碼與測試互相印證，機制確實存在；沒有效果證據。
- 對照本 vault：純 markdown 加 git、沒有旁路狀態，`git revert` 就能完整撤回，前提是**每次合併或拆分各自一個 commit**。Synto 的 tombstone 在本 vault 的對應物，是 `schema/BACKLOG.md` 的「Agent 已判」。

### Hermes llm-wiki：拆頁、封存與索引分層門檻

[Hermes 的 `llm-wiki` skill](https://github.com/NousResearch/hermes-agent/blob/main/optional-skills/research/llm-wiki/SKILL.md)（2026-10-29 起移到 optional-skills，不再預設載入）的規定如下：

- 頁面超過約 200 行就拆成子主題並互連，lint 會標出超過 200 行的頁。
- 內容被完全取代的頁搬到 `_archive/`，從 index 移除，原本的連結改成純文字加「(archived)」。
- index 任一分區超過 50 條就再細分，總數超過 200 條才建 `_meta/topic-map.md`。

規格內沒有自動合併重複頁的步驟。

- 證據強度：一手規格逐字核對。門檻是經驗值，沒說明理由，也沒有實證。
- 對照本 vault：65 頁，index 還沒到 topic map 門檻；但已有 11 頁超過 200 行（2026-11-09 實測）。

### Letta：使用者發起的重整、背景 Dreaming

[Letta 記憶文件](https://docs.letta.com/configuration/memory)寫明，大型重整（拆大檔、合併重複、重組層級）要由使用者開口要求，記憶工作流**動手前會先備份 repo**。記憶層級漂移或膨脹時，可用 `/doctor` 稽核擺放位置、重複內容與 system prompt 的 token 用量。背景 Dreaming 由 subagent 回顧近期對話並更新記憶，觸發條件只有兩種：完成一定數量的 agent steps 後，或 context 被壓縮時。選用的「先審再套用」由 agent 在第二條背景對話裡自審，不請使用者批准。

- 證據強度：官方文件 2026-11-09 一手抓取。文件沒有談效果，也沒有談防失真。

### ReMe Auto Dream：增量、上限、四動作與 provenance

[ReMe](https://github.com/agentscope-ai/ReMe) 的 Auto Dream 由 cron 或手動觸發，只掃最近的日期窗口（預設 2 天），只處理 mtime 有變的檔，每輪最多抽 5 個記憶單元。整合時對每個單元先搜尋相似的 digest node，再從四個動作中擇一：

- CREATE：新建。
- CORROBORATE：同一記憶再現，只補來源。
- REFINE：補邊界或步驟。
- CORRECT：修正錯誤。

護欄有四條：原始 daily 永不改寫；digest 必須在 Sources 段，用帶上下文的句子 wikilink 回 daily；更新只能增加、不得刪除既有 wikilink；不得憑空寫 overview。

- 證據強度：文件、prompt 與程式 enum 一手核對。除了四動作 enum，其他護欄全靠 prompt，沒有防失真實證。
- 對照本 vault：Ingest 第 1 步「寫一頁摘要（或更新既有摘要）」已有雛形。「先搜既有頁、再四選一」和「不憑空寫 overview」可以直接移植。

### Anthropic dreaming：以原始紀錄為 ground truth

[Anthropic〈Components of agent memory〉](https://www.anthropic.com/research/components-of-agent-memory)（2026-11-06）中與本頁相關的實驗：

- **ground truth 校驗**：Pokémon 實驗中，一條方位寫錯的記憶讓 agent 三度走回頭路。dreaming 對照原始 transcript 抓到錯誤並改寫後，agent 才抵達目的地。這是單次對照，屬軼事級證據。
- **wiki 型 dreaming**：Opus 5 agents 跑了 128 個 session，探索檔案、撰寫或修正互連頁、合併重複頁、對照來源校驗主張。在 25 題的評測上，只用 wiki 的得分從 13% 升到 48%；wiki 加搜尋是 61%，只用搜尋是 53%。另一輪 dreaming 把 9 條指向不存在頁面的連結改指到既有頁，另外新增 3 頁。
- **副作用一：膨脹**。另一個 wiki 長到 68 頁、255 條連結、203 KB，是原始語料（10 份文件、115 KB）的 1.77 倍，而且有孤立頁。
- **副作用二：共寫覆蓋**。多個 agent 同時寫一張共用的合約條款表，互相覆蓋，摘要只保住 57 項事實中的 41 項。改成每份合約一頁、由單一 agent 逐字引用條款後，保住 57/57。
- **成本建議**：持續檢查全部記憶並不實際，應聚焦可能變動的資訊，並依存取頻率調整節奏。文章沒有給具體觸發條件。

- 證據強度：單一廠商的內部實驗，題數小、未經同儕審查；2026-11-09 回讀原文核對數字。

## 主動補缺口

### Karpathy 原文就把缺口偵測放在 Lint

[[LLM-Wiki-Karpathy]] 的 Lint 段列了「important concepts mentioned but lacking their own page」和「data gaps that could be filled with a web search」，並說 LLM 擅長建議新問題與新來源。本 vault 的 lint 在 2026-07-22 收窄為「只抓真的壞了」，這兩項不在現行掃描範圍內。

### obsidian-wiki `wiki-synthesize`：共現但無綜合頁

[`wiki-synthesize`](https://github.com/Ar9av/obsidian-wiki/blob/main/skills/wiki-synthesize/SKILL.md) 把「同時連到 A 與 B 的頁數」當作共現分數。做法是取前 20–30 對，扣掉已有綜合頁的配對，再依共現數、是否跨類別打分，挑最有價值的寫成綜合頁。每頁都必須有「Strongest Objection」段：寫出最強的懷疑讀法，並附一條可測的搜尋問句，不得編造引用。規格明說「Don't synthesize for synthesis's sake」。

- 證據強度：一手規格，沒有效果實證。這是本輪唯一「只用 wiki 內部訊號、不上網」的主動補頁做法。

### obsidian-wiki `wiki-status`：核心頁過時優先

[`wiki-status`](https://github.com/Ar9av/obsidian-wiki/blob/main/skills/wiki-status/SKILL.md) 不列出所有過時頁，只報「`updated` 距今 ≥90 天**且**入鏈 ≥5」的核心頁。理由是別頁依賴它，它過時的代價才大。

- 證據強度：一手規格；門檻是經驗值。
- 對照本 vault：git 紀錄顯示 2026-09-17 至 10-29 已跑過 5 輪全庫時效核對，其中 10-14 和 10-29 兩輪各逐頁比對約 60 頁。有了這類訊號，下一輪可以先查核心頁，不必每次都掃全庫。

### 有界研究迴圈：選題、停止與防幻覺

- [obsidian-wiki `wiki-research`](https://github.com/Ar9av/obsidian-wiki/blob/main/skills/wiki-research/SKILL.md)：
  - 題目由使用者給。先讀 index，避免重查已涵蓋的主題。
  - 最多 3 輪：先廣搜，再補第 1 輪留下的缺口，只在仍有重大矛盾時才跑第 3 輪。「depth is achieved or 3 rounds are complete」即停。
  - 查不出權威結論的矛盾，必須在綜合頁明列，不得自行調和。
  - 產出頁標 `lifecycle: draft` 與 provenance 比例，直接進正式 wiki，用頁內信任標記取代 staging 層。
- [jackwener/llm-wiki `research`](https://github.com/jackwener/llm-wiki/blob/HEAD/skills/research/SKILL.md)：
  - 每輪收 5–10 個來源，偏好一手資料。
  - **每個來源在分析前先存檔，存後不可改**。
  - 研究問題要有界，岔題列為 follow-up；報告必須留 Remaining Gaps 一節。
  - 跨來源綜合頁只在結論夠新、證據夠足時才建。
- [nvk `--min-time`](https://github.com/nvk/llm-wiki) 多輪研究：每輪依 sources、articles、cross-refs、credibility 加權，打 0–100 的進度分，連兩輪低於 40 才停。輪與輪之間，用 Impact×Feasibility×Specificity（各 1–5）挑出下一輪的前 3 題。分數由 LLM 自己算，沒有程式邏輯，也沒有效果實證。
- Hermes `llm-wiki` 只做偵測：靠 frontmatter 的 `confidence`、`contested` 欄位和 lint 報告，列出待補佐證的頁。整份流程沒有自動上網研究的步驟。

## 反面證據：自主整理為什麼會壞

完整的證據強度與場景差距，見 [[Agent-維護知識庫的已知失效模式]] 第 1、5、6 條。這裡只列對「讓 AI 多整理」的直接含意。

- **反覆固化會讓有用的記憶變壞**（[arXiv 2605.12978](https://arxiv.org/abs/2605.12978)）：記憶效用先升後降，可能跌破無記憶的基線。即使從正確解答固化，GPT-5.4 仍在 54% 原本不靠記憶就解得出的 ARC-AGI 題目上失敗。同一批軌跡一次固化，結果勝過串流固化，可見**傷害來自反覆改寫，不是證據本身**。只保留原始軌跡的對照組，表現與受測的固化器相當。作者建議：把原始紀錄當一等證據保留，固化要明確設閘門觸發，不要每次互動後都跑。
- **整篇重寫會塌縮**（ACE，[arXiv 2510.04618](https://arxiv.org/abs/2510.04618)，ICLR 2026）：讓 LLM 每一步都整篇重寫累積的 context，一步之內就從 18,282 tokens 塌成 122 tokens，準確率從 66.7 掉到 57.1，低於不做 adaptation 的 63.7。ACE 的解法是 LLM 只產出增量 delta，再由非 LLM 的邏輯合併。
- **自己寫的文件會被自己優先引用**（RAG collapse，[arXiv 2608.22118](https://arxiv.org/abs/2608.22118)）：檢索到自己寫的參考資料時，引用率是 38.9%；別的 AI 寫的原文是 9.4%，人寫的原文是 7.4%。1,528 次模擬中有 79.6% 以同質化收場，**混入一份自己寫的文件就可能觸發**。本 vault 的 wiki 全由 agent 撰寫，補缺口時若拿 wiki 頁當新主張的證據，就落入這個迴圈。
- **研究管線像傳話遊戲**（[arXiv 2608.24306](https://arxiv.org/abs/2608.24306)）：多 agent 深度研究的錯誤，多數由最上層的彙整者引入。把研究者的綜合筆記換成**來源原文片段**，並要求不用沒有引用的資訊，citation recall 約升 5 點，precision 升 3–7 點。只摘要單一文件的 agent 幾乎不出錯。

## 對本 vault 的含意（2026-11-09 評估與拍板）

本 vault 已經給 AI 全權改頁、刪頁、commit、push。缺的不是權限，而是**讓 AI 知道該整理什麼的偵測器與觸發點**。

2026-11-09 實測現況：

- 65 頁，其中 11 頁超過 200 行。
- `01.index.md` 約 2.2 萬字元，單筆「一行摘要」最長約 1,000 字元。依字元數粗估已超過 1 萬 tokens（未實測），可能已達 [[LLM-Wiki-生態實作比較]]「檢索升級門檻」第 ② 條（index 逼近 8–10K tokens）。主因是條目從一行長成段落，不是頁數太多。同日第 1 輪整理已把條目改回各頁 `description`，索引縮到約 1.4 萬位元組，見下方試跑結果。

**值得做的（成本低，直接對應已知失效模式）**：

1. 改既有頁時用局部編輯，不整頁重寫；非大改不可時，回 `raw/` 或原始來源校驗，不以舊版 wiki 為準（依據：ACE、2605.12978、Anthropic dreaming）。2026-11-09 使用者拍板，已寫入 `AGENTS.md` 寫入慣例第 7 條。
2. 補缺口時寫進 wiki 的新主張，證據必須是外部一手來源，不得只引本 vault 其他 wiki 頁（依據：RAG collapse、2608.24306）。2026-11-09 使用者拍板，同上第 7 條。
3. 開一個由使用者在 session 內觸發的「整理」輪：AI 跑偵測（重疊頁、超過 200 行的頁、index 膨脹、多處提及卻無專屬頁、共現卻無綜合頁、核心頁過時），自己挑最多 3 項處理，每項一個 commit。判定不動的（例如 keep-separate）記進 `schema/BACKLOG.md`「Agent 已判」當 tombstone，防止下輪重提。依 Skill 升級訊號原則，先手動跑，重複成套路後才 codify。
4. Ingest 第 1 步明確化為「先搜既有頁，再從新建、補來源、細化、修正四者擇一」（依據：ReMe）。未提交拍板，維持候選。

**整理輪第 1 輪試跑結果（2026-11-09，使用者同意試跑）**：

- **索引膨脹**：唯一實際動手的一項。條目改用各頁 frontmatter 的 `description`，不從舊的長條目改寫，避免失真；「最近更新」每筆縮成一句。索引從 41.3 KB 縮到 14.3 KB，最長一行從約 1,000 字元降到 149 字元。
- **重疊頁**：用標題 bigram 相似度找候選，再讀章節判斷，4 組都判定不合併（keep-separate），已記進 `schema/BACKLOG.md`「Agent 已判」。中文標題用 bigram 比對可行，但候選多半是刻意的母子分層。
- **過長頁**：11 頁超過 200 行，逐頁看章節後都是單一主題，長度來自深度，不是混題。**行數不適合當拆頁觸發**，判準應改為「一頁混了多個可獨立查詢的主題」。
- **核心頁過時**：2 頁符合「updated ≥90 天且入鏈 ≥5」，但這個訊號在本 vault 失準。全庫時效核對時內容沒變的頁不會改 `updated`，所以 `updated` 不等於最後核對日。若要依此縮小時效核對的範圍，得先有地方記「最後核對日」。
- 「多處提及卻無專屬頁」與「共現卻無綜合頁」兩個偵測，本輪沒跑（每輪上限 3 項）。

**屬過度工程，或與既有拍板衝突**：

- 自動 MOC／topic map：Hermes 的門檻是 200 條，本 vault 只有 65 頁。
- 多輪自動研究迴圈、LLM 自算的進度分：成本高，沒有實證。
- embedding 去重：牴觸向量檢索門檻。
- AI 自審的第二對話：牴觸「勿提獨立 refuter」。
- `confidence` 欄位與 90 天過時標記：牴觸 frontmatter 白名單和「語意層不報過時」。
- `state.db` 之類的旁路狀態。
- cron 排程固化：牴觸 session 模式。

## 查證過程註記

- **驗證關卡過度否決、回查後成立**（2026-11-09 主 agent 回讀一手原文）：
  - Letta「大型重整由使用者要求、動手前先備份 repo」（原判 0-3）：現行文件逐字寫明，成立。
  - nvk Librarian「只出報告、`fix` 未實作、dedup／coherence 列在 future」（原判 1-2）：AGENTS.md 逐字寫明，核心成立；分數細節 repo 內自相矛盾，見上。
  - Hermes「約 200 行拆頁、沒有合併步驟」（原判 0-3）：兩項都成立。錯的只是「唯一的結構機制」這個說法，規格另有 `_archive/` 封存。
- 本輪驗證預算只覆蓋 110 條擷取主張中的 25 條。`wiki-synthesize`、`wiki-status`、jackwener `research`、2605.12978、2608.22118、2608.24306 的內容，由主 agent 回讀一手原文補核，沒有經過三票對抗。
- **勿引用**：
  - 搜尋摘要把 Anthropic 實驗用的模型寫成 Opus 5.5，原文是 Opus 5。
  - RAG collapse 論文另有一個數字：「2026-01 ChatGPT 參考資料中，38.9% 被判為 AI 生成」。它和自寫文件引用率 38.9% 數值巧合相同、意義不同，勿混用。

## 證據限制

- 信心標記衡量的是「機制確實如文件所述存在」，不是「機制有效」。除了 ACE 的 benchmark、2605.12978 的受控實驗與 Anthropic 的小樣本對照，其餘都是 prompt 規格或專案自述。
- 目前沒有任何系統對「AI 自主合併或拆分 wiki 頁」量化過失真率。ACE、2605.12978 的場景是 agent playbook 與經驗記憶，Anthropic 的語料是程式碼庫與合約任務，套到個人研究 wiki 都只是類比。
- 來源都落在 2026-06 至 2026-11，repo 變動快，引用前請回查現況。

## 關聯

- 失效面：[[Agent-維護知識庫的已知失效模式]]。本頁「反面證據」節的完整強度與場景差距在該頁第 1、5、6 條；本頁講同一問題「怎麼做」，該頁講「怎麼壞」。
- 生態對照：[[LLM-Wiki-生態實作比較]]。nvk、Hermes、ReMe 的既有比較在該頁；本頁補上 obsidian-wiki 與 Synto，只聚焦自主整理這個切面。
- 設計原型：[[LLM-Wiki-知識管理模式]]。Karpathy 原始 Lint 的缺口偵測，是本頁「主動補缺口」的起點。
- 導覽頁門檻：[[第二大腦實踐與本-vault-優化]]。該頁「以問題簇觸發小型 MOC」與本頁 Hermes 的分區門檻同方向：沒有使用需求就不預建導覽頁。
- 品質訊號：[[LLM-as-judge-知識庫頁面評分]]。nvk Librarian 由 LLM 自評分數，受該頁所述的 self-preference bias 限制。
