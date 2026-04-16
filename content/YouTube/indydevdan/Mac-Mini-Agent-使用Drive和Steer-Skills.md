---
title: Mac Mini Agents：用 Drive 和 Steer Skills 取代 OpenClaw
tags:
  - youtube
  - claude-code
  - ai-agent
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-09
source: https://www.youtube.com/watch?v=LOazLNQnB80
parent: "[[01.index]]"
---

## OpenClaw 的問題

OpenClaw / nano-claw 等工具的問題：
- 以 vibe coding 方式大量生成有漏洞的代碼
- 無差別安裝 packages，高度危險
- 容易遭受 prompt injection
- 安全性惡夢（Karpathy 也明確指出）

**但這類工具揭示了一個重要事實**：給 agents 更多自主性，它們能完成比你預期更多的事。

## 解決方案：極簡安全的 Mac Mini Agent

只用 **4 個 CLI 工具 + 2 個 Skills** 驅動整個多裝置 agent 應用。

### 整體架構

```
觸發層（Trigger Layer）
  └── listen（HTTP server）
        └── agent 裝置
              ├── drive skill    ← 終端機控制
              ├── steer skill    ← GUI 控制
              ├── drive CLI      ← tmux 包裝
              └── steer CLI      ← macOS Swift 應用
```

## 四個核心工具

| 工具 | 功能 |
|------|------|
| `listen` | HTTP server，等待從任何地方傳入的 job |
| `direct` | 客戶端 CLI，發送任務到 listen server |
| `drive` | tmux 包裝器，讓 agent 開啟/控制多個終端視窗 |
| `steer` | macOS Swift 應用，提供 GUI 控制（Accessibility tree + OCR + 點擊） |

## 兩個關鍵 Skills

### Drive Skill
- 教 agent 如何用 tmux 建立和管理終端視窗
- 在多個視窗並行執行命令
- 讀取命令輸出

### Steer Skill
關鍵使用模式（steer.md 中約 130 行）：
```markdown
## When using steer:
1. Focus on target application first
2. Verify focus before acting
3. Observation loop: screenshot → analyze → act
4. Be aware of multiple monitors (affects XY coordinates)
5. Periodically check elapsed time
```

## YAML Job System

```yaml
# 工作狀態追蹤
job_id: abc123
status: running
command: "Update hooks mastery codebase, commit to new branch, airdrop results"
started_at: 2026-03-09T10:00:00
elapsed: 8min
```

查詢工作狀態：
```bash
j <job_id>    # 查詢 YAML 格式的工作摘要
```

## Justfile 工作流程

```justfile
# justfile 快速指令
send PROMPT URL=DEFAULT_URL:
    direct start --url {{URL}} --prompt {{PROMPT}}

send-to-cc:
    just send "$(cat specs/update_hooks.md)" {{CC_URL}}

listen:
    python apps/listen.py

job JOB_ID:
    python apps/direct.py status --url {{DEFAULT_URL}} --id {{JOB_ID}}
```

啟動 agent：
```bash
j listen          # 啟動 HTTP listen server
j send-to-cc      # 傳送任務給 Mac Mini agent
j <job_id>        # 查詢任務狀態
```

## 實際示範任務

### 任務 1：研究新 MacBook 規格
```
Write your favorite programming language and which OOP pillar is your favorite, save to new file, airdrop it to Indydevdan
```
結果：Agent 完成工作後自動 AirDrop 報告到主機 MacBook

### 任務 2：更新 Cloud Code Hooks Mastery Codebase
```
Specs: update_hooks_mastery.md
Deliverables:
- Updated codebase with all current Claude Code hooks implemented
- AirDropped to Andy Deubdan's MacBook Pro
- Screenshots as visual proof for each hook added
- Text Edit document summarizing changes
- Commit to new branch and push
```
結果：Agent 自主開多個終端視窗，完成工程工作，截圖作為 proof of work，並 AirDrop 所有結果

## 設計理念

**這個裝置只屬於 agent，不是你的**：
- 如果裝置出問題，不要自己去修，教 agent 如何修
- 你的工作是建立「建立系統的系統」，而非直接操作

**Agentic Engineering 的定義**：
> 你對 agents 正在做什麼了解得如此透徹，以至於你不需要盯著看。

（反例：Vibe coding = 不知道也不看）

## 可擴展性

- 同一套架構可部署到多台 Mac Mini、MacBook Air、MacBook Pro
- 只需裝置能存取相同 Git repos
- 加入新裝置：clone library repo，安裝 skills，連接 job server

## 對比 OpenClaw

| 面向 | OpenClaw / Claw agents | Mac Mini Agent（本方案）|
|------|----------------------|------------------------|
| 安裝行為 | 無差別安裝 packages | 僅 agent 指定的工具 |
| 安全性 | 高風險，prompt injection | 受控，已知工具集 |
| 可觀察性 | 難以追蹤 | YAML job system + 截圖 proof |
| 代碼品質 | Vibe-coded slop | 工程設計的系統 |
| 自主性 | 高但危險 | 高且可控 |

## 重要原則

> 增加 agents 的自主性，就是增加你自己的自主性

前提是你知道 agents 在做什麼。2026 的主題：**增加對 agentic 系統的信任**。
