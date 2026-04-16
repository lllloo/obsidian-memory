---
title: Google Antigravity 突然變得合理了
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-17
source: https://www.youtube.com/watch?v=e4giCKHIJy8
parent: "[[01.index]]"
---

## 主流 AI 程式編輯器比較

目前市場上有多種 AI 程式編輯器，各有特色：

- **Claude Code**：公認最佳，尤其搭配 Opus 模型，但費用較高
- **Cursor**：開發者喜歡程式碼與 agent 操作並排顯示，但也有自身問題
- **Google Antigravity**（搭配 Gemini 3）：因模型能力與免費方案而迅速在開發者間流行，比 Cursor 更新，但在許多功能上實作得更好

任何好工作流程的關鍵都是 **context 管理效率**。Anthropic 發布了為長期任務設計的 agent harness，Cursor 也發布了自己的 harness。這些原則大部分適用於所有 agent，本文將這些原則應用到 Antigravity 上。

## Agent Harness 的三個核心組成

1. **指示（Instructions）**：引導 agent 行為的 system prompt 與規則，內建於工具本身
2. **工具（Tools）**：附加於 agent 的工具，包括檔案編輯、程式碼搜尋、終端機執行
3. **使用者互動方式**：如何下 prompt、如何追蹤回應

Harness 很重要，因為不同模型對相同 prompt 的反應不同。例如，Claude 在 XML prompt 上表現優異，其他模型可能在 markdown 上表現更好。因此 harness 必須針對特定模型量身打造。

## 規劃先於實作

實作前規劃是確保程式碼符合期望的必要步驟。Antigravity 的規劃功能最令人喜愛的一點是可以透過評論輕鬆修改計畫：

- 啟動規劃模式後，系統會徹底分析指示與既有 codebase，產生詳細計畫
- 仔細閱讀計畫至關重要，確保實作符合願景
- 只需在不符合目標的行加上評論，系統就會將修改納入修訂版計畫
- 持續精煉直到計畫完美，然後讓 agent 自主實作

即使實作結果不理想，也應回到規劃模式修改計畫，而非用後續 prompt 修補。

## Context 管理

計畫完成後，要為每個 agent 提供完成任務所需的 context。常見錯誤是手動標記每個檔案——這會將整個元件都載入 context，即使只需要其中一個函式。

正確做法：讓 agent 的搜尋工具用 `grep` 只取得它需要的特定片段。

**新對話的時機：**
- 每個新任務
- agent 表現混亂或一再犯相同錯誤時
- 完成一個邏輯工作單元之後

例外：同一功能的持續工作、需要同一討論的 context、除錯 agent 已實作的功能。

## 擴充 Agent 能力

**規則（Rules）：**
- 定義專案特定指引，讓 agent 一致遵循
- 儲存在 `.agent` 資料夾下的 `rules` 資料夾中，以 markdown 檔案撰寫
- 範例：加入 WCAG 無障礙合規規則，agent 就會在規劃時自動納入

**Skills：**
- 遵循 Anthropic 制定的開放標準，包含指示、腳本和領域知識
- 在 agent 判斷相關時動態載入，維持 context 管理
- 位於 `.agent` 資料夾中，每個 skill 有一個 `skill.md` 檔案
- 使用方式：指定想用的 skill 和要執行的任務

## 圖片分析的應用

模型的圖片理解能力越來越強：

- **UI 實作**：截圖想實作的設計，讓 agent 直接依截圖實作
- **除錯**：UI 問題用截圖說明比文字描述更清楚，agent 看圖後直接修復

## 測試驅動開發（TDD）

AI 開發同樣需要遵循軟體開發最佳實踐，TDD 與 agent 配合的原因是：agent 有明確的成功標準可以優化，能夠朝目標逐步改進。

流程：
1. 只給 prompt 請 agent 撰寫測試案例，描述輸入、輸出和測試行為，**明確指示不要寫實作程式碼**
2. 對測試案例滿意後，請 agent 執行測試（此時因無實作而失敗）
3. Commit 測試到 git，建立記錄防止 agent 後來修改
4. 請 agent 撰寫 endpoint 的實作，**明確指示不要修改測試**
5. 持續迭代直到所有測試通過

## Codebase 上手

開始在 agent 上使用新 codebase 時，像問隊友一樣提問。agent 會用 `grep` 和語義搜尋挖掘 codebase 找答案，同時理解專案的運作方式。了解 codebase 結構後，實作新功能會更容易。

## Git 工作流程

Git 不只是版本控制，也是 coding agent 的知識庫：

- 清楚的 Git commit 提供知識庫、功能管理和最後穩定版本的追蹤
- 若 agent 修改了不該動的東西可以輕鬆回滾
- 建立可重用的工作流程指令，強制執行 commit 格式（含安全與程式碼審查前置檢查）

## 程式碼審查

AI 生成的程式碼絕對需要審查：

- 使用自訂工作流程，依嚴重程度標示問題，列出需執行的所有檢查
- 可整合 linter 和測試
- 用 Code Rabbit、Sentry 等 AI 工具進行進階分析，在每個 PR 上捕捉問題
- 請 agent 建立 Mermaid 圖表識別架構問題，視覺化呈現容易發現關鍵問題

## 平行 Agent 執行

同時執行多個 agent 能顯著改善效能：

- 各 agent 分配不同任務，使用不同模型（各模型各有所長）
- Antigravity 的 agents 共用工作區，讓各 agent 在獨立分支工作，完成並通過檢查後才合併到主分支

## Debug 模式

遇到難以找出的 bug 時，Debug 模式是最佳解決方案——採用以證據為基礎的方法，生成日誌語句，讓除錯過程更系統化。

Antigravity 沒有原生的 debug 模式，可用 debug mode skill 實作：

- 包含除錯非預期行為的完整指示
- 採用假設驅動的多階段方法
- 由腳本和參考資料引導，大幅提升可靠性
