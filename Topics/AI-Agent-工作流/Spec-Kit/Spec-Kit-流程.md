---
title: Spec Kit 流程
created: 2026-05-16
updated: 2026-05-29
source: https://github.com/github/spec-kit
tags:
  - claude-code
  - agent-framework
  - workflow
---

Spec Kit 是 GitHub 出品的 Spec-Driven Development（SDD）工具組。核心哲學：先寫可執行規格，再產出實作，而非先碼後補文件。支援 30+ AI coding agents。

## 指令命名兩種形式

依安裝模式不同，同一個指令有兩種寫法：

- **Slash command mode（預設）**：`/speckit.constitution`（dot 形式）
- **Skills mode**（`--integration-options="--skills"`）：`/speckit-constitution`（dash 形式）
- **Codex CLI**：`$speckit-*`；**Gemini**：`/speckit:*`

本筆記以 dot 形式為主；agent 端實際顯示可能是 dash，對應同一個指令。

## 指令一覽

| 代號 | 指令 | 必填 | 動作 |
| ---- | ---- | ---- | ---- |
| `CO` | `/speckit.constitution` | ⭐ | 建立專案治理原則 |
| `SP` | `/speckit.specify` | ⭐ | 描述要做什麼（what & why，不談 tech stack） |
| `CL` | `/speckit.clarify` | — | 結構化釐清規格灰區（PL 前強烈建議） |
| `PL` | `/speckit.plan` | ⭐ | 給定 tech stack → 生成技術實作計畫 |
| `CH` | `/speckit.checklist` | — | 生成自訂品質清單，驗需求完整性與一致性 |
| `TK` | `/speckit.tasks` | ⭐ | 生成任務清單（含相依排序與平行標記 `[P]`） |
| `AN` | `/speckit.analyze` | — | 跨 artifact 一致性與覆蓋分析（TK 後、IM 前） |
| `TI` | `/speckit.taskstoissues` | — | 把 tasks.md 轉為 GitHub Issues |
| `IM` | `/speckit.implement` | ⭐ | 執行所有任務 |

## 整體流向

```mermaid
flowchart TD
    Start([開始]) --> CO["/speckit.constitution<br/>治理原則"]
    CO --> SP["/speckit.specify<br/>描述需求（what & why）"]
    SP --> CL["/speckit.clarify<br/>釐清規格（強烈建議）"]
    CL --> PL["/speckit.plan<br/>指定 tech stack → 技術計畫"]
    PL --> Validate["人工審核計畫"]
    Validate --> TK["/speckit.tasks<br/>生成任務清單"]
    TK --> AN["/speckit.analyze（選填）"]
    AN --> IM["/speckit.implement<br/>執行所有任務"]
    IM --> Done([完成])
    CL -. 明確跳過 .-> PL
    AN -. 選填 .-> IM
```

## 關鍵規則

- **Spec first**：`SP` 只描述 what & why，tech stack 留到 `PL` 才給
- **Clarify before plan**：`CL` 在 `PL` 前跑，明確跳過需向 agent 陳述意圖
- **Validate before implement**：`PL` 後人工審核計畫再跑 `TK`，避免過度設計
- **Constitution 是地基**：`CO` 的治理原則貫穿所有後續階段

## specify init 工作流擴充

跑 `specify init` 會安裝擴充到 `.specify/extensions/<name>/`，並在 agent 端註冊額外 `speckit-<extension>-<verb>` 指令。安裝紀錄寫在 `.specify/init-options.json`。

**git 擴充預設啟用**：目前 `specify init` 會自動裝 git 擴充（一組 `speckit-git-*` 指令），**不問**。官方規劃後續版本改成明確 opt-in，需 init 後手動 `specify extension add git`——確切切換版本以官方 release notes 為準。

事後管理：

- 加裝：`specify extension add <name>`
- 移除：`specify extension remove <name>`，slash commands 一併撤掉

若 agent 端跳出非預期的 `speckit-*` 指令，先看 `.specify/extensions/` 與 `.specify/init-options.json` 對帳。

## 何時不該用 / 長期風險

社群普遍認同「先講清楚再寫」方向正確，但多數團隊仍小規模試用觀望，等工具與底層模型更成熟。

保留意見：

- **規格完美 ≠ 產出穩定**：花大量心力寫完美規格，AI 產出的 code 品質仍不一定穩。
- **小專案太重**：需快速迭代的小型專案，整套立法式流程（constitution → specify → plan → tasks → implement）顯得過重。

長期風險：

- **依賴外部模型穩定性**：底層模型行為一變，整個 workflow 可能失效。
- **prompt template 脆弱**：核心邏輯深植提示範本，維護它與 30+ agent 的相容性是長期負擔。
- **失去掌控感**：`/speckit.implement` 這類高抽象指令可能讓開發者對最終 code 失去掌控、不利技能成長。

本質上 spec-kit 是在賭：結構化開發流程的價值，會不會比單純追求更強的模型更高。

## 相關

- [[bookmark-Spec-Kit-Spec驅動開發框架|Spec Kit]] — 概念定位與來源
- [[BMAD-Method-流程]] — agentic agile workflow，phase 更完整
- [github/spec-kit](https://github.com/github/spec-kit)
