---
title: Claude Code 加 Codex 等於 AI 之神
tags:
  - youtube
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-30
source: https://www.youtube.com/watch?v=L7NPhaUBpZE
---

## 背景與動機

OpenAI 開放 Codex 可整合至 Claude Code，讓用戶在 Anthropic 生態系內同時使用兩個競爭對手的模型。主要誘因：

- Codex 的 token 費用比 Opus 4.6 划算得多，對頻繁使用者是重要選項
- 可在 Claude Code 的 usage 限制內補位（Codex 使用的是 ChatGPT 帳戶額度，即使免費方案也適用）

## 安裝步驟

```bash
# 1. 將 Codex 加入 marketplace
# （指令見 GitHub repo，作者在描述附連結）

# 2. 安裝 plugin（user scope）
/plugin install codex@openai

# 3. 重新載入 plugins
reload plugins

# 4. 設定
codex:setup
```

安裝後需以 ChatGPT 帳號登入，完成瀏覽器驗證流程。

## 主要功能

### 1. Codex Rescue（讓 Codex 單獨執行任務）

```
codex:rescue <prompt> [--effort <level>] [flags...]
```

適用場景：Claude Code 達到 Anthropic usage 上限時，以 Opus 規劃、Codex 執行。

### 2. Standard Code Review（中立審查）

唯讀模式，Codex 掃描整個 codebase 給出觀察，不帶批判立場。

### 3. Adversarial Review（對抗式審查）

假定程式碼有問題，以挑剔眼光掃描，專注以下 7 個攻擊面：

1. Authentication（驗證）
2. Data loss（資料遺失）
3. Rollbacks（回滾）
4. Race conditions（競態條件）
5. Degraded dependencies（依賴退化）
6. Version skew（版本偏差）
7. Observability gaps（可觀測性缺口）

輸出格式為結構化 JSON，每個問題包含 severity（critical/high/medium/low）、影響範圍、相關檔案與行號、fix 建議。

## Opus vs Codex 對抗式審查比較

作者對同一個 Twitter engagement bot 同時跑兩者，結果：

| | Opus | Codex |
|---|---|---|
| 共同發現 | Telegram polling 問題（Opus 評 critical，Codex 評 high）| 同上 |
| 獨家發現 | 額外 7 個 high/critical 問題 | 額外 3 個問題 |

結論：Opus 找更多，Codex 找得精準；核心價值是**第二雙眼睛**，避免讓同一個 AI 既生成又評估自己的程式碼。

## 使用時機判斷

- 已在付 ChatGPT $20/月 → 幾乎零成本加入
- Claude Code Pro 方案頻繁撞 usage 限制 → Codex 作為 fallback
- 複雜專案需要不同角度的 code review → adversarial review 最有價值
- Adversarial prompt 越具體效果越好（可指定特定安全領域、架構問題等）
