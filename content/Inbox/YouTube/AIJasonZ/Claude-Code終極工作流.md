---
title: Claude Code 終極工作流
created: 2026-04-15
updated: 2026-04-15
source: https://www.youtube.com/watch?v=UZb0if-7wGE
published: 2025-07-24
parent: "[[01.index]]"
tags:
  - youtube
---

## 初始設定

- 安裝 Claude Code extension，深度整合 cursor/VS Code/Windsurf
- 執行 `/init`：自動掃描 codebase，產生 `CLAUDE.md`（tech stack、依賴、架構）
- `CLAUDE.md` 加入 plan mode 規則：「實作前先規劃，計畫存入 `.claude/tasks/<name>.md`」

## Spec-Driven Development 流程

1. 撰寫 PRD（需求文件）
2. `Shift+Tab` 進入 plan mode（限制工具存取，專注規劃與 web search）
3. Agent 產生實作計畫並存入 `.claude/tasks/`
4. 確認計畫後，逐 phase 執行
5. Agent 執行時持續更新 task doc，記錄完成項目

### Plan Mode 的運作

- 特殊 system prompt，限制工具只能用 web search 和計畫相關工具
- 呼叫 `task` 工具時會啟動 sub-agent 做研究
- 只有最後的研究摘要回傳給 parent agent（節省 token）

## Hooks 功能

### Stop Hook（任務完成通知）

```json
{
  "stop": ["command to play notification sound"]
}
```

### Post-Tool Hook（TypeScript 型別檢查）

每次 agent 寫入/修改 `.ts` / `.tsx` 檔案後，自動執行型別檢查：
- exit code 2：blocking error，阻止 agent 繼續，強制修復
- 其他 exit code：回饋給 agent 但不阻斷流程

可用來複製 cursor 的「自動 lint error 偵測」功能。

### 其他 Hook 應用場景

- 每次寫程式後自動執行測試
- 寫 API 文件後自動更新文件系統

## Custom Commands

- 在 `.claude/commands/` 建立 MD 檔 → 可用 `/command-name` 觸發
- 內容等同發送 prompt 給 Claude Code

### 推薦套件：super-claude

```bash
uv init && uv add supercloud && uv run python supercloud install
```

內建實用指令：
- `/sc:analyze`：深度 codebase 分析
- `/sc:workflow`：依 PRD 逐步實作
- `/sc:build`：打包並處理錯誤
- `/sc:troubleshoot`：排查難以定位的 bug

## 實用快捷鍵與功能

| 功能 | 操作 |
|------|------|
| 跳回過去對話 | `/resume` |
| 匯出對話歷史 | `/export`（可貼入其他 IDE） |
| 回退到過去節點 | 雙擊 Esc |
| 直接執行 shell | `!` 前綴進入 bash mode |
| 永久記憶 | `#` 前綴進入 memory mode |

### cc-undo 套件

自動記錄 Claude Code 所有檔案變更，支援預覽與回滾。

## 整合 Kimi K2 模型

```bash
# ~/.zshrc
export KIMI_API_KEY="your-key"
alias kimi='ANTHROPIC_BASE_URL=https://api.moonshot.ai/anthropic ANTHROPIC_AUTH_TOKEN=$KIMI_API_KEY claude'
```

- 效能介於 Claude 3.5 和 Claude 4 之間
- 成本降低 80%
