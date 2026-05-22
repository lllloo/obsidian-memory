---
title: Python 供應鏈攻擊與 UV 防護
created: 2026-05-22
updated: 2026-05-22
source: https://www.youtube.com/watch?v=bw1ZLzdXJn4
published: 2026-05-21
parent: "[[01.index]]"
tags:
  - youtube
  - python
  - security
---

## 核心觀點

Python 與 JavaScript 生態的 package manager 已經變成供應鏈攻擊入口。每次 `pip install` 或讓 AI agent 自動新增 dependency，本質上都是允許外部程式碼進入本機並執行。AI coding agent 讓這個風險放大，因為 agent 可能在長時間自動迴圈中安裝套件、讀取檔案、接觸環境變數與 credentials。

影片主張 Python 專案應改用 UV，並搭配三個保護措施：精準 pin 版本、排除太新的 package、用 lock mode 同步依賴。

## 供應鏈攻擊如何發生

常見攻擊路徑有三種：

- 維護者被 phishing，導致 package 或 CI token 被盜
- 攻擊者發布名稱相近的惡意 package
- worm 透過受害者檔案系統與 CI/CD token 繼續污染其他 package

受害者或 AI agent 安裝惡意 package 後，惡意程式碼可能讀取 SSH key、環境變數、API key 或其他敏感資料，再送到攻擊者端。

AI agent 讓 typosquatting / slopsquatting 更危險：agent 可能幻覺出不存在或名稱錯誤的套件，剛好裝到攻擊者預先佔好的 package name。

## 不要直接用 pip 作為日常入口

影片建議把 UV 當作 Python 專案預設入口，原因不是單純速度，而是 UV 能用更嚴格的 resolver / lock 行為限制依賴漂移。

`requirements.txt` 太容易變成「看到就裝」的黑盒。`pyproject.toml` 搭配 UV 設定，可以把 dependency policy 放進版本控制，讓團隊與 agent 都遵守相同規則。

## 防護 1：精準 pin 版本

UV 預設新增 dependency 時可能使用 lower bound，例如「大於等於某版本」。這代表未來安裝時可能拿到較新的版本，而新版本若剛被污染，專案會自動吃到風險。

可在 UV 設定中使用 exact bound，讓新增 dependency 時直接 pin 到明確版本。重點不是永遠不升級，而是升級應該是一次明確決策，不是 resolver 自動帶來的變化。

## 防護 2：排除太新的 package

`exclude-newer` 類設定可以拒絕安裝太新的 package，例如 7 天內發布的版本。很多供應鏈攻擊會在前 24 小時內被發現並下架，冷卻期能降低剛發布惡意版本被立即安裝的機率。

這不是絕對安全，但能把「剛被污染就被 agent 裝進來」的風險降很多。實務上可依專案風險調整冷卻天數。

## 防護 3：用 locked sync

`uv.lock` 是依賴快照。CI/CD 與本機同步時應使用 locked mode，讓 `pyproject.toml` 與 lock file 不一致時直接失敗，而不是悄悄解析並安裝新 package。

這對 AI agent 特別重要：如果 agent 修改了 dependency，locked sync 會把未經確認的依賴變更攔下來。

## 給 AI Agent 的額外規則

除了工具設定，也要明確告訴 agent：不要為了小功能隨便新增 dependency。每個 dependency 都要有理由，必要時先詢問；若只需要小段功能，應考慮直接實作或引用特定原始碼片段，而不是引入整個 package。

這條規則應放在 `AGENTS.md`、`CLAUDE.md` 或專案等價規則裡，尤其是允許 agent 長時間自主執行的專案。

## 我的理解

供應鏈安全不是只靠掃描工具，而是要讓 dependency 變更變成可審核事件。UV 的 exact version、exclude-newer、locked sync 分別處理版本漂移、剛發布惡意版本、以及未授權 dependency 變更。對 AI coding workflow 來說，最重要的是把「agent 可以自己裝東西」改成「agent 必須先證明 dependency 值得加入」。
