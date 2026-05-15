---
title: 找工作還在手動投？Claude Code 一次跑完 6 間公司客製履歷
created: 2026-05-15
updated: 2026-05-15
source: https://www.youtube.com/watch?v=HcADayRCJMg
published: 2026-05-13
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - sub-agent
---

## 求職客製化的真實痛點

投履歷最痛的不是被拒，是花 4 小時客製一份只為了石沉大海。本支影片是 5/10 A2 GMAT 講座的現場示範，用 Claude Code 把求職流程自動化：上傳履歷 → 分層職缺 → 找真實 JD → 派 sub-agent 同時寫客製履歷 + Cover Letter。下指令不到 3 句話。

## 示範情境：模擬求職者 Jordan 林先生

設計一份未經客製的標準 CV：

- 臺大學士畢業
- Kellogg 校友（2027 年畢業）
- 過去資歷包含 hexapass、vandora 等公司的產品分析師（PM）

## 步驟一：上傳履歷，Claude 自動分出三個 Tier 職位

事先設定好個人求職工作流後，把履歷丟給 Claude Code 並請它判斷適合的職位。AI 自動抽取履歷文字後，依背景分出三個 Tier：

- **Tier 1**：消費端 PM Intern、Growth PM、monetization PM
- **Tier 2**：Strategy Consulting、Corporate Strategy
- **Tier 3**：差異化路線；明確指出不適合投的職位

## 步驟二：連到 Greenhouse / Lever 找真實 JD

下指令請 AI 針對選定 Tier 搜尋職缺，AI 直接連到北美招聘平台（Greenhouse、Lever）：

- 找到真實的 JD 並附上連結
- 點進去確認不是幻覺，全是真實開出的職位
- 列出不同地點、時區、Tier

## 步驟三：派 6 個 sub-agent 同時做客製履歷 + Cover Letter

確認 Tier 1 後，請 AI 派出 sub-agent。每個 sub-agent 負責一間公司：

- 同時開 6 個 sub-agent
- 各自輸出：分析依據 + 客製履歷 + 客製 Cover Letter
- 過程中持續回報進度，不會打擾使用者
- 全部產出在資料夾，含每間公司名、Tier、職位

## sub-agent 內部邏輯（不是隨便寫）

每個 sub-agent 背後的判斷原則：

1. 分析 JD
2. 幫履歷跟 JD 的契合度打分數
3. 根據分數改寫履歷——契合的搬到最前、字改掉、不相關的刪除
4. 寫 Cover Letter
5. 產 PDF

每份產出還附上：

- 候選人的定位
- Lead-with 前三
- Cover letter 主軸
- 風險環節（去面試時最可能被質疑的地方）

## Airbnb 範例：客製化細節

打開 Airbnb 那份 Cover Letter，內文不是模板：

> What excites me about trip cycle is that relevance at Airbnb isn't a single rank list

直接把候選人背景經歷連結到 Airbnb 的產品特性。不是隨便亂寫。

## 對比：傳統 vs 傳統 AI vs Claude Code

| 模式            | 流程                                                                     |
| --------------- | ------------------------------------------------------------------------ |
| 傳統手動        | 一件一件做，每件好好思考                                                 |
| 傳統 AI（聊天） | 你貼文字進去，AI 吐文字回來；自己複製貼上、改版面、輸出 PDF、放附件寄出 |
| Claude Code     | 一次批次全部做好——分析、客製、產 PDF、放資料夾                          |

差別不是「用 AI ≠ 產出 AI 垃圾」——AI 只是輔助，最後驗證的環節仍由人負責。

## 進階：用 Kellogg referral template 找校友

後續延伸用法：

- 請 AI 做 Kellogg referral template（找校友的四步流程）
- 設計 Template A / Template B
- 讓 AI 自動上 LinkedIn 搜尋校友
- 觀察校友的 resume，根據校友背景連結你的背景
- 把 referral template 改得更貼合對方

最會用 AI 的求職者，投遞效率比手動高很多，品質不一定差。
