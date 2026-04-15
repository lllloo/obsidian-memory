---
title: Claude Cowork 完整教學：自動化任何工作流程
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-27
source: https://www.youtube.com/watch?v=3FCYpGz7ptM
---

## Claude Chat vs Claude Code vs Claude Cowork 差異

| 工具 | 定位 | 主要能力 |
|------|------|---------|
| Claude Chat | 研究員 | 深度網路研究、瀏覽器控制（需安裝 extension） |
| Claude Code | 開發工具 | 建立應用程式、終端機執行 script |
| Claude Cowork | 全能自動化 | 修改本機檔案、深度研究、瀏覽器操控、連接 SMTP/Skills，全在桌面 UI 操作 |

## 設定專案

1. 開啟 Claude 桌面應用 → 點選 Cowork
2. 建立新專案（三種選項）：
   - 從零開始
   - 從 Claude Chat 匯入現有專案
   - **選擇現有資料夾**（最常用）
3. 設定專案名稱和 System Prompt（等同於 AI 的作業指示）

## Connectors（連接器）

在 prompt 視窗按「+」管理：
- PDF Viewer（處理大量 PDF 推薦安裝）
- Gmail（讀取/草擬回覆、提取收據）
- Google Calendar（預約行程）
- Chrome 控制
- 可依使用情境安裝，按 popularity 排序瀏覽

## 實際示範：600 張收據轉 CSV

**任務**：從 receipts 資料夾（642 個 PDF/PNG/JPEG）提取以下欄位，輸出 CSV：
- 供應商（Vendor）
- 幣別（預設 CAD）
- 小計、稅額
- 類別（CRA 商業類別）
- 日期
- 付款方式
- 需人工審核旗標

**重點做法**：提示中明確要求「先規劃再執行」，Claude 會在開始前詢問確認：
- 要處理全部還是先測試小批次
- 輸出格式（選 CSV）
- 類別系統（選 CRA）
- OCR 讀不到時是否 flag 待審

**執行過程**：右側進度清單追蹤：設定 OCR 工具 → 建立 Python 提取腳本 → 批次處理 → 輸出 CSV → 驗證樣本。

**結果限制**：OCR 對部分日期和供應商名稱不準確，需透過對話迭代修正。

## 建立可重複使用的 Skill

將本次對話的整個工作流打包為 skill：

1. 點選 Skills → Skill Creator
2. 描述要封裝的工作流（收據 OCR 提取 → CSV）
3. Claude 建立：
   - `skill.md`（執行指示）
   - Python 提取腳本
   - Eval（測試案例）
4. 點選「Copy to your skills」加入技能庫
5. 之後輸入 `/` 即可呼叫 `receipt-ocr-extractor` skill

## Plugins（預定義技能包）

將 skills + connectors 組合成主題插件，Anthropic 官方提供：
- **Productivity**：整合 Slack、Notion、ClickUp，管理任務和每日重點
- **Marketing/Content**：SEO 文章草稿、內容創作流程

## 排程任務

在專案中設定自動執行的定期任務，例如：每週一早上 9:00 自動執行收據 OCR 提取 skill（需保持電腦開機）。

## 記憶功能（Memory）

- **用途**：跨 session 保留用戶偏好，不需每次重新解釋
- **例**：「我住在加拿大，預設幣別是 CAD」——記住後新對話自動套用
- **儲存位置**：本機（不上傳雲端）
- **機制**：每 24 小時自動摘要對話重點
- **敏感資料**：密碼、健康資料等預設排除
- **設定位置**：Settings → Capabilities → Generate memories from chat histories

也可從其他 AI 提供商匯入過去的記憶。
