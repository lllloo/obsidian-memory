---
title: Nuxt + Docker 開發/部署筆記
created: 2026-06-03
updated: 2026-06-04
tags:
  - docker
  - nuxt
  - deploy
  - nginx
---

# Nuxt + Docker 開發/部署筆記

## 核心設計架構

1. **基礎鏡像**: `node:24-slim` (兼顧體積與 Debian 穩定性)。
2. **多階段構建**: 同一個檔案支援 `dev`、`SSR (Node)` 與 `Static (Nginx)`。
3. **npm ci**: 在構建過程中取代 `npm install`，保證開發與生產環境版本 100% 一致。

## node:slim vs node:alpine

建議使用 `node:slim` 而非 `node:alpine`：

- Alpine 使用 musl libc，並非 Node.js 官方支援的 libc
- 含原生模組的套件（如 `sharp`、`bcrypt`）在 Alpine 上可能編譯失敗或行為異常
- slim 使用 Debian，是 Node.js 官方支援的環境

> 若確定專案沒有原生模組依賴，使用 `node:alpine` 也可以，映像更小。

## 1. 核心 Dockerfile

```dockerfile
# === 1. 基礎環境 (Base) ===
FROM node:24-slim AS base
WORKDIR /app
# slim 版本建議更新一下基礎套件包，確保安全性
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# === 2. 依賴安裝 (Deps) ===
FROM base AS deps
COPY package*.json ./
# 使用 npm clean install (ci) 確保版本與 lock 檔一致，且速度較快
RUN npm ci

# === 3. 開發環境 (Development) ===
FROM deps AS development
# 確保不掛載 volume 時仍可獨立啟動；掛載時 volume 會覆蓋此內容，熱更新不受影響
COPY . .
EXPOSE 3000
# 透過 npm run dev 啟動，並確保監聽 0.0.0.0
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# === 4. 編譯階段 (Builder) ===
FROM deps AS builder
COPY . .
RUN npm run build

# === 5-A. 部署：SSR 模式 (Node.js Server) ===
FROM node:24-slim AS ssr-production
# USER node 放在 WORKDIR 之前，確保目錄由 node 使用者建立，具備正確權限
USER node
WORKDIR /app
# 僅複製 Nuxt 編譯後的 output，不含原始碼與 devDependencies
COPY --from=builder --chown=node:node /app/.output ./.output
EXPOSE 3000
# 直接用 node 執行，確保 docker stop 的 SIGTERM 能正確傳給 Node.js 做 graceful shutdown
# npm start 不轉發 signal，應避免使用
CMD ["node", ".output/server/index.mjs"]

# === 5-B. 部署：靜態模式 (Nginx) ===
FROM nginx:stable-alpine AS static-production
COPY --from=builder /app/.output/public /usr/share/nginx/html
# 若需 SPA 路由支援，請取消下行註釋並準備 nginx.conf
# COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 各 Stage 說明

| Stage               | 用途                                                         |
| ------------------- | ------------------------------------------------------------ |
| `base`              | 安裝系統依賴，供後續 stage 繼承                              |
| `deps`              | 安裝 npm 套件，供後續 stage 繼承                             |
| `development`       | 繼承 `deps`，含 source code，搭配 compose volume 支援熱更新  |
| `builder`           | 繼承 `deps`，複製 source code 並執行 build                   |
| `ssr-production`    | 最終映像，只複製 `.output`，不含原始碼與 devDependencies     |
| `static-production` | 使用 Nginx 提供靜態檔案                                      |

---

## 2. Docker Compose 配置

在 `docker-compose.yml` 中透過 `target` 指定要建構的 stage。

```yaml
services:
  # 【開發模式】支援 Hot Reload
  nuxt-dev:
    build:
      context: .
      target: development
    container_name: nuxt-app-dev
    volumes:
      - .:/app                          # 同步原始碼
      - node_modules:/app/node_modules  # 具名 volume 確保容器內的 Linux 套件不被本機覆蓋
    ports:
      - "3000:3000"
    environment:
      - CHOKIDAR_USEPOLLING=true # 確保 Windows/Mac 檔案變動能被偵測

  # 【SSR 模式】模擬線上 Node.js 運行環境
  nuxt-ssr:
    build:
      context: .
      target: ssr-production
    ports:
      - "3001:3000"
    restart: unless-stopped
    environment:
      - NODE_ENV=production

  # 【靜態模式】使用 Nginx 運行
  nuxt-static:
    build:
      context: .
      target: static-production
    ports:
      - "8080:80"
    restart: unless-stopped

