---
title: 確認 OpenSpec 狀態
created: 2026-05-21
updated: 2026-06-02
tags:
  - claude-code
  - agent-framework
  - workflow
  - debugging
---

OpenSpec 提供幾個指令確認當前 specs / changes 狀態，分工不同——搞混就會卡在錯的訊息上。

## 指令分工

| 指令                                    | 看什麼                       | 何時用                                                |
| ------------------------------------- | ------------------------- | -------------------------------------------------- |
| `openspec view`                       | dashboard 總覽              | 第一眼掃過，看 specs / changes 總量與 0 requirements 異常      |
| `openspec list`                       | active changes 清單         | 看目前進行中的 change proposals                           |
| `openspec list --specs`               | 每份 spec 的 requirements 數量 | 確認**哪一份** spec 壞掉                                  |
| `openspec validate --all --strict`    | 全部 specs / changes 整批驗    | 「全綠才安心」的最終把關                                       |
| `openspec validate <name> --strict`   | 單一目標的錯誤訊息                 | 單點除錯（`--type` 可省，CLI 會自動判別 spec 還是 change）         |

排查順序：**dashboard 警覺 → `list --specs` 確認哪份壞 → `validate <name>` 看為什麼 → `validate --all` 收尾**。

## 關鍵心智

`requirements 0` 是**警訊**，不是「真的沒寫」。spec.md 內明明有 `### Requirement:` 區塊但 list 顯示 0，幾乎可以斷定 parser 解析失敗——下一步直接跑 `validate`。

常見原因：spec.md 缺 `## Purpose` heading。parser 不容錯，少這個 heading 就放棄整份 spec，後面所有 requirement 都當沒看到。

## 修法

在 spec.md 的 `## Requirements` 前補：

```markdown
## Purpose

<一句話描述這個 capability 做什麼>
```

CLI 沒有自動補 Purpose 的指令（Purpose 是需求陳述，CLI 不會幫你猜）。修完跑 `openspec validate --all --strict`，應全綠。
