"""
Fetch high-trust developer tooling updates for vault-updates-sync.

Inputs:
    python fetch_updates.py --since YYYY-MM-DD --repo openai/codex --repo anthropics/claude-code [--starred]

Outputs:
    META:since|||<YYYY-MM-DD>
    OFFICIAL:<name>|||<url>|||<tag>
    CHANGELOG:<source>|||<published>|||<title>|||<url>
    RELEASE:<repo>|||<published>|||<tag>|||<name>|||<url>
    ERROR:<source>:<message>

This script intentionally keeps the first pass mechanical. The skill/analyzer
does the semantic high-precision filtering before writing notes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ObsidianVaultBot/1.0)",
    "Accept": "application/vnd.github+json, application/json;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

DEFAULT_REPOS = ["openai/codex", "anthropics/claude-code"]
OFFICIAL_SOURCES = [
    ("OpenAI Codex", "https://help.openai.com/en/articles/11428266-codex-changelog", "codex"),
    ("Claude Code", "https://code.claude.com/docs/en/changelog", "claude-code"),
    ("GitHub Changelog", "https://github.blog/changelog/feed/", "copilot"),
    ("Cursor Changelog", "https://www.cursor.com/changelog", "cursor"),
]
CHANGELOG_KEYWORDS = [
    "agent",
    "agents",
    "anthropic",
    "claude",
    "code review",
    "codex",
    "copilot",
    "cursor",
    "gpt",
    "mcp",
    "model",
    "openai",
]
RETRY_BACKOFF_SECONDS = [3, 8, 20]


def _sanitize(value: object) -> str:
    if value is None:
        return ""
    return str(value).replace("|||", " ").replace("\n", " ").replace("\r", "").strip()


def _parse_date(value: str) -> dt.datetime:
    return dt.datetime.strptime(value, "%Y-%m-%d").replace(tzinfo=dt.timezone.utc)


def _parse_iso(value: str) -> dt.datetime | None:
    if not value:
        return None
    try:
        normalized = value.replace("Z", "+00:00")
        parsed = dt.datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except ValueError:
        return None


def _parse_rss_date(value: str) -> dt.datetime | None:
    if not value:
        return None
    try:
        parsed = email.utils.parsedate_to_datetime(value)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except (TypeError, ValueError):
        return None


def request_text(url: str) -> str:
    # For GitHub API URLs, prefer `gh api` (handles auth automatically)
    gh = shutil.which("gh")
    if gh and "api.github.com" in url:
        path = url.replace("https://api.github.com", "")
        try:
            proc = subprocess.run(
                [gh, "api", path],
                check=True, capture_output=True, text=True, timeout=25,
            )
            return proc.stdout
        except subprocess.CalledProcessError as e:
            stderr = (e.stderr or "").strip()
            # gh exit 1 with "Not Found" or 4xx — don't retry
            if e.returncode in (1, 4) or "Not Found" in stderr or "HTTP 4" in stderr:
                raise RuntimeError(stderr or f"gh exit {e.returncode}")
            # fall through to curl/urllib on other errors
        except Exception:  # noqa: BLE001
            pass  # fall through

    headers = dict(HEADERS)
    token = os.environ.get("GITHUB_TOKEN")
    if token and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {token}"

    curl = shutil.which("curl")
    last_error: Exception | None = None
    for attempt in range(len(RETRY_BACKOFF_SECONDS) + 1):
        try:
            if curl:
                cmd = [
                    curl, "-sS", "--fail", "-L",
                    "-H", f"User-Agent: {headers['User-Agent']}",
                    "-H", f"Accept: {headers['Accept']}",
                    "-H", f"Accept-Language: {headers['Accept-Language']}",
                ]
                if "Authorization" in headers:
                    cmd += ["-H", f"Authorization: {headers['Authorization']}"]
                cmd.append(url)
                proc = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=25)
                return proc.stdout
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=25) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except subprocess.CalledProcessError as e:
            if e.returncode == 22:
                raise RuntimeError((e.stderr or "").strip() or "HTTP error (4xx)")
            last_error = RuntimeError((e.stderr or "").strip() or f"curl exit {e.returncode}")
        except urllib.error.HTTPError as e:
            if e.code < 500:
                raise RuntimeError(f"HTTP {e.code}")
            last_error = RuntimeError(f"HTTP {e.code}")
        except Exception as exc:  # noqa: BLE001
            last_error = exc
        if attempt >= len(RETRY_BACKOFF_SECONDS):
            break
        time.sleep(RETRY_BACKOFF_SECONDS[attempt])
    raise RuntimeError(str(last_error or "unknown request error"))


def request_json(url: str) -> object:
    return json.loads(request_text(url))


def fetch_starred_releases(since: dt.datetime, skip_repos: set[str]) -> None:
    """Fetch releases from all starred repos in a single GraphQL call."""
    gh = shutil.which("gh")
    if not gh:
        print("ERROR:starred:gh CLI not found; skipping starred repos")
        return

    query = """
