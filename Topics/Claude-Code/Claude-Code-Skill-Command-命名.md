---
title: Claude Code Skill/Command 命名
created: 2026-04-20
updated: 2026-05-08
source: https://code.claude.com/docs/en/skills
tags:
  - claude-code
  - naming-convention
  - skill
  - slash-command
---

skill 與 command 的呼叫名（`name` 欄位 / 資料夾名 / `/` 選單顯示）一律 kebab-case：`<家族前綴>-<動作>`，全小寫。硬性規則（保留字、字元限制、長度、`SKILL.md` 全大寫）以官方 docs 為準。

## 命名慣例

- **同家族共用前綴**：相關 skill / command 用共同前綴分組——`deploy-staging` / `deploy-production`，或 `vault-check` / `vault-sync` / `vault-topic-moc`；在 `/` 選單看起來自動成一組
- **極短捷徑可例外**：單一入口、高頻使用的保留純名（如 `ob`）；前綴是為了分組，沒得分組就不勉強
- **官方偏好動名詞（gerund）**：`processing-pdfs` / `analyzing-spreadsheets` / `writing-documentation`——具體動作勝過名詞
- **避免籠統**：`helper` / `utils` / `tools` / `documents` / `data` / `files` 這類資訊量太低的名字一律不取

## 為什麼是 kebab-case 不是別的

- 官方 `name` 規格本來就只接受小寫字母 / 數字 / 連字號
- 與 plugin / marketplace 常見的 namespace 形式相容（`plugin:skill-name`）
- 比底線或 camelCase 更穩定，也比較不會跟 shell / 路徑慣例打架
