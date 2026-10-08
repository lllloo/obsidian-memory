---
title: 用 Claude Code 搭配 Opus 5.5 打造出色網站
description: 從零開始的建站教學，涵蓋環境與基本指令，再走規劃、CLAUDE.md、反 AI 樣板 skill、design.md、部署與 3D 捲動網站六個階段
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=DP7mgLUKN_U
published: 2026-09-30
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - web-design
  - design-system
  - frontend
  - workflow
---

多數 AI 生成的網站看起來大同小異，問題不在模型，而在沒有一套結構化流程。影片以建築設計公司 Forma 的示範網站為例，走完六個階段。

## 環境準備

| 工具 | 用途 |
|---|---|
| Claude Code | 能實際操作整台電腦的 Claude |
| Warp | terminal，執行 Claude Code 用 |
| VS Code | 檢視 Claude Code 建立與修改的檔案 |

- 從官網下載安裝 Warp（Mac／Windows）
- Claude Code 官網不要按安裝按鈕，往下捲選 terminal 選項，複製對應作業系統的安裝指令貼進 Warp 執行，裝好後輸入 `claude` 啟動
- VS Code 開啟與 Warp 相同的資料夾，即可看到 Claude 建立的檔案
- Warp 用 `Cmd+T` 開新分頁（同一資料夾），可再開一個 Claude Code session；要換資料夾先用 `/exit` 結束 session 回到 terminal

基本 terminal 指令：

```
ls            # 列出目前資料夾的檔案與子資料夾
cd ..         # 回上一層
mkdir <名稱>  # 建新資料夾
cd <名稱>     # 進入資料夾
claude        # 在當前資料夾開 Claude Code session
```

## Claude Code 基本操作

- 輸入 `/` 查看可用指令
- `/model` 切換模型：本片用 Opus 5.5（設計表現最好）；簡單任務用 Sonnet，更複雜的任務用 Fable
- `Esc`：中斷 Claude 並給修正
- `@檔名`：把特定檔案納入 prompt
- `/context`：查看 context window 用量
- `/compact`：對話太長時摘要以釋放空間，可指定摘要要保留什麼
- `/clear`：轉換到另一個任務時開全新對話
- 與 Claude 網頁版不同，離開再開 Claude Code 對話不會保存：用 `/rename` 存下對話、`/resume` 叫回
- 按兩次 `Esc`：回到先前某則訊息、撤銷之後的修改

基本流程：在專案資料夾開 Claude Code，說要建什麼，需要更多控制時再用上述指令。

## 階段一：規劃（plan mode）

plan mode 禁止 Claude Code 建立或修改檔案，只能與你對話，促使它想得更深、問更具體的問題，避免把時間花在錯的方向。用 `/plan` 或 `Shift+Tab` 啟用。

給初始 prompt 說明要做什麼樣的 landing page 後，Claude 依序問了：

- tech stack：選 Next.js（建這類漂亮網站最簡單快速）
- landing page 要有哪些區塊（網站結構）
- 設計風格、是否已有網站內容

答完後 Claude 提出包含「要建什麼、怎麼建」的計畫。執行時可選開 auto mode 直接開工，或在第三個選項寫下對計畫的修改。

完成後請 Claude 啟動網站，它在背景執行並給一個 localhost 連結：只在你的電腦上有效、無法分享，Claude session 結束就失效。

結果：照計畫建好、還從網路抓了圖片，但版面仍是熟悉的 AI 生成樣貌。

## 階段二：`CLAUDE.md` 寫入商業脈絡

新 session 對這個資料夾先前發生的事毫無記憶。`CLAUDE.md` 的內容會在每次對話開頭注入 context window。

可用 `/init` 讓 Claude 檢視專案後產出初版，但在簡單專案上它只會寫怎麼啟動 app、程式碼裡有什麼，**漏掉最重要的資訊：為什麼要建這個網站、每個區塊的目的**。影片的初版有啟動方式、專案簡介與檔案組織，但缺商業脈絡，於是直接請 Claude 補上 Forma 的商業脈絡：

- 這間公司是做什麼的
- 顧客為什麼會來這個網站
- 網站要為業務達成什麼（把訪客轉成客戶）

重要性：之後會反覆修改網站，一致的 `CLAUDE.md` 能在多次修改中維持網站的核心意圖——對 Forma 而言是為建築設計公司開發潛在客戶，每個區塊的內容與設計都應反映這點。

## 階段三：Hallmark skill 擺脫 AI 樣板設計

skill 是一份針對特定工作的指示檔，可像 slash command 一樣輸入名稱呼叫。**Hallmark** 給 Claude Code 一套規則，避開 AI agent 最常用的設計模式；對既有專案，Claude 會拿成果對照 Hallmark 規則檢查。

安裝：從 Hallmark 網站取得安裝指令。不必關掉 Claude Code——在輸入框開頭打 `!` 進入 terminal 模式，貼上指令執行即可。

用 `/hallmark` 要求重建網站：它只問了視覺風格，沒問任何商業相關問題，因為產品已定義在 `CLAUDE.md`。產出與初版差異很大：不再沿用原本的排列、設計更精緻有規劃感、間距與版面更講究，最重要的是不像 AI 生成。

## 階段四：`design.md` 鎖定色彩與字型

