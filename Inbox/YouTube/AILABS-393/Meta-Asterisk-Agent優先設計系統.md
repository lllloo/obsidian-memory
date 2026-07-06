---
title: Meta Asterisk：為 AI Agent 打造的前端設計系統
description: Meta 開源內部設計系統 Asterisk，8 年打磨、基於 React 與 StyleX、首個為 agent 而生，搭配 CLI 與自製 skill 讓 Claude Code 建站並避免 AI slop。
created: 2026-07-06
updated: 2026-07-06
source: https://www.youtube.com/watch?v=-HEdqzzYKco
published: 2026-07-03
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - design-system
  - frontend
---

## Asterisk 是什麼

- Meta 開源的內部設計系統，經 8 年打磨，至今仍跑在自家多款 app 上，屬於「已在規模上驗證過」而非新實驗。
- 主打特色是**首個為 AI agent 而生的設計系統**：agent 可讀懂整個系統並直接拿來建構，不只是給人用。
- 風格為專業極簡，混合品牌級設計與系統化思維，讓網站每個部分遵循同一套規則、彼此契合；可自訂品牌色。
- 技術基礎為 React + StyleX；屬 component library（類似 Shadcn），提供 150+ 個 Meta 風格元件可調整。
- 內建常見頁面模板（login、settings、chat），agent 可直接拉來當起點；playground 可即時預覽各 theme 的樣式、配色與字體。
- 目前仍在 beta，Meta 工程師持續更新。
- 核心原則是 **guidance over enforcement（引導優於強制）**：不加阻擋 agent 的 guardrail，而是給可直接使用的元件；慣例寫在 docs 與 examples 裡，而非塞進 prompt。

## 安裝與設定

- 在 GitHub 依所用 package manager 複製安裝指令，會裝入 core 與 theme（影片選 neutral theme）。
- 指令同時裝 CLI 並把 Asterisk 加為 project dependency。CLI 作為 agent 與 Asterisk 之間的橋樑，**逐步只載入需要的元件、不塞爆 context window**；Asterisk 也有 MCP，但 CLI 較佳正是因為不會一次灌滿 context。
- 用 Claude Code 這類 agent 建構時，還要跑 **Asterisk init** 讓專案準備好給 AI coding agent：
  - 會詢問幾個問題與是否要 template。
  - **Next.js 陷阱**：template 裝在 `pages` 資料夾，而新版 Next.js 用 `app` 資料夾（app router）；`app` 與 `pages` 不能共存否則報錯。需把 template 移到 `app`，或安裝時把頁面名改為 `app`。
  - init 會改寫 `CLAUDE.md` 與 `agent.md`（各 agent 的指引檔），加入該用哪些 Asterisk CLI 指令取得元件、依什麼流程建構的說明；讓 agent 從文件化的事實出發，而非自行猜測或改用 web search。`agent.md` 讓非 Claude 的 agent 也被導向這些文件。
- 即使選空白 template，樣式仍會填入 `globals.css`（存放全站通用的設計與 theme 樣式）。

## 用 Agent 建站的實際結果

- 給 agent 一段詳述想要網站的 prompt；Claude 先定位專案，依 `CLAUDE.md` 裡的 Asterisk workflow 呼叫 CLI，尋找 starter pack、design prompts 等符合方向的資源，再挑最合適的 template、拉元件、寫 code、跑起來。
- 產出的簡單網站雖符合極簡風，但有問題：一張卡片該對齊卻換行、產品未置中；配色像 **AI slop**（AI 建商業網站常見的藍黑配色）；且即使只是簡單網站也耗時約 16 分鐘。

## AI slop detector 與 Asterisk Max skill

- AI Labs 自製 design system（一組跨專案共用的 skill）中的 **AI slop detector skill**：對 agent 建出的網站跑批判式 review，找出所有算 AI slop 的 pattern，產出報告但**不自動修**（讓人自行迭代）；持續進化，若你指出某處仍像 AI slop 會把該 pattern 加入。
- 跑修正後，色盤從典型 AI slop 換成更極簡的配色、去除陳腔濫調的用字，成果明顯更像「設計過」而非「生成的」。
- 進一步做了 **Asterisk Max skill**，把 Asterisk 推到極限：
  - 最重要的是 **ground 模型**：跑 Asterisk manifest 指令產生一份列出所有可用命令與 flag 的檔案，讓模型知道 CLI 裡實際存在什麼、不必猜。
  - 依 `CLAUDE.md` 指示並用工具**實際看設計**（檢查乾淨的 grid、正確的深度層次），並含 evals（自動檢查與測試）。
  - 搭配 AI slop detector 一起跑：用 headless Chrome 反覆截圖、分析、修正，單次 run 內完成 review 與改善，成果比 Asterisk 單獨運作明顯更好。
