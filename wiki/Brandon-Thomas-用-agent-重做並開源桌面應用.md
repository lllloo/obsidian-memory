---
title: Brandon Thomas 用 agent 重做並開源桌面應用
description: 深讀 Brandon Thomas 演講並回查 GitHub，整理 agent 以 Rust 重做 Photoshop 的做法、自報數字與 Autocraft
created: 2026-11-19
updated: 2026-11-25
source: https://ai.engineer/code/2026/talks/brandon-thomas
published: 2026-11-12
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - mcp
---

# Brandon Thomas 用 agent 重做並開源桌面應用

來源：AI Engineer CODE 2026 演講〈How I cloned Adobe with AI〉（閱讀頁場次名為 Let's Open Source the World）的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-Thomas-How-I-Cloned-Adobe-with-AI]]。影片：Day 2 直播 `y9JtCCZP2MQ`（1:20:53–1:40:19）；剪輯單場版 `UCL4K36SHp0`，YouTube 標題就是 How I cloned Adobe with AI，長度約 19:55，與直播區段相符，判定為同一場。回查日期：2026-11-19。

**一句話**：coding agent 讓小團隊能用 Rust 重做 Photoshop、InDesign、Premiere、Office 這類大型桌面應用並全部開源。使用者因此能把應用砍到只剩自己流程要的部分，Web 2.0 之後被平台收走的「動手改工具」能力可以拿回來。

## 講者與立場

- Brandon Thomas，ArtCraft CEO（GitHub 組織是 `storytold`，演講末留的聯絡信箱是 storyteller.ai 網域）。自述當了約 15 年工程師：在 Square 做了 8 年基礎設施（線上支付、認證，長期輪值 on-call），之後 7 年做新創，客群是創作者、藝術家和電影人。人在 Atlanta，大學後拍過很多片。
- **在推自家產品**：整場是 ArtCraft 系列應用的介紹，還推薦大家下載 PdfCraft、預告 Autocraft，結尾徵才。
- 他自己說這場是「前一晚趕出來的」，結構零散，而且超時。技術段（Rust、CI、review 分流、Autocraft）只有約 3 分鐘，是用跳的講完。**整場重心是開源理念和病毒式擴散，不是工程方法**；想找細部做法的人能拿到的不多。

## 演講脈絡（照演講順序）

### 1. 開場：爆紅後的一個月（1:20:56）

他說「kind of cloned Adobe Photoshop and a bunch of other apps」之後爆紅，一個月沒睡好，VC 一直找上門。他把目標定為「open source the entire world」：開源支撐了許多技術，卻從來不在前台；Linux 一直是二等公民；大家被拉進一堆自己沒有所有權的平台，而 AI 給了「把 web 拿回來」的機會。

### 2. 早期 web 與 enshittification（1:23:14–1:27:27）

- **早期 web**：IRC 可以自己架 server、自己寫程式自動化；商用通訊軟體不在意你用第三方 client；網站都有資料匯出與 API，可以拿 Reddit、Flickr、Twitter 做 mashup；買 mp3 有所有權感；Flash 動畫、phpBB 社群、Wikipedia、能改 HTML／CSS 的 MySpace。他把原因歸為當時上網的人大多懂技術。
- **Web 2.0 之後**：寬頻和智慧型手機把所有人帶進來。他說這不是壞事（父母、祖父母也要能用），代價是「把邊角磨圓」：技術性的部分被拿掉，協定被平台取代、API 被收回，發行通路被大廠把關（他特別點出手機從來沒有像桌面那樣能自由發行）。新創拿到市占後發現有定價權，「訂了所有串流服務之後，Netflix 又變回了有線電視」，成長到頂的公司開始想出各種陷阱。
- **Adobe 退訂費的例子**：他說月繳方案在 12 或 18 個月內取消，會被收「up to like $200」的取消費，而且寫在小字裡；一年只拍一部影展短片、只用一個週末的人會多一筆 200 美元帳單。他用 enshittification（逐字稿辨識成 shitification）形容整個過程。回查結果見下方。

閱讀頁特別提醒：這是他對 web 演變的框架，不是完整的歷史。他在意的是**使用者能不能自己動手**：開放的協定或可改的應用，留了空間讓人做新流程；封閉產品則只能等廠商排優先序。

### 3. ArtCraft 的起點：藝術家自己 vibe coding（1:27:32–1:29:56）

