---
title: sr-only 導致 body scrollbar 的 bug
tags:
  - css
  - bug
  - frontend
  - tailwind
created: 2026-04-14
updated: 2026-04-14
---

## `sr-only` 導致 body scrollbar 的 bug

### 根本原因：`position: absolute` 缺少 positioned 祖先

`sr-only` 的 CSS 定義：
```css
position: absolute;
width: 1px;
height: 1px;
padding: 0;
margin: -1px;
overflow: hidden;
clip: rect(0,0,0,0);
white-space: nowrap;
border-width: 0;
```

當 `sr-only` 的父層沒有任何 positioned 祖先（`position: relative`、`absolute`、`fixed`、`sticky`）時，`position: absolute` 的 containing block 會回退到初始 containing block（≈ `<html>`），使元素脫離原本的版面邊界。搭配 `margin: -1px` 的偏移，便會溢出 body 觸發 scrollbar。

### 已知 issue

- Tailwind GitHub [#8571](https://github.com/tailwindlabs/tailwindcss/issues/8571) — sr-only in scrollable div influences body height
- Tailwind GitHub [#1648](https://github.com/tailwindlabs/tailwindcss/issues/1648) — sr-only adds a horizontal scrollbar on Chrome (mobile)
- Tailwind GitHub [Discussion #12429](https://github.com/tailwindlabs/tailwindcss/discussions/12429) — sr-only inside a div with overflow produces unwanted scroll

### 解法（優先順序）

1. **最推薦**：在 `sr-only` 元素的父層加 `position: relative`（建立 containing block）或 `overflow: hidden`
2. 將 `margin: -1px` 改為 `margin: 0`（略微降低螢幕閱讀器相容性）
3. 對 `body` 加 `overflow-x: hidden`（治標）
4. **不需無障礙支援時**：直接改用 `hidden` 完全隱藏