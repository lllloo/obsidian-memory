---
title: "這個 AI 技能能取代初級工程師 90% 的工作（Claude Code Agent Teams）"
tags:
  - youtube
created: 2026-04-13
updated: 2026-04-13
published: 2026-03-09
source: https://youtu.be/PjenU4zwY5U
---

**影片描述**：作者展示自製的 Claude Code Skill「Fix Ticket」，能從讀取 Jira 票券到部署修復、更新票券狀態，全程自動化 bug 修復流水線，並整合多代理程式碼審查與 Playwright 自動化測試驗證。目標是讓 AI 自動化初階工程師約 90% 的日常工作。

**重點摘要：**
- **Fix Ticket 是什麼**：一個 Claude Code Skill（mega skill），開源放在作者 GitHub（startup-cloud-skills），封裝了從讀票到部署的完整 bug 修復流水線，內含 `dev-team`、`review-team`、`review-fix`、`playwright-cli` 等多個子 skill。
- **完整 8 階段自動化流程**：① Branch Strategy（詢問工作 branch）→ ② 讀取 Jira Ticket 並摘要 → ③ Playwright 重現 bug 截圖確認 → ④ 研究根本原因並提出修復計畫（需用戶確認）→ ⑤ 實作修復並執行 build/lint → ⑥ 3 個並行代理從不同角度審查（race condition、edge case、silent failure）並自動修正 → ⑦ Playwright 再次驗證修復生效 → ⑧ Vercel 部署監控（每 45 秒輪詢）並在 Jira 留下測試說明指派 QA。
- **彈性參數控制**：skill 支援 `skip_review`、`skip_jira`、`skip_deploy`、`skip_qa` 等旗標，可視需要跳過特定階段，`auto_commit` 預設為 true，`assign_to` 可指定完成後指派對象。
- **所需 MCP 工具**：Jira MCP、Vercel MCP、Supabase MCP，以及上集介紹的 Playwright CLI Skill，工具鏈完整才能執行全流程。
- **Multi-Agent Code Review 細節**：review-team 由 5 個代理組成（含 devil's advocate 角色），review-fix 則負責在審查發現問題後立即派遣平行代理修正，審查層層疊加提升準確率。
- **實際示範結果**：作者以自己的 SaaS 應用 Jira 看板為例，從觸發 skill 到部署完成、Jira 票券更新全程無需手動介入，展示了從 bug 發現到 QA 交接的完整閉環。
- **核心價值主張**：Fix Ticket 複製了初階工程師「讀票→研究→分析→實作→審查→驗證→部署→交接」的典型工作流程，作者認為可自動化約 90% 的初階工程師日常工作。