- ArtCraft 一開始是「專業取向的 Higgsfield」：給電影人用的生成式工具，而不是 Higgsfield、OpenArt 那種 UGC 取向。做成**桌面工具**，生成的檔案就放在使用者的剪輯軟體旁邊，不鎖在雲端服務裡。公司從一開始就把桌面應用和基礎設施都開源。
- 顧問認為他瘋了：藝術家不懂也不需要開源，GIMP 也沒有藝術家在用。結果他們**觀察到藝術家在 ArtCraft 上用 agent 自己寫流程**。
- 具體例子：替頭部短劇新創做外包的 micro drama 工作室，每月接 3 到 5 萬美元的案子，團隊很大，沒有任何產品符合他們特定的交付流程，也不會有廠商替他們量身打造。但他們內部有人會用 Claude Code（逐字稿辨識成 cloud code），可以拿 API 自己生出合用的介面。
- 由此得出新的開源理由：客戶不想當維護者，也不需要懂所有實作，他們要的是**把用不到的介面全部拿掉**，把應用收斂到自己的流程。他設想同一團隊裡每個負責不同環節的藝術家，各有一個 5 到 10 個版本中的專屬受限版。他的結論是：如果應用的「形狀」和基礎設施都開源，人們能創作的空間會大很多，而 AI 是做到這件事的手段。

### 4. 重做 Photoshop 的做法（1:30:00–1:31:44）

這段是整場唯一講到具體方法的地方：

1. **利用模型已經學過的東西**：提示裡直接說「這是修圖軟體的基本形狀；你訓練時看過所有 Photoshop 教學」。
2. **寫一份很大的規格提示**，要求：
   - UI／UX 和底層功能分開；
   - 所有東西都要能透過 MCP 與 CLI 操作；
   - 每個工具各寫一份計畫，說明怎麼運作；
   - 談清楚資料結構與檔案格式匯入器（importer）。
3. **結果**：他說 24 小時內就有「相當不錯的 Photoshop 近似品」，能用、很眼熟，啟動比原版快 10 倍。
4. **他自己劃的界線**：沒有涵蓋 Photoshop 全部功能，還不到 100% 對等。他們拿「該做的事」當基準量，從 50% 做到剛過 60%，並引 Pareto 法則說假以時日可以到 99.99%。

**為什麼先仿介面**：團隊討論過要直接做新東西，還是先追求對等。決定先照搬 Adobe 的介面和手感，讓藝術家的肌肉記憶直接用得上；之後才做「更 agentic」的新介面。另一個目的是**證明**：他們確實「完全靠 agent」做出了真東西。之後依同樣方式做了 InDesign 和 Premiere 的對應版本。

閱讀頁的提醒：一天做出的是「功能上的近似」，不是功能對等；外觀相同不代表每個流程和檔案格式都與原版行為一致。

### 5. 爆紅與反 AI 藝術家的轉向（1:31:54–1:32:55）

- 他原本還沒打算發 Hacker News，消息先在 Reddit 傳開，兩天後《紐約時報》就來邀訪。Discord 從 3,000 人成長到他說比 Suno、Higgsfield 等社群還大（逐字稿另有一個辨識為「Jev」的名稱，無法判斷是什麼）。
- 他的解讀：很多人覺得被 Adobe 和其他科技公司虧待，這個專案「戳中了神經」。
- 原本反 AI 的藝術家開始說「我們其實很喜歡你們做的事」，開始用、回報 bug、提功能需求。他想藉這個機會教他們 MCP 是什麼、怎麼用 agent 創作，再逐步拿掉臃腫的介面。

### 6. 擴張：從創作工具到 Office（1:32:57–1:36:51）

