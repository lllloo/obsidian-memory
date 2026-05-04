---
title: Tested Sonnet 4.6 via OpenRouter through GitHub CoPilot / VS Code to gauge whats API billing will be like. I was shocked.
created: 2026-05-04
updated: 2026-05-04
source: https://www.reddit.com/r/GithubCopilot/comments/1t1nzqf/tested_sonnet_46_via_openrouter_through_github/
published: 2026-05-02
tags:
  - reddit
  - github-copilot
  - ai-tools
  - bug
---

> **繁中摘要**：實測在 GHCP（VS Code）以 OpenRouter BYOK 跑 Sonnet 4.6，單一「加一個 Alert Box」任務消耗 $4.67 USD；社群指出 BYOK Claude 走 GHCP 時 prompt caching 沒生效，是費用異常飆高的關鍵 root cause（已開 VS Code issue）。

---

## 原文重點

- 設定：OpenRouter 帳號加值 $15，把 API key 設到 GHCP（VS Code）
- 模型：選 Sonnet 4.6（OpenRouter 路由）
- 任務：在現有 webui 加一個 Alert Box
- 結果：3–4 次 tool call 完成，但位置與動畫需手動修正
- 計費：單次任務 OpenRouter activity 顯示 **$4.67 USD**
- 結論：以 API 真實成本看，Anthropic 模型走 BYOK 模式對個人開發者不划算

## 社群討論亮點

- **同任務跨模型成本對照（top comment, score 127）**：
  - Sonnet 4.6 over API：$1.05
  - DeepSeek 4 Flash：$0.02
  - 兩者完成方式相同
- **Prompt caching 在 BYOK 下沒生效（root cause）**：有人指出 Claude 模型走 GHCP BYOK 時並沒有用上 prompt caching，導致 input token 重複計費。已在 VS Code repo 開 issue：`microsoft/vscode#312939`
- **替代組合**：Kimi K2.6（SOTA 等級）+ DeepSeek V4 Flash（低價）；訂閱方案可考慮 OpenCode Go 或 Ollama Cloud 託管
- **DeepSeek V4 Pro 評價**：75% off 促銷價可接受，原價偏貴，不如 Flash 划算
