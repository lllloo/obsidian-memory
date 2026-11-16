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

**`/correct` 拆解**（2026-11-16 讀 [SKILL.md](https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md) 原文）：只能手動觸發（`disable-model-invocation: true`），全文是一段短 prompt，沒有附腳本。它的設計前提是：把每個貢獻者都當成「只看得到自己打開的檔、照抄最近的範例、走最短能編譯的路」的 agent，所以 repo 要設計成「從單一檔案看起來對的改動，對整個 repo 也是對的」。流程分四步：

1. **找出錯誤類型**：讀最近的 commit、revert、review 意見、agent 指示檔，以及解釋 workaround 的註解，把錯誤歸類。同一類發生過兩次才算數。
2. **用最高能生效的層級修**：架構（state 只有一個 owner、每件事只有一種支援做法、隱藏內部讓錯的 import 直接失敗、手動同步的清單改成單一真相來源、刪掉會被照抄的舊做法）→ 型別（讓錯的狀態寫不出來；還能編譯過的，就加 lint／CI 檢查，錯誤訊息要點名該改用哪個檔案、型別或函式；已經很普遍的寫法只擋新增）→ 測試（修掉或刪掉行為壞了還會過、只改內部就會掛的測試）→ 文件與規則放最後，只用於需要判斷的事，因為 agent 跳過它們時什麼都不會失敗。
3. **修完要證明**：先修最常見的幾類，一類一個 commit。每個新檢查都要證明它在**一個真實發生過的錯誤**上會失敗；本地與 CI 跑同一個指令。例外寫在違規那一行，附原因、到期日與人的核准。
4. **維護規則表**：在 agent 指示檔裡放一張「規則 ↔ 由什麼強制執行」的表。之後每次被糾正就修錯並加規則；規則早就在、卻沒有東西強制執行的，算重犯，要在同一個改動裡升到最高能生效的層級；錯誤已經不可能發生的規則就刪掉。

回報格式：每一類附證據、選了哪一層，以及**為什麼更高的層不行**。注意 README 說它會「mines history」，但 SKILL.md 列的來源都是 repo 內的痕跡，沒有對話紀錄；只在對話中口頭糾正、沒有留在 commit 或 review 裡的錯，它第一輪看不到，要靠第 4 步之後的持續循環補上。

**整體結構**（2026-11-16 依 README 整理）：主入口是 `/poteto-mode`，依任務分派到二十多個 playbook（bug fix、perf、feature、refactoring、shipping、overnight 的 autonomous run／autopilot 等）。其餘 skill 在步驟需要時才觸發，另有一批「一條原則一個 skill」的 principle skill（如 `prove-it-works`、`fix-root-causes`、`encode-lessons-in-structure`），由 `poteto-mode` 在開始任務時讀取索引。委派用專屬的 `poteto-agent` subagent，README 明說換成通用 subagent 會跳過讀規則而漂移。它刻意不附 planning skill（「the best spec is code」）；`/automate-me` 會從你的對話紀錄產生自己的 `<name>-mode`，`/setup-pstack` 則設定各角色用哪個模型。

**在 Claude Code 用的限制**：指令要加前綴（`/pstack:poteto-mode`）；Bugbot、Cursor automations 這類 Cursor 專屬步驟會跳過；第三方 marketplace 預設不自動更新。`/deslop`、`control-ui` 等被引用的 skill 在另一個 `cursor-team-kit` plugin 裡，沒有一起附上。注意 pstack 本身是 prompt，屬於倒金字塔的散文層；`/correct` 才是把糾正往確定性層推的那一個。

### 社群怎麼用（2026-11-16 查）

找得到的大多是移植版和介紹文，**親身使用心得很少**，也沒有任何量測。

- **移植版是主流用法**：[michael-denyer/pstack-claude](https://github.com/michael-denyer/pstack-claude) 在安裝前就把 Cursor 名稱轉成 Claude Code、Codex、Copilot、Pi 等 harness 的名稱（官方 Claude Code 版是讓 agent 在執行時自己轉換，多花 token），並加了 `SessionStart` 路由 hook，大任務時 `poteto-mode` 會自己啟動；它追上游，另外維護具名的政策分支。[backnotprop/pstack](https://github.com/backnotprop/pstack) 是同步上游的鏡像，用 `npx skills add backnotprop/pstack` 安裝時**可以只勾選要的 skill**。兩者的 GitHub star 數都在數千級（查詢當下）。
- **Flavio Copes 的使用建議**（[A deep dive into pstack](https://flaviocopes.com/pstack/)，屬於個人看法）：只把 pstack 用在「看起來合理的 diff 還不夠」的工作上，例如要重現的 webhook 重複寄信、大型遷移、難搞的效能問題、可以早上驗收的 overnight run；改一個設定值或一句文字就不用整套。多個 agent 都用 frontier 模型，token 很快就燒完，所以例行工作用便宜模型，用 `/setup-pstack` 分配角色。prompt 的形狀是「現象＋完成條件（agent 能跑或檢查的東西）＋不能改變的行為」。
- **Hermes 版的行為揭露**（[Hermes Marketplace 的 pstack 頁](https://hermes-agent.nousresearch.com/docs/plugins/pstack)）：autopilot、shipping、babysit 會 push 並 force-push agent 自己的分支、squash-merge PR；`reflect` 會不逐項詢問就在 tracker 開 backlog issue。上游 playbook 原文核對結果一致：shipping 用 `gh pr merge <pr> --squash`，autopilot-full 用 `--force-with-lease` force-push 自己的分支。
- **會對外動作的 playbook 不只 autopilot／shipping**（2026-11-16 逐檔讀本機安裝的上游 `skills/poteto-mode/playbooks/`）：`autopilot-full`（push、force-push 自己的分支、merge）、`shipping`（`gh pr merge --squash`、retarget 後 force-push 上層 PR）、`orchestrate`（每個 PR 的 owner 自己 push 和 merge）會落地到 trunk；`autopilot-stack` 做到 verified 為止、不 merge，但 rebase 之後一樣會 force-push。`babysit` 會 push 修正，但明文禁止 rebase、force-push 和 merge；`opening-a-pr` 與引用它的 `refactoring`、`multi-phase-plan` 會開正式 PR（不是 draft），同一 branch 上多個 Task 之間還會 `git reset --hard origin/<branch>`。`worktree-cleanup` 會 `git worktree remove --force`，還會刪 simulator 和快取，不過有未 commit 修改的 worktree 會先停下來問。`reflect` 不等核准就在 tracker 開 backlog issue。`poteto-mode` 的 Autonomy 段把開 PR、更新 ticket 歸為可直接做的外部動作，只對 force-push 到共用分支、部署、刪資料、發訊息給客戶設「Always pause」；使用者說「run until done」這類話時就「keep going」，但它是否也蓋過「Always pause」，原文沒寫清楚。
- **移植版會改觸發政策**：Denyer 版的 `/correct` 正文與上游一字不差，但拿掉了 `disable-model-invocation: true`。依 [Claude Code skills 文件](https://code.claude.com/docs/en/skills)，有這個旗標時 description 不進 context、只能手動觸發；拿掉後 description 會常駐 context，Claude 也能自己決定呼叫。只想手動用的話，應從上游或 backnotprop 鏡像取。
- **skill 數量變動很快**：Flavio 文寫 47 個，Hermes 版寫 17 個 playbook 加 46 個 skill／原則，查詢當下上游目錄是 58 個。引用數量前要重查。

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
