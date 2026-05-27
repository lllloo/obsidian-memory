---
title: AI Design 三層工作流
created: 2026-05-26
updated: 2026-05-27
source: https://www.youtube.com/watch?v=5lycYTOYbPM
published: 2026-05-24
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - design
  - frontend
  - design-system
---

## 核心觀點

AI 產生的設計看起來像客製作品或像 AI 套版，不只取決於模型能力，而取決於工作流層級。影片把 AI design 分成三層：單頁設計、跨頁設計系統、用測試與視覺 diff 驗證設計。

## Level 1：單頁設計

第一層是讓 agent 做出一個不 generic 的單頁。關鍵不是只說「做一個 landing page」，而是把設計意圖、不可妥協的元素、色彩系統、對比、字體、layout rhythm、responsive 行為與反模式寫清楚。

影片特別強調幾個控制點：

- 用設計目的決定對稱或不對稱 layout。
- 明確指定色彩系統，例如 OKLCH 這類更貼近人眼感知的表示方式。
- 用 contrast 建立視覺階層，不讓所有元素同等重要。
- 指定字體策略，也明確列出不要使用的 AI 常見套版字體。
- 把 AI slop 反模式寫進 prompt，例如過度置中的 CTA、泛用 icon、glassmorphism、常見漸層套路。

這一層解的是「單頁看起來不套版」。

## Level 2：設計系統

第二層是讓整個 app 的頁面維持一致。很多 agent-generated app 的 landing page 還可以，但 auth、dashboard、內頁一換場景就失去一致性。影片建議把專案脈絡與設計規則拆成兩份文件：

- `CLAUDE.md`：只放專案資訊、架構與工作規則。
- `DESIGN.md` / `design.md`：放視覺系統、layout、色彩、字體、spacing、元件規則與反模式。

理由是 `CLAUDE.md` 會長駐 context；如果把完整設計規格塞進去，agent 在非設計任務時也會被干擾。設計細節應該做成可按需讀取與持續精煉的設計系統文件。

影片也提到可用外部模板或 design skill 驗證 `design.md`，避免 agent 自己產出的設計規格缺少基本設計原則。

這一層解的是「跨頁一致性」。

## Level 3：設計測試與視覺 diff

第三層是把設計驗證變成可迭代的測試流程。設計不像程式碼一樣有清楚輸入輸出，但仍可以用不同形式的 pin 來約束：

- 把 `design.md` 的反模式轉成靜態測試。
- 把色彩、spacing、typography 規則轉成可檢查條件。
- 用 Playwright 做 visual regression。
- 用 Visly Test 這類 CLI 監控畫面 diff，讓人可以 approve / deny 設計差異。

重點是測試要先於實作。若實作完成後才叫 agent 補測試，agent 容易寫出迎合既有實作的測試；先寫測試則會逼實作符合設計規格。

這一層解的是「設計迭代能不能被檢查與收斂」。

## 工作流總結

| 層級 | 解決問題 | 主要產物 |
|---|---|---|
| Level 1 | 單頁不 generic | 詳細 prompt、設計意圖、反模式 |
| Level 2 | 跨頁一致 | `CLAUDE.md` + `design.md` / `DESIGN.md` |
| Level 3 | 可驗證迭代 | 靜態設計測試、Playwright visual regression、Visly diff |

## 可消化方向

- 可併入 [[Claude-Code-前端設計工作流]]：補上 `DESIGN.md` 與視覺 TDD 的分層。
- 可對照 [[DESIGN.md-官方規格]]：確認本 vault 對 `DESIGN.md` 的命名與內容規則。
- 可補強 [[動效與互動]] 或 UI 設計主題入口：Level 3 的 visual diff 適合放在「設計驗證」而非單純動效。
