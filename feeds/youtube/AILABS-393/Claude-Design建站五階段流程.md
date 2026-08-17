---
title: 用 Claude Design 建立精美網站的五階段流程
description: 從 design.md 品牌定義、design system、wireframe 到交接 Claude Code 的順序，先定規格再生成，避免重做燒 token
created: 2026-08-17
updated: 2026-08-17
source: https://www.youtube.com/watch?v=bBlY5YOsKN8
published: 2026-08-12
parent: "[[01.index]]"
tags:
  - youtube
  - design-system
  - frontend
  - workflow
  - claude-code
  - token-optimization
---

## Claude Design 是什麼

- 在 Anthropic 推出 Opus 4.7 模型時以 research preview 形式問世的設計工具，介面容易上手，非技術者也能用簡單 prompt 產出好設計，**所有付費方案都可使用**。
- 不只做網站：簡報、文件、動畫都能設計。
- Claude 桌面版與網頁版皆有，不一定要裝桌面 app。用 app 的話下載安裝、登入帳號，打開側邊欄點 design 即可進入介面。

**模型與 effort 設定**

- 可選用所有 Claude 模型，包含能力最強的 Fable（存取額度有限）。
- 一般用途的旗艦仍是 Opus，設計上也仍是最好的，**但 Opus 系列很燒 token**。
- Haiku 用量低得多，但可能需要多輪修飾才能得到好設計。
- 每個模型還可設定 effort level，控制模型動手前思考的力度。影片作者的設定是 **Opus 5 + medium effort**——能順利設計又不至於過度浪費 token。
- 也能把自己的 MCP 與 skill 帶進來用。MCP 是讓 agent 連到外部工具與服務的機制；skill 是教 agent 把某件事做得更好的指示集，含步驟指引與可依循的參考資料。

**額度限制**

Claude Design 走 5 小時額度，且**不是設計專用**——你在 Claude 上做的其他事情全部算進同一份額度。在這 5 小時窗口內有 token 上限，用完就得等窗口跑完。它雖然比剛推出時進步很多，仍然非常吃 token，重度使用時額度會消耗得更快。

因此在直接開始 prompt 之前，需要先做幾個步驟，確保拿到想要的設計又不浪費太多 token。

## 階段一：先做 design.md

`design.md` 是 Google 帶起的格式，存放品牌設計的所有細節。AI coding agent 在寫任何東西之前先讀這個檔案，所以它產出的每個畫面都符合品牌——它不需要猜，也就不會跑偏。

**為什麼不讓 Claude Design 自己生 design system**

- Claude Design 本身有建立 design system 的功能。design system 就是一組在整站重複出現的樣式選擇：字體、色彩，以及構成設計的其他細節；用同一個 design system 建出來的設計都會遵循同樣風格、看起來像同一個站的一部分。
- 但**放任 Claude Design 自己建，它會退回 Opus 系列到處都在用的通用色彩與樣式**，結果你的站看起來就跟外面每個 AI 做的站一樣。
- 交給它一份 design.md 當基礎，這個檔案明確告訴它你要什麼，控制度高很多，也不會退回預設值。
- 另一個理由是**一致性**：整套 design system 建立在同一個檔案上，每一頁都遵循完全相同的樣式，多頁網站因此保持一致。

**用 skill 規劃 design.md**

作者做了一支規劃設計的 skill，在 Claude Code 裡執行。

- Claude Code 是 Anthropic 的另一個工具，在終端機執行的 AI coding 工具，可以幫你建整個 app。安裝方式是到官網複製安裝指令、在終端機執行，完成後輸入 `claude` 就能開始下 prompt。
- skill 放進 `.claude` 資料夾下的 `skills` 資料夾（Claude Code 的設定與 config 都放這裡）。若沒有這個資料夾，直接在 prompt 裡告訴 Claude Code 你要在專案裡安裝 skill，它會自行建好並放進去。
- 這個資料夾在 Finder 裡看不到，因為名稱以點開頭的檔案被當成系統檔隱藏。要看到它需要用程式碼編輯器（作者用 VS Code），開啟專案資料夾後就能看到包含隱藏檔在內的所有檔案。
- 用 slash 指令觸發這支 skill 並給它 prompt 說明要建什麼。它會**訪談你**，和你一起詳細規劃產品的視覺識別；蒐集完成後寫出完整的 `design.md`，並執行腳本對照 Google 標準做驗證。
- 這支 skill 還內含 **anti-slop 參考資料**——那些一看就知道是 AI 做的常見模式清單。

