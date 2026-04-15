---
title: 如何用 Paperclip 架設零人公司
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-01
source: https://www.youtube.com/watch?v=rx4w6zhrhPY
---

## 概覽

- Paperclip 是目前 GitHub 上最熱門的開源專案之一——3 週內突破 40,000 stars。
- 核心定位：**多 Agent 協作儀表板**，相當於把多個 Claude Code 等 Agent 組成一間公司。
- 把單一 Agent（如 Claude Code）視為一位員工，Paperclip 就是那家公司的管理系統。

## 解決什麼問題

- 傳統多 Agent 工作流：需要手動開幾十個終端機，難以追蹤進度，容易浪費 token。
- Paperclip 解法：
  - **24/7 運作**：Agent 在你睡覺時持續執行任務。
  - **支援任何 Agent**：Claude Code、Codex、OpenClaw、OpenCode 均可使用。
  - **可觀測性**：儀表板清楚顯示每個任務、決策、工具呼叫與費用。

## 組織架構範例

- 你（人類）= 董事會
- CEO Agent → 管理 CTO、CMO 等
- 各部門 Agent 各自負責不同職能
- 或採用扁平架構（所有 Agent 直接向 CEO 回報）

## 部署：VPS 而非本機

- 本機運行：關閉筆電即停止，且可能影響本機檔案安全。
- **推薦 VPS**（如 Hostinger）：
  - 24/7 持續運作
  - 安全隔離環境
  - 可遠端從任何裝置存取

## 安裝步驟（Hostinger 一鍵部署）

1. 前往 Hostinger，選擇 Paperclip 方案（推薦 24 個月）。
2. 選擇伺服器地點，選擇作業系統時搜尋「paperclip」選擇預設配置。
3. 填寫 Admin Email 與 Password（**務必儲存**，登入需要）。
4. 貼入 **Anthropic API key**（注意：Codex CLI 目前有 bug，無法在 Paperclip 中使用，請用 Anthropic）。
5. 點擊 Deploy，約 2 分鐘完成。
6. 前往 Hostinger 面板 → Docker Manager → Projects → Paperclip → Open，進入登入頁。

## Paperclip 儀表板功能

| 功能 | 說明 |
|------|------|
| Dashboard | 整體概覽：Agent 狀態、任務進度、月費用 |
| Inbox | 最近發生的事件 |
| Issues（任務） | 分派給 Agent 的個別任務 |
| Routines | 定期重複任務（Beta） |
| Goals | 長期目標（超越單次任務） |
| Projects | 多個任務的集合 |
| Agents | Agent 設定與管理 |
| Cost | 各 Agent 的 token 消耗與費用 |

## 設定 Agent

1. 建立第一個 Agent（如 CTO），初始任務：「Hire a team of 7 developers with appropriate roles for building advanced software.」
2. 若遇到 Codex 錯誤：點擊 Agent → Configuration → 切換 Adapter 為 **Claude Code（Anthropic）**。
3. 設定模型：**Opus 4.6**，thinking effort High。
4. 貼入 Anthropic API key，點擊 Test Environment 驗證（注意：成功時仍顯示黃色警告，看最底部是否有「Claude hello probe succeeded」）。

## 手動建立 Agent 範例（資安研究員）

- **角色**：Head of Cybersecurity
- **系統提示**：「你是資安主管，主動搜尋威脅、漏洞與攻擊事件，分析整個系統，確認是否受影響，若有則更新至最新安全版本。」
- **模型**：Opus 4.6，thinking effort Medium
- **Heartbeat 間隔**：每 300 秒（5 分鐘）自動執行資安檢查

## AI 未來工作型態觀點

- 現在：人類做大部分工作
- 未來：人類提供原始目標與方向，Agent 執行所有細節
- LLM 的根本限制：無法提供真正原創的重大發現（是下一個 token 的預測器）
- 但 Agent 已能勝任：研究、開發、測試變體、重複性管理任務
- 從 1 個 Agent 擴展到 100+ Agent 的管理工具——這正是 Paperclip 要解決的問題

## 如何開始使用 Paperclip

1. **第一步**：熟悉介面，點擊探索各功能區域。
2. **第二步**：嘗試不同類型任務（研究 → 開發 → 競爭分析）。
3. **第三步**：擴展到適合自己業務的應用場景。
- 不要一次自動化所有事情——循序漸進，測試哪種任務最有效。
- Agent 最適合的任務：研究、開發、測試大量變體（如郵件標題）。
- Agent 目前較弱的任務：原創創意、真正的文案寫作（但批量測試後仍能找出最好的）。

## 注意事項

- **Codex CLI bug**：目前在 Paperclip 中無法正常運作，請使用 Anthropic（Claude Code）。
- Opus 4.6 成本較高（每次任務約 $1 美元），建議監控 Cost 頁面。
- 可設定月度預算上限，避免意外費用。
- Paperclip 仍是非常新的專案（約 1 個月），部分功能仍有 Bug，遇到錯誤重新描述任務或換不同 Agent 嘗試。
