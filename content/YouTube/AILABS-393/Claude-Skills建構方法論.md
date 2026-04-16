---
title: Claude Skills 建構方法論
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-16
source: https://www.youtube.com/watch?v=aEqKWI-0N0c
parent: "[[01.index]]"
---

## Anthropic 官方 Skills 建構指南重點

最重要的一件事：**測試與迭代**。起始版本和最終版本往往是完全不同的東西。

## Description 設計：何時使用 vs 何時不使用

Description（YAML frontmatter）是 Claude 決定是否載入 skill 的依據。好的 description 要回答兩個問題：

1. 這個 skill 做什麼
2. 什麼時候應該用它（trigger phrases）
3. 什麼時候不應該用它（negative triggers）

範例：
```yaml
# 好的做法
triggers:
  - build a landing page
  - nano banana
negative_triggers:
  - simple bug fix
  - database work
```

## 三層 Progressive Disclosure 結構

Context window 只應載入當下需要的資訊：

- **Level 1（description）**：永遠在 Claude context 中，簡短
- **Level 2（skill.md body）**：workflow 與各 level 3 的引用
- **Level 3（references/ 資料夾）**：domain-specific 細節，按需載入

常見錯誤：把所有 workflow、tips、troubleshooting 塞進單一檔案。

## Critical Section

在 skill.md 最前面列出最重要的資訊，不要埋在指令中間。

## Scripts 資料夾

放置 Claude 可呼叫的可執行工具：

- 設計好 CLI arguments 讓 Claude 容易呼叫
- 提供 preview mode（在執行破壞性操作前先預覽結果）

## Validation Gates

在 workflow 各步驟之間設置明確的通過條件，防止 Claude 自動跳過驗證。若條件固定不變，建立 tool 作為驗證 gate。

範例：Nano Banana skill 的圖片驗證流程：
1. `validate_images` script（結構驗證）
2. Visual review（Claude 自行評估美觀度，給出 pass/fail + 原因）
3. 若 fail：刪除圖片 → 寫新 prompt（含失敗原因）→ 重新生成

## Error Handling

在 skill.md 記錄已知錯誤的處理方式：

```
錯誤：missing or corrupt images
原因：Anti-gravity 不總是生成正確輸出
修復步驟：[具體步驟]
```

發生過一次就必須記錄，因為還會再發生。

## References 作為知識模組

References 是 domain-specific 的細分知識包，可持續擴充 skill 的知識庫而不污染主要 context。例如：

- `prompting_rules.md`：13 條測試迭代出的 prompting 規則
- `design_patterns.md`：設計模式
- `frontend_aesthetics.md`：前端美學指引
