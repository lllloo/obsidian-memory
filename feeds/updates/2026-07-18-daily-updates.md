---
title: "2026-07-18 Daily Updates"
created: 2026-07-18
updated: 2026-07-18
tags:
  - updates
  - codex
  - opencode
  - copilot
---

## OpenAI Codex

**繁中摘要**：0.144.5 強化危險指令偵測，擋下更多 `rm` 變體並在拒絕時給出更清楚的理由，屬 CLI 安全把關的直接改動。（[changelog](https://developers.openai.com/codex/changelog)）

- **dangerous-command detection**：新增更多 `rm` 形式的偵測，降低誤放行破壞性刪除的風險。
- **拒絕理由更清楚**：指令被擋時回報更明確的原因，減少 debug 為何被拒的來回。

---

## OpenCode

**繁中摘要**：v1.18.3 為 Desktop v2 收尾期的維護版，最實用的是 command palette 現在能直接搜尋並開啟 session；其餘為快捷鍵與桌面版體驗修正。（[changelog](https://opencode.ai/changelog)）

- **command palette 開 session**：可從命令面板直接尋找並開啟既有 session，減少切換成本。
- **subagent picker 快捷鍵**：選到第一項時可用 Up Arrow 關閉 subagent picker。
- **Desktop 修正**：修好首頁捲動、WSL server 載入就緒判斷、custom agent 選擇器可見度等數項體驗問題。

---

## GitHub Copilot

### 2026-07-17 · Repository-level usage metrics GA（[Repository-level GitHub Copilot usage metrics generally available](https://github.blog/changelog/2026-07-17-repository-level-github-copilot-usage-metrics-generally-available)）

**繁中摘要**：Copilot usage metrics REST API 正式支援 repo 層級數據，新增兩個端點回傳每日、逐 repo 的 PR 活動細分，涵蓋 Copilot coding agent 與 code review。

- **兩個新端點**：提供 repo 級的每日 PR 活動 breakdown，可據此衡量 coding agent 與 code review 在各 repo 的實際使用量。

---

### 2026-07-17 · Copilot app 納入 usage metrics API（[GitHub Copilot app now available in the usage metrics API](https://github.blog/changelog/2026-07-17-github-copilot-app-now-available-in-the-usage-metrics-api)）

**繁中摘要**：usage metrics API 的 enterprise / organization 1-day 與 28-day 報表現在會列出 GitHub Copilot app 的使用量，給管理者更完整的採用度視野。

- **admin 可見度**：企業／組織層報表新增 Copilot app 使用數據，補齊原本缺的採用度面向。

---

### 2026-07-17 · Copilot code review 客製化強化（[Copilot code review: Customization and configurability improvements](https://github.blog/changelog/2026-07-17-copilot-code-review-customization-and-configurability-improvements)）

**繁中摘要**：Copilot code review 導入 firewall、自訂 setup 步驟與獨立 runner 設定，並改為讀取 head branch 的 custom instructions，讓調整審查規則時可即測即驗。

- **firewall + 自訂 setup 步驟 + 獨立 runner**：審查環境更可控，可依專案配置執行條件。
- **從 head branch 讀 custom instructions**：改動審查指示可直接在 PR 分支測試驗證，不必先併回預設分支。

---
