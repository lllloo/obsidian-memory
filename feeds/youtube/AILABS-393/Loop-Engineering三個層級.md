---
title: Claude Code Loop Engineering 的每個層級
description: 從單一 goal 迴圈、多功能軟體工廠到脫離電腦的手機操作，拆解 agent 自我驗證迴圈的組成、分工規則與 GitHub/Supabase/Vercel 串接方式。
created: 2026-08-19
updated: 2026-08-19
source: https://www.youtube.com/watch?v=PLyRe6Zk--8
published: 2026-08-18
parent: "[[01.index]]"
tags:
  - youtube
  - loop-engineering
  - claude-code
  - sub-agent
  - workflow
---

## 什麼是 agent loop

過去用 agent 建東西時，你其實已經在一個迴圈裡：你給 prompt、agent 建、建完你驗證、錯了再給下一個 prompt。所謂 agent loop，就是把「你」從這個流程中移除，把驗證那一段也交給 agent。

- 真正吃時間的不是「建」——那部分 agent 本來就能背景自主完成——而是「檢查 agent 有沒有做對」。
- agent 要能自行驗證，前提是它知道正確輸出長什麼樣。這是迴圈的核心。
- 迴圈的組成：（1）啟動迴圈的東西、（2）迴圈本體、（3）每一輪結尾的驗證檢查，決定 agent 是否算完成。
- **驗證檢查的標準由你定義**，這一塊交不出去；agent loop 裡你保留的，正好是本來就該屬於你的那一塊：決定要不要關掉 agent。
- 為何現在才談 loop engineering：一年前的模型跑不了這麼久，新模型可以連續數小時自主運作。

影片以 Claude Code 示範，但同一套系統在 Codex 上也適用；工具用 Warp 與 VS Code，兩邊各開同一個資料夾即可跟著做。

## 專案與前置檔案

示範專案是一個美髮沙龍預約 app（Next.js）：使用者選設計師、看不同日期的空檔並預約；另有店員登入端，負責核准／拒絕請求與管理各設計師行事曆。

資料夾內幾個關鍵檔案：

- `CLAUDE.md`：內容只寫「去看 `AGENTS.md`」。因為這個 repo 可能不只跑 Claude Code 一種 agent，而幾乎其他所有 agent 都讀 `AGENTS.md` 當新 session 的規則來源，只有 Claude Code 讀 `CLAUDE.md`。
- `design.functional.md`：涵蓋 app 中所有使用者實際會操作的可點擊部分。
- 視覺設計另有一份檔案，此例直接把 Duolingo 的設計複製進來當風格基準。
- `grill-me` skill：不斷追問，直到 agent 真的搞清楚你要什麼。

**MVP 不要上 loop**：新專案第一件事是做最粗糙的可用版本，只做主要功能。要在它上面套迴圈，得先定義「完成」長什麼樣，但那個階段你還不知道產品要往哪走，定義完成反而比自己直接做第一版更花時間。

## Level 1：單一目標的 loop

一個迴圈、一個目標，檢查工作從你身上移到 agent 身上。示範對象是 landing page——乍看是錯的選擇，因為 landing page 只有一個畫面，agent 一次就能建好、錯了一個 prompt 就能修，套迴圈的成本比頁面本身還高。

但此例要的是用 GSAP skill 做的重動畫 landing page，所有元素都是動畫進場。動畫沒辦法看一眼就驗證，agent 出錯的地方很多、需要大量來回。

> **判斷是否該上 loop 的準則**：這件事是否需要跟 agent 大量來回。

### `/loop` 與 `/goal` 的差別

Claude Code 的斜線選單裡有兩個容易混淆的命令：

- `/loop`：把一個 prompt 掛在計時器上，每 5 分鐘或每小時就再跑一次，不管有沒有變化。
- `/goal`：**持續工作直到你要求的事真的完成**——loop engineering 講的就是這個。

`/goal` 用法很單純：輸入 `/goal`，寫下要達成的目標，同時告訴模型如何驗證是否達成。每一輪結束時，一個較小的模型會讀過對話，判斷 agent 是否還要再做一輪、條件是否已滿足。

### 實作流程

用 `grill-me` skill 要求它寫一份 feature 的 spec 檔。專案內有 `features/` 資料夾，每個子資料夾代表一個 agent 要完成的功能，各含兩樣東西：

- `spec` 檔：關於該功能的一切都寫在這裡。
- `verification/` 資料夾：一開始是空的，agent 跑迴圈時逐步填入。

告訴它要用哪些 skill：

