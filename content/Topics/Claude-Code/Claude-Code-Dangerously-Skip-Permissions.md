---
title: "claude --dangerously-skip-permissions"
tags:
  - claude-code
  - cli
  - automation
created: 2026-04-09
updated: 2026-04-09
---

`--dangerously-skip-permissions` 是 Claude Code CLI 的旗標，啟用後會跳過所有權限確認提示，讓 Claude 全自動執行所有操作。

## 使用方式

```bash
# 互動模式
claude --dangerously-skip-permissions

# 搭配 -p 單次執行
claude -p "重構所有測試檔案" --dangerously-skip-permissions
```

## 適用場景

- **CI/CD pipeline**：在自動化流程中讓 Claude 無人值守執行任務
- **自動化腳本**：批次處理多個操作，不需逐一確認
- **信任環境**：在受控的開發環境中加速工作流

## 風險與注意事項

- 跳過**所有**檔案寫入、刪除、指令執行的確認
- 可能執行破壞性操作（`rm -rf`、`git push --force`、`git reset --hard` 等）
- 建議搭配受限環境使用（Docker container、sandbox、虛擬機）
- 不建議在含敏感資料或 production 環境中使用

## 搭配 CLAUDE.md 設定邊界

即使跳過權限確認，Claude 仍會遵循 `CLAUDE.md` 中的指示。可以在 `CLAUDE.md` 中明確限制行為，例如禁止執行特定命令或修改特定目錄。

## 替代方案：allowedTools

如果不想全部跳過，可以在 `.claude/settings.json` 中用 `allowedTools` 精細控制哪些工具自動允許：

```json
{
  "permissions": {
    "allowedTools": ["Read", "Glob", "Grep", "Bash(git *)"]
  }
}
```

這樣只有指定的工具會自動執行，其餘仍需確認，比全部跳過更安全。