query {
  viewer {
    starredRepositories(first: 100) {
      nodes {
        nameWithOwner
        releases(first: 5, orderBy: {field: CREATED_AT, direction: DESC}) {
          nodes {
            name
            tagName
            publishedAt
            url
          }
        }
      }
    }
  }
}
"""
    try:
        proc = subprocess.run(
            [gh, "api", "graphql", "-f", f"query={query}"],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        payload = json.loads(proc.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ERROR:starred:{(e.stderr or '').strip() or f'gh exit {e.returncode}'}")
        return
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR:starred:{exc}")
        return

    repos = (
        payload.get("data", {})
        .get("viewer", {})
        .get("starredRepositories", {})
        .get("nodes", [])
    )
    for repo in repos:
        name_with_owner = _sanitize(repo.get("nameWithOwner"))
        if name_with_owner in skip_repos:
            continue
        for release in repo.get("releases", {}).get("nodes", []):
            published = _parse_iso(str(release.get("publishedAt") or ""))
            if not published or published < since:
                continue
            tag = _sanitize(release.get("tagName"))
            rname = _sanitize(release.get("name") or tag)
            url = _sanitize(release.get("url"))
            print(f"RELEASE:{name_with_owner}|||{published.isoformat()}|||{tag}|||{rname}|||{url}")


def fetch_releases(repo: str, since: dt.datetime) -> None:
    for line in _fetch_releases_lines(repo, since):
        print(line)


def _fetch_releases_lines(repo: str, since: dt.datetime) -> list[str]:
    """Return RELEASE/ERROR lines for a repo without printing (thread-safe)."""
    url = f"https://api.github.com/repos/{repo}/releases?per_page=30"
    try:
        data = request_json(url)
    except RuntimeError as exc:
        return [f"ERROR:releases:{repo}:{exc}"]

    if not isinstance(data, list):
        return [f"ERROR:releases:{repo}:unexpected response"]

    lines = []
    for item in data:
        if not isinstance(item, dict):
            continue
        published = _parse_iso(str(item.get("published_at") or ""))
        if not published or published < since:
            continue
        tag = _sanitize(item.get("tag_name"))
        name = _sanitize(item.get("name") or tag)
        html_url = _sanitize(item.get("html_url"))
        lines.append(f"RELEASE:{repo}|||{published.isoformat()}|||{tag}|||{name}|||{html_url}")
    return lines




def fetch_github_changelog(since: dt.datetime) -> None:
    url = "https://github.blog/changelog/feed/"
    try:
        text = request_text(url)
        root = ET.fromstring(text)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR:GitHub Changelog:{exc}")
        return

    for item in root.findall(".//item"):
        title = _sanitize(item.findtext("title"))
        link = _sanitize(item.findtext("link"))
        published = _parse_rss_date(item.findtext("pubDate") or "")
        if not published or published < since:
            continue
        haystack = title.lower()
        if not any(keyword in haystack for keyword in CHANGELOG_KEYWORDS):
            continue
        print(f"CHANGELOG:GitHub Changelog|||{published.isoformat()}|||{title}|||{link}")


def fetch_discussions_with_gh(repo: str, since: dt.datetime) -> None:
    gh = shutil.which("gh")
    if not gh:
        return
    owner, name = repo.split("/", 1)
    query = """
query($owner:String!, $name:String!) {
  repository(owner:$owner, name:$name) {
    discussions(first: 20, orderBy: {field: UPDATED_AT, direction: DESC}) {
      nodes {
        title
        updatedAt
        url
        comments { totalCount }
      }
    }
  }
}
"""
    try:
        proc = subprocess.run(
            [
                gh,
                "api",
                "graphql",
                "-f",
                f"owner={owner}",
                "-f",
                f"name={name}",
                "-f",
                f"query={query}",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=25,
        )
        payload = json.loads(proc.stdout)
    except subprocess.CalledProcessError as e:
        print(f"ERROR:discussions:{repo}:{(e.stderr or '').strip() or f'gh exit {e.returncode}'}")
        return
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR:discussions:{repo}:{exc}")
        return

    nodes = (
        payload.get("data", {})
        .get("repository", {})
        .get("discussions", {})
        .get("nodes", [])
    )
    for item in nodes:
        updated = _parse_iso(str(item.get("updatedAt") or ""))
        if not updated or updated < since:
            continue
        title = _sanitize(item.get("title"))
        url = _sanitize(item.get("url"))
        comments = int(item.get("comments", {}).get("totalCount") or 0)
        print(f"DISCUSSION:{repo}|||{updated.isoformat()}|||{comments}|||{title}|||{url}")


def main() -> int:
    default_since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7)).date().isoformat()
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", default=default_since, help="YYYY-MM-DD, default: 7 days ago")
    parser.add_argument("--repo", action="append", default=[], help="GitHub repo owner/name; repeatable")
    parser.add_argument("--starred", action="store_true", help="also fetch releases from all starred repos")
    args = parser.parse_args()

    try:
        since = _parse_date(args.since)
    except ValueError:
        print(f"ERROR:usage:invalid --since date {args.since!r}; expected YYYY-MM-DD")
        return 1

    explicit_repos = args.repo or DEFAULT_REPOS
    print(f"META:since|||{since.date().isoformat()}")
    for name, url, tag in OFFICIAL_SOURCES:
        print(f"OFFICIAL:{name}|||{url}|||{tag}")

    fetch_github_changelog(since)

    if args.starred:
        # Single GraphQL call covers all starred repos (includes explicit repos if starred).
        # Discussions only for explicitly listed repos.
        fetch_starred_releases(since, skip_repos=set())
        for repo in explicit_repos:
            if not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", repo):
                print(f"ERROR:repo:{repo}:invalid owner/name")
                continue
            fetch_discussions_with_gh(repo, since)
    else:
        # No starred flag: use REST for explicit repos only
        for repo in explicit_repos:
            if not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", repo):
                print(f"ERROR:repo:{repo}:invalid owner/name")
                continue
            fetch_releases(repo, since)
            fetch_discussions_with_gh(repo, since)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
