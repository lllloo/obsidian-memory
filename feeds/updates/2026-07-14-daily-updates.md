---
title: "2026-07-14 Daily Updates"
created: 2026-07-14
updated: 2026-07-14
tags:
  - updates
  - opencode
---

## OpenCode

### v1.17.20 · 2026-07-13（[Changelog](https://opencode.ai/changelog)）

**繁中摘要**：小幅維護版，重點是補齊新模型的 provider 相容性——Azure AI 加上 GPT-5.6 支援，並移除影響 OpenAI Luna Responses Lite 的過時 Codex workaround。

- **Azure AI × GPT-5.6**：更新 Azure AI 整合以支援 GPT-5.6，走 Azure 的使用者可直接選用。
- **移除 Luna 過時 workaround**：清掉先前為 Codex 設的相容性補丁，修正其對 OpenAI Luna Responses Lite 的干擾。

---

### v1.17.19 · 2026-07-13（[Changelog](https://opencode.ai/changelog)）

**繁中摘要**：一批 provider／auth 層變更值得注意——新增 OpenAI pro reasoning mode、為 Luna Responses Lite 導入 OAuth，並預設關閉 xAI Responses 的 response storage（隱私預設收緊）。

- **OpenAI pro reasoning mode**：Core 新增對 pro reasoning mode 的支援，並對走 OAuth 的 GPT-5.6 套用 Codex context limits。
- **xAI Responses 預設不留存**：預設停用 xAI Responses 的 response storage，改為 opt-in，降低對話內容外流風險。
- **Luna Responses Lite OAuth**：改用 OAuth 驗證，並修正 console 登出後的 org 切換。
- Desktop 另有多項 UI 修正（review panel 持久瀏覽與 file tab、per-prompt model 選擇、middle-click 開分頁等），屬體驗改善非行為破壞。

---

### v1.17.17 · 2026-07-09（[Changelog](https://opencode.ai/changelog)）

**繁中摘要**：Desktop 推出 v2 free-model selector，可跨多 provider 存取免費模型；Core 強化 Meta 模型的 reasoning variant 處理。

- **v2 free-model selector**：Desktop 新增可多 provider 存取的免費模型選擇器，方便零成本試不同模型。
- **Meta reasoning variants**：Core 改善 Meta 模型 reasoning 變體的處理邏輯；另附 model selector label、sub-agent task rows 等 UI 修正。
