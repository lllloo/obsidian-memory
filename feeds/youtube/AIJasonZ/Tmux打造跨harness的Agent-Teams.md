---
title: Tmux 打造跨 harness 的 Agent Teams
description: 用 Fable 5 當協調者、Sonnet 5 當執行者可省下約 35% 成本，並示範以 Tmux 控制任意 coding agent 組成跨工具 agent team
created: 2026-07-21
updated: 2026-07-21
source: https://www.youtube.com/watch?v=wCSPgHpcxdc
published: 2026-07-20
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - claude-code
  - token-optimization
---

## 為什麼額度燒得那麼快

前沿模型（Fable 5、GPT-5.6 xhigh 等）雖然強，但貴且慢。若全程只用最強模型跑執行工作，額度很快見底。目前包含 Claude Code 官方在內，越來越多人推薦的做法是：**強模型當顧問／規劃者，小模型當執行者**。

Sonnet 5 的價格只有 Fable 5 的約 20%，效能卻接近幾個月前最強的 Opus 4.8，因此適合承擔實際動手的部分。

## 兩種分工模式，哪一種比較划算

官方展示過兩種寫法：

1. **Sonnet 5 當主執行 agent**，只在需要時呼叫 Fable 5 當顧問，審查計畫並給建議。
2. **Fable 5 當主 orchestrator**，負責規劃，再開小模型 worker agent 執行。

Devin 團隊比較後明確推薦第二種。理由是顧問模式代價很高：顧問模型必須讀完主 agent 的完整對話歷史，等於重新付一次新 input token；而 orchestrator 模式走的是快取 context，**cached token 成本大約只有新 input token 的 10%**。

Devin 也據此推出名為 Fusion 的 harness，宣稱效能與 Fable 5 相當甚至更好，成本卻低 35%。其本質就是 Claude Code 的「Fable 5 orchestrator + Sonnet 5 worker」。

## Sidekick：持久 session 取代一次性 sub-agent

要讓分工真的省錢，子 agent 不能是傳統的一次性 sub-agent。

- **傳統 sub-agent**：開一個新 session，做完把最後一則訊息回傳給主 agent。主 agent 若發現有問題想再改，Task 工具會再開一個**全新、沒有先前脈絡**的 session，等於重寫一遍、浪費大量 token。
- **Sidekick（持久 session）**：子 agent 是可續談的 session。主 agent 有回饋時直接對同一個 session 送 follow-up 訊息，完整繼承先前脈絡；而且這些脈絡都是 cached token，既便宜又保有完整上下文。

Claude Code 使用者對這個模型應該不陌生——這正是 agent team 的意思。新版已有 send message 工具可對既有 agent session 補送訊息；agent 完成後會維持 resumable 狀態，直到收到 shutdown 請求為止。啟動 agent team session 時甚至可以指定各自的模型。

## 在 CLAUDE.md 加委派規則

實際做法是把委派規則寫進 `CLAUDE.md`，大意是：

- 你是 coordinator，負責設計、規劃與審查
- 動手執行一律委派給使用 Sonnet 模型的 executor sub-agent
- 明列哪些留在主 agent（設計、規劃、架構、極小的編輯），哪些該委派
- **要有 role check**：讓 sub-agent 知道自己是 sub-agent，避免它再往下無限巢狀開 agent

實測流程：提出「設計並建一個 to-do app」→ 主 agent 提問、規劃，複雜任務會在 task 資料夾產出一份凍結的 spec，讓執行者沒有模糊空間 → 開 Sonnet 5 sub-agent 執行（收到的指示是「你的角色是 executor、自己做、不要再開 sub-agent、先讀 spec 再實作」）。因為是 Sonnet 5，速度明顯比用 Fable 5 直接實作快。

作者的委派規則已放在 AI Builder Club 的 GitHub repo，可直接複製進自己的 `CLAUDE.md`。

## 跨到 Claude Code 以外：Codex plugin

上述做法只在 Claude Code 內成立，但實務上多半同時用好幾個 coding agent（例如 Gemini CLI 在前端設計仍具成本效益、或近期的 Kimi 系列模型）。理想狀態是協調者用最強的 harness，worker 則可自由選擇。

