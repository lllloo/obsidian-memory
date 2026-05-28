---
title: "Harness Engineering 到底是什麼？概念、實戰與爭議，一次全部講清楚"
description: Harness Engineering 概念定位：與 Prompt/Context Engineering 的關係、OpenAI 與 Anthropic 的實戰，以及是否噱頭爭議
created: 2026-05-06
updated: 2026-05-16
source: "https://www.youtube.com/watch?v=7nCzfgDjSo8&t=19s"
published: 2026-05-05
tags:
  - "clippings"
---
![](https://www.youtube.com/watch?v=7nCzfgDjSo8)

繼 Prompt Engineering、Context Engineering 之後，AI 圈最近又冒出了一個新名詞，叫做 Harness Engineering。本期影片，我會帶大家了解關於 Harness Engineering 的一切，具體包括：

- Harness Engineering 是什麼？
- Harness Engineering 與 Prompt Engineering、Context Engineering 有什麼關係
- OpenAI 和 Anthropic 在 Harness Engineering 方面的實戰
- Harness Engineering 的來源
- Harness Engineering 是不是噱頭？它是軟體工程領域的一次技術突破，還是 AI 圈的又一次概念炒作？

🎥 相關影片：
https://www.youtube.com/watch?v=7qO8-kx3gW8&t=1705s
https://www.youtube.com/watch?v=yDc0\_8emz7M
https://www.youtube.com/watch?v=25DEMZ7wsSM&t=630s
https://www.youtube.com/watch?v=GE0pFiFJTKo&t=2s
https://www.youtube.com/watch?v=WWdlme1EAGI&t=8s

⏱ 時間軸：
00:00 影片內容介紹
00:51 Prompt Engineering 和 Context Engineering
04:50 Harness Engineering 是什麼
09:06 OpenAI 的 Harness Engineering 實戰
18:41 Anthropic 的 Harness Engineering 實戰
27:19 Harness Engineering 是不是噱頭

🗎 相關文章連結

OpenAI:
\- Harness engineering: leveraging Codex in an agent-first world
https://openai.com/index/harness-engineering/

Anthropic:
\- Effective harnesses for long-running agents
https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
\- Harness design for long-running application development
https://www.anthropic.com/engineering/harness-design-long-running-apps

LangChain:
\- The Anatomy of an Agent Harness
https://www.langchain.com/blog/the-anatomy-of-an-agent-harness

Mitchell Hashimoto:
\- My AI Adoption Journey
https://mitchellh.com/writing/my-ai-adoption-journey

martinfowler.com:
\- Harness Engineering - first thoughts
https://martinfowler.com/articles/exploring-gen-ai/harness-engineering-memo.html
\- Harness engineering for coding agent users
https://martinfowler.com/articles/harness-engineering.html

`#AI` `#大模型` `#harnessengineering` `#openai` `#anthropic` `#claude` `#agent`

## Transcript

繼 Prompt Engineering、Context Engineering 之後，AI 圈最近又冒出了一個新名詞，叫做 Harness Engineering。從今年 2 月份開始，這個詞頻繁地在 AI 圈裡出現。OpenAI 專門發了一篇文章，講他們怎麼用 Harness Engineering 在 5 個月內寫了將近 100 萬行程式碼。Anthropic 也緊接著發文，分享了自己如何使用精心設計的 Harness 架構來驅動 Agent 的開發應用。不僅如此，就連技術大牛 Martin Fowler 創立的技術網站 martinfowler.com 也開始公開討論起了 Harness Engineering。但與此同時，也有不少人認為這不過是個噱頭而已，換湯不換藥。那 Harness Engineering 到底是什麼？它跟 Prompt Engineering 和 Context Engineering 又有什麼關係呢？Harness Engineering 是真正的技術突破，還是說只是 AI 圈又在炒概念？

這期影片，我們就來把這個事情徹底搞明白。

---

## Prompt Engineering 與 Context Engineering

在講 Harness Engineering 之前，我們不妨先來講講它的兩個前任，分別是 Prompt Engineering 和 Context Engineering。對這兩個概念比較熟悉的同學，可以直接跳到下一個章節。

首先是 Prompt Engineering。這裡的 Prompt 你可以簡單理解成用戶發給大模型的話，而 Prompt Engineering 就是一門研究怎麼把這句話說清楚的技術。舉個具體點的例子，比如說我們可以向大模型發問「幫我的貓起個名字」，這個問題就是 Prompt。接到 Prompt 之後，大模型就會給你一個答案，比如說是什麼花花啊、小白啊之類的，不過這些答案可能都無法讓你滿意，因為你家的貓可能是橘色的，無論是花花還是小白，都與橘色這個顏色相衝突。

那為什麼大模型會給你錯誤的答案呢？這是因為我們沒有在 Prompt 裡面給大模型充足的信息。既然問題出在 Prompt 上面，那解決問題的關鍵自然也在 Prompt 上面了。說得再具體一點，那就是我們需要學會如何更精準地表達自己的需求，這就引出了 Prompt Engineering。

按照 Prompt Engineering 的理念，我們需要發送的 Prompt 就應該是這樣子的：「幫我的橘色小貓起名，兩個字，需要體現出它活潑愛玩的性格」。這個時候大模型就可以給出一些更讓人滿意的名字了。說白了，Prompt Engineering 就是一門調整大模型提示詞的技術。不過如今 Prompt Engineering 已經很少被單獨提起了，一方面它的門檻實在太低，另一方面模型本身的能力也變得更強了，很多時候不需要在 Prompt 上調來調去，就能給出不錯的回答。

下面我們來看看 Context Engineering。假設你拿到了小貓的名字之後，還繼續跟大模型聊天，比如你問它「那它平時吃什麼好呢？」這個就是我們的 Prompt 了。現在重點來了，我們此時要發給大模型的，其實不僅僅有這個 Prompt，還有之前的對話歷史，這樣大模型才知道這個新問題裡面的「它」指代的是什麼。

無論是 Prompt 還是對話歷史，它們都是大模型所接收到的信息。我們把大模型所接收的所有信息起個名字，就叫做 Context。當然 Context 的內容還不只有這兩個，它還包含工具列表、Skill 列表等等。你只需要知道，Context 是有容量上限的，所以我們不可能無止境地往裡面塞東西，我們需要精心設計 Context 裡面的內容，這就叫做 Context Engineering。

Context Engineering 有很多具體的方法，比如說其中一個非常經典的技術就是上下文壓縮——當對話歷史超過某個閾值的時候，我們就可以使用上下文壓縮技術把之前的對話歷史做個總結，以防止 Context 裡面的內容過多而影響回答效果。除了上下文壓縮之外，Context Engineering 還有很多其他的方法，比如說動態檢索外部資料、漸進式披露等等。不過大家發現，Context Engineering 這門技術的效果有一定的上限。為了進一步榨乾大模型的潛力，AI 圈又整出了新花樣，這就引出了我們今天真正的主角。

---

## Harness Engineering 是什麼

要搞明白 Harness Engineering 這個概念，我們就得先從 Harness 這個單詞說起。這個詞在日常生活中其實不太常見。Harness 這個詞的本意其實是馬具的意思，就是套在馬身上、用來控制馬的那些裝備，比如說是韁繩啊、頭套啊這些。雖然馬非常強大，但是我們必須借助馬具的力量來限制馬的活動，這樣我們才能夠讓馬為人類所用。

現在我們把馬具從馬身上單獨拆下來做一個類比。左邊這匹脫掉馬具的馬，對應的就是 AI 領域裡面的大模型。大模型特別強，尤其是像 GPT、Opus 這樣的頂級模型，能幹的事情太多了。但大模型就像馬一樣，如果我們不對它加以干預，任由大模型自己去運行和發揮，那它就會像脫韁的野馬一樣發散思維，甚至產生嚴重的幻覺，最終根本無法穩定地給我們想要的結果。

所以我們必須要把大模型給控制住，就像用馬具來控制馬一樣，而這套用來控制大模型的系統就被稱為 Harness。Harness 就是 Agent 裡面用來控制和駕馭大模型的系統。所以從這一點出發，我們就能推導出 Harness 的公式：**Harness = Agent - Model**，換句話說，一個完整的 Agent 減去裡面的大模型，剩下的所有東西都是 Harness。

需要注意的是，Harness Engineering 是一個非常新的概念，目前業界還沒有形成嚴格的定義，這個公式只是目前大多數人比較認可的一種說法，並非嚴格的學術定義。

我們可以用 Claude Code 來舉例。在 Claude Code 裡面，所有不屬於 Claude 模型的部分都是 Harness，比如說是寫在 AGENTS.md 裡面那些大模型要遵循的規則、Claude Code 可以使用的工具、或者是它的定時排程機制等等，這些都是 Harness。

那 Harness 了解了，順理成章地，Harness Engineering 的概念也就呼之欲出了。Harness Engineering 就是一門專門研究如何構建與設計 Harness 的技術，換句話說就是除了大模型本身不研究，別的什麼都研究。它不再是緊盯著模型輸入的那點提示詞或者是上下文，而是站在更高的系統層面上，研究怎麼給大模型設計一套可以穩定運行的系統，讓大模型能夠踏踏實實地為人類做事。

所以 Prompt Engineering、Context Engineering 和 Harness Engineering 更像是一種層層遞進、研究範圍不斷向外擴展的關係：

- **Prompt Engineering** 研究的是怎麼問問題，具體來說就是如何組織 Prompt，把發給大模型的話說得更清楚、更準確，讓模型能夠更容易理解你的真實意圖並給出理想的結果。
- **Context Engineering** 研究的內容比 Prompt Engineering 更廣一些，它研究的是怎麼給信息，具體來說就是怎麼在最合適的時機，把最合適的內容放到模型的 Context 裡面。Context 裡面的內容不僅包括 Prompt，還包括工具列表、對話歷史等等。
- **Harness Engineering** 的研究範圍就更加激進了，它研究的是如何搭建系統，也就是如何圍繞著大模型搭建一個完整可靠的 Agent，它的研究對象直接覆蓋了除了大模型之外的所有內容，比如說是權限管控、工具管理等等。

---

## OpenAI 的 Harness Engineering 實戰

2025 年 8 月，OpenAI 內部啟動了一個瘋狂的實驗，那就是用 AI 從零開始寫一個真實的軟體產品，全程不允許工程師手寫一行程式碼。這個產品的所有組成部分，都是由 AI 生成的，具體包括業務邏輯、測試、CI 配置、文件、內部工具等等，所有東西都是 AI 生成的。靠著 AI，這個項目的程式碼規模直接幹到了將近 100 萬行，而且這不是一個玩具，它是一個真正在線上跑、有真實用戶的生產系統。達到這樣的規模，總體耗時只用了 5 個月左右，團隊規模一開始是 3 個人在主導，後來也只不過是擴張到了 7 個人，算下來開發效率差不多是純人工的 10 倍了。

有意思的是，這個實驗一開始的進展並不順利。這並不是因為大模型不夠聰明，而是因為 Harness 沒有搭建好。工程師們發現 Agent 經常走錯方向，甚至重複犯同一個錯誤。於是他們意識到，要想讓 Agent 可靠地工作，真正的功夫在於把 Harness 設計好。為此他們做了大量的優化，並且寫了一篇文章詳細記錄了這個過程。

這篇文章的優化點大致可以分三類：**上下文管理**、**驗證與反饋**、**技術債清理**。

### 上下文管理

上下文管理的主要目標，是讓 Agent 獲取到足夠充足的信息。你可以想像一下，一個新入職的工程師，如果對項目一無所知，不清楚模組怎麼劃分，不知道程式碼規範是什麼，不了解團隊過去做過哪些技術決策，那他根本就沒有辦法開始工作。Agent 也是如此。

為了解決這個問題，OpenAI 最初的嘗試是把所有的項目規範和相關信息塞進一個超大的 AGENTS.md 文件，這個文件會隨著用戶的問題一起發給大模型。不過 OpenAI 後來發現，使用一個大而全的 AGENTS.md 文件根本無法解決問題。原因有兩個：第一，內容太多會使得模型的效果變差，就像 HR 第一天砸給你一本巨厚的員工手冊，你肯定一臉懵，完全不知道該從哪裡看起，也完全搞不清楚重點在哪，AI 也是一樣；第二，這個文件會逐步腐化，項目是在不斷演進的，文件裡面的內容卻沒有人及時更新，時間一長就變成了一堆過時信息的垃圾堆。

所以他們後來改變了策略，把 AGENTS.md 文件壓縮到只有 100 行左右，基本上就是一個目錄，對應的文件系統也把相關文件和 AGENTS.md 放在一起。這樣用到哪塊再給 Agent 看哪塊，效果就會好很多。

除此之外，OpenAI 還發現項目裡面有很多重要的信息其實並不在程式碼倉庫裡面，它們可能是散落在 Slack 的聊天記錄裡，可能躺在某個 Google Docs 的文件裡，甚至只存在於某個老員工的腦子裡面。對於 Agent 來說，他只能看見倉庫裡面有什麼，倉庫外面的一切對他來說都跟不存在沒有區別。所以 OpenAI 的做法是強制要求把所有重要的決策和約定都搬進程式碼倉庫，讓倉庫成為唯一的事實來源。

### 驗證與反饋

做好了上下文管理、有了充足的信息之後，Agent 就可以寫程式碼了。後面的重點就是在 Agent 寫完程式碼之後，讓他能夠驗證自己的成果是否正確。

OpenAI 的做法是給 Codex 配上足夠完善的工具和 Skill。比如說他們把 Chrome DevTools 接入了 Codex 的運行環境裡面，這樣 Codex 就可以自己截圖、自己查看 DOM 結構，並且自己模擬用戶操作，從而去驗證 UI 是否符合用戶的要求。如果發現問題，那 Codex 就可以原地修復，整個過程不需要人去介入。除了 UI 之外，OpenAI 還給 Codex 接入了完整的可觀測性工具棧，以便讓 Codex 可以讀取日誌、讀取指標，並在必要的時候追蹤運行鏈路以排查問題。Codex 的每個任務都跑在一個完全隔離的環境裡，有自己獨立的日誌和指標，任務結束之後也能自動銷毀。

在架構合規性方面，OpenAI 把他們的系統分成了好幾層，並且規定了嚴格的依賴關係，從上到下分別是 UI、Runtime、Service、Repo、Config、Types，每一層都只能依賴它下面的層。OpenAI 是使用 linter 和測試來避免違規情況發生：在 Agent 生成程式碼之後，linter 或者測試便會開始檢測程式碼是否合規，如果不合規的話它便會報錯，報錯信息會發回到 Agent 那裡，Agent 會根據報錯信息去修改，改完之後再跑 linter 或者測試，這樣就形成了一個完整的自動閉環，不需要人工去介入。

### 技術債清理

Agent 在大規模生成程式碼的過程中，會不可避免地引入一些糟糕的設計模式，比如重複的程式碼、偏離架構規範的寫法、不一致的命名之類的，慢慢積累下去會把整個程式碼庫搞得一團糟。

OpenAI 的解法是給技術債做一些垃圾回收，具體來說就是設置一個後台的 Codex 任務，定期去掃描整個程式碼庫，找出其中偏離規範的地方，自動修改並提交，以確保程式碼的品質始終維持在一個比較高的水準。除了程式碼之外，他們還對文件做了同樣的事情，設置了一個後台任務定期掃描整個文件庫，找出那些過時的和實際程式碼對不上的文件，自動提交修復。

---

以上就是 OpenAI 所做的一些核心 Harness Engineering 實踐了。看完這些你可能有一個強烈的感覺——這哪裡是在寫程式碼啊，這完全就是在給 AI 構建幹活的環境啊。人負責定方向搭框架，具體幹活的事情就全由 AI 來做了。通過這五個月的瘋狂實驗，OpenAI 不僅跑通了這套 100 萬行程式碼的系統，更重要的是他們在這個過程中重新定義了人類和 AI 在未來的工作邊界。

OpenAI 在文章中拋出了一個非常關鍵的斷言：**Humans steer, Agents execute**（人類負責掌舵，Agent 負責幹活）。到了 Harness Engineering 這一步，人和 AI 的分工就徹底變了——人負責定方向、給上下文、制定規則、在關鍵的地方做判斷，而那些真正重複的、瑣碎的開發工作就交給 Agent 在 Harness 裡面跑就好了。

OpenAI 由此提出了第二個重要觀點：雖然人類不再需要親自手寫程式碼，但軟體工程的工作並沒有消失，而是演變成了完全不同的形態——如今軟體工程師的核心職責，變成了為 Agent 搭建穩定可靠的系統與支撐框架，以此來盡可能提高程式碼產出效率。Harness Engineering 不僅僅是如何寫好 Prompt 或者如何管理上下文這麼簡單，它是在重塑整個軟體工程的開發流程。

---

## Anthropic 的 Harness Engineering 實戰

Anthropic 有兩篇與 Harness Engineering 相關的文章。第一篇是去年 11 月發表的《Effective Harnesses for Long-Running Agents》，講述了如何配置環境以便讓 Agent 長時間自主運行。第二篇是今年 3 月份發表的《Harness Design for Long-Running Application Development》，可以理解為第一篇文章的續集，它在第一篇文章的基礎上對 Harness 架構做了進一步的優化和調整，使其能夠處理更多類型的任務。

這兩篇文章最核心的地方就兩點：一個是跟**任務規劃**有關，另外一個是跟**品質評估**有關。

### 任務規劃

在第一篇文章中，Anthropic 做了一個實驗，直接讓 Agent 執行一個任務——克隆 claude.ai（Claude 的聊天界面）。雖然看起來只是一個聊天界面，但它背後的功能還是挺多的，一口氣做出來幾乎是不可能的事情。

在 Anthropic 的實驗裡，Agent 接到需求之後立馬就開幹了，幹勁非常足，但效果也非常不好，主要是因為這個需求的工作量實在太大了。直接給到 Agent 的話，Agent 就會急於求成，從而引發一系列的問題，比如說他總想一口氣把所有的功能全部做完，結果幹到一半上下文就滿了，直接拋下了個爛攤子。等到下一個 Agent 接手的時候，完全不知道前面發生了什麼，只能靠猜，這一猜就壞事了——雖然有些功能只做了一半，但接手的 Agent 並不知道，粗略地掃了一眼還以為已經大功告成，於是直接宣佈完工草草收場了。

Anthropic 在第一篇文章裡面寫了對應的解法，他們引入了一個叫做 Initializer 的 Agent，用來初始化執行環境，比如說是拆解用戶需求、編寫啟動腳本、添加進度文件等等。這裡面最核心的就是拆解用戶需求這一點，具體來說就是把用戶的需求拆解為一個詳細的功能列表，後續負責幹活的 Agent 就可以直接拿著這個功能列表去幹活，而且這個幹活的 Agent 會一個功能點一個功能點地做，做完一個標記一個，這樣穩紮穩打，整個流程的可控性就高了很多。

後來在寫第二篇文章的時候，Anthropic 對這個思路做了一些演進，他們把 Initializer 裡面最核心的一件事情，也就是拆解用戶需求這個事情，單獨拿了出來做成了一個新的 Agent，叫做 **Planner**。他負責把用戶模糊的需求擴展成一份完整清晰的功能列表，這樣後面 Agent 在寫程式碼的時候，就不用對著用戶的需求猜了，照著功能點一個個做就行。

### 品質評估

一般來說，光是讓 Agent 生成程式碼是不夠的，我們還需要對它生成的程式碼做一些品質評估，看看產出的東西到底行不行。如果產出品質不行的話，我們需要把對應的問題列表發回給 Agent 以便讓他做相應的修改，這才是一個比較合理的流程。

這裡面有兩種評估方案。一種是人工評估，這個就不太行了，效率太低了。那這就引出了第二個方案——讓 Agent 自評，也就是自己評估自己的產出，有問題就修，修完再評，循環往復直到合格為止。聽起來挺合理的是吧？但 Anthropic 發現這個方案根本不好用，原因很簡單，Agent 自評這件事情本質上就是王婆賣瓜，他對自己做的東西天然就有濾鏡，所以即使產出裡面有明顯的 bug，他也能做到視而不見，給自己打個高分之後就草草收工了。

所以 Anthropic 直接把前面兩種方案都廢棄了，搞出了第三個方案，那就是做一個專門的評估 Agent 來評估產出品質。由於這個評估 Agent 是一個獨立的第三方，他自然就沒有理由去替別的 Agent 產出護短，評估結果也就客觀多了。而且把評估 Agent 單獨拎出來還有一個好處，那就是我們可以單獨去優化、去訓練這個評估 Agent，讓他的評估效果做到最好。

換句話說，我們最終需要把生成程式碼和品質評估這兩件事情給拆開，分別交給兩個不同的 Agent 來做：其中負責生成程式碼的那個叫做 **Generator**，負責品質評估的那個叫做 **Evaluator**。

### Planner + Generator + Evaluator 的協作流程

加上之前說過的 Planner，我們就有三個 Agent 了。這三個 Agent 的協作流程大致如下：

首先是 Planner，他會把用戶的需求拆解為具體的功能列表，然後發送給 Generator。Generator 接收到功能列表之後，會從中挑選出一個功能點，然後就著這個功能點去跟 Evaluator 討論交付標準，也就是討論到底做到什麼程度才算是完成了這個功能點。Generator 首先會把他的想法發過去，Evaluator 一開始可能會對這個提議提出一些修改意見，然後再發回給 Generator，Generator 會根據意見再次提交新的交付標準，這個過程會重複幾次，直到 Evaluator 確認 Generator 的提議沒問題為止。

確認好交付標準之後，Generator 便開始生成程式碼來實現這個功能點。實現完畢之後，Generator 會把他的實現結果提交給 Evaluator，Evaluator 會對結果做出評估反饋。如果不通過的話，Generator 就要修改程式碼，這個提交結果、評估反饋的過程也會重複幾次，直到 Evaluator 評估通過為止。到這裡一個功能點就算是開發完了，然後再重複這個流程，把後面的功能點全部都逐步做完。

Anthropic 把這個包含了三個 Agent 的方案叫做 **Full Harness 方案**，相比之下那種只靠一個 Generator 獨立完成所有需求的傳統單 Agent 模式，被 Anthropic 稱為 **Solo 方案**。

Anthropic 拿了一個具體的任務（做一個遊戲製作工具）來驗證這兩個方案的差距。從效果上來看，Solo 方案的問題很多，比如說佈局不合理、產品邏輯難以理解、bug 到處都是，基本上沒有辦法用。而 Full Harness 方案就有了明顯的改善，無論是佈局還是整體的產品邏輯，都達到了可用的水準。

當然這樣做也不是沒有代價的，Full Harness 方案的耗時和花費都要明顯高於 Solo 方案——Solo 方案耗時 20 分鐘、花費 9 美元，而 Full Harness 方案耗時 6 個小時、花費高達 200 美元。不得不承認，Full Harness 的效果確實好了不少，但精雕細琢是有代價的。

### 模型能力進化帶來的簡化

Anthropic 一開始在提示詞裡面強制 Generator 每次只選取一個功能點，做完這個功能點再做下一個，循環往復直到完成所有功能點為止。否則讓 Generator 自行發揮的話，它還是會急於求成，最後留下一堆爛攤子。

不過在 Opus 4.6 發佈之後，這個約束就不怎麼需要了。因為基於 Opus 4.6 做的 Generator 變得更強了，它可以一次把所有的功能點全部都拿過來，自己決定先做哪個再做哪個，穩步向前推進，不需要別人再對它的執行流程指指點點。在這種情況下，Evaluator 也直接評估最終產出就可以了，不需要再分功能點評估了。

---

## Harness Engineering 是不是噱頭

在這一章節裡，我們來聊聊目前爭議最大的問題：Harness Engineering 到底是不是一個噱頭？

### 這個詞是怎麼火起來的

首先，單就 Harness 這個詞來說，其實它並不算是一個全新的詞。在傳統的軟體測試領域就有一個概念叫做 Test Harness，它代表為了支持測試程式碼運行而做的一套框架。在 AI 領域，很多開發者其實也早就默默在用這個概念了，比如有個開源的項目叫做 lm-evaluation-harness，它就是為了支持模型效果評估而做的一套框架。Anthropic 去年 11 月發的那篇文章《Effective Harnesses for Long-Running Agents》裡的 Harness，也代表為了支持 Agent 長時間運行而做的一套框架。所以 Harness 這個概念一直都在那兒，大家也都在默默地用，誰也沒覺得這是個需要大吹特吹的新概念。

Harness Engineering 把這兩個詞組合在一起，目前比較公認的起點是 2 月 5 號 Mitchell Hashimoto 發表的那篇博客《My AI Adoption Journey》。他在裡面寫道，我也不知道業界有沒有公認的叫法，我就姑且管它叫 Harness Engineering，它的核心理念就是只要 Agent 犯了錯，你就去改造系統，讓它絕不再犯同樣的錯，要是有更好的詞，我隨時改口。

從傳播情況來看，這篇文章的討論熱度其實並不算很高。真正引爆這個概念的，是幾天後也就是 2 月 11 號 OpenAI 發的那篇 Harness Engineering 文章，這篇文章信息量極大，迅速在業界引起了巨大反響。緊接著，僅僅 6 天後也就是 2 月 17 號，軟體工程界大名鼎鼎的 Martin Fowler 網站就發了一篇文章，作者是 Thoughtworks 裡一位非常資深的工程師，文章標題叫《Harness Engineering - First Thoughts》，這篇文章一發出來自然就在圈內引發了廣泛的討論。

她在文章裡還點出了一個很耐人尋味的細節：雖然 OpenAI 這篇文章的標題有 Harness Engineering 這兩個詞，但如果你仔細去翻 OpenAI 的文章，你會發現這篇文章的正文裡其實只提了一次 Harness 這個詞。因此她推測 OpenAI 搞不好就是受了 Mitchell Hashimoto 的啟發，事後才臨時把 Harness Engineering 這個詞放到了標題裡面。

隨後到了 3 月 10 號，LangChain 發了一篇文章叫《The Anatomy of an Agent Harness》，這篇文章第一次明確給出了關於 Harness 的公式：Agent = Model + Harness，也就是我們前面聊過那個公式的變體，公式一出，概念就算定調了。隨後在 3 月 24 號，Anthropic 發了那篇 Harness 的文章，拿出了 Planner、Generator 和 Evaluator 的經典架構。雖然 Anthropic 自己比較克制，通篇只用了 Harness 這個名詞，並沒有生搬硬套 Harness Engineering 這個剛剛炒熱的新詞，但在當時那個氛圍下，整個 AI 圈心照不宣，直接就把這套三 Agent 架構當成了 Harness Engineering 的教科書級案例。就這樣，一傳十、十傳百，Harness Engineering 從一個人的私人說法，變成了大家都在用的詞。

### 爭議焦點

如果你複盤完這段歷史再仔細琢磨一下，就會發現一件非常微妙的事情：Harness Engineering 裡用到的所有技術，竟然沒有一個是新的。linter 程式碼檢查、任務拆解規劃、品質評估機制，這些東西其實早就有了。Harness Engineering 真正做的，只是把這些技術重新組織了下，統一放到了一個新詞下面。換句話說，它提供的是一套新的系統思維框架，而不是發明了一批顛覆性的新技術。

懷疑論者的攻擊點主要有兩個：第一，Harness Engineering 根本沒有新東西，全都是「新瓶裝舊酒」，在這種情況下特意造個新詞到處宣傳，可不就是噱頭嗎；第二，所有的 Harness Engineering 都遲早要被淘汰。他們認為，隨著大模型自身能力的持續進化，今天看起來必不可少的這些 Harness 設計，未來很可能會被模型能力本身逐步吸收，最終變得不再需要。

這種擔憂其實連 Anthropic 自己的文章裡都有跡可循。以**上下文焦慮**為例，這是 Sonnet 4.5 的一個問題——具體來說，就是當上下文過長時，模型會急於結束任務，以更少的 token 完成交付，而這往往會影響最終品質。Anthropic 一開始是使用了一種叫做上下文重置的 Harness Engineering 技術來解決這個問題，但後來當模型升級到更強的 Opus 4.5 後，這種現象被大幅緩解，也就不怎麼需要這方面的 Harness Engineering 設計了。再以**強制分步執行**為例，一開始 Anthropic 在提示詞裡強制 Generator 每次只選取一個功能點，等用到更強的 Opus 4.6 之後，這種強制分步執行的機制就不需要了，因為 Opus 4.6 的全局統籌能力夠強，它可以自己做好整體規劃，不需要別人對它的執行流程指指點點。

這恰恰印證了一個非常現實的趨勢：**模型越強，需要的 Harness 就越少。** 大模型自身的進化，正在一口一口吃掉 Harness Engineering 的生存空間。

### 個人觀點

我的觀點是，Harness Engineering 不是噱頭，但應該也不是終局。

說它不是噱頭，是因為它已經實實在在帶來了效果。無論是 OpenAI 還是 Anthropic，都通過 Harness Engineering 把 Agent 的穩定性、自動化程度和生產力往前推了一大步，這些都是可以被驗證的工程成果，而不是概念炒作。當然，也有人會說它不過是「新瓶裝舊酒」，用的都是老技術。但問題在於，工程領域真正的進步，往往不在於發明了什麼新技術，而在於有沒有一套統一的框架，把這些零散的能力組織起來，變成可以系統設計、可以持續優化的工程方法。Harness Engineering 的意義，恰恰就在這裡。

但我不得不承認，Harness Engineering 大概率不是終局。隨著模型能力繼續增強，今天這些用來約束模型、糾正模型、給模型兜底的系統設計，很可能會被模型自身逐步吸收。到那個時候，很多 Harness 可能會變得不再必要，這個詞也許會慢慢淡出大家的視野。

當然，Anthropic 官方在文章裡其實沒這麼悲觀。他們認為，隨著模型變強，Harness 的形態也會跟著進化，去解鎖更複雜的任務，也就是說 Harness 只會變形，不會消失。但不妨大膽推演一下——如果未來的模型真的強到離譜，也許只要給大模型配置上最基礎的 Harness，它自己就能把剩下 99% 的問題全搞定，到了那一天，Harness Engineering 就不再是一門需要大家專門去鑽研的技術了，它會退化成一個單純的環境接口、一個底層基礎設施。

所以我更願意把它看成一個**過渡期的關鍵技術**。它可能不是未來的終局答案，但它是當下最現實的答案。因為模型依然會犯錯，依然會幻覺，依然會在複雜任務中偏離軌道。在這種現實下，Harness Engineering 的重要性就不容忽視。可以說，誰能把 Harness 搭得更穩，誰就能更早把 AI 的能力轉化成真正的生產力，從而從中受益。