volumes:
  node_modules:
```

---

## 3. Docker Compose 常用指令

| 目的 | 指令 |
| :--- | :--- |
| **啟動開發環境** | `docker compose up nuxt-dev` |
| **新增套件後重構** | `docker compose up --build nuxt-dev` |
| **測試 SSR 版本** | `docker compose up nuxt-ssr` |
| **測試靜態 Nginx 版本** | `docker compose up nuxt-static` |
| **查看日誌** | `docker compose logs -f nuxt-dev` |

---

## 4. 關鍵設計說明

### 為什麼要在開發模式使用 `volumes`？

- **雙重掛載技巧：** `- .:/app` 同步代碼，`- node_modules:/app/node_modules` 具名 volume 確保容器內的 Linux 套件不會被本機的 Windows/Mac 套件蓋掉。
- **Hot Reload：** 透過掛載，你在 VS Code 改程式碼，Docker 內的 Nuxt 會立刻偵測到並更新。

### 為什麼 `development` stage 也要 `COPY . .`？

確保映像在「不掛載 Volume」的情況下（如 CI 環境、快速驗證）依然可以獨立啟動。搭配 compose volume 時，volume 會覆蓋 `COPY` 的內容，熱更新仍然正常運作，兩者不衝突。

### 為什麼使用 `USER node`？

`node:slim` 內建 `node` 使用者，讓容器以非 root 身份執行，提升安全性。`USER node` 必須放在 `WORKDIR /app` 之前，確保 `/app` 目錄由 `node` 使用者建立，具備正確的讀寫權限；若順序相反，目錄會由 root 建立，`node` 使用者將無法寫入。

### 為什麼直接用 `node` 執行而非 `npm start`？

`npm start` 不會轉發 `SIGTERM` 訊號給子行程，導致 `docker stop` 時 Node.js 無法執行 graceful shutdown。直接使用 `CMD ["node", ".output/server/index.mjs"]` 可確保訊號正確傳遞。

### 如何進行生產 Build？

```bash
# 建立 SSR 版本的 Image
docker build --target ssr-production -t my-nuxt-app:latest .

# 建立靜態版本的 Image
docker build --target static-production -t my-nuxt-static:latest .
```

---

## 5. 常見問題 (Tips)

- **新增套件：** 在本機 `npm install` 後，請執行 `docker compose up --build` 重新構建開發環境。
- **SPA 路由 404：** 若使用 Nginx 部署且遇到重新整理 404，需在 Nginx 設定中加入 `try_files $uri $uri/ /index.html;`。
- **找不到模組：** 若啟動錯誤提到 `Cannot find module ...`，代表 build 產物非完全自包含，需在 `nuxt.config.ts` 確認 `nitro.preset` 設為 `node-server`（預設值），或檢查是否誤用了其他 preset。
- **缺少編譯工具：** 若 `npm install` 遇到需要編譯 C++ 的套件報錯，在 `base` 階段加入：

```dockerfile
RUN apt-get update && apt-get install -y python3 make g++
```

---

## 6. .dockerignore

建立 `.dockerignore` 檔案，避免 Build Context 將主機的髒資料或敏感資訊傳進映像檔，可大幅縮短 Build 時間。

```text
node_modules/
.nuxt/
.output/
.git/
.env*
```

| 項目                | 原因                                                                                           |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| `node_modules/`     | 容器內會重新安裝，排除可大幅縮小 build context；本機的二進位套件（Windows/Mac）與 Linux 容器不相容 |
| `.nuxt/` `.output/` | build 產物，容器內會重新建構                                                                   |
| `.git/`             | 不需要版本控制歷史，減少 build context 大小                                                    |
| `.env*`             | 避免環境變數（含敏感資訊）被複製進 image；即使後續刪除仍可能從 Image Layer 還原                |

---

## 參考資料

- [Docker 官方 Node.js 容器化指南](https://docs.docker.com/guides/nodejs/)
- [Nitro 部署文件](https://nitro.build/deploy/node)
