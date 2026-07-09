---
title: "claude --dangerously-skip-permissions"
created: 2026-04-09
updated: 2026-06-23
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
| 想盡量無提示但要 background safety checks 攔危險操作 | `auto mode`（需較新版本、Opus 4.6 / Sonnet 4.6 以上；預設僅 Anthropic API，其他 provider 需設 `CLAUDE_CODE_ENABLE_AUTO_MODE=1` 開啟） |
| CI / 鎖死環境，只跑 pre-approved 工具與唯讀 Bash | `dontAsk` |
| 大多數安全操作免問、危險操作問或封鎖 | fine-grained `permissions.allow / ask / deny` |

## 還沒被 bypass 的東西

注意：bypass 略過的是 **`allow` 規則與受保護路徑保護**——`allow` 規則在此模式失效（因一切已預設核可），近期版本起連受保護路徑（`.git`、`.vscode`、`.idea`、`.husky`、`.claude` 等）也一併放行（更早版本仍會提示，確切切換以官方 release notes 為準）。所以**受保護路徑在 bypass 下不是硬邊界**。但 `deny` 與顯式 `ask` 規則並沒有被略過，真正擋得住的有這幾道：

- **`deny` 規則**——在每個模式（含 bypass）都生效，會直接封鎖，是真正的硬邊界
- **顯式 `ask` 規則**——在 bypass 下仍強制跳提示
- **`rm -rf /` / `rm -rf ~` circuit breaker**——刪檔案系統根目錄或家目錄仍會提示，防模型誤刪
- **root / sudo 拒啟動**——Linux / macOS 下以 root 或 `sudo` 啟動會被拒（除非在受認可的 sandbox，如 dev container）
- **sandbox OS-level 隔離**——容器 / VM 的檔案系統與網路隔離才是真正的邊界
- **CLAUDE.md 規則 ≠ 硬邊界**——只能降低 agent 做傻事的機率，不是 OS-level enforcement
- **沒有 prompt injection 防護**——任何 bypass 模式都沒有；要無提示又要安全檢查，改用 `auto mode`

## 相關

- [[Claude-Code-規則系統設計]] — CLAUDE.md / Rules / Hooks 三層機制
- [[Claude-Code-Skills]]

## 來源

- [權限模式官方文件](https://code.claude.com/docs/en/permission-modes)
