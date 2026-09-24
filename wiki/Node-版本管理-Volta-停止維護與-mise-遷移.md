---
title: Node 版本管理：Volta 停止維護與 mise 遷移
description: Volta 停止維護後的替代方案盤點（mise、proto、fnm、nvm 等），以及從 Volta 遷到 mise 的機制差異、限制與隱藏依賴
created: 2026-09-24
updated: 2026-09-24
parent: "[[wiki/01.index]]"
tags:
  - nodejs
  - dev-environment
  - wsl
---

# Node 版本管理：Volta 停止維護與 mise 遷移

Volta 曾是 Node 工具鏈管理的代表作，但**已停止維護**。本頁整理三件事：Volta 現況與它的設計代價、替代方案怎麼選、實際從 Volta 遷到 mise 會碰到什麼。

證據強度逐條就地標：**一手**（官方文件、原始碼、維護者本人發言）、**本機實測**（2026-09-24 在 Ubuntu 24.04／WSL2 上完整遷移一次）、**單一作者意見**（部落格或留言，未經獨立確認）。

## 一、Volta 現況：停止維護（一手）

- 2025-11 維護者在 README 頂端加上 **"Volta is unmaintained"**，並置頂 [issue #2080](https://github.com/volta-cli/volta/issues/2080)，**建議改用 mise**——理由是多數維護者自己已改用它（見 [[Volta-Unmaintained-Issue-2080]]）。最後一個 release 停在 2024-12。
- 官方措辭是「現在能用的應會繼續能用，不必急著遷」，但新 OS 版本或生態變動造成的壞掉**不會再修**，建議排進維護計畫。
- 維護者 chriskrycho 在 issue 中說明為何不交棒：要讓專案恢復健康約需 2–3 個月工程投入、之後每年至少一個月，小額贊助撐不起；**歡迎 fork，但 fork 要自己建立信任**，不承接 Volta 的名聲。

## 二、Volta 的設計代價：看不見的轉接層

Volta 好用的地方與它難除錯的地方是同一件事（一手＋本機實測）：

- **全部走 shim**：`~/.volta/bin` 下的 `node`、`npm` 乃至每個全域 CLI 都是指向 `volta-shim` 的 symlink，執行時才由 Volta 決定用哪個版本、哪份檔案。`which` 只會查到 shim，要用 `volta which <指令>` 才看得到真實路徑。
- **攔截 `npm i -g`**：全域安裝被導進 `~/.volta/tools/image/packages/`，不在 npm 平常的 global prefix。
- **好處是全域工具被釘在安裝時的 Node 版本**：換專案、升級預設 Node，全域 CLI 都不受影響——這正是遷走後最常被懷念的功能（見第四節 miseo）。
- 代價是「查問題查到最後才發現是 Volta」。本機實測一例：Volta 沒裝 pnpm 時，shim 沿 PATH 往後找，在 WSL 裡落到 **Windows 端 Volta 的 pnpm 腳本**而報錯——兩層看不見的轉接疊在一起。

## 三、替代方案怎麼選

| 工具 | 管理範圍 | `which` 是否直接 | 讀 `package.json` 的 `volta` 欄位 | 備註 |
|---|---|---|---|---|
| **mise** | 多語言（Node、Python、Go…）＋環境變數＋task | ✅ activate 模式指真實路徑；shims 模式否 | ❌（一手：官方文件未支援；`devEngines` 需開 idiomatic 設定） | Volta 維護者推薦；功能多、設定概念多 |
| **proto**（moonrepo） | 多語言 | ❌ 以 `~/.proto/shims` 進 PATH（一手：官方文件） | ✅（一手：node plugin 原始碼 `extract_volta_version`，另讀 `devEngines`、`engines`、`.nvmrc`、`.node-version`） | telemetry **預設開啟**，改 opt-in 的 issue 仍開著（一手） |
| **fnm** | 只管 Node | ⚠️ 據記憶是每個 shell 的 symlink 目錄（**未查證**） | ❌ | 讀 `.nvmrc`／`.node-version`，`--use-on-cd` 自動切換，支援 Windows（一手：README） |
| **nvm** | 只管 Node | ✅ 直接改 PATH | ❌ | 自動切換要自貼 shell hook；fish 官方不支援；Windows 只能靠 WSL／Git Bash（一手：README）；每個 Node 版本各一份全域套件 |
| **Corepack** | 只管 package manager | — | — | 不能釘 Node 版本，只能搭配其他工具 |

選型判準：

- **要「無痛延續 Volta」、不改各 repo**：proto 最接近——它讀既有 `volta` 欄位，也用 shim 模型、全域工具行為相近。單一作者 TheJaredWilcurt 的長篇評比（[[Comparing-Node-Version-Management-Tools]]）結論即「選 proto、但先關 telemetry」，並給了設定步驟（[[Proto-as-Volta-Replacement]]）。**此評比為單一作者主觀意見**，評分重心放在 npm 版本釘選與 `package.json` 標準，且對 mise 措辭強烈。
- **要「路徑看得見、裝了什麼一目了然」**：mise 的 activate 模式。這是本頁實際採用的路線，理由是 Volta 的痛點正是轉接層不透明。
- **只碰 Node、想最少概念**：fnm 或 nvm。代價是全域 CLI 綁在各 Node 版本上、切版本就「消失」。

關於 mise 的社群爭議（**單一留言者意見，勿當事實引用**）：issue #2080 有留言批評 mise 開發大量依賴 LLM、PR 缺乏 review、採 CalVer 導致回歸多、GitHub Issues 被關閉。其中「Issues 被關閉」一點，2026-09-24 查 GitHub API 為 `has_issues: true`，**至少現況不成立**；其餘屬觀感，無從核實。Rico Sta. Cruz 2024 年的 [mise vs Volta 比較](https://ricostacruz.com/posts/mise-vs-volta)（[[Can-Mise-Replace-Volta]]）結論是「大致可以取代」，但文中「mise 不支援 Windows」**已過時**——#2080 有使用者回報現已在 Windows 上使用 mise。

## 四、遷到 mise：機制差異與限制

**1. activate 與 shims 要搭配用（一手：官方 shims 文件）**

- activate 模式把各工具的真實 `bin` 目錄直接放進 PATH，`which node` 會是 `~/.local/share/mise/installs/node/<版本>/bin/node`；官方原話是 shims 會 "break" `which`。
- activate 靠互動 shell 的 prompt hook 運作，**非互動 shell（腳本、SSH exec、IDE 背景程序）拿不到**。官方建議 profile 放 shims、互動 shell 再 activate，後者會把真實路徑排到 shims 前面。
- 官方建議把 shims 放 `.zprofile`，但那只有 login shell 讀。**若有工具走 non-login 的 SSH exec shell**（如某些 IDE 的遠端 relay），shims 要放 `~/.zshenv` 才涵蓋得到（本機實測）。zsh 讀檔範圍與 [[Yazi-設定與踩雷]] 第二節的 snap PATH 陷阱是同一套規則。

**2. 全域 CLI 不再釘版本（一手：官方 npm backend 文件）**

- 用 `"npm:<套件>"` 寫進 `~/.config/mise/config.toml` 可以把全域 CLI 集中宣告，一個檔案看得完。
- 但**執行時用的是當下目錄生效的 Node**，不是安裝時的版本。在釘了舊 Node 的專案裡跑這些全域 CLI，可能直接壞掉。這是與 Volta 最大的行為差異。
- 補法：社群工具 [miseo](https://github.com/chancancode/miseo)（[[miseo-README]]）把每個全域 CLI 做成獨立的 mini mise 專案、釘住 runtime，自稱 "Volta lite"。**個人小專案、星數極少，採用前自行評估**；它同樣靠 `~/.miseo/.bin` 的 symlink 轉接。

**3. 專案版本檔不相容（一手：官方 Node 文件）**

- mise **不讀** `package.json` 的 `volta` 欄位。
- `.nvmrc`、`.node-version`、`devEngines` 這類「慣用版本檔」**預設停用**，要先 `mise settings add idiomatic_version_file_enable_tools node`。
- 不想動團隊共用的 repo 時，可放不進版控的 `mise.local.toml`。#2080 也有使用者用 `exec` 模板以 `jq` 讀 `volta` 欄位當過渡（單一使用者做法，未驗證）。

**4. pnpm 走內建 registry 較穩（本機實測）**

pnpm 新版改以原生 binary 發佈，安裝時靠 postinstall 換掉占位檔。用 `"npm:pnpm"` 安裝時這步沒有跑，執行即 `SyntaxError`。改用 mise 內建的 `pnpm`（aqua backend，直接下載獨立 binary）即正常，而且不依賴當下的 Node 版本。

## 五、遷移清單：容易漏的隱藏依賴（本機實測）

shell 設定檔之外，還有地方會把 `~/.volta` 寫死，刪 Volta 前要先搜：

- **systemd user service** 的 `Environment="PATH=..."`：安裝時抓當下 PATH 寫死，不讀 shell 設定。
- **工具自動產生的 launcher 腳本**：例如 IDE 的遠端 relay 腳本把 node 路徑預設為 `~/.volta/bin/node`。這類腳本常以「依序找 Volta → asdf → fnm → mise」偵測 node，Volta 還在時會優先選它。
- 搜法：`grep -rIl "\.volta" ~/.config ~/.local/bin <其他工具目錄>`，並用 `ps` 確認沒有程序正跑在 Volta 的 node 上。

**WSL 特有：Windows PATH 會墊底接手。** WSL 預設把 Windows PATH 接在後面，Linux 端找不到的指令會悄悄執行 Windows 版。換掉 Volta 後，常用指令都由 Linux 端的 mise 提供，這個風險大減但沒消失。要徹底切斷可在 `/etc/wsl.conf` 設 `[interop] appendWindowsPath=false`，再手動加回真正需要的 Windows 目錄。要注意有些工具**靠 Windows 端的 `powershell.exe`、`curl.exe` 運作**，例如 [[WSL-剪貼簿貼圖到-Claude-Code]] 的貼圖橋接走 PowerShell，某些 IDE 的 agent hook 在 WSL 連不到 Windows localhost 時會退回用 `curl.exe`。這幾個目錄必須加回。遇到指令行為怪異，先 `which -a <指令>` 看是否落到 `/mnt/c`。

## 來源（raw）

- 停止維護公告與社群討論：[[Volta-Unmaintained-Issue-2080]]
- mise 官方文件：[[mise-Docs-Shims]]（activate／shims）、[[mise-Docs-npm-Backend]]（全域 CLI 的 runtime）、[[mise-Docs-Node]]（慣用版本檔預設停用）
- 替代方案評比：[[Comparing-Node-Version-Management-Tools]]、[[Proto-as-Volta-Replacement]]（單一作者）、[[Can-Mise-Replace-Volta]]（2024，部分過時）
- 全域工具釘版本：[[miseo-README]]

## 交叉引用

- zsh 讀檔範圍：[[Yazi-設定與踩雷]]——snap 的 `/snap/bin` 只寫在 bash login 讀的檔，與本頁「非互動 shell 要放 `.zshenv`」是同一套 zsh 啟動檔規則的兩個面。
- Windows 端依賴：[[WSL-剪貼簿貼圖到-Claude-Code]]——其 PowerShell 橋接是關閉 `appendWindowsPath` 時必須保留 Windows 路徑的實例。