- **範圍**：CAD、Flash、數位音訊工作站（DAW）、Microsoft Office 的核心應用、Google Docs；有些由他們做，有些來自社群。公司和大學都來詢問。
- **PdfCraft**：他說這是目前最成熟、「ready to go」的一個，可以取代 Acrobat，能在 Linux 和 NetBSD 上跑。
- **Figma 對應版**：連伺服器端也做了，可以多人協作（逐字稿寫「wrapped Paxos multi-user setup」，原意不確定）。他說基礎設施和資料模型全部開源，沒有保留任何專有部分。
- **SolidCraft**：社群工程師主導的 3D CAD，有開放的工程核心，可以透過 MCP 很快做 3D 列印專案。
- **他給的規模數字**：超過 30 萬 GitHub star、4,000 位貢獻者、每天約 170 萬次下載且還在加速、四分之一使用者在 Linux、社群在開發 300 多個應用。
- **其他**：有一個 launcher 統一管理所有應用；所有應用都把 MCP 與 CLI 當一級介面，可以看著 agent 組出創作專案；做了 Adobe、Microsoft 沒正式支援的語言（他說 InDesign 不支援阿拉伯文）；接手 Adobe Animate 這類進入維護末期的產品，因為有動畫工作室說他們靠它吃飯。
- **元件化**：做了一個讓非技術人員也能貢獻的應用，並把 UI／UX 函式庫拆成可重用的 2D、3D 元件與基礎單元。

閱讀頁的提醒：應用清單很長，不代表每一個都能用在所有專業流程上；隨著範圍擴大，他自己劃的「近似 vs 對等」界線更重要。

### 7. 技術段：Rust、CI 與 review 分流（1:36:53–1:38:40）

- **為什麼選 Rust**（投影片列出：原生效能、安裝檔大小、記憶體用量、記憶體安全、缺陷率、冷啟動）：他說有人用 Electron 做過，但高品質創作應用需要原生；引用「Google 有論文說缺陷率低」；啟動快；支援各平台，包括 NetBSD 和平板，還能經 Wasm 部署到 web。閱讀頁提醒：這是他的架構論證，不是證明每個 Rust 應用每一項都贏的 benchmark。
- **不會 Rust 也能用**：他本人從 1.0 之前就寫 Rust，但團隊裡有完全沒碰過這語言的人，「你的 agent 會開得很好」。**最大的問題是編譯時間。** Rust 已經能做豐富的 GUI 應用。
- **踩過的坑**：權限、GitHub、規模化、CI。CI 撐不住（「falling over」），他們開始自己架 runner，找到記憶體便宜的機房託管主機，正在遷過去。閱讀頁的解讀：產生改動變快，不會讓編譯、測試、託管和協調的成本消失，瓶頸只是移位。
- **agent 開發 vs 人工 review**：
  - 後端、需要 schema migration 或 API 設計的工作，**讓人來做**；
  - 桌面應用、遊戲，以及「基本上不可變」（basically immutable）的東西，**把 agent 丟上去並給予完全信任**，人不必全程在迴圈裡，只要在上游決定方向。
  - 例子：社群有人用 40 台機器讓 agent 用 Rust 重寫 Unreal Engine。

### 8. Autocraft：開源的軟體工廠（1:38:49–1:39:38）

他把 Autocraft 描述為「完全自主的軟體工廠」：接 issue、分類排序、用 agent 開發，並把所有決策拿來做 eval 與 post-training；整個「應用工廠」用程式碼定義，他稱之為「開源版的 CodeRabbit」，能「讓工程師保持專注」。演講中說「很快會開源」。

### 9. 結尾

把各種平台重新做成真正的協定，「擁有我們的應用、基礎設施、協定、模型」；徵才，強調全部程式碼開源、員工有時間做自己的專案。

## 回查結果（2026-11-19）

