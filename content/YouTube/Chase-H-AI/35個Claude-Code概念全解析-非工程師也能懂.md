---
title: "35 個 Claude Code 概念全解析（非工程師也能懂）"
tags:
  - youtube
  - claude-code
created: 2026-04-12
updated: 2026-04-12
published: 2026-04-08
source: https://youtu.be/UAMAAoSPu8o
---

Chase H 為非技術背景用戶整理 35 個 Claude Code 核心概念，分四個階段從入門到進階。

## 四個學習階段

### 第一階段：核心必知（Concepts 1-5）
1. **claude.ai vs Claude Code 的差異**：同樣的大腦，但 Claude Code 有「手」，能實際操作電腦
2. **安裝 Claude Code**：一行指令安裝，支援 Mac/Linux/WSL 及 Windows PowerShell
3. **在哪裡使用**：Terminal、VS Code、Claude Desktop App、Co-work 均可，推薦從 Terminal 入手
4. **權限設定（Permissions）**：
   - 預設：每次修改都需確認
   - Accept Edits On：自動編輯文件，bash 指令仍需確認
   - `--dangerously-skip-permissions`：完全略過確認，最快但需謹慎
5. **Plan Mode**：讓 Claude Code 先規劃再執行，填補 prompt 的漏洞，提升輸出品質

### 第二階段：核心功能
6. **使用心態**：把 Claude Code 當協作者，主動追問不懂的概念
7. **CLAUDE.md**：專案記憶文件，告訴 Claude Code 關於專案的所有規則
8. **Context Window**：Claude Code 的短期記憶，過大時需壓縮或開新會話
9. **Compact 指令**：壓縮 context，保留重要資訊
10. **技術棧選擇**：詢問 Claude Code 建議，理解推薦理由

### 第三階段：進階技巧
- **Skills（技能）**：擴展 Claude Code 能力的 Markdown 指令集
- **Plugins**：從官方 marketplace 安裝
- **多代理協作（Multi-agent）**：用多個 Claude Code 實例平行處理任務
- **Git 整合**：版本控制與分支管理
- **MCP（Model Context Protocol）**：連接外部工具與服務

### 第四階段：進階 Power User
- **Ultra Plan**：雲端規劃模式，速度更快
- **Auto Research**：機器學習自動優化工具
- **LightRAG**：開源 Graph RAG 系統
- **Obsidian 知識庫**：輕量 RAG 替代方案
- **GWS CLI**：Google Suite 整合

## 關鍵心態
- Claude Code 是無限耐心的導師，要主動追問、真正理解，而非只是盲目按 Accept
- 與其他人的差異化在於：你能理解 AI 在做什麼，而不只是當「vibe coder」
