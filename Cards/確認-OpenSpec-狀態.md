---
title: 確認 OpenSpec 狀態
created: 2026-05-21
updated: 2026-05-21
tags:
  - openspec
  - workflow
  - debugging
---

OpenSpec 提供三個指令確認當前 specs / changes 狀態，分工不同——搞混就會卡在錯的訊息上。

## 三指令分工

| 指令 | 看什麼 | 何時用 |
|---|---|---|
| `openspec view` | dashboard 總覽 | 第一眼掃過，看 specs / changes 總量與 0 requirements 異常 |
| `openspec list --specs` | 每份 spec 的 requirements 數量 | 確認**哪一份** spec 壞掉 |
| `openspec validate <name> --type spec --strict` | 真正的錯誤訊息 | 確認**為什麼**壞 |

排查順序：**dashboard 警覺 → list 確認哪份壞 → validate 看為什麼**。

## 關鍵心智

`requirements 0` 是**警訊**，不是「真的沒寫」。spec.md 內明明有 `### Requirement:` 區塊但 list 顯示 0，幾乎可以斷定 parser 解析失敗——下一步直接跑 `validate`。

常見原因：spec.md 缺 `## Purpose` heading。parser 不容錯，少這個 heading 就放棄整份 spec，後面所有 requirement 都當沒看到。

## 修法

在 spec.md 的 `## Requirements` 前補：

```markdown
## Purpose

<一句話描述這個 capability 做什麼>
```

CLI 沒有自動補 Purpose 的指令（Purpose 是需求陳述，CLI 不會幫你猜）。修完跑 `openspec validate --specs --strict`，應全綠。

## 為什麼會壞

`openspec archive` 把 delta spec 合併進主 spec 那步是 AI subagent 跑的，不是 deterministic CLI 邏輯。歷史上 agent 會漏寫 `## Purpose`，舊 archive 的 spec 在 v1.3.x 較嚴的 validator 下集體不合規。
