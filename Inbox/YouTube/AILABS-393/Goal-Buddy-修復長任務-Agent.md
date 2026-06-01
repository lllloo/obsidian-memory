---
title: 別爭 Codex 與 Claude Code，Goal Buddy 終於把兩邊都修好
description: 解析開源工具 Goal Buddy 如何補強 Claude Code 與 Codex 的 goal 長任務指令，用本地狀態、明確 oracle 與 scout/worker/judge 三 agent 解決 context 膨脹與缺乏完成定義的問題。
created: 2026-06-01
updated: 2026-06-01
source: https://www.youtube.com/watch?v=q7Am0pV6FjQ
published: 2026-05-31
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - ai-agent
  - automation
---

## 背景：goal 指令與 Ralph 迴圈

Claude Code 先前推出 `goal` 指令，讓 agent 持續工作直到滿足某個條件，專為長任務設計。

在這之前流行的是名為 Ralph Wiggum 的 plugin，做法類似：用 hooks 把 prompt 反覆餵回 Claude Code，直到條件達成。差別在於 Ralph 的條件靠 shell script 字面判斷，必須精確完全比對才算過關，過於僵硬。

`goal` 指令的判斷方式不同：它把「條件 + 目前對話內容」交給一個小模型（Haiku）評估任務是否完成，回傳 yes / no。`no` 就讓 Claude 繼續迭代同一任務。這讓完成判斷變得「主觀」，對於無法量化的任務是實質改進。

## goal 指令的缺陷

影片指出原生 `goal` 指令在重度工作流下會暴露幾個問題：

- **沒有本地狀態 / 知識庫**：不使用任何檔案系統追蹤任務進度，agent 唯一的真實來源（source of truth）只剩 chat context。
- **斷線後依賴對話脈絡續接**：session 因故結束時可用 `claude resume` 恢復、目標不會遺失，但它只能靠 chat context 知道做到哪裡，長任務中途容易出錯。
- **context 膨脹與 compaction**：goal 跑數小時後 context bloat、觸發 compaction 幾乎無可避免；compaction 之後 agent 輸出品質會變差。
- **不拆解任務**：只用主 agent 自行做任務拆解（如同 Claude Code 平常的做法），沒有結構化計畫，agent 可能搞丟還剩哪些待辦。
- **缺乏明確的完成定義**：完全交給模型評估完成與否，雖比 Ralph 用 script 死板要好，但至少該有個 metric 告訴 agent「done 長什麼樣」。

## Goal Buddy 的解法

Goal Buddy 是一個開源工具，目的就是讓 `goal` 指令真正照預期運作。它同時支援 Claude Code 與 Codex，安裝方式是把 install 指令貼進專案資料夾，會以 plugin 形式裝好，新 session 即可看到指令可用。

核心改進：

- **強制本地狀態**：迫使 goal 讀寫本地狀態，而非依賴 chat history。
- **以 proof 收尾**：開工前先讓 agent 知道「完成」的樣子。
- **內建 dashboard**：可視化看 agent 工作中的進度、哪個 agent 正在執行、哪些任務排隊或已完成，不必自己盯。

## 三個 agent 與 PM 角色

Goal Buddy 建立在三個角色明確、存取權限嚴格區分的 agent 上。因為要同時支援 Codex，agent 以 TOML 定義（而非標準 Markdown）。

- **Judge（裁判）**：唯讀。懷疑式地分析高風險決策（risky scope、來源相互矛盾等模式），確保任務安全完成。指令禁止它編輯，因為它只負責判斷。任務關鍵，reasoning effort 設到最高。工作完回傳一個 JSON 結構，內含 approved / rejected 決策與 rationale。
- **Scout（偵查）**：唯讀。負責盤點當前任務、產出精簡的 evidence receipt。因為只是檢視狀態，reasoning effort 設低。
- **Worker（執行）**：唯一有編輯權限的 agent，做實際工作，且一次只允許執行一個任務。
- **PM 角色**：主執行緒，協調整個工作流，做最少必要的工作。它是唯一有權把任務標記為 done 的角色。

## 核心工作流

1. **表達意圖（intent）**：用 agent 能正確理解的方式清楚陳述任務目標。
2. **定義 oracle**：oracle 是一個可觀察的訊號，用來辨識結果是否達成，系統就是針對它反覆迭代來決定能否標記完成。oracle 可以是測試套件、瀏覽器走查（browser rundown）、任何 artifact 或 benchmark。
3. **surface（拆解與視覺化）**：把任務拆成可執行步驟、建立 dashboard、把任務映射成視覺格式。
4. **PM 收尾**：PM 讓 goal 持續運行，直到最終 audit 判定目標達成。

實際使用時跑 `goal prep` 指令初始化工作流並定義想達成的目標。它會先確認 agents 已安裝就緒，再啟動工作流；不同於原生 goal，它會主動反問問題以消除自身模糊性，持續發問直到真正理解你要的實作。

## 任務拆解：slices 與 state.yaml

- **goal 檔案**：放入原始請求加上你的回答，映射成 agent 可理解語言的目標，含資訊摘要，並定義最關鍵的 oracle。
- **slices**：Goal Buddy 把工作流拆成小而可做的任務，稱為 slice。slice 的重點不是小，而是「安全、易於驗證、可獨立執行」。文件中明確定義了安全的切片大小。
- **state.yaml**：追蹤專案與任務，包含所有 goals、rules、依 ID 拆好的任務與指派的 agent、追蹤 active task 的欄位，以及連結的 dashboard。列出 to-do 與 in-progress 任務。

執行迴圈：複製指令執行後，指示 Claude 以完成 goal 檔案內所有事項為目標，從第一個 active task 開始呼叫下屬 agent 執行。Scout 完成後更新進度檔、把發現記錄到獨立目錄、並把 board 從 active 改為 completed。接著迴圈取下一個任務標為 active 並啟動 Judge，Judge 嚴格審查發現並把報告排序成最少的 vertical slices（給 worker 獨立執行的拆解），更新 slice 數與 state 檔。每個任務明確列出允許的檔案、如何驗證、何時停止。最後 PM 做收尾 audit 確認測試都正確執行，再標記 goal 完成。

## 兩個實測觀察

- **可程式化評估的任務**：oracle 是「所有測試必須通過且行為正確」，這種目標明確、可程式化判斷。整體運作得相當不錯（考量 app 的複雜度與規模）。
- **無法程式化評估的任務（設計 UI）**：把同一個模糊 prompt 分別給原生 goal 與 Goal Buddy。Goal Buddy 額外詢問 tech stack，並把不可量化的任務轉成可量化——它把完成定義為「dev server 起得來、瀏覽器走查確認所有 section 如定義運作」。耗時比原生 goal 久，但最後正確完成 app，且成品明顯優於原生 goal 直接產出的簡單 HTML 頁。

## 限制

影片認為可加入更有效的平行化：Goal Buddy 全程都是循序執行（一次一個任務），完全沒用上 Claude Code 的平行化能力。
