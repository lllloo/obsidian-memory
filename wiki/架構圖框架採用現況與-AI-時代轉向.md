---
title: 架構圖框架採用現況與 AI 時代轉向
description: C4／arc42／4+1／UML 誰是主流查無可信數據，唯一產物計數顯示框架本身就不是主流；並記 2026 年 C4 專用工具鏈封存與架構約束機構化的轉向
created: 2026-08-10
updated: 2026-08-10
source: https://robertoverdecchia.github.io/papers/ECSA_2024.pdf
parent: "[[wiki/01.index]]"
tags:
  - diagram-as-code
  - coding-agent
  - ai-agent
---

「目前主流的架構圖框架是哪一套」這個問題，**在可查證的層次上沒有答案**。查下去會發現兩件比答案本身更有用的事：一是所有被引用的採用數字都出自利益相關方的小樣本問卷，二是唯一對真實產物做計數的研究指出**框架本身就不是主流**——大多數人畫的是沒有遵循任何框架的方框連線。

> 本頁為 2026-08-10 deep-research 回存（5 搜尋角度 → 24 來源 → 118 主張 → 對抗查證 25 條，16 確認、9 否決）。**兩處與 harness 原始輸出不同**：一組被 0-3 全票否決的主張經一手複驗確認為真（見「被誤殺的主張」節），且原輸出宣稱「架構約束用於 AI 產碼查無任何討論」是驗證取樣偏誤（`budgetDropped: 6`）造成的假象，已就地更正。每條主張標證據強度與票數。

## 為什麼「主流是哪套」查不到答案

本輪未找到任何大樣本、非廠商自辦的調查在 2024–2026 量測過架構圖框架的選擇。Stack Overflow、JetBrains Developer Ecosystem 這類年度調查都沒有這個題目。實際流通的採用數字只有兩個來源，且都不能當業界代表（**high，3-0**）：

| 來源 | 樣本 | 為什麼不能用 |
|---|---|---|
| IcePanel《State of Software Architecture》2024 / 2025 | n=96 / n=75 | IcePanel 本身就是賣 C4 建模工具的廠商。兩版全文對 arc42、UML、4+1、Kruchten、ArchiMate 的命中數**皆為 0**——問卷從頭到尾預設 C4，只問「對 C4 的熟悉度」與「用哪幾層 C4 圖」，結構上不可能產生跨框架採用率的分母 |
| arc42 官方 FAQ（A-4） | — | 自承其國際使用統計並無良好記錄 |

IcePanel 2024 版還自陳「這是我們第一次發的問卷」，並對「64% 使用建模工具」自嘲「有點意外，畢竟是我們發的問卷」——等同承認受眾偏差。2025 版 68% 受訪者為 6 年以上資歷、57% 為架構師，樣本高度自我選擇。

### 唯一的產物計數：框架不是主流，方框連線才是

ECSA 2024（Migliorini、Verdecchia、Malavolta、Lago、Vicario，《Architectural Views: The State of Practice in Open-Source Software Projects》）從 GitHub 挖出 373 份架構視圖做編碼，結果是 **96% 非正式（方框連線）、4% 半正式（主要為 UML）、0% 正式標記法**（**medium**；主張本身 3-0，但同源另一版因加上「statistically representative」措辭而以 1-2 被否決——爭點在代表性宣稱，不在數字）。

關鍵限制要一起記：該研究的抽取欄位只分 informal／semiformal／formal，**沒有任何欄位問「這張圖遵循哪套框架」**，所以 C4／arc42／4+1 在此資料集中結構上不可量測（全文對 arc42、4+1、Kruchten 命中 0 次，C4 僅 1 次且出現在 Discussion 的建議句裡）。它能支持的命題是「框架化標記法在開源實務中是少數」，不能反過來用來比較框架之間誰多誰少。

### 「arc42 與 C4 主導實務」是定位陳述，不是證據

