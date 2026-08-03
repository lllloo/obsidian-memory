---
title: 3 小時打造文件審查應用（Python、React、Azure）
description: 以發票審查為例，串接 Azure Document Intelligence 與 Azure OpenAI 建立分類、擷取、驗證的處理鏈，配上 FastAPI 與 React 前端，最後用 Container Apps 部署上線
created: 2026-08-03
updated: 2026-08-03
source: https://www.youtube.com/watch?v=YYeZh6Hac9E
published: 2026-07-23
parent: "[[01.index]]"
tags:
  - youtube
  - ai-engineering
  - azure
  - document-processing
  - python
---

## 為什麼是文件審查

作者說這是客戶案子中最常被要求的一類：公司都有文件，都需要審查或處理。共通結構是「文件進來 → 對照某組規則／商業邏輯／品質標準做審查 → 通過與否的核准閘門」，通過就送出或寫回資料庫，不通過就退回修正。換掉文件類型與規則，同一套骨架幾乎能套到任何文件流程。

影片刻意選發票與收據當例子，因為它是所有人都懂、又剛好有明確可測規則的文件。

## 客戶簡報與功能需求

虛構公司 Northstar Facilities，使用者 Maya 是財務部門的行政人員。User story：上傳多語系的發票或收據，拿到一份整理好的審查結果（含最佳的合併擷取結果、VAT 與政策檢查、建議的總帳科目），然後快速核准，或退回給供應商並附上錯誤說明。

拆成功能需求後為：

- 支援 PDF 與圖片
- 自動辨識是發票還是收據（分類步驟）
- 擷取欄位、驗證欄位、套用政策檢查
- 再一次分類，決定歸到哪個總帳（GL）科目
- UI 讓 Maya 修正欄位、核准／退回、草擬更正信
- 保留審查歷史

作者強調這個「先拿到非技術語言的 user story，再翻成功能需求」的步驟，是接客戶案子最先要做清楚的事，也是後面所有實作的驗收基準。

## 整體架構

```
React (Vite) 前端
   ↓
FastAPI 後端（API 層）
   ↓
Azure Document Intelligence（擷取）＋ Azure AI Foundry / Azure OpenAI（LLM）
   ↓
Python 端的決定性財務規則
   ↓
SQLite（本機檔案資料庫）
```

擷取刻意做成 hybrid：先用 Azure Document Intelligence，再用具備 vision 能力的 GPT 模型交叉比對。理由是真實世界一定會撞上 edge case，從多個角度攻同一份文件，最終結果通常最好。

## 先看資料，再寫程式

作者出身資料科學，主張每個專案都從資料開始。他觀察到從軟體開發轉 AI 工程的人常輕忽這步——習慣用資料型別（字串／整數／JSON）去推理，卻不看資料的語意：這份資料在講什麼、有哪些類別。

repo 內附一組合成的樣本文件：多份英文發票、掃描品質較差的版本、收據，並在 manifest 標好每一份的預期結果（哪幾份應該直接 ready、哪一份缺 VAT、哪一份 VAT 無效、哪一份總額對不上）。有這種標好答案的資料集，等於給 AI agent 一個明確的優化目標。

作者的實務建議：開專案時盡量先蒐集可標註的資料集，涵蓋正確、錯誤與各種需要不同輸出的情境。他提到最近一個真實客戶案（審查 40 頁 Word 文件的拼字、文法與商業邏輯）也只從三份 happy path 起步，人工塞進錯誤來看模型在哪停住；等 PoC 之後灌進更長、更多的文件，錯誤與 codebase 的 edge case 才大量浮現——這是常態，不可能一次到位。

## Azure 基礎與 CLI

Azure 的層級是：帳號（tenant）→ 訂閱（subscription）→ 資源群組（resource group）。資源群組可以理解成專案或資料夾。本專案建一個 `RG-invoice-review`，所有資源丟進去。

作者主張盡量用 CLI 而不是點 Portal，因為：CLI 比較快、可以交給 AI agent 執行，而且 Microsoft 幾乎每個月都在改 UI 與命名（Azure OpenAI 改叫 Azure AI Foundry，Portal 搬到 `ai.azure.com` 後一堆轉址迴圈），CLI 反而是相對穩定的介面。代價是要把環境權限交給 agent，得留意它在做什麼。