- **GSAP skill**：產生高度動畫化的 landing page。
- **optimized skill**：重動畫會拖慢頁面，這個 skill 回頭把速度救回來又不拿掉動畫。
- 另給了一張帶插畫的 landing page 圖片當參考。

最關鍵的是驗證方式：告訴它檢查設計時必須使用 global `CLAUDE.md`（套用到整台機器所有專案）中指名的那個截圖工具，因為它比每次開完整瀏覽器快得多。

於是寫出來的東西同時是兩件事：**建頁面的 spec，以及要對該頁面執行的驗證 checklist**。最後再加一句「把這份 spec 寫成 goal」——這句話把 spec 變成可用 `/goal` 直接跑的目標。

為了不用每個功能都重做一次這整套，作者把它包成 **goal-writer skill**：包含上述所有內容（含那關鍵一行），直接在 `features/` 下建好資料夾與已寫成 goal 格式的 spec 檔。

### 結果

agent 跑了第一輪、第二輪，反覆拿 checklist 對自己評分，共執行 38 分鐘後停止，回報一個錯誤：吉祥物的眨眼。補一次修正 prompt 後就正確了。

這個錯誤正是驗證機制本質上抓不到的：**截圖只捕捉單一瞬間，而兩次眨眼之間的間隔太短，兩張截圖抓不到**。其餘插畫成果良好，與主 app 既有的 Duolingo 風格一致，也緊貼參考圖。

## 三個平台的設定

後續所有東西都建立在三樣本機做不到的能力上，且你都不需要親自操作：

| 平台 | 解決的問題 |
|---|---|
| GitHub | 專案目前只有你電腦上一份，硬碟壞或誤刪就全沒了；GitHub 把程式碼放上線存成 repo |
| Supabase | app 還沒有記憶，真實使用者訂了位、重整頁面就消失，需要資料庫 |
| Vercel | app 只跑在你電腦上，別人進不來，需要部署到網路上 |

三個平台你只要用 Google 登入註冊帳號，沒有任何東西要設定，其餘全交給 agent。可行的原因是三者都有 CLI——agent 不能像人一樣點網頁，CLI 就是給 agent 用的平台介面。建 repo、建 Supabase 專案與 Vercel 專案，Claude 都能用 CLI 完成。

註冊完回到 agent，告訴它你要它透過 CLI 使用這三個平台。它會各給你一道命令，你在**另一個終端機**貼上執行（agent 正佔著原本那個）：CLI 會被安裝，接著開瀏覽器登入你的帳號、你按核准，認證就完成了。從此 agent 能在那些平台做所有事，你再也不用開那些網站。

### 平台 skill

平台規則常變，所以官方釋出了給 agent 的 skill：

- GitHub 不太需要——它變動不大，作者沒有做。
- **deploy-to-Vercel skill**：告訴 agent 怎麼用 Vercel CLI 自動部署。
- **Supabase skill 與 Supabase best practices skill**。

這些都是 auto invoke：agent 需要用到就自己會用，你不必做任何事。

## Level 2：軟體工廠迴圈（software factory loop）

一次規劃多個功能並掛上迴圈，讓 agent 整夜照著一份功能清單持續工作，而不是做完一個就停。因為迴圈可能很長，需要一個追蹤器判斷清單是否完成；當清單全部打勾，goal 迴圈才結束。

### 先做 prototype

規劃新功能時不該只寫「要做什麼」，而該實際把 UI 做出來——一個完全可點、但底層不會真的運作的版本。兩個理由：

1. 你能發現「想像中要做的東西」是不是「真正想要的東西」。
2. 這個 prototype 成為跑迴圈的 agent 驗證自己建得對不對的依據。

### 單一項目的內部分工

主 agent 挑起清單上的一項後，並不自己動手：

- 把任務交給 **sub agent** 完成建置。
- 為避免 sub agent 搞砸把 app 弄壞，主 agent 先開一個 branch（資料夾的副本），讓 agent 在上面工作。
- **做事的 agent 絕不驗證自己的工作**——這是 loop engineering 的另一條重要規則。驗證一律交給另一個擁有全新 context window 的 agent。
- 主 agent 把 branch 交給 **adversarial review agent**：這個 agent 必須始終相信工作中存在錯誤，才抓得到 bug。
- review agent 回報問題 → 主 agent 重新啟動 build agent，如此循環直到該功能在清單上被打勾。

### 合併與最終核准

功能完成後要把 branch 的工作放上已部署的 app：GitHub 上的 main 版本就是 Vercel 上顯示的內容，branch 合併進 main，功能就上線。

