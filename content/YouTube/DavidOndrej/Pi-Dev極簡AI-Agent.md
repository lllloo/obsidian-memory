---
title: 極簡 AI Agent 可以做任何事：Pi.dev 介紹
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-06
source: https://www.youtube.com/watch?v=9KYfx_GzY1o
---

## 概覽

- Pi 是目前最被低估的 AI 工具，也是 OpenClaw 的底層框架（harness）。
- 設計哲學：**極簡主義**——只有 4 個內建工具，系統提示不超過 1,000 tokens。
- 知名使用者：Shopify CEO Toby Lütke（個人助理與主要 Coding Agent）、Marc Andreessen（稱為「科技史前十大軟體突破」）。

## Pi vs OpenClaw

| 面向 | Pi | OpenClaw |
|-----|-----|---------|
| 目標族群 | 進階使用者、開發者 | 一般大眾 |
| 系統提示 | < 1,000 tokens | 12,000-16,000 tokens |
| 自訂彈性 | 極高（自訂 UI、工具、Skill） | 有限 |
| 透明度 | 完全透明，無隱藏抽象層 | 部分隱藏 |
| 安全性 | 無護欄，YOLO 模式 | 有基本保護 |

## 四大核心工具

1. **Read**：讀取任何檔案或資料夾，讓 Agent 了解系統狀態。
2. **Write**：建立新檔案，完成從頭建立 REST API 等任務。
3. **Edit**：修改現有檔案，只動必要的幾行，不重寫整個檔案。
4. **Bash**：執行任何終端機指令（安裝套件、執行測試、啟動伺服器、查看 git 狀態等）。

## Pi 的四個模組

- **Pi-TUI**：終端機 UI 函式庫，提供 Markdown 顯示、多行編輯器、載入動畫、無閃爍畫面更新。
- **Pi Coding Agent**：大多數人直接使用的主體。
- **Pi Agent Core**：大腦，定義自訂工具，執行 LLM 呼叫、工具執行、結果回饋的迴圈。
- **Pi-LLM**：統一 API 介面，支援 Anthropic、OpenAI、Google 等所有主流模型。

## 安裝步驟

1. 前往 pi.dev，複製一鍵安裝指令，貼入終端機執行（全域安裝）。
2. 輸入 `pi -v` 驗證安裝成功。
3. 建立 Pi Config 目錄（一次性設定）。
4. 將 OpenRouter API key 儲存至 `auth.json`。
5. 設定預設提供商（OpenRouter）與模型（避免每次都要手動指定）。

## 推薦模型選擇

| 使用情境 | 推薦模型 |
|---------|---------|
| 最強效果 | Opus 4.6 |
| 平衡（推薦起點） | Sonnet 4.6 |
| 節省費用 | GPT-5.4 mini |
| 性價比極高 | Kimi K2.5、MiniMax M2.7 |
| 本機輕量 | Gemma 4 |

## 設定 agents.md（全域系統提示）

- Pi 預設不帶 `agents.md`，但強烈建議建立，位置：`~/.py/agent/agents.md`
- 這個檔案就是 Pi 的個人偏好設定，可以寫入：
  - 偏好語言、回應風格（簡潔 vs 詳細）
  - 不需要徵詢許可就執行
  - 每次使用 TypeScript 而非 JavaScript
  - 任何個人化的工作習慣

## Pi 的自我更新能力

- Pi 可以修改自己的 UI 和擴充功能——這是 Claude Code 和 Codex **都做不到**的。
- 範例：「Create a matrix style theme for Pi」→ Pi 讀取自身設定 → 修改 UI → 執行 `/reload` 套用。
- 執行 `/reload` 即可在**不重啟終端機**的情況下套用所有變更。

## 必知指令

| 指令 | 功能 |
|------|------|
| `pi` | 啟動新會話 |
| `pi -c` | 繼續最後一個會話（最常用） |
| `pi -r` | 瀏覽並選擇歷史會話 |
| `/reload` | 重新載入所有設定 |
| `/tree` | 從當前對話開一個分支（不污染主線） |
| `/fork` | 在新的獨立會話中分叉 |

## Tree 功能（Branch 對話）

- 概念：類似 Git branch，在主線之外開岔處理子問題。
- 使用場景：正在開發功能時出現 Bug，用 `/tree` 分支修 Bug，修完回到主線。
- Pi 會自動為分支產生 context 摘要，主線 context 保持乾淨。

## Fork 功能

- 從當前對話的某個點開一個全新的獨立會話。
- 類比：fork GitHub repo——喜歡現有基礎，但想往不同方向發展。
- 歷史案例：Roo Code fork 自 Cline，Kilo Code fork 自 Roo Code。

## 會話儲存

- 所有會話自動儲存至 `~/.py/agent/sessions/`。
- `pi -c`：繼續最後一次會話（最常用）。
- `pi -r`：手動選擇任意過去的會話。

## 安全注意事項

- Pi 始終以 YOLO 模式運行——**沒有權限確認提示**。
- 不適合初學者；適合了解自己在做什麼的進階使用者。
- 建議：在測試新功能前，確保不在生產環境或重要系統上運行。
