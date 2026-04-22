---
title: 意想不到好用的 Claude Code Skills 合集
tags:
  - youtube
  - claude-code
  - claude-code-skills
  - agent-workflow
created: 2026-04-20
updated: 2026-04-20
published: 2026-04-17
source: https://www.youtube.com/watch?v=qQ5uObNKBOU
parent: "[[01.index]]"
---

影片介紹社群釋出的多個 Claude Code skill / plugin，它們第一眼看起來怪怪的，但實際用在多 session 並行、token 節省、品質評估等日常工作流中都意外有效。

## Peon Ping：多 session 完成通知

解決同時跑多個 Claude Code session、得手動切換確認哪個跑完或卡在 permission prompt 的問題。

- 完成任務或需要權限提示時會主動通知使用者
- 通知聲音改用遊戲角色語音（多個 voice pack 可選），而非系統標準通知
- 可搭配任何 coding agent 使用
- 安裝後以 slash command 選語音包；新 session 啟動時也會有就緒語音

## Dogfood：對抗式 Web App 審查

以 adversarial review 風格自動巡檢網頁應用程式的 bug 與 UX 問題。

- 仰賴 agent browser（CLI 工具，可送 key 事件、引用頁面元素），安裝 skill 前須先裝好
- 給一個網址（線上或 localhost）即可，或直接要求測試當前 app
- 流程：初始化報告 → 以 agent browser 逐頁巡過 → 產出詳細報告
- 報告內容：每個 bug 的重現步驟、截圖、critical/medium/low 分級，並附整段走查影片

## Caveman：壓縮 Claude 回覆的 token

針對 Claude 常見「過度解釋、塞贅詞」的回覆風格，強制它用穴居人語氣回話，號稱可砍掉約 75% token 同時保留技術正確性。

- 原理：刪冠詞、去贅字，用直給短句保留核心資訊
- 常見 filler 詞會被全部裁掉
- 有多種強度等級可調（Caveman 指令 + intensity level）
- 內建最強的 Wyan 模式改用中文回覆，因中文字單位 token 所承載語意更多；但非英文語言的準確度較低，建議一般情境仍留在英文 caveman 模式

**Claude Code 安裝步驟：**

```
# 1. 先裝 plugin marketplace
# 2. 以 plugin 指令搜尋 caveman 並在想要的 scope 安裝
# 3. reload plugins
# 4. 以 caveman 指令設定 intensity
```

回覆會用箭頭等符號把流程壓成緊湊表述。

## Git Time Travel：用 git 歷史當 agent 知識庫

讓 agent 能像翻時光日誌一樣讀懂整段 git 歷史，找出過去操作造成的問題。

- 安裝後會同時帶入 skill.md 與 references（包含各類 pattern / validation）
- references 內建多種已知地雷偵測，例如 force push 到 main、沒先備份就 rebase 等
- 使用方式：給一個問題 prompt，skill 讀完全歷史後輸出詳細報告
- 報告會標示問題點並給改善建議

## Pre-mortem：上線前預測未來 bug

在 app 上線前掃過 codebase，挑出脆弱區塊並預測未來可能發生的故障。

- 會從多個角度分析程式碼，寫出尚未發生但可能發生的 bug 報告
- skill.md 內含完整工作流、判斷 pattern 與回報格式，catalog 相當完整
- 使用方式：在已安裝的專案執行 premortem 指令；過程中可能詢問要聚焦哪些面向
- 最終報告：現存 bug + 未來潛在風險

## Mutation Testing：測試案例品質檢查

評估測試套件是否足以抓出真實 bug。

- 以 mutation 的方式在程式碼中注入不同種類的 bug，再跑測試看是否被抓出
- 會用 git revert 回滾注入的變更，因此執行前必須先 commit 所有改動
- 流程：分析專案結構 → 找測試檔 → 逐一驗證偵測率 → 產出 mutation score 報告
- 報告會列出未被抓到的 mutation，並給強化測試的建議

## The Fool：壓力測試一個想法或計畫

批判性分析並壓力測試一個 idea、plan、decision 或 proposal，協助判斷方向是否能長期走得通。

- 有多種挑戰模式，安裝後會把對應的 skill.md 與 references 帶入專案
- 執行時先問想用哪種模式挑戰，依選擇載入對應 reference 做推理
- 最終輸出多條 failure mode 報告，解釋每種失敗原因與連鎖後果
- 可與 agent 來回推敲，反覆迭代想法

## Reddit Fetch：繞過 Reddit 的 bot 封鎖做研究

Reddit 對 Claude Code 之類的 bot 有封鎖，讓市場研究很難直接抓到內容。Reddit Fetch 用以下方式取得內容：

- 首選走 Gemini CLI 搭配 Tmux（terminal multiplexer，支援 session 內開多個平行終端）
- 失敗時 fallback 到 curl 打 Reddit JSON API
- 安裝後指定要研究的主題即可，skill 會輸出該主題在 Reddit 上的使用者真實意見整理

## Color Expert：避免 agent 產出千篇一律紫白 UI

針對 agent 常收斂到相同 purple + white 風格的問題，提供設計與配色知識庫。

- 涵蓋 WCAG、palette 選擇等色彩科學面向
- 內含 100+ markdown references，來源包含 Wikipedia、YouTube 文字稿等
- 實測結果：agent 會先讀懂 skill 再依規則實作，產出留白與色彩搭配更平衡、更能凸顯重點的介面
- 即便是簡單 prompt 也能明顯改善 UI 品質
