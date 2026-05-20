---
title: Codex 桌面版加入 Claude Code 工作流
created: 2026-05-20
updated: 2026-05-20
source: https://www.youtube.com/watch?v=8kWONfT_-H8
published: 2026-05-16
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - ai-coding
---

> [!info] 影片定位
> Anthropic 改變 programmatic Claude Code 計費後，押注單一供應商的風險明顯升高。Chase 把 Codex（CLI + desktop app）拉進工作流，主打「Claude Code 與 Codex 的 Venn diagram 幾乎是個圓」——學會其一即會其二。本片以 Codex desktop app 為主角，講價格選擇、安裝、設定、用法差異。

## 為何要工具不綁

- Anthropic 近期改 programmatic Claude Code 計費，All-in 單一 vendor 的人錢包受傷。
- 多工具並用是抗政策風險的基本動作。
- Codex 與 Claude Code 介面、操作高度重疊；轉換成本極低。

## Codex 兩種型態

| 型態 | 適合對象 | 備註 |
| --- | --- | --- |
| Codex CLI | 喜歡純 terminal | 安裝幾行指令，用法當 Claude Code 用即可 |
| Codex desktop app | 想要視覺化、跨 plugin / skill 操作 | 也可內嵌 terminal、與 Claude Code CLI 並用 |

> 影片以 desktop app 為敘事主軸，但所有概念對 CLI 一樣適用。

## 訂閱選擇

- Plus：每月 $20，能跑 GPT-5.5。
- Pro：每月 $100，多了 GPT-5.5 Pro。
- 20× Pro 類似 Claude Max。
- OpenAI 比 Anthropic 更寬鬆：同樣 $20，Codex 比 Claude 給更多用量。
- 想試試的人直接 $20 plan + 5.5 即可，不需要先上 $100。
- GPT-5.5 本身耗 token 更少，「c/p 值」實測明顯有感。

## 安裝與初始設定

- openai.com/codex 下載 desktop app。
- 介面長得像 ChatGPT + Claude Code desktop：prompt window、檔案上傳、plugin、plan mode、permissions、model / speed 選擇。
- 進 Settings 從第一個 tab General 開始：
  - 切到 `coding` mode → 拿到比較技術導向的回應。
  - Permissions 同 Claude Code：哪些可改、哪些可自動改。Chase 全開（full access）。
  - Speed：fast mode 會 ×1.5 token 計費，慎用。

### Queue vs Steer（follow-up behavior）

- **Queue（預設）**：你在 agent 做事中再丟 prompt，會等它做完手上的 tool call 鏈再處理新的。
- **Steer**：新 prompt 立即注入當前進行中的 tool call 序列，等於「中途拍肩告訴它順便做這個」。
- 預設留 Queue；要時可在 UI 上手動按 Steer 一次性切換。

### Appearance & Pets
- Pets：一個視覺 hook，agent 在跑時顯示小寵物動畫；可以做為「還在跑 / 跑完」的提示，方便 tab out 去做別的事。

### Configuration
- User config 對應 global 權限設定。
- 開啟 Codex dependencies。
- `config.toml` 是 Codex 的設定檔；要啟用 goals feature（長時間執行的 agent harness）→ 手動在底部加 `feature goals = true`。

### Personalization & Memory
- Personalization 不是 `AGENTS.md` / `CLAUDE.md`，只是設語氣 / 性格。
- Memory 與 Claude Code 同概念：自然語言講「我每週二上健身房」→ 它會記下。
- 部分功能（如 computer use、archiving）只在 macOS 可用。

## 使用模式：Chat vs Project

- **Chat**：類似 Claude 桌面 chatbot 模式，沒有歸屬到專案。
- **Project**：要做正事就進 Project；可從零開新資料夾或選現有資料夾（推薦後者，掌控資料夾位置）。
- 進 Project 時會出現「migrate settings」選項：把 Claude Code 的所有 skills / plugins 一鍵匯入 Codex。
- Project 可指定 work tree、branch、執行位置（local / Codex Web）。

## Plugins 與 Skills

- Plugins ≈ 官方版的 skills，內容比較完整。Chase 列例：spreadsheets、presentations、Chrome、Vercel、Supabase。
- 加 plugin：左上 `+` 按鈕，多數需要 login 到對應服務。
- Skills tab 可看安裝列表、enable / disable / try / uninstall。
- 右上有 `Create skill / plugin` 按鈕，直接呼叫 skill creator skill。
- 呼叫方式：
  - `@<plugin/skill>` 顯式呼叫
  - `/<skill>` 也可（像 CLI）
  - Codex 通常會自動推斷：「幫我做 Excel」→ 它自動用 spreadsheets plugin

## Automations

- 上方「new automation」開新排程，描述要做的事、給 title、選 work tree、project、執行時機。
- 可指定 model 與 reasoning 強度。

## 操作差異與便利點

### 行內視覺與 review
- 跑完 code 變更可在右側 panel review、undo。
- 在前端產出的網頁上可直接「圈起元件 → 留 annotation 評論」，這比純 terminal 改設計流暢得多。

### Context window
- GPT-5.5 Pro 256K vs Opus 1M。
- Chase 觀點：context window 小未必是缺點，可降低 context rot 與 auto-compact drift。
- 但連續多次 auto compact 仍會漂移。
- Codex 沒有 `/clear`：作法是「在同 project 內開新 chat」，等同 clear；所有 chat 都會列在 project sidebar，容易切換。

### 影像生成（內建）
- 因屬 OpenAI 生態，內建 GPT image 能力；不必另接 Higgsfield CLI 之類。
- 直接 prompt「幫我為這 5 大差異產背景圖」就能用。

## 與 Claude Code 並用模式

- Codex desktop app 右上可 toggle 內嵌 terminal，把 Claude Code 開在裡面。
- 等於 1 個視窗同時擁有 Codex desktop UI + Claude Code CLI。
- 兩工具混用比挑邊站更務實。

## 核心啟示

- **Tool agnostic 是新基本功**：押單一 vendor 等於把錢包與工作流交給對方政策決定。
- 從 Claude Code 跳 Codex 的學習成本約 5%；介面差異是漸進的，不是換語言。
- Codex 強在 GUI（plugin/skill 視覺管理、前端 annotation、影像生成、Queue/Steer）；Claude Code 強在 CLI 純粹度與大 context。並用比 either-or 划算。
- 訂閱建議：先 $20 plan 試 GPT-5.5；要 5.5 Pro 才升 $100。
