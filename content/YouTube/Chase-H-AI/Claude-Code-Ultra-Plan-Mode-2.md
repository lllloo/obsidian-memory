---
title: "Did Claude Code Just Get Plan Mode 2.0?"
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/eEYbwJWVQtQ
---

Chase H 實測 Claude Code 的 Ultra Plan 與傳統 Plan Mode 的差異，結論：速度大勝，但有明顯缺陷。

## Ultra Plan 是什麼

從 Claude Code 洩漏內容中出現的新功能，Anthropic 隨後正式發布。

- 在終端啟動 plan mode 後，將規劃推送至**雲端**執行
- 需要有至少一個 commit 的 GitHub repo
- 在瀏覽器中顯示規劃結果，可直接標注修改意見
- 批准後將計畫帶回終端執行

### 使用方式
```
/ultraplan
```
或直接說「ultra plan」

## 實測比較（Kanban Board Web App）

| 項目 | Local Plan Mode | Ultra Plan |
|------|----------------|------------|
| 規劃時間 | 5分30秒（且需重試） | **30秒以內** |
| 前端設計 Skill | 有使用（Google Fonts 等）| **完全忽略** |
| 程式碼品質 | 相當 | 多幾百行但相當 |
| 視覺效果 | 較精緻 | 較基本 |

## 主要問題

**Ultra Plan 無法正確呼叫 Skills**：即使在 prompt 中明確指定使用某 skill，Ultra Plan 仍會忽略。這不是單次問題，在額外測試中也重現。

Skills 是 Claude Code 最強大的原生功能之一，若無法正常調用，代價相當大。

## 結論

- Ultra Plan **不會**取代 Local Plan Mode
- 速度優勢明顯，適合不依賴 Skills 的簡單專案
- Skills 整合問題是重大缺陷，尤其對重度 Skills 用戶
- 功能仍很新，文件說明不足，可能持續改善
- **建議**：在複雜專案上自行測試，結果可能因專案性質而異
