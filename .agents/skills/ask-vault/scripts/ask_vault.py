#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ask-vault — 從任何專案向中央 Obsidian vault(第二大腦)發一個「請求/回應」查詢。

cross-CLI + 跨平台:偵測呼叫者是哪個 coding agent(caller-match),用同一生態的
headless CLI 在 vault root 走 Query 動作(讀 wiki/01.index.md → 定位頁 → 讀頁 →
附引用綜合),印出答案後退出。隨叫隨起、答完即退,不需常駐。唯讀:各 backend 以
其原生機制限制。純 stdlib、無 shell 方言,Windows/mac/Linux 一致。

用法(由 ask-vault skill 以 ${CLAUDE_SKILL_DIR} 展開呼叫):
    python3 <skill_dir>/scripts/ask_vault.py "我之前對 X 的結論是什麼?"
    echo "問題" | python3 <skill_dir>/scripts/ask_vault.py
設定(環境變數):
    OBSIDIAN_VAULT    vault root 路徑(預設 ~/code/obsidian-memory)
    ASK_VAULT_BACKEND 強制指定 backend:claude | codex | opencode(覆寫自動偵測)
    ASK_VAULT_MODEL   指定 model(僅 claude backend 生效;預設沿用各 CLI 預設)

backend 解析順序:ASK_VAULT_BACKEND 覆寫 → 呼叫者環境標記 → 安裝優先序 fallback。
標記驗證狀態:
    claude   = 已驗證   $CLAUDECODE(Claude Code 注入)
    codex    = $CODEX_SANDBOX(Codex 沙箱標記)
    opencode = 任一 $OPENCODE* 環境變數(啟發式)

本檔為 source of truth,checked-in 於 vault repo 的 .agents/skills/ask-vault/scripts/;
skill 目錄透過 symlink(~/.claude/skills/ask-vault)暴露為全域 skill,由 SKILL.md
以 python3 ${CLAUDE_SKILL_DIR}/scripts/ask_vault.py 呼叫。
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# python.md:只修被點名的串流,兩條都要;確保本腳本 print 的答案在 Windows 也是 UTF-8。
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SENTINEL = "schema/vault-map.md"  # CWD 契約哨兵:此路徑只存在於本 vault


def vault_root() -> Path:
    return Path(os.environ.get("OBSIDIAN_VAULT") or (Path.home() / "code" / "obsidian-memory"))


def build_prompt(question: str) -> str:
    return (
        "你是這個 Obsidian LLM Wiki vault 的 Query 助手。針對下面的問題,執行 vault 的 Query 動作:\n"
        "1. 先讀 wiki/01.index.md(先看頂部「最近更新」,再看分類目錄)定位相關頁。\n"
        "2. 讀相關頁;必要時 Grep raw/ 與 wiki/ 補證。\n"
        "3. 用繁體中文綜合回答,每個關鍵主張就地附上來源頁(檔名或 wikilink)。"
        "vault 查不到就明說「vault 無此資料」,不要杜撰。\n"
        "唯讀:不要修改任何檔案。\n\n"
        f"問題:{question}"
    )


def pick_backend() -> str:
    """caller-match:偵測呼叫端,決定用哪個 CLI 跑查詢。"""
    override = os.environ.get("ASK_VAULT_BACKEND")
    if override:
        return override.strip()
    if os.environ.get("CLAUDECODE"):
        return "claude"
    if os.environ.get("CODEX_SANDBOX"):
        return "codex"
    if any(k.startswith("OPENCODE") for k in os.environ):
        return "opencode"
    for name in ("claude", "codex", "opencode"):  # fallback:第一個裝了的
        if shutil.which(name):
            return name
    return ""


def _resolve(name: str):
    """跨平台解析可執行檔(Windows 上 .cmd/.exe shim 需完整路徑)。"""
    exe = shutil.which(name)
    if not exe:
        sys.stderr.write(f"ask-vault: 未安裝 {name}\n")
    return exe


