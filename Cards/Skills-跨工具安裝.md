---
title: Skills 跨工具安裝
created: 2026-06-03
updated: 2026-06-22
tags:
  - skill
  - claude-code
  - copilot
  - cli
---

# Skills 跨工具安裝

[vercel-labs/skills](https://github.com/vercel-labs/skills) 的核心價值是**一份 skill 多工具共用**：安裝到共用的 `~/.agents/skills/`，再讓 Claude Code、GitHub Copilot、OpenCode 各自的技能目錄 symlink 指向同一份源頭，更新一次全部生效。

## symlink vs copy：怎麼選

這是安裝時唯一要做的判斷：

- **symlink（預設）**：多工具指向同一份源頭，改一次到處生效。日常自用、想保持各工具一致時選這個。
- **copy**：每個工具各存一份副本，彼此隔離。要在某工具改 skill 而不影響其他、或要釘住特定版本不被更新波及時才選 copy。

> 取捨本質：symlink 換「一致與省維護」，copy 換「隔離與可釘版本」。沒有隔離需求就用 symlink。

## 常用指令

```bash
npx skills find                                   # 互動式探索可用技能（也可逛 skills.sh）
npx skills add anthropics/skills --skill frontend-design  # 安裝指定 skill（選 symlink）
npx skills ls -g                                  # 列出已安裝
npx skills update                                 # 更新
npx skills remove <skill-name>                    # 移除（或直接刪共用目錄的檔）
```

`add` 也接受完整 URL（`npx skills add https://github.com/anthropics/skills --skill ...`）。

## 參考資源

- [Skills GitHub](https://github.com/vercel-labs/skills)
- [skills.sh](https://skills.sh/)
