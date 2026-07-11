---
title: 哪個 AI 最強？我全都要——讓 Claude 當大腦指揮 Gemini 與 Codex
description: Dustin 的多模型協作配置：Claude 當大腦中樞負責寫程式與長任務，Gemini 處理多模態與長文清洗，GPT/Codex 當備用大腦與生圖，並用 skill、agent、Codex Plugin 串接。
created: 2026-06-22
updated: 2026-06-22
source: https://www.youtube.com/watch?v=LlxyWJU2uDQ
published: 2026-06-19
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - codex
  - gemini
  - multi-model
---

## 核心觀念：模型選擇不該扁平化

社群常爭論「該選 ChatGPT/Codex、Claude、Gemini 還是接 DeepSeek」，但這問題不該被扁平化——不該認定只跟一家、其他都不碰。各家模型商競爭激烈，一家發新版另一家就迭代；Claude 也才剛過一歲，無法預知明年最強的是不是它。比較成熟的心態是**搭配使用**：不是換一個更強的 AI，而是讓對的任務交給對的工具。結語一句話總結這個取向：「小孩子才做選擇，我全都要。」

## Claude：大腦中樞

Dustin 把 Claude 當大腦指揮官，主要原因：

- **寫程式、長時間複雜任務、工具呼叫做得最好**，不會做一做就斷掉或卡關停下。
- 日常都用 Claude 互動、派任務，再由它去呼叫別家模型。

Claude 三個等級的分工：

- **Opus**：不確定的任務、複雜架構、需要智力邏輯推論時用；最聰明但額度消耗最多。額度沒燒完時就用 Opus 狂燒。
- **Sonnet**：步驟簡單、不太需要智力的日常任務（如套既有模板回信）；最適合日常，平常用起來沒太大阻礙。
- **Haiku**：只是上網查資料這類最省額度的任務。

切換策略跟方案有關：Dustin 用 100 美元方案，平常一直用 Sonnet 也不太會燒爆，所以沒特別切 Haiku；但若用 20 美元的 Pro 方案，切換要更精細才能達到最好的 CP 值。

### Claude 的短板：多模態

Claude 吃不了文字文件以外的 input。以下情境比較困難甚至做不到：

- 語音轉文字（轉錄）
- 聽音樂、辨識過門/旋律
- 讀影片、對影片做摘要、抓某一幕畫面

## Gemini：多模態之王與長文價效比之王

Dustin 曾一度嫌棄 Gemini（寫程式/工具呼叫不穩、常幻覺，修 A 壞 B、修 B 又壞 C），但後來接觸更多 use case 後發現它有四個其他家打不過的場景。他的提醒：聽到有人嫌某家模型，通常代表對方看到的 use case 不夠多。

四個關鍵 use case：

- **長文本與大量資料清洗的價效比之王**：幾十萬字摘要、改錯字、貼文情緒標籤、新聞關鍵字標記等，API 最便宜。來自中國的模型雖更便宜，但端點 Server 多在中國，個資隱私有疑慮時不是好選擇；最安全是自架開源模型但受硬體限制。權衡安全/方便/效能，**Gemini Flash Lite 是大量資料清洗的價效比之王**。
- **原生支援聲音與影片輸入**：能分辨同一段語音中多個講者是誰、辨識語氣、聽懂音樂旋律與過門（這 Claude 做不到、GPT 也做不好）。錄影片當下的 Gemini 3.5 Flash 語音轉摘要/逐字稿速度極快——30 分鐘語音約 30 秒開始產出、3 分鐘內轉錄完成且準確，勝過以往要試電腦效能的 Whisper。
- **影片內容理解**：可直接讀懂影片、回報「幾分幾秒是家人、幾分幾秒是路人、幾分幾秒是風景」，再用工具快速剪輯（例：把家族出遊影片中有家人的片段撈出來）。Claude 只能每 5~10 秒截一張圖辨識，耗 token 又不是一步到位。
- **影像辨識與 OCR**：辨識中文書（Claude 偏向只處理拉丁字母，中文常錯需事後修正）、辨識複圖並回傳小圖座標（之後可用程式把小圖摳出來）。還能讀產出檔案的排版，準確指出邊界溢位、孤行、文字疊合等需要修整的地方。

