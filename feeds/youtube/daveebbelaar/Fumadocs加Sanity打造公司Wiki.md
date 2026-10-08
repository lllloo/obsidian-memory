---
title: 用 AI 搜尋打造你自己的公司 Wiki（完整教學）
description: 以 Fumadocs 建文件站、接 Sanity 當 CMS 並自動產生 embeddings，做出關鍵字／語意／混合搜尋與能引用頁面回答的 AI 聊天元件
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=DNuD3Ia8qHM
published: 2026-09-25
parent: "[[01.index]]"
tags:
  - youtube
  - ai-engineering
  - rag
  - mcp
---

## 成品與做法

- 目標：建一個公司知識庫網站，並加上 AI 聊天元件——可問任何關於網站或知識的問題，它會瀏覽相關頁面、列出資源再回答。
- 技術組合：**Fumadocs** 當文件站基底 → 自訂聊天元件 → 接 **Sanity** 啟用語意搜尋。
- 全程用 AI 協助，程式經驗有限也能跟上。講者的教學文件頁設計成可交給 AI agent 瀏覽：卡住時把說明欄連結丟給自己的 coding agent，請它帶你完成設定。

## Fumadocs 基礎

- Fumadocs 是開源的文件網站框架，Fumadocs 官網本身就是用它建的；官網有展示哪些品牌使用它，以及可做的客製化。講者認為是目前用過最好的方案。
- 需先安裝 Node.js，再用建立指令產生範本專案（教學中命名為 Fumadocs playground），安裝後啟動 dev server、在瀏覽器開啟。
- 開箱即有：頂部導覽列、明暗模式切換、`Cmd + K` 搜尋、側邊欄、各種元件、複製為 Markdown、在編輯器中開啟等功能。
- 內容放在 `content` 資料夾，編輯 Markdown 檔（例如改標題）存檔後頁面即時更新。卡片等元件的寫法不必自己學，AI 會處理；只需知道「能做什麼」與專案大致運作方式。

## 從範例專案起步

- 講者的觀點：現代做法不是從零開始，而是找一個喜歡且能跑的範例，再用 AI 做小幅調整與改進（等同反向工程）。
- 停掉 playground 的 dev server，`git clone` 講者提供的公司知識庫 repo（連結在說明欄），進入專案資料夾後安裝依賴（產生 node modules）。
- 用 `cp` 把範例環境變數檔複製成正式的 `.env` 檔；其中含登入密碼與之後要填的金鑰。
- 這個知識庫不做完整的身分驗證，只用**密碼保護**，可在環境變數中改密碼。
- `npm run dev` 啟動，跑在 port 3000；注意要用 `localhost` 而非畫面上的 IP，前往 `localhost:3000/login` 輸入密碼。

## Wiki 結構與頁面負責人

- 首頁是網域根目錄，與文件頁不同；進入 `/docs` 後才是含側邊欄的主導覽。
- 設計知識庫時先想好主要分組：範例依**部門**與**團隊手冊**拆分；做產品文件時則可依畫面、工具、設定分章（講者以自家產品文件站為例）。
- 公司 wiki 的關鍵設計：**每頁都有負責人（owner）**。例如行銷部的客戶案例頁負責人是行銷主管 Noah；使用者不只能自己找資訊或問 AI，還知道該找誰。
- 頁面檔案結構很簡單：一小段 frontmatter（title、description、owner）加上 Markdown 正文（標題、連結）。
- 建議練習：用語音轉文字工具（講者用 Lido）對 coding agent 說「建立一個研究部門區塊，並在裡面加一份研究文件，想想它的內容與負責人」。agent 會建立研究資料夾、一份場域觀察流程文件與新負責人，重新整理網站即出現。
- 這類系統容易維護與擴充，也正是組織成長時最大的挑戰之一；講者認為可以賣給仍在用 Word 文件管理知識的公司。
- Fumadocs 預設已有基本搜尋，能找到剛新增的頁面。

## 為什麼要加 Sanity

- Sanity 是內容管理平台（CMS），講者過去用它管理許多網站，看重其優秀的 API 與完整的 AI 導向設計。
- 要把知識庫提升一級需要兩件事：
  1. **讓非技術人員也能編輯**：不是每個人都願意開 IDE 改 Markdown。Sanity 提供編輯介面，也提供 **MCP server**，可直接接 ChatGPT 或 Claude，把程式與複雜度從使用者面前藏起來。
  2. **自動產生 embeddings**：資料進 Sanity 後會自動建立 embeddings，才能做到片頭那種問答；自己從零做需要 embedding 模型與更多後端程式，成本更高。
- 講者提供的連結有 60 天免費試用，含 embeddings 與用量，不需信用卡。

## 設定 Sanity 存取

