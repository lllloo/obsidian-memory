---
title: Buzz 多 Agent 協作工具實測與取捨
description: Jack Dorsey 的 agent 群組聊天工具實測：context 重複傳送使 token 加倍，但跨模型對抗式審查與行為歸屬追蹤是他處少見的價值
created: 2026-08-17
updated: 2026-08-17
source: https://www.youtube.com/watch?v=a8tLTd4q-fU
published: 2026-08-04
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - token-optimization
  - sub-agent
  - security
---

## Buzz 是什麼

Buzz 由 Twitter 與 Square 共同創辦人 Jack Dorsey 推出，**上線前兩週就拿到超過 20,000 顆星**，仍是非常早期的版本。已經有人稱它為 Slack killer，並拿它和 Hermes、Open Claw 這類 agent 設定比較。

它本質上是一個讓你從單一位置協調多個 agent 的 app——就是一個群組聊天，只是聊天室成員除了人，還有你的 AI agent。**完全免費且開源**，這也是它被稱為 Slack killer 的原因。

### 與既有做法的差異

| 做法 | 限制 |
|---|---|
| Claude Code 的 agent teams | 全部發生在你的終端機裡，團隊其他人看不到；而且只會啟動 Claude agent，不能用其他家的 |
| Claude Tag（Anthropic 在 Slack 的版本） | 只有 team 與 enterprise 方案可用，Pro 與 Max 不行 |
| Codex 的 Slack 整合 | 所有付費方案都可用 |
| 同時接上兩者 | **兩邊完全沒有辦法互相配合**，而且都只在人 mention 它們時才動作，中間每一項任務都得你自己搬運 |

Buzz 的切入點就在這裡：**它讓 agent 直接互相對話**，一個 agent 可以把工作交給另一個，它們像團隊成員一樣協調，而不是等你逐則轉達訊息。

### 主要能力

- 可以接上你已經在付費的 Claude Code 與 Codex 訂閱，加上 Dorsey 自己的 coding agent **Goose**，讓它們一起處理同一件事。
- **行為歸屬追蹤**：每個 agent 有自己的名字與自己的登入身分，該 agent 做的每件事都記在那個名字底下。出問題時可以往回捲，找出是哪個 agent 做的，甚至能查到是誰要求那個 agent 做那件事的。
- **共享記憶**：agent 一邊工作一邊建立自己的記憶（作法和 Claude Code 一樣），邊做邊寫筆記並把筆記互相連結，讓下一個 session 開始時就知道上次的結論、不必冷啟動。**這些筆記全部放在頻道裡，該頻道的每個 agent 都會拿到，不只是寫它的那一個。**

## 安裝與設定

- GitHub 頁面上的 quick start 是給想自己 host 的人用的，不必走那條比較難的路。
- 改到 latest releases 頁面，捲到 asset 區塊直接下載對應作業系統的安裝檔。不確定該用哪個的話，可以把連結給 Claude Code 讓它幫你下載正確版本。
- 安裝方式與一般 app 相同。第一次開啟有兩條路：**加入別人已建好的 community**（需要對方的 community 連結與邀請），或**自己建一個**。建立時你取一個名字，那個名字就成為你的位址，並且由官方替你託管，不必自己架設。
- 之後連接 agent，app 幾乎全部代勞。如果你還沒有 Claude Code，app 會一併安裝它以及 Buzz 執行該 agent 所需的一切。**唯一需要碰終端機的時候是登入 Claude 帳號那一次。**
- 建立 agent：安裝後預設有三個，可以再自行建立任意數量。點 create agent、給名字與描述（**描述即成為它的指示**），選擇你已安裝的 coding 工具、挑模型，建立後即上線。

## 實測：哪裡壞掉

作者用一個 Claude agent 與一個 GPT agent，要求它們一起建一個社群網站。

**第一輪（籠統的 prompt）**：只 tag 兩個 agent 並說明需求。開頭不錯，兩者都做了計畫並互審對方的，然後開始互相 tag。GPT 給完審查後 tag 了 Claude，Claude 回說看到訊息了——**然後就沒有了**。它們就停在那裡，直到人進去推它們一把才繼續。

**第二輪（詳細的 prompt）**：給出逐步的明確指示，並明確指定 **Claude 做計畫、GPT 審查計畫**。這輪好很多，兩者協調得當。

**建置階段的問題**：計畫完成後請它們開始建，Claude 動了起來（可以即時看到 Claude 的活動，包括它的 to-do 追蹤與正在做的每件事）。但**用這種方式建 app 撐不住**：

- 比直接在終端機跑 Claude Code **慢很多**。Claude Code 會同時處理建置的多個部分，而 Buzz 是一個接一個做。
- 連規劃階段用掉的 token 都遠超過應有的量，而且**這是設計問題，不是設定問題**。

### 根因：context 被送了兩次

要理解這個問題得先知道 Claude Code、Codex 這類 agent 工具的 context window 怎麼運作：**模型本身不會記得你過去的訊息，所以每次都要把整段對話重新送過去**——你的舊訊息、Claude 給過的回覆，加上你剛打的新 prompt。

Buzz 在每個 agent 背後跑一個 Claude Code session 來做事，而 **Claude Code 自己的記憶裡已經保有那份對話**。

問題在於：**你每送一則新訊息，Buzz 不是只轉發那一則，而是把整段對話歷史一起送過去。** 於是同一段對話同時存在兩個地方，**你用掉的是原本需要量的兩倍 token**。

