---
title: Python 直譯器指令名跨平台選擇
created: 2026-06-02
updated: 2026-06-18
tags:
  - python
  - cross-platform
  - windows
  - vault-youtube-sync
---

跨平台 skill 的腳本呼叫，不假設單一 Python 指令名永遠存在。實務規則是：先跑 `python3`；如果錯誤明確是命令不存在，再改跑 `python`。

## 為什麼先找 python3

`python3` 是 macOS / Linux 的正規名，能避開裸 `python` 不存在或指向不明版本的問題：

- **macOS 現代版**：已移除 `/usr/bin/python`，裸 `python` 可能 not found；這正是當初 mac sync 失敗的根因。
- **Linux**：`python3` 正規名，`python` 常缺。
- **Windows**：不同安裝來源差異較大，官方 installer、Python Install Manager、Store alias、conda 都可能影響 `python` / `python3` / `py` 的可用性。

結論不是「`python3` 處處可用」，而是「`python3` 是優先選擇；實際執行時若命令不存在，再退回 `python`」。

## fallback 靠錯誤判斷

不需要每次都先寫一段 interpreter 探測邏輯。實務上直接跑：

```sh
python3 script.py
```

如果錯誤是 `python3: command not found`、`python3` 無法辨識之類的命令不存在問題，再改用：

```sh
python script.py
```

不要把它寫成：

```sh
python3 script.py || python script.py
```

因為這會把「腳本本身執行失敗」也當成 interpreter 問題，導致同一個腳本被跑第二次。fallback 應該由人根據錯誤訊息判斷，而不是無條件自動重跑。

這個規則讓 macOS / Linux 多數情境一次過；Windows 若沒有 `python3`，也能用常見的 `python` 手動補跑。


相關：[[Python-Windows-stdout-UTF-8-亂碼]]——同屬跨平台 Python 執行的踩坑。