---
title: Fleet Engineering 是瘋狂進化：Vibe Coding 的下一步
description: 拆解多個 Claude Code session 平行運作的碰撞問題，並用 handoff skill、agent dashboard、Git worktree、Symphony 與 Docker Sandbox 逐層隔離。
created: 2026-07-21
updated: 2026-07-21
source: https://www.youtube.com/watch?v=qxjII6x2yPY
published: 2026-07-20
parent: "[[01.index]]"
tags:
  - youtube
  - claude-code
  - workflow
  - sub-agent
  - automation
---

## 平行 session 的核心問題

AI Labs 團隊從不只跑單一 Claude Code session：一個 session 在做事時，人就去 review 另一個剛交回的成果並派下一件工作，讓自己的時間不被單一 agent 卡住。但一旦真的平行跑，問題不會浮在表面——每個 session 看起來都很忙、輸出讀起來也正常，實際上底下彼此干擾，等你發現時東西已經壞了。

一般性的困擾：

- 分不清目前在哪個 session、每個 session 到底在做什麼
- session 一多就跟不上各自的產出
- 想回到某個含重要 context 的 session，卻忘了它在哪
- 開太多 session 後，忘記某個 session 當初是為什麼開的

結構性的困擾在於 **session 之間不共享即時 context**，各有各的記憶：

- 若 context 與設定都放在全域 `CLAUDE.md`（Claude 讀來理解專案的主要指示檔）或其他被某個 session 持續更新的檔案，其他 session 不會知道那份 context 變了，也不會自行重讀全域檔，只會繼續用過時資訊
- 每個 session 只在啟動時讀全域檔，之後要重讀必須手動要求
- 若需要編輯同一批檔案，會互相覆蓋彼此的改動

## 基本功：session 的續接與交接

這些指令看似基礎，但日常使用對產能與模型輸出品質差異很大：

- `claude --continue`：接回這台機器上最後一個 session
- `claude --resume`：從清單挑一個 session 續接；後面直接接 session 名稱可以一步跳回那個 session 並帶著全部 context
- `recap` 指令：回到 session 後忘了它在做什麼，跑這個拿到一份該 session 工作內容的快速摘要
- `export` 指令：把整段對話輸出成 text 或 markdown 檔，丟進新 session 就能接續舊 session 的進度

影片中的實例：他們的影片動畫由內部動畫系統加 Claude Code 產出，要改動畫時就 resume 當初建置的那個 session（若已關閉則 continue）；隔太久想不起來時用 recap 補回脈絡。

## 檔案所有權與平行規劃

多個 session 動到同一份共享檔案時，**在開工當下就決定檔案所有權**：指定一個 session 擁有某檔案，只有它能改；其餘 session 可讀、可當參考，但不得寫入。做法就是在每個 session 的 prompt 裡直接告訴它不要寫哪些檔案。

若是從零建置、且各部分彼此獨立的專案，團隊的流程是先用 **plan mode** 規劃：把手上關於任務的所有資訊給 agent，要它拆成各 session 可平行執行、共同指向同一個終點的獨立任務。這個規劃與拆分階段很關鍵——它讓各 session 幾乎不會搶檔案或互相覆蓋，也確保每個 session 拿到完成任務所需的同一份共享 context。

## handoff skill 與 agent dashboard

規劃完成後，把每個獨立任務交給不同 session，交接用 **handoff skill**。

handoff 是 `export` 的聰明版本：`export` 只是把整段對話倒進檔案，新 session 會繼承那堆雜亂又拖慢速度的 context；handoff 則把內容壓縮成一份乾淨的交接文件，**以指向既有檔案的方式取代把檔案內容複製進去**，讓新 session 從乾淨且聚焦的狀態開始。該文件包含必要資訊、與該 context 相關檔案的參照，甚至列出 agent 該安裝哪些 skill 才能把任務做好。

用法是先安裝 skill，再於 session 中以 `handoff` 關鍵字呼叫。規劃完成後，請規劃用的那個 session 用 handoff skill 為每個任務各產一份交接文件，每份都回指它產出的 plan 檔。

實際派工用 **Claude agent dashboard**——終端機內的互動介面，可看到目前所有在背景執行的 session、在其間切換、打開任一個看它在做什麼：

- `claude agents` 開啟 dashboard，會列出已完成或仍在執行的 session；也可以直接在裡面輸入 prompt，它會為此啟動一個背景 Claude Code session
- 另一種啟動背景 session 的方式是 `claude` 加 background flag 再接 prompt
- 已經在某個 session 裡、想讓它轉背景繼續跑，用 `bg` 指令（background 的縮寫），終端機隨即釋出