Codex 團隊推出了 Claude Code plugin，可把任務委派給 Codex agent。安裝 plugin、加入 OpenAI Codex、reload plugins 即可使用。提供的指令包括：

- `codex rescue`：把 Codex 當 sub-agent 用
- `codex review`：讓 Codex 審查本地 git
- `codex result`：抓取特定 Codex session 的輸出
- `codex cancel`：取消
- `codex transfer`：把目前的對話歷史 fork 到 Codex 那一側繼續

作者原以為無法對同一個 Codex session 續談，實測發現有 resume 指令可對既有 session 送訊息，等於這條橋已經通了。

## Tmux：控制任何一個 coding agent

若想接的是 Gemini CLI、Grok、Pi Agent、OpenClaw 等任意工具，可以用 Tmux。Tmux 是 terminal multiplexer，能開多個持久終端 session 並持續讀取與操控。

```bash
# 在右側開新終端 session 並啟動 agent
tmux split-window -h

# 對第二個 pane 送訊息並按 enter
tmux send-keys -t .1 "Tell me a joke"
tmux send-keys -t .1 Enter

# 讀回該 pane 目前畫面的內容
tmux capture-pane -p -t .1
```

換句話說，agent 可以像人一樣用 Tmux 開新的 agent session、送訊息、讀畫面，藉此控制任何一個 coding agent，組成真正跨工具的 agent team。

**回報是唯一的難題**：子 session 完成或需要協助時，如何通知主 agent。可用 Tmux 的訊號機制解決——約定子 agent 完成時送出特定訊號，主 agent 則等待該訊號：

```bash
# 子 agent 完成時執行
tmux wait-for -S <signal-name>

# 主 agent 端阻塞等待
tmux wait-for <signal-name>
```

主 agent 可把這個等待放進背景指令，完成即被喚醒。

## open agent teams skill

作者把上述 Tmux 手法封裝成名為 open agent teams 的 skill，內含針對各 harness（Claude Code、Codex、Grok、Pi、OpenCode 等，也可自行擴充）的 reference 與 adapter，並在任何一般終端都能運作。

腳本對外暴露的能力大致是：開新 agent session、對 session 送訊息、等待結果、查看結果、停止 session。實測流程包含幾個值得注意的細節：

- 開完 session 後先跑一次 **peek 檢查**，確認 session 真的跑起來——有些 coding agent 會卡在權限確認畫面
- 等待完成時**設定 max timeout**，session 在背景執行
- 結果不完整時（例如只拿到摘要、沒有實際內容），可對該 session 再送一次訊息要求輸出
- 遇到互動模式的畫面，可直接送 Enter 控制該終端

示範任務是「請 Codex 寫一個關於工程師的笑話，完成後委派給 Pi Agent 審查，同時並行讓 Claude Code 的 Haiku 模型檢查文法，最後彙整回報」——過程中確實出現部分請求被 classifier 擋下的狀況，但流程能自我修復並等到兩邊結果。

這個 skill 同樣放在 AI Builder Club repo，內含 skill 檔與可貼進 `CLAUDE.md` / `AGENTS.md` 的委派規則 reference。

## 更完整的方案：Herd 與 Orca

若想要開箱即用的體驗，Herd 與 Orca 這兩個工具內建 orchestration CLI 並附 UI 層。作者實測後個人偏好 Orca：

- 內建 orchestration skill（CLI + 提示詞開箱即用），安裝後即可達到與前述 open agent 委派相同的效果
- 因為與其介面深度整合，體驗直覺得多：**子 session 會直接在右側跳出**，可把 sub-agent session 排在同一畫面上；左側有階層檢視顯示某 session 底下有哪些子 session
- 可直接進任一 sub-agent 繼續對話，完成後自動回報主 agent
- 其他內建功能：mobile 體驗、開箱即用的 Kanban 檢視、token 用量追蹤
- 完全開源免費，已成為作者近幾週與 agent 溝通的日常主力
