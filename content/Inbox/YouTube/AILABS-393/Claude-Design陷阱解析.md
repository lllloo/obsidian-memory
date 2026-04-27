---
title: Claude Design 其實是個大坑
created: 2026-04-27
updated: 2026-04-27
source: https://www.youtube.com/watch?v=GbuwosWEvHo
published: 2026-04-26
parent: "[[01.index]]"
tags:
  - youtube
---

## 核心論點

Claude Design 的話題與 demo 看似驚艷，實則只是把 Claude Code 換個包裝再賣一次。社群上瘋傳的炫技作品，多數並非工具本身能力的展現，而是來自 Opus 4.7 模型升級與工作流模板，而這些工作流在 Claude Code 也都跑得起來，並且更便宜、更彈性。

- Claude Design 上市時被稱作 Figma killer，導致 Figma 股價下跌
- 但本質是 Claude Code 包成另一個產品再賣
- Claude Design 多出來的編輯與 comment 功能，給 Claude Code 對應工具也能做到

## Claude Design vs Claude Code 實測

頻道用同一個 prompt 在兩邊各跑一次「打造社群網站」：

- **Claude Design**：產出兩個 design，整體優於早期 Claude 生成的 landing page，但仍有問題（其中一版 pricing 區段被截斷、完全沒有 footer）
- **Claude Code**（Opus 4.7、high effort）：在沒有 design harness、沒有特殊 prompt 的情況下，產出的設計已與 Claude Design 平起平坐；只有 sign-up 按鈕字色挑得不太好

結論：Claude Design 並沒有壓倒性優勢，差距更多在工作流與模板，不在工具本身。

## 為什麼 Designer 該直接用 Claude Code

- **可迭代次數多**：Claude Code 使用量限制比 Claude Design 寬鬆，可以實驗更多變體
- **能堆疊在現有站點上**：每次不必從零開始
- **直接輸出可上線的 code**：不是 prototype，不需要工程師重做一次
- **成本問題**：Claude Design 雖然不吃其他額度，但用量燒得異常快
  - 有用戶在最高 max plan 上，約 20 次設計迭代就用光當週額度
  - 也有人 1 小時就吃完額度，產出仍只是 Claude Code 一發就能做出來的簡單設計
  - 在 designer 真正需要大量試錯時最致命

## 真正變強的是 Opus 4.7，不是 Claude Design

Claude Design 看起來厲害，主要是模型本身升級：

- Opus 4.7 是當前 SOTA，在多個 benchmark 上全面進步
- 關鍵升級在 vision：
  - Opus 4.6 影像解析上限 1.15 megapixels
  - Opus 4.7 提升到 3.75 megapixels
- 高解析 vision 表示模型能更精準解讀 reference design，挑出以前漏掉的細節
- 也因此前端設計（Anthropic 過去的弱點）被補齊，模型本身就更有品味、更有創意

換句話說，Claude Design 是 Anthropic 借模型升級做的行銷重包裝。

## 用 Claude Code 複製 Claude Design 工作流

Claude Design 的核心特色之一是先用大量問題澄清需求，再開始設計。Claude Code 用一個 skill 就能複製這個流程：

- skill 內含詢問會話的指示、follow-up 觸發條件、流程定義
- 範例問題庫、不同類型網站的 layout 草稿（讓模型知道元素位置如何擺）
- prompt 進來時，skill 自動針對缺口提問，補完後直接出 code
- 沒有「設計 → code 交接」的斷點，迭代不受時數限制

實測下來，產出的 UI 與 Claude Design 同 prompt 結果差異不大。Claude Design 的優勢只剩在某些情況下會多加一點微互動動畫，讓網站更沉浸。

## 那些「scroll-interactive」demo 的真相

X 上瘋傳的 Claude Design 沉浸式 demo，多半是：

- 用 video 當背景，視覺感大幅加分
- 套用現成的 prompt 模板（網路上一抓一大把），模板會附帶背景影片連結與實作 guideline
- 任何 agent 都能跑相同 prompt，不限於 Claude Design

正式 production 級網站實作建議使用：

- **Lenis**：許多 production app 採用的滾動套件
- **GSAP**：最熱門的動畫函式庫之一，能做出沉浸式互動

頻道測試：下載一段影片，prompt 只告訴 Claude Code「拿這個當 hero section、用這組色票」，其餘讓它自己生。只修正過一次（解釋影片內容），就完成完整 landing page，包含動畫與互動。

## Claude Code 的設計加分項

可疊加的 skill 與函式庫，讓 Claude Code 在設計上彈性遠勝 Claude Design：

- **Scrollytelling skill**（open-source）：用簡單 prompt 就能實作多階滾動敘事，深度超越 Claude Design 預設能做的
- **內建 UI library 整合**：直接把 Shadcn、Aceternity、Hero UI 等元件集合接進來
  - 元件已經內建大量動畫
  - 模型不需要再去想每個元件該長怎樣，可以專注在整體設計
- **front-end design skill** 或客製化 skill：用 skill creator 分析專案現況再生對應 skill
- **MCP server**：例如 Shadcn MCP，agent 自己安裝對的元件，不用人工指定
- 用 design library 而非純生成可避免「一看就是 AI 做的」感

## Git 整合差距最大

Claude Design 的 GitHub 整合相當基礎：

- 只能從連結的 repo 讀取檔案、參考設計
- 主要是 read & reference，幾乎不修改 repo

Claude Code 直接做 full git operations：

- commit、branching 等都做
- 實作出問題或想回到舊版可直接 revert
- 適合反覆嘗試 prototype

進一步可以用 parallel agents + git worktree 模擬 Claude Design 的「探索多版本」：

- 用 sub-agent 在獨立 worktree 各做一個變體
- 同時得到多種設計，挑選最喜歡的合進 main，其他刪掉
- 比 Claude Design 的探索流更可控、更省時間
- 即使不是 Claude Design 生成，產出的設計仍具美感（含用 code 畫出來的 SVG 元素，整體平衡更好）

## 結論

Designer 不需要切換到 Claude Design——直接在 Claude Code 上：

- 用 skill 複製問答式工作流
- 用 Lenis、GSAP、Shadcn 等成熟 library
- 用 parallel agents + worktree 探索變體
- 用 git 保留可回溯的版本

得到等同甚至更好的結果，且不會被週額度卡死。建議直接在 HTML 上做 mock-up，不必走 Claude Design 或 Figma 中轉。
