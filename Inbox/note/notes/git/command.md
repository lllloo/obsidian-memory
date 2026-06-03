---
title: Git 指令
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/git/command
tags:
  - git
---

# Git 指令

本文件整理常用的 Git 指令，包括分支管理、提交操作、差異比較等，適合作為日常開發參考手冊。每個指令附有簡要說明與實際使用場景。

## 常規提交

使用標準化的提交訊息格式，使 Git 歷史記錄更清晰易讀。

- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)

## 遠端管理

### 更改遠端位址

```sh
git remote -v
git remote set-url origin <url>
```

- `git remote -v`：查看目前遠端倉庫網址。
- `git remote set-url origin <url>`：更改遠端 origin 的網址。

### 強制拉遠端分支覆蓋本地

```sh
git pull -f origin develop:develop
```

::: warning 注意
此指令會強制以遠端分支覆蓋本地分支，可能導致本地未提交的變更遺失。請謹慎使用。
:::

## 分支管理

### 刪除本地分支

```sh
git branch -d localBranchName
```

### 刪除遠端分支

```sh
git push origin --delete remoteBranchName
```

## cherry-pick

用於選擇性地將特定提交套用到當前分支。

### 合併其他分支的 Commit

```sh
git cherry-pick fd23e1c 6a498ec f4f4442
git cherry-pick '第1個' '第2個' '第3個'
```

- 第一行是實際使用 commit 哈希值的範例
- 第二行是示意用法，需替換為實際的 commit ID

## diff-tree

用於比較兩個樹對象（通常是 commit）之間的差異。

### 顯示 HEAD 與上一個 HEAD^ 差異的檔案

```sh
git diff-tree -r --name-only --diff-filter=ACMRT HEAD~ HEAD
```

- `-r`：遞迴比較子目錄
- `--name-only`：僅顯示檔案名稱
- `--diff-filter=ACMRT`：僅顯示新增(A)、複製(C)、修改(M)、重命名(R)和類型改變(T)的檔案

### 將差異檔案打包

#### 將 HEAD 與上一個 HEAD^ 差異的檔案打包成 zip

```sh
git archive --format=zip --output=update.zip HEAD $(git diff-tree -r --name-only --diff-filter=ACMRT HEAD~ HEAD)
```

#### 兩個 commit 差異打包

```sh
git archive --format=zip --output=update.zip HEAD $(git diff-tree -r --name-only --diff-filter=ACMRT HEAD~2 HEAD)
```

- 此例比較最近兩次提交之間的差異
