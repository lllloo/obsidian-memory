---
title: 取得 ER 圖的快速途徑
description: 只想要一張 ER 圖又不想碰 diagram 語法時的三條路：GUI 直開、tbls 產 svg、Azimutt 互動切片，兼談 PlantText 的定位
created: 2026-08-11
updated: 2026-08-17
parent: "[[wiki/01.index]]"
tags:
  - diagram-as-code
  - automation
---

本頁是 [[不讀碼時該看哪些圖]] ② ER 切片圖的**執行面補充**：該頁答「為什麼 ER 圖值得看、為什麼要切片」，本頁答「今天就想看到一張 ER 圖，走哪條路最短」。核心前提沿用該頁查證結論，此處不重複舉證，只標來源；本頁新增的工具事實凡未經查證者一律標註。

## 先釐清：PlantText 這類工具的定位

PlantText（planttext.com）是 PlantUML 的免費線上編輯器——左邊寫語法、右邊渲染（此定位屬通用知識，未查證）。把它用在 ER 圖上要注意兩件事：

1. **手寫 ER 圖會過期**：[[不讀碼時該看哪些圖]] 已查證，Mermaid／PlantUML／D2／Structurizr 沒有任何一個能檢查「圖是否還符合實際 schema」，語法驗證只驗語法。ER 圖的價值正在於它是「從 DB metadata 自動產、唯一可信」的圖，手寫即弄丟此性質。
2. 因此這類工具的正確位置是**渲染端而非書寫端**——上游由工具從 DB 重生文字（tbls 可輸出 PlantUML），貼進去只為看圖。而如果目的只是看圖，連這一步都可省：下面三條路全都不需要碰任何 diagram 語法。

**手寫仍有意義的唯一場景**：DB 還不存在、正在設計新表的草稿階段（PlantText／dbdiagram.io／QuickDBD 這類工具在此場景的比較未查證）。

## 三條路（按省事程度排）

| 路徑 | 適用 | 產物去向 |
|---|---|---|
| GUI 直開（DBeaver／phpMyAdmin） | 一次性看懂 | 留在工具裡，不進版控 |
| `tbls doc` 產 svg | 要留檔、要防過期 | commit 進 repo，CI 掛 `tbls diff` |
| Azimutt 互動探索 | 表很多的 legacy 大庫 | 每個 use case 存一張視圖 |

### 1. GUI 直開

- **DBeaver**：連上 DB 後每個 schema 自帶 ER Diagram 分頁，點開即有；[[不讀碼時該看哪些圖]] 查證中它是唯一提供 ER 記法選項的工具（做成檢視時即時切換）。「自帶 ER 分頁」這一句本身屬通用知識，未逐項查證。
- **phpMyAdmin Designer 分頁**：能拉出關聯圖，Laradock 環境零安裝（入口做法見使用者 topics 筆記）。⚠️ 通用知識，未查證。

### 2. tbls 直接吐 svg——預設輸出就是 svg，不經任何 diagram 語言

```bash
tbls doc mysql://user:pass@localhost:3306/mydb docs/schema
```

產出整組 markdown 文件＋每張表一個 ER svg，`distance` 預設 1，天然就是切片。兩個提醒（皆出自 [[不讀碼時該看哪些圖]] 的查證）：

- **先確認 schema 有沒有宣告 FK**——如 Laravel migration 沒寫 `foreignId()->constrained()`，圖上會沒有邊；讀圖前先確認每條邊是宣告的還是推論的。
- 要與 DB 保持一致就把產物 commit，CI 掛 `tbls diff` 抓漂移（diff 才是漂移偵測、lint 是品質檢查；exit code 行為 README 未載明，非開箱即擋 PR）。

### 2.5 SchemaSpy 實測補充（2026-08-11 本機單次實測，非查證研究）

[[不讀碼時該看哪些圖]] 列的另一條成熟路線，實跑後補三個執行面事實：

- **官方 Docker image 免裝 JVM／Graphviz**，掛進 compose 網路即可連容器內 DB，77 張表約 14 秒跑完：

  ```bash
  docker run --rm --network <compose網路名> -v "$PWD/out:/output" \
    schemaspy/schemaspy -t mariadb -host <db服務名> -port 3306 \
    -db <庫名> -s <庫名> -u <帳號> -p <密碼>
  ```

  `-s`（schema）**必給**，漏了會報 `Bad config: Schema was not provided`。產出為可瀏覽 HTML 站：`index.html`（每表有 degree 1／2 切片圖）、`relationships.html`（real／implied 雙版本）、`orphans.html`（孤島表專頁）、`anomalies.html`（schema 異味清單）。
- **隱含關聯推論對 Laravel／Rails 式命名結構性失效**：推論法是「欄位名＋型別比對他表主鍵名」，而此類慣例的主鍵一律叫 `id`、引用欄叫 `xxx_id`，名字永遠對不上，推論一條真關聯都抓不到；能撞名的反而是 `email` 這類泛用欄（實測 77 表僅推出 4 條、全為誤報，皆為各表 `email` 欄被連到 `password_reset_tokens.email`）。這把 [[不讀碼時該看哪些圖]] 的「誤報實質存在」再收窄一層：對 ORM 慣例命名的庫，**推論不只會誤報、還會漏光真陽性**——孤島表的真實關聯只能回程式碼層查 ORM 關聯宣告（`belongsTo`／`hasMany`／join）。
- 據此修正本頁定位：SchemaSpy 對「沒宣告 FK 的孤島」的價值**僅在孤島清單本身**（`orphans.html`），不在補出關聯。

### 3. Azimutt 互動探索

載入後預設空白 → 搜尋一張起點表 → 沿關聯往外點 → 每個 use case 存一張視圖。比靜態圖更貼近「探索陌生大庫」的需求，同樣讀 metadata、不手寫。

## 與本 vault 呈現拍板的交點

Mermaid 已於 2026-08-06 全面停用（含 mermaid.live，見 [[AI-生成流程圖與架構圖]]），故 tbls 的 mermaid 輸出格式不採用；走 svg（預設）即可，給人看的呈現載體現行為本地 HTML 或直接開 svg。跨 repo 提醒：實際對某專案 DB 產圖，回該專案 repo 的 session 做，不在 vault 內進行。
