---
title: "2026-07-13 Daily Updates"
created: 2026-07-13
updated: 2026-07-13
tags:
  - updates
  - copilot
---

## GitHub Copilot

### 2026-07-08（[Deploy managed Copilot settings via MDM in VS Code and CLI](https://github.blog/changelog/2026-07-08-deploy-managed-copilot-settings-via-mdm-in-vs-code-and-cli)）

**繁中摘要**：enterprise 管理者現在可透過裝置原生 MDM 與檔案式設定，直接把 managed Copilot 設定派送到端點，補足既有 server-managed 通道。

- **MDM／檔案式設定派送**：除既有 server-managed 通道外，新增以 native mobile device management 與本機設定檔強制下發 Copilot 設定至 VS Code 與 CLI，適用受管裝置的離線或集中控管情境。

---

### 2026-07-07（[Add review cycles and time to adoption phases in the usage API](https://github.blog/changelog/2026-07-07-add-review-cycles-and-time-to-adoption-phases-in-the-usage-api)）

**繁中摘要**：Copilot usage metrics API 為每個 AI adoption phase 新增兩個 code-review 速度指標，擴充 enterprise 與 organization 報表的 adoption phase cohort 欄位。

- **review 速度指標**：usage API 回傳每個採用階段的 review cycles 與 time-to-adoption 指標，供企業量化 AI 導入對 code review 流程的影響。

---

### 2026-07-07（[Per-user budgets for cost centers in the billing UI](https://github.blog/changelog/2026-07-07-per-user-budgets-for-cost-centers-in-the-billing-ui)）

**繁中摘要**：enterprise 管理者可直接在 billing UI 的 cost center 管理處，為個別使用者設定 user-level 預算上限（限 GitHub Enterprise Cloud）。

- **cost center 個人預算**：在管理 cost center 與 budget 的 billing UI 直接建立 per-user 預算，細緻控管每位使用者的 Copilot 花費。
