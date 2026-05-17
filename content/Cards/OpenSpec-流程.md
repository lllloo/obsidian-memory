---
title: OpenSpec 流程
created: 2026-05-16
updated: 2026-05-17
source: https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md
tags:
  - claude-code
  - agent-framework
  - workflow
---

OpenSpec 是 Fission-AI 出品的輕量 spec 框架（npm）。OPSX 是目前的標準工作流，設計哲學是「Actions not phases」：artifact 之間有相依但沒有 phase gate，任何時候都可以回頭修改任何 artifact。支援 25+ AI coding agents。

## 核心節點

| 代號 | 指令 | Profile | 動作 | 輸出 / 備註 |
| ---- | ---- | ------- | ---- | ----------- |
| `EX` | `/opsx:explore` | core | 發散思考，釐清需求與選項 | 無固定輸出；propose 前用 |
| `PR` | `/opsx:propose` | core ⭐ | 一步建立完整 change | proposal + specs + design + tasks |
| `AP` | `/opsx:apply` | core ⭐ | 依 tasks.md 執行實作 | 過程可隨時更新 artifact |
| `SY` | `/opsx:sync` | core ⭐ | 同步 delta specs 進主規格 | archive 執行時亦會提示 |
| `AR` | `/opsx:archive` | core ⭐ | 合併 delta specs 並封存 change | change 移至 `changes/archive/` |
| `NW` | `/opsx:new` | expanded ⭐ | 建立 change scaffold（只搭架） | — |
| `CT` | `/opsx:continue` | expanded ⭐ | 依相依圖逐步建立下一個 artifact | 與 `FF` 擇一；每次一個 |
| `FF` | `/opsx:ff` | expanded ⭐ | 一次產出所有 planning artifacts | 與 `CT` 擇一；目標清楚時用 |
| `VF` | `/opsx:verify` | expanded ⭐ | 對照 specs 驗收實作 | — |
| `BA` | `/opsx:bulk-archive` | expanded | 批次封存多個 changes | — |
| `ON` | `/opsx:onboard` | expanded | 引導走完整一次 OPSX 流程（end-to-end walkthrough） | — |

Expanded profile 需 `openspec config profile` 啟用，再跑 `openspec update`。

## 整體流向

```mermaid
flowchart TD
    Start([開始]) --> EX["/opsx:explore<br/>發散思考（選填）"]
    Start --> PR
    EX --> PR["/opsx:propose ⭐<br/>建立完整 change"]
    PR --> AP1["/opsx:apply ⭐<br/>執行實作"]
    AP1 --> SY["/opsx:sync ⭐"]
    SY --> AR1["/opsx:archive ⭐"]
    AR1 --> Done([完成])

    Start2([開始 · Expanded]) --> NW["/opsx:new ⭐<br/>建立 scaffold"]
    NW --> FFCT["/opsx:ff ⭐ 或 /opsx:continue ⭐<br/>產出 planning artifacts"]
    FFCT --> AP2["/opsx:apply ⭐<br/>執行實作"]
    AP2 --> VF["/opsx:verify ⭐<br/>驗收"]
    VF --> AR2["/opsx:archive ⭐"]
    AR2 --> Done
```

## Artifact 相依圖

specs 與 design 平行產出（都只依賴 proposal），tasks 需兩者完成才能建立：

```mermaid
flowchart LR
    P[proposal.md] --> S["specs/&lt;domain&gt;/spec.md"]
    P --> D[design.md]
    S --> T[tasks.md]
    D --> T
    T --> AP["/opsx:apply"]
```

## 關鍵規則

- **Actions not phases**：沒有強制 phase gate，`AP` 中發現設計錯誤直接改 design.md 再繼續
- **EX before PR**：idea 模糊先跑 `EX`；目標清楚直接跑 `PR`
- **FF vs CT**：知道要做什麼用 `FF` 一次產出；還在探索用 `CT` 逐步推進
- **Delta not full rewrite**：specs 只記「這次改了什麼」（ADDED / MODIFIED / REMOVED），archive 時才合併進主規格
- **Update vs New change**：同目標、微調執行 → 更新既有 change；意圖根本改變或 scope 爆增 → 開新 change

## 相關

- [[Spec-Kit-流程]] — 類似 SDD 工具，GitHub 出品，phase 更嚴格
- [[GSD-流程]] — 輕量 spec-driven workflow
- [Fission-AI/OpenSpec](https://github.com/Fission-AI/OpenSpec)


## 版本注意（v1.3.1）

- 安裝：`npm install -g @fission-ai/openspec`（目前最新 v1.3.1）
- **`/opsx:sync` 尚未在 v1.3.1 release**：GitHub 文件已記載為 core workflow 的一部分，但 npm 實際版本不含此 skill；`openspec config list` 可驗證
- Core workflow 實際可用指令：`propose → explore → apply → archive`（sync 暫缺）
- 目前若需同步 delta specs，直接在 `/opsx:archive` 時一併處理

## Core Profile 實際指令清單（v1.3.1 確認）

Core profile（預設）只有 4 個 skill，**`/opsx:sync` 不在其中**：

| 指令 | 說明 |
| ---- | ---- |
| `/opsx:propose` | 建立變更並生成所有規劃 artifacts |
| `/opsx:explore` | 探索想法與需求 |
| `/opsx:apply` | 實作 tasks |
| `/opsx:archive` | 歸檔完成的變更 |

`/opsx:sync` 被視為可選進階指令：`archive` 執行時若偵測到未 sync 的 delta specs，會主動詢問是否執行 sync，因此不強制放在 core。