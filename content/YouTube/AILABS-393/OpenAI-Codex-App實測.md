---
title: OpenAI Codex App 實測：打造 3D 動畫 Landing Page
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-06
source: https://www.youtube.com/watch?v=sC4JpJlD3aQ
---

## 步驟一：用 Tripo 3D 生成 3D 資產

建構這類網站的第一步是準備好的 3D 資產。使用 Tripo 3D（AI 驅動的 3D 物件生成器）：

1. 準備車輛圖片（移除背景，避免干擾 3D 生成——可用 Canva 或 remove.bg）
2. 上傳到 Tripo 3D，約 1 分鐘生成模型
3. 確認各角度都符合期望後匯出為 `.glb` 格式
   - `.glb` 優於其他格式：紋理和材質整合在單一檔案中，且是原生 web 格式
   - 免費方案只有 15 次匯出配額，設定 4K 解析度後再匯出
4. 將 `.glb` 檔案放到 Next.js 專案的 `public/` 目錄

## Codex App 介紹

Codex（目前僅支援 macOS）的介面類似 Antigravity 的 agent manager，但更專注於 agents 而非程式碼。

最受歡迎的功能：**內建 skill creator**，以及許多安裝時就附帶的即用 skills——其他 agent 通常需要額外安裝開源 skill creator 才能建立自訂 skill。

## 建立 3D 動畫 Skill

1. 使用 skill creator 並提供詳細描述：如何建構動畫、要使用哪些 library
2. 回答幾個問題後，它執行 skill creator 的腳本並建立 skill
3. Codex 將 skill 安裝在根目錄（與慣例不同），需手動移到 `.agent` 資料夾
4. Skill 遵循 Claude 開源 agent 框架的相同模式：包含 scripts、references 和資產

Skill 也包含一個 YAML 檔，定義觸發 skill 的通用 prompt。

## 實作過程與問題排查

**依賴衝突問題：**
- 請 Codex 設置動畫後，它完成了任務但因環境 timeout 無法安裝依賴
- 解法：請它將依賴寫入 `package.json`，再手動執行 `npm install`
- 出現版本衝突錯誤，需多次 debug 才讓 hero section 動畫正常運作

**平行 Agent 加速：**
- Codex 每個功能都花費大量時間，改用拆分任務的方式
- 將 landing page 拆成四個獨立子任務，各含目標、需求和限制
- 使用 Codex 的 multi-agent 功能，每個 agent 負責一個任務
- 讓各 agent 在獨立的 work tree 工作，避免同時修改同一分支造成衝突
- 所有 agent 幾乎同時完成，合併輸出後沒有衝突，整體速度大幅提升

## 加入捲動動畫（GSAP）

除了 hero section，其他區塊沒有動畫、看起來過於平板。使用 GSAP（業界常用的 JavaScript 動畫 library）：

- 因先前依賴衝突問題，提前在終端機手動執行 `npm install gsap`
- 提供高度詳細的 prompt，明確指示不要碰 hero section
- 各 section 加入捲動觸發動畫後，整體視覺感受明顯提升

## 使用 Aceternity UI 元件

動畫加入後，普通元件相較於 hero section 仍顯平板。改用 Aceternity UI：

- Aceternity 元件內建大量互動效果和動畫，可直接整合進專案
- 請 Codex 將現有元件替換成 Aceternity，保留現有動畫
- 問題：實作後元件是靜態的，沒有 Aceternity 的微互動效果
- 明確指示使用包含懸停傾斜（hover tilt）等微互動效果的版本後，元件才具備互動感

另注意：實作後有漸層不符合主題，提供截圖指出問題，修正為符合主題的配色。

## 後期處理效果（Post-processing）

使用 `postprocessing` npm 套件（React Three Fiber 的後期處理 layer）：

- 可使用伽瑪校正等圖像處理功能
- 目標：在 3D 模型上加入微妙的光暈效果
- 需多次 debug 才讓效果正確顯現，最終為 hero section 增添溫暖光線，使整體更有完成感