**實際流程（範例 app：專案管理工具）**

1. 用 slash 指令觸發 skill，概略說明要建的 app 與用途。
2. 它先分析你的想法的視覺識別，接著提問，例如網站有沒有屬意的顏色。已決定品牌色就交給它，沒有就讓它自己選——因為用了 skill，它不會退回 slop 色系，但事先決定好仍然比較好。
3. 作者的做法是用 **Coolors**（產生並視覺化配色的網站）看顏色搭起來的效果，選定後點 export → 選 code 選項，把產出的文字貼進 Claude Code，它會把這些放進 design.md。
4. 接著它建立 design.md 並跑幾道驗證步驟，產出的檔案完全符合 Google 的格式規範。

**視覺化檢查 design.md**

Google 那套格式對 AI 模型好懂，但**人很難從中想像實際會生出什麼設計**，你判斷不了要不要定案。

不要跑到 Claude Design 裡才測試——那邊生完設計後若不滿意，還得回頭改 design.md 再全部重生一次，每一輪都在燒 token。有不少工具可以直接視覺化 design.md，作者用的是 `designmd.space`。這類工具會顯示設計檔的樣貌、各區塊選用的顏色搭起來的效果，也會把所有元素視覺化，決策容易得多。

**另一條路：抄現成網站的設計**

不想自己做的話，可以拿知名網站的設計當樣本——把它當起點再改成自己的，這是很多人已經在做的事（例如把 Notion 的簡潔風格微調成自己的設計）。有個網站 `getdesign.md` 列出大量品牌及其樣式的 design.md 檔案可以取用。

## 階段二：建立 design system

有了自己的 design.md，就到 Claude Design 建新的 design system。

建立新 system 時它會詢問產品細節，但既然已有 design.md，**直接把它當 asset 上傳**即可。它接著讀該檔案、建立 to-do 並逐項處理，產生 design system 並視覺化所有內容，把之後 app 會用到的各種元素都建出來。

（作者把這支 skill 放上 GitHub 並在影片說明欄提供免費連結，把連結給 Claude Code 叫它安裝即可，它會自行放進 `.claude` 資料夾。）

## 階段三：先做 wireframe

design system 定案後，開始建站之前還有一個很重要的步驟：**做 wireframe**——一份粗略草圖，讓你看到各元素放在哪裡、位置對不對。

不做 wireframe 直接建站的問題：Claude Design 生成設計很慢，你得等很久；等完之後如果不是你要的，整個得重做。

在 Claude Design 的操作：

1. 選擇剛才建好的 design system，選 wireframe 選項，在 prompt 裡說明要幾個畫面。
2. 它還能為每個畫面產生多個版本，讓 Claude 給你幾種不同風格挑選。生成不會太久，可以檢視結構並比較同一頁的各種變化。

**善用 comment 功能**

- 要改某一項東西時，直接在它上面留 comment。comment 會把該元素的精確資訊連同你的 prompt 一起送出，Claude 因此明確知道是哪一塊要改、要怎麼改——比單純下 prompt、讓 Claude 自己猜你指的是哪一區好得多。
- 操作方式：選 comment 功能，點你要改的東西，輸入需要的變更；要加幾個就加幾個。
- **不要一則一則送，把它們集中一次送出**，讓它一起解決、一次修完，等待時間最短。

反覆調整到結構滿意為止，再進下一步。

## 階段四：在 wireframe 上長出正式設計

1. 先從剛才產生的多個變體中挑定要用的那一版。每一頁都有自己的代號，用代號選取。
2. 下 prompt 告訴它把這些畫面轉成完整細節的正式設計，並要求**保留 wireframe 的 layout 與結構**，維持乾淨的間距與層級。
3. Claude Design 會讀取它在建 design system 時做的所有元素，用這些元素建出整站，因此成品完全符合 design system 與 wireframe。

**常見需要修的地方**

- 和 wireframe 一樣可以用 comment 修改，而且**通常需要改很多**——它常常沒把按鈕顏色挑好。有些按鈕需要吸引注意、應該用醒目的顏色突顯，可以叫它修。
- 因為是長在 wireframe 之上，成品會有點空，只是在粗略草圖上補了基本元素而已，可以叫它加入材質與元素讓畫面更豐滿。
- 小改動（例如刪掉某個元素）可以**直接在設計上編輯**，不必下 prompt 給 Claude，省下等待時間與 token。
- 改完後可以請 Claude Design 對整體外觀做 polish，它會做出細緻而有意義的調整。

