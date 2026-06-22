---
title: Ponytail 開源 Skill 讓 Claude Code 更省 token
description: 評測 Ponytail 這個強迫 Claude Code 少寫程式碼的開源 skill，發現它在 Opus 4.8 上比 Haiku 4.5 更省 token、更便宜也更快。
created: 2026-06-22
updated: 2026-06-22
source: https://www.youtube.com/watch?v=aTPTUYC44ds
published: 2026-06-19
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - token-optimization
  - workflow
---

Ponytail 是一個開源 skill，發布 7 天就衝上 40,000 stars。它聲稱能讓 Claude Code 更快、更便宜，並寫出更少的程式碼，同時維持原本的高品質結果。它不是第一個這類工具（影片提到先前的 Caveman 也是同樣概念）——核心想法都是 Claude Code 天生囉嗦，只要叫它別講那麼多，就能得到更精簡、但同樣正確（甚至更正確）的答案。Ponytail 只是這條路線最新、且宣稱數字最漂亮的一版。

## 運作原理：寫程式前的六步檢查

Ponytail 的精髓是在寫任何程式碼之前，先跑一套六步流程，本質上都在問「這個功能是不是已經原生存在、需不需要自製」：

- 這東西到底需不需要存在？不需要就完全不寫。
- 標準函式庫（standard library）能做嗎？能就直接用。
- 這是不是平台原生功能（native platform feature）？
- 這是不是已安裝的相依套件（installed dependency）？
- 能不能一行解決？
- 真的需要寫得這麼囉嗦嗎？

若以上全都「不行」，才動手寫，而且只做剛好能動的最小實作，不過度發揮。影片把這個目標形容為：讓 Claude Code「偷懶但不失職」（lazy but not negligent）。

關鍵在於 Claude Code 常見的問題是「輪子明明已經造好了」，它卻還是從頭再造一個——這正是程式碼暴增的主因。Ponytail 的六步流程就是要攔下這種重造輪子的行為。

不過有些事永遠不會被砍：凡涉及信任邊界驗證（trust boundary validation）、資料遺失處理、安全性、無障礙（accessibility）的部分都不在精簡範圍內。所以它對「該套用精簡」與「不該套用」是有分寸的。

## 安裝與指令

- 安裝只要複製一行指令即可，且不限 Claude Code——也能用於 Codex 或其他 AI agent。
- 有 light、full、ultra、off 幾種強度等級（作者形容很像 Caveman 的強度分級）。
- 另提供 review（審查程式碼）、audit（稽核 repo），以及 debt、gain、help 等 skill，細節可到 GitHub repo 查。

## 評測結果：模型越強，效果越好

repo 內附完整 benchmark 與重現方式，作者實際重跑了約 19 個 benchmark。原始 repo 用的是 Haiku 4.5（理由是成本考量），但作者額外用 Opus 4.8 再跑一次，因為實際在用的是 Opus 而非 Haiku。結論是：模型越強，Ponytail 的效益越明顯。

**程式碼行數（lines of code）**

- Ponytail 官方宣稱可減少約 54%。
- 作者用 Haiku 4.5 重跑為 56%（幾乎一致）。
- 作者用 Opus 4.8 重跑達 71%。

原因是越強的模型越愛「講話」、越囉嗦，有時甚至會把自己講到偏離正確答案，所以對它套上精簡約束的收益更大。作者認為官方用 Haiku 測試反而低估了這個 skill 的效益。

**成本（cost）**

- Haiku 4.5：聚合約減少 25%。
- Opus 4.8：聚合約減少 53%。
- 範圍從最低 13% 到最高 73%（multi-step wizard 案例）。
- 具體例子：原本用標準 Opus（不裝 skill）要 $139 的任務，裝 Ponytail 後只花 $38。
- 反例：在 Haiku 這類小模型上，某些案例反而更貴——count items benchmark 上用 Ponytail 比不用貴了 21%（不過實際差額只有約 2 美分）。原因是小模型本來就「又笨又快」、已經夠精簡了。

**速度（speed）**

- Haiku 4.5：約快 31%，但有三個案例反而更慢（最差約慢 22%）。
- Opus 4.8：每個 benchmark 全面更快，最高達 88%（如 date picker 88%、multi-step wizard 78%），最差案例也有 27% 差距。

## 重點結論

- 核心規律：模型越強，這套「少寫程式碼」架構越有效；在小模型上效益不明顯、偶爾反效果。
- 作者表示拿 Haiku 的數字會讓人覺得「20% 而已、不太有感」甚至像唬人，但換成 Opus 結果天差地別、明顯更有效。
- 既然本質只是一個 skill，幾乎沒有嘗試的下檔風險——最壞情況是某些特別複雜的專案上，要求精簡反而失準，但屬於「無傷大雅」（no harm, no foul）。
- 作者已用 Caveman 一兩個月、固定自動載入，現在打算改用 Ponytail。在大家滿口都是 token 成本的當下，任何能降低成本的工具都會受歡迎。
- 作者也表達很想看到這套用在 Fable（影片形容為非常昂貴的模型）上會是什麼結果。
