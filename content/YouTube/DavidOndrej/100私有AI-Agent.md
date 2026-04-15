---
title: 100% 私有 AI Agent：本地部署完全指南
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-23
source: https://www.youtube.com/watch?v=JLIFx9r5EDg
---

## 重點摘要

- 示範如何在本地執行 Agent Zero，實現 100% 私有的 AI Agent
- 標題 "RIP OpenClaw" 暗示以本地私有方案取代 OpenClaw
- 關鍵設定：Chat model API base URL 為 `http://host.docker.internal:11434`（Ollama 本地模型端點）
- 相關工具：[Agent Zero](https://github.com/agent0ai/agent-zero)
- 無需外部 API，所有推論在本機完成，適合隱私敏感的使用情境
