---
title: OpenClaw 作者打造 Crabbox 阻止 AI 送出爛程式碼
description: 大量平行 agent 的瓶頸已從寫 code 移到 merge；Crabbox 替每個 work tree 在雲端開隔離沙箱跑 dev server 與測試，同步未提交 diff 並回傳截圖影片當 PR 證據。
created: 2026-06-29
updated: 2026-06-29
source: https://www.youtube.com/watch?v=1HkqTlXbQmQ
published: 2026-06-24
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
---

OpenClaw 作者 Peter Steinberg 推出新工具 Crabbox，解決同時運行數十個平行 agent session 時的測試與驗證瓶頸。影片作者本人平常至少同時跑 10 個 agent session，Peter 的截圖則同時跑超過 15 個。

## 核心問題：瓶頸從「寫 code」變成「merge code」

當團隊建立各種 loop 讓 agent 自主找問題、接手工作後，平行 session 產生的 PR 數量爆增，遠超過去做不到的規模。但每個 PR 都帶有破壞系統的風險，造成龐大的 review 與上線負擔。結論是：瓶頸不再是寫程式，而是如何把程式安全 merge 進 code base。

關鍵第一步是給 agent 工具與 skill 去**驗證自己的工作並產出證據**。作者推薦用 Playwright：讓 agent 自行用瀏覽器測試，並輸出影片錄製等 artifact，把這些證據附進 PR，讓人類更容易放心 merge。

## 為什麼本機平行測試會崩潰

只跑 3、4 個 agent 時這套還行，但平行數量一多就出問題。Cloud Code 的 work tree 能給每個工程 ticket 一個隔離環境寫 code，但**測試需要在 work tree 的程式上跑 dev server**，這在本機很難：

- 很多 code base 沒設計成可同時跑多個 instance，有些 port 因合理原因被寫死。
- 本機只有一個 Docker daemon、一個 DB／OS。若跑本機 Supabase，所有 session 共用同一 instance；某個 session 試新 schema 就可能搞垮其他所有 session。
- 即使解決上述問題，跑現代 production repo 本身就很吃資源，難以橫向擴展。

正解是：不要全部在本機平行跑，而是替**每個 work tree 開一個獨立隔離環境**啟動 dev server。每個 agent 擁有自己的 sandbox，內含獨立資料庫等一切，彼此隔離互不影響。

## 自建沙箱 pipeline 的麻煩

要自建這套流程並不簡單：臨時開機器、掛 disk、複製程式進去、安裝依賴、啟動 app、開瀏覽器測試，完成後還要關機刪除。作者團隊曾全程自建，能用但仍有痛點：

測試的目的是揪出 bug。當 agent 在 box 上測到東西壞掉、在本機改了 code 修 bug 後，**沒有簡單方法把這些 dirty file 弄進 sandbox**。走正常的 commit/push/CI 流程不理想，repo 會堆滿大量無謂 commit；也不想重建整個 box。理想狀態是改完後能在數秒內重測。

## Crabbox 的運作方式

Crabbox 讓 agent 在雲端暖機一個 box、同步本機 work tree 的 dirty diff、即時跑測試。核心指令：

```bash
crabbox warmup      # 暖機一個雲端 box
crabbox run <bash>  # 在雲端 box 跑任意 bash 指令
crabbox stop        # 關閉並刪除 box
```

每次 `run` 都會先把本機未提交的變更同步到雲端 box（只要資料夾有 git init，**不必先 commit** 即會同步所有未提交變更），再執行指令，體驗幾乎等同在本機跑。修完 bug 後下次跑任何指令會自動同步最新版本，永遠測到最新狀態。

典型流程：`crabbox warmup` 開 sandbox → `crabbox run setup`（裝依賴、起 dev server）→ 跑預定義測試或用 Playwright 做端對端測試 → 命中 bug 就在本機修、下次自動同步 → `crabbox stop`。

## 設定檔結構

