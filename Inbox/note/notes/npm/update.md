---
title: npm 套件更新與檢查指令
created: 2026-06-03
updated: 2026-06-04
tags:
  - npm
  - cli
---

# npm 套件更新與檢查指令

本文件整理常用的 npm 套件更新、檢查新版本的指令與操作步驟，適合日常前端開發參考。

## 使用 npm 指令

- 檢查已安裝套件是否有新版本：

```sh
npm outdated
```

- 更新 package.json 中定義的所有套件（依照版本範圍）：

```sh
npm update
```

> 注意：`npm update` 會在 `package.json` 既有的 semver 版本範圍內更新套件，並更新 lockfile，但**不會**調整 `package.json` 內的版本範圍字串。

- 若你想「提高」`package.json` 內依賴的版本範圍，建議改用下列方式：

```sh
# 單一套件升級到最新版本（會更新 package.json 與 lockfile）
npm install <package-name>@latest
```

## 使用 npm-check-updates (ncu)

- 安裝工具：

```sh
npm install -g npm-check-updates
```

- 檢查可升級的套件：

```sh
ncu
```

- 更新 package.json 依賴版本：

```sh
ncu -u
```

> 執行完 `ncu -u` 後，請務必再執行 `npm install`，以實際安裝更新後的套件版本。

- 也可用 npx 方式臨時執行：

```sh
# 檢查
npx npm-check-updates
# 更新
npx npm-check-updates -u
```

## 參考資料

- [npm 官方文件](https://docs.npmjs.com/cli/v10/commands/npm-update)
- [npm-check-updates](https://www.npmjs.com/package/npm-check-updates)
