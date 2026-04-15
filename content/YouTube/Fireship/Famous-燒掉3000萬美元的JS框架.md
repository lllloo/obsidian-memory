---
title: 燒掉 3000 萬美元的 JavaScript 框架：Famous 的興衰
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-18
source: https://www.youtube.com/watch?v=ReAnFFqvCeA
---

## 背景：Famous 的誕生

- 2012 年，一家名叫 Bench Rank 的新創公司（「如果 LinkedIn 和 Hot or Not 生了個孩子」）在解決 HTML5 效能瓶頸時，發現了一個技巧：透過 hack `matrix3D` CSS 屬性，將渲染工作推給 GPU
- 這家公司放棄原本的 reputation system 概念，轉型做以 GPU 加速為核心的渲染引擎——就是 Famous
- 他們以這個概念募資 **3000 萬美元**，打著「一套程式碼跑遍所有裝置」的願景
- Famous 的架構：所有元素使用笛卡爾座標系絕對定位，以 4x4 矩陣輸出為 `matrix3D` CSS 屬性

## 為什麼失敗

- **2014 年才發佈可用版本**（2012 年宣佈），錯過最佳時機窗口
- **瀏覽器本身進步了**：GPU 合成與動畫排程成為標準，Famous 的性能優勢縮水
- **生態系改變**：需要複雜 3D GPU 介面的 → Three.js；需要一般介面的 → React（宣告式 UI）
- **API 難以上手**：需要深度理解數學、物理與 JavaScript
- **商業模式問題**：高峰期 25 名員工，創辦人不相信 lean startup，試過主機代管與監控服務都沒成功
- 最終裁掉整個工程團隊，硬轉型做行銷網站 CMS，也失敗了

## 歷史評價

- Famous 嘗試繞過瀏覽器限制「提前發貨未來」，這是它既誘人又脆弱的原因
- 雖然失敗，但推動了業界對效能與 UI 野心的期望
- 網站目前已出售
