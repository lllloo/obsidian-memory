---
title: 用 Herdr 在雲端執行你的 Coding Agent
description: 在 Hostinger VPS 預裝 Herdr，配 SSH key、developer 使用者與 IP 白名單防火牆，登入 Claude Code 與 Codex，讓 agent 關機也不中斷
created: 2026-10-08
updated: 2026-10-08
source: https://www.youtube.com/watch?v=s4stoQM_LT8
published: 2026-09-28
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - workflow
  - claude-code
  - codex
  - security
---

## 整體架構與動機

- 租一台 VPS（虛擬私人伺服器）當雲端工作區，在上面裝 Herdr，再接上 Claude Code、Codex（Grok 等其他 harness 亦可）。
- Herdr 是專為 agent 設計的 terminal multiplexer，本身以獨立 server 形式運行：在本機上已能做到「關掉 terminal，session 仍在跑」。
- 本機版的剩餘問題：闔上筆電、關機或出門時，agent 就停了。搬到 VPS 後，agent 與實體裝置脫鉤，筆電、桌機、手機都只是接進同一個持久雲端工作區的入口。
- 講者認為隨著越來越多工作外包給 agent，這種「集中式雲端工作區」會越來越普遍。

## 選擇 VPS（Hostinger）

- 過去一年許多 VPS 業者因 RAM 短缺漲價 2～3 倍，講者認為 Hostinger 目前價格仍具競爭力，dashboard 功能也完整。
- 建議至少 **8 GB RAM**，預算允許可再往上加。
- 結帳時可選鎖定期間（12 個月、24 個月折扣更多）；機房地點選離自己最近的。
- 建立時可直接選 **Herdr 預裝範本**，開好的 VPS 已裝好 Herdr，省去部分設定。VPS 也能另作學習、專案或部署用途。

## Root 密碼與 SSH key

- Root 密碼：保護伺服器上 root 帳號的權限，可用產生器或自己的密碼管理器產生，務必保存。
- SSH key：用來從自己的裝置連進伺服器的驗證方式。
  - 在本機依作業系統執行 `ssh-keygen`（passphrase 可選），產生金鑰後妥善保管私鑰。
  - 把**公鑰**複製到剪貼簿，在 Hostinger 面板新增 SSH key 貼上，並命名（例如用裝置名稱）。
- 惡意軟體掃描可先跳過，等待 VPS 建立完成（數分鐘）。

## 首次登入：Web console 與 SSH

- 先從 Hostinger 面板開 **web console**，在瀏覽器內的 terminal 確認 Herdr 已安裝，直接執行 `herdr` 即可進入。
- 再從本機 terminal 以 `ssh root@<VPS IP>` 連線，第一次連線會要求確認，回答 yes；連上後同樣可啟動 Herdr。

## 設定 SSH 捷徑

- 編輯本機的 SSH config（第一次使用可先用 `touch` 建檔，各作業系統路徑不同），加入一段 Host 設定並填入伺服器 IP。
- 之後只要 `ssh agent-cloud`（或你自訂的名稱）就能直接進伺服器，不必記完整指令。

## 建立 developer 使用者

- root 能改動伺服器所有設定，日常讓 coding agent 跑在 root 下風險較高，因此另建一個 **developer** 使用者。
- 步驟：
  1. 在伺服器上建立使用者。
  2. 從**本機**執行指令，把 SSH key 授權給 developer 使用者。
  3. 執行一次性指令讓 developer 也能使用 Herdr（預設只裝給 root）。
  4. 把 SSH 捷徑的登入使用者從 `root` 改成 `developer`。
- 需要做系統層級變更時再改用 root 登入；用 `whoami` 隨時確認目前身分。
- 第一次做這類設定時，建議先請 coding agent 解釋每一步在做什麼，再把敏感資訊交給伺服器。

## 用防火牆限制 SSH 來源

- 目前伺服器只靠 SSH key 保護；可再加一層防火牆，只允許**白名單 IP** 連線。
- 前提是有固定 IP：家用網路通常是浮動 IP，講者團隊用 NordLayer 這類 VPN 取得專屬固定 IP。
- 在 Hostinger 面板的 Security → Firewall 新增規則：開放 port 22（SSH）只給白名單 IP，其餘入站流量一律 drop。
- 防火牆設定可在多台 VPS 間共用，設一次後直接套到新開的伺服器。

## 安裝 GitHub CLI、Claude Code 與 Codex

- 到目前為止加上後續幾步都是**一次性設定**。
- 用 root 登入安裝並設定 GitHub CLI（clone、PR、commit 都需要）。
- 改以 developer 登入，安裝 Claude Code 與 Codex（兩者可同時跑安裝指令；Codex 安裝會要求按 `y` 確認）。

## 登入 GitHub、Claude Code 與 Codex

- 伺服器沒有瀏覽器，因此一律走 **device 驗證流程**：terminal 印出 URL 與代碼，在本機瀏覽器開啟並貼上代碼。
- GitHub：用 GitHub CLI 登入，到 `github.com/login/device` 輸入代碼並授權；之後可設定全域的 git name 與 email。
- Claude Code：執行 `claude auth login`，在本機瀏覽器授權後取得代碼貼回 terminal。貼上時畫面不會顯示任何字元，直接按 Enter 即可，看到 login successful 即完成。
- Codex：執行 Codex 的 device auth 登入指令。第一次可能需要先到 OpenAI／ChatGPT 帳號的安全性設定中允許 device 驗證，畫面會提示是否需要。

## 在 Herdr 中測試兩個 agent

- 開 Herdr session，在一個 tab 啟動 Codex、信任資料夾、送出測試訊息。
- 另開 tab 啟動 Claude：選 dark mode、使用訂閱；Claude Code 內還有一次驗證步驟，可按 `C` 複製整行 URL，完成後貼回代碼。
- 兩個模型都能回應即代表設定完成。

## 專案目錄、integrations 與 Herdr skill

- 新伺服器上什麼都沒有，建議建一個 `repositories` 資料夾當工作起點，用 `git clone` 把專案拉進來。
- 執行 `herdr integrations install claude`、`herdr integrations install codex` 把 Herdr 接上各 harness，再檢查 status；所有 Herdr 支援的 harness 都能這樣做，詳見官方文件。
- 想做多 agent 系統（Codex 可以叫起 Claude sub-agent、反之亦然）時，加裝 **Herdr skill**。
- 在 Herdr 中新增 space、指向 `repositories` 下的專案資料夾，即可在新專案開 Codex session（會要求信任已設定的 hooks）。
- Herdr 的所有設定都在設定檔裡，本機已調好的設定可直接複製到雲端環境沿用。

## 用 Cursor 或 VS Code 透過 SSH 連線

- Cursor／VS Code 內建「Connect via SSH」，可直接選先前設定的 SSH 捷徑進入伺服器。
- 在編輯器的 terminal panel 啟動 Herdr，會接到伺服器上**同一個** Herdr session。
- 好處是能用圖形介面瀏覽伺服器檔案、開啟 repo 編輯、看 version control；可以一邊 terminal 跑 agent，一邊用編輯器看檔案、處理 commit 與 PR。

## 日常工作流

- 講者另附一份日常工作流文件，整理如何連線、加入新專案、預覽 web app。
- 例如在伺服器上跑 localhost 服務時，可把 port 轉發到自己的裝置上檢視。
