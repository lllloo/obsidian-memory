---
title: Claude Code 隱藏的 /dream 功能大幅提升記憶管理
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2026-03-24
source: https://www.youtube.com/watch?v=E-1Lmyv6Cjo
---

## Claude Code 的記憶系統

Auto Memory 讓 Claude Code 在對話中自動建立 Markdown 記憶檔，無需手動操作：

- 位置：`~/.claude/projects/<專案名>/memory/`
- 結構：多個主題記憶檔 + 一個 `memory.md` 索引（每次 session 開始時載入）
- 索引格式類似技能清單：記載有哪些記憶檔及其摘要，需要時再讀取詳細內容

## 記憶系統的問題

隨使用時間累積，記憶資料夾會出現：

- **重複內容**：多個檔案說同一件事
- **矛盾資訊**：「永遠用 React」vs「永遠不用 React」並存
- **過期資訊**：已不再適用的習慣或偏好
- **相對日期**：「下星期五」沒有具體日期，隨時間失效
- **索引膨脹**：`memory.md` 越來越長，造成 context bloat

## Dream 的作用

Dream 是 Anthropic 針對上述問題的解法，執行四步驟：

1. **讀取現有記憶**：掃描 `memory.md` 索引
2. **參照最近 session 紀錄**：讀取 `~/.claude/projects/<專案>/` 下的 `.jsonl` transcript 檔（每則訊息、每次工具呼叫都有記錄），對照記憶是否符合實際使用模式
3. **整理記憶**：合併重複、解決矛盾、刪除過期內容、修正相對日期為絕對日期
4. **精簡索引**：`memory.md` 最多 200 行，愈精簡愈好

## 自製 Dream 技能

Dream 正在小範圍推出，多數用戶還沒有存取權。但 prompt 已公開（由 PyBites-AI 分享），可自行建立技能：

```
讓 Claude Code 建立一個名為 dream 的新技能，使用以下 prompt：[貼上 dream prompt]
```

建議加入執行層級選項：
- `/dream`：僅整理當前專案的記憶
- `/dream user`：整理全域（User 層級）記憶
- `/dream all`：整理專案 + 全域記憶

## 實際執行範例

執行 `/dream` 後，它識別出七個問題：
- 近似重複 ×2
- 矛盾內容 ×1
- 過期資料 ×2
- 相對日期 ×1
- 不應放在記憶的程式慣例 ×1

最終結果：合併 2 個檔案、更新 4 個檔案、刪除 3 個檔案、保留 5 個檔案不變。

## 適用時機

Dream 是「邊際效益」型工具，不會改變工作方式，但定期執行可保持記憶系統乾淨，避免 context 污染。
