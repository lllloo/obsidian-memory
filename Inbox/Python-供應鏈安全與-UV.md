---
title: Python 供應鏈安全與 UV
created: 2026-05-27
updated: 2026-05-28
source: https://www.youtube.com/watch?v=bw1ZLzdXJn4
published: 2026-05-21
tags:
  - security
  - python
  - ai-agent
---

**每次 `pip install` 或讓 AI agent 自動新增 dependency，本質上都是允許外部程式碼進入本機並執行。** package manager 已是供應鏈攻擊入口，而 AI coding agent 放大風險——agent 在長自主迴圈中可能安裝套件、讀檔、接觸環境變數與 credentials，還可能幻覺出不存在的套件名（typosquatting / slopsquatting），剛好裝到攻擊者預先佔好的 package。

## 攻擊如何發生

- 維護者被 phishing，package 或 CI token 被盜。
- 攻擊者發布名稱相近的惡意 package。
- worm 透過受害者檔案系統與 CI/CD token 繼續污染其他 package。

裝到惡意 package 後，惡意碼可讀 SSH key、環境變數、API key 送往攻擊者端。

## 核心理念

供應鏈安全不是只靠掃描工具，而是**讓 dependency 變更變成可審核事件**。對 AI workflow 最重要的是：把「agent 可以自己裝東西」改成「agent 必須先證明 dependency 值得加入」。

## UV 三防護（各對應一種風險）

改用 UV 當 Python 專案預設入口（重點不是速度，而是更嚴格的 resolver / lock 行為），把 dependency policy 放進 `pyproject.toml` 版控，讓團隊與 agent 遵守同一規則：

| 防護 | 機制 | 擋住的風險 |
|---|---|---|
| **精準 pin 版本** | 用 exact bound 取代 lower bound（「≥ 某版」） | **版本漂移**——升級成一次明確決策，而非 resolver 自動帶來新版（新版可能剛被污染） |
| **排除太新的 package** | `exclude-newer` 拒裝近期（如 7 天內）發布的版本 | **剛發布的惡意版本**——多數攻擊在前 24 小時被發現下架，冷卻期降低立即中招機率 |
| **locked sync** | CI/CD 與本機用 lock mode，`pyproject.toml` 與 `uv.lock` 不一致直接失敗 | **未授權 dependency 變更**——agent 改了依賴會被攔下，不會悄悄解析安裝 |

## 給 AI Agent 的規則

工具設定之外，明確告訴 agent：**不要為小功能隨便新增 dependency，每個 dependency 都要有理由**；只需小段功能就直接實作或引用特定原始碼片段，而非引入整個 package。這條規則放進 `AGENTS.md` / `CLAUDE.md` 或專案等價規則，尤其是允許 agent 長時間自主執行的專案。

## 相關

- [[Harness-Engineering]] — dependency policy 屬 agent 的 runtime guardrail 一環
