---
title: Claude Code 大型專案 Harness 設定
created: 2026-05-22
updated: 2026-05-22
source: https://www.youtube.com/watch?v=lGalJmyI78w
published: 2026-05-21
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - ai-coding
  - agent-development
---

## 核心觀點

大型 codebase 不是單靠更強的 model 就能穩定交付；真正影響結果的是 agent harness：agent 如何取得正確 context、何時被約束、哪些能力按需載入、以及如何避免在大專案裡被無關資訊拖垮。

影片把 Claude Code 的大型專案設定拆成幾個層次：短而準的 `CLAUDE.md`、hooks、skills、plugins、LSP、專案內部 MCP、sub-agents，以及 codebase map / 分層測試等導航輔助。

## Code Navigation：RAG 不適合大型程式碼庫

早期 coding agent 常用 RAG 式導航：把整個 codebase embedding 起來，query 時用 semantic search 取回片段。這在小型專案可用，但在大型專案會出現幾個問題：

- semantic match 容易拿到過期或相似但錯誤的檔案
- central index 可能跟實際檔案系統不同步
- agent 會根據取回片段幻覺不存在的 module 或 symbol

Claude Code 這類工具更接近開發者實際工作方式：透過 file system、shell、搜尋與精準讀檔逐步縮小範圍。這種方式比較不會把無關片段塞進 context，也更適合大型專案。

## CLAUDE.md 要短且分層

`CLAUDE.md` 是 session 開始時長駐 context 的專案知識，因此不能把所有細節都塞進根目錄文件。大型專案應把 root `CLAUDE.md` 控制在核心規則、全域慣例與不可違反的限制，避免長到干擾 agent 注意力。

若是 monorepo 或多架構專案，每個重要子目錄可以有自己的 `CLAUDE.md`，讓 agent 進入該區域時才載入局部規則。這比在 root 寫滿 frontend、backend、infra、測試、部署的所有細節更穩。

`CLAUDE.md` 也不是一次寫完就不動。模型能力會變，舊模型需要的提醒可能對新模型只是 token 浪費，因此要定期刪掉過時規則。

## Hooks 是強制約束

自然語言規則會被 context 淹沒，hooks 則能把關鍵行為變成強制動作。適合放進 hooks 的事情包括：

- session start 時載入必要 context
- pre-tool-use 阻止 agent 修改不該碰的檔案
- command 失敗時把錯誤回饋給 agent
- stop hook 在 session 結束後整理 learnings，更新專案規則
- lint / test / format 檢查

大型專案裡，hooks 的價值是把「希望 agent 記得」改成「agent 必須經過」。

## Skills 與 Plugins：按需載入專門知識

Skills 適合承載特定任務的流程與背景知識，讓 agent 需要時才載入。若把所有任務規則都放在 `CLAUDE.md`，會讓每次 session 都背著不相關資訊。

Plugins 則把 skills、hooks、MCP 等設定包成可分發單位。團隊協作時，plugins 可以確保每個成員取得相同的工作流與專案 context，不必各自手動安裝零散設定。

## LSP 與內部 MCP

LSP 讓 agent 用接近 IDE 的方式理解 symbol、definition、reference，而不是只靠文字搜尋。對 React、Next.js 這類常見框架，模型本身已有大量訓練資料；但對 C++ 或較冷門語言，LSP 會明顯降低找錯 symbol 的機率。

MCP 則適合連接專案內部工具、文件、資料源、analytics 或安全的修改介面。前提是主程式本身已經穩定，否則過早建立 MCP 會把未成熟系統的問題放大。

## Sub-agents 與大型專案分工

Sub-agents 的價值不是「更多 agent 比較強」，而是隔離 context。主 agent 負責 orchestration，子 agent 處理局部任務並回傳結果，可以避免主 context 被探索細節塞滿。

在大型專案裡，可為特定目錄或工作類型建立自訂 sub-agent，讓它帶有更精準的導航規則與輸出格式。這比所有探索都靠同一個泛用 agent 更節省 context。

## 其他大型專案慣例

- 測試應按子目錄分層，避免每次都跑整包測試造成 timeout
- 非主流架構可建立 codebase map，作為 agent 的目錄索引
- 使用 `.gitignore` / agent ignore 類規則，排除不該讀或不該改的檔案
- 每隔幾個月重新檢查 instructions、hooks、skills 是否仍符合目前模型能力

## 我的理解

大型專案的 Claude Code 設定重點不是堆更多 instructions，而是降低 agent 找 context 的成本，並把不可違反的規則移到可執行約束。`CLAUDE.md` 應該像全域憲法，skills 是按需流程，hooks 是守門員，LSP / MCP / codebase map 則是讓 agent 少猜、多查證的導航層。
