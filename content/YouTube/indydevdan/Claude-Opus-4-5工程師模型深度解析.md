---
title: Claude Opus 4.5：工程師的最強模型
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-16
published: 2025-12-01
source: https://www.youtube.com/watch?v=3kgx0YxCriM
parent: "[[01.index]]"
---

## 核心定位

Opus 4.5 = 工程師的模型。Anthropic 明確針對兩項能力訓練：
1. **Enhanced Agent Delegation**：更好地撰寫給 sub agents 的 prompts
2. **Longer, Harder Tasks**：更長時間運行更複雜任務的能力

> Anthropic blog：「Opus 4.5 is also very effective at managing a team of sub agents, enabling the construction of well-coordinated multi-agent systems.」

## 定價改善

| 版本 | Input | Output |
|------|-------|--------|
| Opus 4.1 | $15/M | $75/M |
| Opus 4.5 | ~$5/M | $25/M |

降至約 1/3（降幅約 67%），同時 Open Router 測量速度約 60 tokens/秒。

## 能力 1：Enhanced Agent Delegation

Sub agent 架構澄清（常見誤解）：
```
你 → prompt → Primary Agent → prompt → Sub Agents
                    ↑                        ↓
              你收到回應        Sub agents 回應給 Primary Agent
```

Opus 4.5 訓練重點：讓 Primary Agent 能寫更好的 sub agent prompts（即 `task` tool 的呼叫）。

實驗：一個 Opus 4.5 實例 → 啟動 5 個 Opus 4.5 sub agents，各自在瀏覽器中操作，結果：
- 截圖每張圖片並命名
- 從 PDF 提取文字並搜尋關鍵字
- 彙總模型定價資訊

## 能力 2：Browser Automation at Scale

工作流程（AI Developer Workflow）：

```
Plan → Build → Host → Browser Test
              ↓ (if errors found)
           Fix/Debug → re-test
```

- 使用 E2B 作為 agent sandbox 主機
- 每個 sandbox = 完整的 dev 環境
- Opus 4.5 能 oneshot 建立全端應用（Voice Notes、圖表、任務追蹤等）

## 模型堆疊建議

```
Haiku    →  速度快、最便宜（簡單任務）
Sonnet   →  Workhorse（中等任務）
Opus 4.5 →  強力 + 快速（複雜、長時間、multi-agent 任務）
```

Opus 4.5 現在「同時是 workhorse 和強力模型」。

## 工程師心態升級

過去（2-3 年前）：「Prompt 是知識工作的基本單位，掌握 prompt = 掌握知識工作」

現在：**Agent = 新的組合單位（Compositional Unit）**

學習路徑：
1. 學會操作單一 agent
2. 學會操作更好的 agent（prompt + context engineering）
3. 學會操作更多 agents（sub agents、parallel）
4. 建 custom agents（嵌入應用程式）
5. 掌握 orchestration level（管理 agent teams）

> 核心轉變：不再問「我能做什麼？」，而是問「我能教 agents 做什麼？」

## 應用：Agent Sandbox 工作流程

```bash
# Fork terminal 並傳入 agent sandbox skill
fork terminal claude-code opus --summary
# Skill: list sandboxes → open all URLs in Chrome
# 5 個 sandboxes 並行運行不同 full-stack apps
```

每個 sandbox 獨立環境，即使一個 agent 掛了不影響其他的。
