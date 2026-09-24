---
title: Yazi 設定與踩雷
description: 在終端多工器 pane 裡補上檔案與 diff 檢視的三條路線，含 snap 安裝的 PATH 陷阱、圖示與隱藏檔設定、WSL2 三條邊界與背景 pane 卡頓
created: 2026-09-21
updated: 2026-09-24
source: https://yazi-rs.github.io/docs/
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - automation
  - wsl
---

# Yazi 設定與踩雷

本頁的起點是一個具體缺口：[[Herdr-使用方法]] 是終端原生的 agent 多工器，沒有 GUI 的檔案總管與 diff 檢視，而 Orca（桌面 ADE）有。要在不換工具的前提下補上「瀏覽 repo、看 coding agent 改了哪些檔」，yazi 是其中一條路。

證據強度分三層，逐條就地標：**本機實測**（2026-09-21 在使用者 Ubuntu 24.04 / WSL2 / yazi 26.9.1 snap 上跑過）、**一手**（官方文件、GitHub issue 與原始碼）、**單一回報者**（論壇留言，未經獨立確認）。

## 一、補檔案檢視的三條路線

| 路線 | 代表 | 取捨 |
|---|---|---|
| Herdr plugin | [`herdr-file-viewer`](https://github.com/smarzban/herdr-file-viewer)（唯讀檢視器）、[`herdr-sidebar`](https://github.com/alexarthurs/herdr-sidebar)（VS Code 風側欄）、[`persiyanov/herdr-reviewr`](https://github.com/persiyanov/herdr-reviewr)（可在 diff 上留言送回 agent） | 與 agent 狀態整合最深，但綁 Herdr 版本 |
| 通用終端 TUI | yazi（瀏覽）＋ lazygit（看變更） | 不綁任何多工器，換回 tmux 照用；不知道 agent 狀態 |
| 旁開 GUI 編輯器 | VS Code + Remote-WSL 指向同一 repo | 功能最完整，代價是多開一個 Electron，抵銷 Herdr 輕量的優勢 |

Herdr 的 plugin 機制（`herdr plugin install owner/repo`）能裝 action、pane、event hook，官方有 marketplace 自動索引帶 `herdr-plugin` topic 的 repo（一手，[plugins 文件](https://herdr.dev/docs/plugins/)）。**2026-09-21 選了第二條路**：理由是不綁多工器、單一 binary 好裝、不合用直接關掉。第三條路留作「想用滑鼠點、想要完整編輯器」時的升級選項。

## 二、安裝與最小設定（本機實測）

snap 一行可裝（`sudo snap install yazi --classic`），classic 模式無沙箱限制、讀寫 home 與 repo 正常。但有一個**只在 zsh 使用者身上出現的陷阱**：

- Ubuntu 靠 `/etc/profile.d/apps-bin-path.sh` 把 `/snap/bin` 加進 PATH，**該檔只有 bash 的 login shell 會讀**。zsh 的 login 與非 login shell 都讀不到，結果是裝好了卻 `command not found`。
- 解法是在 `~/.zshrc` 自行 `export PATH="$PATH:/snap/bin"`。這不是 yazi 的問題，任何 snap 裝的 CLI 在 zsh 下都會踩到。

最小設定兩項，皆為官方文件一手：

```toml
# ~/.config/yazi/yazi.toml
[mgr]
show_hidden = true
```

`[mgr]` 是由舊名 `[manager]` 更名而來，引用舊文件的設定片段會無聲失效。同段可調的還有 `ratio`（3 元素陣列，設 0 可隱藏面板但至少留一個非零）、`linemode`、`sort_by`（8 值：none/mtime/btime/extension/alphabetical/natural/size/random）、`sort_dir_first`。

**圖示需要 Nerd Font，字型必須裝在 Windows 端**（WSL 裡裝無效，畫面是 Windows 程式在畫）。不想處理字型就在 `theme.toml` 清空 `[icon]` 的五個陣列與 `[status]` 的分隔符號（官方 FAQ 提供）。作者 sxyazi 對此類回報的立場是「yazi 不控制圖示渲染，那是終端行為」，以 not-a-bug 關閉（[issue #2179](https://github.com/sxyazi/yazi/issues/2179)）。終端若支援 fallback 字型，只裝 `Symbols Nerd Font` 即可；Windows Terminal 只能設單一字型（**未查證**），故建議直接裝整款 patched 字型。

官方另建議加 `y` 這個 shell wrapper（[Quick Start](https://yazi-rs.github.io/docs/quick-start) 原文），用 `y` 啟動、按 `q` 離開時 shell 會停在最後瀏覽的目錄，按 `Q` 則留在原地。

## 三、對「看 agent 改了哪些檔」的專用件（一手）

官方 monorepo 的 19 個外掛中只有兩個針對 Git，分工不同：

- **`git.yazi`**：把 Git 變更狀態顯示成檔案清單的 linemode。需 `require("git"):setup { order = 1500 }` 並在 `yazi.toml` 註冊 `[[plugin.prepend_fetchers]]`（`*` 與 `*/` 各一）。
- **`vcs-files.yazi`**：直接列出變更檔案，實作為 `git diff --name-only --relative HEAD` 加 `git ls-files --others --exclude-standard`，以 `vcs://` 虛擬檔案系統 yield。**限制是相對 HEAD**——agent 一旦 commit，清單就不再列出。

官方 Tips 另收錄 `g r` 一鍵 cd 回 repo 根目錄（社群 @aidanzhai 投稿）：

```toml
[[mgr.prepend_keymap]]
on   = [ "g", "r" ]
run  = 'shell -- ya emit cd "$(git rev-parse --show-toplevel)"'
```

`$(...)` 外的雙引號是原文就有的，多處轉錄會剝掉，少了它含空格的 repo 路徑會失敗。

外掛安裝管道是 `ya pkg`（官方 README 稱引入於 v25.5.31，取代舊的 `ya pack`；release notes 未能獨立確認）。**`ya pkg` 在 snap 版可用**（本機實測 `ya pkg list` 正常回傳）——[issue #2903](https://github.com/sxyazi/yazi/issues/2903)「ya is not exposed from the snap build」是 25.6.11 時期的回報、已關閉，不影響 26.9.1。這條原本是研究報告列的頭號開放問題，實測後直接消解。

## 四、踩雷

**背景 pane 卡 5 秒（一手，開啟中）**。[issue #4331](https://github.com/sxyazi/yazi/issues/4331)：在 tmux 之類的多工器裡，進 yazi、開檔、按 `q` 離開時各卡約 5 秒。一位使用者比對 commit 後指出是 #4271 引入的，**26.8.15 之後的版本才有**。機制是 yazi 啟動時送 DA1 探測終端能力，在多工器裡走 passthrough，pane 在背景時回應回不來，一路等到 timeout；pane 在前景則不卡。目前無官方修正，留言提到的 workaround 是降版到 26.5.6 或改用 Alacritty。**回報全部來自 tmux，Herdr 是否重現未驗證**——Herdr 自行以 Rust 實作，對 DA1 passthrough 的處理不一定相同。

**flavor 舊 key 被無聲忽略（一手）**。[ayu-dark.yazi issue #6](https://github.com/kmlupreti/ayu-dark.yazi/issues/6)，**測試版本正是 26.9.1**：yazi 未用 `deny_unknown_fields` 也未定 serde alias，舊 key 不報錯、不警告，只是那幾個元件悄悄退回內建預設色。`[help] on`→`chord`、`[help] run`→`action`、`[help] footer` 移除（皆 26.8.15）、`[completion]`→`[cmp]`（25.2.26）、`[select]`→`[pick]`（v0.4.0）。症狀是「顏色怪怪的但說不上哪裡」。

**外掛只保證與 HEAD 相容（一手）**。官方 monorepo README 開頭警告逐字：「most of the plugins below only guarantee compatibility with the latest code of Yazi」，sxyazi 在 [#2579](https://github.com/sxyazi/yazi/issues/2579) 加強為「latest nightly」，並把相容矩陣提案婉拒關閉——**這是官方的取捨立場，不是待補 TODO**。snap 的固定版本不在保證範圍內。削弱面：官方外掛有 `@since` 機制，git.yazi／full-border／chmod 標 `@since 26.8.15`、smart-enter 標 25.5.31，皆 ≤ 26.9.1，實務上多半可用。`ya pkg` 安裝時不做版本檢查，不合要到載入期才報錯。

**`ya pkg upgrade` 的 hash 誤判（單一回報者，未重現）**。[#3291](https://github.com/sxyazi/yazi/issues/3291) 回報外掛未被修改卻被判為已修改而中止升級，跨 macOS 與 Ubuntu、跨多個外掛與 flavor；issue 以 needs-info 自動關閉，關閉 32 天後回報者仍說每隔幾天再發生。維護者未能重現，工作假設是「用 git 同步 package.toml 的跨機 dotfiles」才觸發。**只有一位回報者**（iandol），無獨立確認。

## 五、WSL2 三條邊界（一手，3-0 全票）

1. **`for = "windows"` 在 WSL2 永遠不會命中**。`[opener]` 的平台判定是編譯期 `cfg!`（`platform.rs`：`Self::Windows => cfg!(windows)`），WSL2 跑的是 Linux build（`Triple: x86_64-unknown-linux-gnu`），原始碼無任何 WSL 特例分支。想用 Windows 程式開檔，必須在 unix/linux 分支自己填 `explorer.exe`／`wslview`。
2. **Windows 缺 `file(1)` 那組坑不適用**。官方安裝文件要求 Windows 使用者裝 Git for Windows 並設 `YAZI_FILE_ONE`，[issue #3455](https://github.com/sxyazi/yazi/issues/3455) 的 debug 明載 `WSL: false`、`Triple: x86_64-pc-windows-msvc`，是原生 Windows。Ubuntu 預設已有 `file`，WSL2 不需設。
3. **複製檔案到 Windows 剪貼簿：沒有內建，官方也沒給 WSL 寫法**。`yank` 只進 yazi 內部 buffer、`copy` 只複製路徑文字；官方 Tips 唯一談剪貼簿的一節標題字面就是「Linux: ...」，只給 xclip／wl-copy 的 `text/uri-list` 寫法。**本機實測**：`wl-copy` 在 WSLg 下能跑、能送字串，但 Windows 端 `Get-Clipboard -Format FileDropList` 回空、`-Format Text` 才拿到——沒有 CF_HDROP，貼到檔案總管貼不出檔案。旁證 [microsoft/wslg#467](https://github.com/microsoft/wslg/issues/467) 顯示 WSLg 剪貼簿橋接只做文字類格式。可行方向是改呼叫 PowerShell `Set-Clipboard -Path`，**未實測**。這與 [[WSL-剪貼簿貼圖到-Claude-Code]] 是同一條 WSLg 剪貼簿限制在不同方向上的表現（該頁是 Windows→WSL 的圖片，本頁是 WSL→Windows 的檔案）。

## 六、第一手心得（單一回報者，經 HN Algolia API 核對原句）

**外掛缺可靠的退出 hook**。[Klaster_1（2026-04-12）](https://news.ycombinator.com/item?id=47737776)逐字：「there's no reliable exit hook and plugins have to override hotkeys and resort to various hacks. I had to patch a session saving extension so it kills mpv-based music preview plugin after yazi quits with "q". Kinda rough experience, but at least manageable with plugins in Lua.」他從 Total Commander 遷來，整體評價為 feels nice。意涵是外掛裝多了之後收尾行為可能不乾淨。

**「不能在當前目錄內過濾」已過時**。[BaculumMeumEst（2023 首發串）](https://news.ycombinator.com/item?id=37531434)用了一天就切回 nnn，理由是找不到只過濾當前目錄的方法、用 `fd` 會撈出整顆硬碟。**此問題已解**：現行預設 keymap 含 `{ on = "f", run = "filter --smart", desc = "Filter files" }`（本機核對 main 分支 `keymap-default.toml`）。同串另有使用者反映文件不足、連按 `?` 開說明都找很久，作者當場承認並邀社群寫 quick guide。

**沒查到的**：用了數月的長期評價、與 ranger/lf/nnn/broot/superfile 的實際切換感受、效能問題、資料遺失風險。deep-research 五路搜尋在這面向零條主張通過驗證，**該面向視同未查到，不要用設定面的證據去填補**。

## 七、勿引用

以下為 2026-09-21 對抗式查證中 0-3 或 1-2 落敗的主張。**落敗不代表反面為真**，只是無可靠結論：

- 「Windows Terminal 自 v1.22.10352.0 起以 Sixel 內建支援圖片預覽」「升級終端後 WSL2 圖片預覽即正常」「Windows 版受 ConPTY 限制、`wezterm ssh` 可繞過取得完美預覽」——整組落敗。**「WSL2 能不能看圖片／PDF 預覽」目前沒有可引用的結論**。
- 「snap 內建 fzf 0.44.1 太舊導致 `z`／`Z` 的 zoxide 對話框失效」「snap 沙箱會讓 yazi 優先用內建依賴而非 PATH 上的新版」——皆 0-3 落敗。若日後裝了 fzf 發現 `z` 無反應，再回頭查這條。
- 「Matt-FTW/dotfiles 的 `g r` 綁法證明外接 git 是常見做法」——1-2 落敗，單一 dotfiles 不足以證明採用率。
- 「最多人採用的鍵位／linemode／ratio／sort 偏好」——**本輪沒有任何具採用率證據的主張存活**，可設定面不等於多數人怎麼設。

## 八、方法論教訓（2026-09-21）

這輪 deep-research 跑了 100 個 agent、5.5M token、約 16 分鐘，**成本效益不佳**：16 條存活主張中，設定面的多數在事前用 `gh` 打 API 讀 repo 與官方文件時已取得。新增價值最高的三條裡，兩條（HN 原句、`ya pkg` 在 snap 可用）由主 agent 事後補查，一條（#4331 背景 pane 卡頓）**五路搜尋全數漏掉**。

三個重複出現的失效模式，與 [[平行跑多個-coding-agent-的工具選型]]、[[長跑-Agent-的目標定義與計畫工具]] 記錄的同型：

1. **verifier 過度否決**：把「已過時的抱怨」整條殺掉，而非標記為過時；論壇心得整批陣亡，導致報告自稱「該角度落空」，實際上搜尋階段有撈到，死在驗證階段。
2. **一手 repo 該自己讀**：`gh` 打 GitHub API 讀 issue／原始碼／dotfiles，成本遠低於派搜尋 agent，命中率也高。
3. **subagent 會在本機做實測**：這輪有 agent 直接在使用者機器上跑 `wl-copy` 與 PowerShell 讀剪貼簿。結果強度確實高於文件推論，但**動到了使用者的剪貼簿內容**，超出預期的研究範圍，派工時應明示邊界。

## 交叉引用

- 宿主工具：[[Herdr-使用方法]]——本頁補的正是它沒有的檔案與 diff 檢視；其 plugin 機制是本頁「路線一」的載體。
- 鍵位對照：[[Herdr-按鍵設定]]——要在 Herdr 綁一鍵開 yazi pane 的話設定寫在那裡，兩層鍵位可能互搶。
- 上游選型：[[平行跑多個-coding-agent-的工具選型]]——本頁是該頁「終端層」方案在檔案檢視面的補件；**該頁總表尚未收錄 Orca**（MIT、約 73.9k 星、有 Linux AppImage／deb／rpm），是已知缺口。
- zsh 啟動檔規則：[[Node-版本管理-Volta-停止維護與-mise-遷移]]——第二節的 snap PATH 陷阱與該頁「非互動 shell 的 mise shims 要放 `.zshenv`」是同一套 zsh 讀檔範圍的兩個面。
- 同源限制：[[WSL-剪貼簿貼圖到-Claude-Code]]——WSLg 剪貼簿橋接只做文字類格式，該頁是 Windows→WSL 方向，本頁第五節是 WSL→Windows 方向。
