from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
HOOK = ROOT / ".agents/skills/vault-lint/scripts/pre-commit"

PAGE = """---
title: {title}
description: 說明測試頁面的核心概念、適用情境與相關知識連結，供自動化檢查使用
created: 2026-11-25
updated: 2026-11-25
parent: "[[wiki/01.index]]"
tags:
  - test
---

{body}
"""
INDEX = """---
title: 索引
created: 2026-11-25
updated: 2026-11-25
tags:
  - index
---

- [[甲頁]] — 說明測試頁面的核心概念、適用情境與相關知識連結，供自動化檢查使用
- [[乙頁]] — 說明測試頁面的核心概念、適用情境與相關知識連結，供自動化檢查使用
"""


class PreCommitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp_dir.name)
        self.git("init", "-q")
        self.write("schema/vault-map.md", "# 測試 vault\n")
        self.write("wiki/01.index.md", INDEX)
        self.write("wiki/甲頁.md", PAGE.format(title="甲頁", body="[[乙頁]]"))
        self.write("wiki/乙頁.md", PAGE.format(title="乙頁", body="[[甲頁]]"))
        self.git("add", "-A")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def git(self, *args: str) -> None:
        subprocess.run(["git", *args], cwd=self.repo, check=True)

    def write(self, relative: str, content: str) -> None:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def run_hook(self) -> subprocess.CompletedProcess[str]:
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        return subprocess.run(
            [sys.executable, "-B", str(HOOK)], cwd=self.repo, env=env,
            capture_output=True, text=True, encoding="utf-8",
        )

    def test_clean_staged_snapshot_passes(self) -> None:
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unstaged_broken_edit_does_not_block(self) -> None:
        self.write("wiki/甲頁.md", PAGE.format(title="甲頁", body="[[乙頁]] [[不存在]]"))
        result = self.run_hook()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_staged_broken_edit_blocks_even_if_worktree_fixed(self) -> None:
        self.write("wiki/甲頁.md", PAGE.format(title="甲頁", body="[[乙頁]] [[不存在]]"))
        self.git("add", "wiki/甲頁.md")
        self.write("wiki/甲頁.md", PAGE.format(title="甲頁", body="[[乙頁]]"))
        result = self.run_hook()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("DEADLINK:wiki/甲頁.md:不存在", result.stderr)

    def test_staged_index_drift_blocks(self) -> None:
        self.write("wiki/01.index.md", INDEX.replace("- [[乙頁]] — 說明", "- [[乙頁]] — 改寫"))
        self.git("add", "wiki/01.index.md")
        result = self.run_hook()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("INDEXDRIFT:wiki:乙頁.md", result.stderr)


if __name__ == "__main__":
    unittest.main()