2026 年的 ICSA workshop 論文 RAD-AI（Larsen & Moghaddam，SDU Denmark，arXiv 2603.28735）正文直接寫「Two frameworks dominate practice」，但引用鏈 [1] 是 arc42.org 網站、[2] 是 Simon Brown 自出版的 Leanpub 書，**全文無任何採用率數字**（**high，3-0**）。

同篇有一個值得單獨記下的反面教材：它的量化開場白「93% 的組織因架構與實作不一致而承受負面業務結果」引用的是 vFunction《2025 Architecture in Software Development Report》——**架構現代化廠商自辦的行銷調查**。廠商行銷數字被洗進同儕審查論文，引用時務必回溯到原始來源判斷強度。

可以說的只有生態聲量：在 RAD-AI 全文中 C4 出現 83 次，UML 僅 2 次且都在 "PlantUML"（被當成 C4 的算繪工具），4+1 與 Kruchten 各 0 次。**在 2026 年的架構文件研究語境裡，UML 與 4+1 已不在比較清單上**，C4 是預設參照框架。這是聲量與生態訊號，與採用率是兩回事。

## 落地形態：C4 已與 diagram-as-code 綁定

唯一的同儕審查工業經驗報告是 SEAA 2025（Jongeling 等，《Adopting the C4 model for lightweight architecture modeling》），案例為 Grundfos（丹麥嵌入式軟體，約 150 名軟體工程師）。摘要原句：「architecture diagrams were expressed in PlantUML and stored within Markdown files alongside the code」，正文明說 **not in a dedicated modeling tool**（**high，3-0**）。

證據強度必須一起標：導入兩年後的回顧式問卷，48/150 回覆（約 30% 回應率），作者載明「some criticism citing an increase of effort with little perceived value」、約三分之一受訪者覺得更難，並在結論自陳「We do not claim that these results are generalizable to all industry contexts」。同期併行的架構債重構是干擾因素。另有一個精確性補充：並非 100% PlantUML——component view 因 PlantUML 無法細控版面而改用 draw.io。

## AI 時代的三個實際轉向

### ① C4 的專用工具鏈萎縮，語法被通用工具吸收

**`structurizr/cli`、`structurizr/java`、`structurizr/lite` 三個核心 repo 已全部 archived，最後 push 同為 2026-02-01**（**high**；本頁作者以 GitHub API 一手複驗，見下方「被誤殺的主張」）。stars 分別為 567、1,135、384。

同時方向相反的訊號是 C4 語法進入通用 diagram-as-code 工具：Mermaid 官方文件有 C4 專頁、npm registry keywords 含 `c4 diagram`。但它在 Mermaid 內長期是二等公民（**high，3-0**）——官方文件掛警語「This is an experimental diagram for now」，不使用全自動佈局（靠敘述順序調位置），`Lay_U/D/L/R` 永不支援，sprites／tags／links／legend 與自訂 stereotypes 皆不支援。GitHub issue #7849（2026-06-12 開，仍 OPEN）目標是「replace the legacy row-grid C4 renderer with the unified rendering pipeline」；至 2026-08 元素形狀遷移（#7842）已併入 develop，**邊線與佈局仍是 legacy**。

另有一份受 Structurizr 啟發的全新 `c4-beta` 語法 RFC 原型（PR #7843，作者 filipsajdak），**C4 model 作者 Simon Brown 本人參與 RFC 討論並對 `external` 關鍵字提出異議**（**high，3-0**）。但它至 2026-08-10 仍是 open draft、reviews 為空、已發布版本不含此語法，且 issue 內文自陳「Prepared with assistance from Claude Code」——屬生態聲量，不入採用率。

把兩邊放在一起看，這條線索指向一個值得追蹤的趨勢判斷：**C4 作為「規格」正在擴散，C4 作為「產品」正在收縮**。

### ② 架構約束用於 AI 產碼已是機構級議題——但仍無實證

