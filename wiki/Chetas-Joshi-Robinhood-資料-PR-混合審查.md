---
title: Chetas Joshi Robinhood 資料 PR 混合審查
description: Robinhood 資料平台的 data PR 審查分三層：腳本查事實、agent 判風險、人管保護決策；含整場論證、可照做步驟、回查與自報數字強度
created: 2026-11-19
updated: 2026-11-19
source: https://www.ai.engineer/talks/MQiojLnK-E0-60-our-data-prs-now-merge-no
published: 2026-11-10
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - automation
  - evaluation
---

# Chetas Joshi Robinhood 資料 PR 混合審查

來源：AI Engineer 演講〈60% of Our Data PRs Now Merge With No Human Review〉的官方閱讀頁與整場機器逐字稿（約 28 分鐘），落地於 [[AI-Engineer-Joshi-Data-PRs-Merge-No-Human-Review]]；YouTube `MQiojLnK-E0`，2026-11-10 上傳。閱讀頁缺第 05 段（回饋迴圈與加密欄位例），本頁該段依逐字稿整理。逐字稿把 ingestion 辨識成 injection、linter 辨識成 linder，引用時要自行還原。另於 2026-11-19 回查 Robinhood 官方工程部落格、Apache Iceberg 規格、OpenLineage 文件與 GitHub 文件，結果見「回查」一節。

**一句話**：PR 已經能用機器速度開出來，但「這個改動進 production 安不安全」仍要靠少數知道誰在讀這張表的人來判斷。Robinhood 的解法是把審查拆成三種答案、交給三種審查者：能對照權威來源回答是非的事實交給腳本，需要讀程式碼推理的風險交給 agent，少數保護性決策永遠交給人。

## 講者與立場

- Chetas Joshi，Robinhood data platform 團隊工程師，負責資料湖背後的分散式 ingestion 與處理框架（演講自述）。
- **沒有推銷產品**：審查系統是內部自建，演講沒有提到可下載的工具或 repo，也沒點名用了哪個模型、lineage 工具或 table format。可借用的是設計原則，不是軟體。
- 立場偏保守：演講多次限定 agent 的能力邊界（只讀 repo、找不到不等於不存在、某些決策永遠不給 agent），並主動講「哪裡做錯了」。但標題的 60% 是自報成果數字，強度見後文。

## 演講脈絡（依順序）

### 1. 問題：PR 以機器速度湧入，審查仍是人的速度（0:00–3:36）

- 開場情境：一個改 schema 的 PR，CI 全綠、測試過、lint 過，還能不能合？它仍可能讓資料錯過 freshness SLA、弄壞三個團隊外的下游消費者，或讓不該碰到的資料被讀到。
- 範圍限定：只談 **data pipeline 的 PR**，包括 schema 變更、pipeline 程式、設定變更、資料存取授權（grant）。這類 PR 由 data platform 團隊審，所以堆積也堆在他們身上。
- AI coding assistant 讓新 query、schema 變更或授權幾分鐘就能開出 PR。既有的 CI 加人工審查其實有效，抓得到壞程式、低效 query、下游破壞與敏感資料外洩；問題是人工那一半只能用人的速度，而且只能靠某人腦中的 context：誰讀這張表、表多大、資料多敏感。
- **錯配**：PR 數量上升，但懂「什麼能安全進 production」的人數沒變，佇列就排在這幾個人面前。目標因此是做一個跟得上 PR 開立速度的 AI 審查者。

### 2. 總覽：三種職責、三個負責者（3:36–5:12）

- **Layer 1：確定性腳本**。對照權威來源（schema registry、catalog）查事實；檢查失敗就讓 CI 變紅、擋住 PR，沒有討論、不經模型。
- **Layer 2：agent**。它的規則會告訴它 Layer 1 已經檢查了什麼，讓它專注在那些檢查抓不到的風險；它審 PR、打風險分數，然後核准或升級給人。
- **人**：負責只有人該做的決定。
- **合併條件**：檢查通過**且**有一個核准（agent 核准，或升級後由人核准），兩者都要。
- 成本理由：用 AI 做判斷，不用 AI 重新推導腳本查得到的事實。

