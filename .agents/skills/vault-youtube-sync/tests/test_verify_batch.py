from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / ".agents/skills/vault-youtube-sync/scripts/verify_batch.py"
UPDATE_SCRIPT = ROOT / ".agents/skills/vault-youtube-sync/scripts/update_checkpoint.py"


class VerifyBatchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.notes_dir = Path(self.temp_dir.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write_note(self, filename: str, video_id: str, *, draft: bool = False) -> None:
        draft_line = "draft: true\n" if draft else ""
        (self.notes_dir / filename).write_text(
            "---\n"
            f"source: https://www.youtube.com/watch?v={video_id}\n"
            f"{draft_line}"
            "---\n",
            encoding="utf-8",
        )

    def run_verify(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", str(SCRIPT), str(self.notes_dir), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    def write_index(self) -> tuple[Path, str]:
        original = (
            "---\n"
            "title: 測試頻道\n"
            "updated: 2026-07-16\n"
            "last_sync_id: old123\n"
            "---\n"
        )
        path = self.notes_dir / "01.index.md"
        path.write_text(original, encoding="utf-8")
        return path, original

    def run_update(
        self, index: Path, *args: str, new_id: str = "new123"
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(UPDATE_SCRIPT),
                str(index),
                "2026-07-17",
                f"--new-id={new_id}",
                *args,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    def test_all_terminal_states_allow_checkpoint(self) -> None:
        self.write_note("完整.md", "complete123")
        result = self.run_verify(
            "--expected", "complete123",
            "--expected", "filtered123",
            "--expected", "unavailable123",
            "--filtered", "filtered123",
            "--unavailable", "unavailable123",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VERIFY:ready", result.stdout)

    def test_missing_subagent_output_blocks_checkpoint(self) -> None:
        result = self.run_verify("--expected", "missing123")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MISSING:missing123", result.stdout)
        self.assertIn("VERIFY:blocked", result.stdout)

    def test_draft_blocks_checkpoint(self) -> None:
        self.write_note("待重試.md", "draft123", draft=True)
        result = self.run_verify("--expected", "draft123")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("RESULT:draft123:draft:", result.stdout)

    def test_filename_collision_is_caught_as_missing_video(self) -> None:
        # 模擬兩支影片選到同一檔名，後寫入者覆蓋前者：磁碟只剩第二支。
        self.write_note("同名.md", "second123")
        result = self.run_verify(
            "--expected", "first123", "--expected", "second123"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MISSING:first123", result.stdout)

    def test_duplicate_source_blocks_checkpoint(self) -> None:
        self.write_note("重複一.md", "duplicate123")
        self.write_note("重複二.md", "duplicate123")
        result = self.run_verify("--expected", "duplicate123")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DUPLICATE:duplicate123:", result.stdout)

    def test_unrelated_old_draft_still_blocks_checkpoint(self) -> None:
        self.write_note("完整.md", "complete123")
        self.write_note("舊草稿.md", "oldDraft123", draft=True)
        result = self.run_verify("--expected", "complete123")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("EXTRA_DRAFT:oldDraft123", result.stdout)

    def test_updater_keeps_checkpoint_when_expected_video_is_missing(self) -> None:
        index, original = self.write_index()
        result = self.run_update(index, "--expected", "new123")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MISSING:new123", result.stdout)
        self.assertIn("VERIFY:blocked", result.stdout)
        self.assertEqual(index.read_text(encoding="utf-8"), original)

    def test_updater_writes_only_after_embedded_verification_passes(self) -> None:
        index, _ = self.write_index()
        self.write_note("新影片.md", "new123")
        result = self.run_update(
            index,
            "--expected=new123",
            "--expected=filtered123",
            "--expected=unavailable123",
            "--filtered=filtered123",
            "--unavailable=unavailable123",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VERIFY:ready", result.stdout)
        self.assertIn("RESULT:filtered123:filtered:-", result.stdout)
        self.assertIn("RESULT:unavailable123:unavailable:-", result.stdout)
        self.assertIn("OK:", result.stdout)
        updated = index.read_text(encoding="utf-8")
        self.assertIn("last_sync_id: new123", updated)
        self.assertIn("updated: 2026-07-17", updated)

    def test_legacy_updater_call_cannot_bypass_verification(self) -> None:
        index, original = self.write_index()
        self.write_note("新影片.md", "new123")
        result = subprocess.run(
            [
                sys.executable,
                "-B",
                str(UPDATE_SCRIPT),
                str(index),
                "new123",
                "2026-07-17",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(index.read_text(encoding="utf-8"), original)

    def test_retry_only_batch_verifies_then_keeps_index_byte_for_byte(self) -> None:
        index, original = self.write_index()
        self.write_note("重試完成.md", "retry123")
        result = self.run_update(
            index, "--expected=retry123", new_id="old123"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VERIFY:ready", result.stdout)
        self.assertIn("NOOP:", result.stdout)
        self.assertEqual(index.read_text(encoding="utf-8"), original)

    def test_leading_hyphen_video_id_is_supported(self) -> None:
        index, _ = self.write_index()
        self.write_note("特殊ID.md", "-leading123")
        result = self.run_update(
            index, "--expected=-leading123", new_id="-leading123"
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VERIFY:ready", result.stdout)
        self.assertIn("last_sync_id: -leading123", index.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
