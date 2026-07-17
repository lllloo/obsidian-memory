from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DEFAULT_SCRIPT = ROOT / ".agents/skills/vault-lint/scripts/lint_scan.py"
SCRIPT = Path(os.environ.get("LINT_SCAN_SCRIPT", DEFAULT_SCRIPT))


class OrphanDetectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault = Path(self.temp_dir.name)
        self.write_text("schema/vault-map.md", "# 測試 vault\n")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_text(self, relative: str, content: str) -> None:
        path = self.vault / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def write_note(self, relative: str, title: str, body: str = "") -> None:
        self.write_text(
            relative,
            "---\n"
            f"title: {title}\n"
            "created: 2026-07-17\n"
            "updated: 2026-07-17\n"
            "tags:\n"
            "  - test\n"
            "---\n\n"
            f"{body}\n",
        )

    def run_scan(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--days", "0"],
            cwd=self.vault,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    def test_index_only_link_still_reports_orphan(self) -> None:
        self.write_note("wiki/01.index.md", "索引", "[[目標頁]]")
        self.write_note("wiki/目標頁.md", "目標頁")

        result = self.run_scan()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ORPHAN:wiki/目標頁.md", result.stdout)

    def test_raw_and_schema_links_do_not_hide_orphan(self) -> None:
        self.write_note("wiki/01.index.md", "索引", "[[目標頁]]")
        self.write_note("wiki/目標頁.md", "目標頁")
        self.write_note("raw/source.md", "來源", "[[目標頁]]")
        self.write_text("schema/rules.md", "[[目標頁]]\n")

        result = self.run_scan()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ORPHAN:wiki/目標頁.md", result.stdout)

    def test_self_link_does_not_clear_orphan(self) -> None:
        self.write_note("wiki/01.index.md", "索引", "[[目標頁]]")
        self.write_note("wiki/目標頁.md", "目標頁", "[[目標頁]]")

        result = self.run_scan()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ORPHAN:wiki/目標頁.md", result.stdout)

    def test_other_wiki_content_backlink_clears_orphan(self) -> None:
        self.write_note("wiki/01.index.md", "索引", "[[目標頁]]\n[[相關頁]]")
        self.write_note("wiki/目標頁.md", "目標頁", "[[相關頁]]")
        self.write_note("wiki/相關頁.md", "相關頁", "[[目標頁]]")

        result = self.run_scan()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("ORPHAN:wiki/目標頁.md", result.stdout)
        self.assertNotIn("ORPHAN:wiki/相關頁.md", result.stdout)
        self.assertIn("SUMMARY:orphan=0", result.stdout)


if __name__ == "__main__":
    unittest.main()