### 3. 貫穿全場的範例 PR（5:12–6:40）

一個 PR 對資料湖中的一張表做兩件事：

1. 上游來源表多了一欄，PR 讓 ingestion pipeline 把它帶進湖裡。
2. 湖裡既有的一欄從 `INTEGER` 加寬成 `BIGINT`，以容納更大的值。

講者說加寬型別「大概是最安全的 schema 變更」，但只要欄位變了，真正的問題就是「下游誰在讀它」。有些讀者登記在 lineage 工具裡，問題是：那就是全部嗎？

### 4. Layer 1：四個確定性檢查（6:40–10:26）

| 檢查 | 做法 | 範例 PR 結果 |
|---|---|---|
| Data contract | 腳本把 PR 提出的 schema 與 key 和 schema registry 比對 | 新欄位確實存在於上游，通過 |
| Required tags | 每張表要有 owner，PII 要在 catalog 標註；腳本直接查 catalog | 有 owner、PII 已標，通過 |
| Lineage blast radius | 欄位變動時，腳本走過 lineage 工具登記的每個讀這欄的下游 job，檢查會不會壞 | 所有已登記消費者都能處理加寬型別，通過 |
| Performance | CI 在 staging 用 production 量級的 mock 資料跑這個改動，看叢集大小是否夠、能否趕上 freshness SLA | 通過 |

- 關鍵限定：lineage 檢查「對下游的視野，完整度恰好等於登記的紀錄，不多不少」。閱讀頁的說法是：腳本從 lineage 清單出發，不在清單上的 job 對結果毫無貢獻。
- 結論的措辭被刻意限定為「**就腳本看得到的範圍**，這個 PR 是安全的」。畫面上每一項都是對「已登記的圖像」的陳述。

### 5. Layer 2：agent 怎麼讀 PR（10:26–12:00）

- **從 diff 開始**。PR 描述與 commit message 說明作者意圖，但「意圖不能解釋掉真實的發現」：描述說安全、程式碼說不安全時，以程式碼為準。
- **工具只有 repo 檔案工具**：列檔、搜尋、讀檔，可以追出 diff 之外的 pipeline 定義與 access grant。**不能**查 live catalog、lineage 工具或 production 狀態；live 事實仍是 Layer 1 的事。
- **規則依變更類型設定**，而且知道 Layer 1 已經涵蓋什麼。規則瞄準三類：query 反模式、敏感資料存取、lineage 以外的消費者。例子：
  - 沒有 partition 的 cross join 結果可能正確，但會把叢集打爆。
  - 一個看起來普通的 grant 可能開放敏感資料。
  - schema 變更時，agent 走過 repo 裡的 pipeline 定義與 access grant，找沒登記的消費者。講者形容這是「人本來要手動做的繁瑣搜尋」。

### 6. agent 找到 lineage 沒登記的 job（12:00–14:31）

- repo 裡有一個 job 讀這個被加寬的欄位，但從沒登記進 lineage，所以 Layer 1 看不到它。它把值寫進另一張表，而那張表的對應欄位仍是 `INTEGER`。
- 推演：原本範圍內的值照常寫得進去；第一個需要更大範圍的值抵達時，那次寫入就會失敗。一個合法的 schema 變更、CI 全綠、通過所有已登記的檢查，下游 job 仍會壞。
- agent 在 review comment 把整條鏈寫出來：從被改的欄位、經過那個 job、到會失敗的寫入。
- **為什麼 lineage 會漏**：工作負載跑在不同 query engine 上，每個 engine 要各自發布 lineage；某個 engine 沒發布，那段關係就不存在於圖上。沒有一個 catalog 能自動看到一切。
- **code walk 的極限**（講者強調不要誇大）：repo 搜尋只看得到 repo 裡的東西。手動跑的 ad hoc query、在 codebase 外定義的 dashboard，對 repo 搜尋完全不可見。所以 agent 被要求「誠實面對這個極限」：找不到時不准說「沒有下游消費者」，只能說「在我搜過的這些地方沒找到」。**沒找到不等於不存在**，agent 永遠不能宣稱「全部安全」。