## 開發專屬的問題

一旦是真的在寫軟體，前述問題之上還會多一層：

- 多個 session 在同一專案編輯相同檔案，因為不知道彼此在做什麼而互相覆蓋
- 有遠端 GitHub repo 時，session 們會在推程式碼與切換 branch 時打架：一個推到某 branch、另一個切到別的 branch，很快就把 branch 與整個 repo 搞亂
- 多個 localhost server 會互相殘殺，因為全都想佔用 localhost 3000
- 所有 session 共用同一份專案相依：只要一個 session 換掉某個相依套件、改變 app 的建置方式或動到資料庫，其他 session 就會壞掉，且完全不知道發生過這個改動

## Git worktree

Git worktree 是 Git 內建功能，讓你在同一份本機專案上同時處理多個 branch，每個 branch 各有自己的資料夾。不必為了換 branch 而整份 clone，也不用來回切換。

用法可以直接請 Claude Code 幫你建 worktree，然後在該 worktree 內實驗。跑多個 session 時，各自在獨立 worktree 工作，就不會因編輯同一檔案而互相覆蓋，也不會在 branch 上衝突——每個 session 都有自己的隔離副本。

## OpenAI Symphony 與 Claude Code 分支版

worktree 解掉程式碼衝突，但派工仍得靠人手動。**OpenAI Symphony** 把這段自動化：它是開源的 orchestrator（管理一批同時工作的 coding agent 的系統），原本為 OpenAI 自家的 Codex agent 而建。

核心構想是**讓待辦清單成為追蹤一切的單一位置**，顯示每個 session 的即時進度，讓你看到完成多少、剩下多少，並確保各任務彼此獨立。Symphony 透過 Linear 做這件事（專案管理工具，每個欄位代表任務目前的狀態）；OpenAI 依 Harness Engineering 原則打造它，意思是整個 codebase 由 AI agent 規劃、撰寫並測試，而不是由人做。

由於 Symphony 開源，有人做了搭配 Claude Code 的版本：它跑一個 daemon（常駐背景程序）持續檢查你 GitHub repo 裡的 issue（也就是你在那裡建的任務）。當出現帶特定 label（例如 to do）的新 issue，就自動啟動一個背景 Claude Code session 去做，為該任務開獨立 branch，完成後開 pull request 請求合併回主要程式碼。

## Docker Sandbox 與 orchestrator 模式

worktree 只擋住檔案覆蓋與 Git 混亂，Symphony 這類分支只是讓流程順暢。**session 仍會因為某一個動了相依套件而壞掉，也仍會搶 localhost server**。要真的解掉開發面的問題需要 sandboxing：讓 agent 在一份可拋棄、完全隔離的開發環境副本中工作，不碰你的真實機器。影片使用 Docker Sandbox（同時是該集贊助商）。

- 每個 sandbox 跑在專屬 micro VM 上，有硬性安全邊界；Claude 安裝套件或建置專案的動作全部關在 sandbox 內，真實系統不受影響
- 影片主張這是唯一能讓 coding agent 在保持隔離的同時建置並執行 container 的 sandbox 方案，與 Claude Code 的平行 sub agent（各自在自己的 Git worktree）天然搭配

安裝與使用：跑安裝指令後以登入指令登入，再用 `sbx` 指令加 name flag、sandbox 名稱、`claude` 建立 sandbox；啟動後你對話的 AI agent 就跑在該隔離 sandbox 內。

預設情況下 sandbox 內的 agent 會把改動直接寫進你的 working tree（也就是真實專案檔案）。要更進一步可用 **clone mode**：建立 sandbox 時加 clone flag，sandbox 會帶著專案的複本，agent 的改動只發生在複本裡，不碰真實檔案。

影片最後的建議是：現在不需要再手動開一堆 Claude Code session 了。模型 spin up 與管理 sub agent／任務的能力已大幅進步，可以直接請 Claude Code 先規劃整個功能，再逐一取出子任務、為它開一個 Docker sandbox、把子任務交給該 sandbox。每個子任務都在自己的隔離環境完成，不影響其他 session。**同一個規劃 session 擔任 orchestrator**，管理所有 sandbox 並把各自的改動收回來；某個 sandbox 完成且確認任務無誤後，規劃者可以把它刪掉。執行期間可從 sandbox dashboard 觀察進度。