**加動畫**

動畫很重要，它讓網站用起來更舒服、把視線引導到真正重要的地方（例如捲動進場之類的小細節會讓網站更有生命力）。

作者下 prompt 請 Claude Design 為所有畫面加上動畫，例如捲動進場之類的細微效果，並**特別要求保持克制、不要做得太彈跳**（那會有違和感）。完成後可以看到捲動進場與文字彈出的動畫，整站互動感提升很多。

## 階段五：交接給 Claude Code

設計定案後，要把它變成最終交付的真實產品。

- Claude Design 過去沒有這個能力，**現在可以直接把設計匯出到 Claude Code**。
- 它走的是 **Claude Design MCP**，讓 Claude Design 與 Claude Code 互相溝通，而且是**雙向的**：設計可以從 Claude Design 進到 Claude Code，也可以再帶回來。
- 操作：打開 Claude Code，貼上從 Claude Design 拿到的 prompt。它會先讀 metadata（設計的摘要資訊），列出專案檔案，先讀 design system（設計定義所在），再逐一讀取所有元素。取得完整設計後在你的專案裡建出來，連 Claude Design 裡的動畫一併帶過去。

**務必做深度審查**

視覺上看起來都對，但 Claude Design 的原始程式碼轉成真實 app 時仍可能有內部問題。

作者請 Claude Code 做 deep review，它開始拿 design.md 對照實際建出來的東西檢查兩者是否吻合，**抓到多個問題，其中包括 responsive 問題**（app 在手機、平板等不同螢幕尺寸上顯示不正確）。

Claude Design 的產出容易有這個毛病，因為它還是早期版本，設計出來的東西對它當初針對的目標最好——為網站做的設計在網站上很棒，但不見得適用其他螢幕尺寸。跑完修正後，app 的視覺部分就正常且 responsive 了。

## 接資料庫：Supabase

此時 app 雖然功能可用（點按鈕會作用、能新增專案細節），但**重開 app 之後所有進度都不見了**，因此需要資料庫把資料存起來。

作者用 **Supabase**——最熱門的後端供應商之一，管理使用者與資料的最佳方案之一。他們幾乎每個 app 都用它，不論客戶是誰，連很多內部工具的整套設定都跑在上面；理由是它接手掉大量原本要自己做的工作，而且它極易與 Claude Code 這類 AI agent 串接。

**Supabase 的 agent skill**

- Supabase 有官方 agent skill，內含 agent 可用的指示、腳本與資源，讓它更可靠地操作 Supabase。
- 安裝方式：複製安裝指令交給 agent。這個 bundle 內有**兩支 skill**：
  - **supabase skill**：使用指南，任何資料庫或登入相關任務都會觸發。
  - **best practices skill**：優化 app 效能的最佳做法，在 prompt 裡提到 optimize performance 之類的字眼時啟動。
- 兩者背後有龐大的參考資料庫涵蓋各類問題。

**skill 不等於工具：必須另接 CLI 或 MCP**

- 作者事先自己做好了資料結構（schema）放進專案主資料夾，因為不想讓 agent 決定 app 的資料怎麼組織。
- **skill 只是一包指示，構不到 Supabase 伺服器上的專案去做變更**——它就是一段告訴 agent 怎麼做的文字，本身不附帶任何能對 agent 之外的東西動手的工具。
- 因此 Supabase skill 會要求你接上它的 **CLI**（終端機工具）或 **MCP**，兩者都能給 agent 直接操作 Supabase 專案的工具。
- 作者選 MCP，因為設定較簡單，也不必處理 CLI 登入帳號所需的金鑰。做法：到官網複製對應 agent 的安裝指令，在專案資料夾的終端機執行；接著在 Claude Code 裡跑 `/mcp` 就會看到已連線，但還不能直接用，因為尚未登入。選 authenticate 會導向瀏覽器登入，完成後 MCP 即連上。

**執行結果**

MCP 接好後，Claude Code 載入 skill 開始作業：做了大量變更，並針對資料庫請求跑測試以確保建出最好的版本；它也依 skill 裡的準則**把不該讓所有使用者存取的區域全部鎖起來**。整套後端就這樣透過 skill 交由 Supabase 承載。

（部署上線的部分影片未涵蓋，留待後續影片。）