### 7. agent 的產出與這個 PR 的結局（14:31–16:38）

agent 產出的形狀跟好的人類 reviewer 一樣：

1. **逐行 review comment 附理由**：不是「看起來有風險」，而是「這行改了這個欄位，而這個 job 讀它」。
2. **風險分數**：發現的問題多嚴重，決定下一步。
3. **決定**：沒有嚴重風險可以核准；有需要人的風險就升級，comment 與理由一起交給人，讓人從調查開始而不是從零開始。

範例 PR 的結局：agent 把下游寫入評為高風險並升級。人做了 agent 做不到的事：確認那個 job 在 production 真的在跑。這不是理論風險。修正方式是**調整順序**而不是拒絕改動：先把下游表的欄位加寬，原 PR 才合併部署，沒有事故。

### 8. 永遠交給人的三類決定（16:38–17:39）

多數改動在檢查通過、agent 對判決有信心時，由 agent 自己核准。但以下三類，agent 無論多有信心都不能核准，只能提出風險與理由：

1. **觸及敏感資料的 grant**：誰能碰敏感資料，每次都要人決定。
2. **看起來改變意圖的 migration**：改的是資料「代表什麼」，而不只是怎麼搬、怎麼存。
3. **agent 自己沒信心的判決**：沒有找到具體問題，不代表可以「四捨五入成核准」。

### 9. 回饋迴圈與加密欄位例（17:39–20:11，閱讀頁缺此段）

- 流程：agent 的判決與理由寫在 review comment；人回覆同意或不同意，**並說明原因**。講者強調原因才讓回饋有用，否則只是投票。回覆每天收集；每週由 on-call 讀回饋、**手動**更新 review 規則。
- 講者明說這是手動的：沒有東西自動重訓，也沒有規則自動改。有個想法是讓事故調查 agent 協助每週這一輪，但**尚未實作**。沒有回饋，每次改規則都只是猜。
- **加密欄位例**（另一個 PR）：某欄在來源資料庫標為個資，但 ingestion pipeline 在寫入資料湖前已經加密，所以 PR 提議在湖裡標為非敏感。agent 依上游標籤判斷這不對而標記；作者反駁，請 agent 參考其他表上類似欄位怎麼分類，而不只看上游標籤；人同意作者。這種糾正可以讓下次類似欄位不再被不必要地升級。
- 講者的限定：這只因為**該 pipeline 在寫入前加密**才成立，不是「加密就一律非敏感」。

### 10. 怎麼衡量：二乘二矩陣（20:11–22:34）

- 把 agent 的決定與 PR 實際需要的決定交叉：好 PR 被核准、壞 PR 被升級是正確；壞 PR 被核准是 **miss**（危險，改動會上線）；好 PR 被升級是 **false escalation**（花人的時間）。
- 一個全部升級的閘門可以沒有 miss，但審查負擔一點都沒減。
- 截至 2026-08-31：miss rate 約 2%（**未說明分母**），多數來自規則缺口，而不是判斷失誤。false escalation 沒有一個乾淨的單一數字，主要原因是缺 context，如加密欄位例。總結：「miss 給我們新規則，false escalation 告訴我們 reviewer 缺什麼 context。」
- **一個 miss 的實例**：一份資料有開放副本，下游有 job 從開放副本讀某些欄。隱私團隊把這些欄重新標為個資後，欄位移到受限副本、從開放副本消失。重新標記本身合理，PR 被核准合併，下游 job 讀不到欄位就壞了。講者定性為「規則缺口，不是判斷失敗」。
- 補上的規則有明確觸發條件與搜尋目標：**欄位被重新標為敏感時，搜尋 codebase 中仍從即將失去該欄的那份副本讀它的程式**。這樣即使隱私分類正確，也能抓到會壞的讀取。

### 11. 結果（22:34–24:20）

截至 2026-08-31（全部自報）：

