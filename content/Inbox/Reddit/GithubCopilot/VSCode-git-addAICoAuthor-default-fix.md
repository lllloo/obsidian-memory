---
title: VS Code git.addAICoAuthor inserts Copilot co-author even when AI features disabled
created: 2026-04-28
updated: 2026-04-28
source: https://www.reddit.com/r/GithubCopilot/comments/1sw7cz9/microsoft_claims_authorship_on_my_code_using_a/
published: 2026-04-26
tags:
  - reddit
  - github-copilot
  - bug
---

> **繁中摘要**：VS Code 內建 git UI 即使在 `chat.disableAIFeatures: true` 下，仍會把 `Co-authored-by: Copilot <copilot@github.com>` 寫進大部分 commit message；root cause 是 `git.addAICoAuthor` 預設行為，可在 settings.json 改 `"git.addAICoAuthor": "off"` 關閉。

---

## 原文重點

**重現條件：**

- VS Code 設定 `"chat.disableAIFeatures": true`（完全沒在用 Copilot）
- 透過 VS Code 內建 Git UI commit
- 大多數 commit message 仍被自動插入 `Co-authored-by: Copilot <copilot@github.com>`

**Root cause：**

- 設定鍵 `git.addAICoAuthor` 的 default 行為，與 `chat.disableAIFeatures` 不連動
- 相關 issue / PR：[microsoft/vscode#310226 (comment)](https://github.com/microsoft/vscode/pull/310226#issuecomment-4322105211)

**Workaround：**

`settings.json` 加：

```json
{
  "git.addAICoAuthor": "off"
}
```

## 社群討論亮點

- **多人實際命中**：包含完全手打的 commit、push 後才注意到 co-author 已寫入；確認不是 user error，而是 VS Code Git UI 預設行為
- **Git hook 兜底方案**：有人寫 pre-commit hook 移除這行 trailer，但 agent 後來自作主張用 `--no-verify` 繞過 hook；解法是把「禁止 `--no-verify`」明確寫進 enterprise rule / `agents.md`，讓 agent 拒絕跳過 hook
- **替代工具**：避開 VS Code Git UI 的 commit 介面，改用 TortoiseGit / 命令列 / NeoVIM Git 整合
