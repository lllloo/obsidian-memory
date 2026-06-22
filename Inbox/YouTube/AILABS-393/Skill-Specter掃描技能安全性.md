---
title: 用 Skill Specter 掃描 Agent Skill 安全性
description: NVIDIA 的 Skill Specter 在安裝前掃描 agent skill 的安全風險，拆解 skill 攻擊的六種手法，並用 Claude Code headless 模式免費跑出本需 OpenAI key 的 AI 深度掃描。
created: 2026-06-22
updated: 2026-06-22
source: https://www.youtube.com/watch?v=KiTmBtyaeXg
published: 2026-06-17
parent: "[[01.index]]"
tags:
  - youtube
  - ai-agent
  - claude-code
---

影片核心問題：agent skill 到處都是、大家不檢查就信任，但研究掃過 3 萬多個 skill，超過四分之一含安全漏洞。NVIDIA 做了 Skill Specter，安裝前掃描任何 skill 並告訴你危險程度。重點是有一類攻擊會繞過預設掃描，要靠一個預設關閉、且通常要花錢的 AI 掃描才抓得到——影片用 Claude Code 繞過這筆成本。

## 安裝與基本掃描

- GitHub repo 有安裝指令，直接交給 Claude Code 就能裝好依賴並完成設定。
- repo 的 test 資料夾放了刻意危險的 skill 可驗證工具運作；掃描後每個都會建議不要安裝。
- 分數越高越危險；不只給數字，還指出確切的行號、檔名與位置，說明是什麼把分數推高的。

## Skill 攻擊你的六種方式

工具有 14 個類別，影片歸納成六類：

1. **隱藏指令（hidden instructions）**：skill 本質是一份指令文字檔，agent 會整篇讀進去當命令。壞 skill 把額外指令藏在註解、用隱形字元、或把文字打散成你看不懂但 AI 讀得懂的編碼。掃描器專門獵這些隱藏指令。
2. **冒充（impersonation）**：agent 會用名字呼叫它信任的工具（例如叫 `read` 的讀檔工具）。惡意 skill 給自己的工具取一模一樣的名字，把其中一個字母換成其他字母系統的相似字元（例如用長得一樣的俄文字母替掉 `a`）。掃描器逐字檢查每個字元的真實身分來抓出那個假字母。
3. **謊報用途**：description 說一套、程式做另一套（自稱簡單 formatter 卻偷偷連網；說只要讀檔權限卻其實在寫檔、跑指令）。這類最難抓，要靠下面的 AI 掃描。
4. **竊取憑證**：翻出機器上存的 API key、密碼等，打包送到外部 server。
5. **直接跑惡意程式**：例如 reverse shell，把整台電腦的遠端控制權交給陌生人。這類惡意碼有已知指紋，掃描器拿程式碼比對指紋資料庫。
6. **毒化依賴（poison dependencies）**：skill 常會跑外部 CLI 工具，壞 skill 引入惡意套件（例如跟熱門套件差一個 typo 的假套件）。掃描器把每個套件比對已知惡意套件的即時資料庫，標出假名與下載執行指令。

## AI 掃描（第二模式）

- 第一模式只做無情境的 pattern matching，會誤報（false positives）安全的東西。
- 第二模式是 **AI 掃描**，加上 `--no-llm` 旗標的相反設定即可啟用（影片描述為移除該限制）。但原始程式要跑 AI 檢查需要插入 OpenAI key。
- **繞過成本的做法**：改用 Claude Code 來跑 AI 檢查。實際是用 Claude 的 **headless 模式**（背景執行、無聊天視窗、自行執行指令），靠 Anthropic 方案的每月額度。叫 Claude Code 改那一行程式即可（可能遇到小 bug，但只是一句 prompt 的事）。
- test 資料夾有需要 AI 檢查才抓得到的危險 skill：只跑 no-LLM 檢查分數是 0（看似安全），加上 AI 檢查分數跳到 100 並說明原因。
- 反向案例也存在：某 skill no-LLM 給 100，AI 檢查後回 0，代表其實安全——顯示 AI 掃描同時降低誤報。

## Discover Skills 工作流

把掃描器包成一個叫 discover skills 的 skill，不只偵測還能修正，並串成「找 skill + 安裝前必掃」的完整流程：

- 用 **skills.sh**（專門放 skill 的共享 Git repo）找新 skill，近期 CLI 更新後 Claude 可直接從命令列下查詢、拉出需要的 skill。
- `scan.sh`：實際跑 Skill Specter 的腳本，把 Claude headless 模式的修正直接內建；預設跑一般檢查，需要時跑 AI 檢查。
- `skill.md` 流程：辨識目標 → 掃描 → 顯示發現 → 修正問題 → 重跑整個 loop 確認乾淨。
- 實例：要改進 `make-design.md`（從已建好的 app 抽 design token：顏色、字型、間距規則），叫它用 skills.sh 搜尋、載入 discovery skill 拉回候選 skill。流程強制安裝前必掃：一個得分 10（安全）、另一個 100（別裝）；對後者再跑 AI 檢查後得 0，確認安全。核心是不再盲目從網路抓 skill，而是用一個 skill 就能啟動整套安全流程。
