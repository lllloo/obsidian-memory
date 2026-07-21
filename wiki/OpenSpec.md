---
title: OpenSpec
description: 說明 Fission-AI 輕量規格工具的安裝、目錄、delta spec 與五步工作流，並標示流程可信但效果未實證
created: 2026-07-16
updated: 2026-07-21
source: https://github.com/Fission-AI/OpenSpec
published: ""
parent: "[[wiki/01.index]]"
tags:
  - coding-agent
  - agent-framework
  - ai-agent
---

# OpenSpec

[Fission-AI 的 OpenSpec](https://github.com/Fission-AI/OpenSpec) 是一套輕量的 **spec 層工具**，核心主張是**在寫任何程式碼前，先讓開發者與 AI coding agent 就「要建什麼」達成共識**（README 原話：*"agree on what to build before any code is written"*）。它不是 RAG、不是重型流程框架，而是把「規格」變成一組 checked-in 的 markdown，夾在你與 AI 之間當作實作契約。

在 [[AI-自主工作流的實證檢驗]] 的 spec-driven 光譜裡，OpenSpec 定位為 **Spec Kit 的輕量替代**——比 Spec Kit 的七步（`constitution → specify → clarify → plan → tasks → analyze → implement`）精簡，也比 BMAD 的多角色鏈輕。**注意該頁的核心結論**：整個 SDD 領域「流程描述清楚，但『這樣做讓 agent 做得更好』幾乎沒有夠格的獨立效果證據」——OpenSpec 的**流程可信、效果未經實證**，採用前請把它當「協作結構」而非「已證明的提效方案」。

本頁內容來自 deep-research（2026-07-16，5 路平行搜尋＋每條主張 3 票對抗式查證）。除另註明外，各條皆 **3-0 通過驗證、強度 high**，且來自一手來源（官方 GitHub docs 的 main 分支、openspec.dev、npm registry）。

## 安裝與初始化（high）

前置需求：**Node.js 20.19.0+**（行為關鍵門檻，故保留版本號；其餘版本以官方 changelog 為準）。

```bash
# 全域安裝（官方主推）
npm install -g @fission-ai/openspec@latest

# 其他套件管理器（bun 仍需 Node.js 20.19+ 在 PATH）
pnpm add -g @fission-ai/openspec@latest
yarn global add @fission-ai/openspec@latest
bun add -g @fission-ai/openspec@latest

# 免安裝
npx openspec@latest --version
nix run github:Fission-AI/OpenSpec -- init   # NixOS

# 在專案內初始化：建立 openspec/ 目錄並自動為所選 AI 工具寫整合檔
cd your-project && openspec init

# 驗證與升級
openspec --version
openspec update            # 升級 CLI 後刷新產生的整合檔
```

來源：官方 [README](https://github.com/Fission-AI/OpenSpec)、[installation.md](https://github.com/Fission-AI/OpenSpec/blob/main/docs/installation.md)、[getting-started.md](https://github.com/Fission-AI/OpenSpec/blob/main/docs/getting-started.md)、[openspec.dev](https://openspec.dev/)、npm registry — 六個來源逐字一致。

## 目錄結構（high）

```
openspec/
├── specs/                    # 現行行為的真實來源（source of truth）
│   ├── auth-login/           # 一個 capability 一個資料夾
│   │   └── spec.md
│   └── checkout-cart/
│       └── spec.md
├── changes/                  # 提案中的變更（每個變更一資料夾）
│   ├── <change-name>/
│   │   ├── proposal.md       # 為何做、做什麼
│   │   ├── specs/            # delta spec（ADDED/MODIFIED/REMOVED）
│   │   ├── design.md         # 設計決策（可選）
│   │   └── tasks.md          # 可獨立驗證的實作步驟
│   └── archive/              # 已完成變更（巢狀於 changes/ 內）
└── config.yaml               # 專案設定（可選）
```

**常見誤述（勿引用）**：網路上流傳「`archive/` 與 `changes/`、`specs/` 三者平行」的結構——此版本在對抗驗證中被 **0-3 否決**。正典為 **`archive/` 巢狀在 `changes/` 底下**（`changes/archive/`）。

來源：[concepts.md](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md) 樹狀圖、getting-started.md、openspec.dev、live repo tree。

## 核心概念（high）

| 概念 | 定義 |
|---|---|
| **specs/** | 系統**當前**行為的權威真實來源，描述系統「現在」怎麼運作 |
| **changes/** | 提案中的修改，住獨立資料夾，直到準備好合併才併入；**多個變更可並存互不衝突** |
| **deltas（delta specs）** | 用 `ADDED` / `MODIFIED` / `REMOVED` / `RENAMED` 區塊表達「這次變更對 spec 的增刪改」——這是 OpenSpec 能用於**既有專案（brownfield）**的關鍵設計 |
| **archive model** | 變更完成時把 delta spec **合併回主 specs**，並移到帶日期的 archive 目錄；是 OpenSpec 內部操作，**非 git merge** |

concepts.md 逐字：*"Specs are the source of truth — they describe how your system currently behaves."* / *"Changes are proposed modifications — they live in separate folders until you're ready to merge them."*

## 工作流：終端機 2 步 + 聊天室 N 步（high）

官方原話：*"Steps 1 and 2 happen in your terminal. The rest happen in your AI assistant's chat."* 前兩步（安裝、初始化）在**終端機**，其餘全在 **AI 助理聊天室**中透過 `/opsx:` 斜線指令進行。

core profile 五步序列：

```
/opsx:explore ──► /opsx:propose ──► /opsx:apply ──► /opsx:sync ──► /opsx:archive
```

| 步驟 | 做什麼 |
|---|---|
| **explore** | （可選但建議）規劃前的思考夥伴——**不產 artifact、不寫碼**，只釐清方向 |
| **propose** | 建立變更目錄，產出 `proposal.md`、`specs/`（delta）、`design.md`、`tasks.md` |
| **apply** | 實作 tasks.md 裡的任務 |
| **sync** | 把 delta specs 套用回主 specs |
| **archive** | 最終合併並移入 `archive/` |

Artifact 產生順序為 `proposal → specs → design → tasks → implement`，各階段建構在前者脈絡上，但是「dependency enablers」而**非 rigid gates**：`design` 可跳過；`specs` 與 `design` 都只依賴 `proposal`；`tasks` 依賴 `specs`，並在 `design` 存在時一併依賴它（`design` 被跳過時則僅依賴 `specs`）。

## CLI 指令（high）

| 指令 | 作用 |
|---|---|
| `openspec init [path]` | 建立資料夾結構並配置 AI 工具整合 |
| `openspec new change <name>` | 建立一個 change 目錄 |
| `openspec validate [item-name]` | 驗證 change/spec 的結構問題 |
| `openspec archive [change-name]` | 封存完成的 change，把 delta spec 合併回主 specs |
| `openspec update` | 升級 CLI 後刷新產生的整合檔 |
| `openspec list` | 列出項目 |

`init` 的 `--tools` 選項接受 `all` / `none` / 逗號分隔清單（如 `claude,codex,cursor,gemini`），支援 `claude`、`cursor`、`github-copilot` 等 30+ 工具。

**舊語法已 deprecated**：noun-based 的 `openspec change ...` 已改為 verb-based 的 `openspec new change ...`。

來源：[cli.md](https://github.com/Fission-AI/OpenSpec/blob/main/docs/cli.md)。

## 與 AI Coding Agent 整合（high）

OpenSpec 原生整合 **30+ 種 AI 助理**（官方 [supported-tools.md](https://github.com/Fission-AI/OpenSpec/blob/main/docs/supported-tools.md) 實際列舉 31 個 tool ID），透過各工具的自訂 slash command——明確包含 Claude Code、Cursor、Codex、GitHub Copilot、Cline、Continue、Windsurf、Gemini。

執行 `openspec init` 時依所選 profile/workflow 與 delivery mode 為所選工具寫入整合檔：

| 工具 | 整合檔位置 |
|---|---|
| **Claude Code** | `.claude/skills/openspec-*/`（skill 檔）與 `.claude/commands/opsx/<id>.md` |
| **Cursor** | `.cursor/commands/opsx-*`（部分用 `.cursor/rules`） |

31 個工具中 28 個產生 tool-specific 命令檔，僅 3 個用 skill-based fallback。（工具數字在不同頁面有 20+/25+/30+/40 的浮動，但實際列舉穩定在 31 個，「30+」為準確下界。）

## 最佳實踐（medium／secondary 來源）

以下來自 [openspec.pro/best-practices](https://openspec.pro/best-practices/) 與實戰部落格，**非官方一手文件、強度低於上列各節**，方向一致值得參考：

- **Proposal 品質**：`problem` / `solution` / `scope` / `risks` 四點都要答清楚。
- **Task sizing**：拆成可**獨立驗證的編號步驟**，避免產生巨大 diff。
- **Spec 寫法**：用 **Given/When/Then** 具體場景取代模糊形容詞——這樣才能成為 AI 的實作契約。
- **Scope 管理**：**多個小 change 勝過單一大 change**。

## 時效性警告

- **命令命名有版本漂移**：文件同時出現舊前綴 `/openspec:proposal` 與新前綴 `/opsx:propose`；引用具體斜線指令前回查你安裝版本的官方 docs。
- **archive 位置**在 v0.17.2 曾有 doc/command 不一致（issue #412），但正典結構確為 `changes/archive/`。
- 版本號（Node 20.19+、套件版本）會隨迭代變動，行為關鍵處以官方 changelog 為準。

## 未解問題（本輪未查證充分）

- `/opsx:sync` 與 `/opsx:archive` 的確切分工邊界——來源僅粗略描述。
- `openspec/config.yaml` 的可設定欄位與 schema——只確認存在且為 optional。
- delta specs 的 `ADDED/MODIFIED/REMOVED/RENAMED` 實際撰寫格式與 `validate` 的具體檢查規則。
- README 提及的 **'Stores (beta)'** 是什麼——屬新功能，未查證。

## 相關頁面

- [[AI-自主工作流的實證檢驗]] — OpenSpec 所屬的 spec-driven 方法論的效果證據盤點：流程可信但缺獨立效果驗證，且列出該領域「必須停止引用的空氣數字」（含被否決的「Spec Kit 比 OpenSpec 多耗 2 倍 token」）。
- [[Agent-Harness-Engineering-框架綜述]] — 「業界怎麼說該建 agent」的框架層綜述，與本頁的具體工具實作互補。
- [[Mem0]] — 該頁釐清一個常見的**類別錯置**：OpenSpec 不是 mem0 的整合對象。本頁的 OpenSpec 不是 agent host（不跑 MCP、不裝 plugin），而是**裝進** host 的 workflow 框架；兩者若同在一個 host 是**爭同一個位置**——本頁的 `specs/` 用 checked-in 可 review 的規格決定 agent 該遵守什麼，mem0 用雲端不可 review 的記憶做同件事，權威來源會分裂。
