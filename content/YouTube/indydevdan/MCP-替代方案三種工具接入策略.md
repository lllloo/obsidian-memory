---
title: 頂尖工程師拋棄 MCP Server 的原因：3 種替代方案
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-11-10
source: https://www.youtube.com/watch?v=OIKTsVjTVJE
---

## 問題：MCP Server 的 context 消耗

MCP Server 在 agent 啟動前就消耗大量 context。一個中等規模的 MCP Server 耗掉 10,000 tokens（5% context window）；堆疊 2-3 個，20%+ context 在 agent 開始工作前就消失。

三種替代方案共同原則：**用原始程式碼作為工具（use raw code as tools）**。

## 方案一：CLI as Tools

做法：
- 建立一個 CLI 工具（用 click/typer 等框架）包裝所有 agent 需要的功能
- 用一個 ~25 行的 prime prompt 教 agent 如何使用這個 CLI
- Prompt 指定 agent 只讀 readme 和 CLI 檔案，不讀其他 Python 檔

效果：context 消耗比 MCP 少約 50-60%

優點：
- 完全控制 agent 可以使用哪些工具
- CLI 同時服務：你、你的團隊、你的 agent（三贏）
- 按需啟用，不會一直佔用 context

## 方案二：Scripts as Tools（Progressive Disclosure）

做法：
- 每個功能做成**獨立的單一檔案 Python script**（使用 Astral UV，在檔案頭宣告依賴）
- 寫一個 README 列出每個 script 的使用時機
- Prime prompt 只讓 agent 讀 README，不讀 script 本身
- Agent 需要時才用 `--help` 取得 script 詳細用法

關鍵 prompt 技巧：
```
I will not read scripts themselves unless --help doesn't provide information needed.
```

效果：context 降至 MCP 的 10%（從 10K 降到 ~2K tokens）

這就是 Anthropic 說的「Progressive Disclosure」——只在需要時才載入 context。

## 方案三：Skills as Tools

做法與 Scripts 幾乎相同，差別在於：
- 所有 script 打包進一個 skill 目錄（含 `skill.md`）
- 用 `skill.md` 告訴 agent 每個 script 的使用時機
- 自動觸發，不需要手動執行 prime prompt

特點：Progressive Disclosure 自動化，但這是 **Claude 生態系鎖定**（Claude ecosystem lock-in）。

## 各方案比較

| 項目 | MCP | CLI | Scripts | Skills |
|------|-----|-----|---------|--------|
| Agent 自動調用 | ✓ | ✗ | ✗ | ✓ |
| Context 消耗 | 最多 | 中 | 最少 | 最少 |
| 自定義性 | 低（除非自建） | 高 | 高 | 高 |
| 可移植性 | 低 | 中 | 高（單一檔案） | 中（整個目錄） |
| 複雜度 | 低 | 中 | 中 | 中 |
| 工程投入 | 低（外部 MCP） | 中 | 中 | 中 |
| 生態鎖定 | 無 | 無 | 無 | Claude 專屬 |

MCP 額外特性（常被忽略）：Resources、Prompts、Elicitation、Completion、Sampling

## Dan 的個人使用策略

**新工具開發：**
- 80%：先做 CLI，附 prime prompt；一個 ~5 行的極簡 prompt 就夠：`read these files, summarize tools`
- 10%：需要多 agent 規模化時，把 CLI 包成 MCP Server（CLI 的 method 直接呼叫 CLI）
- 10%：需要嚴格保護 context 時，改用 scripts 或 skills

**外部工具（不自己建的）：**
- 80%：直接用外部 MCP Server，不要重造輪子
- 15%：需要修改/擴展時改用 CLI
- 5%：需要 context 保護時改用 scripts/skills

**核心建議**：永遠先建 CLI，因為可以同時服務你、團隊和 agent，且之後可輕鬆包成 MCP Server。

## 關鍵洞見

- Context 問題的根本解：**讓 agent 專注在單一目的**（focused, one-purpose agent），刪掉後重開，這樣根本不需要 context 工程
- Prompt engineering 優先於 context engineering：好的 prompt 可以 prompt engineer 出不需要的 context
- 所有方案本質相同：都是 `context + model + prompt + tools`，差別只在工具的發現方式
