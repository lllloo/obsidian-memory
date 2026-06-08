---
title: 拿不到 Content-Disposition
created: 2026-06-03
updated: 2026-06-08
tags:
  - bug
  - frontend
  - api
  - http
---

# 拿不到 Content-Disposition

前端用 `res.headers.get('Content-Disposition')` 讀下載檔名卻拿到 `null` 時，第一直覺常是「程式碼寫錯」，但真正原因幾乎都在**回應標頭被傳輸鏈中間層攔掉**，不在前端。最典型的訊號是：**本地開發正常、一上線就消失**。

## 為什麼「本地有、線上沒有」

本地透過 dev server proxy（webpack、Vite、local nginx）轉發 API，proxy 通常原封轉發所有標頭，所以讀得到。上線後請求會穿過雲端代理（Cloudflare、AWS ELB）或 CDN，這些中間層可能預設不轉發非標準標頭，`Content-Disposition` 就在這一層被吃掉。

**環境差異本身就是定位線索**：問題在哪一段傳輸鏈，由「哪個環境會壞」直接指出來——不必先懷疑前端程式碼。

## 關鍵判斷：null 的兩種本質

`headers.get()` 回 `null` 有兩種完全不同的成因，混淆會修錯方向：

- **標頭沒送達**——源站根本沒設，或中間層（CDN／代理）把它過濾掉。
- **標頭送達、但 JS 沒權限讀**——跨域時瀏覽器預設只放行少數 safelisted 標頭，`Content-Disposition` 必須由伺服器在 `Access-Control-Expose-Headers` 明列才讀得到。

**一眼分辨**：DevTools Network 看得到這個標頭、但 `headers.get()` 拿到 null —— 就是後者（CORS 沒 expose）；DevTools 也沒有 —— 就是前者（沒送達）。

## 排查與修法

CORS 沒 expose 是最常被忽略、也最好修的——伺服器加一行：

```js
// Express
res.setHeader('Access-Control-Expose-Headers', 'Content-Disposition')
res.setHeader('Content-Disposition', 'attachment; filename="example.txt"')
```

要切出「源站沒給」還是「中間層吃掉」，用 `curl -I` 直打源站，對比瀏覽器所見：

```sh
curl -I https://your-api/file
```

源站有、瀏覽器沒有 → 中間層（Nginx／Cloudflare）過濾，調代理設定；源站就沒有 → 伺服器補上標頭。

## 參考資料

- [MDN - Access-Control-Expose-Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Access-Control-Expose-Headers)
