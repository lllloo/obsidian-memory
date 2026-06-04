---
title: Awesome Copilot
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/ai/awesome-copilot
tags:
  - copilot
  - ai-tools
  - github
  - best-practices
---

# Awesome Copilot

[Awesome Copilot](https://github.com/github/awesome-copilot) 是 GitHub 官方維護的精選資源集，收錄了高品質的 GitHub Copilot 自訂指令（Instructions）、Prompt 檔案，以及各種讓 Copilot 更聰明的配置範例。

## 什麼是 Instructions 與 Prompts

GitHub Copilot 提供兩種自訂方式，讓 AI 更符合你的開發習慣與專案需求：

### Instructions（自訂指引）

存放於 `.github/instructions/` 目錄，副檔名為 `*.instructions.md`。透過 YAML frontmatter 的 `applyTo` 欄位指定適用的檔案類型，Copilot 在開啟符合條件的檔案時會自動載入對應指引。

```yaml
---
applyTo: '**/*.vue'
description: 'Vue.js 3 Composition API 最佳實踐指引'
---
```

適合用來定義：程式碼風格、命名慣例、框架最佳實踐、安全規範等「持續性」的開發準則。

### Prompts（可重用提示）

存放於 `.github/prompts/` 目錄，副檔名為 `*.prompt.md`。可在 Copilot Chat 中手動呼叫，適合封裝重複性的工作流程，例如產生 README、撰寫測試、建立 ADR 等。

## 如何使用 Awesome Copilot 的資源

1. 前往 [github/awesome-copilot](https://github.com/github/awesome-copilot) 瀏覽可用的 instructions 與 prompts
2. 挑選適合你專案技術棧的檔案（例如 Vue、TypeScript、Docker）
3. 複製到你的專案 `.github/instructions/` 或 `.github/prompts/` 目錄
4. 依專案需求調整 frontmatter 與內容

## 參考資源

- [Awesome Copilot GitHub](https://github.com/github/awesome-copilot)
- [VS Code Copilot 自訂設定](https://code.visualstudio.com/docs/copilot/customization/overview)
