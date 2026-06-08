---
title: Graphify 把 Repo 變知識圖譜
description: Graphify 把整個 repo（程式碼、文件、影音、圖片）轉成可查詢的知識圖譜當作 Claude Code 的地圖，比 grep 更省 token、更準，且開源免費、可自動隨 commit 重建。
created: 2026-06-08
updated: 2026-06-08
source: https://www.youtube.com/watch?v=ChskqGovoHg
published: 2026-06-05
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - knowledge-graph
  - rag
---

## Graphify 解決什麼問題

開源、免費、約 60,000 星。把整個專案（程式碼、docs、PDF、圖片、影片）映射成知識圖譜，讓 AI coding assistant（不限 Claude Code）查圖譜而非 grep 檔案。

知識圖譜對 Claude Code 而言就是一張地圖：A 怎麼連到 B、B 怎麼連到 C、以及這些連結為何重要，都已清楚標出。對比預設的 grep 檔案（類似一直按 Ctrl+F 搜尋），有地圖就能用更少 token 得到更準確的答案。

token 節省幅度：有人宣稱高達 70x，作者認為偏高；實測（見下方 demo）較低但仍可觀。

## 三個 pass 如何建圖

- **Pass 1：程式碼結構（免費、deterministic）**：用 tree-sitter 解析程式碼檔案，抽取 class、function、import、call graph 與 inline 註解。完全在本地跑、不涉 LLM，是程式碼裡既有的確定連結，不是 AI 猜測。
- **Pass 2：影音**：若有影片／音訊檔，用 faster-whisper 轉成文字後注入知識圖譜。
- **Pass 3：docs / 論文 / 圖片**：非程式碼的內容（PDF、文件、圖片）由 LLM 做語意分析——這份文件是什麼意思、該擺在圖譜哪裡。這一 pass 在沒有真正 embedding 的情況下，做的事類似 RAG 系統。

建圖後產生三種元素：

- **Node（節點）**：圖中的每個圓點。
- **Edge（邊）**：兩個相連節點間的連線。
- **Community（社群）**：性質相近節點的大型分群。

## 與 Graph RAG 的差異

外觀很像 Graph RAG，但有兩大差別：

- **Embedding**：Graphify 完全不用任何 embedding 系統；LightRAG、RAG-Anything、Microsoft Graph RAG 等則用 embedding。
- **使用情境**：Graphify 最適合 code base——想搞懂某個大 repo 怎麼接線時最合適。Graph RAG 適合非結構化資料，例如數萬份彼此不必相連的 PDF／markdown 政策文件，問「政策對 X 怎麼說」。

兩者界線略模糊，因為 Pass 3 讓 Graphify 帶點「RAG light」性質。若指向的是一堆 markdown 文件而非程式碼，Graphify 也能處理，甚至轉成 Obsidian vault。

## 安裝與指令

安裝簡單：把 Graphify GitHub 連結貼進 Claude Code，叫它「幫我安裝 Graphify」即可；或手動照步驟。平台無關，支援任何 coding agent。

指令很多但不必記——安裝後附帶 Graphify skill，會依自然語言教 Claude Code 該用哪個指令。幾個值得知道的：

- `/graphify`：對當前目錄跑完整建圖。
- `graphify query` / `graphify explain`：明確要 coding agent 查知識圖譜回答，別偷懶自己猜。
- `graphify claude install`：變成 hook，之後一律用 Graphify 回答，不必每次明講。
- Obsidian flag：一個指令就建出整個 Obsidian vault 並填入 Graphify 的成果。

## Demo：token 差異

對 Open Design（開源版的 Claude Design，相對大的 code base）跑 `/graphify .`：

- 跑約 6 分鐘，掃 203 檔，得 1,907 節點、3,447 邊、109 社群，輸出約近 120K token。
- 完成後列出 god nodes（最顯著的節點與連結）、意外連結、建議問題。

同一問題（「追蹤一個 design request 如何從 web app 流到 coding agent 再回來」）對照測試：

- **用 Graphify**：直接載入 Graphify skill、跑 `graphify query`，約 80,000 token。
- **不用 Graphify**：Claude Code 派兩個 explore agent 爬 code base，光是它們就先用掉 100,000 token，加主 session 約共 200,000 token。

兩邊答案相同，但 Graphify 版約只花非 Graphify 版的 40% 成本。且圖譜建好後重複查詢都很便宜，這正是 memory 那一塊的意義。

## 維持更新與團隊協作

`graphify hook install` 會在每次 commit 後自動重建，只做 AST、零 API 成本——只看實際改了什麼、現在連到哪，重建那棵樹。也支援 team setup：兩位 dev 平行改同一 repo 也能處理。

最終得到一張持續存在又會隨 repo 演進的地圖，交給 Claude Code 換取更有效率的答案。
