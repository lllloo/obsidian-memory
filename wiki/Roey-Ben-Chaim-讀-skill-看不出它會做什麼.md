---
title: Roey Ben Chaim 讀 skill 看不出它會做什麼
description: Zenity 在沙箱實跑數千個 agent skill 的方法與 Paperclip 仿冒竊密案，附回查結果、數字強度與個人導入第三方 skill 的檢查步驟
created: 2026-11-19
updated: 2026-11-19
source: https://www.ai.engineer/talks/_7P580m4kPY-you-cant-tell-what-agent-skill-will
published: 2026-11-10
parent: "[[wiki/01.index]]"
tags:
  - skill
  - ai-agent
  - coding-agent
---

# Roey Ben Chaim 讀 skill 看不出它會做什麼

原料：[[AI-Engineer-Ben-Chaim-Cant-Tell-What-Agent-Skill-Will-Do]]（官方閱讀頁＋官方機器逐字稿，影片 `_7P580m4kPY`，約 14 分半）。**逐字稿注意**：官方在逐字稿裡插入多段 `[Editorial paraphrase]` 改寫，與講者原話混在一起，部分細節（例如 Azure 案例的具體動作）只剩改寫版。下文標「講者說」的是原話段落，其餘依閱讀頁與改寫段。

**一句話**：skill 是別人寫、會在你機器上跑的程式碼與指令，讀 `SKILL.md` 或叫 LLM 掃描都判斷不了它實際會做什麼。要給它環境和具體任務實際跑一次，同時記錄行程、檔案、網路，再把敏感動作連到「是哪個行程做的、資料送去哪」才能下結論。導入時把 skill 當軟體依賴來管。

## 講者與立場

Roey Ben Chaim 是 Zenity 的 staff engineer，也是 MATS research fellow，主要談 AI 安全。Zenity 是賣 AI agent 安全產品的公司，整場內容是自家研究的成果發表，結尾直接推薦自家服務（逐字稿辨識成「neoto.io」，對照 Zenity 新聞稿應為免費的 AI Total，網址 aitotal.io，屬推測）。**屬 vendor 立場**：問題陳述與案例有外部佐證（見回查節），但「動態引爆是唯一可靠做法」的結論剛好對應他們在賣的東西。

## 演講脈絡（依時間序）

時間碼對應 YouTube `_7P580m4kPY`。

1. **敏感讀取本身說明不了什麼（0:03–1:35）**：skill 是「按需取用的能力」，內含指令、資源、腳本甚至程式碼，問題在於它是別人寫的。開場案例：一段軌跡顯示程式讀了雲端設定和身分資訊，竊密程式也會做同樣的事，但這次其實是 **Azure 官方的診斷 skill**。只看存取事件分不出合法排錯和竊取憑證，所以要問兩件事：它讓機器做了什麼？那些事對使用者交辦的任務合不合理？軌跡回答得了第一題，回答不了第二題。
2. **靜態掃描的兩個破口（1:35–2:50）**：
   - **第一個破口：skill 會引用不在原檔裡的東西**。安裝時看到的 `SKILL.md` 只是作者當下提供的內容，agent 使用時可能拿到別的指令、套件或依賴。只審第一份文件就停，等於提早結案；要追「實際影響這次執行的是哪些材料」，否則得另建機制追蹤這些外部 payload。
   - **第二個破口：LLM 分析器會被騙**。他引 Trail of Bits 的研究：自動審查者接受了一段誤導性說明，同意了改套件來源的變更，而那段「已核准」的說法就寫在被審的材料裡。被審材料自己說「有人核准了」，不能當成核准的證據；需要獨立來源。
