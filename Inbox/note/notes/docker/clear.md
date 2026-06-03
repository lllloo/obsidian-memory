---
title: Docker 資源清理指令彙整
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/docker/clear
tags:
  - docker
  - cli
---

# Docker 資源清理指令彙整

這份文件說明如何在 Docker 中移除不必要的資源（如未使用的容器、映像檔、網路、資料卷等），以釋放磁碟空間，並提供常用清理指令與注意事項。

## 查看目前使用空間

在清理前，先確認目前的磁碟使用狀況：

```sh
docker system df
```

輸出範例：

```text
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          12        3         2.45GB    1.87GB (76%)
Containers      5         2         128MB     96MB (75%)
Local Volumes   8         2         512MB     384MB (75%)
Build Cache     24        0         890MB     890MB
```

| 欄位 | 說明 |
| --- | --- |
| TYPE | 資源類型（映像檔、容器、資料卷、Build Cache） |
| TOTAL | 該類型的總數量 |
| ACTIVE | 目前正在使用中的數量 |
| SIZE | 佔用的磁碟空間 |
| RECLAIMABLE | 可回收（清理後可釋放）的空間 |

加上 `-v` 可查看每個資源的詳細資訊：

```sh
docker system df -v
```

## 一鍵清除所有未使用資源

清除下列資源：

- 停止的容器
- 未使用的網路
- 沒有被任何容器使用的映像檔
- 建立時產生的中間暫存層

```sh
docker system prune
```

執行後會先顯示確認提示：

```text
WARNING! This will remove:
  - all stopped containers
  - all networks not used by at least one container
  - all dangling images
  - all dangling build cache

Are you sure you want to continue? [y/N]
```

加上 `--force` 可略過確認提示，適合在自動化腳本中使用：

```sh
docker system prune --force
```

加上 `--volumes` 同時清除未使用的資料卷（預設不清除）：

```sh
docker system prune --volumes
```

::: warning 注意
`--volumes` 會一併移除未被任何容器掛載的資料卷，請確認資料卷內無重要資料再執行。
:::

更徹底加上 `-a`，額外刪除所有**未使用**的映像檔（包括已經建構但未被執行的）：

```sh
docker system prune -a
```

::: warning 注意
此指令會移除所有未被任何容器使用的映像檔，請確認無需保留再執行。
:::

## 移除已停止的容器

容器在 `docker stop` 或程式執行完畢後進入「已停止（Exited）」狀態，不會自動刪除，久了會累積佔用空間。

先用以下指令確認哪些容器處於停止狀態：

```sh
docker ps -a
```

輸出範例（STATUS 為 `Exited` 的即為已停止）：

```text
CONTAINER ID   IMAGE         COMMAND      STATUS                    NAMES
a1b2c3d4e5f6   nginx         "/docker…"   Exited (0) 2 days ago    web-old
f6e5d4c3b2a1   postgres:14   "docker…"    Up 3 hours               db
```

確認無誤後，移除所有已停止的容器：

```sh
docker container prune
```

加上 `--force` 略過確認提示：

```sh
docker container prune --force
```

::: tip 提醒
正在執行（`Up`）的容器不會受此指令影響。
:::

## 移除未使用的映像檔

### 懸掛映像檔（dangling image）

懸掛映像檔是指沒有標籤（tag）且未被任何容器使用的映像檔，通常由重複 `docker build` 後產生。每次重新建構同一個 tag 的映像檔，舊的映像層就會失去 tag 成為懸掛映像檔。

移除懸掛映像檔：

```sh
docker image prune
```

加上 `-a` 可刪除所有未被任何容器使用的映像檔（包含有 tag 但未被使用的）：

```sh
docker image prune -a
```

::: warning 注意
`-a` 參數會移除所有未被任何容器使用的映像檔，請確認無需保留再執行。
:::

使用 `--filter` 只移除特定條件的映像檔，例如移除 24 小時前建立的：

```sh
docker image prune -a --filter "until=24h"
```

也可以指定更長的時間範圍，例如 7 天前：

```sh
docker image prune -a --filter "until=168h"
```

## 移除未使用的網路

移除所有未被任何容器使用的自訂網路：

```sh
docker network prune
```

::: tip 提醒
以下三個 Docker 內建預設網路不受此指令影響，永遠不會被移除：

- `bridge`：容器預設使用的橋接網路
- `host`：直接使用宿主機網路
- `none`：完全隔離，無網路
:::

## 移除未使用的資料卷

::: danger 警告
資料卷（Volume）通常用於儲存持久化資料，例如資料庫的資料檔案。移除後**無法恢復**，請務必謹慎操作。
:::

先確認目前存在哪些資料卷及其使用狀況：

```sh
docker volume ls
```

輸出範例：

```text
DRIVER    VOLUME NAME
local     mysql_data
local     redis_data
local     my-project_uploads
```

確認哪些資料卷真的沒有在使用後，再移除未被任何容器掛載的資料卷：

```sh
docker volume prune
```

## 參考資料

- [Docker Official Documentation - docker system prune](https://docs.docker.com/reference/cli/docker/system/prune/)