- 在 Sanity 管理後台建立專案（例如「公司知識庫」），一開始是空的。
- 在專案的 API 頁建立 token：名稱隨意、不會過期、給 **developer** 權限；把 token 與 **project ID** 填進 `.env`。
- 專案內的 `sanity` 資料夾已備好 schema。在知識庫專案根目錄依序執行：
  - `npm run sanity setup`（需要上述兩個環境變數；出錯通常是 terminal 不在正確資料夾，或環境變數沒設好）
  - 匯入指令，再檢查狀態
- 匯入後在 Sanity 後台的 datasets 可看到新建的知識 dataset。

## 切換到 Sanity 內容來源

- 在 `.env` 把**內容來源**設為 `sanity`，網站就從讀本機 Markdown 改成讀 Sanity 的資料；外觀不會有任何變化。
- 驗證方式：刪掉本機某個 Markdown 檔再重新整理，頁面內容仍在，證明資料已來自 Sanity dataset。

## Sanity Studio 與編輯

- `npm run studio` 在另一個本機 port 啟動 Sanity Studio，用建立專案的同一帳號登入（講者用 Google 登入）。
- Studio 內可看到所有知識頁（結構化文字）與員工個人檔案；介面對非技術人員也很友善。
- 所有資料模型皆可客製；coding agent 已持有 Sanity API key，可代為修改、上傳、匯入 schema。
- 部署託管版 Studio：先用 Sanity CLI 登入，再執行 `npx sanity deploy`，為 Studio 取名後即取得 sanity.io 上的託管網址。團隊成員與 AI agent 都能從雲端進來編輯。
- 編輯流程：在 Studio 修改頁面 → 存成草稿 → 發布；網站動態從 Sanity 載入內容，重新整理即可看到更新。等於把運作方式從 repo 裡的 Markdown 改成託管在雲端的專業 CMS。
- 教學文件中也有連接 Sanity MCP server 的說明：開發環境中有 API key，coding agent 可直接操作；要讓同事（例如研究負責人 Hannah）從自己的 Claude 桌面 app 或 Codex 管理內容，只需加入 MCP server、完成驗證，就能用聊天方式編輯，發布後即出現在網站上。

## 關鍵字、語意與混合搜尋

- Fumadocs 內建的 `Cmd/Ctrl + K` 是**關鍵字搜尋**：必須字面相符。範例中搜「laptop」能找到遺失或被竊裝置的流程，但搜「computer」或「notebook」就找不到，因為頁面裡沒有那個字。
- 小型知識庫靠瀏覽就夠，但知識庫的目標是擴展到整個組織，這時需要**語意搜尋**——依意義而非精確字詞比對。
- 連上 Sanity 並把內容來源設為 sanity 後即自動啟用語意搜尋，因為 Sanity 預設在背景產生 embeddings。搜「computer」也會帶出遺失／被竊裝置的頁面，因為 laptop 與 computer 語意相近。
- 也可做**混合搜尋**並設為預設。範例介面可切換三種模式比較：關鍵字搜「computer」沒結果、語意搜尋出現大量相關內容，合併兩者通常是效果最好的做法。

## 加入 AI 聊天元件

- 「Ask the guide」聊天元件：講者表示這個元件幾乎可以放進任何網站——把既有網站內容搬進 Sanity，掛上元件就能運作。
- 前提是內容來源設為 sanity，並額外提供一個 LLM API key。範例用 OpenAI 模型，但可換成任何 LLM，甚至用 Ollama 跑免費開源模型（較慢、品質較差）；要換 Claude 等其他供應商，直接請 coding agent 改即可。
- 在 `.env` 填入 OpenAI API key 與模型名稱（想沿用講者的模型就保持預設）。
- 實際表現：
  - 問「拜訪客戶後的餐費可以報銷什麼？」→ 顯示搜尋查詢與查過的頁面，回答並連回出處頁（差旅支出）。
  - 問「我的筆電掉了，該怎麼辦？」→ 回答以串流輸出；對話紀錄存在本機，不需資料庫，可回到先前的對話。
  - 問付款相關問題 → 指出財務負責人是 Daniel Brooks，想了解客戶付款條件時可以直接在 Slack 找他。
- 講者認為這正是它與單純 SharePoint 或一般文件站的差異：幾分鐘內就能把 AI 問答加進網站。
- 商業用途：可當作品集專案，或向在地企業提案（內部知識庫或對外網站問答），講者稱這類系統可賣到數千美元，且不必自己處理 agent、embeddings 等複雜技術。

## 後續：部署與安全

- 目前 Sanity 託管所有資料，但網站本身只跑在 localhost，只有自己能存取，且只有簡單的密碼登入。
- 實際使用需部署，並加強身分驗證：例如接 Google 登入且只允許自家 Google Workspace 的使用者，或用 GitHub、帳號密碼驗證。
- 做法取決於部署位置與方式，影片不展開；可把教學頁連結交給 coding agent 協助完成。
