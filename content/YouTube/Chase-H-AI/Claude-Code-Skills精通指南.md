---
title: Claude Code Skills 精通指南
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-16
source: https://www.youtube.com/watch?v=UtGszoiwrsQ
parent: "[[01.index]]"
---

## Skills 是什麼

Skills 就是文字 prompt。告訴 Claude Code 如何以特定方式做特定事情，僅此而已。可以應用於幾乎任何使用場景，也可以串連 sub-skills 打造複雜工作流程。

## Skills 的運作機制

Claude Code 不會把所有 skills 載入 context window，而是維護一份清單，記錄每個 skill 的名稱和約 100 字的描述。

當你的指令觸發某 skill 時，它才被載入到 context window。因此：
- Skill 本身可以很長（數千 tokens）
- 清單永遠存在，全文只在需要時載入

## 觸發 Skills 的三種方式

1. **自然語言（模糊）**：「Let's build a website」—— 祈禱它會用 skill
2. **明確指定**：「Let's use the front-end design skill」
3. **強制觸發**：`/frontend-design` —— 100% 執行該 skill

## 管理 Skills 的注意事項

**避免 skill bloat**：
- 盡量精簡 skill 數量（scalpel，不要 50 把刀）
- 區分 user scope（所有專案通用）vs. project scope（僅此 repo）
- 安裝後執行 `/reload plugins` 啟用

**優化 skill 描述**：描述寫得好，Claude Code 才能正確選用正確 skill。

## 安裝 Skills

**從 Marketplace**：
- `/plugin` → 搜尋 skill → 選安裝範圍（user 或 project）

**從 GitHub**：
- 直接複製安裝指令（如 `playwright CLI install skills`）貼入終端機
- 或把整個頁面貼給 Claude Code，讓它自己處理

## 建立自訂 Skills：Skill Creator

Skill Creator 是 Anthropic 官方 skill，可在 `/plugin` marketplace 找到。功能：
- 建立新 skill
- 修改優化現有 skill
- 評估 skill 效能
- 自動 benchmark（帶 skill vs. 不帶 skill 的比較）

**使用流程**：

```
/skill-creator
```

描述你想要的 skill → Skill Creator：
1. 生成三個 sub-agents 探索問題
2. 詢問澄清問題
3. 自動跑 6 組測試（3 個含 skill、3 個不含）
4. 輸出 benchmark 報告（pass rate、時間、token 使用）
5. 提供 skill 為何有價值的摘要

**範例**：建立一個根據內容描述生成 YouTube 標題、並對照近期高績效影片的 skill，Skill Creator 自動分析近三個月表現、競爭環境，產出分層建議（Tier 1 穩健、Tier 2 冒險、Tier 3 全力一搏）。