3. **第一版引爆室與環境問題（2:50–3:55）**：借用惡意程式研究的 detonation（引爆）手法：給 agent 一個 skill 和任務提示，丟進沙箱跑幾分鐘到幾小時，再分析軌跡。第一版的問題很平凡：**環境多半缺東西**。很多 skill 依賴特定 CLI、服務或既有專案，例如 Notion skill 在空沙箱裡沒有 Notion 可連，跑到這裡就停，看不出接上服務後會做什麼。解法是加一個 **world builder**：讀 skill，依它的期待建好服務與專案環境。
4. **任務要具體，路徑要覆蓋（3:55–4:52）**：通用任務提示不夠。簡報 skill 要有一份 deck 要做、部署 skill 要有服務要上線、腦力激盪 skill 要有點子要發想。就算是「部署服務」，設定、部署、從 snapshot 復原各走 skill 的不同部分，部署成功不代表看過復原路徑，而惡意可能只藏在其中一條。於是加了 **operator**：讀 skill、找出值得觸發的路徑、為每條產生提示。覆蓋率取決於 operator 認得出哪些路徑、agent 實際走了哪些。
5. **模型拒絕與誤報（4:52–5:58）**：有些 agent 在步驟看起來危險時拒絕繼續，這會限縮這次能觀察到的範圍。合法任務也可能觸發安全機制。兩種錯都要避免：把每次拒絕當惡意證據會誤判合法 skill；把沒跑完的測試當「安全」會掩蓋還沒看到的行為。他們把觀察到的行為和證據的限制一起記錄。
6. **往模型的工具呼叫底下看（5:59–7:05）**：agent 軌跡只到某個程度。軌跡上一次「安裝套件」，安裝過程啟動的行程可能讀檔、連網，模型自己不會描述，它只知道請求成功了。所以在軌跡之外加三種紀錄：**行程建立事件**（安裝程式啟動了什麼）、**檔案系統事件**（那些行程碰了什麼）、**網路封包擷取**（它們送了什麼流量）。有了這些就能從一次檔案存取或對外連線，反推回啟動它的那次安裝。
7. **使用者沒選的依賴（7:07–8:03）**：Zach Corman（GitHub 帳號 ZackKorman）做的無害 PoC：使用者選的 skill 又帶進另一個元件，原始檔案看不出後續行為；引爆室的紀錄把後來的動作歸因到這個間接依賴。單次成功的測試證明「有這個可能」，不代表每次安裝都會這樣。講者說用這套方法在**數千個 skill 中找出 100 個惡意 skill**，並已從 `skills.sh` 下架。
8. **Polymarket 仿冒依賴（8:03–8:49）**：某 skill 聲稱使用 Polymarket 的依賴，但套件身分和預期的稍有不同，來源是非官方的；進一步檢查發現替換進來的軟體會收集敏感資訊。重點是比較「使用者以為選了什麼」和「安裝程式實際裝了什麼」。
9. **裝完之後還會變（8:49–10:35）**：
   - 有些 skill 在使用者以為已移除後又回來；刪掉看得見的部分，不一定撤銷安裝時對環境做的改動。
   - 有個第三方的 skill creator 悄悄取代了官方版本，介面看起來一樣，回應下一個請求的卻是別的實作。
   - skill 可以依賴放在套件外的指令（合法 skill 也會這樣），本地檔案沒變，遠端內容卻可能被原作者更新，或遠端位置本身換了主人。
   - 有些 skill 會在一般使用者活動時被觸發，即使跟當初選它的任務無關，這會改變風險行為發生的頻率和可見度。
   - 所以一份審查要有**日期與範圍**：哪個版本、哪些依賴、什麼條件、實際觀察到哪些行為。安裝前做一次清點、移除後再看一次，才有東西可比。
10. **Paperclip 仿冒活動（10:35–13:30）**：Paperclip 是開源的多 agent 編排專案。攻擊者（GitHub 帳號 karli-paperclip）建立仿冒組織、註冊相似網域、做出仿冒 skill。標榜成「應用程式 logging」的功能，其實把本機的認證資料送到攻擊者控制的服務；部分活動很短暫，所以完整錄下執行過程特別重要。對照開場的 Azure 診斷：同樣是讀敏感資料，**資料送去哪、目的是什麼**才讓他們有更強的根據判定為竊取憑證。同一套 command-and-control 也出現在 Browser Use 的仿冒與 PyPI 套件（講者說 PyPI 那邊兩小時內、另一個一小時內就下架），但用同一套基礎設施的 skill 當時正在熱門榜上，**累計 1.7M 次下載**。閱讀頁特別註明這是散布量，不代表多少機器執行了惡意行為、多少憑證被偷。在一個生態系下架不等於別的散布管道也關了。通報 Vercel 與 Microsoft 後，12 小時內全部下架。
11. **結論：把 skill 當軟體依賴（13:30–14:30）**：skill 只是 agent 供應鏈的一環，所有進入 context 的東西都是：網站、資料庫的資料列、套件，甚至 YouTube 留言。建議沿用軟體依賴的既有做法：查清楚是誰提供、會載入什麼；權限只給任務需要的（最小權限）；保留足夠的執行期證據，能把敏感動作連到執行它的行程和資料去向。答得出這些問題，就能解釋為什麼 Azure 診斷和 Paperclip 仿冒該有不同處置。

