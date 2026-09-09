---
title: Graft 用知識圖譜解決 AI Agent 最大的成本問題
description: 以程式碼知識圖譜取代 agent 的反覆搜尋，實測 token 少 42%、時間少 60%，並說明與 vector search 的根本差異與安裝設定流程
created: 2026-09-09
updated: 2026-09-09
source: https://www.youtube.com/watch?v=cyIWQHYoUg8
published: 2026-09-08
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - token-optimization
  - ai-agent
  - graph-engineering
---

> [!note] 名稱備註
> 影片自動字幕在 Graft 與 Graph 之間漂移，實際指令為 `graft init`／`graft build`，本筆記統一寫 Graft。

## 問題：agent 在動手改之前就先燒掉大量 token

Claude Code、Codex 這類 agent 的預設找檔方式有結構性缺陷：

- 你要求改一個功能，agent 必須先在專案裡找到該改哪些檔，用終端機指令搜尋相關字詞。
- 模型很少第一次就找到，得連續用多個工具逐步縮小範圍；每決定下一個工具，agent 都要把**目前為止的整段對話＋所有工具回傳結果**再送一次給模型。
- 例：把一個按鈕改成綠色 → 先搜哪個檔含該按鈕 → 結果送回模型 → 再用工具讀該檔特定行 → 才真正動手改。
- 後果有三層：context window 持續膨脹、多輪往返拖慢速度、context 太雜導致輸出品質下降。這也是單一 session 做多個任務就撞到用量上限的主因。

### 既有解法（vector search）為何不夠

常見做法是把程式碼片段轉成向量，用語意相似度比對。問題是相似度說不出「各部分如何連接」——建立帳號與刪除帳號的程式碼都會命中「帳號」相關提問，但兩者行為相反，選錯代價很高。這也是多數 coding agent 根本不採用它的原因。

## Graft 的做法：知識圖譜而非相似度

Graft 是安裝在本機的終端機指令，開源免費，**不需要另外的 API key**，直接跑在你既有的訂閱上。

- 它讀原始碼、建出一張專案地圖：每個部分是一個 **node**，部分之間的呼叫關係是一條 **edge**。
- Agent 問「什麼東西用到了這個部分」，Graft 沿著 edge 回傳相連的程式碼，讓 agent 直接看見這次改動可能弄壞什麼——這正是 vector search 做不到的。
- 地圖存成本機 JSON（結構化、可掛細節），另附瀏覽器 viewer 可視覺化探索連結關係。
- 程式碼變動時只更新變動的部分，不重建全圖，地圖自動保持最新。
- 有一個**選用**步驟：用模型替各部分寫白話說明頁。地圖本身已足以告訴 agent 什麼連到什麼，這步只是額外補上「這段做什麼」。

### 兩種接法：CLI hooks vs MCP

安裝時兩種都會裝到，差別在**誰發起查詢**：

| 模式 | 行為 | 影片提到的取捨 |
|---|---|---|
| CLI（hooks） | 每次 session 開始注入使用說明；每則 prompt 都比對關鍵字，自動附上最多 3 個匹配位置 | 較快，但不管 agent 需不需要都會附加 |
| MCP | 不附加任何東西，agent 需要時才主動查 | Graft 自家測試中答對率略高 |

程式碼本身只有在 agent 實際讀那幾行時才進 context，因此模型能用更少輪次抵達正確檔案。

## 官方 benchmark 數字

Graft 團隊自己的 162 次執行結果（自家 benchmark，非第三方）：

- 最佳情況：token 用量便宜 4 倍
- 平均：時間少 60%、工具呼叫少 46%、token 少 42%、成本低 32%

節省全部來自「省下的搜尋」，所以**專案越大效益越明顯**；小專案本來就沒多少搜尋可省。

## 安裝與設定

1. 從官網複製安裝指令在任意資料夾執行，或直接複製對應 agent 的 setup prompt 貼給 agent 自己裝。
2. 在專案資料夾內執行 init 指令（**必須在該資料夾內跑**，因為它會把該專案的指示寫進資料夾）。過程會問你用哪個 coding agent，各 agent 設定不同。
3. 完成後專案裡會出現一個 graft skill（說明有哪些指令），並安裝多個 hook 強制 agent 走 Graft 流程：session 開始注入使用說明、每則 prompt 附上匹配位置、Claude 編輯檔案後更新地圖。
4. 既有專案要再跑一次 build 指令，讓 Graft 掃過現有程式碼建圖。空資料夾則從 0 個 node 開始，skill 會在有檔案後叫 Claude 建圖。

支援 Claude Code、Codex 及其他走終端機指令或 MCP 的 coding agent。

## 實測：預約排程 App

用 Fable 5.1 建一個給獨立服務提供者的預約排程 app（類似 Calendly）。先寫 PRD，再放一份針對該模型調過的 claude.md，讓它能長時間自走不偏題；並明確告訴模型它是獨立作業、不要停下來要權限。

| | 有 Graft | 無 Graft |
|---|---|---|
| 首次建置時間 | 39 分鐘 | 47 分鐘 |
| context 用量 | 約 31% | 約 35% |

兩版功能實質相同。**首建差距小是因為當下地圖還沒建起來**；差距在後續改動才拉開——地圖建好後，整個 landing page 改版不到 2 分鐘完成。改完 Graft 自動把新檔加進地圖，並顯示該輪自估省下的 token。

## 已知限制

Graft **只映射程式碼**。實際專案裡的 PRD、各領域說明檔、learnings.md 這類給 agent 脈絡的文件都不在地圖內，agent 要讀它們時仍走預設的搜尋方式。影片作者表示因為自己也大量把 Claude Code 用在非寫程式的任務上，所以自行改了一版以涵蓋多個 plan 檔的情境。
