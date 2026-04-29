---
title: DESIGN.md 使用指南
created: 2026-04-29
updated: 2026-04-29
tags:
  - design
  - design-system
  - ai-coding
  - frontend
---

如何把 DESIGN.md 用起來。官方 8 大 canonical 區段定義見 [[DESIGN.md-官方規格]]，本篇只講實務工作流。

## 何時需要 DESIGN.md

- 開始新專案，要讓 AI coding agent 從一開始就有設計規範可讀
- 想把設計系統納入 Git 版控，取代 Figma handoff 流程
- 多人或多個 agent 同時協作，需確保 UI 視覺一致

不需要的情境：純後端專案、快速 prototype（設計方向未定）、Stitch 設計還在迭代中（先定稿再匯出）。

## 撰寫原則

四條準則，缺一不可：

- **具體數值**：寫「8px」不寫「圓角」；寫「32px / 700 weight」不寫「大標題」
- **語義命名**：用 primary、surface、accent，不用 blue-500；命名代表用途而非顏色值
- **token 層級**：只寫 token 定義，不塞完整 CSS block；讓 agent 決定如何實作
- **納入版控**：與程式碼同步 commit，合併前 review 變更，確保 agent 讀到的版本一致

違反這四條的常見症狀見文末「常見陷阱」表。

## 與 Claude Code 整合（四步驟工作流）

1. 在 Stitch 完成設計，匯出 `DESIGN.md` 放專案**根目錄**（與 `CLAUDE.md` 同層）
2. 在 `CLAUDE.md` 加明確指示：「生成或修改任何 UI 元件時，請參照 DESIGN.md」
3. 每次 prompt **明確引用**：「依照 DESIGN.md 建立 primary button」（不要只說「照設計做」）
4. 可把 token 轉為 Tailwind config（`tailwind.config.js`），詳見常見陷阱第三條

官方 CLI（`npx @google/design.md`）有 lint、diff、export、spec 等子命令可輔助驗證，詳見 [[DESIGN.md-官方規格]]。

## Extended Sections（社群擴展，非官方必填）

`awesome-design-md` 等社群整理的品牌範例常在官方 8 段之外加入兩個延伸段落：

**Responsive Behavior**：斷點定義、觸控目標最小尺寸（通常 44px）、元件在小螢幕的收合策略。

**Agent Prompt Guide**：快速色彩對照表（讓 agent 不用每次查完整色盤）、預設 prompt 範例（「建立一個使用 primary 色調的 CTA 按鈕」）。

> 使用這些延伸段落時，應在文件中標明為 **extended format**，避免誤認為官方必填結構。

## 品牌範例庫：awesome-design-md

需要 DESIGN.md 起手式範例時，[getdesign.md](https://getdesign.md/)（GitHub: [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)）收錄約 70 份知名品牌（Claude、Linear、Stripe、Figma、Apple…）按產業分類整理的 DESIGN.md，採 Stitch format + extended sections，**不是** Google 官方 spec 本身。

**使用方式**：造訪 `https://getdesign.md/<brand>/design-md` 下載，貼入專案根目錄作為起點。完整品牌清單與風格描述見 [[Awesome-Design-MD]]。

> 注意：非官方授權的設計系統，僅供學習與風格參考，**不可直接商用**。

## design-md Skill 五階段分析流程

社群 `design-md` skill（來自 `google-labs-code/stitch-skills`）可自動分析 Stitch 專案並產生 DESIGN.md，五個階段依序執行：

1. **Retrieval** — 抓取專案畫面、HTML、設計 metadata
2. **Extraction** — 識別 design token（色彩、字體、間距、元件）
3. **Translation** — 將 CSS / Tailwind 值轉為語義化設計語言
4. **Synthesis** — 產生完整 DESIGN.md 文件
5. **Alignment** — 確保輸出符合 Stitch Effective Prompting Guide

安裝方式依實際 repo 說明為準，使用前確認 repo 是否仍存在（`google-labs-code/stitch-skills`）。

## 常見陷阱

| 徵兆 | 原因 | 解法 |
|------|------|------|
| Agent 產出 UI 與設計稿不一致 | DESIGN.md 只放本機，agent 讀不到；或未納入版控 | commit 進 git，`CLAUDE.md` 明確指示 agent 讀取 |
| DESIGN.md 內容變來變去 | Stitch 設計未完成就匯出，邊做邊改 | 在 Stitch 先定稿視覺方向再產出 DESIGN.md |
| token 轉 Tailwind 時命名衝突 | 語義命名（primary）與 Tailwind 預設（blue-500）未對齊 | 在 `tailwind.config.js` 覆寫 theme，保持單一命名來源 |

## 相關主題

- [[DESIGN.md-官方規格]] — 8 大 canonical 區段定義、alpha spec 狀態、官方 CLI 命令
- [[Claude-Code-前端設計工作流]] — Layer 1 Prompt 注入層引用此主題
- [[Stitch]] — Google Stitch MOC（生成 DESIGN.md 的主要工具）
- [[動效與互動]] — 動效類別的設計規格

## 來源卡片

- [[Awesome-Design-MD]] — 品牌範例庫總覽

## 外部資源

- [getdesign.md](https://getdesign.md/) — 品牌範例瀏覽入口
- [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — GitHub 源
- [Google Stitch](https://stitch.withgoogle.com/) — 官方入口
