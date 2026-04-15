---
title: 100% 私有 AI Agent：本地部署完全指南
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-23
source: https://www.youtube.com/watch?v=JLIFx9r5EDg
---

## 概覽

- 想像一個完全在你電腦上運行的超強 AI Agent——沒有任何資料離開你的機器，完全私密，幾乎無所不能，這就是 Agent Zero。
- 本影片展示 Agent Zero 的全新簡易安裝方式、如何搭配本地模型運行，以及實際使用場景。

## 安裝 Agent Zero

- 前往 agent-zero.ai（注意勿進入仿冒網站），使用官方一鍵安裝腳本。
- 在終端機貼上腳本並執行，選擇「新實例」從零開始安裝。
- 選擇版本：想搶鮮體驗功能選測試版，穩定功能選最新正式版。
- 預設連接埠為 5080，可自訂實例名稱。
- 安裝過程會拉取 Docker 映像（包含完整 Linux 環境，數 GB 大小）。
- **Docker 容器的好處**：Agent Zero 在隔離容器中運行，避免其他代理（如 Claude Code、OpenClaw、Codex）以完全授權模式直接操作主機時可能帶來的資料外洩或檔案刪除風險。

## 連接本地模型（Ollama）

- 本地運行模型的主要平台有兩個：Ollama 與 LM Studio，Agent Zero 對 Ollama 支援更好。
- 前往 ollama.com，使用一鍵安裝腳本安裝 Ollama。
- 安裝後可用 `ollama list` 查看已下載的模型清單。

## 選擇模型

- 選擇模型的關鍵因素是硬體規格：
  - Nvidia GPU：看 VRAM 大小決定可跑的模型
  - Apple Silicon：CPU 與 GPU 共享記憶體，比同價位 Nvidia 更有優勢
  - 一般建議範圍：20–35B（較舊電腦建議 9–13B）
- Qwen 系列提供多種參數大小可選擇。
- 使用 `ollama run <模型名稱>` 下載並啟動模型。

## 在 Agent Zero 設定 LLM

- 進入設定，選擇 LLM 提供商為「Ollama」。
- 填入模型名稱（可用 `ollama list` 確認）與 context length（建議最低 16K，理想 32K 以上）。
- 設定 API base URL：`http://host.docker.internal:11434`（讓 Agent Zero 從容器內連到 Ollama）。
- 「聊天模型」負責主要推理；「工具模型」負責背景任務（建議用速度快、成本低的小模型，如 GLM 4.7 Flash）。
- 「嵌入模型」可同樣透過 Ollama 設定（如 `nomic-embed-text`），避免嵌入資料外傳。

## 實際應用案例

### 私人照片分析

- 將照片拖入 Agent Zero，要求讀取 metadata（GPS、拍攝日期、相機型號）並依類別（食物、人物、風景、文件等）整理到子資料夾，最後生成旅行報告。
- Agent Zero 擅長多步驟任務，比其他代理更持久，不會輕易停下來詢問確認。
- 所有資料完全不離開本機，可離線使用。

### 適合用本地 Agent 處理的敏感資料

- 醫療健康資料（病歷、基因檢測結果等）
- 財務紀錄、加密貨幣相關資料
- 個人影片
- 密碼與帳號憑證
- 法律文件、NDA
- 日記與心理諮商筆記
- 商業機密與創意構想

## 結語

- 本地 AI 模型雖然速度較慢，但換來的是完整的隱私保護，對敏感工作場景而言非常值得。
- 如果想用技術能力打造真正的 AI 事業，可進一步參考作者的相關課程或加速器計畫。
