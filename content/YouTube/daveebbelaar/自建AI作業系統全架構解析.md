---
title: 自建 AI 作業系統全架構解析
tags:
  - youtube
  - ai-agent
  - software-architecture
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-20
source: https://www.youtube.com/watch?v=rZX1OYetbSM
---

## 什麼是 AI 作業系統

參考 Jensen Huang（Nvidia CEO）的框架，AI 作業系統包含：

- **多模態輸入**：文字、語音、圖片等
- **記憶**：短期與長期記憶
- **模型**：驅動系統的 LLM
- **子代理（Sub-agents）**：以 markdown 技能檔案形式存在
- **工具**：CLI 指令、MCP 伺服器、外部服務整合
- **電腦使用**：瀏覽器、終端機操作
- **檔案系統**：結構化資料庫 + 非結構化 markdown 檔案

Dave 的核心理念：和傳統作業系統一樣，新增功能應像「安裝新 app」，而非重建整個系統。

## 三層架構

### 第一層：觸發式動作（Trigger-based Actions）

觸發條件 → 執行動作的自動化流程：

- Webhook（來自 WhatsApp、YouTube、Email、表單等）
- API 端點（FastAPI）
- 事件驅動處理（Event-driven Architecture）

技術實作：
```
Webhook → FastAPI 端點 → Redis 佇列 → Celery Worker → 執行邏輯
```

安全措施：簽名驗證（Signature Verification）確保 webhook 來源合法。

### 第二層：排程工作流（Scheduled Workflows）

定期執行的自動化任務（Cron Jobs）：

- 每週二 9:00 AM 執行競爭對手分析
- 每日報告生成
- CRM 資料同步

使用 **Celery Beat** 實現，和 Webhook 走同樣的 Worker 架構，差別只在觸發點。

DAG（有向無環圖）式工作流：每個節點是一個處理步驟，資料逐步傳遞，類似 n8n/Zapier 但完全在 Python 內實作。

### 第三層：AI 代理層（Agent Layer）

使用者發起的動態對話式任務（透過 WhatsApp、Slack、Claude Code 等）：

- 不是固定的 if-then，而是代理動態決策
- 可追問澄清問題
- 可觸發第一、二層的功能

Dave 的 WhatsApp 代理目前具備的工具：
- 網路搜尋
- 儲存內容創意到檔案系統
- **委派任務**：spawning 完整的 Claude Code subprocess（最強大但也最昂貴）

注意成本：使用 Opus 4.6 一次實驗就可能花費 $50 美金。建議設定 `max_turns` 和 `max_budget`。

## 基礎設施

部署在雲端伺服器，使用 Docker Compose 管理：

```
FastAPI（端點） + Caddy（反向代理/HTTPS）
  ↓
Redis（任務佇列）
  ↓
Celery Workers（執行任務）
  ↓
PostgreSQL（持久儲存） + 外部 API + Context Hub（Markdown 技能檔）
  ↓
Claude Agent SDK（可 spawn 雲端 Claude Code 實例）
```

CI/CD 設定：push 到 main branch → GitHub Actions 觸發 → Slack 通知部署完成。

## Context Hub（知識庫）架構

Dave 採用階層式 Context 載入系統，靈感來自 Open Viking 專案：

```
context-hub/
├── identity/      # 個人/商業使命、目標、價值觀
├── inbox/         # 待辦、想法（保持空白）
├── areas/         # 各個領域（內容、產品、客戶、健康...）
├── projects/      # 進行中的研究或建構專案
├── knowledge/     # SOP、研究文件
└── archive/       # 封存資料（代理預設不讀）
```

**三層 Context 載入**：

| 層級 | 檔案 | 內容 | 目的 |
|------|------|------|------|
| 0 | `abstract.md` | 一行說明 | 全庫掃描（< 2000 tokens）|
| 1 | `overview.md` | 短描述 + 關係 | 決定是否深入 |
| 2 | 完整檔案 | 全部內容 | 真正需要時才讀 |

所有檔案用 GitHub 版本控制，可讓本地 Claude Code 和雲端代理共用同一個 context hub。

## Soul 檔案

靈感來自 Open Claw 的 `soul.md`：深度描述自己的價值觀、使命、目標、做事方式。放在系統提示的最前面，配合 Opus 4.6 使用時，對話品質明顯提升。

## 五項關鍵原則

1. **從第一原則建立**：不要直接 clone 現有 repo，理解需求後從頭建構
2. **從最急迫的層開始**：自動化個人任務 → 第三層；商業流程 → 第一、二層
3. **持久化儲存**：所有事件保存到資料庫，方便除錯和追蹤失敗
4. **長期思維**：建立可擴充的基礎架構，不需每次新工具出來就重建
5. **Context 是王**：AI 的能力取決於它所擁有的 context 品質
