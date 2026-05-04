---
title: Claude Code vs Codex 九大面向對比
created: 2026-05-04
updated: 2026-05-04
source: https://www.youtube.com/watch?v=8ImlAQOyVTs
published: 2026-05-02
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - ai-coding
  - codex
---

> [!info] 影片定位
> 把 Opus 4.7 與 GPT 5.5 放回各自原生 CLI（Claude Code 與 Codex CLI），跨九大面向實測比對；2.1.0 之後 Claude Code 體驗滑坡，Codex 在多數面向已反超。

## 可用性（Usability）

- Claude Code 在 2.1.0 更新後品質明顯下滑：terminal glitch、rendering 破圖、cache leak，曾經精緻的 TUI 變得「vibe coded」。
- 拿掉 `--dangerously-skip-permissions`，改成預設 auto mode；即使在 auto mode 下仍會跳 permission prompt。實測曾把 prompt 丟下去切到別 session，回來才發現整段 skill creation 卡在寫 `.claude/` 的權限提示上等了很久。
- Codex CLI 用 Rust 寫，UI 比 React-based 的 Claude Code 順、長 session 也不會壞。
- Codex 的 yolo mode 真的不問權限；Claude auto mode 名字像但行為不是。
- 人格設定：Codex 一個 setting 就能調成 direct / concise，因為 GPT 5.5 預設比 Opus 4.7 sycophantic 很多；Claude 這邊只能靠 `CLAUDE.md` instructions 壓。
- Pre-installed skills：Codex 內建 agent browser skill（建 app 時瀏覽器驗證不必另接 MCP）、內建 skill creator 直接生完整結構；Claude Code 都得自己另裝 skill creator，否則只會丟一份 `.md`。
- Claude Code 仍贏的兩件事：rewinding（影片作者最常用的功能）、`Ctrl+O` 展開 thinking 可中途修正方向。
- 結論：Usability 這局 Codex 拿一分。

## 成本（Cost）

- 兩家方案價錢接近，但同價位「能做多少事」差距大。
- Claude Code 沒 free tier，Pro 額度做任何稍有規模的事都會爆，Opus 4.7 在 Pro 上根本跑不動；Max plan 也很快見底。
- Codex CLI 在 free plan 就能用（有限額），同樣 5 小時 window 機制。
- 同一支 app、同等 debug 強度下實測 token 消耗：
  - Opus 4.7：173,000 tokens
  - GPT 5.5：82,000 tokens
- GPT 5.5 用更少 token、更少 retry 完成同樣工作，Codex 在同一 5 小時 window 撐得更久、cost-efficient 明顯較佳。
- 量測方法：兩家都把 session 存成 JSON（結構不同），自寫小工具讀 session 計 token；Claude Code 已有 `context` 指令但 Codex 沒有等價內建。

## 規劃（Planning）

- 在含有現成 FastAPI 後端的資料夾內讓兩者進 plan mode，要求補前端。
- GPT 5.5 探索專案後問了基本問題、~8 分鐘出 plan；plan 簡單，含主要流程／關鍵變更／要加的頁面／如何測試，且把 assumptions 清楚分段。
- Opus 4.7 在 Claude Code 同任務 ~24 分鐘出 plan，但細緻得多、考量更多面向、甚至主動把 shadcn/ui 拉進來改善 UX。
- 結論：Planning 這局 Opus 4.7 較深入。

## Greenfield 建構（Monorepo 實測）

- 同一 prompt：建 monorepo（Python Flask 後端 + Next.js 前端 + 完整 pipeline）。
- Claude Code 因 harness 設計自動切 plan mode，Codex 則直接開幹，總時間更快（Claude Code ~16 分鐘多花在 planning）。
- GPT 5.5 出的 app UI 較陽春，先求功能跑通；初次跑不起來、debug 中發現未提供 API key 時，它**自動加上 local fallback** 讓 app 不會整個崩，作者偏好這種 production 友善行為。
- Opus 4.7 反而要求先給 API key 才肯開工，並把整個 app 蓋在「key 一定存在」的假設上；key 缺席就直接吐 error，沒有 fallback。
- 但 Claude Code 出來的 UI 與 UX 一致性明顯較好（接續先前影片的觀察：Opus 4.7 UI 較強）。
- Debug 風格差異：
  - Codex：用 agent browser 自己看實作、自己驗。
  - Claude Code：往回問人「你覺得是哪裡問題？」、加 UI debug indicator + console log 後請人回報，靠來回。
- 自治程度看 Codex，UX 看 Claude Code。

## init 指令對比

