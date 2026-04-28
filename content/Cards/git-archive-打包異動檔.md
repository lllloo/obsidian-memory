---
title: git archive 打包異動檔
created: 2026-04-28
updated: 2026-04-28
tags:
  - git
  - cli
  - deploy
---

## 指令

```bash
git archive -o update.zip HEAD $(git diff --name-only --diff-filter=ACMR HEAD~1..HEAD)
```

## 用途

把「上一個 commit 到目前 HEAD」之間新增（A）、修改（M）、改名（R）、複製（C）的檔案，打包成 `update.zip`。常用情境：上版／交付異動檔給沒有 Git 的環境，只壓縮這次更動的檔案。

## 變體

指定兩個 commit 之間：

```bash
git archive -o update.zip <to-commit> $(git diff --name-only --diff-filter=ACMR <from-commit>..<to-commit>)
```

輸出刪除清單（另存 `deleted.txt`，方便對方手動刪檔）：

```bash
git diff --name-only --diff-filter=D HEAD~1..HEAD > deleted.txt
```

## 重點

- `--diff-filter=ACMR`：只取新增/修改/改名/複製，**不含刪除**（D）
- `archive` 後面第一個參數是「要從哪個 commit 抓檔案內容」，通常用 `HEAD`
- `$()` 命令替換在 Windows cmd 不支援，需改用 PowerShell 或 Git Bash
