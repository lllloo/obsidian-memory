from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / ".agents/skills/vault-watch/scripts/watch.py"

_spec = importlib.util.spec_from_file_location("watch", SCRIPT)
watch = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(watch)


BOARD = """---
title: Watch Board
---

| Issue | 追蹤重點 | 狀態 |
|---|---|---|
| [owner/repo#1](https://github.com/owner/repo/issues/1) | 只認官方回應的一般項 | open |
| [owner/repo#2](https://github.com/owner/repo/issues/2) | 冷門項，關鍵訊號來自社群 `[全留言]` | open |
| [owner/repo#1](https://github.com/owner/repo/issues/1) | 重複列，應被去重 | open |
"""


class ParseRefsScopeTests(unittest.TestCase):
    """parse_refs 逐列判定留言採計範圍：預設 official，列尾標 [全留言] 者為 all。"""

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.board = Path(self.temp_dir.name) / "01.index.md"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def parse(self, text: str):
        self.board.write_text(text, encoding="utf-8")
        return watch.parse_refs(self.board)

    def test_scope_defaults_to_official_and_tag_opts_in(self) -> None:
        refs = self.parse(BOARD)
        self.assertEqual(
            refs,
            [
                ("owner/repo", "1", "owner/repo#1", "official"),
                ("owner/repo", "2", "owner/repo#2", "all"),
            ],
        )

    def test_tag_does_not_leak_to_other_lines(self) -> None:
        text = (
            "| [a/b#1](u) | 標了全留言 `[全留言]` | open |\n"
            "| [a/b#2](u) | 沒標 | open |\n"
        )
        scopes = {ref: scope for _, _, ref, scope in self.parse(text)}
        self.assertEqual(scopes, {"a/b#1": "all", "a/b#2": "official"})


class CommentScopeFilterTests(unittest.TestCase):
    """fetch_one 依 scope 決定採計哪些留言；社群留言只在 scope="all" 時成為訊號。"""

    ISSUE = {"state": "open", "labels": [], "title": "t"}
    PREV = {"state": "open", "labels": [], "title": "t", "checked_ts": "2026-08-01T00:00:00Z"}
    COMMUNITY = {
        "id": 10,
        "author_association": "NONE",
        "created_at": "2026-08-05T00:00:00Z",
        "user": {"login": "someone"},
        "body": "根因複現：wl-paste 回 image/bmp",
    }
    MAINTAINER = {
        "id": 11,
        "author_association": "MEMBER",
        "created_at": "2026-08-05T01:00:00Z",
        "user": {"login": "dev"},
        "body": "修了",
    }

    def fetch(self, comments, scope):
        def fake_gh_api(path, paginate=False):
            return (comments, None) if "/comments" in path else (dict(self.ISSUE), None)

        original = watch.gh_api
        watch.gh_api = fake_gh_api
        try:
            return watch.fetch_one("owner/repo", "1", dict(self.PREV), scope)
        finally:
            watch.gh_api = original

    def test_official_scope_ignores_community_comment(self) -> None:
        _, deltas, err = self.fetch([self.COMMUNITY], "official")
        self.assertIsNone(err)
        self.assertEqual(deltas, [])

    def test_all_scope_reports_community_comment_with_association(self) -> None:
        _, deltas, err = self.fetch([self.COMMUNITY], "all")
        self.assertIsNone(err)
        self.assertEqual(len(deltas), 1)
        kind, detail = deltas[0]
        self.assertEqual(kind, "official")
        # runbook 依 <assoc> 決定寫「官方已回應」還是「社群有新回應」，故欄位必須帶得出來。
        self.assertEqual(detail.split("|")[:3], ["someone", "NONE", "2026-08-05"])

    def test_official_scope_still_reports_maintainer_comment(self) -> None:
        _, deltas, err = self.fetch([self.COMMUNITY, self.MAINTAINER], "official")
        self.assertIsNone(err)
        self.assertEqual(len(deltas), 1)
        self.assertEqual(deltas[0][1].split("|")[:3], ["dev", "MEMBER", "2026-08-05"])


if __name__ == "__main__":
    unittest.main()
