---
title: GSD 框架（Get Shit Done）
created: 2026-04-20
updated: 2026-04-20
tags:
  - claude-code
  - agent-framework
  - context-management
---

以「一個 task 一個乾淨 context window」為核心的 agent orchestration 框架。涵蓋是什麼、工作流程、安裝與使用、費用陷阱、與其他框架對比、何時該用。

## 核心概念

**GSD（Get Shit Done）** 由 **TÂCHES（solo developer）** 發起，GitHub 組織 `gsd-build`。核心設計：對抗 **context rot**（Claude 對話前 20% 精準，40–80% 準確度大幅下降）。

最新版為 **GSD-2**（`gsd-build/gsd-2`）：基於 **Pi SDK** 的 **standalone TypeScript CLI**，對 Claude Code 獨立執行。前一代 `get-shit-done`（v1.38.1, 2026-04）仍在維護，但定位為「注入 Claude Code 的 prompt framework」，架構上與 v2 不同。

對抗 context rot 的機制（v2 架構）：
- **Fresh session per task**：每個 task 在全新 context window 執行，不累積垃圾
- **State machine driving execution**：由狀態機驅動，不是 LLM 自己 loop
- **狀態持久化到本地 MD 檔**（requirements.md、roadmap.md、state.md、phase context）
- **Adversarial planning**：planning agent + verifier agent 互相挑戰計畫
- **Sub-agent 用不同模型**（輕任務 Sonnet、重任務 Opus）
- **Extract learning**：流程結束後擷取決策、模式、教訓供未來 session 參考
- **Crash recovery**：lock files + session forensics，中斷後可 resume
- **Observability**：內建 cost tracking、progress dashboard、stuck detection
- **Git strategy**：worktree 隔離 + 自動 branch/merge

鐵律：**一個 task 必須在一個 context window 內完成**。

## 工作流程

### Phase 1：初始化

1. `/new-project` — 掃描現有 codebase（空白可跳過）
2. 追問 app 想法、目標用戶、功能範圍、out-of-scope
3. 生成 `.planning/project.md`（**刻意精簡**，避免 agent 迷失在文件中）
4. 多個 sub-agent 平行研究不同面向（stack / features / architecture / pitfalls）
5. **Synthesizer agent**（用 Sonnet 以節省成本）整合研究、標示潛在風險
6. 確認 MVP 需求、批准 roadmap

### Phase 2：逐 phase 實作

1. 選 `with discussion` 或 `skip discussion`
2. Discussion 模式：agent 追問需求，生成 `.planning/phases/<phase>/context.md`
3. **Planning agent** 生成計畫 → **Verifier agent** 交叉驗證 → 通過後 commit
4. 計畫拆成多個 wave，獨立 wave 平行執行
5. 每個 wave 完成用 **Playwright 自動測試**驗證（腳本用完即刪）
6. Summary + 驗證指引等人工批准，再進下一 phase

### 執行模式

一行指令驅動整個里程碑：

```bash
gsd
/gsd auto
```

- **Auto mode**：給計劃後走開，完全自動執行
- **Step mode**：手動、更有掌控感
- 兩種模式都支援 token budget ceiling

## 安裝與設定

```bash
# GSD-2（最新，standalone CLI）
npm install -g gsd-pi@latest

# 啟動設定精靈
gsd
```

設定精靈支援：
- **Claude Max OAuth**：一鍵登入（技術上支援，但見下方費用警告）
- **API key**：Anthropic Console、OpenAI、Google、OpenRouter，合計 20+ providers

建議開兩個 terminal：
- Terminal 1：`gsd auto`（實際執行工作）
- Terminal 2：討論 terminal（隨時補充指令，GSD 從磁碟讀取）

> 參考：舊版 `get-shit-done` 安裝用 `npx get-shit-done-cc@latest`，是注入 Claude Code 的 prompt framework，不是 CLI。

## 費用警告（重要）

GSD-2 技術上支援 Max plan OAuth，**但使用違反 Anthropic 官方 ToS**：

> Anthropic 明確規定 Claude Free/Pro/Max OAuth 認證**僅限 Claude Code 與 Claude.ai 使用**；第三方工具（包含 GSD-2）需用 API key 認證。此禁令已於 **2026-04-04 正式執行**，並非只針對 GSD，是跨所有第三方 Claude 工具的政策。

