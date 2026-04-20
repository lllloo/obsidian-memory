---
title: Claude Code 命名規則
created: 2026-04-20
updated: 2026-04-20
source: https://code.claude.com/docs/en/slash-commands
tags:
  - claude-code
  - naming-convention
  - skill
  - slash-command
---

## 命名格式

`<家族前綴>-<動作>`，全小寫 kebab-case。

## 規則

1. **同家族共用前綴**：相關 command / skill 用共同前綴分組。例如 vault 家族：`vault-check`、`vault-topic-moc`、`vault-youtube-sync`
2. **極短捷徑可例外**：單一入口且高頻使用的保留純名，如 `ob`、`vault`
3. **commands 與 skills 共用同一套命名規則**：兩邊不能撞名，否則會互相遮蔽（參考 anthropics/claude-code issue #15842）
4. **不用子目錄 namespace**：Claude Code v2.1.88+ 對 `.claude/commands/<subdir>/*.md` → `/<subdir>:<cmd>` 的解析仍不穩定（issue #2422、#1504），扁平命名更穩
5. **description 要寫清楚觸發條件**：frontmatter description 中用「Use when...」「觸發詞...」明示，Claude 才會在對話中自動叫用

## 為什麼用 kebab-case

- Claude Code 官方 skills 文件明定 skill 名稱與資料夾名都用 kebab-case
- Plugin 使用 `plugin-name:skill-name` namespace，與 kebab-case 一致
- 避免底線、camelCase 的視覺歧異

## 2026 版本方向

v2.1.101（2026-04-11）官方已將 custom commands 與 skills 統一，長期建議新增的 command 改放在 `.claude/skills/<name>/SKILL.md`，同時支援 `/name` 叫喚與 autonomous trigger。現有 `.claude/commands/` 舊格式仍相容。

## 套用範例

本 repo `obsidian-memory` 的現況：

- `/ob`（短捷徑）→ 委派 obsidian agent
- `/vault`（短捷徑）→ 委派 vault-query agent
- `/vault-check` → 稽核迴圈
- `vault-topic-moc`（skill）→ MOC 整合
- `vault-youtube-sync`（skill）→ YouTube 頻道同步

全部符合規則。新增時延用 `vault-<動作>` 家族前綴即可（例：`vault-export`、`vault-stats`）。
