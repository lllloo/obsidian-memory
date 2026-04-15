---
title: Claude Skills — 比 MCP 更強大的 Agent SOP
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-10-17
source: https://www.youtube.com/watch?v=1WImBwiA7RA
---

## 什麼是 Claude Skills

- Claude Code 新功能，概念上是「教 agent 如何完成某項任務的 SOP」
- 由 prompt 指令 + 可選的資源檔（模板、預定義函式）組成
- 最簡單的形式：一個 `skill.md` 檔案，包含觸發說明和執行指令

## Skill 結構

```
.claude/skills/<skill-name>/
  skill.md          # 必要：描述 + 執行指令
  resources/        # 可選：參考範例、模板
  functions/        # 可選：預定義函式（Python、JS 等）
```

- `skill.md` 開頭的 description 會常駐在 agent context，讓 agent 知道有哪些 skill 可用
- 正文（執行細節）在 agent 決定呼叫該 skill 時才載入
- 架構上沿用 Claude Code command 的基礎設施

## 為什麼可能比 MCP 更好

| 比較項目 | MCP | Skill |
|----------|-----|-------|
| Token 消耗 | 高（工具描述常駐） | 低（只有 description 常駐） |
| 使用難度 | 需要額外設定使用順序 | 開箱即用 |
| 範例：Shadcn MCP | ~4,200 tokens | ~70 tokens |

## 實際範例

### Slack GIF 創作器
- 包含 description + 完整 GIF 生成說明 + 預定義 Python 函式
- 執行時動態生成並運行 Python code

### Algorithm Art Skill
- 包含模板範例，agent 先讀範例再生成，確保風格一致
- 使用 p5.js 生成互動式動畫藝術

## 為自己的 Codebase 建立 Skill

1. 載入 `skill-creator` skill
2. 提示 agent 調查 codebase 慣例（如「前端加新 UI component 的最佳做法」）
3. 讓 agent 建立 `frontend` skill，包含慣例文件與 component guide
4. 之後新增 UI 時，agent 會自動先呼叫此 skill 確保符合既有規範

## 資源

- [awesome-claude-skills](https://github.com/) — 作者維護的 skill 集合，包含 UI design 等實用 skill
