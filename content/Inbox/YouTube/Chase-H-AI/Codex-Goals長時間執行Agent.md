---
title: Codex Goals 成為最佳長時間執行 Agentic Harness
created: 2026-05-11
updated: 2026-05-11
source: https://www.youtube.com/watch?v=nOFordZCyzs
published: 2026-05-09
parent: "[[01.index]]"
tags:
  - youtube
  - codex
  - claude-code
  - agentic
---

## 核心定位

Codex 新推出實驗性 `/goal` 指令，把 RALF loop（Read-Act-Loop-Feedback，俗稱「Ralph loop」）內建成一個 slash command，不需再外掛 GSD、Superpowers 等 orchestration layer 就能跑數小時甚至數十小時的自主編碼任務。一行指令啟動整個迴圈，是目前最低門檻的長時間 agentic harness。

## 啟用方式

實驗性功能，預設關閉。Codex 桌面版與 CLI 共用同一份設定：

- 從 Settings → Configuration 打開 `config.toml`
- 加入兩行：

```toml
[features]
goals = true
```

- 重啟 Codex 確保設定生效
- 也可以直接讓 Codex 自己改：「Hey, can you enable goals for me?」

啟用後輸入 `/goal`，UI 不會跳通知（experimental feature 的 bug），但 thread 標頭會顯示 `goal` badge 表示已進入 goals loop。

## RALF loop 基本原理

`/goal` 本質是 RALF loop 的精緻封裝。原始 RALF loop 在 Claude Code 裡其實就是一行 bash：

```bash
while true; do claude < prompt.md; done
```

運作流程：

- AI session 讀 `prompt.md`（目標與完成條件，例：lift coverage on authentication files to 75%）
- 同時讀 `state.md`（已完成什麼、還剩什麼、目前嘗試到哪）
- 跑一個 turn 後寫回 `state.md`
- 迴圈持續，直到達成 prompt 裡定義的 completion criteria

優點是簡單；缺點是沒有 budget 管理、crash recovery、deliverable audit 等 scaffolding，這些都得自己補。

## Goals 與 RALF loop 的差異

big picture 一樣（持續 loop + 內部狀態檔 + 完成條件），但 Codex 多了兩個對使用者隱形的 markdown 檔：

- `continuation.md`
- `budget_limit.md`

每個 turn 結束時 Codex 會走以下四條路徑之一：

- 還有工作、budget 充足 → 繼續下一個 turn
- 接近 token cap → 注入 `budget_limit.md`，優雅收尾、產出 final report 列出剩餘工作，等使用者升額後可續跑
- 任務完成 → 呼叫 `update_goal` tool 改狀態、audit deliverables、全部 thumbs up 才標 goal complete
- 中途暫停／編輯 goal／crash → 不像傳統 RALF loop 直接斷掉，有 graceful handling

優於 GSD、Superpowers 等 Claude Code orchestration layer 之處在於：那些工具要看 40 分鐘教學才會用，Codex goals 一個 `/` 指令就跑。

## 實作建議

關鍵不在 `/goal` 本身，而在前置的 plan：

- 先用 plan mode 把模糊想法收斂成「非常具體的 end result」
- 完成條件必須**可量化**，不能是「make me a SaaS product that makes a billion dollars」
- verification 段落要列出真正能驗證的步驟（跑 `npm run build`、起 dev server、開 Playwright 跑互動驗證等）
- plan 完成後選「No, I'll tell you what to do」拒絕直接執行，然後送出 `/goal use goal to implement this plan`

verification 沒收緊，goal 會在「看似完成」就停手，產出半成品。

## Demo：Rift Salvage 2D 街機遊戲

影片 demo 用 goal 蓋一款 top-down arcade survival 遊戲：

- 玩家 drone sprite、3 個敵人、1 個 boss、energy core、hazard mine、rift background、badges、2 個 UI flavor assets
- 全部用 OpenAI GPT Image 2 自動生圖（Codex 是 OpenAI 產品，內建 image gen 是相對 Claude Code 的差異點）
- verification 包含 `npm run build`、起 dev server、Playwright 自動化測試（開啟、檢查 canvas 非空、模擬鍵盤、模擬碰撞、強制傷害、確認 health 變化、boss win state UI 等）

第一輪約 30 分鐘完成：canvas 遊戲、鍵盤觸控、敵人 spawn、地雷計分、shield power-up、boss phase、win/lose/pause/restart、11 個 image gen 點陣 asset、Playwright verifier。

第二輪在新 thread 用 plan mode 補強：射擊系統、敵人會還擊並有 HP、加快 boss phase、加按鈕直接觸發 boss、提升對比度。15 分鐘完成，總計約 45 分鐘做出能玩的遊戲。

## 重要陷阱：thread 與 goal 綁定

- 每個 goal run 綁定當前 thread / session
- 同一個 project 要跑第二次 goal，**必須開新 thread**，不能在原 chat 內再 `/goal`
- 想像成開新 terminal

## 與 Claude Code 的關係

影片立場：不該二選一，兩者並用最強。

- Claude Code 偏好純 terminal 體驗
- Codex 桌面版 inline 顯示 asset、狀態變化，比純 terminal 觀察 long-running task 順手
- 推薦組合：Claude Code 做 plan → 丟給 Codex 用 `/goal` 跑 → Claude Code review 產出 → 來回協作（whole greater than sum of its parts）
- 對 Claude Code 來說要做到一樣的事，可以串 Higgsfield CLI / MCP 補圖像生成，但要自己接 orchestration layer，不像 Codex goals 一條龍

## 風險與限制

- experimental feature：UI 回饋不完整（`/goal` 無 confirmation badge 的問題仍存在）
- 跑很久不代表結果好，網路上有人跑 50 小時、3 天的截圖但完成度未必更高
- 完成條件不夠具體會得到 mediocre / half-baked 產出
- 還是要靠人在 plan 階段把目標、verification、acceptance criteria 鎖定