相比 Claude，Gemini 連續工具呼叫能力沒那麼好，但多模態與長文清洗是它的強項。

## GPT / Codex：備用大腦、第二意見、生圖最強

OpenAI 的 Agentic AI 終端工具叫 Codex，介面與 Claude Code 類似（Gemini 也有同類工具）。Dustin 用 Codex 的理由：

- **額度大方**：同樣訂閱方案下，OpenAI 給的額度比 Claude 大方、可用比較久（屬政策面，未來可能反轉）。
- **長任務處理**：GPT-5.5 目前與 Claude Opus 不相上下，可信任跑長任務不斷掉。
- **備用大腦**：Claude 額度用爆或伺服器 shut down 時，馬上轉 Codex 繼續工作不停擺。
- **救援與評審**：有些 Claude 解不掉的問題，GPT 反而解得掉；也可當評審，用不同模型角度審查，避免球員兼裁判。
- **生圖最強**：截至 2026 年中，GPT 的 Image 2 是生圖最強、斷崖式領先；Claude 沒有生圖模型，Gemini 的 Nano Banana 仍有不小差距。需要生圖時就用 GPT。

### 為什麼仍用 Claude 當主力、Codex 當備用

純個人原因：一是先用慣了 Claude Code；二是 **Harness（規則與環境）都養在 Claude Code**——`CLAUDE.md`、rules、hooks 都在這裡。同樣厲害的模型，配上熟悉且調好的環境跑起來最順。

## 怎麼讓主力模型呼叫別家

讓 Claude 主力自動派任務給別家，不用一直手動切換，靠 skill、agent 與插件：

- **skill / agent**：skill 是技能、agent 是常態角色，都能指定模型做特定任務。
- **Codex Plugin**：OpenAI 官方 GitHub 上的 `Codex Plugin` 專案。把網址丟給 Claude Code 安裝後，輸入 `/codex` 會出現一連串指令，例如：邀請 Codex（GPT 模型）審查目前程式碼/內容、卡關時請 Codex 救場、對抗式（毒舌）審查。Dustin 還依這些 prompt 請 Claude 自製了 `Codex image` 指令，直接邀 Codex 進來做圖。
- **Gemini 接法**：可請 Claude 找能在 Claude Code 內呼叫 Gemini 的 plugin；Dustin 自己則把 Gemini 做成 **agent**——
  - 一個專用 agent：用 Gemini API 做語音轉文字，傳檔方式、檔案過大怎麼處理、預設模型都寫在 agent 檔裡。把 Email 送進去說「用 Gemini 轉錄逐字稿」就會自動派出該 agent。
  - 一個通用 Gemini agent：呼叫電腦裡安裝的 Gemini CLI，依任務分配不同智力等級的模型。例如 200 多頁 PDF 不讓較貴的 Claude 讀，而是「用 Gemini agent 幫我讀並摘要」——agent 判斷只是單純摘要就用 Flash（不用較貴的 Pro），摘要完把結果回傳給 Claude 整合。

整體工作流：主要對話都不離開 Claude，只是幫 Claude 裝好 Codex 工具、Plugin、Gemini 工具與 Gemini agent，它就會自動把任務分配給最適合的模型，拿到結果後再接著做下一步。

## 實戰範例：用 Codex 生 IG 分享圖卡

Dustin 示範把 Reddit 上 24 小時內的 AI 熱點內容整理後做成 Instagram 圖卡分享。Claude 只能做類似 HTML 網頁風格的圖片，無法像 GPT 生圖模型那樣產出客製化精美圖卡，於是用自製的 `Codex image` 指令，後面接「用日式簡約風格為以上摘要產出 Instagram 分享圖卡」。Claude 會直接呼叫 Codex 工具（事先登入、吃自己的訂閱額度），過程中回報 Codex 進度，最後把圖片放到指定位置（成果風格可再請它調整）。
