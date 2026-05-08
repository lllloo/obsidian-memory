---
title: "claude --dangerously-skip-permissions"
created: 2026-04-09
updated: 2026-05-08
tags:
  - claude-code
  - cli
  - automation
---

`--dangerously-skip-permissions`（等同 `--permission-mode bypassPermissions`）跳過權限提示，**僅用於有隔離邊界的環境**——容器 / VM / devcontainer、受控 sandbox 自動化腳本、壞了能整包砍掉的短期實驗環境。

主機本機 dev、production、含敏感資料時都不該開——`rm -rf`、`git reset --hard`、`git push --force` 會無提示直接執行。

## 不要跟 `auto mode` 搞混

`bypassPermissions` 重點是「略過提示」不是「拔掉所有限制」；如果只是「少按確認」需求，更細粒度的權限模式更合適：

| 場景 | 用 |
|---|---|
| 想少按確認，但還要看大多數 Bash / network 提示 | `acceptEdits` |
| 想盡量無提示但要 background safety checks 攔危險操作 | `auto mode` |
| 大多數安全操作免問、危險操作問或封鎖 | fine-grained `permissions.allow / ask / deny` |

## 還沒被 bypass 的東西

- **deny rules**——即使 bypass 也擋（硬邊界）
- **受保護路徑**——`.git`、`.vscode`、`.idea`、`.husky`、`.claude` 等部分子目錄官方有額外保護，但細節可能隨版本改
- **CLAUDE.md 規則 ≠ 硬邊界**——只能降低 agent 做傻事的機率，不是 OS-level enforcement
- **沒有 prompt injection 防護**——任何 bypass 模式都沒有

## 相關

- [[Claude-Code-規則系統設計]] — CLAUDE.md / Rules / Hooks 三層機制
- [[Claude-Code-Skills]]

## 來源

- [權限模式官方文件](https://code.claude.com/docs/en/permission-modes)
