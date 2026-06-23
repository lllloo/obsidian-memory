---
title: 圖片上傳後畫面會旋轉
created: 2026-06-03
updated: 2026-06-23
tags:
  - bug
  - frontend
  - javascript
---
# 圖片上傳後畫面會旋轉

本文件說明手機拍照上傳圖片後，常見方向顯示異常的原因，並提供前端與後端處理建議，協助解決圖片旋轉問題。

## 問題描述

手機拍照並上傳圖片時，雖然在手機本身顯示正常，但在部分瀏覽器或裝置上可能出現方向異常（如橫向變直向、倒置等）。
造成此問題的原因如下：

- 手機拍照時，圖片會記錄 EXIF 方向資訊，手機端能正確解析並顯示。
- 現代瀏覽器以 `<img>` / `background-image` 直接顯示 JPEG 時，已預設依 EXIF 方向轉正（`image-orientation: from-image`，Chrome 81+、Firefox、Safari 皆然），通常不會顯示異常。方向問題主要出現在**不套用 EXIF 的處理路徑**——如用 canvas `drawImage`、`FileReader` + canvas 做預覽，或 EXIF 被剝除／未保留時。
- 圖片上傳後若 EXIF 資訊被移除或未正確處理，也會造成方向錯誤。

## 前端處理方式

- 使用 exif-js 讀取 EXIF 資訊，判斷圖片原始方向，並使用 JavaScript 修正圖片方向。

### 實作步驟

1. 安裝 exif-js（可用 CDN 或 npm）。
2. 讀取圖片檔案並取得 EXIF Orientation 資訊。
3. 根據 Orientation，使用 canvas 旋轉圖片至正確方向。
4. 將修正後的圖片顯示或上傳。

## 後端處理方式

- 伺服器端自動修正圖片方向，移除 EXIF 方向資訊。

## 結論

建議由後端統一處理圖片方向問題，於圖片上傳時先判斷 EXIF 方向並自動轉正，移除或修正 EXIF 方向資訊，確保所有裝置與瀏覽器皆能正確顯示圖片，簡化前端負擔並提升使用者體驗。

## 參考資料

- [exif-js](https://github.com/exif-js/exif-js)
