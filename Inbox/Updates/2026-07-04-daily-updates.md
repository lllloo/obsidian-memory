---
title: "2026-07-04 Daily Updates"
created: 2026-07-04
updated: 2026-07-04
tags:
  - updates
  - claude-code
---

## Claude Code

### 2.1.201 · 2026-07-03（[Changelog](https://code.claude.com/docs/en/changelog)）

**繁中摘要**：小版本，只調整 Claude Sonnet 5 session 的 harness reminder 行為。

- **Sonnet 5 harness reminder**：Sonnet 5 session 不再用對話中途的 system role 插入 harness reminder，避免污染 mid-conversation 的 system 訊息語境。

---

### 2.1.200 · 2026-07-03（[Changelog](https://code.claude.com/docs/en/changelog)）

**繁中摘要**：兩項預設行為變更值得留意——`AskUserQuestion` 不再自動繼續、permission 「default」模式更名為「Manual」；其餘為大量 background session/subagent 穩定性修復。

- **AskUserQuestion 不再自動繼續**：問題對話框預設不再自動 auto-continue，需經 `/config` 才 opt-in idle timeout；互動流程需人明確回應。
- **Permission 模式更名 Manual**：CLI、`--help`、VS Code、JetBrains 中「default」模式改稱「Manual」；`--permission-mode manual` 與 `"defaultMode": "manual"` 與舊 `default` 並存可用。
- **啟動 crash 修復**：`.claude.json` 內 `disabledMcpServers` / `enabledMcpServers` 被設成非 array 時啟動崩潰，已修。
- **Background session/subagent 穩定性**：修復 sleep/wake 後靜默停轉、Esc 取消後重跑、stale `daemon.lock` 導致 background agent 不再啟動、被 rate limit 截斷的 subagent 回傳空結果等多項；被 rate limit 或 server error 中斷的 subagent 現會把 partial 或錯誤回報給 parent 而非假裝成功。
- **無障礙輸出改善**：screen reader 隱藏裝飾字符、transcript 符號讀成短標籤、巢狀表格以 `Header: value.` 呈現。

---
