---
title: Graph Engineering 的驗證機制設計
description: 說明 graph 相對 loop 的平行優勢與除錯盲點，並示範用 skill creator 建 standalone、embedded、second opinion 三類驗證 skill，再以 orchestrator skill 統一扇出
created: 2026-08-03
updated: 2026-08-03
source: https://www.youtube.com/watch?v=H7t3uUp3HVw
published: 2026-07-29
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - graph-engineering
  - sub-agent
  - workflow
  - best-practices
---

graph engineering 把主任務拆成多個節點平行跑，速度與覆蓋面都勝過線性的 loop，但代價是：小節點的一個錯誤會污染整份輸出，而你最後只拿到成品、幾乎無法回溯是誰先出錯。影片主張解法在驗證層，並整理 Anthropic 與作者團隊實際採用的做法。

## 從 loop 到 graph

- **loop engineering**：交給 agent 一個工作循環——你只給最終目標，它自己邊做邊調整。作者團隊原本大量使用。
- loop 的結構限制在於一切走直線：做一步、驗證一步、通過才進下一步。即使兩個步驟毫無關聯，後者仍得空等前者。
- **graph** 把主任務拆小、每個部分配一個 agent。好處有二：多個 agent 同時推進，速度大幅提升；可以為每個節點各自挑模型，不再把最貴的模型燒在根本不需要那麼多智慧的部分。
- 但那是**單一 agent 的成本**下降，總成本反而暴增——同時跑一整批 agent 的 token 消耗遠高於單一 agent。用 graph 要預期額度比平常更早見底，Claude Code 與 Codex 的 20 美元方案基本撐不起這種設定。
- Claude Code 的 dynamic workflow 就是 graph 的一種：把任務扇出給一組 sub-agent。

## 節點與邊

- **node（節點）**：從大任務切出的單一工作，在自己獨立的 context window 中執行後回報。
- **edge（邊）**：控制資料如何從一個節點流向下一個，確保某個 agent 的輸出在對的時點落到對的 agent 手上。每個節點都必須以某種方式接進整張圖。
- 例：一組 agent 同時審查同一份成果——彼此不互等，但都從同一份工作出發，最後所有報告匯流到同一處。

## 常見的圖形

- **鑽石形**：頂端一個任務扇出成多個並行 sub-agent，再收斂回單一 agent 統整成一個答案。（作者頻道早期介紹過這個形狀，當時 graph engineering 一詞尚未出現，誤稱為 loop；實際上是被反覆執行的 graph。）
- **fan-in at a barrier**：同一個問題送給一組 agent，每個從不同角度檢視；在**所有** agent 回報完成前不往前推進，全部到齊後才去執行修正。適合需要多角度同時判斷的情境。
- 形狀還有很多，但全都建立在同一個基礎上——驗證。檢查沒設好，後面每個 agent 都在錯誤之上疊東西。

## 為什麼 agent 自帶的驗證不夠

跑一整支 agent 艦隊時，會出現單一 agent 不會有的問題：

- **量太大**：全部同時進行，成果一次湧回來，最後很難逐一審查。
- **不透明**：出錯時沒有辦法判斷是什麼造成的。

所有 agent 無論你要不要都會驗證自己寫的東西——以程式碼而言就是跑測試、接住錯誤。但那只抓得到重大錯誤，不會檢查**寫法**；寫法持續走偏日後就是麻煩。

Claude Code 內建的幾項：

- **verify skill**：把程式碼從頭到尾走一遍，確認行為與預期相符。
- **tool chaining**：agent 自己跑各種檢查工具、讀回錯誤並修正。它能自行推導專案的指令，但把指令寫進 CLAUDE.md 可以省下每次重新推導的功夫。
- **code review skill**：對照一組標準檢查程式碼。不是每個 agent 都內建，沒有的話可以直接請 agent 幫你做一個。

作者結論：真正有效的是自己設計的驗證，不要整套仰賴內建。

## 用 skill creator 建自己的驗證 skill

- 最快的途徑是 Claude Code 的 skill creator plugin（這個 Claude Code skill 也能在 Codex 使用）。跑 plugin 指令、搜尋 skill creator、安裝。
- 安裝範圍二選一：user scope（不論在哪個資料夾都在）或只裝在當前專案。因為是會一直用的 skill，作者選 user scope。安裝後用 slash 指令重載 plugins 即可使用。
- 接著描述你要哪一種驗證。作者最常用的是「拿完成品對照最初的需求」的 review skill——這在 graph 裡格外重要，因為**每個 agent 只看得到自己那一塊**，需要有東西讓它把那一塊對回原始需求。

### 判斷節點的模型不能省

作者為社群網站 UI 建驗證系統時的實測：

