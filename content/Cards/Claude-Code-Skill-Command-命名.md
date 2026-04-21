---
title: Claude Code Skill/Command 命名
created: 2026-04-20
updated: 2026-04-21
source: https://code.claude.com/docs/en/skills
tags:
  - claude-code
  - naming-convention
  - skill
  - slash-command
---

聚焦 skill 與 command 的**名稱**（`name` 欄位、資料夾名、`/slash-command` 叫喚名）。description、優先順序、版本差異不在本頁。

## 命名格式

`<家族前綴>-<動作>`，全小寫 kebab-case。

## 硬性規則（官方規範）

`name` 欄位與資料夾名：

- 只能用小寫字母、數字、連字號（`a-z`、`0-9`、`-`）
- 最長 64 個字元
- 不能含 XML 標籤
- **保留字禁用**：`anthropic`、`claude`
- `name` 省略時 fallback 到資料夾名，兩者需一致
- `name` 即 `/slash-command` 叫喚名，全域唯一

`SKILL.md` 檔名本身：大小寫敏感，必須全大寫（不是 `skill.md`、不是 `README.md`）。

## 命名慣例（軟性建議）

1. **同家族共用前綴**：相關 command / skill 用共同前綴分組，例：`deploy-staging`、`deploy-production`；或以 vault 為家族的 `vault-check`、`vault-sync`、`vault-topic-moc`
2. **極短捷徑可例外**：單一入口且高頻使用的保留純名，如 `ob`、`review`
3. **官方建議用動名詞（gerund form）**：動詞 + `-ing`，例 `processing-pdfs`、`analyzing-spreadsheets`、`writing-documentation`。名詞短語（`pdf-processing`）或動詞開頭（`process-pdfs`）也可接受
4. **避免籠統命名**：`helper`、`utils`、`tools`、`documents`、`data`、`files` 這類不具描述性的名字

## 為什麼用 kebab-case

- 官方 skills 文件明定 `name` 與資料夾名**只能**用小寫字母、數字、連字號
- Plugin 使用 `plugin-name:skill-name` namespace，與 kebab-case 一致
- 避免底線、camelCase 的視覺歧異
