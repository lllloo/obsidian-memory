---
title: Claude Designer：並行 UI 迭代終極工作流
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-06-26
source: https://www.youtube.com/watch?v=YJ3Z9XhlF5w
---

## 核心概念

將 Claude Code 客製化為「Claude Designer」，利用四個核心功能實現 10 倍速 UI 迭代：

1. **Sub-agents**：並行產生多個 UI 變體
2. **CLAUDE.md**：設定 UI 設計模式規則
3. **Custom Commands**：封裝 UI 迭代流程
4. **Git Worktree**：在真實 Next.js 專案中並行迭代

## Sub-Agents 並行 UI 生成

```
Start three parallel agents to implement variations of the to-do app UI:
one minimalist, one modern, one kanban style
```

- 三個 sub-agent 同時運作，各自產出不同風格的 HTML 檔案
- 適合 UI 設計，因為各變體相互獨立，無 merge conflict 問題

## CLAUDE.md 設定

UI 模式規則範例：
- 指定色彩、字型、版面規範
- 規則：「建立 UI 時，一律輸出到單一 HTML 檔案」

## Custom Commands 設計

### `/extract-design-system`

輸入：UI 截圖 URL
輸出：`prd/design-system.json`（色彩、字型、陰影等）

### `/iterate-design`

輸入：設計參考 + 描述
動作：啟動 3~5 個 sub-agent，各自用不同風格實作同一 UI
輸出：`ui-iterations/ui1.html`、`ui2.html`、`ui3.html`...

## Git Worktree 並行迭代（真實專案）

```bash
# 建立 worktree
git worktree add -b demo-branch trees/demo-branch

# 在 worktree 中安裝並啟動
cd trees/demo-branch && pnpm install && pnpm dev
```

### `/execute-parallel-agents` Command

1. 依要求建立多個 worktree（命名規則：`trees/<branch-name>`）
2. 在每個 worktree 執行 `pnpm install`
3. 啟動對應數量的 sub-agent，各自在獨立 branch 迭代 UI
4. 完成後挑選喜歡的版本合併：`git merge <branch>`

注意：完成後記得清除不用的 worktree，每個都包含完整 node_modules。

## 完整 UI 設計流程

1. 從 Dribbble/Mobbin 找靈感截圖
2. `/extract-design-system <image-url>` → 取得 design-system.json
3. `/iterate-design` → 產出多個 HTML 變體
4. 選出喜歡的版本，繼續迭代（暗色版、細節調整等）
5. 確定設計後，複製 HTML 到 cursor/Claude Code 拆解為 Next.js components

## SuperDesign Extension

作者與 Jack 開發的開源 cursor extension（superdesign.dev）：
- IDE 內建 canvas，並排預覽多個 UI 變體
- 點擊變體後可選擇：生成更多變化、提供反饋迭代、複製 prompt 到 cursor
- 使用 Claude API SDK，需設定 Anthropic API key
- 未來版本將支援直接整合 Git worktree
