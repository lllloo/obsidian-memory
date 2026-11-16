---
title: Lauren Tan 把糾正寫進程式庫
description: Lauren Tan 在 AI Engineer CODE 2026 的主張：每次糾正 agent 都改成程式庫裡的確定性檢查，先穩內圈再自動化外圈，附數字強度與可直接用的 pstack skill
created: 2026-11-16
updated: 2026-11-16
source: https://ai.engineer/code/2026/talks/lauren-tan
published:
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - ai-agent
  - testing
---

# Lauren Tan 把糾正寫進程式庫

來源：AI Engineer CODE 2026 演講〈All Code Is Slop (Except Mine)〉的官方閱讀頁與機器逐字稿，落地於 [[AI-Engineer-CODE-2026-Lauren-Tan-All-Code-Is-Slop]]；工具部分另核對 [pstack README](https://github.com/cursor/plugins/blob/main/pstack/README.md)。

**一句話**：agent 再犯同一個錯時，不要往 `AGENTS.md` 多加一行，而是把這個糾正放進 agent 繞不過的地方：API 設計、架構、lint、型別或驗證。內圈還在產 slop 時就自動化外圈，只會更快產出更多 slop。

## 講者

Lauren Tan，網路代號 poteto。演講中自稱在 SpaceXSI 做 Grok Bot（官方文件站標題就是「Grok Bot | SpaceXSI Docs」，[docs.x.ai/grok-bot](https://docs.x.ai/grok-bot/overview)）。pstack README 自述待過 Meta、Netflix、Cursor，也是 React core team 成員、參與 React Compiler。README 仍寫「ship high quality code at Cursor」，看起來是換工作前寫的，以演講自述為準。

## 信任倒金字塔：時間該花在哪

她把這套做法講成「信任」，不講「軟體工廠」：不是盲目相信 agent，而是投資 agent 的環境，讓你有理由相信它會做對。投影片由寬到窄（官方閱讀頁的圖片說明）：

1. **程式庫本身**：API 設計、架構、重構
2. **靜態分析**：lint、型別、編譯器、各種測試
3. **驗證**：執行期驗證與形式化驗證，用來抓 bug、檢查不變量，也確認 agent 是否理解你的意圖
4. **散文**：rules、skills、`AGENTS.md` 這類需要判斷的指示
5. **人工 review**

前兩層是確定性的，可以讓「做對的事」變成預設。她的理由是：寫在程式裡才可重現，所以比較值得信任；而程式庫是 agent 最大的輸入之一。

**花園比喻**：以前一天 review 同事 3 個 PR，現在比較像 300 個，程式碼像持續流入的活物。workaround、反模式、過時程式和技術債，會被下一個 agent 當成既有慣例照抄，就像雜草蔓延。所以清掉舊的壞範例，本身就是在改善之後的產出，不只是還技術債。

## 四個具體做法

| 做法 | 背景 | 機制 |
|---|---|---|
| 在產品程式禁用 `useEffect` | 「需要細微判斷才能用對的東西，常常會變成 slop」，agent 也用不好 | 只允許出現在自研框架 Dune 的部分 API 內部，整類問題消失，review 不必再抓 |
| 用目錄名稱表達執行環境 | Cursor 裡 agent 常把 main thread 程式 import 進 renderer，造成長任務與卡頓 | 兩個頂層目錄就叫 `electron-main` 與 `electron-renderer`，互相 import 由依賴圖分析器與 lint 擋下 |
| 禁掉約 99% 的註解 | agent 把文件、註解、rules 當成「這次可以不做對」的申辯欄，或把一次小糾正過度推成死規則 | 註解會過時、沒人讀，又無法強制執行；改用 lint，錯誤訊息直接叫 agent 修根因 |
| 計時器的反面教材 | Cursor 裡 agent 大量用 `setTimeout`、`requestAnimationFrame`、`requestIdleCallback` 補 VS Code 命令式與 React 宣告式之間的架構衝突，還寫註解替這種修補辯護 | 計時器蔓延，大量建立與銷毀造成 GC 與卡頓。她的結論是架構選擇本身讓 client 與 agent 的表現都變差 |

閱讀頁特別提醒：禁用 `useEffect` 是這個團隊的在地架構選擇，不是說這個 hook 本身就是錯的。

**通則**：每次糾正 agent，都要變成確定性檢查，或用更好的 API／架構把這類問題整類消掉。做久了 review 能抓的東西會越來越少，最後可以讓 agent 自己合掉大部分 PR。

## 驗證層：review 縮成看證據

Code review 逐漸縮成看驗證產物：影片、截圖、圖、形式化驗證結果。

- **執行期驗證**：讓 agent 自己跑程式，用開發者同樣的除錯工具（例如 Chrome DevTools Protocol）。
- **Feature map**：從使用者視角列出所有功能的「網站地圖」，放在驗證 skill 裡。這樣你講「左邊側欄那個東西」時，agent 不必猜，雙方有共同詞彙。
- **Skill 內附自訂 CLI**：agent 每次重用同一套 CLI 與 driver，省 token，而且這套工具本身可以測試。
- **形式化驗證（實驗中）**：用 TLA+ 對跨裝置、跨平台通知這類主要使用者流程做 model checking；用 Lean 證明自研虛擬化套件不會閃爍或抖動。她說已經抓到不少 bug，但「不是銀彈」，只是環境裡的另一層。
- **UI 的 property-based testing**：用 [Bombadil](https://github.com/antithesishq/bombadil)（Antithesis 開源，repo 描述為 web 與終端 UI 的 property-based testing），也已抓到幾個 UI bug。

**經濟論點**：這些都不是新技術，只是以前太貴、太難寫也太難維護。agent 把成本壓低了，所以她說「we're entering a golden age of software testing and verification」。她引用一位 Cindy 的推文，說每天約 70% 的 token 花在驗證，她自己的用量也差不多。推文原文未查到，這個數字只能當軼聞，**勿引用為量測值**。

## 先穩內圈，再自動化外圈

> 「If your inner coding loop produces slop, then automating that loop just produces more slop.」

順序是：先改善 agent 會照抄的程式庫、把約束做成可執行的檢查、讓 agent 能真的測行為，最後才擴大反覆呼叫 agent 的自動化。她舉的外圈例子：每次切新版，Grok Bot 自動開一個 Cursor project，像真實使用者一樣操作，fuzz 整個 build，每個 bug 開修復 PR 並自動合併。她說能這樣做，是因為程式庫已經好到 PR 預設就不錯，多數產品程式不再需要深度人工 review。

## 數字與證據強度

| 主張 | 強度 |
|---|---|
| 她本人上個月合進生產約 3,000 個 PR，花約六個月才走到這一步 | 講者自報 |
| 團隊上個月約 11,000 個 PR，10 月約 227 人至少貢獻 1 個，穩定版約每天一版 | 團隊自報，無公開資料可核 |
| 相對 revert 率下降並穩定在約 0.5% | 團隊自報；分母、revert 的定義都沒交代 |
| 啟動、打字、開新對話與切換對話都比上線時快 | 團隊自報，沒有給量測方法 |
| 70% token 用在驗證 | 轉述他人推文，原文未查到；**勿引用** |

官方閱讀頁自己也標註：這些是團隊自報的成果，不是能證明「每個 repo 合併量增加後都會變好」的對照實驗。可以搬走的是**做事的順序**，不是數字。

## pstack：把這套做成 skill

[pstack](https://github.com/cursor/plugins/tree/main/pstack) 是她放在 `cursor/plugins` 的 skill 套件，README 附 Claude Code 安裝方式（`/plugin marketplace add cursor/plugins` → `/plugin install pstack@cursor-plugins`；Cursor 專屬功能在 Claude Code 會跳過）。和演講直接對應的幾個：

| skill | 對應演講的哪一段 |
|---|---|
| `/correct` | 核心原則本身：從歷史挖出重複的錯誤類型，用最高能生效的層級修（架構 → 型別／lint／CI → 測試，文件最後），並維護「規則 ↔ 由什麼強制執行」對照表 |
| `/create-verification-skill`、`/maintain-verification-skill` | 執行期驗證與 feature map：替專案產生本地驗證 skill，之後修正 feature map 的漂移 |
| `/create-formal-verification-skill`、`/statechart` | 形式化驗證層：`/statechart` 檢查 TLA+ 模型，畫成使用者視角的 mermaid statechart，標出違規狀態 |
| `/no-comments` | 禁註解：review 前移除註解，並針對註解宣稱的約束提議改用程式強制 |

## 與既有頁的關係

- 和 [[Uncle-Bob-的不讀碼約束閘門]] 是同一個方向的兩個極端案例：兩人都想用機械閘門取代逐行 review。Uncle Bob 的閘門偏測試與度量；Tan 的重心放在更前面的 API 設計與架構，讓錯誤從一開始就寫不出來。兩人都**沒有外部量測**。
- 為 [[用測試約束-AI-產碼]] 的 property-based 層補一個 UI 端的實際案例（Bombadil），並把形式化驗證推到 TLA+／Lean。
- [[不讀碼時該看哪些圖]] 提到「把架構邊界寫成 CI 上會 fail 的依賴規則」，`electron-main`／`electron-renderer` 正是現成的實例。
- [[Agent-Harness-Engineering-框架綜述]] 的非 Anthropic 一手實作分享表收錄了 Mitchell Hashimoto「agent 犯一次錯就工程化一個解法」，和 Tan 的通則同形；Tan 多給了**優先序**：能改架構就不寫 lint，能寫 lint 就不寫散文。

## 張力與限制

- **「刪 harness」不是直接反例**：同場 Philipp Schmid〈[I deleted 90% of my harness](https://ai.engineer/code/2026/talks/philipp-schmid)〉主張在 eval 環境裡移除工具層與 prompt 層的鷹架，並量測 turn、token 與成本。他刪的是替舊模型補缺陷的**工具與指示**；Tan 加的是**程式庫的領域與架構不變量**，模型變強也不會因此失效。兩人反而在「少靠散文」這點上一致。真正的張力只在：拿 lint 補某代模型特有壞習慣（例如偏好某種舊寫法）的那一部分，換新模型時值得重新檢討。
- **禁註解的代價**：「為什麼這樣設計」與業務背景沒有地方寫。pstack 的 `/no-comments` 是把註解裡宣稱的約束轉成程式強制；不能轉成程式的背景知識要放在哪，演講沒有回答。
- **前提是程式庫歸你管**：禁 API、用目錄劃邊界、自研框架都需要對架構有完全的決定權。接手的既有專案要先用 baseline 凍結舊違規，只攔新的違規，才走得下去。
- **規模差異**：上百位貢獻者、每天發版的 Electron client 才養得起 Dune 這種自研框架和 TLA+／Lean。小團隊能直接搬的是前兩層的做法（禁 API、依賴邊界、帶修復指引的 lint 訊息），形式化驗證不一定划算。

## 勿引用（2026-11-16 核對）

- 「把軟體工廠比作米其林廚房」：官方逐字稿與閱讀頁都沒有這句，出處不明。
- Cindy 推文的 70% 數字：見上方強度表。
