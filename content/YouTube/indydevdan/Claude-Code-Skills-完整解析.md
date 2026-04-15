---
title: 終於搞懂 Claude Agent Skills：工程師完整解析
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-10-27
source: https://www.youtube.com/watch?v=kFpLzCVLA20
---

## 四大 Claude Code 能力比較

| 能力 | 觸發方式 | Context 效率 | Context 持久性 | 最適合 |
|------|---------|-------------|----------------|--------|
| **Skills** | Agent 自動觸發 | 高（Progressive Disclosure） | ✓ | 重複性解決方案 |
| **MCP Servers** | Agent 自動調用 | 低（啟動即消耗大量 token） | ✓ | 外部服務整合 |
| **Sub-agents** | Agent / 手動 | 高（獨立 context） | ✗（結束後消失） | 並行任務、隔離工作 |
| **Custom Slash Commands** | 手動觸發 | 中 | ✓ | 一次性任務、最基本單元 |

另外：
- **Hooks**：確定性自動化，在生命週期事件執行命令（非 LLM 決策）
- **Plugins**：打包發佈 Claude Code 擴展
- **Output Styles**：自定義輸出格式（如 text-to-speech 摘要）

## 何時用哪個

**Skills 用於**：需要 agent **自動應用**的重複工作流程，且需要打包成可重用的解決方案
- 例：PDF 文字擷取、style guide 違規偵測、管理 Git work trees

**MCP 用於**：連接外部工具與資料來源
- 例：Jira、資料庫查詢、即時天氣 API

**Sub-agents 用於**：需要**並行執行**或**隔離 context** 的任務（允許事後 context 消失）
- 例：修復所有 failing tests、全面安全審計
- 關鍵字：「parallel」→ 自動聯想 sub-agent

**Slash Commands 用於**：一次性任務、手動觸發的簡單工作
- 例：建立 Git commit message、建立 UI component

## 最重要的原則：Prompt 是根本

**Composition 層次（由低至高）：**
```
Prompt (Slash Command) → Sub-agent → MCP Server → Skill
```

- Skill 是最高層的組合單元，可以包含 Slash Commands、Sub-agents、MCP Servers
- Slash Command 是最基本的 primitive，也可以組合所有其他元素
- 一切最終都是 `context + model + prompt + tools`

**建議順序**：
1. 先建 Slash Command（prompt）
2. 需要並行時 → Sub-agent
3. 需要外部服務 → MCP Server
4. 需要管理多個相關 prompt/功能成為一個領域解決方案時 → Skill

## Skills 的正確理解

**錯誤用法**：用 Skill 做一次性任務（這是 Sub-agent 或 Slash Command 的工作）

**正確用法**：當一個問題需要多個相關工作（不只是「建立 work tree」，而是「管理整個 work tree 生命週期」）

**Skill 的真正價值**：
- 將 domain-specific 專業知識封裝成 agent 可自動調用的模組
- 以目錄結構組織資源，agent 按需載入（Progressive Disclosure）
- 可重用、可分享、可版本控制

**結構**：
```
.claude/skills/<skill-name>/
  skill.md          # 技能定義與觸發條件
  script1.py        # 獨立腳本
  script2.py
  README.md
```

## Skills 的優缺點

**優點：**
- Agent 自動調用（提升自主性）
- Context 保護（Progressive Disclosure，不像 MCP 一次性消耗）
- 獨立的檔案系統結構，易於組織與分發
- 可組合其他功能（MCP、Sub-agents、Slash Commands）

**缺點：**
- 無法在 skill 目錄內嵌入專屬 Slash Commands 目錄（沒有完整去到底）
- 可靠性尚待驗證（連鎖多個 skill 時是否穩定？）
- 本質上是「有意見的 prompt engineering + 模組化」，技術上沒有太多創新

整體評價：8/10。不替代任何現有功能，而是在更高層次的組合單元。