```bash
az login
az group create --name RG-invoice-review --location westeurope
az cognitiveservices account create ...   # F0 = 免費方案
```

新帳號有 200 美元、30 天的額度；Document Intelligence 也有免費方案。作者說整支影片的花費，比直接拿 OpenAI API 玩一個下午還便宜。

## Azure Document Intelligence

Microsoft 的文件擷取服務（舊名 Form Recognizer，CLI 與部分文件仍沿用舊名）。關鍵特性：

- 不是 LLM，是預訓練的自訂機器學習模型，因此更快也更便宜
- 內建一票 pre-built 模型：銀行對帳單、支票、合約、信用卡、發票、收據等，本專案用 invoice 與 receipt 兩個
- 回傳的不只是文字，還有 pixel 等級的位置資訊——能對每個抓到的欄位在頁面上畫出框。作者認為這是它勝過 LLM 的地方，LLM 能「理解」頁面，但做不到這種精準定位，而這些額外資訊在下游常派得上用場

開源替代方案作者提到 Docling，並說這個難度的範例用 Docling 也做得完；但真接客戶案時遲早會遇到需要 hybrid 的狀況。

**一個關鍵限制**：Document Intelligence 沒有內建 classifier，無法自己判斷這份是發票還是收據。所以流程必須是「先分類、再擷取」——分類那步交給 LLM。

## Azure AI Foundry / Azure OpenAI

作者所有客戶專案的 LLM 都走 Azure，不直接打 OpenAI 或 Anthropic，理由是資料保護與安全性的說法比較好賣。他的常用說法：交給 Azure OpenAI 的資料，安全性大致等同放在 Outlook 收件匣裡的資料——而客戶本來就在用 Outlook。模型定價與直接用 OpenAI 相同，可用的模型也一樣。

設定時的實務坑：

- 資源名稱必須**全球唯一**，不只是帳號內唯一
- Foundry 底下還有一層 project，要留意當下選對 project
- 新專案預設**沒有任何 deployment**，沒先部署模型就呼叫必定失敗
- 模型可用性依 region 而異，quota 與 region 的限制很煩人；換一個模型通常就過了
- 驗證方式預設是 Entra ID，要改成 key authentication

程式端幾乎沒有差別——`from openai import OpenAI`，只換掉 client 的 base URL，請求就繞道 Azure。

## Pydantic 資料模型與 mapping 層

Document Intelligence 回傳的是龐大的 JSON。作者的習慣是解析完的資料一定要進資料模型，用 Pydantic 定義嚴格 schema。專案裡分成三塊：

- `schemas/`：invoice 與 receipt 兩套 Pydantic 模型
- `common.py`：兩者共用的欄位型別（如 extracted string、extracted date），把 Azure 那份雜亂 JSON 標準化成可重用的建構塊
- `mapping.py`：負責把 Azure 的 JSON 物件映射到上面的模型

有了資料模型，商業邏輯才有東西可掛——「這份文件有沒有 VAT 號碼」不只是有沒有這個 key，而是 Pydantic 層先驗證欄位存在，再由後續函式檢查格式是否符合歐盟 VAT 規範。

## Pipeline：chain pattern

作者請 agent 在 `pipeline/` 建立一個 chaining pattern：一個 base pipeline step 類別，一個 pipeline context，run function 只是依序 loop 過所有步驟。

實際的四個步驟：

1. **分類**：用 LLM（Pydantic AI + structured output）判斷 invoice / receipt
2. **擷取**：依分類結果呼叫對應的 Document Intelligence 模型，映射進 Pydantic 模型
3. **驗證**：跑決定性的財務規則
4. **總帳科目建議**：另一個 structured output 分類步驟

第 4 步其實可以併進第 1 步，作者刻意拆開示範，理由是這步可能要換不同模型，拆開比較乾淨。

這是最單純的線性鏈，沒有分支與 router。作者認為它的價值在於：一旦這個模式被建立起來，之後叫 AI agent「加一個 pipeline step」，它會讀 codebase 自動照著同樣的模式寫。他把這當成給 AI 時代的一個大 tip——**直接問 agent「我要做 X，有什麼適合的 design pattern」**，它會給幾個選項；不問而直接說「去把 classifier 寫出來」，codebase 很快就會變得一團亂，這正是大多數用 AI 寫的專案的下場。

