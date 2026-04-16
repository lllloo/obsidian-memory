---
title: 如何建構並交付 AI 客製化解決方案
tags:
  - youtube
  - ai-agent
  - claude-code
created: 2026-04-13
updated: 2026-04-13
published: 2026-04-13
source: https://www.youtube.com/watch?v=Q679gH7oszg
parent: "[[01.index]]"
---

## 背景

Dave 和共同創辦人以 2 人小團隊運營 Datalumina Solutions，加上按需聘用的外包人員。過去 3 年完成超過 50 個 B2B AI 客製化專案。技術棧始終以 Python 為後端語言。

主要服務類型：文件處理、內容生成、客服支援、內部知識助理、資料提取。

## 發現與用例選擇（Discovery）

**探索電話（Discovery Call）**的目標是找到「真正的問題」，而非客戶以為他們需要的東西。

核心問題：**ROI 在哪裡？** 建構客製化 AI 軟體成本不低，必須確認有實際投資報酬。

### 從簡單高影響用例開始

大多數組織有大量低垂果實（Low-hanging Fruit），卻專注在複雜的大問題：
- 一個員工每天重複的手動流程，可能只需要簡單的 n8n/Zapier 連接
- 文件處理流水線，則需要 LLM 加持

**原則：永遠選快贏而非大夢想。**

### 紅旗警示

以下情況要小心是否適合接案：
- 「因為大家都在用 AI」——沒有明確 ROI
- 沒有清晰的成功標準（無法衡量好壞）
- 客戶期望從第一天就達到完美
- 資料存取/安全性/授權問題未解決

## 準確率的客戶教育

這是最棘手的部分。LLM 不是傳統確定性軟體：

| 版本 | 預期準確率 |
|------|-----------|
| 第一次交付（V1） | 70–80% |
| 迭代後 | 90% |
| 完美（99%+） | 通常不切實際 |

**正確框架**：以「迭代式開發」而非「一次完美」來溝通。快速交付 → 建立回饋機制 → 持續改進。

客戶也需要投入時間提供具領域知識的回饋，必須從一開始就說清楚。

## 用例評估框架

在決定是否接案前，檢查以下條件：

- 流程是否簡單且可重複？
- 是否有明確的成功/失敗規則？
- 錯誤是否可以升級給人工處理？（Human Escalation）
- 是否需要全程人工審核？（Human in the Loop）
- 錯誤的影響有多大？（直接面向客戶的高風險系統更需謹慎）

## 範疇界定（Scoping）

最難的部分之一。核心原則：**明確定義「做什麼」和「不做什麼」。**

常見陷阱：
- 客戶不斷追加需求（Scope Creep）
- 低估 LLM 在規模下的不可預測性
- 先把非核心部分過度工程化，但核心指標還沒達到

工作方式：找出核心 KPI → 只優化那個指標 → 列出 must-have 和 nice-to-have。

### PoC vs MVP

| 類型 | 定義 | 交付物 |
|------|------|--------|
| **PoC（概念驗證）** | 不確定能否達到 KPI，需先證明 | 本地 Demo + 報告 |
| **MVP（最小可行產品）** | 已知可行，建最小可用版本 | 可部署、有實際價值的系統 |

PoC 通常不交付生產系統，客戶需理解這點。

## 提案結構

標準提案文件內容：

1. 問題陳述（用客戶的話描述）
2. 解決方案與範疇邊界
3. 技術方法（可含架構圖）
4. 納入與排除的功能
5. 成功標準與量測方式
6. 時程與定價
7. **持續成本估算**（API 費用、基礎設施、維護）

## Sprint 結構

採用 **2 週 Sprint 模型**，定價 €10,000–20,000 / Sprint：

```
Day 1–2：設置與架構（Scaffolding）
Day 3–8：核心開發（整合 LLM、迭代品質）
Day 9–14：測試、打磨、Demo
```

溝通方式：非同步為主（不做每日站會）。

### 現實中的 Sprint 間隔

理想：Sprint 1 → Sprint 2 → Sprint 3（連續）

現實：Sprint 1 交付後，客戶通常「消失」2–8 週進行內部評估，造成現金流壓力。

應對策略：過度規劃管線，讓多個客戶專案交錯進行。

## 技術棧

所有專案標準化使用同一個棧，基於 **GenAI Launchpad** 框架（`launchpad.datalumina.com`）：

- **後端**：FastAPI + Celery + Redis + PostgreSQL（自架 Supabase）
- **前端**：Next.js（由共同創辦人 Yuri 負責）
- **LLM**：Azure OpenAI（客戶資料合規要求）
- **工作流**：DAG-based Python 模組
- **框架整合**：Pydantic AI、Langfuse、Sentry

每個新客戶專案 = Fork GenAI Launchpad → 已配置 Docker、資料庫、認證、檔案結構。

## Claude Code 使用方式

Dave 的 vanilla 設定：

- 模型：Opus 4.6（錄製時）
- 同時開啟 1–3 個 session（不做複雜的 work tree 系統）
- 流程：**Plan Mode 先，再 Execute**
- 每個 session 從新開始，需主動告訴它要先讀哪些文件（避免浪費 context）

```
開新 session → "先讀這兩份文件，再看這兩個檔案" → 執行任務
```

注意：context window 管理是最重要的事，保持 CLAUDE.md 更新。

## 測試與評估

每個專案必備：

- **Unit Tests**：各節點單元測試
- **Integration Tests**：整合測試
- **LLM Evals**：以真實資料庫記錄作為測試輸入，驗證特定步驟的輸出

建立技能（Skill）讓 Claude Code 自動從資料庫拉取問題記錄、診斷問題：

```
客戶回報問題 → 腳本拉取該記錄 → Claude Code 分析 → 修復
```

## 部署流程

```
本地開發 → GitHub → CI/CD（GitHub Actions）→ Hetzner VM → Caddy（HTTPS）
```

為什麼選 Hetzner：比 AWS/Azure 便宜 10 倍，可靠，使用多年。

容器化：從第一天就用 Docker Compose，Fork 起點已預設好所有設定。

安全措施：
- 預設封鎖所有 IP
- 使用 Netbird（靜態 IP VPN）將資料庫存取限制在已知 IP
- 防火牆只開放 80/443 port
- 內部服務使用私有網路

監控工具：
- **Langfuse**：LLM trace 追蹤（整合在 GenAI Launchpad）
- **Sentry**：錯誤追蹤（hook 到 Slack 頻道），可將錯誤複製為 Markdown 直接丟給 Claude Code 修復

## AI 開發的商業模式

過去：按時計費（小時/日費）。

現在：AI 讓生產力提升 5–10 倍，但 Dave 選擇**維持同樣定價，用速度換更多專案量和更高品質**，而非降價。

理由：市場尚未意識到 AI 工程師的效率提升，目前仍是黃金時期。

長期策略：成為客戶的長期 AI 開發夥伴：
- 軟體永遠不完整（維護、新功能、更新）
- 信任建立後，新專案自然而來
- 可收取維護費和 API 費用，形成穩定的重複性收入
