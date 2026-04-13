---
title: Pi CEO Agents、Claude 1M Context 與多 Agent 決策團隊
tags:
  - youtube
  - claude-code
  - multi-agent
  - agent-harness
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-23
source: https://www.youtube.com/watch?v=TqjmTZRL31E
---

## 三大創新

### 1. Claude 1M 真實 Context Window

- Anthropic 以固定單一價格提供 100 萬 token context，**沒有長 context 加價**
- 競爭對手（Gemini、Llama 4）的 1M context 在 250K 後品質急劇下降
- Claude Opus 4.6 / Sonnet 4.6 在 250K 後仍能保持關鍵資訊
- 影響：Core 4 的 Context 得到大幅強化

### 2. 可客製化 Agent Harness（Pi）

- 一般工具只有固定架構（agents、skills、commands）
- Pi 讓你完全自訂資料夾結構、檔案、前置 frontmatter
- 可建立獨特的 micro-application，而不只是通用的 coding agents
- 口號：「There are many coding agents, but this one is mine」

### 3. Agent Expertise（累積記憶）

- 每個 agent 有自己的 expertise 檔案（scratch pad / mental model）
- 不是泛用記憶，而是**針對特定 domain 的知識與模式**
- 得益於 1M context，expertise 可以達到數萬 tokens 仍不影響成本

## CEO 與 Board 多 Agent 決策系統

### 架構

```
Brief（問題輸入）
  → CEO Agent（Opus，控制整個流程）
      → Board Members（並行辯論）
          - Revenue Agent（90 天內能賺多少？）
          - Technical Architect（技術風險與機會）
          - Compounder（長期複利優勢）
          - Product Strategist（產品路線）
          - Contrarian（反對意見）
          - Moonshot（10x 大賭注）
  → Memo（決策輸出，含 SVG + MP3 語音摘要）
```

### 設定檔結構

```yaml
# config.yaml
meeting:
  max_duration: 5      # 分鐘
  max_budget: 5.00     # 美元

brief:
  required_sections:
    - key_questions
    - stakes
    - constraints

paths:
  briefs: ceo-agents/briefs/
  debates: ceo-agents/debates/
  memos: ceo-agents/memos/
  agents: ceo-agents/agents/

board:
  - revenue
  - technical_architect
  - compounder
  - product_strategist
  - contrarian
  - moonshot
```

### Brief 模板格式

```markdown
## Situation
[具體情境描述]

## Stakes
[風險與機會]

## Constraints
[限制條件]

## Key Questions
[需要回答的核心問題]
```

Brief 不符合格式時系統自動拒絕，強制良好的 prompt engineering。

## 工作流程

1. `j ceo` → 啟動 CEO and Board 系統（Pi extension）
2. `ceo begin` → 系統掃描 briefs 目錄，選擇一個 brief
3. CEO 框架問題 → 所有 board members 並行回應
4. CEO 迭代辯論（在時間/預算約束內反覆進行）
5. 時間到 → CEO 要求每位成員給出最終立場
6. CEO 生成 Memo（含決策圖、投票結果、張力分析、下一步行動）
7. 自動以 11 Labs 生成語音摘要

示範決策結果（Blend Stack 收購案）：
- 5:1 票數建議接受 $12M 收購（11x ARR）
- 條件：$1.5-2M 留任 earnout、90 天知識轉移
- Moonshot 持異議：認為 blend engine 是平台基礎設施，價值遠不止於此

## CEO Agent 系統提示架構

```yaml
# CEO agent frontmatter
name: CEO
model: claude-opus-4-6
expertise: ceo-agents/expertise/ceo.md
skills:
  - mental_model
  - active_listener
  - 11labs_summary
tools:
  - converse    # 向 board 廣播
  - read
  - write
```

系統提示結構（Pi frontmatter 解析後注入）：
- Purpose / Variables / Instructions / Workflow / Context / Report
- 動態注入：session 目錄、對話記錄 path、teams 清單、expertise、skills

## 各 Board Member 設計重點

每位成員有獨特的「氣質」與「推理模式」：

- **Revenue Agent**：只關注 90 天內的收入，傾向保守立場
- **Moonshot Agent**：「What if we're thinking too small?」主張 10x 大賭
- **Compounder**：尋找長期複利優勢，與 Revenue Agent 常對立
- **Contrarian**：專門找漏洞，反駁主流意見

## 中間狀態可觀察性

```
debates/<session_id>/
  conversation.jsonl   # 所有發言記錄（from/to 結構）
  tool_use.jsonl       # 每個 agent 的工具呼叫
  expertise/           # 各 board member 的 scratch pad
    revenue.md
    moonshot.md
  svgs/                # 各成員產生的視覺化論述
```

## 成本參考

- 標準 5 分鐘 / $5 約束的 session：實際花費約 $2.50
- 重大決策建議：提高 budget 限制，優先取得最佳智識輸出

## 應用場景

高 leverage 決策：
- 收購 / 融資決策
- 產品路線選擇
- 行銷平台優先順序
- 技術架構轉型
- 重大人事或合作決策

核心哲學：**不要在沒有諮詢 agent 團隊的情況下做任何重大決策**，因為這個智識量能已經唾手可得。
