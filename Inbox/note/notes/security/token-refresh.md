---
title: "登入系統 Token 機制：Access Token 與 Refresh Token"
created: 2026-06-03
updated: 2026-06-04
tags:
  - security
  - frontend
  - api
---

# 登入系統 Token 機制：Access Token 與 Refresh Token

在現代 Web 應用程式開發中，基於 Token 的驗證（Token-based Authentication）已是標準配備。為了在「安全性」與「使用者體驗」之間取得最佳平衡，雙 Token 機制（Access Token + Refresh Token） 是目前業界的主流做法。

本文將深入探討其運作原理、存放位置的選擇策略（LocalStorage vs Cookie），以及實作的最佳實踐。

## 核心機制：雙 Token 設計

為什麼登入後不給一個 Token 就好，而要給兩個？

### Access Token (存取權杖)

- 角色：使用者的「通行證」。
- 用途：附帶在每個 API 請求中（Header），證明「我是誰」以及「我有什麼權限」。
- 格式：通常為 JWT (JSON Web Token)，內含 User ID、Role 等資訊。
- 效期：極短（例如：15 分鐘 ~ 1 小時）。
- 特點：因為驗證時通常不查資料庫（Stateless），一旦發出就很難收回。所以必須設定短效期，萬一被竊取，駭客能作惡的時間也很短。

### Refresh Token (更新權杖)

- 角色：用來換取新通行證的「憑證」。
- 用途：當 Access Token 過期時，發送給 Authentication Server 以換取新的 Access Token。
- 格式：可以是隨機字串或 JWT，通常儲存在後端資料庫中以支援撤銷（Revoke）。
- 效期：長（例如：7 天 ~ 30 天）。
- 特點：權限極大（擁有它 = 擁有無限 Access Token），因此儲存安全性要求極高。

## Token 存放位置比較

前端該把 Token 存在哪裡？這是開發者最常爭論的話題。主要選項有 Memory (變數)、LocalStorage 與 Cookie。

### 比較總表

| 儲存位置             | 存取方式           | XSS 風險        | CSRF 風險   | 容量       | 自動過期     | 傳輸特性           |
| :------------------- | :----------------- | :-------------- | :---------- | :--------- | :----------- | :----------------- |
| Memory (JS 變數)     | 程式變數           | 最低 (難以竊取) | 無          | 記憶體限制 | 頁面重整即逝 | 手動放入 Header    |
| LocalStorage         | `localStorage` API | 高 (JS 可讀)    | 無          | 大 (5MB+)  | 否 (永久)    | 手動放入 Header    |
| Cookie (非 HttpOnly) | `document.cookie`  | 高 (JS 可讀)    | 有 (需防禦) | 小 (4KB)   | 有           | 自動隨每個請求發送 |
| HttpOnly Cookie      | Server 設定        | 無 (JS 不可讀)  | 有 (需防禦) | 小 (4KB)   | 有           | 自動隨每個請求發送 |

### 為什麼 Access Token 不建議放在一般 Cookie？

雖然它跟 LocalStorage 一樣都有 XSS 風險，但它集結了所有缺點：

1. 浪費頻寬：瀏覽器會自動把 Cookie 帶到每一個請求（包含圖片、CSS）。Access Token (JWT) 體積很大，這會造成嚴重的流量浪費。
2. 容量太小：只有 4KB，JWT 稍微多帶點資訊就塞不下了。
3. API 難用：`document.cookie` 是字串處理，不如 `localStorage` 的 Key-Value API 直覺。
4. 優點無力：雖然它有「自動過期」功能，但 JWT 本身就有 `exp` 欄位，後端驗證過期一樣會擋，前端也能靠邏輯判斷，所以此優點無法抵消上述缺點。

### 為什麼不全部使用 HttpOnly Cookie？

雖然 HttpOnly Cookie 防禦了 XSS，但：

1. CSRF 風險：因為 Cookie 會自動發送，惡意網站可以偽造請求。你必須額外實作 CSRF Token 機制。而 LocalStorage/Memory 需要 JS 主動讀取並放入 Header，天然免疫 CSRF。
2. 前端無法讀取：前端 JS 讀不到 Cookie 內容，就無法解析 JWT 裡的資訊（如 User ID、過期時間），導致前端難以做狀態判斷（例如：是否該顯示「管理員」按鈕）。

## 最佳實踐建議

綜合以上分析，我們推薦以下組合：

### 方案 A：極致安全 (金融/支付類應用)

- Access Token：放在 Memory (JS 變數)。
  - 優點：XSS 攻擊也偷不到。
  - 缺點：重新整理頁面 Token 就沒了。
  - 解法：App 初始化時，主動呼叫 `/refresh-token` 取得新的 Access Token。
- Refresh Token：放在 HttpOnly Cookie。
  - 設定：`HttpOnly; Secure; SameSite=Strict`。
  - 優點：JS 偷不到，且只在 `/refresh-token` 請求時自動帶上，路徑單純，CSRF 風險可控。

### 方案 B：開發便利與體驗平衡 (一般應用)

- Access Token：放在 LocalStorage。
  - 優點：實作簡單，重整頁面登入狀態還在，且免疫 CSRF。
  - 缺點：若有 XSS 漏洞，Token 會被偷。
- Refresh Token：放在 HttpOnly Cookie。
  - 堅持：這是底線，Refresh Token 權限太大，絕對不能讓 JS 碰觸。

## 運作流程

1. 登入 (Login)：
   - Client 傳送帳號密碼。
   - Server 驗證通過，回傳 Access Token (JSON) 並設定 Refresh Token (HttpOnly Cookie)。
2. 存取資源 (Access)：
   - Client 將 Access Token 放入 `Authorization: Bearer <token>` Header 發送請求。
   - Server 驗證 Access Token 有效，回傳資料。
3. 過期與刷新 (Expiration & Refresh)：
   - Client 發送請求，Server 回應 401 Unauthorized。
   - Client 的攔截器 (Interceptor) 捕獲 401 錯誤。
   - Client 呼叫 `/refresh-token` API（瀏覽器自動帶上 HttpOnly Cookie）。
   - Server 驗證 Refresh Token 有效，回傳新的 Access Token。
   - Client 更新本地 Token，並重試 (Retry) 原本失敗的請求。
4. 完全失效：
   - 若 Refresh Token 也過期，Server 回傳錯誤，Client 強制登出並導向登入頁。

## 參考資料

- [MDN - HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)
- [OWASP - Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [Auth0 - Refresh Tokens](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)
