---
title: Loop Engineering 如何 10 倍強化 Hermes Agent
description: Loop Engineering 把人從寫 prompt 的角色換成設計自跑系統；拆解 deterministic 與 non-deterministic 兩類 loop、五步流程與六個關鍵設定，並在 Hermes 與 Claude Code 上落地。
created: 2026-06-22
updated: 2026-06-22
source: https://www.youtube.com/watch?v=AQRDjI5owZI
published: 2026-06-15
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - automation
  - claude-code
---

影片核心：loop engineering 不是新東西（cron job 早就是一種 loop），但搭配像 Hermes 這種「常駐自跑」的 agent 才真正發揮。多數人把 loop 架起來了，卻漏掉真正讓它運作的關鍵設定。重點是：你不再當寫 prompt 驅動 agent 的人，而是設計一個會自己驅動 agent 的系統。

## 從 Prompt Engineering 到 Loop Engineering

- 過去重要的技能是 prompt engineering：人力寫好一連串正確指令去驅動 coding agent。
- Loop engineering 反過來：你不自己寫 prompt，而是設計一個「會幫你做 prompt engineering、並自行驅動 agent」的系統。焦點從「寫指令」移到「設計能自跑的系統」。
- 推手：OpenClaw 作者主張不該再 prompt coding agent，而該設計會替你 prompt 的 loop；Claude Code 作者 Boris 在 Anthropic 開發者大會也說他已不再 prompt Claude，而是讓 loop 去 prompt、由 Claude 自行判斷該做什麼。
- 你的角色不會縮小反而更重要：是你的領域知識與經驗在「定義最終目標」，這會體現在做出來的成品上。

## Loop 是什麼

- Loop = 你定義最終目標，agent 自己想出達成步驟、沿途自我修正、繞過問題直到達標。
- 以前模型撐不住長任務時做不到：你得 prompt、盯著它、自己檢查輸出、找問題、再 prompt 修——**人自己就是那個 loop**（負責每步之間的錯誤檢查與修正）。這正是 loop engineering 要從你身上卸下的。
- 類比 reinforcement learning：不給正確答案，只在做對時給正向訊號、做錯時給負向訊號，讓它自己摸索變好。差別在這裡被訓練的不是模型本身，而是 agent 朝你要的任務迭代。loop 沒過，agent 不會把任務標成完成，會重試到達標。

## 模型能力提升是這趨勢的底層動力

- 影片指出 Opus 4.5 之後長任務表現大幅變好，不再需要一步步引導 agent 的精細 harness（會手把手帶過每一步的結構化設定），焦點轉向「把專案準備成能長期自跑」。
- 影片提到 Anthropic 推出 Fable 5、主打長而複雜的任務，且任務愈長愈複雜表現愈好（與舊模型相反），但也提到曾一度將其下架。精確的模型版本切換時點以 Anthropic 官方公告為準。

## 既有的 Loop 系統演進

- **Ralph loop**：較早期之一，設好最終目標、用 hooks（特定事件觸發的腳本）嚴格防止 agent 在未真正達標前把任務標成完成；但 hooks 太死板。
- **Claude 的 goal 指令**：做同樣的事但更彈性，不用寫死檢查，改由另一個模型判斷任務是否真的完成。
- **Goal Buddy 2**：再往上，讓 agent 在本地檔案追蹤進度，並在開始前就定義「done 長什麼樣」，所以它隨時知道在朝什麼目標前進。
- **Hermes / Open Claw**：同一哲學，把人完全移出畫面，讓 agent 自行處理一切。

## 五步流程

Loop 的單輪基本循環（在 Claude Code 與 Hermes 都適用）：

1. **檢查專案目前狀態**。
2. 由模型據此**決定下一步動作**。
3. **執行動作**——真正做事的地方：呼叫工具、寫檔、跑指令。
4. 完成後**收集回饋**，看實際發生了什麼。
5. 據此**判斷任務是否完成**。

prompt engineering 只控制第 2 步「決策」；loop engineering 一次處理全部五步。

## 六個必須做對的設定

每一個都對應一個它要解決的具體問題：

- **Context management**：每一輪都留意進 context 的東西，因為那決定 agent 當下知道什麼。不能只靠 chat context——即便有上百萬 token 的視窗，對話一長，system prompt 與指令會被近期的 tool output 淹沒，注意力偏向最新內容，重要的東西就丟了。
- **Feedback quality**：回饋告訴 agent 做得如何，是整個系統最重要的訊號之一。形式可以是測試輸出、剛做好的 UI 截圖等，agent 讀它來決定下一步。
- **Verification gates**：把回饋轉成明確判決的檢查點，告訴 agent 任務到底算不算完成。
- **Termination condition**：明確規定 loop 何時停。沒設清楚，agent 不是太早收手就是空轉不進展。
- **Error handling**：最常被忽略。要寫清楚 tool call 失敗時模型該怎麼做，讓系統乾淨處理，而不是留下破碎狀態製造更多問題。
- **State across turns**：context 視窗存不下全部，要靠外部檔案替 agent 追蹤資訊，讓它不斷線地繼續工作。

提醒：把「找路徑」交給模型而非自己做，loop 很吃 token、會變貴，要刻意決定何時才用；能給 loop 的 token 愈多，它通常處理得愈好。

## 兩種 Loop

### Deterministic loop（確定型）

- 用於「done 有清楚定義」的任務：測試通過、程式編譯成功之類。目標明確，模型清楚達標條件。
- Hermes 常駐運行，很適合跑這類 loop。可把 Hermes 指向任何你部署、附帶測試案例的 app 替你監控；若某次 commit 弄壞 production，可在 Hermes 設自動化來抓。
- Hermes 的 self-evolving skills 功能會依 workflow 自動建立與演化 skill，維持 app 健康。
- 典型流程：設好監控自動化後，要它以 non-interactive 模式啟動 Claude Code（不需你驅動），在 loop 裡修問題直到所有測試通過。它會載入 sub-agent driven development skill 與 GitHub PR workflow skill 管理 GitHub 上的 app；先找出弄壞 production 的問題，啟動 non-interactive Claude Code 跑測試、全綠後用 GitHub CLI commit。

### Non-deterministic loop（非確定型）

- 用於無法用清楚規則判斷是否完成的任務：建 UI、需要判斷的功能——這類得靠人看了自己判斷。
- AI 做 UI 容易一直回到同樣的套路（AI slop）。作者做了 **AI slop detector** skill，收錄如何避免 AI slop 與會露餡的 pattern。
- 一樣用 Hermes 是為了 self-evolving skills：若跑完 skill 後 UI 仍有 AI slop，skill 能把這回饋直接吸收進自己。
- 流程：要 Hermes 用該 skill 檢查 UI 有沒有那些 pattern，有就修，並啟動 non-interactive Claude Code 反覆修到沒得修為止。
- **Adversarial loop（對抗式檢查）**：Hermes 讓「審核的模型」與「建構的模型」不同。影片用以 code review 見長的 GPT 系列模型當 verifier、Claude 系列模型當 builder，兩者互相檢查彼此的成果。跑完這個 loop 產出的 UI 比 Opus 系列近期直出的通用結果好很多；事後若仍看到 AI slop，提一句它就會更新 skill、強化既有的 verifier。
