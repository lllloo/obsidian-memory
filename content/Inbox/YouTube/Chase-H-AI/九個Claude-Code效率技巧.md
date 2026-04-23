---
title: 九個 Claude Code 效率技巧
created: 2026-04-15
updated: 2026-04-15
source: https://www.youtube.com/watch?v=XkSBO-CZDFs
published: 2026-03-27
parent: "[[01.index]]"
tags:
  - youtube
---

## 技巧一：CLI 取代 MCP

MCP 已是過去式，優先改用 CLI（命令列介面工具）：
- CLI 住在 terminal，Claude Code 也住在 terminal，無額外 overhead
- Token 消耗更低，功能通常更完整
- CLI 工具通常配套技能一起安裝

## 技巧二：`/btw`（By The Way）

在 Claude Code 進行長任務時，`/btw` 允許開啟側邊對話：
- 不中斷正在執行的任務
- 側邊對話不會增加 context window 用量，幾乎免費

## 技巧三：完成聲音 Hook

```
/hook
```

設定任務完成時播放提示音。有多個 Claude Code 視窗同時執行時，可避免忘記查看結果，每週可節省數小時。

## 技巧四：`/clear` 清除 Context

主動使用 `/clear` 重置 context window：
- Context Rot 問題：token 使用量越高，Claude Code 表現越差
- 在 256K tokens（約 25%）時：效率 91~92%
- 在 1M tokens（100%）時：效率掉到 65~78%（Opus vs Sonnet）
- 建議在 20~25% 時就清除，重新開始

## 技巧五：Status Line

```
/status line
```

在 prompt 輸入欄下方顯示常駐狀態列，可顯示：當前目錄、使用模型、context window 用量百分比。指定想顯示的項目即可建立。

## 技巧六：Skill Creator 技能

Anthropic 官方的 Skill Creator 技能不只建立技能，還能：
- 修改與改進既有技能
- 執行量化基準測試，對比改前改後的實際效果數字

## 技巧七：Agent Teams（實驗性功能）

需在設定中手動開啟，與一般 Sub-agent 的差異：
- Sub-agent：各自獨立工作，只跟主 session 溝通
- Agent Teams：Sub-agent 彼此可互相溝通、協調
- 啟動時需明確說「建立一個 agent team 來做 A、B、C」

## 技巧八：Plan Mode 中問開放性問題

進入 Plan Mode 後，主動要求更深的思考：
- 「我沒想到什麼？」
- 「這樣做有什麼非預期的後果？」
- 「這個領域的專家在這時候會問什麼問題？」

Plan Mode 預設問題偏表層；用這些提示強迫它更深入，對技術背景不足的使用者特別重要。

## 技巧九：Claude Code 結合 Obsidian

將 Claude Code 的工作目錄設在 Obsidian vault 資料夾，讓所有輸出以 Markdown 存入 vault：
- Claude Code 建立、整理文件
- Obsidian 提供圖形介面查看文件間的連結關係
- 特別適合個人助理、知識管理類型的專案
