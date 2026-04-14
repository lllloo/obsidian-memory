---
title: Ageless Linux 反作業系統年齡驗證法
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-03-20
source: https://www.youtube.com/watch?v=nkY_s9HpL9M
---

## 背景：OS 層級年齡驗證法

2025 年 10 月，加州通過 **Digital Age Assurance Act（AB 1043）**，規定：

- 2027 年 1 月 1 日起，所有通用作業系統（Windows、macOS、Android、Linux）必須在帳號建立時收集使用者年齡
- 必須提供 API，讓開發者查詢使用者年齡作為 app/網站的存取控制依據
- 加州所有議員一致投票通過，理由是「保護兒童」

## 實際影響分析

表面理由「保護兒童」，但家長控制已是解決好的問題；真正的最終目標被認為是：

- 將每台設備綁定登入身分（Apple、Facebook、Google 帳號）
- 所有網路行為預設可被追蹤 → **大規模監控基礎設施**
- 對大型科技公司有利（Meta 花費數百萬遊說通過此法，OpenAI 共同贊助），對小型開發者造成合規負擔

Microsoft 與 Apple 作為間接受益者保持旁觀，Linux 社群大多沈默。

## Ageless Linux 的反制

**Ageless Linux** 不是真正的 Linux 發行版，而是一個針對 Debian 系（Ubuntu、Kali）的腳本，明確宣示不遵守 AB 1043：

```bash
# 在任何 Debian-based 系統上執行此腳本
# 腳本會：
# 1. 修改 OS release metadata
# 2. 安裝聲明文件（告知加州政府「我們不遵守」）
# 3. 部署一個刻意無效的年齡驗證 API
```

執行後你在法律上成為「作業系統提供者」，若加州兒童使用你的系統且你未提供有效年齡收集介面，可被罰款每名兒童 $7,500。

## 法律困境

這個腳本是公然違法設計——違反法律本身就違法。作者 John McCardle 在影片留言區現身說明，表示將持續記錄所有被加入 Linux 的年齡驗證合規措施，並提供逆向工具。
