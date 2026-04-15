---
title: Git Worktree 完整說明與使用方式
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-19
source: https://www.youtube.com/watch?v=JVM40liIElk
---

## 什麼是 Git Worktree

- Git Worktree 是 2026 年最重要的概念之一，在使用多個 AI Agent 時尤其關鍵。
- 核心概念：**同一個 Git 歷史，多個獨立工作目錄**——就像在兩個分頁開啟同一份 Google Doc，但各自可以獨立編輯。
- 解決了傳統工作流的問題：處理功能開發時突然來了緊急 bug，原本需要 stash → 切換分支 → 修 bug → 切回 → pop stash，而 Worktree 讓兩件事完全並行。

## 為什麼現在爆紅

- Git Worktree 在 2015 年就已存在，但過去 10 年一直是小眾功能。
- 2026 年因 AI Agent 的普及而爆炸性成長——Google Trends 顯示近期搜尋量暴增至過去的數倍。
- 沒有 Worktree，多個 AI Agent 同時修改相同檔案時會產生衝突與上下文汙染。

## AI Agent 需要 Worktree 的原因

- **真正的平行執行**：Agent A 做功能開發，Agent B 修 bug，各自在獨立目錄中運作，互不干擾。
- **消除上下文汙染**：若你在 Agent 工作時切換分支，Agent 的 context 會讀到不一致的狀態。
- 掌握 Worktree 的人才是真正的「多 Agent 指揮家」，其他人只是 vibe coder。

## 方法一：透過 Claude Desktop App（適合初學者）

- Claude Desktop App 會自動為每個工作階段分配 Worktree，不需要手動操作。
- 確保兩個工作階段都選同一個專案資料夾即可，各自會有獨立 Worktree。
- 操作步驟：
  1. 開啟 Claude Desktop，切換到「Code」模式
  2. 點擊「New Session」並選擇專案資料夾
  3. 再開一個 New Session，選同一個資料夾
  4. 兩個 Claude Code 實例會自動運行在不同 Worktree 上

## 方法二：在終端機手動使用（進階）

### 常用指令

```bash
git worktree list                    # 列出所有 worktree
git worktree add <路徑> <分支>        # 建立新 worktree
git merge feature/authentication     # 合併 worktree 的分支
```

### 終端機技巧

- `tab` 自動補全路徑，節省輸入時間（如輸入 `cd doc<tab>` 直接補全 documents）
- `ls` 列出目錄，`clear` 清空終端機輸出
- 啟動 Claude Code 不需授權確認：`claude --dangerously-skip-permissions`

### 建議模型設定

- 執行 `/model` 選擇 **Opus 4.6 + 1M context**
- 開啟 **/fast 模式**（需使用 API key，非訂閱制；成本更高，但速度與品質的飛躍值得）
- Opus 在長 context 下的表現遠比 Gemini 3.1 Pro 和 GPT-5.4 穩定

## 實際開發示範：Git 學習 App

### 流程

1. 初始化 Git repo，建立基本 Express App（`/users` endpoint）
2. 使用第二個 Claude Code 建立兩個 Worktree：
   - `feature/authentication`
   - `feature/frontend-design`
3. Agent 一（認證）：在 authentication Worktree 中建立 JWT 認證後端
4. Agent 二（前端）：在 frontend-design Worktree 中建立互動式 Git 學習單頁 App
5. Agent 三（審查者）：在 root 目錄啟動，同時讀取兩個 Worktree 的程式碼並進行審查
6. 發現衝突後，讓 Claude Code 自動處理 merge conflict
7. 合併兩個分支，重啟伺服器

### 成果

- 最終 App：互動式 Git 指令學習工具，包含翻卡效果、指令說明、使用統計（顯示 Git worktree 只有 18% 的開發者在用）
- 由三個 Claude Code Agent 共同完成，兩個各自在獨立 Worktree 開發，第三個負責整合

## 結語

- Git Worktree 目前只有 18% 的開發者在使用——看完這支影片就超越了絕大多數人。
- 越是複雜的大型專案，Worktree 的優勢越明顯；簡單小專案用單一 Claude Code 就夠了。
- 這個趨勢只會繼續增長，現在是學習的最好時機。