- 約 60% 的 data pipeline PR 不經人審合併。
- 人工審查工作量約少 75%，約每月省 132 個工程師小時。講者把原因歸給 agent 的具體 comment 與理由讓人審得更聚焦：範例 PR 被升級後，工程師可以直接去確認某個 consumer 是否在跑。
- 與這些 PR 相關的事故約少 30%。閱讀頁特別限定：這描述的是混合審查上線後的團隊經驗，**包括**負責保護性決策與調查升級的工程師。
- 講者強調這不是「沒有人的審查」：保護性決策照設計仍到人手上，目標是減少審查工作，不是移除問責。

### 12. 做錯的架構與提案（24:20–26:10）

**現行架構的問題**：

- Layer 1 與 Layer 2 是兩個獨立觸發、平行執行的系統，各自產出結果。當初看似理所當然，但兩邊都看不到對方的通過、失敗或故障狀態。
- agent 知道腳本**被設定**要檢查什麼，卻不知道這次**跑出來**的結果。
- agent 不能呼叫 Layer 1 檢查。調查中遇到需要 production live 事實的問題時，它無法自己取得。
- 合併仍要求檢查通過加核准，但沒有一個系統掌握完整的執行期全貌。任一邊跑不完就等人，**沒有自動 fallback**。

**提案（尚未建置）**：單一入口。先由分類器看整個 PR，決定哪些改動要一起審、哪些分開審，是整個 PR 層級的決定，不是逐檔獨立路由。agent 也會拿到可呼叫的確定性檢查，與 repo 工具並列，需要 live 事實時可以請求對應檢查。講者明說這是方向不是成果，回報的節省全部來自現行的平行系統。

### 13. 三條帶走的教訓（26:10–28:00）

1. **確定性評估**：能對權威來源證明的，就讓腳本證明，不要在是非題上花判斷。腳本證明的每一件事都是不需要 AI 的審查工作，成本也因此壓低。
2. **只標記、不放行**：不是對每個 PR，而是對真正讓人害怕的改動（敏感 grant、migration 意圖、低信心判決），agent 的工作止於提出風險與理由，決定每次都歸人。
3. **計算 false escalation**：全部升級的閘門沒替任何人省時間，只是把工作搬來搬去。要像衡量 miss 一樣衡量它的成本。

收尾：「Who reviews the bots?」腳本管權威來源能證明的一切，agent 管需要 context 與判斷的一切，人管只有人能做的決定。

## 搬到個人 Claude Code／Codex 工作流程

個人或小團隊通常沒有 schema registry、catalog 與 lineage 工具，也不會有「agent 核准就合併」的審查門。能直接搬的是分工方式與幾條紀律：

1. **先列出「是非題」，做成會擋的檢查**。把專案裡「對照某個權威來源就能回答」的問題列出來，例如 migration 是否有對應 rollback、新欄位是否在 model／DTO 定義裡、權限設定檔是否只改了允許的範圍。能寫成腳本的就放進 CI 或 pre-commit，失敗即擋；不要叫 review agent 每次重新推導。
2. **review 提示裡寫明「這些已有檢查」**。在給 review subagent 或 `code-review` 類 skill 的指示中列出 CI 已涵蓋的項目，請它專注在檢查抓不到的地方。這是 Robinhood 讓 agent 不重複 Layer 1 工作的做法，也能少花 token。
3. **依變更類型給搜尋目標**。例如「改欄位型別或欄位名稱時：搜尋 repo 中所有讀寫這個欄位的 job、query、export 與其他表」「改權限設定時：列出新增的可存取者」。改 DB 欄位型別這類情境可以直接要求 agent 回報下游寫入端的欄位型別，抓「上游加寬、下游仍窄」。
4. **要求報告搜過哪裡**。在 review 指示中加一條：找不到消費者時，只能寫「在 X、Y、Z 沒找到」，不能寫「沒有消費者」。並請它列出 repo 外可能的讀者（排程 SQL、BI dashboard、其他 repo），交給你自己確認。
5. **保護性類別寫成固定規則，不靠 agent 自評**。在 `AGENTS.md`／`CLAUDE.md` 或 review skill 中列出永遠要你親自看的類別：權限與敏感資料、改變資料語意的 migration、agent 自認沒把握的判決。agent 對這些只寫風險與理由，不給「可以合」的結論。
6. **發現下游風險時改順序，不只是退回**。先改下游（加寬目的欄位、更新讀者），再合上游。
7. **把每次不同意寫下原因，定期改規則**。不同意 review 結論時，回覆要附原因。累積幾次後（例如每週）手動整理成 review 規則；漏抓的案例改寫成「觸發條件＋搜尋目標」格式的新規則。能進一步變成腳本的，按第 1 步移到確定性層。
8. **記兩種錯**。簡單記一份清單：agent 放過但其實有問題的（miss）、agent 擋下但其實沒事的（false escalation）。後者太多時，表示 review 指示缺 context，而不是要再加嚴。

