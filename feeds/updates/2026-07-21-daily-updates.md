---
title: "2026-07-21 Daily Updates"
created: 2026-07-21
updated: 2026-07-21
tags:
  - updates
  - opencode
  - codex
  - copilot
---

## OpenCode

### v1.18.4 · 2026-07-20（[Changelog](https://opencode.ai/changelog)）

**繁中摘要**：v1.18.4 針對 Anthropic 相容 provider 上的 Kimi 模型加入 adaptive thinking control（預設輸出摘要推理），並修正多個 provider/model 層行為（OpenAI 逾時、推理選項尊重、Azure 端點）；其餘為 Desktop UI 修復。

- **Kimi adaptive thinking**：Anthropic 相容 provider 上的 Kimi 模型改用 adaptive thinking control，預設輸出摘要推理結果。
- **provider 推理選項修正**：改為尊重 provider 定義的推理選項，不再回退到錯誤的推理控制；同時減少 OpenAI provider 在連線緩慢時的標頭逾時。
- **Azure 端點恢復**：恢復 Azure Cognitive Services 端點對 Azure 託管模型的支援。
- **Desktop 修復**：終端主題同步應用主題、審查面板對齊與調整大小改進、v2 提示輸入重寫（命令/上下文/shell/附件/歷史更可靠）等多項 UI 修復。

---

## OpenAI Codex

### v0.144.5 · 2026-07-16（[Release](https://github.com/openai/codex/releases/tag/rust-v0.144.5)）

**繁中摘要**：加強 dangerous-command 偵測，涵蓋更多 forced `rm` 形式，並在指令被拒絕時提供更清楚的拒絕原因。

- **危險指令偵測強化**：擴大偵測範圍納入更多 forced `rm` 變體，降低誤放行風險；拒絕訊息也更明確，方便判斷為何指令被擋。

---

## GitHub Copilot

### 2026-07-20 · Billing UI 新增 cost center AI credit pool 管理（[AI credit pools for cost centers in the billing UI](https://github.blog/changelog/2026-07-20-ai-credit-pools-for-cost-centers-in-the-billing-ui)）

**繁中摘要**：billing UI 新增可直接在建立/編輯 cost center 時管理其 AI credit pool 的介面，此前僅能透過其他途徑管理。

- **billing UI 直接管理 credit pool**：管理者建立或編輯 cost center 時可就地調整其 AI credit pool，簡化額度分配流程。
