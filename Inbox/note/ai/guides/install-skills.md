---
title: "Skills 安裝指南"
created: 2026-06-03
updated: 2026-06-04
tags:
  - skill
  - claude-code
  - copilot
  - cli
---

# Skills 安裝指南

透過 [vercel-labs/skills](https://github.com/vercel-labs/skills)，一次安裝技能可同時供 Claude Code、GitHub Copilot 和 OpenCode 使用。安裝後，多個工具都能獲得相同的最佳實踐與優化規則。

## 核心概念

**一次安裝，多邊都能用。** 安裝到共用的 `~/.agents/skills/` 目錄，Claude Code、GitHub Copilot 和 OpenCode 的技能目錄都透過 **Symlink** 連結至同一份源頭。

## 探索可用技能

前往 [skills.sh](https://skills.sh/) 查看所有可用的技能，或使用互動式命令發現：

```bash
npx skills find
```

## 安裝方法

例如安裝 `frontend-design` 技能（來自 Anthropic 官方技能集合）：

```bash
npx skills add anthropics/skills --skill frontend-design
```

或使用完整 URL：

```bash
npx skills add https://github.com/anthropics/skills --skill frontend-design
```

安裝時選擇 **Symlink** 選項。技能會儲存在共用位置 `~/.agents/skills/`，Claude Code、GitHub Copilot 和 OpenCode 的技能目錄會透過 Symlink 指向它。

## 管理技能

- **列出已安裝技能**：基本用法為 `npx skills ls -g`
- **更新技能**：常見指令為 `npx skills update` 更新已安裝技能
- **移除技能**：通常可用 `npx skills remove <skill-name>` 移除技能，或直接刪除共用目錄中的技能文件

## 常見問題

**Q: Symlink 和 Copy 有什麼差別？**

- **Symlink**：多個工具的技能目錄連結至同一份源頭，更新一次即可生效於所有工具
- **Copy**：每個工具各自儲存一份副本，便於隔離但需分別更新

## 參考資源

- [Skills GitHub](https://github.com/vercel-labs/skills)
- [skills.sh](https://skills.sh/)
