---
title: Claude Code + Obsidian 指揮中心設定
created: 2026-05-20
updated: 2026-05-20
source: https://www.youtube.com/watch?v=glAoiBWVkmU
published: 2026-05-15
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - obsidian
  - agentic-os
---

> [!info] 影片定位
> Chase 把 Obsidian 改造為 Claude OS 的「Command Center」：整合 terminal、自製 observability plugin、常用 skill/automation 一鍵啟動。重點不是抄他的版面，而是學會「Claude Code 寫一個 Obsidian plugin 來顯示你個人化的指標 + 用 skill 取代手動跑」的工作流。

## 為何 Obsidian 不只用來讀 markdown

- 只把 Claude Code 開在 vault 裡讀寫 markdown，遠遠浪費了兩者的潛力。
- Command Center 提供的是 **observability + 一鍵 skill 觸發 + 整合 terminal**，讓 Claude OS 在同一個窗格內運轉。
- 純 terminal 是強項但有缺點（visual report、自訂 dashboard 不直觀）；Obsidian 補上這層。

## Command Center 的構造

### 左：整個 vault
- 平常的 file explorer，可瀏覽所有 markdown。

### 中：自製 plugin（Claude Code 寫出來的）
- Chase 的版本分三層：
  - **Overview**：5 小時 token burn、訂閱數、最新 upload、行事曆、daily tasks。
  - **Audience**：YouTube 表現、哪些題目有效。
  - **Research**：trending GitHub（最近 7 天 AI 相關 top 10）、Hacker News、AI landscape headlines、X 對話、YouTube trending、content opportunity。
- 內容**完全自訂**：任何一塊都可用 Claude Code 一個 prompt 改掉或新增。
- 一鍵打開「常用 skill / automation」按鈕：
  - 例如 `Plan today`、`YT pipeline`、`weekly review`、`morning brief`、`inbox brief`、`deep research`。
  - 按下去等於開一個 **headless Claude（claude -p）** 跑該 skill；不會污染當前互動 session 的 context。

### 右：行事曆
- 沒有特殊 plugin，直接是 pinned browser tab。
- Obsidian 的 web viewer 即可塞進來。

### 整合的 terminal
- Claude Code 仍照原本方式在 terminal 用，UX 不變。
- 同窗格旁邊就是 dashboard，省去頻繁切視窗。

## 建構步驟拆解

### 1. 想清楚要看什麼（observability）
- 不是抄 Chase 的分區，而是問「你想在跑 Claude Code 時眼角同步看到什麼」。
- Chase 看到的，是他已經在做的事的具象化（例如 morning brief 對應一個已有的 skill）。
- 範例：
  - 多家公司的人 → 每個 tab 一家公司／一個 persona
  - 內容創作者 → audience metrics + research feeds
- 重點：dashboard 上的每個區塊應該對應「你本來就重複在做的工作」。

### 2. 美術 / 視覺風格用 Claude Design
- Plugin 本質是 code → 用 Claude Design 像建 web app 一樣生 prototype。
- **要 Claude Design 同時生 3-5 個 macro 風格變體**，再挑。
- Chase 的範例是 black + orange 配色。

### 3. 設快捷按鈕（skills / automations）
- 把日常會反覆觸發的 skill 變成按鈕。
- 點按鈕 → 開 headless Claude（`claude -p`）跑 skill → 不會佔用當前活躍 session。
- 同樣完全自訂，常用例：plan today、YT pipeline、weekly review、morning brief。

## Obsidian 必裝 plugins

從 Settings → Community plugins 加：

| Plugin | 用途 |
| --- | --- |
| Terminal | 把 terminal 嵌進 Obsidian，能在裡面跑 Claude Code |
| Hot reload | Claude Code 修改 plugin 後不需要重啟 Obsidian |
| Iconize | 給每個資料夾加圖示 |
| 自製 Command Center plugin | Claude Code 替你寫的那個 |

Core plugins 還要手動啟用 **Web viewer**（預設關），這樣點外部連結就在 Obsidian 內開，不必跳 Chrome。

## 檔案架構與 navigation

### Karpathy 三層結構
- `raw/` — 非結構化原料（research dump 等）
- `wiki/` — 內部 Wikipedia-like 報告，從 raw 提煉
- `outputs/` — 對外的 deliverable（投影片、文章成品等）

舉例流程：「研究 AI agents」→ research 結果進 raw → 整理成 wiki article → 衍生 slide deck 進 outputs。

### Index 檔的角色
- 每一層資料夾放一個 `index.md` 當「該層內容目錄」。
- Claude Code 從 vault → wiki → master index → topic index → 對應檔案，逐層 hop。
- 對 3 個檔案是 overkill，對 3000 個檔案是必須。

### Chase 自己的版本
- `archive / content / daily notes / dashboard / inbox / op / projects / raw / system / wiki`。
- 仍可歸到「unstructured / structured / output」三大桶，只是再分支。
- 規則：**你能講清楚 = Claude Code 能跟著走**；找不到結構就會狂吃 token 變慢，逼你引入 RAG 增加複雜度。

## CLAUDE.md 內容建議

- 「Less is more」。
- 最低要寫：
  - **Vault 結構**：每個資料夾在幹嘛
  - **Navigation pattern**：Claude 該怎麼從 vault 找到某類資料
  - **Obsidian best practices**：wikilink、embed、tag 慣例
- 目的：讓 Claude Code 產出的 markdown 自然帶 wikilink / embed / tag，回饋給人類也容易讀，形成 symbiotic loop。

## Anthropic 計費變動的影響

- Claude Code 的 headless / programmatic 使用（`claude -p`）**不再從 Max subscription 扣**。
- 取而代之：Anthropic 每月在 Max 訂閱外送 $200 額度供 headless 使用，**但用 API 計費**（比 Max 補貼貴約 10×）。
- Chase 的判斷：
  - 一般使用者點 dashboard 按鈕跑 skill 的頻率不會把 $200 用光；主要工作仍在 terminal。
  - 若真不夠用 → 把 layer 從 `claude -p` 換成 `codex` headless，5 分鐘 refactor 完事；輸出品質不差。

## 核心啟示

- Command Center 的價值在「**讓 dashboard / skill / terminal / vault 在同一畫面**」，而不是任何特定版面。
- Claude Code 寫一個自己的 Obsidian plugin 是這個工作流的真正解鎖點；Claude Design 用來迭代美術。
- File structure（含 index 檔）是 Claude Code 在大 vault 找東西不爆 token 的前提；想清楚自己的結構比抄 Karpathy 更重要。
- `CLAUDE.md` 重點放 vault 結構 + navigation + Obsidian 風格慣例，不要堆業務細節。
- 政策風險（headless 計費）用「換 layer 為 Codex headless」即可化解；不需綁死 Claude Code。
