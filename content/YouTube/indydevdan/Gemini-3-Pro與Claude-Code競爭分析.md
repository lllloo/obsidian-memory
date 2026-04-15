---
title: 給 Gemini 3 Pro 自己的電腦：Claude Code 終於有對手了
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 
source: https://www.youtube.com/watch?v=V5IhsHEHXOg
---

## 三個發布的信號評估

| 發布 | 評分 | 說明 |
|------|------|------|
| Gemini 3 Pro | 高信號 | 新的最強模型，幾乎拿下所有 benchmark |
| Google Anti-Gravity | 低信號 | VS Code fork，類似 Cursor 但較粗糙，launch 感覺倉促 |
| Nano Banana Pro（圖片生成） | 高能力 | 最強圖片生成工具 |

## 核心示範：給 Agents 自己的電腦

使用 E2B 作為 agent sandbox 服務，讓每個 agent 在獨立環境中執行。

**同時運行 15 個 agent sandboxes：**
- 5 個 Gemini 3 Pro agents
- 5 個 Claude Code (Sonnet 4.5) agents
- 5 個 Codex CLI agents

每個 agent 各自在 sandbox 中：Plan → Build → Host → Test

## Agent Skill 重新程式化（Reprogramming）

關鍵技術：用 CLAUDE.md 記憶檔讓 agent 識別自訂語法。

```markdown
# CLAUDE.md 設定
Anytime the engineer starts a command with backslash (\),
look for the file and execute the command.
Look for: standard prompts, nested prompts, agent sandbox prompts.
```

- `\sandbox` → 執行 agent sandbox skill
- `\agent sandboxes: plan build host test` → 觸發完整工作流程

**任何 agent 都可以學習使用 skills（Gemini CLI、Codex CLI 都能用 Claude skills）**。

## Agent Sandbox Skill 工作流程（170 行 prompt）

```
1. Read agent sandbox documentation
2. Plan the application
3. Build in sandbox environment
4. Host the application
5. Browser test
6. Report results (or loop back to fix)
```

## 全端應用建置結果

| 任務 | Gemini 3 Pro | Claude Sonnet 4.5 | Codex |
|------|-------------|-------------------|-------|
| SQL CRUD 介面 | 完成 | 完成（無錯誤） | 部分完成 |
| Pelican SVG | 完成（更精緻） | 完成 | 完成（問題較多） |
| Pokemon Card SVGs | 完成（有 2 張成功） | 完成 | 部分 |
| 筆記應用 | 完成 | 完成 | 未完成 |

注意：`best-of-N` 策略 —— 預期有些 sandbox 會失敗，從成功的中選最好的。

## 核心論點：模型愈來愈不重要

> 「每一次新發布，模型都越來越不重要。」

瓶頸已從「模型智能」轉移到：
- 你能建造什麼樣的 agentic 系統？
- 你能讓 agents 持續運行多久？
- 你能建立多好的 agent sandbox 環境？

**最重要的 benchmark** = 模型在你的具體使用情境中的表現，而非公開排行榜。

你只用了 Gemini 3 Pro 73 分智能指數中的 50-60 分——上限還很遠。

## 策略建議

1. 用 `best-of-N` + agent sandboxes 大量投放 compute
2. 用 memory files 重新程式化任何 agent 以使用 shared skills
3. 預期部分 agent 失敗，設計時就考慮容錯
4. Scale compute = Scale impact

> 頻道里程碑：100K subscribers。
