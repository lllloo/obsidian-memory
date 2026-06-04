---
title: Volta 簡易使用教學
created: 2026-06-03
updated: 2026-06-04
tags:
  - volta
  - npm
  - cli
---

# Volta 簡易使用教學

這份文件說明如何安裝、設定與管理 Volta 及 Node.js 版本，適用於前端開發環境建置。

## 安裝版本

```sh
volta install node@20
```

## 專案綁定版本（自動切換）

在專案資料夾內執行：

```sh
volta pin node@20
```

這樣當你進入這個資料夾時，Volta 會自動切換成指定版本的 Node.js。

## 查看 Node.js 相關版本

```sh
volta list node
```

## 查看目前使用的版本

```sh
volta list
```

## 查看所有 Volta 管理的工具與版本

```sh
volta list all
```

## package.json 設定範例

當你使用 `volta pin` 指令後，Volta 會自動在專案的 `package.json` 中添加 `volta` 欄位：

```json
{
  "volta": {
    "node": "20.12.2"
  }
}
```

## 移除版本

目前官方的方法不能直接移除特定版本，但可以自行清除未使用的版本：

- [Uninstall 方法參考](https://github.com/volta-cli/volta/issues/327#issuecomment-920336408)
- [Windows 系統清除方法](https://github.com/volta-cli/volta/issues/327#issuecomment-1210123006)

## 參考資料

- [Volta 官方網站](https://volta.sh)
