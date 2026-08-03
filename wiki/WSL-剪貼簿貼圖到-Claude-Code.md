---
title: WSL 剪貼簿貼圖到 Claude Code
description: WSL2 按 Alt+V 貼圖「閃一下沒反應」的根因在解碼層而非按鍵，附把 BMP 換成 PNG 的 daemon 解法與實測數據
created: 2026-07-30
updated: 2026-07-30
parent: "[[wiki/01.index]]"
tags:
  - claude-code
  - wsl
---

在 WSL2 裡跑 Claude Code，按 `Alt+V`／`Ctrl+V` 貼剪貼簿圖片會「畫面閃一下、沒有任何文字」。直覺會怪按鍵被終端攔截，但**根因在影像解碼層**：WSLg 只把 Windows 剪貼簿的圖片曝露成 `image/bmp`，而 Claude Code 的影像管線不接受 BMP。偵測層放行、解碼層拒收，於是無聲失敗。

## 根因：三層鏈斷在最後一層

```
① 偵測  grep -E "image/(png|jpeg|jpg|gif|webp|bmp)"   → 命中 image/bmp    ✓ 通過
② 取圖  wl-paste --type image/bmp                      → 落地 BMP 檔       ✓ 通過
③ 解碼  processImage / sharp（只吃 png/jpeg/gif/webp）  → 不認 BMP          ✗ 靜默失敗
```

三個關鍵後果：

- **不會顯示錯誤訊息。** 偵測層已把 `bmp` 列入 grep pattern，所以不觸發「No image found in clipboard」，使用者只看到畫面閃一下。
- **內建的 PowerShell fallback 永遠走不到。** 取圖鏈是 `||` 短路串，第 4 條 `wl-paste --type image/bmp` 先成功，執行流程到不了後面那條用 `System.Windows.Forms.Clipboard` 直讀 Windows 剪貼簿的 fallback。fallback 被 BMP 自己攔在門外。
- **按鍵不是元凶。** WSL 下 `Ctrl+V` 與 `Alt+V` 都預設綁定 `chat:imagePaste`（官方 keybindings 文件明文「On WSL, both shortcuts are bound by default」），「畫面閃一下」本身就證明按鍵到得了 TUI。

## 證據與強度