- **Dockerfile**：封裝本機所需的一切，例如 Node、Docker、Supabase CLI 等必要 CLI，可直接 prompt agent 產生。
- **`crabbox.yml`**：定義 sandbox provider、不要同步的檔案（exclude）、要傳入的環境變數。所列環境變數會經 SSH 連線直接推進 box（加密 data plane，相對安全）。exclude 通常不需列 `node_modules`、`.next`、`.turbo`、`.env`（多半已在 gitignore），但可用來排除很重又不需同步的資料夾（如過往證據或存取檔）。
- **`setup.sh`**：讓 agent 跑單一腳本就把 dev server 完整拉起，不必一步步來。

## Artifact（證據）指令

Crabbox 提供產出與發佈證據的指令：

- 每次 run 可帶 artifact glob，指令結束後自動下載符合的 artifact 回本機（agent 寫端對端測試腳本特別有用，跑完檔案自動回傳）。
- `artifacts collect`：在雲端電腦截圖。
- `artifacts videos`：螢幕錄製雲端電腦畫面。
- `artifacts publish`：直接上傳到 S3 bucket。

證據可上傳 S3，或用 GitHub release assets 上傳檔案並 inline 嵌入 PR，把圖片／影片貼成 PR comment。

## 實際設定示範（搭配 Daytona）

示範對象是一個有登入功能、可與 assistant 對話、跑本機 Supabase 的 web app。Provider 選 **Daytona**（sandbox 啟動快）。

設定步驟：

1. Dockerfile 裝 Supabase CLI 等套件。
2. `crabbox.yml` 指定 provider 為 Daytona、傳入 snapshot（Daytona 上預建的 image）、default work root、sync 行為（exclude）、環境變數。
3. `setup.sh` 一鍵起 dev server。
4. `daytona login` → `daytona organization list` → `daytona organization use <org>`。
5. `daytona snapshot create` 給名稱並指向 Dockerfile 與 context 資料夾，定義 CPU／記憶體／disk／region。
6. Daytona 需用 API key 連接：到 Daytona 建 key，設成本機環境變數。
7. `crabbox warmup --provider daytona` 並給一個 slug（session ID）暖機 sandbox。

作者另外寫了包裝腳本 `cbx.sh`，把多個 Crabbox 指令併成單一指令。例如 `up` 指令會開 box、輪詢狀態直到 ready，再跑 `setup.sh`。**Daytona 預設 60 秒會 timeout**，所以要在背景跑指令、每 10 秒回報結果直到完成。如此 agent 只需 `bash cbx.sh up` 就放手讓 setup 在背景跑。

## 跑指令與 SSH tunnel

跑指令：`crabbox run --provider daytona --id demo bash <command>`。有個 `--no-sync` flag 可叫 Crabbox 此次不同步檔案，適用讀檔或用 Playwright CLI 測試等不需 resync 的情境。作者在 `cbx.sh` 已預設 provider 與何時帶 `--no-sync`。

可開 SSH tunnel 把本機 3000 port 接到 sandbox 3000 port、本機後端 port 接 sandbox 後端 port，就能在本機瀏覽器測雲端 dev server。但這會佔用本機 port 造成衝突，對平行場景不是好解法。

## 用 skill 讓 agent 自主測試

作者更傾向讓 agent 在雲端跑 Playwright CLI bash 指令並取回證據，或跑預定義端對端測試。他定義了一個叫 `crabbox test` 的 skill：agent 用 Crabbox 在雲端起 dev server，再用 Playwright CLI 測試，搭配自訂的 `pw`（preview）指令（帶 ID、provider、`--no-sync`）。如此只要告訴 agent「用 crabbox 幫我測 web app」，它就會開 box、起 dev server、用 Playwright 跑完整端對端測試，帶回截圖或錄影證據。可同時跑任意多個平行 session 而不衝突。

## 開源資源

Crabbox 為開源工具。作者另提供 `crabbox setup` skill，可交給 Cloud Code 或 Codex 自動走完設定 Dockerfile、連接 provider、`crabbox.yml` 的整套流程；還有一個標準 code base harness skill，除了設定 Crabbox 也涵蓋其他能讓 agent 更有效率交付的要素。
