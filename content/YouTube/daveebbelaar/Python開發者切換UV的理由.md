---
title: Python 開發者為何切換到 UV
tags:
  - youtube
created: 2026-04-15
updated: 2026-04-15
published: 2025-08-07
source: https://www.youtube.com/watch?v=5rTwOt9Qgik
---

## UV 是什麼

UV 是超高速 Python 套件管理工具，核心功能是取代 `pip install`。安裝速度可達 pip 的 100 倍。除了安裝套件，UV 還能：

- 建立新專案結構（含 `.gitignore`、`pyproject.toml`）
- 自動建立與管理 virtual environment
- 管理主要依賴與開發依賴
- 管理 Python 版本（不需另外安裝 Python）

UV 由 Astral 開發，與 Python linter Ruff 同一團隊。

## 安裝

```bash
# macOS（推薦）
brew install uv

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 確認安裝
uv --help
```

## 新專案工作流程

```bash
# 建立新專案（含 .gitignore、pyproject.toml、.python-version、hello.py、README）
uv init my-project
cd my-project

# 在 IDE 開啟
cursor .
```

`uv init` 自動產生的結構：
- `.gitignore`（Python 常用排除清單）
- `.python-version`（釘定 Python 版本）
- `pyproject.toml`（取代 `requirements.txt`）
- `hello.py`（測試用）
- `README.md`（佔位符）

## 管理依賴

```bash
# 新增套件（自動建立 .venv 並更新 pyproject.toml）
uv add openai pydantic fastapi

# 移除套件
uv remove fastapi

# 新增開發用依賴（獨立 group，不進 production）
uv add ipykernel --dev
```

`pyproject.toml` 的 dependencies 欄位只記錄實際安裝的套件，不像 `pip freeze` 會混入所有子依賴，保持精簡。

## 團隊協作：uv sync

```bash
# clone repo 後一行指令完成環境設定
uv sync
```

`uv sync` 讀取 `pyproject.toml`，自動建立 `.venv` 並安裝所有依賴，速度接近即時。

## 執行 Python 檔

```bash
# 不需啟動 venv，直接執行
uv run hello.py
```

## 管理 Python 版本

```bash
# 列出已安裝的 Python 版本
uv python list

# 安裝特定版本
uv python install 3.12
```

不需另外安裝 Python，透過 UV 管理所有版本。

## 相容既有 pip 專案

```bash
# 支援直接用 requirements.txt 安裝
uv pip install -r requirements.txt
```

無需遷移現有專案，直接相容。

## 搭配 GitHub CLI 的完整流程

```bash
uv init my-project
cd my-project
uv add openai pydantic
git init && git add . && git commit -m "init"
gh repo create my-project --private --source=. --push
```

從構想到推上 GitHub repository，約 15 秒完成。
