---
title: Girish Konda 把 sub-agent 當分散式系統
description: 深讀 Girish Konda 演講：以分散式系統失效模型看 sub-agent 交接，整理 SAFE handoffs、Pacemaker 回查與可照做步驟
created: 2026-11-19
updated: 2026-11-19
source: https://ai.engineer/talks/DxP5aW4VknQ-your-sub-agents-are-distributed-system-treat
published: 2026-11-10
parent: "[[wiki/01.index]]"
tags:
  - ai-agent
  - agent-framework
  - coding-agent
  - mcp
---

# Girish Konda 把 sub-agent 當分散式系統

> **一句話主張**：orchestrator 把工作分給多個 sub-agent，就是在蓋一個分散式系統（併發 worker、共享可變狀態、對外有副作用、結果合併）。分散式系統的老問題（部分失敗、逾時無法判讀、dirty read、無界 fan-out、重試造成重複寫入）全都會出現，只是介面被包成「傳入字串、回傳字串」而看不見。解法是把交接當網路呼叫，回傳**具名狀態**而非純文字，並由**程式碼**而非 prompt 強制檢查。

原始資料：`raw/fetched/AI-Engineer-Konda-Sub-Agents-Are-a-Distributed-System.md`（官方閱讀頁＋完整機器逐字稿，YouTube `DxP5aW4VknQ`，約 23 分鐘）。

## 講者與立場

