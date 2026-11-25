#!/usr/bin/env python3
"""為 vault-lint 語意層列出自上次健檢以來變動的 wiki 內容頁。

窗口起點是最近一個標題以 `健檢：` 開頭的 commit（呼叫端收尾時用此前綴 commit，
無檔案變更的一輪用 --allow-empty）；沒有這種 commit 時涵蓋全部歷史。
候選頁依最近一次變動由新到舊排列，一輪全部審完；腳本本身不寫入任何檔案。

輸出格式：

  SEMANTIC:<file>            本輪應審頁面
  SUMMARY:semantic=<count>   本輪應審頁數
  SUMMARY:since=<sha|none>   窗口起點 commit（不含該 commit 本身的變動）
  SELECT:complete            選頁正常完成；缺少此行或出現 ERROR 即視為異常

用法：python3 .agents/skills/vault-lint/scripts/semantic_select.py
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REVIEW_PREFIX = "健檢："


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        detail = next((line for line in result.stderr.splitlines() if line.strip()), "未知錯誤")
        raise RuntimeError(f"git {args[0]} 失敗：{detail.strip()}")
    return result.stdout


def last_review_commit(root: Path) -> str | None:
    for line in git(root, "log", "--format=%H%x09%s").splitlines():
        sha, _, subject = line.partition("\t")
        if subject.startswith(REVIEW_PREFIX):
            return sha
    return None


def discover_changed_pages(root: Path, since: str | None) -> list[str]:
    """依最近一次變動由新到舊列出 since 之後變動且仍存在的 wiki 內容頁。"""
    revision = f"{since}..HEAD" if since else "HEAD"
    pages: list[str] = []
    seen: set[str] = set()
    for raw in git(root, "log", revision, "--name-only", "--pretty=format:").splitlines():
        page = raw.strip()
        if (
            page in seen
            or not page.startswith("wiki/")
            or not page.endswith(".md")
            or page == "wiki/01.index.md"
            or not (root / page).is_file()
        ):
            continue
        seen.add(page)
        pages.append(page)
    return pages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."), help=argparse.SUPPRESS)
    args = parser.parse_args()

    root = args.root.resolve()
    if not (root / "schema" / "vault-map.md").is_file():
        print("ERROR:not-vault-root（找不到 schema/vault-map.md，請在 vault root 執行）")
        return 1

    try:
        since = last_review_commit(root)
        pages = discover_changed_pages(root, since)
    except (OSError, RuntimeError) as exc:
        print(f"ERROR:semantic-select（{exc}）")
        return 1

    for page in pages:
        print(f"SEMANTIC:{page}")
    print(f"SUMMARY:semantic={len(pages)}")
    print(f"SUMMARY:since={since[:7] if since else 'none'}")
    print("SELECT:complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
