---
title: Safari Canvas Size 上限
created: 2026-06-03
updated: 2026-06-03
source: https://bugloop.com/issues/canvas-size
tags:
  - bug
  - frontend
  - javascript
  - css
---
# Safari Canvas Size 上限

## 問題背景

使用 [html2canvas](https://html2canvas.hertzen.com/) 將頁面轉成圖片時，若內容尺寸過大，Safari 會產生空白或截圖失敗的錯誤。

原因是 Safari 對 `<canvas>` 的**總面積（Total Area）有嚴格上限**，超過後 canvas 會被靜默清空（全白），不會拋出任何錯誤訊息，導致難以察覺。

> **注意**：當截圖內容的寬或高**任一邊超過 4,096px** 時，就需要特別留意此問題。這是 iOS Safari 最嚴格的限制邊界，一旦總面積超過 16,777,216（即 4,096 × 4,096），canvas 就會被靜默清空。

## 各瀏覽器上限

> 資料來源：[canvas-size](https://github.com/jhildenbiddle/canvas-size)
>
> 實際上限因裝置與瀏覽器版本而異，建議使用 `canvas-size` 套件動態偵測。

### Mobile

| Browser (OS)           | Max Width | Max Height |              Max Area (Total) |
| ---------------------- | --------: | ---------: | ----------------------------: |
| Chrome (Android)       |    32,767 |     32,767 | 16,384 x 16,384 (268,435,456) |
| Firefox (Android)      |    32,767 |     32,767 | 21,748 x 21,748 (472,907,776) |
| Safari (iOS >= 9)      |       N/A |        N/A |  4,096 x  4,096  (16,777,216) |

> Safari iOS 的單邊寬高技術上允許極大值，但實際受**總面積 16,777,216 px** 限制，例如 8,192 x 2,048 可行，但 4,097 x 4,097 則不行。

### Desktop

| Browser (OS)       | Max Width | Max Height |              Max Area (Total) |
| ------------------ | --------: | ---------: | ----------------------------: |
| Chrome (Mac, Win)  |    32,767 |     32,767 | 16,384 x 16,384 (268,435,456) |
| Edge (Mac, Win)    |    32,767 |     32,767 | 16,384 x 16,384 (268,435,456) |
| Firefox (Mac, Win) |    32,767 |     32,767 | 21,748 x 21,748 (472,907,776) |
| Safari (Mac)       |       N/A |        N/A | 16,384 x 16,384 (268,435,456) |

## iOS Safari 記憶體限制

除了面積上限外，iOS Safari 還有額外的記憶體上限限制：

- iOS Safari 15+：Canvas 記憶體上限約 **384 MB**
- 每個 4,096 x 4,096 的 Canvas 使用約 **64 MB**（4096 × 4096 × 4 bytes）
- 舊版 iOS 記憶體上限更低，裝置型號也會影響實際上限

## 解決方案

### 1. 動態偵測上限（推薦）

使用 [canvas-size](https://github.com/jhildenbiddle/canvas-size) 套件在截圖前偵測當前裝置的實際上限，再決定是否需要縮放或分段處理。

### 2. 降低 scale 參數

`html2canvas` 預設 `scale` 為 `window.devicePixelRatio`（Retina 螢幕通常為 2），將其降低可有效減少 canvas 面積：

```js
html2canvas(element, { scale: 1 })
```

### 3. 分段截圖後合併

若內容必須保持原始尺寸，可將頁面拆成多個區塊分段截圖，再用 canvas 或圖片處理工具合併為一張圖片。

### 4. 使用替代套件

[html-to-image](https://github.com/bubkoo/html-to-image) 對部分場景有更好的相容性，可作為 `html2canvas` 的替代方案評估。
