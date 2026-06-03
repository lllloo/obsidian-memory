---
title: 最後一行移除下邊框
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/notes/css/remove-last-row-border
tags:
  - css
  - frontend
---

# 最後一行移除下邊框

說明：本檔案示範在三欄（每行 3 個）或類似欄位佈局中，如何使用 SCSS 選擇器移除最後一行或不足欄數項目的下邊框，避免出現多餘的分隔線。

## 移除最後一行（或最後幾個）項目的下邊框

下方為一個三欄式（每行 3 個）的 SCSS 範例，用以示範如何在最後一行移除下邊框：

```scss
.three-part {
  > div {
    width: calc(100% / 3);
    /* 使用下邊框（底部分隔線） */
    border-bottom: 1px solid #ccc;
    &:nth-last-child(1) {
      /* 只有一個元素時移除下邊框 */
      border-bottom: none;
    }
    &:nth-last-child(2) {
      &:nth-child(3n + 1),
      &:nth-child(3n + 2) {
        /* 最後一行有兩個元素時，根據位置移除下邊框 */
        border-bottom: none;
      }
    }
    &:nth-last-child(3) {
      &:nth-child(3n + 1) {
        /* 最後一行剛好三個元素時，移除第一個位置的下邊框（視版型需求） */
        border-bottom: none;
      }
    }
  }
}
```

上面的 SCSS 範例用於三欄式排列（每行 3 個項目）的情況，目的是在最後一行（不足 3 個或剛好 3 個的情況）移除不必要的邊框，避免在項目結尾出現多餘的分隔線。

主要想法：

- 當只有 1 個元素在最後一行：移除該元素的邊框（`:nth-last-child(1)`）。
- 當最後一行有 2 個元素時：移除最後兩個元素中對應會顯示下邊框的那些（透過 `:nth-child(3n + 1)` / `3n + 2` 配合 `:nth-last-child(2)`）。
- 當最後一行有 3 個元素時：只需移除會是該列第一個位置的元素（`3n + 1`），視排版邏輯而定。
