---
name: vault-page-score
description: 用 LLM-as-judge 依 rubric 為 wiki 頁面評分,五個語意面向各給三檔並附頁內原文佐證,用來排序「該優先補哪幾頁」。唯讀、不寫任何檔案、不做總分;一頁一個獨立 subagent,絕不一次丟多頁讓模型排序。**rubric 尚未通過信度驗證,結果只能當參考、不可當品質 gate**。使用時機:使用者要求「幫 wiki 頁打分」「評一下這幾頁品質」「哪幾頁該補」「跑一下頁面評分」,或直接呼叫 /vault-page-score。
---

# Vault Page Score

依 rubric 為 wiki 頁面評分，產出「哪幾頁該優先補」的排序參考。

**唯讀，不寫任何檔案**——不寫 wiki、不寫 `schema/`、不寫 `feeds/`、不產報告檔。評分結果只回到對話，由呼叫端自行消化。理由：rubric 尚未通過信度驗證，任何落地都是讓未驗證的分數獲得不該有的權威。

## 定位與已知限制（每次跑都要記得）

這個 skill 建立在 `wiki/LLM-as-judge-知識庫頁面評分.md` 的查證結論上，其中三條直接約束本流程：

1. **rubric 必須明文寫出**——無 rubric 的 judge 會**看起來很穩定卻穩定地量錯東西**（自我一致性不受影響、與人類判準的相關卻大幅劣化）。所以分數重跑幾次都一致**不構成可信的證據**。
2. **絕不一次丟多頁讓模型排序**——多候選評分時過半判決會因候選順序翻轉。本流程一頁一個獨立 subagent，互不見面。
3. **只評機械層測不到的語意殘差**——`vault-lint` 已確定性地測過死連結、孤立頁、frontmatter；重複測只會稀釋分數。

**judge 與撰寫者同模型**（subagent，乾淨 context）。這是刻意的取捨：self-preference bias 的機制在權重而非 context，乾淨 context 擋不住；但本 vault 22 頁全部由同一模型維護，偏誤若均勻分布則對**排序**不生影響。**殘餘風險有明確方向**——熟悉度逐頁不同，模型可能給「自己寫得順的頁」偏高、給「引文與數字密集的頁」偏低，而後者在本 vault 正是好頁。校準方式見下方「驗證」。

## 主流程

1. 用 harness-native `Read schema/vault-map.md` 確認 cwd 是 vault root；讀不到就停止，請使用者 cd 到 vault root（`~/code/obsidian-memory`；cmd.exe 用 `%USERPROFILE%\code\obsidian-memory`）。
2. 決定要評哪些頁。使用者指定就用指定的；未指定則問清楚，**不要預設全掃 22 頁**——這個 skill 的用途是回答具體問題，不是例行普查。
3. `Read .agents/skills/vault-page-score/references/rubric.md` 取得評分 prompt 全文。
4. `Read` 每一頁目標頁全文。
5. **每頁各派一個 subagent**：`Agent` + `subagent_type: "general-purpose"`，prompt = **rubric.md 全文 + 該頁全文**（不要叫 subagent 自己 Read rubric）。多頁時在同一則訊息內平行送出。
   - **一個 subagent 只評一頁。** 不要把多頁塞進同一個 subagent，那正是第 2 條約束禁止的形狀。
6. 彙整回對話：每頁五面向檔次一覽 + 各頁最該補的一項（附 subagent 引用的原文）。**不做總分、不做跨頁加權排名**；要指出優先順序就依「0 檔數量」與具體嚴重程度說明，並講清楚那是判斷不是計算。
7. 明講本輪的限制：judge 與撰寫者同模型、rubric 未經信度驗證。**不要把分數表述成客觀量測。**

**fallback**：環境無 `Agent` 工具時，主 agent 直接 `Read references/rubric.md` 並逐頁自行套用同一份 rubric，流程與紀律完全相同（仍須一頁一頁獨立評、附原文證據、不做總分）。

## 驗證（手動跑，skill 不內建）

rubric 在通過下列驗證前**只能當參考，不可當品質 gate**。三階各有中止條件，沒過就別往下走：

- **階段 0 — 分辨力**：手挑 3 頁（1 頁明顯好、1 頁明顯弱、1 頁中間），各跑一次。若三頁檔次沒拉開 → rubric 太模糊，改寫或放棄。
- **階段 1 — test-retest**：同 3 頁各重跑 3 次。若同一頁同一面向跨次跳超過一檔 → 無可用信度，**放棄；不要靠「多跑幾次取平均」搶救**（該救法在原查證中未通過驗證，無依據）。
- **階段 2 — 跨家族校準**：用另一個模型家族評同一批頁，比對**排序**是否一致（不是分數是否相等）。本 vault 已有經端到端驗證的唯讀 headless 呼叫模式可沿用：

  ```
  codex exec -s read-only -C <vault-root> --skip-git-repo-check -o <outfile> <prompt>
  ```

  prompt 用同一份 rubric.md 全文 + 頁面全文。**要看的具體問題是：同模型 judge 有沒有把引文／數字密集的頁排低？** 差異集中在證據密集頁 = 上述殘餘偏誤成立，該改用跨家族 judge；差異隨機分布 = 同模型 subagent 夠用。
  （注意：`codex` 與 `opencode` 共用同一 ChatGPT oauth，背靠背呼叫會互相輪替作廢 refresh token；一次只用一個。）

**放棄條件也寫在前面**，免得沉沒成本推著走：全跑完但結果與你自己的直覺高度一致 → 也該放棄，那代表它沒告訴你新東西，只是花錢確認已知。結果與直覺分歧才是有價值的情況，逐頁人工核對分歧點。

驗證結論（無論通過與否）值得記進 `wiki/LLM-as-judge-知識庫頁面評分.md`——那頁明列這是文獻答不了、只能自己量的問題。
