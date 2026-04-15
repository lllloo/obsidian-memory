---
title: Kimi K2.5 是目前最強開源模型嗎？
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-31
source: https://www.youtube.com/watch?v=D4ICNmfXmwI
---

## 模型定位與架構

Moonshot AI 發布了 Kimi K2.5，宣稱是迄今最強大的開源模型，但這個說法已有誤差——它是**開放權重**（open-weight），而非開源（open source）：

- **開源**：程式碼、訓練資料與方法論公開，任何人可以檢視、修改和分發
- **開放權重**：只釋出最終模型權重，訓練程式碼與訓練資料集均未公開

Kimi K2.5 的架構與 Deepseek 的混合專家（Mixture of Experts）模型相似：

- 總參數量：1 兆
- 每次查詢實際啟動：320 億（僅 32B）
- 效果與 1 兆參數模型準確度相當，但所需運算能力和成本大幅降低
- 這是它被視為速度最快的開放權重模型之一的核心原因，也是相對便宜的主要原因

## Kimi K2.5 的兩大核心主張

**1. Agent Swarm 協調能力**

Kimi 2.5 以模型層級訓練出協調 agent swarm 的能力，可執行高達 100 個 sub-agents 的平行工作流程，橫跨 1,500 個協調步驟。

與 Claude 的差異：Claude 也能產生 sub-agents，但 Kimi 2.5 的協調器能力內建於模型本身。透過**平行 agent 強化學習**訓練，模型不只因正確答案獲得獎勵，也因平行化執行步驟的效率獲得獎勵。

根據官方宣稱：
- 內部評估顯示端到端執行時間減少 **80%**
- 在長程任務基準上超越 Opus 4.5 和不使用 swarm 的 Kimi 2.5

**2. 視覺 Agent 智慧**

聲稱在前端能力上特別強，能夠互動並實作互動式版面和豐富動畫。

Kimi 2.5 的多模態能力不是事後添加，而是在訓練過程中整合進去，避免了大多數模型的視覺與文字能力取捨問題，兩者的能力能夠同步提升。

更特別的是：它能接受**影片作為輸入**並生成程式碼，是最早能做到這一點的模型之一。

## 實測結果

### Agent Swarm 實測：Shadcn → Material UI 遷移

任務：將整個多頁面專案的 UI 從 Shadcn UI 遷移到 Material UI，要求使用 agents 平行處理各頁面。

- 建立待辦清單列出所有需要轉換的頁面
- 將相似頁面歸組（如：登入、注冊、忘記密碼歸為同一組）
- 實際產生 5 個 agents（多產生的是 CLI bug）
- 耗時約 **15 分鐘**完成
- 完成後自動驗證、清理不再使用的元件、確保移除 Shadcn 的依賴

**結果**：UI 外觀幾乎相同，只有 hero section 的文字與視覺從並排改為垂直堆疊。整個任務只使用了 **25% 的 context window**，表示適合長期執行的 agent。

**結論**：Agent swarm 可行，但不一定更快，在大型 codebase 上會更耗時。

### 視覺 Agent 實測：複製 Notion 介面

測試方法：錄製在 Notion 介面導覽和使用 `/` 指令的畫面，不告訴模型錄了什麼，讓它自行分析。

- Kimi 使用 `read media file` 工具分析影片
- 正確識別為 Notion 風格介面，列出所有功能，判斷是有 macOS 樣式視窗的 Notion clone
- 開始實作後，UI 準確——頁面圖示、Notion 功能都有，部分功能一開始未完全運作
- `/ 指令` 功能起初無法運作，給予修復 prompt 後，它自行迭代實作修正、驗證結果，最終讓整個介面像一個可用的 Notion clone

注意事項：影片和圖片會快速消耗 context window，使用大型檔案時要特別小心 context 膨脹。

## 整體評估

- 模型主張大致得到驗證
- 可能成為 Claude Code 的較便宜替代方案（Claude 的方案費用較高，Kimi 的定價較低）
- 目前 CLI 仍有 bug，對新產品而言屬正常
- Agent swarm 效能在小型專案和大型 codebase 之間有明顯差異
