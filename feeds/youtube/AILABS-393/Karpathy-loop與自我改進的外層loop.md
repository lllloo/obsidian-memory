---
title: 用這個方法讓 Claude Code 效能翻十倍
description: 把 Karpathy autoresearch 的單檔實驗 loop 改造成 app 功能開發流程，並加一層外層 loop 讀取執行紀錄、改寫工作指示以修正 agent 的慣性錯誤
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=qLfSDQ5NGh0
published: 2026-10-02
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - loop-engineering
  - workflow
  - sub-agent
---

## Karpathy 的方法

Andrej Karpathy 的 autoresearch 專案讓 AI agent 持續訓練模型、反覆執行，直到模型真的變好，全程在 loop 中進行、不需要人指揮每一步。結構只有三個檔：

| 檔案 | 角色 | agent 權限 |
|---|---|---|
| 訓練檔 | 唯一可改的檔；每輪改一處、訓練幾分鐘 | 可改 |
| 評分檔 | 給模型打分；分數變好就保留修改，持平或變差就撤回 | **不可碰**——能改評分檔就能把分數改得更好拿，而不是改善模型 |
| `program.md` | Karpathy 用白話英文寫的指示，說明每輪怎麼跑 | 人寫 |

Karpathy 寫好指示後讓 loop 跑 2 天：agent 跑了 700 次實驗，找到 20 個讓模型訓練更快的修改。700 次實驗靠人逐步控制會耗費大量時間，agent 自己跑卻能窮舉各種可能。

Shopify CEO 也跑過同類 loop：在睡覺時對自家一個模型跑了 37 次實驗，隔天早上模型表現提升 19%。結論：只給 agent 目標，它就能自己不斷嘗試、逐步改善，這也是 loop engineering 開始流行的起點。

## 何時值得用 loop

用錯任務會浪費 token 又拿不到想要的結果。值得建 loop 的任務需同時具備四個條件：

1. **任務會重複做**：建 loop 要時間，只有反覆執行才回本；一次性的工作一個好 prompt 就夠
2. **用量額度足夠**：每輪 agent 都會重讀專案、嘗試新修法，失敗的輪次也照樣燒 token；$20 方案跑長 loop 會在完工前撞上限
3. **成果能被明確打分**：在 app 裡就是一小段測試某功能並確認運作的程式碼
4. **agent 能實際執行成果、看到哪裡壞**：才知道下一輪該修什麼

頻道自身的原則：只對有明確可量測分數的任務用 loop；**從不讓整個 app 在單一 loop 裡建完就宣告完成**，只用 loop 一次建一個功能，或建一個 loop 檢查能驗證的簡易版 app。

## 套用到 app 開發的架構

以下各元件都可以請 Claude 照描述代建。

**project context skill**：專案專屬的記憶庫，內含 app 做什麼、有哪些頁面、遵循的慣例、應避免的事，隨 app 成長持續更新。用 skill 而非一般檔案，是因為只有 skill 的簡短描述常駐 context window——agent 隨時知道它存在，但只在需要時才載入完整內容。

**build skill**：驅動整個流程的主 skill，讓 loop 在無人看管下執行，流程如下：

1. 呼叫 **write checks** skill 先寫檢查（類似頻道先前影片的 test author agent，但針對本專案客製）。先寫檢查，agent 才有可驗證的依據，而不是自己評自己的程式碼
2. 用白話列出每個檢查在測什麼；這一步要和 agent 來回討論，確保涵蓋工作中常見的問題
3. 你同意後，一支名為 **approve checks** 的小程式把檢查移進鎖定資料夾，並以 Claude Code settings 中的規則禁止 agent 編輯該資料夾——loop 就無法把自己的檢查改簡單
4. build skill 把檢查 commit 進版控，多一層防護
5. 開始跑 loop，但不在自己的 context 裡實作：每個功能交給 **feature builder agent**，每次從全新 context 開始，各功能 context 互不干擾
6. 每輪結果寫進檔案留存
7. 所有功能完成後產出報告

loop 的固定規則與工作方式都寫在 `program.md`，沿用 Karpathy 的格式。

## 實測：訂餐功能

在一個做到一半的餐廳網站專案上，要求用 build skill 建「訪客線上點餐自取」功能：

- 該功能不在功能清單上，Claude 先把線上點餐規則加進用來追蹤功能的 `features.md`
- 初版列出 10 項檢查；要求加入訪客 email，變成 11 項，新增的檢查確認 email 是真實地址
- 核可後 commit，feature builder agent 約 6 分鐘完成，11 項檢查第一輪全過，不需第二輪

loop 也抓到分數沒反映的問題：檢查只測點餐規則，所以 loop 只寫了規則、沒寫訪客實際使用的點餐表單。loop 在標記完成前自行補上表單並接上規則。

## 慣性問題：loop 不會跨輪記取教訓

這類 loop 的問題是 agent 有慣性。某種做法不管用時，它會在該輪內改善，但下次跑 loop 時不會記得。每個功能都由全新的 feature builder agent 搭配同一份指示檔開工，所以某輪犯的錯會延續到下一輪。

解法是**第二層 loop**：讀取第一層 loop 的執行情況，改寫第一層的工作方式。頻道把它做成名為 **auto loop** 的 skill：

- Karpathy 的做法是人寫 `program.md`；這裡改由 auto loop 改寫 `program.md` 的「how to work」段落
- 讀取 results 檔：每輪記錄是否保留或撤回、agent 嘗試了什麼、哪些檢查仍失敗
- 找出反覆出現的問題（例如 agent 一再犯同樣的錯、兩個功能出現同一個缺口），把每個慣性連同佐證的輪次寫下
- 改寫 how to work 段落，後續功能就用新指示建
- **auto loop 不能改檢查**：能改就能把檢查改簡單，輪次不再失敗但慣性從未被修正

與 build skill 的差別：build skill 只跑一遍，每個功能拿同樣的指示，loop 學到的東西不會帶到下個功能；auto loop 同樣一次跑一個功能、沿用同一個 feature builder agent 與 write checks skill，但把 loop 包在另一個 loop 內，每完成一個功能就檢討並更新指示，下一個功能從實際有效的方法開始。

## 實測：協作功能

在一個缺乏多人協作與分享工作流程能力的專案管理 app 上，要求加入共享專注時段與共同執行專案的功能。auto loop 先把功能加進追蹤檔、列出檢查（可修改或直接開工）。

auto loop 歸納出的兩個慣性：

1. **共享資料庫**：10 項檢查全過，但 app 從未寫入資料。新增慣性指示——**在讓檢查通過的同一輪就把功能接上 app**
2. **mention**（輸入 `@` 加人名指派任務）：檢查通過，但 app 舊有部分仍用舊方式解析 `@`。新增慣性指示——**找出 app 中所有已在做同一件事的地方，讓每一處都遵循新規則**

兩條指示都奏效：後續功能的畫面一開始就接好了。

檢查的實際作用：builder 在「共享專案」上錯了兩輪——第一輪弄壞 mention，mention 檢查失敗、該輪撤回；第二輪用簡單算法分配每人比例，三人各 33，加總只有 99，該檢查失敗；第三輪修正後 10 項全過。

完成後的報告會說明 agent 在哪裡出錯、如何修正，以及整體工作流程的樣貌，下個功能就不會再遇到同樣問題。