- Girish Konda，Microsoft principal software engineer；開場聲明觀點僅代表個人、不代表雇主。
- 業餘維護開源 [MCP Pacemaker](https://github.com/girishkvs/mcp-pacemaker)：本地 bridge，負責讓 MCP server 在編輯器重啟、重開機、token 過期後持續運作（MIT 授權）。演講的實例幾乎都出自這個專案，加上他自己的 IETF Internet-Draft 和其他演講。
- **推銷成分**：沒有推 Microsoft 產品，但所有實例都來自他自己的開源專案、文章和個人草案，SAFE 模型也是他自己提的。他明說「這是我自己用的模型，不是通用模型」。
- 素材來源：過去一年在實際工程工作（開發 session、code review、事件分流 incident triage）裡使用 agent 和 sub-agent 的經驗。

## 論證脈絡（依演講順序）

### 1. 架構本身就是分散式系統（0:00–3:08）

- 架構：orchestrator 切任務交給三個 sub-agent，**同時跑**、讀**同一份共享狀態**（memory 檔、repo working tree、issue、vector store），並透過 tool call 碰真實系統（資料庫、API、CI、部署管線），最後由 orchestrator 合併成一個答案。
- 他的判斷：orchestrator＋worker＋共享可變狀態＋併發執行結果合併，就是典型分散式系統。工具卻只給你一個「string in, string out」的函式，把所有該決定的事都丟回呼叫端。
- 他列出四種「不新、也不是 agent 特有」的經典失效，以及在 agent 裡的樣子：
  | 經典失效 | 一般系統 | sub-agent 版本 |
  |---|---|---|
  | 部分失敗 | 做到一半回傳例外或錯誤碼 | 做到一半，回傳**看起來像成功**的文字 |
  | dirty read | 有隔離層級與版本 | 每個 worker 讀同一份共享 context，包括別的 worker 只是**猜**的內容 |
  | 無界 fan-out | 忙碌的服務用 429／503 推回 | orchestrator 看不到推回，照樣起下一個 worker |
  | 重試 | 用冪等性讓重試可靠 | 重跑 sub-agent 等於整個任務重跑，**副作用一起重來** |

### 2. 失效模型：最難處理的是「流暢但錯」（3:08–4:54）

- 由易到難：crash-stop（停了就不動，最好處理；sub-agent 拋錯屬此類）→ 沒回應（遺失或很晚）→ 類似 Byzantine 的情況（有回答但答案錯）。
- 做到一半的 sub-agent 最接近最後一類：沒有惡意，但從外面看一樣，它不 crash、答得很流暢，且與成功用**同一個型別簽章**回傳。
- 例子（他自己說是先前演講用的示意）：讓 agent 分類告警，三條路徑得出同樣的「benign」、同樣的信心水準：
  1. 真的拉了 telemetry 並與基準比較；
  2. 認出看過的告警標題，直接套舊答案；
  3. 什麼都沒查，直接生成答案。
- 重點：orchestrator 讀得到**結論**，讀不到**背後做了多少工**。就算把信心值一併保留也救不回來。下一步決策可能正取決於「有沒有人看過**這則**告警的 telemetry」。

### 3. 逾時只是懷疑，不是事實（4:54–7:28）

- timeout 觸發時，orchestrator 只知道等了多久。三種情況看起來一樣：sub-agent 還在跑、它 crash 了、它做完了但回覆遺失。
- 理論依據：FLP（1985）說在非同步系統中只要有一個程序可能失敗，共識就可能無法完成；Chandra & Toueg（1996）的答案是**會出錯的失效偵測器**，只能「懷疑」。（逐字稿把 asynchronous 辨識成 a synchronous，閱讀頁正確。）他強調這是理論極限，不是工具缺口。
- Pacemaker 的兩個方向相反的實例：
  - **慢不是死**：第一次執行會自我下載的 server 撞上一般的 30 秒呼叫 timeout，看起來壞掉了。修法：給 `initialize` 自己的 timeout。
  - **死被誤記成慢**：server 在呼叫中途 crash，呼叫後來逾時，timeout 記錄**覆寫**了說明 crash 原因的 exit code。修法：只有 server 還活著時才記 timeout，已退出就保留更有資訊的原因。
- 結論：**timeout 記成 `unknown`，並保留真正原因**。
- **把失敗變成值**：sub-agent 回傳 status、做了什麼、沒做什麼、證據、副作用。`partial` 是正常結果。
- 協議已經有位置：A2A 的 task 可以 completed／failed／canceled／rejected，或停下來要輸入；MCP tool result 可以設 `isError: true`。但 sub-agent 仍可能標 completed 而文字內容說的是別的；**只讀文字的迴圈看不到這個差異**，orchestrator 必須讀這些訊號。
- 另一個切分（出自他的個人 Internet-Draft）：「檢查了、結果是否」和「根本無法檢查」是不同事實。混為一談會改變什麼被重試、誰被 page、事後稽核說查過什麼。

### 4. Dirty read：一個猜測變成三份一致的產出（7:28–9:09）

- 示意例子（他說是編的）：負責分流的 worker 在共享 context 寫下「錯誤率降了 80%」，那是**推論**而非量測。第二個 worker 寫 review 記錄時引用這句；第三個寫 runbook 步驟時拿它當繼續的理由。orchestrator 合併三份產出，三份一致，但其實是**同一句無根據的話被讀了三次**。
- 類比：1995 年對 SQL 隔離層級的批判文獻把 dirty read 定義為「在寫入方 commit 或 rollback 前讀到值」。共享 context 裡，猜測一寫下就可讀，且沒有任何標記說它未經檢查。
- 常見修法「問三個 sub-agent 取 quorum」為什麼沒用：weighted voting（1979）的 quorum 有效，是因為讀 quorum 權重＋寫 quorum 權重大於總權重，強迫每次讀都與最新的寫重疊——**重疊才是保證**。三個讀同一份共享 context 的 sub-agent 不是獨立副本，它們的一致是一個來源被數了三次。

### 5. 選一個一致性模型（9:09–11:35）

- 資料庫已有詞彙：linearizable（每個操作看似在真實時間某一點發生）、sequential（一個尊重各程序自身順序的全序）、causal（因果相關的操作在各處順序一致）、session guarantees（對單一 client 的承諾，如 read-your-writes、monotonic reads）、eventual（停止更新後最終收斂）。**共享 context 一個都沒承諾**。
- 不需要最強的：最強的模型在網路分割時無法保持可用；causal 和 session guarantees 只要 client 黏在同一處就能保持可用。對 sub-agent 來說，那個「同一處」就是 orchestrator。
- 由此提出 **SAFE handoffs**（他自己的模型，來源是 Pacemaker、其他文章與 Internet-Draft）：
  - **S — Source reads**：worker 傳遞的每個事實都帶來源、版本、as-of 時間、revision；決策只用夠新的來源事實。
  - **A — At-most-once effects**：每個寫入有 identity 和**針對該動作的一次性核准**；結果靠 read back 確認，**絕不 replay**。
  - **F — Fan-out budgets**：每個下游依賴有 gate 和有上限的等待；被拒絕算失敗。
  - **E — Explicit outcomes**：每次交接以具名狀態結束；timeout 是 `unknown`，原因保留。

### 6. S：在決策時檢查來源（11:35–13:09）

- 把事實當**紀錄**而非句子。Lamport（1978）定義事件的 happened-before；一個事實的 provenance 就是它從哪讀、何時讀。
- 紀錄欄位：claim 與其 revision、來源與其版本、適用 scope，以及**三個時間**（單一 timestamp 會混在一起）：資料截至何時、何時讀取、何時被決策使用。
- 示意數字：資料截至 9:05，9:06 讀取，9:07 決策；選定的新鮮度上限是 5 分鐘，資料在決策時 2 分鐘舊，可用。到 9:15 同一份資料 10 分鐘舊，orchestrator 拒絕這筆 stale 紀錄，要求下一次決策前重讀。
- 把 claim 抄進新筆記**不會**推進資料的截至時間。
- 這條要求同時區分了觀察和推論：觀察有來源與讀取時間，推論沒有。80% 那句話的寫入者交不出這兩項。

### 7. A：靠 identity 回收寫入（13:09–16:43）

- 情境：sub-agent 呼叫工具建立 PR，寫入成功但回覆遺失。orchestrator 只知道結果 `unknown`；若把整個任務再委派一次，worker 會再走到建立步驟，第一個 PR 可能早就存在。
- RPC（1984）的語意：正常回傳代表程序恰好執行一次；拿到例外則是執行一次或零次，而且不會告訴你哪個。所以要選投遞語意：
  - at-most-once：不重試，接受可能遺失；
  - at-least-once：重試，接受可能重複；
  - 「exactly once」：至少執行一次，**加上**接收端能辨識重複（例如 idempotency key）。
- MCP 的 idempotent hint 只是 hint、預設 false；**需要冪等就自己做**。
- Pacemaker 的設計：client 重啟回來時，bridge 會對新的 server 重播該 client 記錄下來的 `initialize`。這是安全的，因為只是握手，不還原工具狀態。但它**絕不重播不確定的 tool call**：回收共用 server 時先 drain，到期還沒回應的呼叫標為「可能已執行」，叫呼叫端自己去查。
- SAFE 做法：每個副作用有 identity，核准綁定該動作、只能用一次；呼叫後用 identity read back。**submitted 不等於 confirmed**；confirmed 是你觀察到效果（例如真的看到那個 PR 存在）。
- 暫停與恢復：lease 是有逾時的鎖。Kleppmann 談分散式鎖的文章描述：client 持鎖時暫停、lease 過期、別人接手，第一個 client 醒來照寫。修法是 fencing token：每次授鎖遞增，storage 記住看過的最大值，拒絕帶舊 token 的寫入。
- 套到 agent：sub-agent 經常暫停與恢復。他的說法是「restore context, not side effects」，把核准當 fencing token：一個動作、用一次，**在 gate 檢查，不是記在 prompt 或對話裡**。Pacemaker 修過同類 bug：過期的 exit 或已刪除的 resume 不能再移除或復活取代它的 session。

### 8. F：在共用資源處做併發預算（16:43–18:42）

- Pacemaker 在加上冷啟動限制前，許多 session 同時透過 `npx` 啟動 server，共用一個套件快取，**全部**以 npm 的 lock compromised 錯誤失敗。單一請求都沒錯，失敗來自併發本身。
- 下游推回也可能只是一句純文字：MCP 規格的 tool 執行錯誤範例就是把 rate limit 寫成一句話。模型讀到了，orchestrator 的程式碼可能從沒看，下一個 worker 照樣啟動。
- Pacemaker 的兩種准入政策，到期行為刻意不同：
  - **套件管理器冷啟動**：預設一次放 2 個，其他人最多等 15 秒；超過就**不經 gate 直接啟動**。他寫明理由：快取損毀是「風險」，卡住的 client 請求是「必然」，這是刻意選擇可用性並記錄下來。
  - **session 上限**：到上限時新 session 最多等 10 秒，仍無空位就拒絕，拒絕在健康回報中**算失敗**。
- check-then-act race：容量必須在非同步啟動**之前**預留，否則排隊中的多個啟動各自看到「還有位子」、啟動完才登記，就會超賣上限。
- 套到 sub-agent：每個下游給 orchestrator 一個數字、一個有上限的等待、以及被拒絕時的處理。

### 9. E：讓程式碼決定 claim 是否通過（18:42–20:01）

- 每次交接以具名狀態結束（如 `stale`、`unknown`），不是只有文字。
- 關鍵是**誰決定這個狀態**：worker 提議狀態和提議結論一樣容易。所以把 agent 輸出當不可信輸入，像處理來自網際網路的 request body：orchestrator 用**程式碼**檢查 schema 是否相符、證據在不在、夠不夠新、數字重算是否成立。
- 檢查失敗就回傳**帶理由的拒絕**，不是把文字往下傳再附一段警告（警告很容易在下一個 worker 的輸入裡被忽略）。
- 他的一句話：如果同一個模型能跳過檢查然後宣布通過，那是 request，不是 boundary。
- 示意例子：sub-agent 說錯誤率下降。之前 1,000 個請求 10 個錯，之後 600 個請求 6 個錯。錯誤數從 10 降到 6，但重算比率都是 1%：數量跟著流量降，比率沒變。重算後拒絕這個 claim。可以接受的結果是「兩期比率都是 1%」的有根據結論，或刻意交給人決定；**有信心的猜測不行**。

### 10. 限制、代價與適用範圍（20:01–22:00）

SAFE **不做**的事：

- 不讓事實變真：有來源的事實是「可檢查」，不是「正確」。
- 不給 exactly-once：回覆遺失時，在 read back 前仍是 `unknown`；at-most-once 也允許零次執行。
- 不 rollback：多步驟任務在失敗前已改變外部狀態時，撤銷要靠針對該動作設計的補償步驟，如 Sagas（1987）。
- 沒有跨 worker 的全域順序，只有每個事實的因果歷史。

代價：

- CAP：網路分割時在可用性與一致性間取捨。Pacemaker 的冷啟動刻意選可用性；SAFE 對寫入選一致性，**寧可拒絕也不猜**。
- PACELC：即使沒故障，也是用延遲換一致性。每次新鮮度檢查都是多一次讀取；**每個拒絕都需要有人負責後續**。

不適用：

- sub-agent 只起草文字、人讀過才會發生任何事：大部分機制是額外負擔。
- 多個 orchestrator 或 peer agent：沒有單一處可以黏住，需要別的協調方式。

### 11. 三個結論（22:00–）

1. 把每次交給 sub-agent 都當網路呼叫：可能做到一半失敗、可能很慢、可能回來兩次。
2. 回傳狀態，不只是文字。結果若無法表達 `partial`、`stale`、`unknown`，orchestrator 就會讀成「完成」。
3. 從 SAFE 開始並**在程式碼裡強制執行**；合用的留、不合用的改。「我們早就知道怎麼建分散式系統，只是要注意到自己正在建一個。」

閱讀頁的收尾提問很實用：你的 orchestrator 程式碼在 worker 回傳 `partial`、`stale`、`unknown` 時分別會做什麼？三者對應不同下一步：檢查剩下沒做的、重新取證據、查寫入是否已發生。

## 搬到個人 Claude Code／Codex 工作流程

前提判斷：Konda 自己說「只起草文字、人看過才動」的情境，SAFE 大多是負擔。個人日常用 sub-agent 做搜尋、審查、起草，主 agent 和你都會讀結果，**不必全套**。值得搬的是下面幾件成本低的事；只有 sub-agent 會碰外部狀態（開 PR、push、改 issue、寫共享檔）時才加 A 和 F。

**1. 讓 sub-agent 交回具名狀態（E，成本最低、最該做）**

Claude Code sub-agent 回到主對話的是最後一則**文字**報告，官方文件沒有描述結構化輸出欄位（[sub-agents 文件](https://code.claude.com/docs/en/sub-agents)）。所以要在委派 prompt 裡規定結尾格式，例如：

```
最後輸出一段 JSON：
{"status": "done|partial|stale|unknown|refused",
 "done": [...], "not_done": [...],
 "evidence": [{"claim": "...", "source": "檔案路徑/URL/指令", "read_at": "...", "observed_or_inferred": "observed|inferred"}],
 "side_effects": [{"action": "...", "target": "...", "confirmed_by": "read back 的指令與結果，沒有就寫 null"}]}
```

主 agent 收到後先看 `status` 和 `not_done`，不要只讀摘要文字。若你用腳本或 SDK 編排，能用 schema 驗證輸出就用，讓「格式不符」成為硬失敗。

**2. 區分觀察與推論（S 的輕量版）**

要求每條結論標 `observed`（有檔案／指令／URL 可回查）或 `inferred`。主 agent 對 `inferred` 的結論不往下游傳成事實；要用就先自己查。數字類 claim（「降了 X%」「快了 N 倍」）一律要分子分母，讓主 agent 能重算——Konda 的 10/1000 對 6/600 例子就是這類。

**3. 平行 sub-agent 不要共寫一份草稿當彼此的依據**

讓多個 sub-agent 共用一份筆記檔來交換發現，就是 dirty read 的溫床。改成各自回報給主 agent，由主 agent 合併並追溯每條結論的來源；幾個 sub-agent 結論一致時，先確認它們是否讀了同一份來源，**不要把一致當獨立佐證**。

**4. 會寫外部狀態的步驟：給 identity，重試前先 read back（A）**

- 以「能查回來的名字」當 identity，例如固定的 branch 名稱。建 PR 前先 `gh pr list --head <branch>`，已有就不建。
- sub-agent 逾時或被中斷後，**不要整個任務重新委派**；新的委派第一步是查「上次那個寫入是否已發生」。
- Claude Code 的 Agent 工具在被 rate limit、過載或伺服器錯誤中斷時，會回傳已產生的部分輸出並註明被切斷（同上官方文件）。這正是 `partial`／`unknown` 的情境，主 agent 應依此判斷，而不是當成完成。
- 不可逆動作（push、merge、刪除）留在主 agent 或人手上，不交給 sub-agent。這與 [[Claude-Code-放手運行的安全與驗證]] 用 deny 擋不可逆操作的做法互補：deny 擋的是「能不能做」，A 管的是「做了沒、會不會做兩次」。

**5. fan-out 預算（F）**

- Claude Code 有同時執行 sub-agent 的預設上限，可用環境變數調整（官方文件）。若 sub-agent 都會冷啟動 `npx`／`uvx` 類 MCP server，同時開太多可能重演 Pacemaker 的 lock compromised；這時把平行數壓低，或分批派。
- 讀到 rate limit（429、503 或 MCP `isError` 內的「rate limit exceeded」文字）時，主 agent 應降低後續派工，不是繼續派。

**6. 檢查放在程式碼或 hook，不放 prompt（E 的強制部分）**

個人工作流程裡「程式碼檢查」的落點：編排腳本的輸出驗證，或 Claude Code 的 `SubagentStop` hook（sub-agent 結束時觸發，官方文件）。prompt 裡寫「請確實檢查」屬於 Konda 說的「request，不是 boundary」。

**不能直接用的部分**

- 一次性核准綁定動作、fencing token：需要權限 gate 能辨識「同一個動作是否已用過核准」。Claude Code／Codex 的權限機制以工具與指令樣式為單位放行，**不是**一次性的動作 token；要做得自己在 hook 或外部服務實作，個人規模多半不值得。
- 三個時間＋新鮮度上限：適合事件分流這類資料會快速過期的工作。個人寫程式時資料多半是 repo 檔案，「重讀檔案」本身就是新鮮度檢查，成本低到不必建紀錄格式。
- 多 orchestrator／peer agent：Konda 明說不適用。用看板或多 session 互相協作的工作流程，要另找協調方式。

## 回查結果（2026-11-19）

| 演講說法 | 一手來源 | 結果 |
|---|---|---|
| Pacemaker 給 `initialize` 獨立 timeout，原因是首跑自我下載撞 30 秒呼叫 timeout | [Pacemaker CHANGELOG](https://github.com/girishkvs/mcp-pacemaker/blob/main/CHANGELOG.md)：「Give `initialize` its own timeout. Sharing the 30s call timeout meant a server whose first run downloads itself returned `-32001 upstream timeout` and appeared broken.」 | **對得上** |
| crash 後 timeout 覆寫 exit code，改為只在仍存活時記 timeout | 同 CHANGELOG：「A crash keeps its own error message… A timeout is now only recorded while the child is still alive.」 | **對得上** |
| 同時 `npx` 冷啟動導致 lock compromised 全數失敗；gate 預設 2、等 15 秒後不經 gate 啟動 | CHANGELOG 記「17 simultaneous `npx` invocations here produced `npm error code ECOMPROMISED / Lock compromised` and failed every one of those sessions」；[configuration 文件](https://github.com/girishkvs/mcp-pacemaker/blob/main/docs/configuration.md)：`MCP_MAX_CONCURRENT_SPAWNS`、`MCP_SPAWN_GATE_WAIT_MS` 預設 `2`、`15000`，逾時「the spawn proceeds ungated rather than hold a client request」 | **對得上**；「17 個同時啟動」是 CHANGELOG 的細節，演講沒提 |
| session 上限等 10 秒後拒絕、拒絕計入健康失敗；容量在非同步啟動前預留 | configuration 文件：`MCP_QUEUE_TIMEOUT_MS` 預設 10 秒，逾時回 HTTP 503；CHANGELOG：「The bridge's own 503 counts as a failure」「Reserve session capacity before asynchronous startup, preventing queued cold starts from overbooking the configured cap」 | **對得上** |
| 不重播不確定的 tool call；過期 exit／已刪 resume 不能移除或復活替代 session | configuration 文件：「A timeout or child exit never triggers automatic replay of a potentially executed tool call.」；CHANGELOG：「A stale exit or deleted resume cannot remove or resurrect a replacement session.」 | **對得上** |
| MCP tool 錯誤用 `isError: true`，規格範例把 rate limit 寫成一句話；idempotent hint 只是 hint、預設 false | [MCP tools 規格](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)的 tool 執行錯誤範例文字為「Failed to fetch weather data: API rate limit exceeded」；[schema](https://modelcontextprotocol.io/specification/2025-06-18/schema)：ToolAnnotations「all properties… are **hints**」，`idempotentHint`「Default: false」，且客戶端不應依不可信 server 的 annotation 做決策 | **對得上** |
| A2A task 可 completed／failed／canceled／rejected，或停下要輸入 | [A2A 規格](https://a2a-protocol.org/latest/specification/)的 TaskState：COMPLETED、FAILED、CANCELED、REJECTED 為終態；INPUT_REQUIRED、AUTH_REQUIRED 為中斷態 | **對得上**（演講沒提 auth-required） |
| 個人 Internet-Draft 區分「檢查為否」與「無法檢查」 | [draft-konda-agentproto-evaluation-state](https://datatracker.ietf.org/doc/draft-konda-agentproto-evaluation-state/)（-01 版，2026-10，Informational，單一作者）：區分 established-negative、not-established、stale 等；REQ-1 要求不得把未建立的輸入回報成負值 | **對得上**；草案是需求文件，尚未定義欄位與編碼；未查到工作組採納紀錄（未逐一確認，不確定） |
| Kleppmann 的 fencing token | [How to do distributed locking](https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html)：client 暫停、lease 過期，storage 以遞增 token 拒絕舊寫入 | **對得上** |

未逐一回查：FLP（1985）、Chandra & Toueg（1996）、Gifford weighted voting（1979）、Berenson 等人的 SQL 隔離層級批判（1995）、Birrell & Nelson RPC（1984）、Lamport（1978）、Sagas（1987）、PACELC。演講引用的年份與論點與這些文獻的通行理解一致，但本頁未讀原文。

**Pacemaker 現況（2026-11-19 查）**：repo 建於 2026-08，最近一次 push 在 2026-11 初，有正式 release、MIT 授權，GitHub star 數為 0。是活躍維護的個人專案，**沒有外部採用證據**。

## 證據強度與限制

- **示意例子不是資料**：告警三條路徑、80% 錯誤率、9:05／9:06／9:07 時間線、10/1000 對 6/600，講者都明說是「made-up example」或先前演講用的示意。它們用來說明概念，**不能當成「sub-agent 實際會這樣失敗」的頻率證據**。
- **Pacemaker 事件**：單一作者、單一專案的自報經驗，CHANGELOG 有紀錄但無外部重現；且 Pacemaker 是 MCP bridge，不是 sub-agent 系統，演講是把 bridge 的教訓**類比**到 sub-agent。
- **SAFE 模型**：講者自提、自用，沒有評估、沒有對照、沒有與其他做法比較成效。他自己說不是通用模型。
- **經典理論的套用**：FLP、quorum、RPC 語意等在原領域是嚴格結果，套到 LLM agent 是類比。例如「sub-agent 讀共享 context＝dirty read」在結構上成立，但 agent 沒有 commit／rollback 語意，類比只到「未經確認的內容可被讀取」這層。
- **沒有數字主張需要標「勿引用」**：演講幾乎不給量化成效，Pacemaker 的設定值都與 repo 文件一致。唯一需注意：逐字稿說 FLP 針對「a synchronous system」，是語音辨識錯誤，原論文是非同步系統，引用時以閱讀頁為準。

## 與 vault 既有頁的張力與互補

- **與 Cognition「分享完整 context」的取向衝突**：[[Context-優先與多-agent-的適用邊界]] 收錄 Cognition 主張分享完整 context 與 agent trace，避免決策分散。Konda 則認為共享 context 是 dirty read 的來源，要傳的是**帶來源與時間的紀錄**，並由 orchestrator 把關。兩者其實針對同一病灶（agent 間資訊不一致），解法方向相反：一個是多給、一個是給得有標記。該頁「寫入保持單執行緒」的判準與 Konda「單一 orchestrator 才適用」的前提一致。
- **與 MAST 失敗分類互補**：同一頁收錄的 MAST 實證把多 agent 失敗歸為系統設計、agent 間錯位與任務驗證；Konda 的部分失敗與 E（由程式碼驗證）正好對準「任務驗證」這一類，提供具體機制，但他自己沒有實證。
- **dirty read 與知識庫的自我引用是同一機制**：[[Agent-維護知識庫的已知失效模式]] 第 6 條描述 agent 優先引用自己寫的內容。Konda 的「一個來源被數三次」是同一現象在平行 sub-agent 裡的版本。本 vault 的寫入規則「wiki 頁可當脈絡、不能當證據」本質上就是 S（只有外部一手來源算觀察）。
- **與 Lauren Tan 同一立場**：[[Lauren-Tan-把糾正寫進程式庫]] 主張把糾正寫成確定性檢查；Konda 的「同一個模型能跳過的檢查是 request 不是 boundary」把同一原則用在 sub-agent 交接上。
- **MCP 協議演進改變 A 的一部分前提**：依 [[MCP-無狀態化-2026-07-28]] 的整理，新版協議移除了 `initialize` 握手與 session。Pacemaker 的「重播 `initialize` 是安全的」建立在有握手的舊版協議上；對無狀態版本，重播握手這件事本身不再存在，但「不重播不確定的 tool call」與 read back 的原則不受影響。
- **綜合頁中的位置**：[[AI-Engineer-2026-演講精華-AI-工作流程]] 在「多 agent 協作」一節引用本場的 SAFE handoff 與共享 context 汙染例子；本頁是該段的完整版。
