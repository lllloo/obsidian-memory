---
title: Agent 記憶體管理 — Git Context Controller
tags:
  - youtube
  - ai-agent
  - claude-code
  - memory
created: 2026-04-14
updated: 2026-04-14
published: 2026-02-18
source: https://www.youtube.com/watch?v=pAIF7vZm5k0
parent: "[[01.index]]"
---

## 問題：Context Window 限制

Coding agent 有效 context window 約 120-200k token，導致：
- 長時間任務中 agent 「越來越笨」
- 重複犯同樣錯誤，忘記之前嘗試過的方法
- Claude Code 的 MEMORY.md 只對單一 session 有效，多 agent 間無法共享

## Git Context Controller 方法

由 one-context 專案實作，讓 agent 像用 git 管理代碼一樣管理記憶體。

### 檔案結構

```
project/
  main.md          # 全域 roadmap 與專案脈絡
  branches/
    <approach>/
      commit.md    # 里程碑摘要（類似 git commit log）
      log.md       # 完整對話歷史（observation/sort/actions）
      metadata.md  # 高層次元資料，方便搜尋
```

### 四個操作

- **branch**：決定探索新方向時建立，如 `playwright`、`api` 等
- **commit**：完成子任務或里程碑時更新 commit.md
- **merge**：探索完成後，將 branch 記憶合併回 main.md
- （隱含）**search**：Agent 根據查詢搜尋特定 session 或 turn

### 效果

- Claude Code 軟工任務表現提升 13-14%
- 讓較小型模型（如 Gemini 4.5）達到 frontier model 等級
- 跨 session、跨 agent 共享記憶

## one-context 工具實際使用

安裝：`npm i -g one-context-ai`

啟動：`one-context`（會開啟左右分割介面）

工作流：
1. 建立 context（可視為一個專案記憶群組）
2. 加入 session（選 Claude Code 或 Codex + workspace）
3. Agent 工作時，stop hook 自動將對話儲存到本地 DB 並生成摘要
4. 新 session 可搜尋舊有記憶，跨資料夾、跨 agent 均可存取

## 與 Claude Code 自有記憶的差異

| | Claude Code MEMORY.md | Git Context Controller |
|--|--|--|
| 跨 session | 有限 | 是 |
| 跨 agent | 否 | 是 |
| 可分享 | 否 | 可產生分享 URL |
| 複雜度 | 單一檔案易膨脹 | 分層結構 |