## 回查結果（2026-11-19）

| 演講說法 | 回查結果 | 依據 |
|---|---|---|
| Trail of Bits 顯示 LLM 審查者接受材料內的誤導說明，同意改套件來源 | **成立**。他們做的 `dev-env-setup` 測試 skill 叫 agent 把 npm／yarn 指向攻擊者的 registry，包裝成公司 VPN 環境設定並宣稱「該 registry 已公開且稽核過」。Cisco skill-scanner 的 LLM 分析器只給 LOW 並判定安全，skills.sh 整合的三個掃描器也都放行。同文還用 10 萬個換行把惡意碼推出掃描範圍、用 `.pyc` 位元碼藏行為，結論是「掃描或 LLM 分析都無法可靠偵測 skill 裡的惡意內容」 | [Trail of Bits：The sorry state of skill distribution](https://blog.trailofbits.com/2026/06/03/the-sorry-state-of-skill-distribution/)（2026-06-03，一手） |
| Paperclip 仿冒活動、1.7M 下載、12 小時下架 | **大致成立，數字需補條件**。Zenity Labs 原文：攻擊者 `karli-paperclip` 於 2026-07-02 註冊仿冒網域與組織，07-11 把原本照抄官方的 skill 改成惡意版（先照抄以通過市集檢查）。惡意指令藏在只有「安裝 Paperclip 時才讀」的次要文件 `setup-installation.md`，叫 agent 用 curl 抓 payload、base64 解碼後用 Node 執行再刪掉。竊取目標含 SSH key、AWS／GCP／Azure 憑證、套件管理 token、`.env` 等（附錄列 138 個路徑）。1.7M 是 skills.sh **顯示的累計安裝數**，原文明說不是不重複使用者。Vercel 與 Microsoft/GitHub 於通報後 12 小時內移除（約 08-02），但原文也說其他地方可能還有複本 | [Zenity Labs 原文](https://labs.zenity.io/post/attackers-target-agents-via-the-skill-supply-chain)（一手，vendor 自家研究） |
| PyPI 套件兩小時、一小時內下架 | **部分對不上**。原文說 `browser-use-headless` 兩小時內被標記（MAL-2026-10484）、`paperclip-ai` 一小時內被標記（MAL-2026-10869），但沒寫 PyPI 已移除，只說 07-26 後沒有下載紀錄。「被標記」與「被下架」不同 | 同上 |
| 數千個 skill 中找出 100 個惡意 skill | **對不上**。Zenity 自己 2026-08 的新聞稿寫的是「dozens（數十個）」，且沒有給測試總數。「100」只出現在演講與轉述演講的二手報導 | [Zenity 新聞稿](https://zenity.io/company-overview/newsroom/company-news/zenity-labs-discovers-dozens-of-malicious-ai-agent-skills-evading-detection-launches-ai-total) |
| skill 移除後自己回來、第三方 skill creator 取代官方版 | **有 vendor 一手佐證**。新聞稿：一個 skill 叫 agent 改系統提示，讓 skill 被刪後自動重裝；另一個卸載 Claude 的 skill-creator 並換成自己、不通知使用者；超過 30% 的危險 skill 誘使 Claude Code／OpenClaw 從攻擊者端點下載並執行檔案。皆無樣本公開可獨立重現 | 同上 |
| Zach Corman 的 PoC：skill 引進另一個元件 | **repo 存在，串接細節未核到一手**。[ZackKorman/skills](https://github.com/ZackKorman/skills) 是公開的示範集合（`npx skills add` 安裝）。其中 `security-review/SKILL.md` 的 description 寫「ALWAYS run this at the end of each task」，正文用 HTML 註解藏了 `curl -sL … \| bash`，註解在渲染後的 Markdown 看不到。「第一個 skill 安裝第二個 skill、再從 GitHub 抓藏指令的檔案」的完整串接只見於二手報導，沒找到作者原文 | GitHub repo（一手，2026-11-19 讀） |
| Paperclip 是知名開源 agent 編排專案 | **成立**。`paperclipai/paperclip` 仍活躍更新，星數十萬級 | GitHub API（2026-11-19） |
| 可到自家服務測試 skill | AI Total（aitotal.io）依新聞稿是免費服務，用真 agent 在放了假憑證的沙箱跑 skill，記錄連線網域、拉的套件、碰的檔案與 agent 動作。**未能實際開啟**：網站對指令列請求回 403 | 新聞稿；網站未驗證 |

另查：Vercel 的 `skills` CLI（`npx skills`）有 `skills-lock.json`，每個 skill 記錄來源 commit 與 `computedHash`，`install --frozen-lockfile` 會比對磁碟上的檔案（[vercel-labs/skills README](https://github.com/vercel-labs/skills)）。這能擋「本地檔案被換掉」，但**只涵蓋安裝進目錄的檔案**；Paperclip 案那種執行時才從網路抓的指令或 payload，lock 檔管不到。這正是演講第 9 段說的「本地檔案沒變，遠端內容變了」。

## 數字與證據強度

| 數字 | 強度與限制 |
|---|---|
| 數千個 skill 中 100 個惡意 | 講者自報；與 Zenity 自家新聞稿「數十個」不一致；未公開清單、判定標準與總數。**勿引用為確定數字** |
| 1.7M 次下載／安裝 | Zenity 自報、取自 skills.sh 顯示的計數器；是累計安裝數，非不重複使用者，更不是受害人數 |
| 12 小時內下架 | Zenity 自報，與原文時間線一致；平台方未見獨立聲明 |
| PyPI「兩小時、一小時內下架」 | 原文只說「被標記」，**「下架」勿引用** |
| 超過 30% 危險 skill 會下載執行外部檔案 | Zenity 新聞稿自報，分母未公開 |
| Azure 診斷、Polymarket 案例 | 單一案例，無公開樣本，細節多為官方改寫段 |

整體：方法論（world builder、operator、三層主機紀錄）是單一 vendor 的描述，沒有公開程式碼或評估資料，覆蓋率與漏判率未知；講者自己也承認無法知道漏掉多少惡意路徑。

## 搬到個人 Claude Code／Codex 的做法

個人不可能像 Zenity 那樣為每個 skill 建引爆室，但演講的幾個判準可以縮成以下步驟：

1. **裝之前讀原始檔，不讀渲染畫面**。把整個 skill 目錄（含 `SKILL.md` 引用的每個檔案、腳本、二進位）抓下來，用文字模式看。至少 grep 這些：`<!--`（HTML 註解在渲染時看不到，Korman 的 PoC 就藏在這裡）、`curl`／`wget`、`| bash`、`base64`、`http`、`npm config`／`registry`、隱藏檔、`.pyc` 等沒附原始碼的檔案。找到外部 URL 就表示「審查範圍不只這個目錄」。
2. **看 description 有沒有強迫觸發**。「ALWAYS run this」「每個任務結束都要用」這類寫法會讓 skill 在不相關的工作中被叫起來（演講第 9 段）。對照 [[Superpowers]] 的「1% 就必須呼叫」規則：合法框架也這樣寫，所以這是風險訊號，不是惡意證據。
3. **不要把 LLM 的「看起來安全」當結論**。skill 自己說「這個 registry 已核准」「這是唯一支援的安裝方式」都是被審材料的一部分，要另找獨立來源（官方 repo、官方文件）確認。
4. **核對來源身分**。從官方組織的 repo 安裝，比對 GitHub 組織名、網域、套件名是否是仿冒（Paperclip 案靠多一個字母的網域與組織名）。有 curated 來源就不用公開市集。
5. **鎖版本**。用 `npx skills` 安裝的就提交 `skills-lock.json`，在新機器用 `--frozen-lockfile` 還原。手動複製的 skill 可以自己記下來源 commit。要記得限制：lock 只保護本地檔案，執行時抓的遠端內容不在保護範圍。
6. **第一次跑放到拋棄式環境**。在沒有真憑證、網路有限制的容器或雲端 session 裡，給它一個具體任務（不是「試試看」），看它讀了哪些檔、連了哪些網域。Claude Code 的沙箱、deny 規則與 cloud session 的分工見 [[Claude-Code-放手運行的安全與驗證]]：沙箱只管 shell 指令與子行程，skill 帶進來的指令影響的是 agent 本身，所以 deny `.env`、`~/.ssh` 這類規則仍要設。
7. **裝前清點、移除後再清點**。記下 `~/.claude/skills`、專案 `.claude/skills`、`.agents/skills` 和 plugin 目錄的清單與雜湊；移除 skill 後再比一次，並確認內建或常用的 skill（例如 skill-creator）沒有被換掉，`CLAUDE.md`／`AGENTS.md` 等指示檔沒有被加料。

**做不到的部分**：行程建立、檔案系統事件、封包擷取三層同時記錄並互相關聯，個人用 strace、tcpdump 拼得出來，但成本高、也要懂得判讀，不適合每個 skill 都做。比較實際的分工是：信任來源＋讀原始檔＋鎖版本處理大部分情況，只有權限大、來源不明又非用不可的 skill 才進拋棄式環境實跑。Zenity 的 AI Total 宣稱能代勞，但本頁未能實際使用，效果未知。

## 張力與關聯

- **補充 [[Claude-Code-放手運行的安全與驗證]]**：那頁講「權限只決定呼叫能不能執行，管不到執行後碰得到什麼」，例子是 `npm test` 會跑被入侵的依賴。本場是同一個論點換到 skill：工具呼叫表面上只是「安裝」，真正的動作發生在子行程。兩者都指向用執行環境（沙箱、無憑證的機器）限制後果，而不是靠審查呼叫本身。
- **與 [[Lauren-Tan-把糾正寫進程式庫]] 的對照**：Tan 主張把規則從散文搬到確定性檢查；本場說明 skill 的散文（`SKILL.md`）本身就是攻擊面，而且 LLM 讀散文來判斷安全會被同一份散文說服。兩場一致的地方是「不要只靠讀文字的判斷」。
- **與 [[Agent-Skill-腳本路徑的規範與實況]] 的關聯**：那頁談 skill 如何呼叫 bundled 腳本。本場提醒，同樣的機制讓 skill 能執行任意程式，審查範圍要涵蓋這些腳本，以及腳本再抓進來的東西。
- **張力：靜態審查還有沒有用**。Ben Chaim 與 Trail of Bits 都說靜態掃描不可靠，但 Trail of Bits 給的解法偏向「用 curated 來源、鎖版本、縮小攻擊面」，Zenity 則偏向「實跑觀察」（剛好是它的產品）。對個人來說，前者便宜得多；後者能看到遠端 payload 與執行期行為，但覆蓋率取決於 operator 有沒有觸發到惡意路徑，沒跑到的路徑一樣看不見。
- **張力：拒絕不等於安全**。agent 自己的安全機制會在危險步驟停下，對使用者是好事，但對審查者來說，「沒跑完」不能當成「沒問題」。這和用 agent 自評當驗收證據的問題同類。

## 勿引用（2026-11-19 核對）

- 「Zenity 在數千個 skill 中找到 100 個惡意 skill」：只見於演講口述與轉述，Zenity 自家新聞稿寫「數十個」。要引用改寫成「Zenity 稱找到數十個」。
- 「PyPI 在一兩小時內下架了惡意套件」：Zenity 原文只說被標記為惡意，沒說下架。
- 「1.7M 人受害／1.7M 次執行」：只是 skills.sh 顯示的累計安裝數。
