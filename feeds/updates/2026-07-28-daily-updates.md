---
title: "2026-07-28 Daily Updates"
created: 2026-07-28
updated: 2026-07-28
tags:
  - updates
  - opencode
---

## OpenCode

### v1.18.6 · 2026-07-27（[OpenCode Changelog](https://opencode.ai/changelog)）

**繁中摘要**：OpenCode v1.18.6 修復了跨分支切換時 repository cache 互相污染的問題，並改善 provider／MCP 狀態刷新的可靠性。

- **分支專屬 cache 修復**：修正 repository cache 未依分支區分的問題，過去刷新某一分支的 cache 會意外連動移動其他分支 checkout 的狀態，屬正確性層級的 regression 修復。
- **Provider 清單刷新**：修正在 V1 server 上連接 provider 或完成 provider OAuth 後，provider 清單不會自動刷新的問題。
- **Legacy MCP 狀態**：修正開啟 V1 workspace 時 legacy MCP 狀態未正確刷新的問題。
- **相容性**：改善桌面版與較新 client API 在多項流程上的相容性。

---