Thoughtworks Technology Radar **Vol 34（2026-04）** 收錄技術條目 `Architecture drift reduction with LLMs`，ring = **Assess**，做法是靜態分析工具結合 AI 評估，明確點名 **ArchUnit**、Spectral、Spring Modulith；問題定義正是「AI coding agents 複製劣化模式造成的漂移」，並記錄三項經驗：初次掃描會產生大量違規需分流、把 agent 產生的修正保持小而聚焦較易 review、需要額外驗證迴圈防止回歸（**medium-high**；本頁作者一手 WebFetch 該條目，但取得的是頁面摘要而非完整逐字正文，引用個別語句前應回讀原頁）。

Structurizr 官方 `/ai` 頁把 C4 模型定位為 AI 產出的**輸入驗證與一致性保障**：「Structurizr was designed to support the C4 model... can therefore enforce the hierarchy of abstractions... and enforce the rules」，並提供 MCP server 做 DSL 驗證、解析與 inspection（**medium-high**，同上為一手 fetch 摘要）。該頁未提及從架構模型產生程式碼或反向工程。

**但實證強度必須說清楚：目前為零。** Radar 的 Assess 意思是「值得探索以理解它會如何影響你的企業」，不是建議採用。Codesai（Manuel Rivero，2026-04-26）記述在 Java 客戶專案用 ArchUnit、在 TypeScript 練習用 ArchUnitTS 做 guardrail，核心論點是「while we cannot always prevent an agent from generating code that breaks a desired design rule, guardrails like architecture tests can certainly prevent that code from ever becoming a permanent part of our system」，並說明選架構測試而非 linter 是因為「architecture tests make the intent of design rules easier to read」——但**全文無任何量化數據**（無違規攔截率、無專案數、無成本數字），是純經驗論述（**high**，一手 fetch）。

而唯一的同儕審查工業案例正面反證：Grundfos 論文原句「**no automated means are in place to check the alignment between documentation and implementation. Thus the teams rely on manual means, e.g., code reviews**」（**high，2-1**；爭點僅在單案例能否支撐「尚未成立」的措辭）。該論文全 17 頁對 archunit／fitness function／LLM／AI／agent／CI／pipeline 的命中數皆為 0，RAD-AI 亦把 automated compliance checking 列為 future work。旁證同向：arXiv 2308.09978 指出「participants rarely rely on automated tools to check architecture conformance」。

⚠️ **必要限定**：這是 absence of evidence。本輪的檢索面是架構文件研究與問卷，**未從 ArchUnit／fitness function 工具生態側反查**（Maven 下載量、GitHub 依賴數、工程部落格實測），且 Grundfos 的問卷資料早於 2025–2026 的 agentic coding 浪潮。只能支撐「此用法目前查不到量化實證」，不能宣稱它無效或不存在。這條約束的可行性論證見 [[Uncle-Bob-的不讀碼約束閘門]]——那裡真正防住繞過的是 CI 上把驗收規格檔機械鎖死的 guard，屬同形式的最高性價比案例；而 [[不讀碼時該看哪些圖]] 的第三張「圖」（依賴規則不是圖而是會 fail 的 CI 檢查）正是本節在單一專案上的落地形式。

### ③ 從程式碼反推架構圖：準確度數字比 call graph 樂觀，但那是不同任務

ArchAgent（arXiv 2601.13007，Pan、Mao、Ma、Ling，2026-01-19）在 8 個 production 級 GitHub 專案（1k–22k 原始檔，Go／Java／C-C++／Python／YAML）上做架構恢復評測，以專案官方架構文件為 ground truth 做元素層級比對：**F1 μ=0.966（σ=0.025）對 DeepWiki 的 μ=0.860（σ=0.067）**，paired t-test p=0.0036，effect size 1.62（95% CI [0.045, 0.165]）；另有 30 位五年以上經驗的資深工程師以 within-subjects 平衡設計評估 16 張圖（8 repo × 2 系統）。Ablation 顯示餵入依賴脈絡可提升準確度（Qwen 3 平均 +0.11、p=0.00087；Llama 3 平均 +0.07、p=0.023）（**medium-high**，本頁作者一手 fetch 全文複驗數值）。

