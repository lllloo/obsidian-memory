---
title: MOC 筆記組織法
tags:
  - obsidian
  - workflow
created: 2026-03-22
updated: 2026-03-22
---

MOC（Map of Content）是用一篇筆記作為某個主題的索引，透過 wikilinks 串連相關筆記。

## 為什麼不用資料夾分類

- 一篇筆記常橫跨多個主題，資料夾只能放一個位置
- [Obsidian CEO Steph Ango](https://stephango.com/vault) 建議靠連結和標籤組織，資料夾越少越好
- 太早分資料夾會變成空殼，太晚分又會太亂

## 混合式策略

結合 MOC 和資料夾的漸進式做法：

```
Inbox/                  ← 日記
Cards/                  ← 未分類筆記先放這
├── Quartz 部署筆記.md
├── MOC 筆記組織法.md
└── skill-creator 是什麼.md
Topics/                 ← 主題區
├── Vue.md              ← MOC（初期，單檔索引）
└── Obsidian/           ← 升級後的資料夾
    ├── index.md        ← 原本的 MOC
    ├── CLI 整合指南.md
    └── ...
Templates/              ← 模板
```

### 演進流程

1. **新筆記一律放 `Cards/`**
2. 某主題累積足夠筆記 → 在 `Topics/` 建 MOC（如 `Topics/Vue.md`）
3. 筆記多到需要獨立管理 → MOC 轉為 `Topics/<主題>/index.md`，相關筆記搬入
4. 何時拆分由自己決定，不急

## 好處

- 前期零負擔，不用想分類
- MOC 用連結串連，比資料夾更靈活
- 需要時可以無痛升級成資料夾
