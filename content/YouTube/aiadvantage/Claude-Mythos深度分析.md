---
title: Claude Mythos 深度分析
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-04-08
source: https://www.youtube.com/watch?v=NOR4NHL-SiI
---

## 什麼是 Claude Mythos

- Anthropic 新旗艦模型，**尚未公開發布**，以預覽形式揭露
- 推出 **Project Glass Wing**：與各大科技公司合作，先用 Mythos 強化安全性，再正式上線
- Poly Markets 預測：超過 50% 機率在 4 月底前發布

## Benchmark 表現

| 指標 | Opus 4.6 | Claude Mythos |
|------|----------|---------------|
| SWE-bench Pro | 57.5 | 93.9 |
| Multimodal | ~27% | ~59% |
| MMLU | — | 小幅提升 |

- 軟體工程 benchmark 從 80.8 跳至 93.9，幅度空前
- 找到 OpenBSD（27 年歷史）安全漏洞，成本約 $50 token（未完全驗證）
- 前代 Opus 在 Firefox 發現 2 個漏洞；Mythos 發現 **181 個**

## 關鍵洞察一：是模型能力讓 Agentic 工具起飛

- 2023 年的 BabyAGI、AgentGPT 等 agentic 系統早已存在，當時失敗原因是**底層模型不夠強**，不是工程問題
- 真正的轉捩點是 **Opus 4.5**：prompt 遵循度大幅提升，能在 20 分鐘工作後保持完整記憶
- Mythos 的能力提升意味著 agentic 工具的適用範圍將沿「職業影響力光譜」大幅擴展
  - 現在：軟體開發、內容創作受益最大
  - 物理性工作（水電工）幾乎不受影響
  - 未來：影響會往光譜中段延伸

## 關鍵洞察二：時機不是巧合

- 中國 GLM 5.1 開源模型（SWE-bench Pro 54.9，接近 Opus 4.6 的 57.5）發布約 9 小時後
- Anthropic 即發布 Mythos 公告，配套 Microsoft、Google、Linux Foundation 等合作夥伴背書
- 歷史模式重演：OpenAI 過去常在 Google 發布前搶先公告

## 關鍵洞察三：第二、三階效應

- **第二階**：競爭對手（OpenAI、Google）被迫加速推出對應產品
- **第三階**：超強模型 + agentic 工具組合，將出現每月花費 $10 萬以上的個人用戶，因為 AI 帶來的價值遠超成本
- Anthropic 已禁止透過 OAuth 以 $200/月 Claude 訂閱使用 OpenClaw，迫使高度依賴者轉向 API（$2,000–$3,000/月）

## AI 學習路徑框架（作者分享）

1. **基礎層**：學會使用 ChatGPT / Claude 等主流工具
2. **Context 層**：學習管理 context，建立個人 prompt 與知識系統（大多數人缺少此層）
3. **Agentic 層**：使用 OpenClaw、Claude Code 等自動化 agent

作者強調：必須先建好 Context 層，Agentic 工具才能有效運作