分類步驟的 structured output 模型除了 document kind，agent 還自動加了 confidence 與 reasoning。作者認為稍微 overkill（用 literal 直接回 invoice / receipt 也行），但保留了，同時提醒：**這種 confidence 值除非在 prompt 裡給範例，否則通常不太可靠**。

## 財務驗證規則

發票的檢查：

- 歐盟 VAT 號碼是否存在、格式是否合法、是否為有效號碼
- 總額對帳：小計、稅額、總計加總是否吻合（帶一個容差）

收據的檢查明顯少很多，因為收據上的資訊本來就少（通常沒有 VAT 號碼）。

作者指出這一段是最「文件專屬」的部分：換一個專案，這裡就是要坐下來跟客戶談的地方——文件我們能擷取了，AI 工具都在了，那到底要檢查什麼？

**總帳科目**：agent 產出一個 accounting 模組，裡面是 10 個 GL 代碼的 enum，每個附上何時該用的說明（清潔、維護、電氣等，對應這家清潔服務公司的業務）。示範中一張模糊的發票被歸到 6190 雜項營業費用，作者認為這個「歸到最含糊的類別」的結果反而是對的。

## 前端與 API 層

前端 stack：Vite（作者提到正確發音接近法文的 veet）跑開發伺服器、React、strict TypeScript、Tailwind CSS，套件管理用 pnpm，開發伺服器在 `localhost:5173`。後端 FastAPI 跑在 `localhost:8000`，內建的 `/docs` 直接拿來看目前有哪些 endpoint。

資料庫用 SQLite，就是放在檔案系統上的一個 `.db` 檔。

作者請 agent 寫了一個放在 `scripts/` 的 bash 腳本，從 repo root 一個指令同時起前後端，省去管理多個終端機。第一版 agent 寫了 100 多行（一堆環境檢查與註解），他直接要求「盡可能寫短、不要做環境檢查」，砍到約 10 行。他把這列為使用 AI 的一大 tip：**明講要它寫短**，否則它傾向堆滿註解與檢查。

**命名重構的插曲**：agent 把上傳端點取名 `/api/invoices`，但它同時也能處理收據。作者故意裝傻反問「既然也支援收據，為什麼叫 invoices」，agent 自己承認 `documents` 比較清楚，於是前後端一起重構。他的評語是：能跑不等於程式碼合理，AI 只會把空格填滿，不會替你想這件事。

## 完整審查工作流

最終的迴圈：上傳 → 跑 pipeline → 每一步的中繼結果都存進資料庫供 UI 使用 → 顯示分類、GL 建議、擷取結果與驗證結論 → 使用者核准或退回 → 退回時可自動草擬給供應商的更正信 → 全部進歷史紀錄。

UI 上的表現：

- Happy path 的發票：全綠、可核准；核准後不可再編輯，歷史頁可刪除
- 有問題的發票：VAT 缺漏顯示為 error，此時使用者**無法核准**，只能退回；點下去可用後端的 LLM 草擬一封說明缺少 VAT 號碼的更正信，複製寄出（作者說再往前一步當然可以做成自動寄信整合）
- 額外的 hybrid 交叉檢查會產生 warning，例如「vendor name 信心值低於 80%」——示範中那次其實抓對了，作者認為這個門檻是實務上要自己調的設定
- 收據：規則較少，示範那張加油收據全綠通過

作者提醒：交付給真實使用者後，一定還會冒出一堆調整需求。接案時要分清楚哪些是原始需求內的微調，哪些是**新的功能需求**（例如客戶事後說「其實我還有一些 Word 檔」——那是要另外規劃與計價的東西）。

## 部署到 Azure Container Apps

部署策略：作者平常會把前後端拆成兩個 deployment，客戶案若能自己選會用 Hetzner 的 VPS，但很多客戶用 Azure。這次為了示範，把整個 app 收成**單一 container**——React SPA 建置成靜態檔，由 uvicorn 上的 FastAPI 在同一個 port 一併服務。

用到的 Azure 資源：

- **Container Apps**：跑應用程式本體，部署後拿到一個 Azure 給的 HTTPS URL（可再掛自訂網域）
- **Container Registry**：註冊 Docker 映像
- **Storage Account**：用 Azure Files 檔案共享掛載 SQLite 檔與上傳檔案
- **Log Analytics**：看應用程式日誌

