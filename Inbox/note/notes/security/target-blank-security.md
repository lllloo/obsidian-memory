---
title: 安全使用 target="_blank" 的方式
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/security/target-blank-security
tags:
  - security
  - frontend
---

# 安全使用 target="\_blank" 的方式

本文件說明使用 `target="_blank"` 開啟新分頁時可能面臨的安全風險，並提供完整的解決方案來防止「反向標籤劫持」（Reverse Tabnabbing）攻擊，適合前端開發者了解與實作安全的外部連結。

## 安全風險說明

### 什麼是反向標籤劫持攻擊

當使用 `target="_blank"` 開啟外部連結時，新開啟的頁面會獲得原始頁面的 `window.opener` 參考，這讓惡意網站有機會操控原始頁面。

**攻擊流程：**

1. 使用者點擊含有 `target="_blank"` 的連結
2. 新分頁開啟後，惡意網站取得 `window.opener` 物件
3. 惡意網站透過 `window.opener.location` 將原始頁面導向釣魚網站
4. 使用者回到原始分頁時，看到的是偽造的釣魚頁面

### 潛在風險

- **釣魚攻擊**：原始頁面被導向看似合法的釣魚網站
- **資料竊取**：使用者可能在釣魚網站輸入敏感資訊
- **信任濫用**：利用使用者對原始網站的信任進行詐騙

---

## 不安全的寫法

以下是容易受到攻擊的常見寫法：

```html
<!-- ❌ 危險：僅使用 target="_blank" -->
<a href="https://external-site.com" target="_blank"> 查看外部網站 </a>

<!-- ❌ 危險：JavaScript 開啟新視窗 -->
<button onclick="window.open('https://external-site.com')">開啟外部網站</button>
```

**為什麼不安全：**

- 新開啟的頁面可以透過 `window.opener` 存取原始頁面
- 惡意網站可以執行 `window.opener.location = 'https://fake-site.com'`
- 原始頁面會在背景被重新導向到惡意網站

---

## 安全的解決方案

::: tip 現代瀏覽器已預設保護
Chrome 88+、Firefox 79+、Safari 12.1+ 等現代瀏覽器已將 `target="_blank"` 的預設行為改為自動套用 `rel="noopener"`，不再讓新頁面存取 `window.opener`。

仍建議明確寫出 `rel="noopener"`，以確保在舊版瀏覽器的相容性，並讓程式碼意圖更清楚。
:::

### 方案一：使用 rel="noopener"

這是最主要的解決方案，可以阻斷新頁面對原始頁面的存取：

```html
<!-- ✅ 安全：使用 rel="noopener" -->
<a href="https://external-site.com" target="_blank" rel="noopener">
  查看外部網站
</a>

<!-- ✅ 更安全：同時使用 noopener 和 noreferrer -->
<a href="https://external-site.com" target="_blank" rel="noopener noreferrer">
  查看外部網站
</a>
```

**屬性說明：**

- `rel="noopener"`：防止新頁面存取 `window.opener`
- `rel="noreferrer"`：不傳送 HTTP Referer 標頭，增加隱私保護

### 方案二：JavaScript 安全開啟新視窗

當需要用 JavaScript 開啟新視窗時，確保清除 `opener` 參考：

```javascript
// ✅ 安全的 JavaScript 寫法
function openSafeWindow(url) {
  const newWindow = window.open(url, '_blank', 'noopener,noreferrer')

  // 額外保護：手動清除 opener 參考
  if (newWindow) {
    newWindow.opener = null
  }
}

// 使用範例
document
  .getElementById('external-link')
  .addEventListener('click', function (e) {
    e.preventDefault()
    openSafeWindow('https://external-site.com')
  })
```

## 注意事項

- 使用 `rel="noreferrer"` 會阻止瀏覽器傳送 HTTP Referer，外部網站無法得知流量來源，可能影響 SEO 分析與流量統計。
- 若希望保留 Referer 以利 SEO 分析，僅使用 `rel="noopener"` 即可，避免加上 `noreferrer`。
- 針對重要外部連結，建議根據實際需求選擇是否加上 `noreferrer`。

## 參考資料

[MDN - rel="noopener"](https://developer.mozilla.org/en-US/docs/Web/HTML/Link_types/noopener)
[MDN - rel="noreferrer"](https://developer.mozilla.org/en-US/docs/Web/HTML/Link_types/noreferrer)
[OWASP - Reverse Tabnabbing](https://owasp.org/www-community/attacks/Reverse_Tabnabbing)
[Google Web Fundamentals - External links](https://web.dev/external-anchors-use-rel-noopener/)
[Can I use - rel=noopener](https://caniuse.com/rel-noopener)