| 主張 | 證據 | 強度 |
|---|---|---|
| 解碼層不支援 BMP | 把剪貼簿抓下的 BMP 餵給 Claude Code 的 Read tool，回「cannot read binary files」，被當二進位垃圾而非圖片 | **一手實測**（2026-07-30、Claude Code 2.1.220、WSL2 Ubuntu-24.04、Windows Terminal） |
| 偵測層已含 bmp、取圖鏈有四條 | `strings` 直接讀 Claude Code binary，取得完整 grep pattern 與 `xclip`／`wl-paste` 四條取圖指令 | **一手實測**（同上） |
| 格式白名單為 png/jpeg/gif/webp | binary 內緊接 `processImage` 後的字串常數，與 Claude API 可接受的 media type 一致 | 一手實測；白名單用途為推斷 |
| WSL 雙鍵預設綁定 | 官方 keybindings 文件 `chat:imagePaste` 欄 | 一手官方文件 |
| PowerShell fallback 的引入版本 | [#57440](https://github.com/anthropics/claude-code/issues/57440) 作者稱 v2.1.136 | **單一 issue 作者說法**；官方 CHANGELOG 線上僅保留近百餘版，**無法獨立驗證版本號**。功能存在於 2.1.220 則已實測確認 |

**勿引用**：網路搜尋摘要流傳「WSL 貼圖已在 v2.1.157 修好並新增專屬 `Alt+V` 鍵」——官方 CHANGELOG 查無任何 `Alt+V` 條目，此版本號無依據；且若真已修好，2.1.220 不會仍在解碼層失敗。

官方文件的「Work with images」章節至今只列拖曳、`Ctrl+V`、給路徑三種通用方法，**完全沒有 WSL 相關說明**——這正是 [#57440](https://github.com/anthropics/claude-code/issues/57440) 在告的事（該 issue 已 closed，但文件缺口經查證仍在）。

## 解法：把 BMP 換成 PNG 的背景 daemon

不必等官方，也不需要 ImageMagick 之類的轉換器——Windows 端自己就能編碼 PNG：

```
輪詢 wl-paste -l
  → 見 image/bmp 且無 image/png
    → PowerShell 取圖存 PNG（System.Windows.Forms.Clipboard.GetImage → ImageFormat::Png）
      → wl-copy --type image/png 回填 Wayland 剪貼簿
        → Claude Code 取圖鏈第 ② 條 wl-paste --type image/png 命中 → 貼圖正常
```

實測驗證的三個性質（2026-07-30，同上環境）：

- **不會迴圈。** 回填後 Wayland 不再曝露 `image/bmp`，觸發條件自動失效，同一張圖不會被重複處理，**不需要 hash 去重**。WSLg 也不會把 Wayland 的 PNG 反向同步回去造成格式反覆（觀察 8 秒穩定）。
- **不會弄丟 Windows 端的圖。** 回填後 `Clipboard::ContainsImage()` 仍為 `True`，在 Windows 應用照樣能貼。
- **落地的是完整 PNG。** 取圖鏈產出的檔案與來源 PNG 逐位元一致。

成本（輪詢間隔 2 秒）：平均每秒約 2.8 ms CPU、記憶體 2.4 MB。間隔 1 秒時約 5.4 ms/秒，成本與間隔近似成反比。

## 為什麼只能輪詢

事件驅動在 WSL 不存在——實測 `wl-paste --watch` 回：

```
Watch mode requires a compositor that supports the wlroots data-control protocol
```

WSLg 的 Weston 不實作 `wlr-data-control`。這條先前只有二手說法（見 [#25935](https://github.com/anthropics/claude-code/issues/25935) 內文），現有一手證據。替代的 PowerShell 常駐監看（`AddClipboardFormatListener`）雖能事件驅動，但要養一個 .NET process，記憶體開銷遠高於輪詢，不划算。

## 已知限制

- **有轉換延遲**：等於 0～輪詢間隔（間隔 2 秒時平均約 1 秒，因輪詢相位隨機）。複製後立刻按鍵可能仍抓到 BMP，再按一次即可。
- **只處理 Windows 來源的圖**：Linux 端來源的 BMP 會讓 PowerShell 回 `no-image`，直接跳過。
- **daemon 一停，它 `wl-copy` 持有的剪貼簿內容即失效**——`wl-copy` 是以常駐 process 持有 Wayland selection。
- 掛成 `systemd --user` service 時有個坑：**該環境的 `PATH` 不含 Windows 目錄**，`powershell.exe` 會找不到（前景手動跑因繼承 shell 的 PATH 而正常）。改用絕對路徑即可；`WSL_INTEROP` 未設也能用絕對路徑執行 `.exe`。

## 這頁與 vault 其他頁的關係

把截圖手動貼進 Claude Code 對話（`Ctrl+V`／`Alt+V`）是「把畫面交給 agent 看」最直覺的一條路徑，在 WSL2 上這條路徑會無聲斷掉；但 [[設計品質的可量化檢測]] 那套「截圖 → AI 核對設計偏離」閉環多數走工具管線（axe-core／DeepGaze／Playwright、agent 自駕瀏覽器讀截圖檔），未必依賴人手動貼圖，官方「給檔案路徑」的替代管道也不受此限——只有真的靠貼圖這條路徑時才受影響，不宜說該頁檢測流程「跑不起來」。反方向的載體問題見 [[AI-生成流程圖與架構圖]]：那頁處理「怎麼把圖給人看」（固化成 mermaid.live 連結），本頁處理「怎麼把圖給 agent 看」。

## 上游追蹤

[anthropics/claude-code#61609](https://github.com/anthropics/claude-code/issues/61609)（open）是唯一仍開著的 WSL 貼圖 issue，但它的描述停在「Ctrl+V 沒反應」，沒觸及解碼層這個根因。官方若補上 BMP 解碼（或讓取圖鏈在 BMP 命中後轉 PNG），本頁的 daemon 即可退場。追蹤狀態見 `feeds/watch/01.index.md`。

**不主動回報上游**（2026-07-30 使用者決定）：本頁的根因鏈比 #61609 精確，但不整理成 issue 或留言送出，只被動追蹤該 issue 的狀態。本機已有 `clip2png` 可用，無須等官方修。
