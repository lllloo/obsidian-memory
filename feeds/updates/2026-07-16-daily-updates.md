---
title: "2026-07-16 Daily Updates"
created: 2026-07-16
updated: 2026-07-16
tags:
  - updates
  - opencode
---

## OpenCode

### v1.18.2 · 2026-07-15（[Changelog](https://opencode.ai/changelog)）

**繁中摘要**：v1.18.2 把 subagent 巢狀衍生改為預設關閉（可用 `subagent_depth` 設定深度上限），並強化 Meta 系列模型的 reasoning；其餘為 Desktop 快捷鍵與數個 UI 修復。

- **subagent 巢狀預設關閉**：subagent 預設不再自動衍生下層 subagent，需以 `subagent_depth` 明確放寬深度上限——改變多層 agent 編排的預設行為，避免無意間的遞迴展開。
- **Meta 模型 reasoning 強化**：提升 Meta 系列模型的推理表現。
- **Desktop 體驗修復**：新增 `Mod+N` 開分頁快捷鍵、release build 恢復 Help 按鈕、archive 時間為 null 的 session 重新顯示於首頁清單、Windows 移除與視窗控制衝突的 drawer 關閉鈕。

---
