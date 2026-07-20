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


class LintScanTests(unittest.TestCase):
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
        is_wiki_content = (
            relative.startswith("wiki/") and Path(relative).name != "01.index.md"
        )
        wiki_metadata = ""
        if is_wiki_content:
            wiki_metadata = (
                "description: 說明測試頁面的核心概念、適用情境與相關知識連結，供自動化檢查使用\n"
            )
        parent = (
            'parent: "[[wiki/01.index]]"\n'
            if is_wiki_content else ""
        )
        self.write_text(
            relative,
            "---\n"
            f"title: {title}\n"
            f"{wiki_metadata}"
            "created: 2026-07-17\n"
            "updated: 2026-07-17\n"
            f"{parent}"
            "tags:\n"
            "  - test\n"
            "---\n\n"
            f"{body}\n",
        )

    def write_custom_note(self, relative: str, frontmatter: str, body: str = "") -> None:
        self.write_text(relative, f"---\n{frontmatter}---\n\n{body}\n")

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

    def test_wiki_description_and_parent_are_required(self) -> None:
        self.write_note("wiki/01.index.md", "索引", "[[缺欄頁]]")
        self.write_custom_note(
            "wiki/缺欄頁.md",
            "title: 缺欄頁\n"
            "created: 2026-07-17\n"
            "updated: 2026-07-17\n"
            "tags:\n"
            "  - test\n",
        )

        result = self.run_scan()

        self.assertIn("FM:wiki/缺欄頁.md:missing=description,parent", result.stdout)

    def test_wiki_description_length_is_30_to_80_unicode_characters(self) -> None:
        self.write_note("wiki/01.index.md", "索引", "[[過短頁]]\n[[過長頁]]")
        for filename, title, description in (
            ("過短頁.md", "過短頁", "短" * 29),
            ("過長頁.md", "過長頁", "長" * 81),
        ):
            self.write_custom_note(
                f"wiki/{filename}",
                f"title: {title}\n"
                f"description: {description}\n"
                "created: 2026-07-17\n"
                "updated: 2026-07-17\n"
                'parent: "[[wiki/01.index]]"\n'
                "tags:\n"
                "  - test\n",
            )

        result = self.run_scan()

        self.assertIn("FM:wiki/過短頁.md:description-length=29", result.stdout)
        self.assertIn("FM:wiki/過長頁.md:description-length=81", result.stdout)

    def test_quoted_30_character_description_is_valid(self) -> None:
        self.write_note("wiki/01.index.md", "索引", "[[有效頁]]")
        self.write_custom_note(
            "wiki/有效頁.md",
            "title: 有效頁\n"
            f'description: "{"合" * 30}"\n'
            "created: 2026-07-17\n"
            "updated: 2026-07-17\n"
            'parent: "[[wiki/01.index]]"\n'
            "tags:\n"
            "  - test\n",
        )

        result = self.run_scan()

        self.assertNotIn("FM:wiki/有效頁.md:", result.stdout)

    def test_invalid_parent_and_field_order_are_reported(self) -> None:
        self.write_note("wiki/01.index.md", "索引", "[[錯序頁]]")
        self.write_custom_note(
            "wiki/錯序頁.md",
            "title: 錯序頁\n"
            f"description: {'序' * 30}\n"
            "created: 2026-07-17\n"
            "updated: 2026-07-17\n"
            "tags:\n"
            "  - test\n"
            'parent: "[[01.index]]"\n',
        )

        result = self.run_scan()

        self.assertIn("FM:wiki/錯序頁.md:parent-invalid", result.stdout)
        self.assertIn("FM:wiki/錯序頁.md:field-order", result.stdout)

    def test_unquoted_parent_is_invalid_yaml_link_property(self) -> None:
        self.write_note("wiki/01.index.md", "索引", "[[未引號頁]]")
        self.write_custom_note(
            "wiki/未引號頁.md",
            "title: 未引號頁\n"
            f"description: {'引' * 30}\n"
            "created: 2026-07-17\n"
            "updated: 2026-07-17\n"
            "parent: [[wiki/01.index]]\n"
            "tags:\n"
            "  - test\n",
        )

        result = self.run_scan()

        self.assertIn("FM:wiki/未引號頁.md:parent-invalid", result.stdout)

    def test_wiki_draft_cannot_bypass_metadata_checks(self) -> None:
        self.write_note("wiki/01.index.md", "索引", "[[草稿頁]]")
        self.write_custom_note(
            "wiki/草稿頁.md",
            "title: 草稿頁\n"
            "created: 2026-07-17\n"
            "updated: 2026-07-17\n"
            "draft: true\n"
            "tags:\n"
            "  - test\n",
        )

        result = self.run_scan()

        self.assertIn("FM:wiki/草稿頁.md:missing=description,parent", result.stdout)

    def test_index_and_raw_skip_wiki_only_frontmatter_rules(self) -> None:
        self.write_custom_note(
            "wiki/01.index.md",
            "title: 索引\n"
            "created: 2026-07-17\n"
            "updated: 2026-07-17\n"
            "tags:\n"
            "  - test\n",
        )
        self.write_custom_note(
            "raw/source.md",
            "title: 來源\n"
            "tags:\n"
            "  - test\n"
            "created: 2026-07-17\n"
            "updated: 2026-07-17\n",
        )

        result = self.run_scan()

        self.assertNotIn("FM:wiki/01.index.md:", result.stdout)
        self.assertNotIn("FM:raw/source.md:", result.stdout)


if __name__ == "__main__":
    unittest.main()
