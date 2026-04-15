---
title: 測試 Desiderata 2.0
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-01-21
source: https://www.youtube.com/watch?v=IFrmfN1fxLg
---

Emily Bache 研究 25 份測試品質屬性清單，提出對 Kent Beck 12 項測試 Desiderata 的更新版本。

## 背景：Kent Beck 的 Test Desiderata

Kent Beck 在 2019 年發布 12 項「desiderata」（理想屬性），幫助開發者設計更好的測試。核心概念：沒有一個測試能同時滿足所有屬性，需要做取捨。

Emily Bache 研究了約 25 位作者的清單（包括 Dave Farley、Kevlin Henney 等），發現 Beck 的版本有兩個顯著問題。

## 關鍵發現：兩個異常的 Desiderata

### Fast（快速）
幾乎**所有**清單都包含這個屬性。原因：快速測試提供更快的回饋，而快速回饋是好工程的基礎。

### Predictive（預測性）
**幾乎沒有其他清單**提到這個屬性（Beck 獨有）。但 Emily 認為這是最重要的屬性之一。

> Predictive：執行完整測試套件後，能預測軟體是否沒有重大缺陷、是否適合部署到生產環境。

差異的原因：大多數作者關注**單個測試的屬性**，而 Predictive 是**整個測試套件**的屬性。

## 核心問題：混淆了兩個層次

Beck 把「單個測試的屬性」和「整個測試套件的屬性」放在同一份清單——這是根本的分類問題。

類比鞋子：「舒適、防水、好看」是評估**一雙鞋**的屬性；「整個衣櫃是否有適合各種天氣和場合的鞋」是評估**整個鞋櫃**的屬性。

## 四個 Macro Desiderata（測試套件層次）

Emily Bache 提出的 Testerata 2.0 框架，將所有個別測試屬性歸入四個更高層次的目標：

**1. Fast（快速）**
整個測試套件必須跑得夠快，才能在開發流程中持續使用。

**2. Predictive（預測性）**
整個套件必須能預測部署成功與否——如果所有測試都通過但生產環境仍有重大 bug，測試套件就沒有達到這個目標。

**3. 低總持有成本（Low Total Cost of Ownership）**
包括撰寫、維護、執行測試的成本。大多數個別測試的屬性（可讀性、獨立性等）都服務於這個目標。

**4. 支持持續開發（Support Ongoing Development）**
測試應協助我們理解要建立什麼、以及設計出好的程式碼結構。在 TDD/BDD 中尤其明顯——測試本身是設計工具，不只是驗證工具。

## 結論

Beck 的 12 項 Desiderata 並不完整，但更根本的問題是**層次混淆**。

優秀開發者在優化測試時，實際上是在優化整個測試套件朝向四個 Macro 目標：快速、可預測、低成本、支持開發。所有個別測試屬性都是在服務這四個目標中的一個或多個。