作者刻意用 storage account 而非獨立資料庫服務：storage account 在 Azure 上幾乎免費，跑一個 PostgreSQL 一個月很快就 20–40 美元。對內部應用來說這樣完全可行，但真的做客戶案他仍會用正規資料庫。

**環境變數的兩個位置**（部署最常踩的坑之一）：本機跑得好好的，部署後應用層也要拿得到那些變數。API key 之類的放在 container app 的 **secrets**；endpoint 這種非機密的則是 container 層的 **environment variables**，兩者不在同一個畫面。CLI 的好處是它知道怎麼管這些，省掉大量點擊。

**安全性**：部署上網路後預設任何人都能存取，作者加了一道簡單的密碼保護（不是完整登入系統），並要求 authentication layer 涵蓋所有可到達的 URL。他明確聲明這**不是**安全應用程式的完整指南，那道單一密碼大概很好破，下游服務的安全性也還沒談。

**成本控制**：玩完之後在資源群組最上層直接刪除整個 resource group，所有資源一併消失、不再計費。作者說 Azure 平台雖大，但要真的把東西弄壞幾乎不可能——真正要小心的是客戶資料，以及應用程式或資料庫是否公開可存取。

## 開發過程中的實務筆記

**Monorepo 的 Python 路徑問題**：後端與前端同一個 repo，`pyproject.toml` 在 `backend/` 而不是 root，於是 IDE 找不到虛擬環境（要手動貼路徑）、playground 匯入 app 會噴 import 錯誤。他花了不少時間才發現 agent 加的是 VS Code 版的 `python.analysis` / basedpyright 設定，而 Cursor 需要另一個對應設定。作者自嘲寫了十年 Python，路徑與 import 至今仍在折磨他；也因此他們客戶案一律從自家的專案範本（GenAI Launchpad）開始，這類問題早就解決過了。

**playground 資料夾**：作者固定把「拿來實驗、跑單一範例、看資料長什麼樣」的程式碼放在 `playground/`，不放進應用層。應用層是應用層，測試探索是測試探索。他也刻意先手動建好 `services/` 資料夾與空檔案，藉此把 AI 導向他想要的結構，而不是任它自由發揮。

**Jupyter interactive session**：在互動式 session 跑非同步程式會撞上 event loop already running，解法是 `uv add nest-asyncio` 後 `import nest_asyncio; nest_asyncio.apply()`。這是純粹的開發便利 hack，生產環境不需要，所以它只存在於 playground。

**ruff 的 import 排序警告**：修改 `sys.path` 讓 playground 找得到 app 時，若寫成多行 insert，ruff 會抱怨 import 不在頂端；改寫成單行的 `sys.path.append` 形式 ruff 就認得。作者順手請 agent 把這個寫法統一到所有 playground 檔，並在 playground 放一個 `agents.md` 說明為什麼要這樣寫。

**物件導向重構**：agent 第一版把分類步驟拆成一堆私有函式，作者看不懂也不喜歡，請它改成一個類別，分成「設定」「prompt」「執行」三塊。他坦言這在功能上沒差別、有人會覺得他把事情變複雜，但這是「能跑但你不知道它在幹嘛」與「能跑而且你打開檔案就懂」的差別。

**git 與金鑰**：作者在 `development` 分支上開發，用 commit 當 checkpoint，讓觀眾可以逐步對照。過程中 GitHub 的 push protection 擋下了一次推送——原因是他早先在測試檔裡硬寫了 API key。他的評語是「還好它擋了」。

**AI 工具用法**：主要在 Cursor 裡工作，小任務用 Composer 2.5 fast，大任務試 Grok 模型；多數改動先進 plan mode 看計畫再執行，趕時間或有把握的小事才直接執行。用 Glido 語音輸入下 prompt。一個他反覆示範的模式：**丟出一個計畫給 agent 跑，同時自己去做下一件事**，回來再檢查。

**保持理解**：作者反覆強調不要走到「我不知道這個應用怎麼運作」的不歸點。他的做法是在推進的同時，時不時停下來要 agent 解釋（例如「mapping.py 是不是把 Document Intelligence 的 JSON 映射到我們的模型，我這個心智模型對嗎」、「幫我在 docs 寫一份文件說明所有 endpoint 與 run pipeline 怎麼運作」），確認之後再繼續。
