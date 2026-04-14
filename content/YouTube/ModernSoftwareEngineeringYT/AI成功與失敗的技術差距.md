---
title: AI 成功與失敗之間的技術差距是什麼？
tags:
  - youtube
  - software-engineering
created: 2026-04-14
updated: 2026-04-14
published: 2026-03-06
source: https://www.youtube.com/watch?v=ekRMQ5qUMlo
---

## 核心命題：沒有技術基礎能靠 AI 成功嗎？

Dave Farley 與 Steve Smith 的回答直接：**不行**。

例外情況：個人用途（整理 NAS 相片庫、bash 腳本）或一次性工作，可以在低技術基礎下用 AI 完成，因為不需要長期維護與演進。

## 個人用途 vs 企業級軟體開發的根本差異

- **Vibe coding**（直覺式 AI 編碼）適合一次性個人問題、快速原型
- 企業組織面對的是持續演進的複雜系統，需要嚴格紀律管理變更
- 問題不在於「能不能跑起來」，而在於「能不能長期安全演進」

精實創業場景：用 AI 快速建出 MVP 收集早期回饋是合理的，但後續仍需正式工程實踐接手。

## AI 效果的關鍵：能偷師多少過去的範例

AI 的能力高度依賴訓練資料的覆蓋程度：

- **效果好**：Java、通用 Web 應用（大量開源範例）
- **效果差**：Terraform、Gradle、企業內部框架（少有公開高品質範例）
- 核心洞見：越是公司獨有的技術棧，AI 越難產生高品質輸出；越接近通用技術棧，AI 越有效

## 強技術基礎讓 AI 發揮的案例

以 Elmax 交易所為例：

- 交易報告閘道（Trade Reporting Gateway）等低複雜度服務，可由 AI 完全重新生成
- 前提：該組織有嚴格的技術標準、CI/CD pipeline、Coding patterns，可作為 AI 的訓練上下文
- 關鍵結論：**AI 成果的品質 = 組織技術基礎的品質的映射**

英國政府案例：
- 有 gov.uk 設計手冊（設計系統）+ 強大 platform engineering + 結構化業務問題
- 成果：從政策文件到可上線的數位服務，以週計而非月計
- 但這個速度是建立在數年累積的建構區塊之上

## 最關鍵的技術基礎清單

### 1. 規格明確化（Specification of intent）
- 清楚定義「想要什麼」是最重要的能力
- 可執行的驗收測試（executable acceptance tests）= 可直接餵給 AI 驗證的規格

### 2. 自動化驗證（Verification）
- 約束不再是「敲程式碼的速度」，而是「驗證輸出是否符合預期」
- 有測試套件才能安全接受或拒絕 AI 生成的程式碼

### 3. 架構決策記錄（Architecture Decision Records, ADR）
- 以 Markdown 形式維護，並用掃描工具檢查各服務是否符合
- 不是「稽核」而是「為何你做了不同選擇？」的對話起點
- 可以直接作為 AI 的 context 餵入

### 4. Coding Standards 與 Domain Model
- 不需要龐大文件，只需清楚的命名規則、domain model 邊界
- Domain model 理想上由業務人員擁有並維護（如 Elmax 的 BA 控制 domain model）
- 這些知識現在可用 Markdown 表達，直接餵給 AI

### 5. 強大的 Platform Engineering
- 快速回饋的交付 pipeline
- 標準化服務架構降低 AI 需要「發明」的部分

## 團隊協作的挑戰

Gen AI 工具目前主要是個人工具，但最有效的交付單位是團隊：

- 不同人使用 AI 的方式差異極大，難以標準化
- Pair programming + AI（兩個人類 + AI）或 Mob programming + AI（AI 擔任打字員）是可行的嘗試
- 需要「共享的 AI 使用方式」，類似於過去的共享開發規範

## 推薦工具

**Nwave（nwave.ai）**：開源工具，引導你完成從問題設定、架構決策、設計決策到實作的完整流程，內建 ADR 輸出與可執行規格，鼓勵 TDD
