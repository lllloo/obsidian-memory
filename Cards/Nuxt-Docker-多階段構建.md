---
title: Nuxt + Docker 多階段構建
created: 2026-06-03
updated: 2026-06-11
tags:
  - docker
  - nuxt
  - deploy
  - nginx
---

一份 Dockerfile 用多階段構建同時支援 `dev`、`SSR (Node)`、`Static (Nginx)` 三種模式，compose 用 `target` 切換。模板可照抄，每個設計都有理由（見下方判斷段）。

## 先講判斷

- **slim 優於 alpine 作為預設**：Node 官方 image 有 Alpine variant，但官方 caveat 是 Alpine 使用 musl libc，依賴 glibc 假設的軟體可能出問題；含原生模組的套件（`sharp`、`bcrypt`）更容易踩相容性坑。確定無原生模組依賴、且體積優先時才考慮 alpine。
- **`node` 直跑，避免 `npm start` 當 PID 1**：`npm` / shell wrapper 可能讓 signal handling 變得不穩定，`docker stop` 時 graceful shutdown 較不可預期。`CMD ["node", ".output/server/index.mjs"]` 讓 Node.js 直接收訊號，行為最單純。
- **非 root runtime 要明確處理 ownership**：不要依賴 `USER node` / `WORKDIR` 順序自動建立可寫目錄；不同 builder / 執行方式的 ownership 行為可能不同。穩定做法是先 `mkdir` + `chown`，或在 `COPY` 時用 `--chown=node:node`。
- **`npm ci` 取代 `npm install`**：鎖 lock 檔版本，開發與生產 100% 一致。
- **雙重掛載技巧**：`- .:/app` 同步原始碼支援熱更新，`- node_modules:/app/node_modules` 具名 volume 佔位，防容器內 Linux 套件被本機（Windows/Mac）的二進位蓋掉。
- **`development` stage 仍要 `COPY . .`**：確保不掛 volume（CI、快速驗證）也能獨立啟動；掛 volume 時會被覆蓋、熱更新不受影響，兩者不衝突。
- **`.env*` 必進 `.dockerignore`**：被 `COPY` 進去的敏感資訊即使後續刪除，仍可從 image layer 還原。`node_modules/`、`.nuxt/`、`.output/`、`.git/` 也排除（容器內重建、縮 build context）。
- **static 模式產物要用 `generate`，不是 `build`**：`npm run build`（node-server preset）的 `.output/public` 只有 client assets、沒有 index.html——Nginx 靜態部署必須用 `npm run generate` 的 prerender 產物，所以 static 走獨立的 generator stage。
- **production stage 只 COPY `.output`**：不含原始碼與 devDependencies，映像最小、攻擊面最小——別為了 debug 方便把整個 `/app` 搬進去，多階段構建的核心收益就在這裡。

## Dockerfile 模板

Node 版本以當前 LTS 為準（下例 `node:24-slim`）。

```dockerfile
# === 1. 基礎環境 ===
FROM node:24-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*
# 若套件需編譯 C++，在此加：python3 make g++

# === 2. 依賴安裝 ===
FROM base AS deps
COPY package*.json ./
RUN npm ci

# === 3. 開發環境 ===
FROM deps AS development
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# === 4. 編譯（SSR 用） ===
FROM deps AS builder
COPY . .
RUN npm run build

# === 4-B. 靜態產物（static 用，prerender 出 HTML） ===
FROM deps AS generator
COPY . .
RUN npm run generate

# === 5-A. 部署：SSR（Node server） ===
FROM node:24-slim AS ssr-production
USER node
WORKDIR /app
COPY --from=builder --chown=node:node /app/.output ./.output
EXPOSE 3000
CMD ["node", ".output/server/index.mjs"]

# === 5-B. 部署：靜態（Nginx） ===
FROM nginx:stable-alpine AS static-production
COPY --from=generator /app/.output/public /usr/share/nginx/html
# SPA 路由需自備 nginx.conf（含 try_files），取消下行註解：
# COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Compose：用 target 切模式

```yaml
services:
  nuxt-dev:
    build: { context: ., target: development }
    volumes:
      - .:/app
      - node_modules:/app/node_modules
    ports: ['3000:3000']
    environment:
      - CHOKIDAR_USEPOLLING=true   # Windows/Mac 檔案變動偵測

  nuxt-ssr:
    build: { context: ., target: ssr-production }
    ports: ['3001:3000']
    restart: unless-stopped
    environment:
      - NODE_ENV=production   # Vue Router 等套件 runtime 讀此決定行為；node:slim 不預設

  nuxt-static:
    build: { context: ., target: static-production }
    ports: ['8080:80']
    restart: unless-stopped

volumes:
  node_modules:
```

## 踩坑

- **新增套件後容器找不到**：本機 `npm install` 不會進容器；且具名 volume 只在**首次為空**時從 image 複製內容，`up --build` 重建 image 也蓋不掉舊 volume——要 `docker compose down -v` 再 up，或直接進容器跑 `npm install`。注意 `down -v` 會刪掉 compose 內**所有**具名 volume，同份 compose 還有 DB 資料 volume 時改用 `docker volume rm` 單刪——先 `docker volume ls` 查實名（格式：`<專案目錄名>_node_modules`），再 `docker volume rm <實名>`。
- **Nginx 靜態部署重新整理 404**：SPA 路由需自備 nginx.conf 加 `try_files $uri $uri/ /index.html;`，並在 static stage COPY 進去（見模板註解行）。
- **啟動報 `Cannot find module`**：build 產物非自包含——確認 `nuxt.config.ts` 的 `nitro.preset` 是 `node-server`（預設），沒誤用其他 preset。

## 相關

- [[Docker-與-PM2-取捨]] — 同根因延伸：為什麼容器內程序管理交給 Docker 而非 PM2
- [[Docker-網路隔離只暴露-Nginx]] — 部署後的網路隔離拓撲

## 參考資料

- [Docker 官方 Node.js 容器化指南](https://docs.docker.com/guides/nodejs/)
- [Nitro 部署文件](https://nitro.build/deploy/node)
