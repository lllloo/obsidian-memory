---
title: Approval Test 與 Acceptance Test 的差異
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-20
source: https://www.youtube.com/watch?v=n5vzuQAToZE
---

Kent Beck 與 Emily Bache 的對話，釐清兩種測試術語的區別。

## 核心定義

**Acceptance Test（驗收測試）**
- 從客戶或使用者角度驗證軟體是否被接受
- 通用術語，存在超過 25 年
- 幾乎所有開發者都做過某種形式的驗收測試

**Approval Test（核准測試）**
- 由 Emily Bache 推廣的特定技術，2012 年才開始叫這個名字
- 舊稱：golden master testing、snapshot testing、text-based testing
- 流程：Arrange → Act → **Print → Diff**（取代傳統 Assert）
- 將輸出結果與先前「核准過的版本」進行 diff 比對

## 三狀態輸出 vs 二狀態輸出

傳統單元測試：**紅 / 綠**（Pass / Fail，二值）

Approval Test：**三種狀態**
1. 無差異 → 系統正常
2. 有差異，但屬預期內的變更 → 按下「Approve」更新基準
3. 有差異，是真正的 bug → 需修正

這個「可更新」特性使 Approval Test 在行為合法改變時非常方便——按一下 Approve 即可讓所有相關測試變綠。

## 適用格式

- PDF、HTML（建議先轉成純文字再比對）
- GUI widget 序列化為字串後的樹狀結構
- Android 截圖（像素差異）
- 任何能轉成可 diff 文字的輸出

## 主要優勢

- **高診斷性（Diagnosability）**：測試失敗時提供完整 diff，能看到哪些地方相同、哪些不同
- 行為合法變更時，更新測試比修改 assertion 容易得多

## 主要風險

- **壓力下容易誤 Approve**：看到 100 個失敗，可能在確認不充分的情況下全部 Approve
- 長期維護成本較高：無法像單元測試那樣「綠燈就等於沒問題」

**應對方式**：使用成熟的 Approval Testing 框架（不要自己造輪子），讓工具幫助：
- 偵測 Approve 的內容中是否含 stack trace
- 將多個失敗分群，確保你至少逐群檢查一個案例

## 與 Golden Master / Snapshot Testing 的區別

| 術語 | 含意問題 |
|------|---------|
| Golden Master | 暗示基準版本「黃金不可動」，但 Approval Test 的基準是經常更新的 |
| Snapshot Testing | 暗示「拍個快照，不在乎內容」，但 Approval Test 要求開發者明確審視並核准 |

Approval Testing 的關鍵是：**你必須主動看過並核准**，而不是自動記錄然後忽略。

## AI 對 Approval Testing 的影響

Kent Beck 認為 AI 天生擅長文字比對與詮釋，有潛力協助解讀 Approval Test 的失敗原因。但 2026 年初仍屬早期，建議積極實驗。