而且**每多一個 agent 就是一個各自帶著自己 context 的 session，所以成本不是相加而是相乘**。（Anthropic 對 agent teams 也是同樣說法：token 用量隨你跑的 agent 數量上升。）

平心而論，這是 Buzz 目前的狀態——它是一個上線兩週、版本 0.5 的產品，這些問題都屬於會被修掉的那一類。**方向沒有錯，只是它還不是你會把團隊搬過去的東西。**

### 額外的 token 觀察

即使只是回覆一則簡單訊息，也會走完一整套思考流程並在途中拉進一堆工具，所以吃掉的 token 遠超你的預期：**回覆一句問候用掉 31,000 token；同樣的事在終端機的 Claude Code 裡約 4,000 token**，而且是送了完全相同的 context 的情況下。因此任何長時間執行的東西都會很花錢。

## 做對的部分

以下沒有一項構成「該換過去」的理由，但這是 Buzz 值得關注的原因，也是這類 agent 工具中最接近真正像 Slack 的一個。

**Huddles**：像在 Slack 裡和團隊開 huddle 一樣，只是對象是你的 agent。開一個、agent 加入，你就能和它對話、它也會回你。目前**有點壞掉**，因為 agent 回覆用的是 markdown，而 markdown 被朗讀出來的效果正如你所想像的那麼怪。

**Compute sharing**（內建於 app）：讓你把手邊的幾台 Mac mini 或其他電腦串起來，用合併後的算力託管一個大模型，並把整套設定分享給團隊，讓所有人都用同一個。Buzz 甚至會告訴你你的設定跑得動哪些模型，大約有 35 個可挑。（這正是先前一波人買 Mac mini 串起來、想在自己電腦而非別人伺服器上跑大模型的做法。）

**匯出 agent**：不只匯出設定，**記憶也一起帶走**——agent 摸索出來的一切都跟著它走。你會拿到一個 JSON 檔或 PNG，帶到別的地方匯入即可。

**訊息 ID 與可搜尋的記錄（最重要的一項）**：Buzz 為每一則訊息指派 ID 來追蹤，不論是人或 agent 發的，你可以像搜尋 Slack 一樣搜尋全部內容，查出哪個 agent 做了什麼、以及是誰要求它做的。對團隊而言，弄清楚哪個 agent 做了什麼，對於確保工作方向一致非常重要。**這是這裡唯一一件別人沒有好好做過的事。**

## 最適合的用途：對抗式審查

已經確認在 Buzz 上做建置是不行的，但有一件事它真的最擅長：**讓 agent 互相爭論**。

這叫 **adversarial review（對抗式審查）**：讓一個 agent 攻擊產出、另一個防守，兩者之間就能抓出單一 agent 自己會漏掉的東西。

設定方式是 mention 你要的 agent，並各自指派立場。作者的做法：

1. 讓 GPT 去攻擊 PRD（說明 app 應該做到什麼的文件），**指示它假設 PRD 裡的每一項都是錯的**；Claude 負責防守。
2. 兩個 agent 在同一個 thread 裡進行。GPT 先提出論點並 ping Claude 針對這些點防守 PRD。
3. Claude 逐點回應，兩者從此來回往返。
4. GPT 提不出新的反對意見後，Claude 寫出最終計畫並請人確認。

**共享空間的價值就在這裡**：兩個 agent 都看得到整條 thread，所以它們知道已經做過哪些工作、已經爭論過什麼，而不是被丟一個 prompt 然後叫它去審查某個東西。

Claude Code 的 agent teams 也做這件事、而且做得很好，但**那裡每一個 agent 都是 Claude，而且 session 結束時爭論也跟著消失**。在 Buzz 裡是兩家不同公司的模型互相交鋒，而且整段內容事後仍然留在那裡。

## 結論：該不該用

**個人開發者：不要。** 這樣協調一群 agent 不值得，因為你想要它的每個用途，都已經在你付費的訂閱裡了：

- 想同時跑好幾件事 → sub-agent 做得到，而且更便宜。
- 想讓 agent 互相爭論、彼此抓漏 → Claude Code 有 agent teams，Anthropic 自己的文件就給了「五個 agent 試圖推翻彼此的理論」這個例子。
- 想讓對手的模型審查你的工作 → OpenAI 出了官方 plugin 把 Codex 放進 Claude Code，而且**早在 Buzz 出現的四個月前（三月）就推出了**。

所以 Buzz 的 agent 切換是你白付的成本。Claude Code 與 Codex 各自都是完整的設定，本身就有自己的工具與整合、彼此串接好了，而且更快、用更少 token。

**團隊：另一回事。** 因為現在你確實無法分辨哪個 agent 改了什麼、又是誰觸發的。**這是真正尚未被解決的問題，而 Buzz 是唯一有人拿出來的認真答案。**

不過取捨很鮮明：**Buzz 給你一份近乎完美的「agent 做了什麼」的記錄，卻幾乎不給你任何「agent 被允許做什麼」的控制權。**

### 團隊採用前必須知道的兩個早期版本問題

1. **沒有端對端加密**——伺服器的營運者可以讀到裡面的每一則訊息，包括你的私人訊息。而且這是刻意的，因為他們要讓每一件事都可被搜尋，好讓 agent 拿得到所有 context。
2. **無法把 agent 限制在單一頻道**——你加進去的任何 agent 都能看到整個 workspace 裡發生的所有事。

因此團隊若有任何需要保密的東西，目前做不到。
