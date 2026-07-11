---
title: OKF 與本 vault 的相容性
description: Open Knowledge Format 對本 vault 的適用邊界：內部維持 Obsidian LLM Wiki，未來需要交換時再建立 OKF 匯出層
created: 2026-07-11
updated: 2026-07-11
source: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
parent: "[[wiki/01.index]]"
tags:
  - wiki
  - knowledge-graph
  - obsidian
---

# OKF 與本 vault 的相容性

[Open Knowledge Format（OKF）0.1 草案](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) 定義可供人與 agent 讀寫、交換的 Markdown 知識 bundle。它與本 vault 的 [[LLM-Wiki-知識管理模式]] 在 Markdown、YAML frontmatter、Git、索引與交叉連結上方向一致；但它面向跨組織的知識目錄交換，不是持續綜合原始來源的私有 LLM Wiki。

## 對照

| OKF 慣例 | 本 vault 現況 | 判斷 |
|---|---|---|
| `title`、`description`、`tags` | 已採用 | 保留 |
| directory index 供漸進揭露 | `wiki/01.index.md` | 保留；不改為保留檔名 `index.md` |
| 標準 Markdown links | 內部以 Obsidian wikilink 為主 | 只在未來匯出時轉換 |
| 每個 concept 必填 `type` | 以摘要、實體、概念、比較、綜合頁作慣例分類，未寫入 frontmatter | 現階段不補，避免沒有消費者的維護成本 |
| `timestamp`（ISO 8601 datetime） | `updated`（日期） | 匯出時映射，不改內部 schema |
| `# Citations` | 主來源放 frontmatter `source`，多來源可就地連結 | 重要外部主張可採用，非全庫遷移條件 |

## 決定（2026-07-11）

**不將 `wiki/` 遷移為 OKF bundle，也不全面加入 `type` 或雙寫連結。** 現有結構服務 Obsidian 圖譜、raw write-once 證據鏈與 agent 綜合流程，直接套用 OKF 的互通性成本目前沒有明確受益者。

**保留 OKF 作為未來的匯出 profile。** 若需要讓外部 agent、工具或組織消費選定知識時，另建獨立 bundle：映射既有 `title`、`description`、`tags`、`updated`，補 `type`，將 wikilink 轉成 bundle-relative Markdown links，並保留來源 citation。這不改動內部 wiki，也不影響 [[LLM-Wiki-生態實作比較]] 已拍板的不採 nvk 雙連結決定。

## 重新評估條件

- 要公開或交付一組 wiki 知識給非 Obsidian 消費者。
- 外部 agent 或工具要求可驗證的標準 bundle。
- OKF 結束 draft，且出現實際的消費工具或交換案例。

## Citations

[1] [Open Knowledge Format Specification v0.1 Draft](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