def run_claude(vault: Path, prompt: str) -> int:
    exe = _resolve("claude")
    if not exe:
        return 127
    # --allowedTools 限唯讀工具;stdout(答案)/stderr 直接繼承透傳。
    args = [exe, "-p", prompt, "--allowedTools", "Read Grep Glob", "--permission-mode", "manual"]
    model = os.environ.get("ASK_VAULT_MODEL")
    if model:
        args += ["--model", model]
    return subprocess.run(args, cwd=str(vault)).returncode


def run_codex(vault: Path, prompt: str) -> int:
    exe = _resolve("codex")
    if not exe:
        return 127
    # -s read-only 原生唯讀沙箱;-C cwd;-o 只把最終訊息寫檔(exec 的 stdout+stderr
    # 進度/reasoning 太吵,全收進 log,成功只吐 -o 檔的答案、失敗才倒 log 診斷)。
    out_fd, out_path = tempfile.mkstemp(prefix="askvault-codex-")
    os.close(out_fd)
    log_fd, log_path = tempfile.mkstemp(prefix="askvault-codexlog-")
    try:
        with os.fdopen(log_fd, "wb") as log:
            rc = subprocess.run(
                [exe, "exec", "-s", "read-only", "-C", str(vault),
                 "--skip-git-repo-check", "-o", out_path, prompt],
                cwd=str(vault), stdout=log, stderr=subprocess.STDOUT,
            ).returncode
        if rc != 0:
            sys.stderr.write("ask-vault: codex exec 失敗(可能需 codex login,或與 opencode 共用 oauth 造成 token 失效)\n")
            sys.stderr.write(Path(log_path).read_text(encoding="utf-8", errors="replace"))
            return rc
        sys.stdout.write(Path(out_path).read_text(encoding="utf-8", errors="replace"))
        return 0
    finally:
        for p in (out_path, log_path):
            try:
                os.unlink(p)
            except OSError:
                pass


def run_opencode(vault: Path, prompt: str) -> int:
    exe = _resolve("opencode")
    if not exe:
        return 127
    # opencode 無 read-only flag;不加 --auto,預設不自動核准寫入 → 實質擋住改檔。
    # 進度/todos/tool 行走 stderr、最終答案走 stdout;stderr 收進 log,成功只放行 stdout。
    log_fd, log_path = tempfile.mkstemp(prefix="askvault-oclog-")
    try:
        with os.fdopen(log_fd, "wb") as log:
            rc = subprocess.run(
                [exe, "run", "--dir", str(vault), prompt],
                cwd=str(vault), stderr=log,  # stdout 繼承透傳(乾淨答案)
            ).returncode
        if rc != 0:
            sys.stderr.write("ask-vault: opencode run 失敗(可能與 codex 共用 oauth 造成 token 失效,或需 opencode auth login)\n")
            sys.stderr.write(Path(log_path).read_text(encoding="utf-8", errors="replace"))
        return rc
    finally:
        try:
            os.unlink(log_path)
        except OSError:
            pass


RUNNERS = {"claude": run_claude, "codex": run_codex, "opencode": run_opencode}


def main() -> int:
    vault = vault_root()
    if not (vault / SENTINEL).is_file():
        sys.stderr.write(f"ask-vault: 找不到 vault(缺 {SENTINEL}):{vault}\n")
        sys.stderr.write("  請設 OBSIDIAN_VAULT 指到 vault root,或改腳本內預設值。\n")
        return 1

    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = sys.stdin.read()
    if not question.strip():
        sys.stderr.write('用法: python3 ask_vault.py "你的問題"   或   echo "問題" | python3 ask_vault.py\n')
        return 1

    backend = pick_backend()
    runner = RUNNERS.get(backend)
    if runner is None:
        sys.stderr.write(
            "ask-vault: 找不到可用的 CLI backend(claude/codex/opencode 皆未安裝)。"
            "可設 ASK_VAULT_BACKEND 指定。\n"
        )
        return 127
    return runner(vault, build_prompt(question))


if __name__ == "__main__":
    sys.exit(main())
