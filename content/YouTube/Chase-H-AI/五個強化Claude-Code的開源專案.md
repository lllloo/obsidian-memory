---
title: 五個強化 Claude Code 的開源專案（2026 年 3 月）
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-28
source: https://www.youtube.com/watch?v=6SnFH43qPAw
---

## AutoResearch（Karpathy）

約 60,000 星，三週前發布。本質是「機器學習演算法即服務」：

- 自動執行實驗迴圈：每次嘗試改善 `train.py`，成功則 git commit，失敗則 git reset
- **核心檔案**：
  - `problem.md`：定義任務，使用者只需編輯這個
  - `train.py`：LLM 會修改這個（相當於神經網路的 weights）
  - `prepare.py`：Karpathy 寫的基礎框架，不需修改
- **適用場景**（必須有二元評分）：Python 腳本效能優化、Prompt 優化、技能通過/失敗測試
- **不適用**：創意寫作、主觀評分的任務

實測：Shopify CEO 用 0.8B 參數模型跑 8 小時、37 次實驗，效率提升 19%。

## OpenSpace（HKUST）

1,700 星，4 天前發布。透過 MCP 監控技能使用品質，自動分入三個桶：

- `autofix`：技能完全失效，直接修
- `autoimprove`：技能有效但可優化
- `autolearn`：已達最佳，凍結不動

宣稱在 220 個真實世界任務測試中，使用改善後的技能可節省 46% tokens，任務品質從 40% 提升至 70%。

## CLI Anything（HKUST）

24,000 星，3 月初發布。兩步安裝後，指向任何開源專案即可自動生成 CLI 工具：
- 自動分析程式碼、執行測試、生成文件、發布為 Claude Code 工具
- 已驗證的專案：Blender、Inkscape、OBS、Zoom、draw.io、Notebook LM
- 首次生成後可繼續精煉，追加更多功能

## Claude Peers

約 1,000 星，上週發布。透過 MCP 伺服器 + SQLite 讓多個 Claude Code session 互相通訊：

- 第一個 session 啟動後自動運行，後續 session 開啟時會接收前面 session 的摘要
- 結合 Anthropic 「長期應用開發哈尼斯」架構（Generator → Executor → Evaluator 三角色），可讓「建立者 session」和「評估者 session」真正互相對話，解決 Claude Code 自評偏高的問題

## Google Workspace CLI（GWS）

Google 開發者所建，給予 Claude Code 存取整個 Google 套件的能力（Gmail、Docs、Sheets、Drive）：

- 可沙箱化設定：僅開放特定資料夾或 email 過濾條件
- 內建 Model Armor（Google 的 prompt injection 防護），可設定為僅警告或自動攔截
- 技能數量龐大，建議先讓 Claude Code clone 此 repo 後討論哪些技能對自己有用
