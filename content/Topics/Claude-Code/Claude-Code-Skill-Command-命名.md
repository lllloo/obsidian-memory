---
title: Claude Code Skill/Command 命名
created: 2026-04-20
updated: 2026-04-25
source: https://code.claude.com/docs/en/skills
tags:
  - claude-code
  - naming-convention
  - skill
  - slash-command
---

聚焦 skill 與 command 的**名稱**：`name` 欄位、資料夾名，以及你在 `/` 選單裡看到的呼叫名。

## 命名格式

`<家族前綴>-<動作>`，全小寫 kebab-case。

## 硬性規則（官方規範）

`name` 欄位與資料夾名：

- 只能用小寫字母、數字、連字號（`a-z`、`0-9`、`-`）
- 最長 64 個字元
- 不能含 XML 標籤
- **保留字禁用**：`anthropic`、`claude`
- `name` 省略時會 fallback 到資料夾名，因此兩者最好一致
- 在本地 skill 裡，`name` 通常就是 `/skill-name` 的呼叫名；若來自 plugin / marketplace，實際顯示可能帶 namespace

`SKILL.md` 檔名本身：大小寫敏感，必須全大寫（不是 `skill.md`、不是 `README.md`）。

## 命名慣例（軟性建議）

1. **同家族共用前綴**：相關 command / skill 用共同前綴分組，例：`deploy-staging`、`deploy-production`；或 `vault-check`、`vault-sync`、`vault-topic-moc`
2. **極短捷徑可例外**：單一入口且高頻使用的保留純名，如 `ob`
3. **官方偏好動名詞（gerund）**：例如 `processing-pdfs`、`analyzing-spreadsheets`、`writing-documentation`
4. **避免籠統命名**：`helper`、`utils`、`tools`、`documents`、`data`、`files` 這類資訊量太低的名字

## 為什麼用 kebab-case

- 官方 `name` 規格本來就只接受小寫字母 / 數字 / 連字號
- 與 plugin / marketplace 常見的 namespace 形式相容
- 比底線或 camelCase 更穩定，也比較不會和 shell / 路徑慣例打架