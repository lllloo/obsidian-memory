---
title: "Update: Compared Claude 4.7 with Qwen 3.6 35B with Qwen 3.6 27B - in Vscode Copilot on the same complex task"
created: 2026-04-27
updated: 2026-04-27
source: https://www.reddit.com/r/GithubCopilot/comments/1st1m93/update_compared_claude_47_with_qwen_36_35b_with/
published: 2026-04-22
tags:
  - reddit
  - github-copilot
  - ai-tools
  - local-llm
---

> **繁中摘要**：在 VSCode Copilot 環境下，用同一個高複雜度專案比較 Claude Opus 4.7、Qwen 3.6 35B（MOE）與 Qwen 3.6 27B（dense）。三任務測試結論：Opus > Qwen 27B > Qwen 35B；27B 較擅長抓概念誤解，35B 較會做未驗證假設。

---

## 原文重點

**測試環境：**

- 後端：llama.cpp + LM Studio
- Quantization：4-bit weight + Q8 KV cache
- 介面：VSCode Copilot（custom model 接 local server）
- Token 速度：Qwen 3.6 27B 在 100k context 約 49 tokens/sec（推測 llama.cpp + Q8 KV cache 影響 prompt ingestion）

**Task 1 — Audit（互審文件）：**

- Qwen 3.6 35B 先針對整個專案（約 1M tokens 程式碼，需穿過多次 context summarization、讀 bash history 找 shellscripts）產生文件
- 由 Opus 4.7、Qwen 27B、Qwen 35B 各自 audit 同一份文件，輸出統一格式
- GPT 5.4 xhigh 盲審 ranking：**Opus 4.7 > Qwen 27B > Qwen 35B**
  - 27B：最會抓**概念性誤解**（conceptual misunderstandings），但較具詮釋傾向
  - 35B：細節豐富，但較常做出 **未經驗證的 edge-case 假設**

**Task 2 — Rewrite Documentation：**

- 換 Qwen 27B 重做 35B 的文件任務
- Context summarization 比 35B 慢非常多（35B 是「shoot through」）
- 結論：27B 的 audit / correction 能力較好，但獨立寫 documentation 不如 35B
- 一個關鍵問題：context summarization 後 27B 不會穩定 reload skills（如 `copilot-readme` 檔），猜測需要強化 system prompt 重申 copilot instructions

**Task 3 — Real work（pytorch hook、runtime model analysis）：**

- 27B 在低層級 inference manipulation 任務上開頭順利但作者因時間中止
- 切到 35B 重做，GPT 5.4 評估反而 35B 架構分析較強
- 唯一持續問題仍是：35B 會做 **未驗證假設**；當追問「你檢查過 model loader 嗎？」時模型回應品質明顯較差

## 社群討論亮點

- 有用戶在 M3 Max 64GB RAM 上跑 Qwen 3.6 27B，主觀感覺品質接近 Sonnet 4.6，速度可接受；同時掛在 GitHub Copilot 與 Claude Code 中使用，認為已可考慮取消雲端訂閱
- 開放問題：尚未有人對比 Qwen 與 OpenRouter 上最熱門的 Sonnet
