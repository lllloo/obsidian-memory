---
title: 拿不到 Content-Disposition 的原因與解決方式
created: 2026-06-03
updated: 2026-06-04
tags:
  - bug
  - frontend
  - api
  - http
  - nginx
---
# 拿不到 Content-Disposition 的原因與解決方式

在前端或後端開發中，常常需要從 HTTP 回應中取得 `Content-Disposition` 標頭，來判斷檔案下載的檔名或附件資訊。不過，有時候會遇到「拿不到 Content-Disposition」的情況，本文整理常見原因與解決方式，並說明本地 proxy 有資料但線上卻沒有的狀況。

## 本地 proxy 有資料，線上卻沒有的情況

在本地開發時，通常會使用 proxy（如 webpack dev server、local nginx）來轉發 API 請求。這時 proxy 可能會保留所有 HTTP 標頭，因此能順利取得 `Content-Disposition`。

但推到線上環境時，若使用了雲端代理（如 Cloudflare、AWS ELB）或 CDN，這些中間層可能預設移除或未正確轉發 `Content-Disposition` 標頭，導致前端拿不到資料。

## 常見原因

1. **伺服器未設定 Content-Disposition**
   - 有些 API 或檔案伺服器預設不會加上 `Content-Disposition` 標頭，導致前端或程式端無法取得。
2. **跨域 (CORS) 限制**
   - 如果伺服器未在 `Access-Control-Expose-Headers` 中明確列出 `Content-Disposition`，瀏覽器無法存取該標頭。
3. **代理或 CDN 過濾**
   - 某些代理伺服器或 CDN 可能會移除部分標頭，造成客戶端拿不到。

## 解決方式

### 1. 檢查伺服器回應

可用瀏覽器開發者工具或 curl 指令檢查伺服器是否有正確回傳 `Content-Disposition` 標頭：

```sh
curl -I https://your-api/file
```

### 2. 設定 CORS 標頭

如果是跨域請求，伺服器需在回應中加上：

```http
Access-Control-Expose-Headers: Content-Disposition
```

範例（Node.js Express）：

```js
res.setHeader('Access-Control-Expose-Headers', 'Content-Disposition')
res.setHeader('Content-Disposition', 'attachment; filename="example.txt"')
```

### 3. 檢查代理或 CDN 設定

確認中間層（如 Nginx、Cloudflare）是否有移除或過濾標頭，必要時調整設定。

## 前端取得方式

以下範例說明如何在前端取得 Content-Disposition 標頭：

```js
fetch('https://your-api/file').then((res) => {
  const disposition = res.headers.get('Content-Disposition')
  // disposition 可能為 null，需檢查
})
```

## 結論

「拿不到 Content-Disposition」通常是伺服器設定、CORS 限制或代理/CDN 過濾造成。建議先檢查伺服器回應，再確認跨域標頭設定，最後排查代理或 CDN 問題。
