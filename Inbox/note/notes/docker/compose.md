---
title: Docker Compose
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/docker/compose
tags:
  - docker
  - cli
---

# Docker Compose

Docker Compose 是用來定義與執行多容器應用程式的工具，透過 `compose.yml` 描述所有服務的設定，用一行指令啟動整個環境。

## compose.yml 結構

```yaml
services:       # 定義容器服務
  app:
    image: node:24-slim
    ports:
      - '3000:3000'

volumes:        # 定義 named volume（可選）
  db_data:

networks:       # 定義自訂網路（可選，預設會自動建立）
  backend:
```

### services 常用欄位

```yaml
services:
  app:
    image: node:24-slim          # 使用現有 image
    build:                       # 或從 Dockerfile 建構
      context: .
      dockerfile: Dockerfile.dev
    container_name: my-app       # 自訂容器名稱
    ports:
      - '3000:3000'              # host:container
    environment:
      - NODE_ENV=production
      - API_KEY=secret
    env_file:
      - .env                     # 從檔案讀取環境變數
    volumes:
      - .:/app                   # bind mount
      - db_data:/var/lib/data    # named volume
    networks:
      - backend
    restart: unless-stopped      # 容器異常時自動重啟
    depends_on:
      - db
```

## volumes 類型

### Bind Mount

將本機目錄直接掛載進容器，雙向即時同步：

```yaml
volumes:
  - ./src:/app/src               # 相對路徑
  - /absolute/path:/app/data     # 絕對路徑
```

適合開發環境，讓容器即時反映本機檔案異動。

### Named Volume

由 Docker 管理的獨立儲存空間，需在頂層 `volumes:` 聲明：

```yaml
services:
  db:
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

適合需要持久化的資料（資料庫、上傳檔案），容器刪除後資料仍保留。

### Anonymous Volume

不命名的 volume，通常用來「佔位」防止某個路徑被 bind mount 覆蓋：

```yaml
volumes:
  - .:/app
  - /app/node_modules    # 保護容器內的 node_modules 不被上一行覆蓋
```

沒有名稱，難以辨識與管理。執行 `docker compose down -v` 或 `docker rm -v` 才會一併移除，單純 `docker compose down` 不會刪除。不建議用來儲存重要資料。

### 三種類型比較

| 類型 | 資料位置 | 資料持久 | 適合場景 |
| --- | --- | --- | --- |
| Bind Mount | 本機指定路徑 | 是 | 開發時同步原始碼 |
| Named Volume | Docker 管理 | 是 | 資料庫、持久資料 |
| Anonymous Volume | Docker 管理 | 需以 `-v` 或後續清理移除 | 佔位用途 |

## 常用指令

```bash
# 建構並啟動（前景）
docker compose up --build

# 建構並啟動（背景）
docker compose up --build -d

# 停止並移除容器（保留 volume）
docker compose down

# 停止並移除容器與 volume
docker compose down -v

# 只重新建構 image（不啟動）
docker compose build

# 查看執行中的容器
docker compose ps

# 查看日誌
docker compose logs -f app

# 進入容器執行指令
docker compose exec app sh

# 執行一次性指令後移除容器
docker compose run --rm app npm install

# 指定 compose 檔案
docker compose -f compose.dev.yml up --build -d
```
