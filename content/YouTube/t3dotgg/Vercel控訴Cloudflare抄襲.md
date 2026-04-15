---
title: Vercel 控訴 Cloudflare 抄襲
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-19
source: https://www.youtube.com/watch?v=mVKxygo5Sdo
---

## just-bash 是什麼

Vercel CTO Malte 開發的開源套件：在 TypeScript 中模擬 bash 環境，讓 AI agent 能夠以虛擬 bash 方式探索程式碼庫，同時避免直接存取真實 Linux shell 帶來的安全風險。

設計目的：把 bash 執行層「抬高」到 Node.js 層，讓 agent 的 fs 操作留在記憶體中，不碰底層系統。

## 爭議：Cloudflare 未溝通就 fork

Cloudflare 工程師 Sunil Pai 在看到 just-bash 後非常興奮，在沒有先聯繫 Malte 的情況下，直接在 Cloudflare 的官方 GitHub org 下以 `@cloudflare/shell` 名義 fork 並發布。

Malte 的控訴：
- Cloudflare 移除了「這是 beta 版」的警告說明
- 移除了 Python 安全層（用 Pyodide 的不安全方式替換）
- 移除了多層 defense-in-depth 安全機制（防止 host breakout）
- 宣稱可在 Node.js、Deno、Cloudflare Workers 等環境通用，卻拿掉了針對 Node 的安全保護

## Vercel vs Cloudflare 底層架構差異

這場爭議凸顯了兩家平台本質上的不同：

**Vercel**：每個開發者的程式碼跑在獨立的 Docker image / Linux 實例上，Node.js 可以直接呼叫底層 shell，因此 just-bash 的安全層至關重要。

**Cloudflare Workers**：使用 V8 隔離（isolate）作為安全邊界，worker 環境本身就無法執行真實 bash，所以 just-bash 的安全層對他們是不必要的——但也意味著原本的 just-bash 根本無法在 Cloudflare 上執行。

結論：Sunil 想要的是 bash 模擬層本身，而不是安全保護層，這就是為什麼他把安全層移除了——對 Cloudflare 的架構來說它確實不必要。

## 事件真相：善意誤踩地雷

Sunil 事後澄清：這是他個人週末在西班牙的 vibe coding 實驗，打算測試完再正式聯絡 Malte 討論 hook 整合，沒想到倉庫設定得太完整，被當成正式 fork 發布。

Malte 最終也公開道歉，承認自己在沒有先私下聯繫 Sunil 的情況下就公開指控是錯誤的。

## Theo 的結論

- Sunil 是出於真心喜歡 just-bash 才這樣做，沒有惡意
- Cloudflare 最大的失誤是讓 fork 出現在官方 org 下，讓外界以為是正式產品
- Malte 最大的失誤是選擇公開指控而非先私下發訊息
- 根本原因：Vercel 和 Cloudflare 之間已積累太多壞帳（Vinext fork 事件），導致任何動作都被預設為惡意

> 先發 DM，再公開發文。這不難。
