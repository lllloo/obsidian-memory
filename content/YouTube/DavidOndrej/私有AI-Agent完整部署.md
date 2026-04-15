---
title: 100% 私有 AI Agent 完整部署教學
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-02-07
source: https://www.youtube.com/watch?v=45-Y8I_Nn4I
---

## 概覽

- Agent Zero 是目前市場上最強大且完全私有、開源、免費的 AI Agent。
- 部署在 VPS 上可 24/7 運作，且不將你的資料送給 Anthropic、OpenAI 等公司。
- 本教學包含：VPS 部署、Docker 安裝、Agent Zero 設定、Nabana Pro（圖片生成）整合、Perplexity Deep Research 整合。

## 部署步驟（VPS + Docker）

1. 在 Hostinger 購買 KVM2 VPS（2 vCPU、8 GB RAM、100 GB 磁碟）。
2. 選擇 Ubuntu 作業系統，進入 Hostinger 內建 Terminal。
3. 安裝 Docker：
   ```bash
   curl -fsSL https://get.docker.com | sudo sh
   sudo usermod -aG docker $USER
   ```
4. 建立 `docker-compose.yaml`（使用 GitHub Gist 範本）：
   - 修改管理員帳號與密碼（不要用預設 admin/admin）
   - 填入 OpenRouter API key（取得 Opus 4.6 存取）
5. 儲存並執行：`docker compose up -d`
6. 從 Hostinger 面板取得 VPS IP，在瀏覽器開啟 `http://<IP>:5080` 進入 Agent Zero 登入頁。

## 模型設定

- 前往 Agent Zero 設定頁：
  - **Chat Model**：Opus 4.6（主要交談與思考）
  - **Web Browser Model**：Opus 4.6（操控瀏覽器）
  - **Utility Model**：Kimi K2.5（便宜且夠用，處理一次性任務）
- Agent Zero 的多模型委派是對比 OpenClaw 的重大優勢——Opus 只用在真正需要的地方，大幅降低成本。

## 安全功能：Secret Store

- 其他 Agent 通常讓你把 API key 直接發在對話中（非常不安全）。
- Agent Zero 內建 **Secret Store**：
  - Agent 看得到變數名稱（如 `OPENROUTER_API_KEY`），但永遠看不到實際數值。
  - 數值不加入 context window，不傳送給外部提供商。
  - 從 Settings → External Services → Secrets Management 設定。

## 整合 Nabana Pro（圖片生成）

1. 取得 OpenRouter API key（已含 Nabana Pro 存取）。
2. 在 Secret Store 加入 `OPENROUTER_API_KEY=<你的key>`。
3. 複製 OpenRouter 官方 Python 範例文件，告知 Agent Zero：「Turn this into reusable knowledge. Save as a markdown file for future reference.」
4. Agent 建立知識檔案，之後可直接說「Generate image of flying cat over Dubai」——Agent 自動使用正確 API key 生成圖片。

## 整合 Perplexity Deep Research

1. 前往 OpenRouter，找到 Perplexity Deep Research 模型的 Python 文件。
2. 複製文件，告知 Agent Zero 建立知識記憶並指定使用 Perplexity 做深度研究。
3. 後續只需說「Do a deep research on [topic]」，Agent Zero 自動觸發 Perplexity Deep Research 並用 API key 執行。

## 知識與記憶系統

- **知識目錄**：`/ao/user/knowledge/`（使用者擁有的知識檔案）。
- **向量搜尋**：Agent Zero 自動索引知識資料夾，用 Utility Model 進行語義搜尋。
- **memory_save 工具**：Agent 自動用此工具儲存重要記憶，確保放在正確目錄。

## Projects 功能

- Agent Zero 有獨特的 Projects 系統，比 ChatGPT 的 Projects 更強大：
  - 每個 Project 有獨立的 system prompt 補充說明
  - 獨立的記憶空間（不與其他 Project 混雜）
  - 獨立的 Secret Store（不同 Project 可用不同 API key）
  - 獨立的檔案目錄結構
- 適合用途：為公司不同部門或不同員工建立不同 Project，各有不同角色與權限。

## Agent Zero vs OpenClaw 比較

| 面向 | Agent Zero | OpenClaw |
|-----|-----------|---------|
| 開源 | 完全開源 | 是 |
| 隱私 | 最高（Secret Store，本機執行） | 中等 |
| 成本 | 低（多模型委派） | 較高（Opus 用於所有呼叫） |
| 成熟度 | 近 2 年，最成熟 | 相對較新 |
| 目標族群 | 注重隱私與安全的進階使用者 | 一般大眾 |
| 記憶系統 | 知識目錄 + 向量搜尋 | Markdown 檔案 |
| Projects | 完整獨立的 Project 系統 | 無 |

## 安全原則

- 不要將 Agent Zero 的 Docker Container 暴露在公共網路，只限 VPS 內部存取。
- API key 在 Secret Store 中儲存，永遠不出現在對話記錄或送給外部 AI 提供商。
- 整個 VPS 環境專屬給 Agent Zero，不混用其他個人資料。
- 定期從 OpenRouter 輪替 API key，設定消費上限（防止洩漏後被濫用）。
