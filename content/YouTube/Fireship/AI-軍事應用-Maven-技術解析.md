---
title: AI 軍事應用：Maven Smart System 技術解析
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-03-24
source: https://www.youtube.com/watch?v=nxwkn9Dt9-I
---

## 背景

美國國防部宣布全面採用 **Maven Smart System**，這套 AI 平台將部署至陸、海、空、陸戰隊及太空軍，核心功能是「縮短殺傷鏈（kill chain）」——用 AI 加速目標識別與決策流程。目前人類仍需在迴路中按下最終確認，但系統設計趨向自動化。

主要供應商：
- **Palantir**（Alex Karp）：提供核心作業系統平台
- **AWS / Azure**：雲端基礎設施
- **Anduril**（Palmer Luckey）：提供 Ghost 無人機、Anvil 攔截器、Ghost Shark 水下無人機等硬體
- Google 曾參與，後因員工抗議退出

## 系統技術架構（開源重現版）

雖然正式技術棧屬於機密，但可用開源工具重建類似系統：

### 1. 資料攝取層
- 使用 **Apache Kafka** 串流整合多種資料來源：無人機影像、特種部隊通訊、衛星 GPS 等
- Kafka 讓整個系統能即時更新

### 2. 資料處理層
- **Apache Spark** 訂閱 Kafka topic，對資料進行轉換
- 無人機影像送進 **OpenCV** 進行物件偵測與分割

### 3. 語意理解層（Palantir 的核心秘密）
- **Ontology（本體論）**：將不同來源的混亂資料映射為統一結構，捕捉物件間的元資料與關聯性
- 相當於整個組織（或戰場）的數位孿生

### 4. 關係資料庫
- 使用**圖資料庫（如 Neo4j）**而非關聯式資料庫
- 人員、車輛、武器成為節點，行動軌跡成為邊，還原真實世界的關聯

### 5. 政策管控層
- **Open Policy Agent**：在整個堆疊中強制執行作戰規則

### 6. AI 代理層
- 透過 **Model Context Protocol** 接入 AI agents
- 可使用開源 LLM（如 Kimi、Qwen），並以 Heretic 去除審查限制

## 現況

Anthropic Claude 曾是 Maven 系統的主力 LLM，後來 Anthropic 拒絕軍事用途，被排除出政府合約；OpenAI 接手填補。