**不能直接搬的部分**：

- **60% 自動合併**依賴 Layer 1 的權威資料源與一整個團隊的回饋迴圈；沒有這些前提，讓 agent 核准合併等於只剩 Layer 2，缺少它刻意倚賴的確定性底線。
- **讓 bot 核准滿足 GitHub 必要審查**：GitHub 有「Allow GitHub Actions to create and approve pull requests」設定，個人帳號 repo 預設不允許；文件沒有說明這類核准是否計入 branch protection 的必要核准數（2026-11-19 查 [GitHub Docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)）。不確定，要用之前自己實測。
- **lineage 檢查**：個人專案多半沒有 lineage 工具，第 3 步的 repo 搜尋是唯一可用的替代，而且同樣看不到 repo 外的讀者。

## 回查（2026-11-19）

| 說法 | 回查結果 | 判定 |
|---|---|---|
| Robinhood 用確定性檢查加 AI 審 PR | Robinhood 官方部落格〈[Automating Database Safety](https://robinhood.com/us/en/careers/blog/automating-database-safety-building-a-security-first-ai-for-storage-operations/)〉（2026-07-27，Storage 團隊）描述另一套 Storage PR Agent：審 Postgres schema migration PR，LLM 解析 diff、經 MCP 取表統計、寫風險摘要，但「agent never decides whether a schema migration is safe」，由 fail-closed 的確定性檢查器決定，證不了安全就交給 Storage 工程師 | **同公司有一手佐證的類似設計，但不是同一套系統**；該文沒提 data pipeline PR、lineage 或 Joshi。值得注意的是兩套的放權不同，見「張力」 |
| 加寬 `INTEGER`→`BIGINT` 是安全的 schema 變更 | [Apache Iceberg 規格](https://iceberg.apache.org/spec/)把 `int`→`long` 列為各版本都允許的型別提升；另限定若該欄是 partition 來源且 transform 結果會變則不允許 | **就 table format 層級成立**。但演講沒說用哪個 table format；規格管的是表本身，不管下游把值複製到另一張窄欄位表，那正是本場的重點 |
| 每個 query engine 要各自發布 lineage | [OpenLineage 文件](https://openlineage.io/docs/)以各系統的 integration（Airflow、Spark、Flink、Hive、dbt 等）發送事件，沒有 integration 的系統就沒有事件 | **與業界常見做法一致**；Robinhood 用的 lineage 工具未公開，無法確認細節 |
| Robinhood 工程師大量由 AI 寫、審程式 | 只找到二手報導（[Complete AI Training](https://completeaitraining.com/news/robinhood-ceo-says-ai-agents-now-write-and-review-most-of/)，2026-08-24）轉述執行長 Vlad Tenev 在 podcast 的說法：工程師 AI 採用率接近 100%、改為監督 agent 寫與審 | **二手、未找到原始節目**，只當背景，勿引用為數據 |
| 60%、2%、75%、132 小時、30% | 除演講與閱讀頁外，找到的都是轉述本場的第三方摘要（StartupHub、TeamDay、個人部落格），沒有獨立來源 | **只有講者自報** |
| 可下載的工具或 repo | 演講未提任何開源工具 | 無可核對 |

## 證據強度與限制

- **所有數字都是自報、單一團隊、無對照組**：60% 不經人審合併、約 2% miss、約 75% 審查工作量下降、約每月 132 小時、事故約少 30%，截至 2026-08-31。沒有給 PR 總數、統計期間或導入前基線。
- **2% miss rate 未說明分母**（閱讀頁明寫）：是佔所有 PR、佔 agent 核准的 PR，還是佔有問題的 PR，不知道。而 miss 多半要等東西壞了才被發現，觀察期內沒壞的 miss 不會被算到，實際值可能偏低。
- **false escalation 沒有數字**：講者自己說沒有乾淨的單一數字。所以「第三條教訓：計算 false escalation」在他們自己的系統裡也還沒做到量化。
- **事故少 30% 不能歸因給 agent**：閱讀頁限定這是混合系統（含人）上線後的整體經驗，沒有對照。
- **132 小時是推估性質**：怎麼量「人工審查工作量」沒有說明。
- **範例 PR 是挑過的成功案例**；兩個反例（加密欄位、重新標記為個資）是講者主動揭露的，屬於比較可信的部分。
- **提案的單一入口架構尚未建置**，沒有任何成果數字，勿引用為已驗證做法。
- 演講沒有揭露模型、提示或規則全文，無法重現。

## 張力與互補

- **同公司內的對照**：Robinhood Storage 團隊的 PR Agent（見上表）規定 agent **從不**決定 migration 是否安全，由 fail-closed 的確定性檢查器把關；data platform 團隊則讓 agent 在一般改動上可以直接核准。兩邊一致的是「保護性決策歸人或歸確定性檢查」，差別在 agent 可放行的範圍。這也呼應 Joshi 的第二類保護決策（改變語意的 migration 一律歸人）。
- **與 [[Lauren-Tan-把糾正寫進程式庫]]：糾正落在哪一層**。Tan 主張每次糾正都盡量變成確定性檢查，散文規則最弱。Robinhood 的事實檢查確實在確定性層，但從回饋學到的東西（加密欄位例、重新標記規則）是每週手動寫進給 agent 的 review 規則，屬於較軟的散文層。「欄位重新標為敏感時搜尋舊副本的讀者」這條，按 Tan 的順序其實有機會改寫成腳本（比對 grant 變更與 repo 內的引用）。
- **與 [[Claude-Code-放手運行的安全與驗證]]：自動合併的條件**。該頁整理的 Hallie 做法是 auto-merge 只開給低風險類別、且 repo 要有 required checks，判準是「錯一次收得回來嗎」。Robinhood 的保護類別（敏感授權、改語意的 migration）正好是收不回或代價高的那類，兩者方向一致；Robinhood 多了「低信心判決也歸人」。
- **與 [[Meta-值班團隊-給每個輪替一個-AI-隊友]]：放權粒度不同**。Meta 以單一行動為單位，靠累積紀錄逐項升級自主；Robinhood 的保護類別是固定的，不因 agent 表現好而開放。兩者都把糾正累積成團隊共用知識，但 Meta 落在團隊記憶，Robinhood 落在 review 規則。
- **與 [[AI-產碼加速下的-review-瓶頸]]：risk tiering 的具體案例**。該頁引用 Thoughtworks 報告「code review 正被拆成依風險分級的路徑」，Robinhood 是一個實作案例。但該頁也提醒先確認 review 真的是約束點；Robinhood 只描述佇列堆在少數有 context 的人面前，沒有提供佇列或部署等待的量測，是否為約束點只能信講者。
- **與 [[Stephen-Chin-與-Cassandra-Chin-PR-描述要附證據包]]：互補**。Chin 把「誰改了什麼、測試跑在哪版」先用確定性程式算好再交給 writer；Robinhood 讓 agent 的 comment 寫出完整依賴鏈，讓升級後的人能從調查開始。兩者都在減少人重建脈絡的成本。
- **與 [[Matt-Pocock-的-PR-瓶頸解法]]：誰來標風險**。該頁指出寫 PR 的 agent 自己填 blast radius 容易標錯，宜用規則強制。Robinhood 的保護類別就是用規則強制，不靠作者或 agent 自評。
- 同場綜合：[[AI-Engineer-2026-演講精華-AI-工作流程]] 在自動合併與改進迴圈兩節引用了本場的摘要。