- 用 Haiku 跑 reviewer，回報一長串問題，光看數量像是表現很好。
- 同一份工作換 Opus 跑，標出的項目少得多——看起來像最差的結果，直到讀了它的理由。
- Haiku 報的很多是團隊**刻意保留**的設計，Opus 從周邊程式碼推斷出這點，Haiku 完全沒抓到。便宜的 review 什麼也沒省，因為 review 本身還需要被 review。
- 放進 graph 就更嚴重：一整批節點都用同一個 skill 檢查自己的工作，會有一群 agent 花時間與 token 去修根本沒壞的東西，而且錯誤散在同時進行的多個 agent 裡，無從判斷是哪一個先開始。
- 結論：負責判斷的那個節點，正是省 token 代價最大的地方——模型選擇決定的不只是 review 品質，而是整張圖的品質。

## 三類驗證 skill

### standalone（手動觸發）

- 只在你自己執行時才跑。設計上是對「已經存在的成果」做深入檢視，所以不該每輪自動觸發——那會在還沒完成的工作上燒掉一次重度 review 的成本。
- 作者用過的例子是 Cursor 的 thermonuclear code review：扇出一組 agent，每個從不同的資安角度掃過程式碼，所有發現匯整到同一處一起處理。屬於「app 做完才跑一次」的類型。
- 建這種 skill 建議走 skill creator 而不是直接下 prompt，因為產出的東西經過測試，比較可信。prompt 裡要指明想 review 的領域，並註明要「comprehensive」，讓它知道你要的是深度掃描而非快速掃過。

### embedded（嵌入工作流自動觸發）

- 不需你開口，在既有流程中自動觸發。例如做成「有人要求新功能時就啟動」：檢查每個被建立的元件是否符合 skill 裡訂的規則，未通過檢查就不讓實作結束。
- 可以自己建 embedded skill，但**不能**把預裝的 skill（如前述 verify skill）改成自動觸發——那些 skill 的指令位於產品內部，你動不到。
- 自建做法：告訴 skill creator 在每次功能實作後執行驗證步驟，並要求端到端測試該功能，以便抓出新工作是否弄壞了原本正常的部分。由 skill creator 產生的 skill 會附帶它在過程中結構化並測試過的 references 與 scripts。
- 驗證功能時 Claude 預設走瀏覽器測試：開完整 Chrome、載入頁面、截圖。接了 Puppeteer 或 Playwright 也是同樣的事。
- 但 Chrome 吃記憶體且笨重，在工作流內反覆檢查頁面會慢到實際損失時間。較輕的替代是 **Chrome headless shell**：拔掉多餘部件的精簡版瀏覽器，agent 一樣前往頁面、一樣截圖，只是快得多。可以直接內建進你建的驗證 skill，之後每個功能都自動獲得視覺檢查。

### second opinion（另開乾淨 session）

- 作者自身工作流中用得最多的一個。理由很簡單：**建造它的 agent 是最不適合審查它的那個**——它拿建造時的同一份 context 在評判自己的產物。
- 全新的 Claude session 沒看過那些脈絡，能給不受偏誤影響的直接答案。
- Claude 內建的 advisor 做類似的事，但它會讀當前對話，因而繼承同一份 context；second opinion 正是為了「不要那份 context」而存在。
- 實作方式是在現有 session 內用 `-p` flag 另起一個獨立的 Claude Code session，在背景交給它一份 prompt。
- 兩個注意事項：因為是完整另起 session，回覆很慢；模型選擇在此處比任何地方都重要（整件事的意義就在於更聰明的第二次閱讀），所以值得明確指定該 session 用 Opus。

## 用 orchestrator skill 串接多角度審查

- 一個 skill 蓋不住全部。認真 review 就是從多個角度看，每個角度有自己的衡量方式。全部塞進同一個 skill，agent 會因方向太多而**變差**而非變好。
- 正確做法是每個角度一個獨立 skill，再串起來。Anthropic 團隊也是這樣運作：把 code review skill、simplify skill、verify skill 串接（三者現已隨 Claude Code 出貨），再加上自家的 design skill——對照 `design.md`（存放產品所有設計決策的檔案）檢查介面。等於四個方向同時 review。
- 但不能直接叫 agent 一次跑完全部。上面還需要**一個 orchestrator skill**，唯一職責是執行其他 skill：為每個 review skill 各開一個 agent、各自帶一個 skill，在各自獨立的 context window 中同時審查，最後把所有發現彙整成一份報告給負責修正的 agent。
- 建 graph 時，prompt 裡只需要說「使用那一個 skill」，它扇出的每個節點都載入這一個 skill，底下的審查自己再扇開。