⚠️ 兩項不可省的限制：(a) **全文沒有 Limitations 或 Threats to Validity 章節**，對這類論文是明顯的品質缺口；(b) ground truth 是「專案官方架構文件」，也就是在量測「與人寫的文件有多像」，不是與實際執行行為比對。

**與 [[不讀碼時該看哪些圖]] 的既有結論不衝突**：那頁記的 ICSE 2020 中位 recall 0.884 與 ISSTA 2024 平均漏 61% 講的是 **call graph 完整性**（邊層級、健全性），本頁是**架構恢復**（元素層級、與文件的相似度）。任務不同、判準不同，不能互相推翻，也不能用 0.966 去主張「自動產架構圖已經可信」。

## 證據強度總表

| 主張 | 強度與票數 |
|---|---|
| 無產業級調查可回答「哪套框架主流」；流通數字皆為廠商小樣本 | **high，3-0** |
| ECSA 2024：373 份視圖中 96% informal、4% semiformal、0 formal | **medium**（數字 3-0，「代表性」措辭版 1-2 被否決） |
| 「arc42 與 C4 主導實務」引用鏈只到框架作者自家網站與書 | **high，3-0** |
| Grundfos：C4 以 PlantUML 寫入 Markdown、與程式碼同 repo，非專用建模工具 | **high，3-0**（單一公司，作者自陳不可外推） |
| Grundfos 無任何自動化文件—實作一致性檢查，只靠 code review | **high，2-1** |
| Structurizr cli／java／lite 三 repo 已封存，最後 push 2026-02-01 | **high**（本頁 GitHub API 一手複驗，推翻原 0-3 否決） |
| Mermaid C4 為 experimental、仍跑 legacy renderer、多項功能不支援 | **high，3-0** |
| `c4-beta` RFC 原型在審、Simon Brown 參與討論、尚未採納 | **high，3-0** |
| Thoughtworks Radar Vol 34 收錄 architecture drift reduction with LLMs（Assess） | **medium-high**（一手 fetch 摘要，非逐字全文） |
| ArchAgent F1 0.966 vs DeepWiki 0.860 | **medium-high**（一手 fetch 全文複驗；論文無 Limitations 節） |
| IcePanel 2024 的 AI 相關數字是「未來 5 年預期」而非已量測實務 | **high，3-0** |

## 被誤殺的主張（原 0-3 否決，經一手複驗為真）

harness 的對抗查證把「Structurizr 官方工具鏈於 2026 年 2 月封存」整組三條主張以 **0-3 全票否決**，否決理由未隨結果傳回。以 GitHub API 直查 `archived` 欄位複驗（2026-08-10）：

| repo | archived | 最後 push | stars |
|---|---|---|---|
| `structurizr/cli` | `true` | 2026-02-01T14:27:37Z | 567 |
| `structurizr/java` | `true` | 2026-02-01T14:29:40Z | 1,135 |
| `structurizr/lite` | `true` | 2026-02-01T14:25:09Z | 384 |

**封存屬實，全票否決是誤判。** 此案例的方法論意義大於內容：N-0 否決不等於事實為假，核心事實可能被周邊細節（如「使用者被導向 Patreon 資助產品」這類無法複現的敘述）連坐。同輪另一個同型錯誤是最終 summary 宣稱「架構約束用於 AI 產碼在所有一手來源中命中為零」——實際上搜尋階段已抓到 Thoughtworks Radar 與 Codesai 兩個直接命中，只是其 claim 落在 `budgetDropped: 6` 未進驗證階段。**驗證取樣的缺席被寫成了事實的缺席**，這是本輪最需要記住的失效模式。

## 勿引用

