---
title: "2026-06-21 Daily Updates"
created: 2026-06-21
updated: 2026-06-21
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.185 · 2026-06-20（[Changelog](https://code.claude.com/docs/en/changelog#2-1-185)）

**繁中摘要**：stream stall 提示文字更新，並將觸發延遲從 10 秒調整為 20 秒，減少假性警告對使用者的干擾。

- **Stall 提示文字**：由「No response from API · Retrying in …」改為「Waiting for API response · will retry in …」，語意從錯誤狀態變成等待狀態，更準確反映實際情況
- **觸發門檻延長**：靜默 20 秒後才顯示提示（原為 10 秒），對高延遲 API 呼叫（如長 context 推理）更友善

---

## OpenAI Codex

### v0.141.0 · 2026-06-18（[Changelog](https://developers.openai.com/codex/changelog#codex-cli-01410)）

**繁中摘要**：remote executor 安全性與跨平台能力大幅升級，並新增 MCP server 整合與 Realtime 語音控制；多項 bug fix 補上安全性漏洞。

- **Noise relay 加密**：remote executor 改用經認證的 end-to-end 加密 Noise relay channel，傳輸層安全性提升
- **跨平台 remote execution**：跨邊界執行時保留 executor-native 的 working directory 與 shell 設定，減少環境差異問題
- **MCP server per thread**：selected executor plugin 可為每個 thread 啟動獨立的 stdio MCP server，agent 多工場景更靈活
- **App-server 子 thread 管理**：client 可列出 child thread 並關聯 external-agent import，多 agent 協作可追溯性提升
- **Realtime 語音控制**：新增 speech append 控制與 conversation entry 選項，語音 workflow 粒度更細
- **Bug fix**：修復 hook trust bypass 持久性、plugin capability routing、Windows sandbox 憑證恢復與 idle relay 保持等安全與穩定性問題

---

## GitHub Changelog

### 2026-06-19（[AI credits consumed per user now in the Copilot usage metrics API](https://github.blog/changelog/2026-06-19-ai-credits-consumed-per-user-now-in-the-copilot-usage-metrics-api)）

**繁中摘要**：Copilot usage metrics API 新增每位使用者每日 AI credits 消耗量，企業管理員可直接用 API 做配額追蹤與計費分析。

- **Per-user AI credits 欄位**：usage metrics API 回傳資料新增每人每日消耗量，與 usage-based billing API 來源一致
- **企業配額管理**：可程式化查詢個別成員用量，無需手動查 UI，有利自動化計費稽核或超量預警

---
