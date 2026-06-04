---
title: Docker 網路隔離：只暴露 Nginx
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/docker/network
tags:
  - docker
  - nginx
  - security
---

# Docker 網路隔離：只暴露 Nginx

在多服務架構中，只讓 Nginx 對外開放 port，前端、後端、DB 全部走 Docker 內部網路，不暴露給 host。

## 架構

```text
Host
 │
 └── port 80
        │
     Nginx          ← 唯一對外的服務
        │
     app 網路（bridge）
        ├── Frontend   （無 host port）
        └── Backend    （無 host port）
                │
             data 網路（bridge, internal: true）
                └── DB （無 host port，無法對外連線）
```

## compose.yml

```yaml
services:
  nginx:
    image: nginx:alpine
    ports:
      - '80:80'      # 只有 nginx 對外開放
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf:ro
    networks:
      - app
    depends_on:
      - frontend
      - backend

  frontend:
    build: ./frontend
    # 沒有 ports → 一般情況下 host 無法透過 localhost 直接存取
    # 僅同網路容器可透過服務名稱連線
    networks:
      - app

  backend:
    build: ./backend
    networks:
      - app          # nginx 可透過 app 網路連到 backend
      - data         # backend 可透過 data 網路連到 db

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=secret # 示意用，正式環境請改用 .env 或 secrets
    volumes:
      - db_data:/var/lib/postgresql/data
    networks:
      - data         # 只在 data 網路，backend 以外無法存取

networks:
  app:
    driver: bridge
  data:
    driver: bridge
    # internal: true → 只在此網路的容器（db）無法對外連線
    # backend 同時在 app 網路，仍可對外連線
    internal: true

volumes:
  db_data:
```

## nginx.conf

容器間透過**服務名稱**作為 hostname，這是 Docker DNS 自動提供的：

```nginx
server {
    listen 80;

    # 前端
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 後端 API
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 核心概念

### `ports` 與容器隔離

`ports` 會將容器 port 綁定到 host，外部可直接存取。不寫 `ports` 的服務，一般情況下 host 無法透過 `localhost` 直接連線，只能透過同網路的其他容器存取。

### 自訂網路的隔離效果

不同網路的服務**無法直接通訊**：

- `nginx` 只在 `app` 網路 → 無法直接連到 `db`（在 `data` 網路）
- `frontend` 只在 `app` 網路 → 無法直接連到 `db`
- `backend` 同時在兩個網路 → 橋接 `nginx` 與 `db` 的中間層

### `internal: true`

加在 `data` 網路上，代表**只在此網路**的容器無法對外發出連線（無法存取 internet）。

若容器同時加入其他非 internal 網路，仍可透過該網路對外連線（例如下方 `backend`）。

| 服務 | 所在網路 | 能否對外連線 |
| --- | --- | --- |
| `db` | 只在 `data`（internal） | ❌ 無法 |
| `backend` | `app` + `data` | ✅ 透過 `app` 網路仍可 |

> 若 `backend` 也需要完全隔離，可移除它的 `app` 網路，改讓 `nginx` 直接加入 `data` 網路。但通常 backend 需要呼叫外部 API，保留對外能力是合理的。

DB 容器通常不需要對外連線，加上 `internal: true` 可確保即使 DB 被攻破也無法對外建立連線。

## 驗證隔離效果

```bash
# 確認 frontend、backend、db 沒有對外的 port binding
docker compose ps
# PORTS 欄位只有 nginx 顯示 0.0.0.0:80->80/tcp

# 若容器內沒有 nc，可先確認是否能解析服務名稱
docker compose exec frontend sh -c "getent hosts db"
# 預期：找不到 db（名稱解析失敗）

# 嘗試從 frontend 容器直接連 db（應失敗）
docker compose exec frontend sh -c "nc -zv db 5432"
# 預期：名稱解析失敗（如 Name not known）或連線不可達

# 從 backend 容器連 db（應成功，因為同在 data 網路）
docker compose exec backend sh -c "nc -zv db 5432"
# 預期：open
```

## 參考資料

- [Docker Docs - Networking overview](https://docs.docker.com/engine/network/)
- [Docker Docs - Networks（Compose 參考）](https://docs.docker.com/reference/compose-file/networks/)
- [Docker Docs - Publishing and exposing ports](https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/)
