---
title: 拯救網頁的 JavaScript 肥大問題
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-29
source: https://www.youtube.com/watch?v=1t-k6-m50Fc
---

## 三種 JS 套件肥大的根源

Theo 介紹 James Garbet 的文章《Three Pillars of JavaScript Bloat》，分析現代 npm 依賴樹中不必要肥大的三大原因。

## 第一柱：過時的引擎相容性支援

部分套件為了支援 ES3 時代的瀏覽器（IE6/7）或極老版本的 Node，引入大量 polyfill：

- `is-string` → `has-tostringtag` → `has-symbols` → `call-bound` → `get-intrinsic` → 更多子依賴
- `for-each`、`object.keys`、`string.prototype.trim` 等 ES5 功能至今還有獨立套件，每週數百萬次下載

這些需求僅存在於 Hero Devs 這類維護古老系統的特殊族群，卻透過依賴樹影響所有開發者。

**Cross-realm 問題**：在 iframe 和父頁面之間傳遞物件時，`instanceof` 無法跨 realm 使用，因此需要用 `Object.prototype.toString` 替代——這讓部分 polyfill 的存在有其技術理由。

## 第二柱：原子化架構（Atomic Architecture）

套件被拆分到極致，每個函式都是獨立套件：

| 套件 | 內容 | 每週下載 |
|------|------|---------|
| `shebang-regex` | 一個 regex | 1.33 億次 |
| `slash` | 一行程式碼 | 9,600 萬次 |
| `path-key` | 4KB 檔案 | 1.58 億次 |
| `once` | 確保函式只被呼叫一次 | 1.31 億次 |

這些套件大多只被同一個作者的另一個套件使用，形成「應該是 inline 程式碼，卻拆成獨立套件」的怪現象。

副作用：供應鏈攻擊面積擴大。曾有維護者帳號被入侵，導致數百個微型套件同時被污染。

## 第三柱：過期的 Pony Fill

Pony fill 是 polyfill 的變體：不污染全域環境，而是提供獨立的 import 路徑。問題是當原生支援已普及，這些 pony fill 卻從未被移除：

- `globalThis`（2019 年起廣泛支援）：`globalthis` 套件仍有每週 4,900 萬次下載
- `Object.entries`（2017 年）：相關套件每週 3,500 萬次下載
- `Array.prototype.indexOf`（2010 年）：每週 230 萬次下載

## 解決方案

- **E18（E18E）基金會**：整理現代化替代套件、建立 cleanup initiative
- **nip**：找出專案中未使用的依賴和 import
- **E18 CLI**：`analyze` 模式分析可移除的依賴，`migrate` 指令自動遷移（例如 chalk → picocolors）
- **npmgraph**：視覺化依賴樹，找出可精簡的路徑

## Theo 的行動

Theo 當場捐款 $5,000 給 E18 基金會（該組織當時只有 $17,000 存款），並呼籲觀眾和公司贊助。他認為 E18 是讓 JavaScript 生態系存活的關鍵工作，而這些開發者的貢獻遠遠被低估且薪酬不足。
