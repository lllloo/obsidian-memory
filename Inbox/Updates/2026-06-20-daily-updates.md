---
title: "2026-06-20 Daily Updates"
created: 2026-06-20
updated: 2026-06-20
tags:
  - updates
  - claude-code
  - codex
  - copilot
---

## Claude Code

### v2.1.183 · 2026-06-19（[Changelog](https://code.claude.com/docs/en/changelog#2-1-183)）

**繁中摘要**：Claude Code 2.1.183 強化 auto mode 的安全護欄，阻擋未經授權的破壞性 git／IaC 指令，並修復多個影響 subagent、MCP 與 tmux 的重要 bug。

- **Auto mode 安全強化**：`git reset --hard`、`git checkout -- .`、`git clean -fd`、`git stash drop` 在用戶未明確要求捨棄本地變更時一律阻擋；`git commit --amend` 僅限 agent 本 session 自己建立的 commit；`terraform destroy` / `pulumi destroy` / `cdk destroy` 需明確指定 stack 才允許——大幅降低誤毀工作狀態的風險。
- **Deprecated model 警告**：`-p` print mode 與 agent frontmatter 設定的 model 若已 deprecated 或被自動升版，現在會在 stderr 顯示警告，方便及早更新設定。
- **`attribution.sessionUrl` 設定**：可選擇隱藏 commits / PR 中的 claude.ai session 連結，適用 web 與 Remote Control session。
- **`/config` 改善**：新增 `--help` 列出所有 shorthand key；Enter / Space 均可切換 toggle 設定，Esc 改為儲存並關閉（原為 revert）。
- **MCP 安全修復**：需要驗證的 MCP server 不再在 headless / SDK mode 把 auth-stub tools 暴露給 model。
- **Subagent 修復**：修復 WebSearch 在 subagent 中回傳空結果、`thinking.disabled` 觸發 400 錯誤、model 只回傳 thinking block 時 turn 靜默結束等問題。
- **其他值得注意**：移除啟動畫面的 "setup issues" 提示行（改跑 `/doctor`）；修復 tmux teammate pane 因 shell rc 初始化慢而無法啟動；修復 scheduled task / webhook trigger 被誤判為鍵盤輸入。

---

## OpenAI Codex

### Codex app 26.616 · 2026-06-18（[Changelog](https://developers.openai.com/codex/changelog#codex-app-26616)）

**繁中摘要**：Codex macOS 應用新增 Record & Replay，可將手動示範的操作流程錄製成可重用技能；同時支援 local 與 remote host 之間的 thread handoff。

- **Record & Replay（macOS）**：錄製一次示範操作即可轉成可重複呼叫的 skill，適合把常見 workflow 自動化而不需手寫 prompt。
- **Thread handoff**：任務可在 local 與 remote host 之間交接，方便混合環境下的 agent 工作流。
- **Automation run history 批次操作**：可對歷史執行記錄進行 bulk action，加速管理大量自動化任務。

---

## GitHub Changelog

### 2026-06-18（[Copilot-authored pull requests now included in author searches](https://github.blog/changelog/2026-06-18-copilot-authored-pull-requests-now-included-in-author-searches)）

**繁中摘要**：`author:@me` 等 PR 搜尋現在會一併回傳 Copilot cloud agent 代你開的 PR，讓 human 與 agent 建立的 PR 可在同一個介面統一追蹤。

- **`author:` 搜尋含 Copilot PR**：`github.com/pulls` 的 `author:@me` 搜尋及 PR 列表的 Authors 篩選器，現在都會顯示 Copilot 代開的 PR，不需再另外切換 filter 查找。

---
