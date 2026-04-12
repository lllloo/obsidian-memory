---
title: "10 Minute Masterclass: Claude Code Skills"
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
source: https://youtu.be/UtGszoiwrsQ
---

10 分鐘速成：深入理解 Claude Code Skills 的運作原理、使用方式與自訂技巧。

## Skills 是什麼

Skills 本質上就是**文字 prompt**，用來告訴 Claude Code 如何以特定方式執行特定任務。如果能在 Claude Code 裡用 prompt 做到，就能做成 Skill。

## Skills 的載入機制

- Claude Code 不會把所有 Skills 預載入 context window
- 它持有一份清單：每個 Skill 的名稱 + 約 100 字描述
- 當對話觸發相關需求，Claude Code 才動態載入對應 Skill
- **問題**：Skills 太多（30–50 個）會導致選錯 Skill

## 三種觸發 Skills 的方式

1. **自然語言**（隱性）：說「幫我設計前端」，看它是否自動呼叫
2. **明確指定**：「使用 front-end design skill」
3. **強制呼叫**：`/front-end-design`（100% 觸發）

## 安裝 Skills

- `/plugin` — 開啟 Skills 市集，可搜尋或瀏覽安裝
- **User scope**：所有專案皆可用
- **Repo scope**：僅限當前專案（適合專案特定工作流）
- 安裝後執行 `/reload plugins` 啟用
- CLI 工具的 Skills：通常在 GitHub repo 提供一行安裝指令

## 自訂 Skills：Skill Creator

官方 Skill，在 Plugin 市集可找到。功能：
- 建立新 Skill
- 優化現有 Skill 的描述（提升觸發準確度）
- 自動 benchmark：生成測試案例，比較有無 Skill 的效果差異
- 提供評估報告：assertion pass rate、時間、token 消耗

使用方式：`/skill-creator`，描述想建立的 Skill 即可。甚至可以請 Claude Code 分析目前工作習慣，主動建議應建立哪些 Skills。

## 最佳實踐

- **保持 Skills 精簡**：寧可少而精，避免 Skill 膨脹導致選錯
- Skills 可組合：一個主 Skill 呼叫子 Skills，建構完整工作流
- 優化 Skill 描述 = 提升自動觸發的準確率