- Claude Code `init`：直接生 ~90 行 `claude.md`，含架構、app flow、前後端結構、執行指令；資訊較冗、redundant 多。
- Codex `init`：較精煉，含 commit guideline、PR guideline、security instructions，專案結構段落維持輕薄不過載。
- 結論：`agents.md` 處理 Codex 較好。

## 程式碼審查（Code Review）

- 同一份 codebase，同一 prompt 要求 reliability review，分別寫到不同檔，再開新 session 用 Claude diff 兩份。
- Claude review 更詳盡：依優先級組織、附 component 與實際 code snippet。
- Codex report 標 line number 但不附 code snippet。
- 兩邊都有獨家發現，沒人完全包住對方。
- Claude Code 還順便回報 leaked API key 與 vulnerability——但任務是 reliability review，這些超綱；Codex 嚴守原始 scope。
- 用工程角色比喻：
  - GPT 5.5 像 backend engineer：先把功能正確交付。
  - Opus 4.7 像 full-stack engineer：功能與 UX 一起想。

## Context 管理與 Compaction

- Claude Code：有 in-session context editing，會把過時的 tool call、reasoning 移除，避免 bloat；compaction 不完美但至少不會把垃圾留著一起壓。
- Codex：不編輯 context，整段對話照原樣 compact，但**保留最後 20,000 tokens 不壓**，讓壓縮後 next prompt 還能順順接。
- 實測：compaction 後 Codex 表現比 Claude Code 好——Claude Code 多步驟 compaction 流程細，但 Codex 保留 tail 在實務上更有用。

## 記憶（Memory）

- Claude Code harness 跨 session 基本上 stateless；新有的 memory feature 可儲存偏好或指令，但**範圍是 project-scoped**，換 project 就丟失。
- Codex 走相反路線：跨 session、跨 interaction 累積 global memory，能跨 project 保留模式、提高一致性。
- 簡言之：Claude Code 把 memory 收在單一 project 內，Codex 是 cross-session、cross-project。

## 生態系（Ecosystem）

Claude Code 因為發展久，整體 surface 仍領先：

- **Hook system**：在 agent 生命週期特定點（tool 執行前後等）跑自家 script，可阻擋不安全指令、跑 formatter 等。Codex 目前無等價物。
- **Worktree**：sub-agent 可在獨立 worktree 跑，互不影響效能。
- **Effort level / `ultrathink` 關鍵字**：可控推理強度。
- **多介面**：Claude Code、desktop app、web app、browser extension、mobile app delegate，session 跨環境移動順暢。Codex 主要是 web app 與最近才出的 desktop app。

Codex 也有獨家：

- **Cloud `attempt` flag**：同任務跑 N 次、自動挑最好的實作。Claude Code 只能靠 configuration / instruction 達到類似效果，沒有同等 flag。
- **OpenAI 影像模型整合**：直接在 CLI 為網站生圖；Claude 沒有原生 image model，視覺主要靠 SVG，質感差一截。要做有真實圖片的 UI，Codex 不必明示就會處理。

## Sub-agent 設計差異

兩邊都有 sub-agent，但設計選擇不同：

- **觸發方式**：
  - Claude Code 可在無明確指令下自動 spawn sub-agent。
  - Codex 只在 prompt 明確要求時才 spawn，且會給 agent 命名並傳完整 prompt。
- **工具權限**：
  - Claude Code：parent 用 explicit allow list 指定 sub-agent 能用哪些工具。
  - Codex：sub-agent 預設繼承 parent 的工具存取。
- **Context 處理（最大差異）**：
  - Claude Code：sub-agent 拿到**全新 context**——只看到 parent 給的 prompt + system prompt + global rules，沒有對話歷史，強調 context isolation。
  - Codex：把 parent 的完整對話歷史 fork 進 sub-agent session，再疊上 parent prompt；agent 留住更多脈絡。
- **實測影響**：作者用 Claude Code 跑 research sub-agent 結果不夠好，因為 sub-agent 只看到當下 prompt 缺乏先前脈絡；Codex 拿到完整歷史後在「需要連續性」的任務上表現更好。

## 整體取向

- **GPT 5.5（Codex）**：像 backend engineer，先把功能正確跑起來、cost 與 token 效率高、自治 debug 能力強、長 session 穩。
- **Opus 4.7（Claude Code）**：像 full-stack engineer，functionality 與 UX 並重、planning 較深、UI 較細，但 cost 較高、2.1.0 後體驗不穩、harness 設計取捨開始反噬（如 sub-agent context isolation 過嚴）。