| 演講說法 | 回查結果 | 依據 |
|---|---|---|
| 超過 30 萬 GitHub star | **成立，但是全組織加總**：`storytold` 組織所有 repo 的 star 合計約 30.3 萬。單一 repo 最高是 PhotoCraft 約 8 萬，其次 ArtCraft 本體約 4.2 萬、Craft Anything 約 3.7 萬、PdfCraft 約 2.1 萬。另外 SolidCraft 在別的組織（`tangency-labs`），約 1.7 萬 | GitHub API |
| 爆紅一個月 | **時間對得上**：PhotoCraft、PdfCraft、FilmCraft 等主要 repo 建立於 2026-09-30，WordCraft、GridCraft、CADCraft 等在 10 月上中旬陸續建立，距演講約 6 週 | GitHub API |
| 重做 Photoshop，功能對等約 60% | **repo 存在，對等百分比查不到**：PhotoCraft README 寫明是「clean-room reimplementation of Adobe Photoshop, rebuilt in pure Rust」，狀態標「early alpha」，支援 macOS、Windows、Linux、FreeBSD 與 Web。README 沒有對等百分比，也沒交代「該做的事」清單怎麼定 | [PhotoCraft README](https://github.com/storytold/photocraft) |
| 所有東西 MCP 與 CLI 可操作 | **成立（以 PhotoCraft 為例）**：README 說每個選單、工具和對話框都執行同一個 500 多個命令的 registry，UI、CLI、JSON control channel 和 MCP server 共用；有 `photocraft-cli run`、`batch` 和 `mcp` 子命令 | 同上 |
| 4,000 位貢獻者 | **無法核實**：PhotoCraft 單一 repo 的 contributors 清單（含匿名）約 600 筆，全組織不重複人數沒有現成數據 | GitHub API |
| Discord 從 3,000 人成長到比其他 AI 創作社群大 | **成長幅度成立**：ArtCraft Discord 邀請連結回報約 22 萬成員。是否大於 Suno、Higgsfield 沒有查證 | Discord invite API |
| 每天約 170 萬次下載 | **無法核實，GitHub 數據看起來低很多**：PhotoCraft、PdfCraft、craft-launcher 三個 repo 的 release 下載累計各約 545 萬、457 萬、759 萬，合計約 1,760 萬，分攤到約 7 週約每天 36 萬。他們可能還有其他發行管道，所以這只能說明 GitHub 這部分支撐不了 170 萬／天 | GitHub API（release asset `download_count`） |
| Adobe 月繳方案退訂要付最多約 200 美元，寫在小字 | **機制成立，細節不準**：FTC 2024 年控告 Adobe，指控對「年約月繳」方案在第一年內取消收**剩餘月費的 50%** 作為提前解約費，並把揭露藏在小字和需要 hover 的圖示裡。是年約，不是他說的 12 或 18 個月；200 美元是他的個人估算。Engadget 2026-03 報導 Adobe 同意和解（7,500 萬美元付給司法部，另提供 7,500 萬美元的免費服務），仍待法院核准 | [FTC 新聞稿](https://ftc.gov/news-events/news/press-releases/2024/06/ftc-takes-action-against-adobe-executives-hiding-fees-preventing-consumers-easily-cancelling)、[Engadget](https://www.engadget.com/big-tech/adobe-agrees-to-pay-settlement-for-making-its-subscriptions-hard-to-cancel-210336635.html) |
| Google 有論文說 Rust 缺陷率低 | **有一手來源，但情境是 Android**：Google 安全部落格〈Rust in Android: move fast and fix things〉說記憶體安全漏洞密度比 Android 的 C／C++ 低約 1000 倍；中大型改動的 rollback 率低約 4 倍；code review 時間少約 25%；同規模改動需要的修訂少約 20%。這是 Google 內部資料，不是同儕審查論文，也不等於桌面創作應用的缺陷率 | [Google 部落格](https://blog.google/security/rust-in-android-move-fast-fix-things/) |
| Autocraft「很快會開源」 | **已公開**：[`storytold/autocraft`](https://github.com/storytold/autocraft) 已是公開 repo（Apache-2.0；repo 建立日 2026-11-05，比演講早一週，可能先私有後公開，公開日無法確認）。細節見下節 | GitHub |

### Autocraft 實際長什麼樣（讀 README 前半，未實際安裝）

README 把它定位為「維護 backlog 很大的 GitHub repo 的 model harness」，比演講的「完全自主軟體工廠」保守很多：

- **流程**：把所有 issue、PR 和留言每分鐘同步到本地 SQLite，再依序跑 Sync → Duplicates → Classify → Priority → Decide → Label → Review → Fix → Fix-up → Verify → Merge queue → Act → Post-merge review。
- **模型分工**：分類、排序、找重複用一個叫 Jev 的分類模型（README 寫是 TypeSafe 的 Jev，沒有它就由 Haiku 代替）加 Claude Haiku 第二意見、Sonnet／Opus 當仲裁；review 由 Opus 讀整個 repo 給判定和完整修正清單；修 bug 由 Sonnet／Opus 寫 patch、在沙箱測、開 PR。合併前 Opus 會用對抗方式、獨立於第一輪再 review 一次 head commit；合併後 Opus 再做一次 post-merge review，把缺陷開成後續 issue。
- **人在哪裡**：README 明說「pipeline 是圍繞維護者的判斷建的，那才是稀缺資源，不是 token 成本」。每個階段都有「停下來等人」的條件：重複判定、範圍爭議、不符規則的合併、每個 repo 的寫入權限都要 operator 核准，而且核准只能在 dashboard 上給，不能從 CLI 設。
- **信任邊界**：不可信的程式碼只在另一個 OS 使用者的 rootless Podman 裡跑；會用工具的模型呼叫跑在 bubblewrap 沙箱裡，只拿到唯讀 checkout 和唯讀查詢工具；所有 GitHub 寫入集中在單一檔案 `src/github/write.ts`，有稽核表，而且有測試在別的檔案也寫入時會失敗；有全域與每個 repo 的開關、每一步有每日上限。
- **依賴**：Node、`gh`、Claude Code CLI（所有 Claude 呼叫都走它）、bubblewrap，Podman 可選。
- 演講提到的「用決策做 post-training」在我讀到的 README 前半沒有出現，**未確認**。

## 可以搬到個人 Claude Code／Codex 流程的做法

### 1. 重做一個「模型很熟」的工具：大規格提示

適用：要做的東西有廣為人知的原型（某個 CLI、某類編輯器、某個 SaaS 的子集）。

1. 第一段直接點名原型，請模型列出它對原型的理解（工具、選單、資料模型、檔案格式），自己先校正錯誤。
2. 規格裡固定寫四件事：核心邏輯與 UI 分層；每個動作都是命令，可以從 CLI（之後再加 MCP）呼叫；每個工具或子功能各一份計畫；資料結構與匯入／匯出格式。
3. 先做「最常用的 20%」，用一份功能清單當對等基準，並寫下清單怎麼定的，否則「60%」沒有意義。
4. 每個匯入器都要用真實檔案做往返測試（讀進來、存出去、和原檔比對）。PhotoCraft 的做法是拿原版自己的合成結果當 oracle 比對渲染結果，這比「看起來很像」可靠得多。

### 2. 把「每個動作都是命令」當架構原則

這是本場最值得搬的設計：UI、CLI、MCP 共用同一個命令 registry。好處是 agent 能自己操作與驗證你的應用（不用模擬點擊），也能寫批次腳本。和 [[Lauren-Tan-把糾正寫進程式庫]] 的「skill 內附自訂 CLI 讓 agent 重複驗證」是同一件事從應用端做起。即使只是個人小工具，新功能先加 CLI 子命令再接 UI，成本很低。

### 3. 依「錯了能不能收回」分配自主度

他的分法可以直接寫成規則：

- **人主導**：schema migration、對外 API 設計、後端資料模型。在 `AGENTS.md` 寫明這些路徑要先出計畫等確認，並用 hook 或 CODEOWNERS 之類的路徑規則強制，不要只靠散文。
- **agent 放手**：前端畫面、桌面應用的介面、遊戲邏輯、一次性腳本。

但要修正他的說法：桌面應用**不是**「不可變」的。匯入器和存檔邏輯會寫使用者的檔案，壞了就是資料遺失，是單向門。所以檔案格式的讀寫要歸到「人主導」或至少「有往返測試才放行」那一邊。

### 4. 預先準備 CI 容量

agent 產改動的速度一上去，CI 先倒。編譯慢的語言（Rust、C++）尤其明顯。個人專案可以先做的：開啟編譯快取、只在 PR 跑完整矩陣、必要時用自架 runner。換到編譯慢的語言前，先把這筆成本算進去。

### 5. Autocraft 的可抄部分

整套 Autocraft 是為「backlog 很大、有大量外部貢獻者」的開源專案設計的，要跑 dashboard、OAuth App、多個模型帳號，**個人專案用不上**。值得抄的是它的安全設計：

- 所有對外寫入（GitHub comment、label、merge）集中在一個模組，用測試保證沒有別的檔案在寫；
- 每個 repo 的寫入權限要人在 UI 上開，不能從 CLI 自己打開；
- 會用工具的模型呼叫在唯讀沙箱裡跑；
- 合併前由另一個模型呼叫「獨立、對抗式」再看一次。

### 不能直接搬的

- **「24 小時重做 Photoshop」**：沒有公開提示詞、模型、花費、人力投入，也沒有當天的版本可看，無法重現。
- **「不懂 Rust 也沒關係」**：只對「讓 agent 寫、自己不必逐行讀」的工作成立。一旦要自己 debug 編譯錯誤或 lifetime 問題，還是需要語言知識；這是他的團隊經驗，不是對照結果。
- **用決策做 post-training**：需要自己的模型與訓練管線，個人用 Claude Code／Codex 做不到。

## 證據強度與限制

| 主張 | 強度 |
|---|---|
| 24 小時做出能用的 Photoshop 近似品 | 講者自報、單一案例，無公開可重現的材料 |
| 啟動比原版快 10 倍 | 講者自報，沒有量測方法 |
| 功能對等 50% → 60%，最終可達 99.99% | 講者自報；基準清單未公開；99.99% 是推測 |
| star、Discord 規模 | 經 GitHub API、Discord API 部分核實（見回查表） |
| 4,000 貢獻者、300 多個社群應用、四分之一使用者在 Linux | 講者自報，未核實 |
| 每天 170 萬次下載 | 講者自報；GitHub release 數據遠低於此，**引用前要重查** |
| 藝術家用 agent 自己寫流程、反 AI 藝術家轉向 | 講者觀察的軼聞，沒有數據 |
| Rust 缺陷率低 | 有 Google 一手資料，但限 Android 系統程式碼情境 |

整場沒有任何對照：沒有比較「用 agent」和「不用 agent」做同樣東西的成本，也沒有交代模型、token 花費與人力。

### 勿引用

- 「Adobe 在 12 或 18 個月內取消就收約 200 美元」：條件和金額都不準，應引用 FTC 起訴書的「年約第一年內取消，收剩餘月費的 50%」。
- 「ArtCraft 單一 repo 有 30 萬 star」：30 萬是整個組織加總，單一 repo 最高約 8 萬（2026-11-19）。

## 與既有頁的關係

- [[AI-Engineer-2026-演講精華-AI-工作流程]] 是同屆 28 場的綜合，本頁是其中 Thomas 一場的深讀。
- 和 [[Lauren-Tan-把糾正寫進程式庫]] **有張力**：Tan 主張先穩內圈（架構、lint、驗證）再自動化，否則自動化只會量產 slop；Thomas 說桌面應用「給 agent 完全信任」。不過從 repo 看，PhotoCraft 其實有 SonarCloud、CodeRabbit 和對照原版輸出的 oracle，Autocraft 也有多層 review 和人工核准。他嘴上說的放手，實際上有一層驗證撐著；演講只是沒講這部分。
- [[Matt-Pocock-的-PR-瓶頸解法]] 用「單向門／雙向門」判斷 review 強度，和 Thomas 的分流同一個方向。差別是 Matt 提醒小 diff 也可能是單向門，正好反駁「桌面應用不可變」的說法。
- [[AI-產碼加速下的-review-瓶頸]] 指出 review 之後還有下游佇列；Thomas 的「CI 撐不住、改自架」是瓶頸移到 build／CI 的實例（他的自報經驗）。
- [[Claude-Code-放手運行的安全與驗證]] 整理了沙箱、deny、CI 的分工；Autocraft 的唯讀 bubblewrap 沙箱、單一寫入模組、per-repo 核准，是同一套思路在多 repo 維運上的做法。
- [[AI-自主工作流的實證檢驗]] 的結論是 vendor 敘事多、獨立實證少；本場的「60% 對等」「24 小時」正好是沒有定義基準、無法重現的典型。

## 張力與限制

- **「clean-room」與做法的落差**：PhotoCraft README 說只依公開規格與觀察到的行為實作、不含專有程式碼。但演講描述的做法是直接叫模型調用它對 Photoshop 的訓練知識。傳統 clean-room 靠兩組人隔離來證明沒有接觸原始碼，靠模型記憶來實作能不能算 clean-room，演講沒有討論；本頁不做法律判斷，只標出這個問題。
- **仿介面的長期成本**：先照搬 Adobe 的介面是為了讓藝術家沿用肌肉記憶，但他也說之後要做「更 agentic」的新介面。兩條路線同時維護，或之後要使用者再學一次，演講沒有交代怎麼處理。
- **規模與成熟度**：清單上的應用多數在 README 標 early alpha。PdfCraft 被他稱為最成熟，但本頁沒有實際安裝測試。
- **維護量**：數萬 star、數千個 open issue（PhotoCraft 回查時約 5,600 個 open issue／PR）正是 Autocraft 要處理的問題；能不能靠 agent 長期維護這麼多應用，目前還看不出結果。
