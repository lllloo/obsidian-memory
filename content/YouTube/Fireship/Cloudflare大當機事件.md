---
title: Cloudflare 大當機事件
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-11-19
source: https://www.youtube.com/watch?v=tF_4baiIUiQ
---

## 事件概要

- 2025 年第三次大規模網路中斷（前兩次分別是 AWS 和 Azure）
- **Cloudflare** 全球網路在東部時間早上 6 點開始出現「internal service degradation」
- 受影響服務：X（Twitter）、ChatGPT、Down Detector 本身，以及 League of Legends

## 根本原因

Cloudflare CTO 說明：

> 「一個潛伏的 bug 在我們的 bot mitigation（機器人防護）服務中，在一次例行設定變更後開始崩潰，並連鎖降級整個網路。這不是攻擊事件。」

**更具體的原因：**
- 自動生成用來管理威脅流量的設定檔
- 該設定檔的 entry 數量超過預期上限
- 觸發負責處理大量 Cloudflare 服務流量的軟體系統崩潰
- **原本設計來保護網路的防護機制，因為過度膨脹造成比任何駭客都大的破壞**

## 深層問題

- 網路並非完全去中心化的中立平台
- 現實是少數**巨型中心化基礎設施供應商**掌控一切
- 任何一個倒下，損害都是大規模的

## 啟示

- Cloudflare 狀態頁因為過於精簡（只剩基本 HTML）反而撐住了，作者調侃「可能是架在 Vercel 上」
- 系統設計應避免單點故障，關鍵設定文件要有大小限制防護
