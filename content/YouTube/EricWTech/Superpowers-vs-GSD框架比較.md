---
title: Superpowers vs. GSD：端對端測試框架比較
tags:
  - youtube
created: 2026-04-16
updated: 2026-04-16
published: 2026-04-15
source: https://www.youtube.com/watch?v=GJmlik1C4Tg
---

## 測試情境設定

作者在同一個 brownfield 專案（食品訂購系統）上，同時使用 Superpowers 與 GSD 兩個 spec driven development 框架，目標是新增端對端測試覆蓋率。

- 使用 G Stack 撰寫需求規格文件
- 透過 Git worktree 將專案分成兩個獨立環境，各自執行不同框架
- 評估指標：測試準確度、token 消耗量、程式碼品質

## Superpowers 執行方式

- 使用內建 Git worktree skill 建立隔離環境
- 採用測試驅動開發（TDD）：先寫測試，再實作
- 使用 dispatch parallel agent 平行執行實作
- 包含驗證（verification）與程式碼審查階段
- 整體流程走完只需一輪 fix cycle

**Superpowers 測試結果：**
- 總計 107 個測試（103 通過，4 個設計跳過）
- 整體功能覆蓋率：46%（94 個功能中涵蓋 43 個）
- 各頁面覆蓋率：customers 頁 90%、orders 頁 78%
- 過程中發現並修復約 10 個 bug

## GSD 執行方式

GSD 的設計目標是讓每個 Claude Code session 的 context window 使用率不超過 50%，因此拆成多個 session 執行（步驟 0 到步驟 9）：

1. 建立 Git worktree（借用 Superpowers 的 skill）
2. 初始化 GSD 專案，設定一個 milestone、一個 phase
3. 規劃階段（plan phase）：拆成兩個計劃——基礎設施（infrastructure）與關鍵路徑測試（critical path tests）
4. 分別用不同 sub agent 執行兩個計劃
5. 新開 session 進行程式碼審查（code review）
6. 自動修復（auto fix）與驗證（validation）
7. 安全稽核（security audit）
8. 提取學習（extract learning）：擷取此次開發的決策、模式與教訓，供未來 session 參考

GSD 的 extract learning skill 特別強調知識累積，可讓後續 session 做出更明智的決策。

**GSD 測試結果：**
- 總計 110 個測試（102 通過，8 個跳過），執行時間約 2 分鐘
- 整體功能覆蓋率：53%（比 Superpowers 高 7%）
- 各頁面覆蓋率：login 100%、customers 90%、orders 80%
- 過程中修復 4 個 bug
- 共約 16 個 commits，大量規劃與文件產出

## 最終評分比較

| 評估項目 | Superpowers | GSD |
|---------|------------|-----|
| 測試準確度 | 9/10（通過率較高） | 8/10 |
| Token 效率 | 勝出（比 GSD 省 5~7 倍） | 較高消耗 |
| 程式碼品質 | 普通 | 較佳（有 code review、UAT、security） |
| 可維護性 | 勝出（git history 乾淨） | 較多 noise |
| 迭代次數 | 1 次 fix cycle | 2 次 fix cycle |
| Token 分配 | 實作 60-70%、修復 20-30%、審查 10% | 僅 25% 用於實作，其餘用於規劃/驗證 |

**Token 消耗說明：**
- Superpowers：5 倍以上效率優勢，以更少 token 達成相近結果
- GSD：大量 token 花在研究、規劃、品質關卡（quality gates）

## 總結

- **準確度**：基本持平，各有優勢（Superpowers 選用本地資料庫替代遠端，測試數字略佳；GSD 安全性與 UAT 更完整）
- **Token 效率**：Superpowers 明顯勝出
- **文件品質**：GSD 產出更豐富的規劃產物與學習文件
- **適用情境**：需要快速交付、成本敏感的專案選 Superpowers；重視品質關卡、長期可維護性的大型專案可考慮 GSD
