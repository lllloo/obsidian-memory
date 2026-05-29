---
title: Claude Code Skill/Command 命名
created: 2026-04-20
updated: 2026-05-29
source: https://code.claude.com/docs/en/skills
tags:
  - claude-code
  - naming-convention
  - skill
  - slash-command
---

skill / command 命名一律 kebab-case：`<家族前綴>-<動作>`，全小寫。先分清兩個「名字」：**呼叫名**（`/` 後輸入的字）來自**資料夾名**（skills）或**檔名**（`.claude/commands/`），不是 frontmatter；frontmatter `name` 只是 skill 清單的**顯示標籤**（預設沿用資料夾名），唯 plugin-root `SKILL.md` 例外才由 `name` 決定呼叫名。kebab-case、保留字（不可用 `anthropic` / `claude`）、64 字元上限等硬性規則是針對 frontmatter `name` 定義，但資料夾 / 檔名沿用同套慣例最省事。`SKILL.md` 全大寫等其餘規則以官方 docs 為準。

## 命名慣例

- **同家族共用前綴**：相關 skill / command 用共同前綴分組——`deploy-staging` / `deploy-production`，或 `vault-check` / `vault-sync` / `vault-topic-index`；在 `/` 選單看起來自動成一組
- **極短捷徑可例外**：單一入口、高頻使用的保留純名（如 `ob`）；前綴是為了分組，沒得分組就不勉強
- **官方偏好動名詞（gerund）**：`processing-pdfs` / `analyzing-spreadsheets` / `writing-documentation`——具體動作勝過名詞
- **避免籠統**：`helper` / `utils` / `tools` / `documents` / `data` / `files` 這類資訊量太低的名字一律不取

## 為什麼是 kebab-case 不是別的

- 官方 `name` 規格本來就只接受小寫字母 / 數字 / 連字號
- 與 plugin / marketplace 常見的 namespace 形式相容（`plugin:skill-name`）
- 比底線或 camelCase 更穩定，也比較不會跟 shell / 路徑慣例打架