換算成本：$200 Max plan ≈ **$2,500–$5,000 API credits**，在 GSD 裡用 API 直接燒錢。

社群實測（個人記帳 web app，Claude Code 原生 vs GSD-2）：

| 指標 | Claude Code 原生 | GSD-2 |
|------|------------------|-------|
| 時間 | 4 分 38 秒 | 約 1.5 小時（含卡頓） |
| 費用 | < 1% 的 5 小時 Max 用量 | **~$27.20 API 費用** |
| 視覺效果 | 較佳 | 較差 |
| 功能完整性 | 達標 | 達標 |

GSD-2 執行中多次卡住（17 分鐘、40 分鐘停頓，需重啟）。

## 在三框架中的位置

| 面向 | GSD | Superpowers | GStack |
|------|-----|-------------|--------|
| 約束目標 | 環境（每 task fresh context） | 流程（TDD） | 視角（多 persona） |
| 擅長階段 | 專案管理、里程碑切分 | 實作 TDD | 策略規劃、QA |
| 文件產出量 | 大量 | 中 | 集中於 design doc |
| Token 效率 | **較差** | 較好 | 中 |

詳細對比見 [[Superpowers框架]]、[[GStack框架]]。

與 **BMAD Method** 的比較：BMAD 適合需求鎖定、全面前期研究（Business Analyst / Design Thinker 等角色出發，生成 PRD 再拆 sharded tasks）。GSD 適合需求不確定、需大量實驗。BMAD 對需求變更容忍度低。

## 何時該用

- **適合**：需求不確定、要大量實驗；從未做過的客製化解法；MVP 快速打造；需要文件化決策累積給未來 session；純 API 或 OpenRouter 使用者
- **不適合**：簡單小型 app（overkill）；Max plan 訂戶（違反 ToS）；短時程、成本敏感的專案；需求鎖定且要求嚴謹文件（該用 BMAD）

**Anthropic Harness 指南觀點**（社群整理）：Opus 4.5+ 之後 Claude 已內建足夠強的 planner-generator-evaluator 迴圈，GSD 填補的 context 焦慮問題縮小；若要用 GSD，可考慮**替換其 evaluator 為 Anthropic 的 graded evaluation 評分機制**（design quality / originality / craft / functionality 四維度）強化品質關卡。

## 常見陷阱

**Token 爆炸**
- 徵兆：規劃階段就燒掉 600K+ tokens
- 原因：四個平行 researcher sub-agent（stack / features / architecture / pitfalls）各自用 33K–75K tokens 再合成
- 解法：小專案不啟動 GSD；啟動時先設 token budget ceiling

**卡住不前**
- 徵兆：auto mode 長時間停頓（社群實測 17 分鐘、40 分鐘）
- 原因：sub-agent 進入無效迴圈
- 解法：GSD-2 內建 stuck detection 會主動告警；或完全重啟 session；設 token budget ceiling 避免無限燒

**文件太多 agent 迷路**
- 徵兆：sub-agent 忽略 project.md 中的 out-of-scope
- 原因：planning 文件冗長
- 解法：GSD 本身已強調 project.md 保持精簡；人工檢查文件長度

**Max plan OAuth 誤用**
- 徵兆：帳號收到警告、訂閱被中止（2026-04-04 後）
- 原因：Anthropic ToS 明確禁止第三方工具使用 Claude OAuth
- 解法：GSD 一律用 API key，不要借用 Max plan OAuth token

## 來源

**官方 / 開發者**
- [gsd-build/gsd-2 (GitHub)](https://github.com/gsd-build/gsd-2) — GSD-2，standalone CLI
- [gsd-build/get-shit-done (GitHub)](https://github.com/gsd-build/get-shit-done) — v1 prompt framework，仍在維護
- [Anthropic Legal & Compliance — Claude Code Docs](https://code.claude.com/docs/en/legal-and-compliance)

**影片 / 社群**
- https://www.youtube.com/watch?v=ZgfybHGxzJU
- https://www.youtube.com/watch?v=uEit1oOJK0w
- https://www.youtube.com/watch?v=GJmlik1C4Tg
- https://www.youtube.com/watch?v=celLbDMGy8w
- https://www.youtube.com/watch?v=bzutStZJ1Ig
- https://www.youtube.com/watch?v=nBH07G-zayk