- ❌ **IcePanel 2025 版的 AI 使用率數字**（37% 已用於部分工作流／33% 僅探索／19% 尚未探索／44% 使用 AI+DaC）——以此組數字為主體的主張被 **0-3 否決**，但同一批數字又被另一條 3-0 通過主張的查證者主動引用，狀態自相矛盾。使用前必須重讀原文核對，並記得 n=75 且 44% 是「AI/LLMs 與 diagrams-as-code」**合併計數、兩者無法拆開**。
- ❌ **「mermaid 下載量比 PlantUML 高兩個數量級」**——npm 週下載（2026-08-02～08-08）mermaid 13,450,759 對 PlantUML 系列合計約 294,322，實際是 45.7 倍（只取三個主要套件則 74.2 倍），寫「兩個數量級」過寬。更重要的是**這個比值本身不可作為跨工具採用比**：PlantUML 主要發佈通道是 Java jar 與 IDE／伺服器外掛，不在 npm。
- ❌ **「mermaid 下載量 9.5 倍成長證明 AI 帶動 diagram-as-code」**——同期 npm 全站計數本身暴漲（typescript 2.88 倍、react 3.82 倍、連零成長的 lodash 都 2.30 倍）。正規化後 mermaid 專屬成長約 **3–4 倍**，仍顯著但不是 9.5 倍；且相關不等於因果。
- ❌ **「EU AI Act 將驅動架構文件採用轉變」**（0-3 否決）——該主張講的是 AI *系統* 需被文件化，與 AI coding agent 產碼是兩件事，不可混用。

## 本輪未查證

以下為零主張，不得由本頁內容推導：

1. **ArchUnit／fitness function 工具生態的量化指標**（Maven Central 下載、GitHub 依賴數、實測攔截率）——本輪只證明架構文件研究側完全沒提，未從工具側反查。這是「架構約束當 AI 產碼驗收界面」能否從聲量升級為實證的關鍵缺口。
2. **是否存在任何大樣本非廠商調查**曾量測架構圖框架選擇——本輪未檢索到，但也未窮盡（SEI、ThoughtWorks Radar 歷年、IEEE Software 調查等未逐一排查）。
3. **mermaid 下載成長中 direct 與 transitive 的比例**——要把「AI 帶動 DaC」從相關性推向因果，需要能拆解直接依賴與遞移依賴的資料源。
4. **雲廠商官方架構文件採用哪套框架**——本輪只碰到 Azure architecture icons 頁，未做系統性比對。
5. **書籍與會議議程比重**——完全未查。

## 時效性

本頁快照日為 2026-08-10。Structurizr 封存狀態與 Mermaid C4 遷移進度都在移動中（#7842 已於 2026-07-30 併入 develop），任何「截至 2026-06」的敘述兩個月內即已部分過時；引用前建議回查 GitHub 現況。ECSA 2024 的 373 份視圖採自 2023 年的挖掘窗口，早於 agentic coding 普及。C4 的分層哲學本身十年未變，時效風險最低。

## 關聯

- [[不讀碼時該看哪些圖]] — 本頁是它的**現況層**：該頁答「該看哪一層、畫哪三張」（規範性），本頁答「業界實際上在用什麼、有沒有數據支撐」（描述性）。兩頁在同一處交會——該頁第三張「圖」（依賴規則交給 CI）正是本頁 ② 節那條機構級趨勢的單專案落地形式，而本頁證明它目前**只有 Assess 級的機構背書與零量化實證**，該頁把它列為建議做法時應一併知道這個強度。
- [[AI-生成流程圖與架構圖]] — 工具選型層前作。本頁的 ArchAgent 數字補上該頁「無獨立 benchmark」的缺口，但要注意任務不同（架構恢復 vs 流程圖生成）；該頁的 Mermaid 實踐約定已撤銷，工具查證仍有效。
- [[Uncle-Bob-的不讀碼約束閘門]] — 本頁 ② 節「架構約束當驗收界面」的最完整個案實作：那裡的 `dependency-checker` 與 CI 上機械鎖死的 acceptance-boundary-guard 正是 Thoughtworks 條目講的做法，只是出自單人專案而非企業實證。
- [[用測試約束-AI-產碼]] — 同一問題的另一條路線（用測試而非架構規則約束產碼）。本頁的結論「約束型做法目前普遍缺乏量化實證」對該頁同樣適用，而該頁記的 BenchJack 顯示評估管線本身也可能被繞過——兩者疊加意味著「約束住 AI 產碼」在 2026 年仍是設計主張而非已驗證工程實務。
