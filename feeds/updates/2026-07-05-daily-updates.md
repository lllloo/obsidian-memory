---
title: "2026-07-05 Daily Updates"
created: 2026-07-05
updated: 2026-07-05
tags:
  - updates
  - copilot
---

## GitHub Copilot

### 2026-07-02（[Improved accuracy and coverage in Copilot usage metrics reports](https://github.blog/changelog/2026-07-02-improved-accuracy-and-coverage-in-copilot-usage-metrics-reports)）

**繁中摘要**：Copilot usage metrics API 三處修正讓報表更完整，最該知道的是 Copilot CLI 的建議行數終於計入（舊版一律報 0）；若靠此 API 量化 CLI 產出，要注意版本門檻造成的低估。

- **CLI 建議行數納入**：`loc_suggested_to_add_sum` / `loc_suggested_to_delete_sum` 現含 Copilot CLI 活動，需 CLI ≥ 1.0.57；1.0.64 起加入去重避免重複計算，1.0.57–1.0.64 之間可能略微低估。
- **IDE 覆蓋擴大**：原本只在 server-side telemetry 可見的使用者，其 IDE 與 plugin 版本現會列入 `totals_by_ide`。
- **計費歸屬修正**：未關聯到組織的 AI credit 消耗改為正確歸屬，server-side-only 使用者也對上帳單資料，總量更貼近實際消耗；既有已報數值不變，僅補上先前未報部分。

---
