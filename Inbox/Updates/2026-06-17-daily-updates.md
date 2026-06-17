---
title: "2026-06-17 Daily Updates"
created: 2026-06-17
updated: 2026-06-17
tags:
  - updates
  - copilot
---

## GitHub Changelog

### 2026-06-16（[GitHub Models is no longer available to new customers](https://github.blog/changelog/2026-06-16-github-models-is-no-longer-available-to-new-customers)）

**繁中摘要**：GitHub Models 宣布退場，新客戶即日起無法使用；現有客戶暫時不受影響，但完整退場時程後續將另行公告。

- **新客戶封閉**：從即日起，未曾使用過 GitHub Models 的組織或企業帳號將看不到此功能入口，不可再開通。
- **現有客戶緩衝期**：已在使用的客戶可繼續使用，完整退場時程尚未公布——需持續關注後續公告，評估是否遷移到其他模型 API（如 OpenAI、Azure OpenAI）。

---

### 2026-06-15（[Copilot usage metrics now include more of your active users](https://github.blog/changelog/2026-06-15-copilot-usage-metrics-now-include-more-of-your-active-users)）

**繁中摘要**：Copilot 使用量報告改用伺服器端遙測補強客戶端訊號，活躍用戶統計更完整；REST API 回傳結果也新增 Business 與 Enterprise 席位的分類明細。

- **統計方式改變**：同時採計 server-side telemetry，先前因客戶端未回報而缺席的活躍用戶現在會出現在報告中，數字可能顯著上升。
- **API 回傳欄位新增**：企業版 Copilot 使用量 REST API 現在包含 Copilot Business 與 Copilot Enterprise 的席位分類，方便管理員分析授權使用率；Admin UI 儀表板同步更新。
