---
title: CSS 換行
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/css/newline
tags:
  - css
  - frontend
  - tailwind
---

# CSS 換行

本文說明 CSS 中處理文字換行的各種屬性與技巧，提供常用的換行解決方案與程式碼範例。適合前端開發者參考使用。

## 結論

### 英文字太長自動換行（先換行再斷行）

```css
overflow-wrap: break-word;
/* tailwind */
.break-words
```

適用於避免英文單字過長導致版面溢出。

### 英文字太長直接斷行

```css
overflow-wrap: break-word;
word-break: break-all;
/* tailwind */
.break-words .break-all
```

適用於強制英文單字在任何位置斷行。

### 禁止自動換行

```css
white-space: nowrap;
```

適用於單行顯示、避免自動換行。

## CSS 換行屬性說明

### overflow-wrap / word-wrap

- `overflow-wrap` 用於指定是否允許單詞內換行。
- `word-wrap` 是 `overflow-wrap` 的舊稱，語意相同。
- 常用值：
  - `normal`（預設）：使用瀏覽器預設換行規則。
  - `break-word`：允許單詞內部換行，單字過長時自動斷行。

```css
overflow-wrap: break-word;
word-wrap: break-word;
```

### word-break

- 控制單詞或字串的斷行方式。
- 常用值：
  - `normal`（預設）：標準斷行規則。
  - `break-all`：非 CJK 文本可在任意字元間斷行。

```css
word-break: break-all;
```

### white-space

- 控制元素內空白字元與換行的呈現方式。
- 常用值：
  - `normal`（預設）：連續空白合併，遇到邊界自動換行。
  - `nowrap`：所有內容在同一行顯示，不自動換行。
  - `pre`：保留所有空白與換行，類似 `<pre>` 標籤。
  - `pre-wrap`：保留空白與換行，並在邊界自動換行。
  - `pre-line`：合併多餘空白，保留換行，遇到邊界自動換行。

```css
white-space: pre-wrap;
white-space: nowrap;
```

## 保留空白與換行

- `white-space: pre-wrap;` 可保留空白字元與換行符號。
- 搭配 `overflow-wrap: break-word;` 可避免溢出。

```css
.css {
  white-space: pre-wrap;
  overflow-wrap: break-word;
}
```

- tailwind：`whitespace-pre-wrap break-words`

## 單行文字溢出顯示省略號

單行文字過長時可用 CSS 讓多餘部分以省略號顯示：

```css
.ellipsis {
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
```

- tailwind：`overflow-hidden whitespace-nowrap text-ellipsis`

## 多行文字溢出顯示省略號

多行截斷可用 CSS line-clamp 技巧，搭配 tailwind 實現：

```css
.multi-ellipsis {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2; /* 顯示 2 行，可依需求調整 */
}
```

- tailwind：`line-clamp-1`、`line-clamp-2` ...

## 參考資料

- [Tailwind CSS 文檔](https://tailwindcss.com/docs/word-break)
