---
title: Messenger、IG 個人訊息讓 Claude Code 代讀代回？這個 MCP 一次打通
created: 2026-04-27
updated: 2026-04-27
source: https://www.youtube.com/watch?v=-HOakZC7Vps
published: 2026-04-23
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - mcp
  - beeper
  - messenger
  - instagram
---

## 為什麼要用 Beeper

讓 Claude Code 接私人即時通訊有三條路，前兩條都有問題：

| 方法                        | 問題                                                                 |
| --------------------------- | -------------------------------------------------------------------- |
| 官方 API                    | Messenger / Instagram / LINE 只開放商業帳號（粉絲專頁、官方帳號）；私人帳號無法用 |
| 瀏覽器 MCP（登入瀏覽器後操作） | 穩定但模擬人類操作，非常慢、非常耗 token                            |
| 逆向工程的私有 API          | 違反服務條款，輕則失敗，重則帳號直接沒了                            |

第三條路（Beeper）是介於官方 API 與逆向工程之間的合規方法。Beeper 是一家把多個即時通訊整合在一個 inbox 的公司，原理是讓你在 Beeper 裡登入取得憑證，再透過 bridge 連上各通訊服務代為讀寫訊息。它有官方 API 與自己的 MCP，可以讓 Claude Code 直接接上。

## 安裝與設定流程

### 1. 註冊 Beeper

- 搜尋並安裝 Beeper 程式（目前 MCP 只支援 Mac）
- Email 註冊 + 收驗證碼

### 2. 綁定帳號

- 在 Beeper 內按「+」加入帳號，輸入帳號密碼
- 兩步驟驗證會照常要求驗證碼或開啟其他裝置
- **不要用 VPN 登入**，Facebook 會視為可疑流量把帳號鎖住，用平常的網路就好
- 免費版可綁 5 個帳號；一個服務只能同時綁一個帳號
- 支援帳號類型：WhatsApp、Twitter、Telegram、LinkedIn、iMessage、Email、Facebook、Instagram；**LINE 目前未支援**

### 3. 開啟 Desktop API 與 MCP

- 左下角設定 → Developers → 打開 Desktop API（預設關閉）
- 桌面版 Claude：直接點「Install Desktop MCP」按鈕安裝
- 終端機版 Claude Code：複製 Developer 頁面下方的設定文字，貼給 Claude Code 請他幫你設定
- API Token 在 Developer 頁面最下方按「+」建立，設定到期日，需要送訊息就把該選項打開

### 4. 安全設定 Token

- **不要直接把 Token 貼到對話視窗**——對話記錄會留下 Token
- 正確做法：請 Claude Code 教你安全的設定方法（用指令把 Token 寫進設定檔）
- 不慎外洩 → 立刻回 Developer 頁取消舊 Token、重建新的
- 設定完需要重開 Claude Code（MCP 在 session 開始時載入，過程中不會重載）

### 5. 驗證連線

- 重開後在對話打 `/mcp`，看到 `Connected` 即成功
- 測試讀 Messenger 訊息、讀 IG 訊息、傳訊息，都通就完成

## 風險評估

### 公司層面（低風險）

- Beeper 是正規公司，已被上市公司收購
- 程式碼大部分開源，可檢視有無惡意行為
- 官方宣稱訊息只有自己看得到
- 可選擇不走雲端，所有連線都在本機完成（這次 MCP 就是裝在本機）
- Beeper 程式關閉後 MCP 也抓不到，因為不經過網路雲端

### 仍存在的風險

- **未經官方認證**：Meta 改規則時可能暫時壞掉，但 Beeper 維護速度快
- **可能被偵測為自動化**：官方可能要求重新驗證身份；目前回報多是重新驗證即可，不是永久封鎖
- **不是所有對話都加密**
- **Token 外流是自己的問題**，不該貼進 AI 對話

## 適用對象

- Mac 使用者
- 需要 Claude Code 串接 Messenger / Instagram / WhatsApp / Telegram 等私人帳號代讀代回
- LINE 使用者目前需要等支援或找其他方法

評估過上述有限風險後，這是目前合規路徑中最完整的方案。
