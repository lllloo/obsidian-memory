---
title: Codex /goals 功能完全指南
created: 2026-05-10
updated: 2026-05-10
source: https://www.youtube.com/watch?v=rIs802-bXDY
published: 2026-05-09
parent: "[[01.index]]"
tags:
  - youtube
---

## /goal 功能是什麼

OpenAI 在 Codex 中推出 `/goal` 功能，讓 agent 可以持續工作數小時完成複雜任務。同類功能還有 Hermes agent 的 persist goal（跨 turns 維持目標直到完成）。

**解決的核心問題**：模型在長任務中會過早宣告完成。例如要求修復所有失敗的測試，agent 可能跑 10-15 分鐘後就回報「已修復」，但實際上並不完整。

**演進背景**：早期有個叫 Ralph Loop 的開源專案，把 coding agent 放在 for loop 中，每次結束後把輸出寫進檔案再重新觸發。這是個簡單的程式化迴圈，Codex `/goal` 和 Hermes goal 是對這個概念的升級。

## 運作機制

關鍵差異：停止條件改由 **LLM 判斷**，而非程式化的迭代次數上限。

運作流程：
1. 使用者輸入 `/goal <目標描述>`
2. Agent 開始執行任務
3. 完成後觸發一次 LLM call，判斷目標是否達成
4. 若未達成 → 帶著持續提示（含目標脈絡與狀態）再次觸發 agent
5. 若達成 → 結束 session

Codex 的持續提示包含明確指示：「不要把代理信號當作完成依據，只有在目標真正達成、無待完成工作時才標記 complete。」Hermes agent 則用額外的 LLM call 判斷結果。

對比 Ralph Loop：
- 停止條件：程式化迭代上限 → LLM 判斷
- 每次迴圈的提示：相同提示 → 帶有目標脈絡與狀態的持續提示

## 設定與啟用

```bash
codex features list          # 列出所有實驗性功能（含啟用狀態）
codex features enable goal   # 啟用 goal 功能
```

啟用後在 Codex 中輸入 `/goal`，即可輸入目標描述。

**執行中可用指令**：
- `/goal`（再次執行）— 查看目前狀態、運行時間、token 消耗
- `goal pause` — 暫停
- `goal clear` — 停止
- `side` — 從當前對話 fork 出一個分支對話（可邊等待邊詢問）

## 如何寫好 goal prompt

好的 goal prompt 需要明確定義：
- **要達成什麼**
- **不能改動什麼**
- **如何驗證進度**（例：用 Playwright interactive 驗證視覺是否一致）
- **何時停止**（量化的停止條件）

原則：目標規模應大於單一 prompt，但小於開放性 backlog。

範例：
```
將此專案從 JavaScript 遷移至 TypeScript，確保所有畫面視覺上
完全一致，使用 Playwright interactive 驗證輸出。
```

對於原型開發，應指向 plan.md 或 PRD 檔案，並為每個 milestone 建立測試。

也可做評估集迴圈：
```
優化 prompt 檔案中的 prompt，直到評估分數達到目標分數。
每次修改後執行評估，檢查失敗案例，保持 prompt 最精簡。
```

**模糊目標的後果**：「繼續直到一切修好」這種描述 → agent 要麼過早退出，要麼陷入無意義的迴圈。

## 實戰經驗分享（Vincent，open-claw 維護者）

連續跑 3 天、30 個 loop、大量 token：

1. **前期對齊（初始訪談）**：不要直接貼入 prompt。先與 agent 對話，告訴它：
   - 專案是什麼
   - 自己在意什麼
   - 壞的用戶體驗長什麼樣
   - 已嘗試過的解法
   - 常見的 bug 類型
   然後讓 model 提問，確認理解後再開始。

2. **量化停止條件**：避免模糊。明確如「找到 20 個新的離散 bug，並為每個 bug 提出修復方案、push 到 branch、記錄到 run 資料夾」。

3. **新專案的目標 prompt**：列出參考實作、反模式清單、設計模式以及使用者期望行為。

## Goal Buddy（開源輔助工具）

幫助構建好的 goal prompt：

```bash
npx goal-buddy   # 啟動 goal-buddy
# 在 Codex 中輸入 /goal-prep
```

`goal-prep` 會觸發 Codex 與使用者進行訪談，生成兩個檔案：
- `goal.md` — 清楚描述需求、限制、停止規則與詳細迴圈的 goal 文件
- `state.yml` — 根據程式碼列出所有任務的狀態追蹤

執行時改用 `/goal <goal.md 路徑>` 取代直接輸入提示，讓 agent 參考 goal.md 並更新 state.yml。

## Mission 概念（長期水平任務）

`/goal` 功能主要設計用於數小時的 coding 任務，不適合需要數週或數月的目標（例：改善 SEO 策略、優化廣告投報率）——因為這類任務沒有即時可驗證的結果。

**Mission 概念**：適合真正長期的目標。

運作方式：
1. 將長期目標寫入 `mission.md`（定義要優化的指標）
2. 觸發 agent run → agent 提出假設 → 執行一步 → 輸出 artifacts
3. **排程下次執行**（可能是數小時、數天甚至數週後），而非立即重複
4. 每次觸發時，新 session 接收 mission.md 與上次步驟摘要
5. 若 agent 遇到不確定或目標不清晰的狀況，可向人類發送訊息

**實驗案例**：讓 agent 迭代經營 Twitter 帳號、優化廣告活動、推動產品成長。初始 tweet 表現普通，agent 觀察後調整成「創辦人語氣的串文」，下一篇表現立刻顯著改善。目前開放 closed beta 早期測試。
