---
title: Axios npm 供應鏈 RAT 攻擊事件
tags:
  - youtube
created: 2026-04-14
updated: 2026-04-14
published: 2026-03-31
source: https://www.youtube.com/watch?v=o7NYXvYohYk
---

## 事件概況

2026 年 3 月底，npm 上的 Axios（每週超過 1 億次下載）被植入兩個惡意版本，包含精心設計的供應鏈攻擊，可危害開發者機器與 CI/CD 伺服器。

- Axios 本身原始碼零問題，攻擊者透過注入惡意依賴套件發動攻擊
- 惡意版本在 npm 以 Proton Mail 信箱發布（正常版本走 GitHub Actions）
- 推測攻擊者取得了維護者的 npm access token

## 確認是否中招

1. 檢查 `package.json` 是否安裝了受影響的 Axios 版本
2. 進入 `node_modules`，確認是否存在 `plain-crypto-js` 套件
3. 若存在，執行以下指令（Mac/Windows/Linux 各有對應命令）確認 RAT 是否已落地：

```bash
# 依平台執行對應的 RAT 檢測指令（參考 Step Security 指南）
```

## 攻擊技術細節

攻擊流程（RAT Dropper 機制）：

1. **植入惡意依賴**：攻擊者在合法的 `plain-crypto-js`（偽裝成 cryptojs）中加入 `postinstall` 腳本
2. **偵測系統環境**：腳本判斷受害者作業系統
3. **拉取第二階段 payload**：向遠端 C2（Command & Control）伺服器取得針對性 RAT
4. **寫入並執行**：RAT 落地後建立遠端存取管道，可竊取 AWS 憑證、OpenAI API keys 等
5. **自我清除**：刪除自身、移除 `package.json` postinstall 腳本 → `npm audit` 看不出異常

## 若已中招的處置步驟

- 立即輪換所有 API keys 與 tokens（AWS、OpenAI 等）
- 僅刪除 RAT 檔案**不夠**，系統視為已完全淪陷
- 參考 [Step Security 指南](https://step.security.io) 進行完整清除流程

## 背景：為何 Axios 仍被廣泛使用

- Axios 10 年前以 Promise-based HTTP 請求竄紅，取代 callback 模式
- 現今各 JS runtime 原生支援 `fetch`，理論上 Axios 應已被取代
- 但許多開發者仍因 DX（開發者體驗）偏好繼續使用第三方套件
- 此事件揭示依賴第三方套件的潛在風險
