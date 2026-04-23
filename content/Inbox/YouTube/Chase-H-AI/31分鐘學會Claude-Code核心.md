---
title: 31 分鐘學會 Claude Code 核心概念
created: 2026-04-15
updated: 2026-04-15
source: https://www.youtube.com/watch?v=TwkdDcO4vWQ
published: 2026-03-22
parent: "[[01.index]]"
tags:
  - youtube
---

## 安裝與使用方式

搜尋「Claude Code install」進入官方文件，依作業系統執行對應指令即可。

使用方式光譜（從多控制到少控制）：
- **Terminal**：最多控制、完整功能
- **IDE 內建 Terminal**（VS Code、Cursor）：terminal + 側邊檔案管理，視覺上更友善
- **Claude Code 桌面應用**：居中
- **Co-work**：最少控制、最流暢體驗

95% 的使用案例，各方式效果相近。

VS Code 設定：`Ctrl+\`` 開啟 terminal，`cd` 到專案資料夾，執行 `claude` 或 `claude --dangerously-skip-permissions`。

## 權限設定

三種層級（`Shift+Tab` 切換）：

| 層級 | 說明 |
|------|------|
| 預設 | 每次檔案修改都詢問 |
| Accept Edits On | 檔案修改免詢問，shell 指令仍詢問 |
| Bypass Permissions On | 完全不詢問（需先加 `--dangerously-skip-permissions` 啟動） |

Anthropic 資料顯示多數 power user 使用 Bypass 模式。建議初學者從 Accept Edits 開始。

## Prompting 技巧

**Plan Mode 搭配四要素：**

1. **目標導向**：說明「為什麼建這個」，而非只描述「建什麼」
2. **提供範例**：截圖或 GitHub repo 連結比文字描述更有效（截圖可直接拖入）
3. **開放性問題**：問「這個領域的專家會問什麼？」、「我沒想到什麼？」、「有什麼非預期後果？」；Plan Mode 的預設問題偏表層，這些問題逼出更深思考
4. **技術問題不要跳過**：看到不懂的技術選項（Next.js vs Astro vs HTML）不能只按「推薦」，要問到理解為止。不需要會寫程式，但需要理解軟體工程基本概念，否則遇到複雜專案會撞牆

## 技能（Skills）

技能 = 文字 prompt，告訴 Claude Code 如何以特定方式完成特定事情。兩種類型：

- **改善型**：教 Claude Code 把某件事做得更好（例：前端設計技能）
- **工作流程型**：把反覆執行的多步驟操作合併成一個指令

安裝：`/plugin marketplace` 搜尋安裝，或複製 GitHub URL 讓 Claude Code 自動安裝。

呼叫：`/技能名稱 <prompt>` 或自然語言（加「用正確的技能」可提高觸發率）。

Anthropic 官方有 frontend-design 技能可直接參考原始 Prompt 內容。

## Context Window 管理

**Context Rot 問題**：token 使用量越高，Claude Code 效能越差。

| Token 使用量 | Opus 效率 | Sonnet 效率 |
|-------------|-----------|-------------|
| 256K（25%） | ~92% | ~92% |
| 1M（100%） | ~78% | ~65% |

操作：
- 使用 `/clear` 重置 context（在 20~25% 時主動清除）
- 清除後 Claude Code 仍可從現有檔案重新取得 context
- 若需要帶走特定對話內容，請求 Claude Code 生成摘要
- 設定 Status Bar 顯示即時 context 百分比：告訴 Claude Code「建立顯示 context window 用量的永久狀態列」

## CLI 工具整合

CLI 工具住在 terminal，Claude Code 也住在 terminal，無額外 overhead，比 MCP 更省 token。

範例：**Playwright CLI**（瀏覽器自動化）
- 安裝：複製 repo URL 貼入 Claude Code 說「幫我安裝 Playwright CLI」
- 使用：告訴 Claude Code 用 Playwright 測試 web app，讓它自行設計測試案例
- `--headed` 可讓瀏覽器視窗顯示出來

## 部署流程

GitHub + Vercel 的標準流程（兩者都有免費方案）：

1. **GitHub**：建立 repo → 複製 URL → 告訴 Claude Code `commit and push to <URL>`（首次需完成認證）
2. **Vercel**：用 GitHub 帳號登入 → Import 剛建的 repo → Deploy
3. **自動化**：日後 `commit and push` → GitHub 更新 → Vercel 自動重新部署

建議進一步安裝 GitHub CLI 和 Vercel CLI，之後所有操作可直接用自然語言完成。