design skill 能改版面、間距與元素擺放，但模型仍會用訓練時的預設色彩與字型。例如 Claude 的 Opus 模型做網站總是預設暖奶油色或米白色，不論搭配哪個 design skill。

`design.md` 類似 `CLAUDE.md`，但記錄網站要用的色彩、字型與間距，用來覆蓋模型的預設設計選擇。有了它，之後新增或修改元素，甚至整站改版，色彩與字型都能保持一致。

取得方式：

- 不必自己寫，可到 aura.build 瀏覽大量現成的 `design.md`，挑喜歡的下載
- 要完全符合自家品牌的獨特設計，頻道付費社群另有 design.md planner skill

套用步驟：

1. 把下載的檔案複製到網站專案資料夾，改名為 `design.md` 方便在 prompt 中指稱
2. 請 Claude Code 讀 `design.md` 並依此改版網站，同一個 prompt 中要求保留現有頁面結構與動畫

結果：整體結構不變，但配色、字型、間距完全換新；之後再改版面或加元素都會遵守 `design.md` 的設計規則，是維持視覺品牌一致的關鍵。

## 階段五：GitHub 與 Vercel 部署

**GitHub 與 commit**：GitHub 像存程式碼的 Google Drive。加新功能時舊功能可能壞掉，所以要先存檔，每個存檔點叫 commit，可直接請 Claude Code 在 commit 間切換；新功能有問題就回到上一個 commit。請 Claude 在專案初始化 Git 並建 commit，之後每加新功能都建新 commit。

- 在自己電腦上的是 local commit；推到 GitHub 的 repository 後成為 remote commit
- 有新的 remote commit 時，Vercel 會讀取變更並更新正式網址上的網站

**GitHub 設定**：

1. 建 GitHub 帳號（可用 Google 登入）
2. 請 Claude 安裝並設定 GitHub CLI（讓你用 terminal 指令控制 GitHub）
3. 它會要你執行一個指令：在 Claude Code 的 terminal 模式執行，取得一次性代碼與連結，開連結輸入代碼並授權即完成登入
4. 請 Claude Code 把專案上傳到 private repository

**Vercel 部署**：

1. 建 Vercel 帳號，在 dashboard 選 add new 建新專案
2. 連接 GitHub 帳號、授權存取該 repository，從清單選 import
3. 設定頁維持預設直接繼續，Vercel 會測試並執行專案
4. 若有測試失敗，把 Vercel log 的錯誤交給 Claude 調查
5. 部署成功後在專案 dashboard 取得分配的網域（也可加自訂網域）

之後改為安裝 Vercel CLI（同樣請 Claude Code 安裝、依指示登入授權），部署出問題時 Claude Code 能自己用 CLI 抓取並修正，不必手動操作。

## 階段六：Scroll World 3D 捲動網站

先建簡單網站是為了把建站基礎打好。**Scroll World** skill 能做出捲動時鏡頭穿越一連串 3D 電影感場景的頁面，場景由生成式 AI 影片工具產生。安裝：到 Scroll World 的 GitHub repo 取得安裝指令，逐一貼進 Claude Code 執行。

**先開 Git branch**：branch 是專案的副本，每個 branch 有自己的 commit；原本的是 main branch，在把 commit 合併回去前保持不動。合併稱為 merge，GitHub 要求 merge 前先經過審查，即 pull request。先開新 branch 再做 Scroll World，正式網站在捲動版完成前維持原樣。

**規劃與實作**：

- 執行 `/scroll-world` 啟動規劃，它會問世界的背景脈絡、外觀、鏡頭如何移動，以及是否要行動版
- 選桌機與行動版兩者，規劃了 18 段影片（各 9 段）。不必自己描述任何片段，skill 會用給定脈絡與 `CLAUDE.md` 自行規劃，不滿意隨時可修改
- skill 的文件化流程預設用 Higgsfield 生成影片、Manus 為備援；影片改用 Runway。換用其他平台時**務必確認該平台有 MCP**，因為 skill 透過 MCP 取得影片

成果：捲動時鏡頭穿越五個階段的故事，每階段有自己的動畫、轉場串成完整旅程；行動版使用為手機螢幕比例製作的獨立影片，而非裁切桌機版。

## PR 審查與合併（贊助商 CodeRabbit）

捲動版取代正式網站前要走 pull request。可以請 Claude Code 審 PR，影片則示範贊助商 CodeRabbit：

- 申請試用（目前 14 天）、選 GitHub Cloud 並用 GitHub 帳號登入、add repositories 授權要審的專案
- 開 PR 後自動開始審查變更檔案，標出可能的 bug 與安全問題並提出修正；PR 檔案多，約 15 分鐘完成
- 產出變更導覽與 sequence diagram；review change stack 把變更分成五層，其中兩層標為有風險，共找到 11 個問題，依 major／minor 排序
- 每個問題附一段可直接貼給 Claude Code 的 prompt，已含問題脈絡
- 內建 AI agent 可問答（例如這些變更對網站有什麼影響），也可要求自動修正，產生 patch 供檢視後 commit 回 PR

修完重要問題後 merge PR，捲動版併入 main 並更新正式網站。

**AI deep scan**：掃整個 repository 而非單一 PR。網站有表單、使用者能互動就可能有安全問題；實測找到表單 email 欄位的安全風險，按 fix 後 AI agent 修正並開新 PR 推上。
