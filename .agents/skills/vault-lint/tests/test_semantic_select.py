from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DEFAULT_SCRIPT = ROOT / ".agents/skills/vault-lint/scripts/semantic_select.py"
SCRIPT = Path(os.environ.get("SEMANTIC_SELECTOR_SCRIPT", DEFAULT_SCRIPT))


def load_selector():
    spec = importlib.util.spec_from_file_location("semantic_select_under_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"無法載入 selector：{SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SemanticSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.selector = load_selector()

    def test_twenty_pages_are_covered_in_two_days_without_repeating(self) -> None:
        pages = [f"wiki/{index:02d}.md" for index in range(20)]
        first_day = date(2026, 7, 18)

        first, _, _, batches = self.selector.select_daily_batch(pages, 10, first_day)
        second, _, _, _ = self.selector.select_daily_batch(
            pages, 10, first_day + timedelta(days=1)
        )

        self.assertEqual(batches, 2)
        self.assertEqual(len(first), 10)
        self.assertEqual(len(second), 10)
        self.assertTrue(set(first).isdisjoint(second))
        self.assertEqual(set(first) | set(second), set(pages))

    def test_same_day_is_stable_and_does_not_mutate_input(self) -> None:
        pages = [f"wiki/{index:02d}.md" for index in range(17)]
        original = list(pages)
        on_date = date(2026, 7, 18)

        first = self.selector.select_daily_batch(pages, 6, on_date)
        second = self.selector.select_daily_batch(pages, 6, on_date)

        self.assertEqual(first, second)
        self.assertEqual(pages, original)

    def test_at_or_below_cap_selects_every_page(self) -> None:
        on_date = date(2026, 7, 18)
        for count in (5, 10):
            pages = [f"wiki/{index:02d}.md" for index in range(count)]

            selected, deferred, batch_index, batch_count = (
                self.selector.select_daily_batch(pages, 10, on_date)
            )

            self.assertEqual(selected, pages)
            self.assertEqual(deferred, [])
            self.assertEqual(batch_index, 0)
            self.assertEqual(batch_count, 1)

    def test_new_page_is_selected_within_the_new_batch_cycle(self) -> None:
        original_pages = [f"wiki/{index:02d}.md" for index in range(20)]
        first_day = date(2026, 7, 18)
        first_selected, _, _, _ = self.selector.select_daily_batch(
            original_pages, 10, first_day
        )
        pages = ["wiki/new.md"] + original_pages
        reviewed: set[str] = set()

        for offset in range(1, 4):
            selected, _, _, batches = self.selector.select_daily_batch(
                pages, 10, first_day + timedelta(days=offset)
            )
            reviewed.update(selected)

        self.assertEqual(len(first_selected), 10)
        self.assertEqual(batches, 3)
        self.assertEqual(reviewed, set(pages))
        self.assertIn("wiki/new.md", reviewed)

    def test_git_discovery_uses_latest_change_order_and_excludes_non_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            self.init_repo(vault)
            self.write(vault, "wiki/A.md", "A\n")
            self.write(vault, "wiki/B.md", "B\n")
            self.write(vault, "wiki/C.md", "C\n")
            self.write(vault, "wiki/01.index.md", "index\n")
            self.commit(vault, "初始頁面", "2026-07-16T08:00:00+08:00")

            self.write(vault, "wiki/B.md", "B2\n")
            (vault / "wiki/C.md").unlink()
            self.commit(vault, "更新 B 並刪除 C", "2026-07-17T08:00:00+08:00")

            pages = self.selector.discover_changed_pages(
                vault, 3650, date(2026, 7, 18), "+08:00"
            )

            self.assertEqual(pages, ["wiki/B.md", "wiki/A.md"])

    def test_calendar_window_is_replayable_and_index_exclusion_is_exact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            self.init_repo(vault)
            self.write(vault, "wiki/before.md", "before\n")
            self.commit(vault, "窗口前", "2026-07-11T23:59:59+08:00")
            self.write(vault, "wiki/start.md", "start\n")
            self.commit(vault, "窗口起點", "2026-07-12T00:00:00+08:00")
            self.write(vault, "wiki/foo01.index.md", "content\n")
            self.write(vault, "wiki/01.index.md", "index\n")
            self.commit(vault, "窗口終點", "2026-07-18T23:59:59+08:00")
            self.write(vault, "wiki/after.md", "after\n")
            self.commit(vault, "窗口後", "2026-07-19T00:00:00+08:00")

            pages = self.selector.discover_changed_pages(
                vault, 7, date(2026, 7, 18), "+08:00"
            )

            self.assertEqual(pages, ["wiki/foo01.index.md", "wiki/start.md"])
            self.assertNotIn("wiki/01.index.md", pages)
            self.assertNotIn("wiki/before.md", pages)
            self.assertNotIn("wiki/after.md", pages)

    def test_cli_is_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            self.init_repo(vault)
            for index in range(12):
                self.write(vault, f"wiki/{index:02d}.md", f"{index}\n")
            self.commit(vault, "建立測試頁", "2026-07-17T08:00:00+08:00")
            before = self.git_status(vault)

            command = [
                sys.executable,
                "-B",
                str(SCRIPT),
                "--root",
                str(vault),
                "--days",
                "3650",
                "--cap",
                "10",
                "--date",
                "2026-07-18",
                "--utc-offset",
                "+08:00",
            ]
            first_env = os.environ.copy()
            first_env["PYTHONHASHSEED"] = "1"
            second_env = os.environ.copy()
            second_env["PYTHONHASHSEED"] = "2"
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=first_env,
            )
            repeated = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                env=second_env,
            )
            after = self.git_status(vault)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(repeated.returncode, 0, repeated.stdout + repeated.stderr)
            self.assertIn("SUMMARY:semantic=", result.stdout)
            self.assertIn("SELECT:complete", result.stdout)
            self.assertEqual(result.stdout, repeated.stdout)
            self.assertEqual(before, "")
            self.assertEqual(after, "")

    def test_cli_fails_closed_when_git_is_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            vault = Path(temp_dir)
            self.write(vault, "schema/vault-map.md", "# 測試 vault\n")

            result = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(SCRIPT),
                    "--root",
                    str(vault),
                    "--date",
                    "2026-07-18",
                    "--utc-offset",
                    "+08:00",
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn("ERROR:semantic-select", result.stdout)
            self.assertNotIn("SELECT:complete", result.stdout)

    def init_repo(self, vault: Path) -> None:
        self.write(vault, "schema/vault-map.md", "# 測試 vault\n")
        subprocess.run(["git", "init", "-q"], cwd=vault, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Vault Lint Test"], cwd=vault, check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "vault-lint@example.invalid"],
            cwd=vault,
            check=True,
        )

    def write(self, vault: Path, relative: str, content: str) -> None:
        path = vault / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self, vault: Path, message: str, commit_date: str) -> None:
        env = os.environ.copy()
        env["GIT_AUTHOR_DATE"] = commit_date
        env["GIT_COMMITTER_DATE"] = commit_date
        subprocess.run(["git", "add", "-A"], cwd=vault, check=True, env=env)
        subprocess.run(
            ["git", "commit", "-q", "-m", message], cwd=vault, check=True, env=env
        )

    def git_status(self, vault: Path) -> str:
        return subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=vault,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout


if __name__ == "__main__":
    unittest.main()
