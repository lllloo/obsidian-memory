---
title: Google Open Knowledge Format 標準化 AI 知識庫
description: Google 推出 Open Knowledge Format（OKF），用 index.md 加 YAML 描述把 second brain 標準化成可分享、可攜的知識庫，降低 agent 檢索的 token 與出錯率。
created: 2026-06-29
updated: 2026-06-29
source: https://www.youtube.com/watch?v=k4sMSsMzX2g
published: 2026-06-26
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - claude-code
  - rag
---

## second brain 的核心問題

許多人用 Claude Code 把整套知識系統當作業系統在跑，搭配 Git 版控、push 到 GitHub 讓團隊共用、用 `Claude.md`（含各資料夾的專屬 `Claude.md`）指引 agent 導航。但即使 Claude 擅長從檔案取得 context，仍經常出錯：

- 把檔案放錯位置，要人提醒正確去處。
- 不知道相似資訊已存在於別的資料夾（只是名稱不同），於是又新建一個資料夾。
- 根本問題：Claude 不知道它要的資訊「已經存在」，只有主動搜尋時才找得到；除非明確叫它去看某檔，否則它不知道那個檔存在。

Claude 的搜尋方式是用關鍵字比對檔案內容、並以檔名為輔助線索。在巢狀很深的資料夾結構中，它得試很多次才命中正確檔案——既浪費時間，也消耗大量 token。知識庫越大，問題越明顯。

## OKF 解決的是「標準化」

OKF（影片中亦稱 OKP）要解的是標準化問題，這在 agent 生態已重演多次：

- 要讓 agent 連結 terminal 以外的外部資源 → 出現 MCP，成為各 agent 通用協定。
- 要打包可重用指令 → 出現 skills，同樣擴散到各 agent。
- 要標準化設計意圖的溝通 → Google 推出 design.md 標準。
- 現在要標準化「知識」本身 → 就是 OKF。

這個概念並非全新，源自 Andrej Karpathy 提出的 LLM Wiki 模式。在此之前主流是 RAG：把大量文件轉成向量，靠語意比對 query 回傳最相關片段。Karpathy 指出 RAG 的問題是每次提問 agent 等於從零重建資訊、給你答案卻不會隨時間累積知識。他主張改用 markdown 檔建知識庫，利用模型導航檔案系統的能力，讓 agent 邊走邊累積 context。此後很多人開始自建 second brain，但每個都圍繞創建者個人 workflow 設計，他人接手得花時間讓 agent 探索資料夾、搞懂內容。

OKF 用「標準化的檔案組織方式」解決這點：不只 agent，連人也能看懂知識庫裡有什麼，並透過打包成 bundle 讓知識可分享、可攜（portable）。bundle 內含 markdown 檔承載實際資訊，每個檔都有 YAML front matter（檔頭一小段描述該檔內容），讓 agent 先知道檔案裝了什麼。OKF 不引入新東西，只提供一個人人可產出、可讀取的標準格式。

影片也推測：Google 正把 web search 推向 agentic search，OKF 可能是支援此轉變的一步——目前網站靠 LLMs.txt 提供給模型的網站資訊，未來網站或許會加上 OKF bundle，讓 agent 更有效率地查詢內容、給出更好的搜尋結果。目前 OKF 僅定位為內部使用，但這是可能的走向。

## OKF 運作原理

OKF 把知識庫中的所有東西表示為稱為「concepts」的物件（可以是資料、markdown 文件、YAML 檔等）：

- 所有要組織的資訊放進「以主題命名」的資料夾，每個資料夾只裝該主題的內容。
- 每個資料夾內都有 `index.md`，這是 agent 最先讀的檔，提供該資料夾內容的 context。
- 每個 concept 文件有一小段 YAML（含 name 與 description），讓 agent 知道它是什麼、裝了什麼——作用與 skills 的 YAML 區塊相同：逐步餵 context，agent 先讀描述再決定是否拉入相關內容，只載入需要的部分。

兩大設計原則：

- **極簡（minimalism）**：每個 concept 只代表「一件事」，type 欄位說明那是什麼。一旦 concept 混入多個不相關主題，agent 就失去精準載入所需資訊的能力。
- **知識庫與消費者分離**：無論消費者是 agent、人、團隊成員還是其他，知識本身保持獨立、也不綁定特定平台，因此幾乎可搭配任何東西使用。

## OKF 隨附的三樣東西

- **enrichment agent**：把存在 BigQuery（Google 的大型資料庫）的資料轉成 OKF concept 文件，再跑一次 LLM 檢查。
- **HTML 視覺化工具**：把 OKF bundle 轉成可互動的 graph 圖檢視，更易探索。
- **範例資料**：提供格式正確的 OKF 資料範本，供 agent 參考。

## 實測：套用在團隊的 second brain 上

影片作者已有一個透過 GitHub 共用的團隊 second brain，便拿來測試 OKF。為避免動到主分支，他們開新 branch（等於專案的獨立副本）做變更。

由於他們沒用 BigQuery，OKF 隨附的轉換工具（只支援 BigQuery）派不上用場。作為變通，他們自建一個叫「markdown to OKF」的 skill，把任意 markdown 資料夾轉成符合規範的 OKF bundle。設計上採 script-first：大部分工作交給程式碼，只有需要判斷的部分交給 agent——因為用程式碼做能減輕 agent 負擔、省 token。skill 內含轉換腳本與 evals（讓 agent 對輸出跑的測試 prompt，確認轉換正確）。

切到新 branch 執行轉換後：

- 產生根層級的 `index.md`，以連結引用所有子資料夾（作者指出這很像 Obsidian 連結不同頁面、建 graph view 的方式）。
- `index.md` 不只在根層，每個子資料夾內也有一份，列出該資料夾的所有內容，讓 agent 知道有哪些可用。
- 跑 `visualize` 指令產生代表整個知識庫的 HTML 文件，可在瀏覽器打開，列出所有節點與檔案間連結，提供互動式理解整個系統的方式。

**搜尋測試**：第一次叫它找檔案，它仍預設用平常的 pattern matching——因為 OKF 還不是廣泛採用的標準、又剛推出，Claude 不知道它存在。於是他們在 `Claude.md` 加一段，說明如何導航該系統、各檔角色、結構該怎麼用。加上之後再叫它導航到某檔，這次它開始走那些 `index.md`：

- 比 Claude 平常搜遍整個知識庫快很多。
- token 用得更少，因為先載入 YAML metadata，先理解每個檔裝什麼再決定要不要打開。

## 主要效益與現實定位

兩大優勢：**更低的 token 用量**與**更快的檢索速度**，且更不容易出現前面提到的錯誤——因為結構記錄在 `Claude.md`，agent 不會忘記檔案該放哪；又因 `index.md` 寫明每個檔做什麼，agent 知道每個檔的用途。

現實定位：目前模型靠 pattern matching 與自跑 terminal 指令已相當能幹，所以在 OKF 成為 agent 開箱即支援的開放標準之前，它比較像是一種「優化」，而非非用不可的必需品。
