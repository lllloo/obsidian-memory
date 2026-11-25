from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DEFAULT_SCRIPT = ROOT / ".agents/skills/vault-lint/scripts/semantic_select.py"
SCRIPT = Path(os.environ.get("SEMANTIC_SELECTOR_SCRIPT", DEFAULT_SCRIPT))


class SemanticSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.vault = Path(self.temp_dir.name)
        self.write("schema/vault-map.md", "# 測試 vault\n")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_without_review_commit_covers_all_history_newest_first(self) -> None:
        self.init_repo()
        self.write("wiki/A.md", "A\n")
        self.write("wiki/B.md", "B\n")
        self.write("wiki/C.md", "C\n")
        self.write("wiki/01.index.md", "index\n")
        self.write("wiki/foo01.index.md", "content\n")
        self.commit("初始頁面")
        self.write("wiki/B.md", "B2\n")
        (self.vault / "wiki/C.md").unlink()
        self.commit("更新 B 並刪除 C")

        result = self.run_select()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(
            self.semantic(result),
            ["wiki/B.md", "wiki/A.md", "wiki/foo01.index.md"],
        )
        self.assertIn("SUMMARY:since=none", result.stdout)

    def test_window_starts_after_last_review_commit(self) -> None:
        self.init_repo()
        self.write("wiki/舊.md", "old\n")
        self.commit("回存：舊頁")
        self.write("wiki/修補.md", "fixed during review\n")
        self.commit("健檢：修補一頁")
        self.write("wiki/新.md", "new\n")
        self.commit("回存：新頁")
        self.write("wiki/又新.md", "newer\n")
        self.commit("回存：健檢：不在標題開頭不算")

        result = self.run_select()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.semantic(result), ["wiki/又新.md", "wiki/新.md"])

    def test_empty_review_commit_resets_window(self) -> None:
        self.init_repo()
        self.write("wiki/A.md", "A\n")
        self.commit("回存：A")
        subprocess.run(
            ["git", "commit", "-q", "--allow-empty", "-m", "健檢：無發現"],
            cwd=self.vault, check=True,
        )

        result = self.run_select()

        self.assertEqual(self.semantic(result), [])
        self.assertIn("SUMMARY:semantic=0", result.stdout)
        self.assertIn("SELECT:complete", result.stdout)

    def test_cli_is_read_only(self) -> None:
        self.init_repo()
        for index in range(12):
            self.write(f"wiki/{index:02d}.md", f"{index}\n")
        self.commit("建立測試頁")

        result = self.run_select()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(len(self.semantic(result)), 12)
        self.assertEqual(self.git_status(), "")

    def test_cli_fails_closed_when_git_is_unavailable(self) -> None:
        result = self.run_select()

        self.assertEqual(result.returncode, 1)
        self.assertIn("ERROR:semantic-select", result.stdout)
        self.assertNotIn("SELECT:complete", result.stdout)

    def run_select(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), "--root", str(self.vault)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )

    def semantic(self, result: subprocess.CompletedProcess[str]) -> list[str]:
        return [
            line.removeprefix("SEMANTIC:")
            for line in result.stdout.splitlines() if line.startswith("SEMANTIC:")
        ]

    def init_repo(self) -> None:
        subprocess.run(["git", "init", "-q"], cwd=self.vault, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Vault Lint Test"], cwd=self.vault, check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "vault-lint@example.invalid"],
            cwd=self.vault, check=True,
        )

    def write(self, relative: str, content: str) -> None:
        path = self.vault / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def commit(self, message: str) -> None:
        subprocess.run(["git", "add", "-A"], cwd=self.vault, check=True)
        subprocess.run(["git", "commit", "-q", "-m", message], cwd=self.vault, check=True)

    def git_status(self) -> str:
        return subprocess.run(
            ["git", "status", "--porcelain"], cwd=self.vault, check=True,
            capture_output=True, text=True, encoding="utf-8",
        ).stdout


if __name__ == "__main__":
    unittest.main()
