---
title: "claude --dangerously-skip-permissions"
created: 2026-04-09
updated: 2026-04-25
tags:
  - claude-code
  - cli
  - automation
---

`--dangerously-skip-permissions` 是 Claude Code CLI 的旗標，**等同於** `--permission-mode bypassPermissions`。

啟用後，Claude Code 會跳過一般權限提示與 safety checks；**唯一仍會保留的提示，是對受保護路徑的寫入**。

## 使用方式

```bash
# 互動模式
claude --dangerously-skip-permissions

# 搭配 -p 單次執行
claude -p "重構所有測試檔案" --dangerously-skip-permissions
```

## 它實際跳過了什麼

- 一般工具權限提示
- 多數原本要逐次確認的 tool approval 流程
- auto mode 的 background safety checks（因為這不是 auto mode）

## 仍然不會無提示放行的東西

官方文件明確列出：**受保護路徑寫入**在所有模式下都有額外保護。

另外，**明確的 deny rules 仍然是硬邊界**；`bypassPermissions` 的重點是略過提示，不是把所有限制都拔掉。

常見受保護位置包含：

- `.git`
- `.vscode`
- `.idea`
- `.husky`
- `.claude`（但 `.claude/commands`、`.claude/agents`、`.claude/skills`、`.claude/worktrees` 是例外）

## 適用場景

- **隔離容器 / VM / devcontainer**：你願意把整個工作區交給 Claude 自動跑
- **受控自動化腳本**：你已經用 sandbox、deny rules、測試與環境隔離把風險壓低
- **短生命週期實驗環境**：壞了就整包砍掉重來

## 風險與注意事項

- **沒有 prompt injection 防護**：官方直接建議如果你要「少提示但保留安全檢查」，應優先考慮 `auto mode`
- **CLAUDE.md 不是硬安全邊界**：它可以降低 agent 做傻事的機率，但不是 OS-level enforcement
- **會直接執行高風險命令**：像 `rm -rf`、`git reset --hard`、`git push --force` 這類都可能在無提示下發生
- **不適合 production 或含敏感資料環境**

## 比較安全的替代方案

### 1. `acceptEdits`

適合你想少按很多次確認，但還是保留大部分 Bash / network prompt 的場景。

### 2. `auto mode`

如果你的需求是「盡量無提示，但要有 background classifier 幫我攔危險操作」，選 `auto` 比 `bypassPermissions` 合理。

### 3. Fine-grained permission rules

不要用舊版 `allowedTools` 寫法；官方 `settings.json` 用的是 `permissions.allow / ask / deny`：

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Bash(git status)",
      "Bash(git diff *)"
    ],
    "ask": [
      "Bash(git push *)"
    ],
    "deny": [
      "Read(./.env)",
      "Bash(curl *)"
    ]
  }
}
```

這樣可以做到「大多數安全操作免問，但危險操作仍要問或直接封鎖」。

## 相關

- [[Claude-Code-效率技巧與設定]] — 權限模式 cycle、`Shift+Tab` 與日常操作

## 來源

- [CLI reference](https://code.claude.com/docs/en/cli-reference)
- [Choose a permission mode](https://code.claude.com/docs/en/permission-modes)
- [Configure permissions](https://code.claude.com/docs/en/permissions)
- [Claude Code settings](https://code.claude.com/docs/en/settings)