這裡是你最後把關的地方：功能完成時會開一個 pull request（把 feature branch 合併進 main 的請求），agent 會在 PR 附上截圖。想更保險，可以請 Claude 切到該 branch，在自己電腦上實測後再合併。

### 用到的 skill

- **new-feature skill**：叫 agent 在 `features/` 下建資料夾，每個資料夾要有 `spec.md` 與其他驗證用素材。此例定義了兩個功能：一是列出沙龍每位人員的 services 頁；二是顧客與設計師完成一次服務後，可透過店員（admin）新增評論。
- **goal-writer skill**：這些 skill 彼此串連——不希望某功能變成 goal（只想單純做、不跑迴圈）就別用 goal-writer；用了它就會連帶觸發 new-feature skill，並補上把 spec 變成可執行 goal 的規則。
- **functional-UI skill**：由 new-feature skill 呼叫，要求 app 內要有一個 `mocks/` 資料夾，內含一份 HTML 檔作為整個 app 的完全可運作 prototype，同時具備店員端與顧客端的畫面。每個資料夾只該有一份，已存在就不重建。每建一個新功能，就在該功能資料夾內再加一份 HTML——它拿已複製的 app，只取該功能會改動的部分呈現。
  - 例：services 功能的 mock 顯示會新增一個完整 services 頁並由某個按鈕進入；點 book now 選設計師後，會先問你要哪一項服務。這在正式 app 與 clone 裡都還沒實作，只存在於這份 feature prototype，讓你先看見成品是否符合預期，也成為迴圈驗證的依據。
- **feature-batch skill**：用一份 queue markdown 檔（單一表格）列出所有功能。呼叫 skill 並告訴它要加哪些功能，它會寫好檔案並加入項目，接著給你實際要跑的 goal 命令。此例把 queue 檔放進 goal 執行，**停止條件是沒有任何一列處於 to-do 或 building**（全部進到 done）。

實際運行時，第一個功能建了約 3 小時仍在進行；過程如前述：先派 sub agent 建，再派 adversary agent 檢查驗證。

### 成果

到 GitHub 專案（找不到就叫 agent 給連結）的 pull request 分頁，可以看到 agent 為你的 review 開的 PR：完整摘要加上各頁截圖作為工作完成的證明。review 完就能合併。合併後的線上版本（網址結尾是 vercel，因為還沒接自訂網域）就有了 services 頁，可看到沙龍提供的所有服務；進 book now 會看到每位設計師各自的服務項目，且必須先選服務才能預約。

作者強調 skill 說穿了只是寫在檔案裡的指示，這裡沒有任何你自己做不出來的東西。

## Level 3：脫離電腦

到這裡整個流程只剩兩件事需要你：規劃功能，以及在功能／變更送給使用者前給最終許可。這兩件事都不需要你坐在筆電前——尤其是規劃：你描述想要什麼、它追問到理解為止、再建出 prototype，全都可以在手機上完成；小改動的最終許可也可以在手機上給。

Level 3 的目標就是**移除你對筆電的依賴**，使用的是一個叫 PO 的 app：

- 它在你自己的筆電上跑 agent，並從手機開一個視窗看進去。你的 agent 仍在自己的機器上，所有檔案、skill、已登入的 CLI、以及這支影片建的所有東西都照常運作。
- Claude Code 內建的 remote control 功能也能做類似的事，但很多地方是壞的——例如 skill：remote control 裡沒有可以執行 skill 的選單。PO 是免費的。
- workspace 系統：每個 workspace 就是一個資料夾，裡面可以開不同的對話。它自己會跑 Claude Code，不需要另外的訂閱。
- 不只能跑在筆電上，也能跑在你連線的 Mac mini 上——從筆電控制 Mac mini，從手機也能控制那台 Mac mini。
- 介面比整個終端機介面精緻得多，看起來像 Cursor，但功能都在：`/goal` 可用，其他自製的斜線命令也可用。

手機上的介面與電腦端完全相同，Claude Code 的功能與斜線命令都可直接用。示範中在手機上跑 new-feature 命令實作了先前沒做的顧客端登入流程；除了寫出整份 feature 檔，它還能直接在介面裡給出 mock 的圖片，手機上也看得到，讓你當場驗證 UI。

- **mobile-preview skill**：把 HTML mock 部署成連結（Vercel 上的免費部署）。點連結就進到實際的 mockup，可以真的點來點去操作，而不是只看圖片——用手機經營這座工廠時，這才是你要的。
