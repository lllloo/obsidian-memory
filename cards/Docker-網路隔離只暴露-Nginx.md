---
title: Docker 網路隔離：只暴露 Nginx
created: 2026-06-03
updated: 2026-06-11
tags:
  - docker
  - nginx
  - security
---

**多服務 compose 只讓 Nginx 寫 `ports`，其餘服務一律不發佈 host port**——前端、後端、DB 全走 Docker 內部網路，靠服務名稱（Docker DNS）互連。沒寫 `ports` 的服務無法透過 `localhost` 存取，對外攻擊面只剩 Nginx 一個入口；注意這道隔離擋的是外部流量——Linux host 本機仍可直連容器的 bridge IP。

## internal: true 的精確語意（最容易誤解的點）

`internal: true` 約束的是「**僅在**該網路」的容器無法對外連線，不是「掛上這個網路就被隔離」：

| 服務 | 所在網路 | 能否對外連線 |
|---|---|---|
| `db` | 只在 `data`（internal） | 無法 |
| `backend` | `app` + `data` | 可以——透過 `app` 網路逃逸 |

所以 DB 加 `internal: true` 是有效防線（即使被攻破也無法對外回連），但 backend 同時掛兩個網路就不受約束——通常是合理取捨（backend 多半要呼叫外部 API）；真要連 backend 一起隔離，拔掉它的 `app` 網路、改讓 Nginx 直接加入 `data` 網路。

## 拓撲

```text
Host ── port 80 ── Nginx
                     │ app 網路（bridge）
                     ├── Frontend（無 host port）
                     └── Backend ──┐ data 網路（bridge, internal: true）
                                   └── DB（無 host port、無法對外）
```

不同網路的服務無法直接通訊：nginx / frontend 只在 `app`，連不到 `db`；backend 雙網路，是唯一橋接層。

```yaml
networks:
  app:
    driver: bridge
  data:
    driver: bridge
    internal: true
```

各服務只要在 `networks:` 掛對網路即可；Nginx 的 `proxy_pass` 直接寫服務名（`http://backend:8000`），Docker DNS 解析。

反向代理時必須轉發這四個 header，否則後端會收到錯誤資訊（X-Forwarded-Proto 錯會導致 redirect loop 或 secure cookie 失效）：

```nginx
proxy_set_header Host              $host;
proxy_set_header X-Real-IP         $remote_addr;
proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

## 驗證隔離有沒有真的生效

三個檢查點：`docker compose ps` 的 PORTS 欄只有 nginx 該出現 `0.0.0.0:80->80`；從 frontend 連 db 應失敗、從 backend 連 db 應成功（`docker compose exec <svc> sh -c "nc -zv db 5432"`）。精簡 image 多半沒裝 `nc`——改用 `getent hosts db` 驗名稱解析即可：frontend 應解析不到，backend 應解析到。

## 相關

- [[Nuxt-Docker-多階段構建]] — 同為 Docker 部署脈絡；其 static 模式即由 Nginx 出口

## 參考資料

- [Docker Docs - Networking overview](https://docs.docker.com/engine/network/)
- [Docker Docs - Networks（Compose 參考）](https://docs.docker.com/reference/compose-file/networks/)
