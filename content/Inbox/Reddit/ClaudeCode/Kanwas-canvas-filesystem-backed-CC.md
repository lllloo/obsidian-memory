---
title: We added CC to a Miro-like canvas backed by the filesystem, and open-sourced it
created: 2026-05-04
updated: 2026-05-04
source: https://www.reddit.com/r/ClaudeCode/comments/1t1qjxj/we_added_cc_to_a_mirolike_canvas_backed_by_the/
published: 2026-05-02
tags:
  - reddit
  - claude-code
  - ai-tools
---

> **繁中摘要**：開源工具 Kanwas，做成 Miro-like canvas 但底層是 markdown / yaml / 檔案系統 + git history。用來放 spec、product direction、screenshot、decision log 等「圍繞 code 的非 code 工作」，作者認為 CC 在 repo 內 execution 很強，但對 pre-code 思考工作的 terminal/chat 介面不夠順手。

---

## 原文重點

### 痛點

CC 在 repo 內 execution 強，但「圍繞 code 的工作」（spec、product direction、user feedback、screenshot、launch note、architecture tradeoff、decision log、初期 research）在 terminal/chat 介面很彆扭：

- 模型不夠主動 push thinking
- 不夠多問問題
- 難以分支多想法
- 好的 output 容易被埋掉
- reasoning trail 難分享
- 隊友想反應只能複製貼到 Notion / Linear / Slack / Miro

### 架構

- Miro-like 工作區，agent 與人類同台協作
- 底層是 **檔案系統**：markdown / YAML 檔，搭配 **git history**
- canvas 上可放 note、doc、link、screenshot、decision、instruction、agent output
- 開源；作者強調要逃離 Notion 這類「不可改」的黑盒

### 連結

- Repo：[github.com/kanwas-ai/kanwas](https://github.com/kanwas-ai/kanwas)
- 網站：[kanwas.ai](https://kanwas.ai/)

### 可遷移點（即使不用 Kanwas）

「canvas 視覺化 + md/yaml 為單一事實來源 + git 為歷史」這個 stack 設計可借鏡：把 spec、決策、研究散件都放成 plain text + 視覺化前端，與本 vault 的 Obsidian + Quartz 結構相似。

## 社群討論亮點

- **Real-time collaboration 質疑**（1 分留言）：個人檔案系統上的 md 檔如何做到即時協作？技術細節在 selftext 沒講
- **替代 Cowork 的潛力**（多人）：實測使用者覺得 output 比 cowork 好，「在 canvas 上看著迭代」比 chat 形式直觀
- **Onboarding 反饋**：建議加 one-click usecases 讓新人快速試出價值，不要全靠 onboarding 流程說明
