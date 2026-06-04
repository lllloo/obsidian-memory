---
title: Git 設定
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/git/setting
tags:
  - git
---

# Git 設定

本文件整理常用 Git 設定指令與說明，適合日常開發參考。

## 查看所有 Git 配置

```sh
git config --list
```

顯示目前所有 Git 設定（包含全域與專案層級）。

## 常用快捷鍵（alias）

在 `~/.gitconfig` 中加入以下設定，可簡化常用指令：

```ini
[alias]
  co = checkout
  st = status
  br = branch
  lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit -20
```

也可透過指令逐一設定：

```sh
git config --global alias.co checkout
git config --global alias.st status
git config --global alias.br branch
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit -20"
```

`git lg` 效果說明：

- 彩色 graph 樹狀分支圖
- 短 commit hash（紅色）
- branch/tag 標籤（黃色）
- 相對時間（綠色）
- 作者名稱（藍色）
- 預設顯示最近 20 筆，可加參數調整，如 `git lg -50`

## 換行符號自動轉換設定

```sh
git config --global core.autocrlf false
```

選項說明：

- `true`：提交時將 CRLF 轉為 LF，檢出時將 LF 轉為 CRLF（適合 Windows 使用者與跨平台專案）。
- `input`：提交時將 CRLF 轉為 LF，檢出時不變（適合 Linux/macOS）。
- `false`：不進行任何換行符轉換，保持原始狀態。

## 清除暫存區與重設檔案

```sh
git rm --cached -r .
git reset --hard
```

指令說明：

- `git rm --cached -r .`：將所有檔案從暫存區移除（不刪除實體檔案）。
- `git reset --hard`：將所有檔案重設至最後一次提交狀態，覆蓋本地修改。
