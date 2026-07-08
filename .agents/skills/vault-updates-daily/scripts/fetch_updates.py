"""
Fetch high-trust developer tooling updates for vault-updates-daily.

Usage (cwd = repo root):

    # 一般用法：自動讀 raw/Updates/01.index.md
    python3 .agents/skills/vault-updates-daily/scripts/fetch_updates.py

    # 指定日期範圍
    python3 .agents/skills/vault-updates-daily/scripts/fetch_updates.py --since YYYY-MM-DD

    # 進階：手動傳入來源（略過 01.index.md）
    python3 .agents/skills/vault-updates-daily/scripts/fetch_updates.py \
        --official "OpenAI Codex|https://developers.openai.com/codex/changelog|codex" \
        --repo openai/codex [--starred]

Sources come from raw/Updates/01.index.md by default.
When no --official / --repo / --starred flags are given, the script parses the index automatically.

Outputs:
    META:since|||<YYYY-MM-DD>
    META:starred|||live|||<n> repos            (authed: live viewer query, snapshot refreshed)
    META:starred|||snapshot|||<date>|||<n> repos  (no auth: fell back to snapshot + atom feed)
    OFFICIAL:<name>|||<url>|||<tag>
    CHANGELOG:<source>|||<published>|||<title>|||<url>|||<body-snippet>
    RELEASE:<repo>|||<published>|||<tag>|||<name>|||<url>|||<body-snippet>
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
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ObsidianVaultBot/1.0)",
    "Accept": "application/vnd.github+json, application/json;q=0.9, */*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

_GITHUB_RSS_URL = "https://github.blog/changelog/feed/"
_ATOM_NS = {"a": "http://www.w3.org/2005/Atom"}
DEFAULT_SNAPSHOT = ".agents/skills/vault-updates-daily/starred-repos.txt"
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


def _sanitize_body(text: str, max_chars: int = 800) -> str:
    """Strip markdown/HTML noise, collapse whitespace, truncate."""
    if not text:
        return ""
    plain = re.sub(r'<[^>]+>', ' ', text)          # strip HTML tags
    plain = re.sub(r'!\[.*?\]\(.*?\)', '', plain)   # strip image embeds
    plain = re.sub(r'\s+', ' ', plain).strip()
    return _sanitize(plain[:max_chars])


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
                check=True, capture_output=True, text=True,
                encoding="utf-8", errors="replace", timeout=25,
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
                # 不用 --fail：curl 對 4xx/5xx 一律 exit 22 無法區分，改由 -w 取
                # http_code 自行判斷（4xx 不重試、5xx 退避重試，與 urllib 分支一致）。
                cmd = [
                    curl, "-sS", "-L", "-w", "\n%{http_code}",
                    "-H", f"User-Agent: {headers['User-Agent']}",
                    "-H", f"Accept: {headers['Accept']}",
                    "-H", f"Accept-Language: {headers['Accept-Language']}",
                ]
                if "Authorization" in headers:
                    cmd += ["-H", f"Authorization: {headers['Authorization']}"]
                cmd.append(url)
                proc = subprocess.run(cmd, check=True, capture_output=True, text=True,
                                      encoding="utf-8", errors="replace", timeout=25)
                body, _, code_s = proc.stdout.rpartition("\n")
                code = int(code_s.strip() or 0)
                if 200 <= code < 400:
                    return body
                if code < 500:
                    raise RuntimeError(f"HTTP {code}")
                last_error = RuntimeError(f"HTTP {code}")
            else:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=25) as resp:
                    return resp.read().decode("utf-8", errors="replace")
        except RuntimeError:
            raise  # 4xx：不重試，直接回報
        except subprocess.CalledProcessError as e:
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


GRAPHQL_URL = "https://api.github.com/graphql"


def _graphql_post(token: str, payload: str) -> str:
    """POST GraphQL payload via curl/urllib，沿用 request_text 的重試策略
    （4xx 不重試、5xx/網路錯誤退避重試）。"""
    curl = shutil.which("curl")
    last_error: Exception | None = None
    for attempt in range(len(RETRY_BACKOFF_SECONDS) + 1):
        try:
            if curl:
                proc = subprocess.run(
                    [curl, "-sS", "-L", "-X", "POST", "-w", "\n%{http_code}",
                     "-H", f"Authorization: Bearer {token}",
                     "-H", "Content-Type: application/json",
                     "-H", f"User-Agent: {HEADERS['User-Agent']}",
                     "-d", "@-", GRAPHQL_URL],
                    input=payload, check=True, capture_output=True, text=True,
                    encoding="utf-8", errors="replace", timeout=30,
                )
                body, _, code_s = proc.stdout.rpartition("\n")
                code = int(code_s.strip() or 0)
                if 200 <= code < 400:
                    return body
                if code < 500:
                    raise RuntimeError(f"HTTP {code}")
                last_error = RuntimeError(f"HTTP {code}")
            else:
                req = urllib.request.Request(
                    GRAPHQL_URL,
                    data=payload.encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                        "User-Agent": HEADERS["User-Agent"],
                    },
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=30) as resp:
                    return resp.read().decode("utf-8", errors="replace")
        except RuntimeError:
            raise  # 4xx：不重試，直接回報
        except subprocess.CalledProcessError as e:
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


def graphql_query(query: str, variables: dict[str, str] | None = None) -> dict:
    """Call GitHub GraphQL. Prefers `gh api graphql` (auth handled by gh);
    falls back to curl/urllib POST with GITHUB_TOKEN/GH_TOKEN when gh is
    absent **or fails**（未登入、額度用盡、暫時性錯誤都落 token fallback）.

    Raises RuntimeError (no auth route / HTTP / GraphQL errors).
    """
    variables = variables or {}
    body: str | None = None
    gh_error: str | None = None
    gh = shutil.which("gh")
    if gh:
        cmd = [gh, "api", "graphql"]
        for key, value in variables.items():
            cmd += ["-f", f"{key}={value}"]
        cmd += ["-f", f"query={query}"]
        try:
            proc = subprocess.run(cmd, check=True, capture_output=True, text=True,
                                  encoding="utf-8", errors="replace", timeout=30)
            body = proc.stdout
        except subprocess.CalledProcessError as e:
            gh_error = (e.stderr or "").strip() or f"gh exit {e.returncode}"
        except Exception as exc:  # noqa: BLE001
            gh_error = str(exc)
    if body is None:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            if gh_error is not None:
                raise RuntimeError(f"gh failed ({gh_error}) and no GITHUB_TOKEN/GH_TOKEN fallback")
            raise RuntimeError("gh CLI not found and no GITHUB_TOKEN/GH_TOKEN set")
        payload = json.dumps({"query": query, "variables": variables})
        body = _graphql_post(token, payload)

    result = json.loads(body)
    if isinstance(result, dict) and result.get("errors"):
        errors = result["errors"]
        if isinstance(errors, list):
            message = "; ".join(str(e.get("message", e)) for e in errors[:3] if isinstance(e, (dict, str)))
        else:
            message = str(errors)
        raise RuntimeError(message or "GraphQL error")
    return result if isinstance(result, dict) else {}


_STARRED_QUERY = """
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
            description
          }
        }
      }
    }
  }
}
"""


def read_snapshot(path: str) -> tuple[list[str], str | None]:
    """Read the starred-repos snapshot: (repos, updated-date-or-None)."""
    repos: list[str] = []
    updated: str | None = None
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError:
        return repos, updated
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if s.startswith("#"):
            m = re.search(r"updated:\s*(\d{4}-\d{2}-\d{2})", s)
            if m:
                updated = m.group(1)
            continue
        if re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", s):
            repos.append(s)
    return repos, updated


def write_snapshot(repos: list[str], path: str) -> None:
    """Persist the starred repo list so token-free environments can still
    check them via the atom feed. Best-effort: never crash the fetch."""
    try:
        today = dt.datetime.now(dt.timezone.utc).date().isoformat()
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("# starred repos snapshot for vault-updates-daily; machine-written, do not hand-edit\n")
            fh.write(f"# updated: {today}\n")
            for repo in sorted(set(r for r in repos if r)):
                fh.write(repo + "\n")
    except OSError as exc:
        print(f"META:starred|||snapshot-write-failed|||{exc}", file=sys.stderr)


def fetch_releases_atom(repo: str, since: dt.datetime) -> None:
    """Token-free release fetch via github.com's per-repo atom feed.

    Used as the starred fallback when there is no gh/token auth: the atom feed
    is served by github.com (not the REST API), so it is not subject to the
    unauthenticated 60/hr API rate limit."""
    url = f"https://github.com/{repo}/releases.atom"
    try:
        text = request_text(url)
        root = ET.fromstring(text)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR:releases:{repo}:atom {exc}")
        return
    for entry in root.findall("a:entry", _ATOM_NS):
        updated = _parse_iso(entry.findtext("a:updated", default="", namespaces=_ATOM_NS))
        if not updated or updated < since:
            continue
        # Atom entries carry no separate tag_name; the title IS the tag/name.
        title = _sanitize(entry.findtext("a:title", default="", namespaces=_ATOM_NS))
        link_el = entry.find("a:link", _ATOM_NS)
        html_url = _sanitize(link_el.get("href") if link_el is not None else "")
        body = _sanitize_body(entry.findtext("a:content", default="", namespaces=_ATOM_NS))
        print(f"RELEASE:{repo}|||{updated.isoformat()}|||{title}|||{title}|||{html_url}|||{body}")


def _starred_from_snapshot(since: dt.datetime, skip_repos: set[str], snapshot_path: str) -> None:
    repos, updated = read_snapshot(snapshot_path)
    if not repos:
        print(f"ERROR:starred:no auth and no snapshot at {snapshot_path}; "
              "run 'fetch_updates.py --snapshot-starred' locally (with gh login or GITHUB_TOKEN) first")
        return
    print(f"META:starred|||snapshot|||{updated or 'unknown'}|||{len(repos)} repos")
    for repo in repos:
        if repo in skip_repos:
            continue
        fetch_releases_atom(repo, since)


def query_starred_repos() -> list[str]:
    """Enumerate the authenticated viewer's starred repos (needs gh/token).
    Raises RuntimeError when no auth route is available."""
    query = "query { viewer { starredRepositories(first: 100) { nodes { nameWithOwner } } } }"
    payload = graphql_query(query)
    nodes = (
        payload.get("data", {})
        .get("viewer", {})
        .get("starredRepositories", {})
        .get("nodes", [])
    )
    return [_sanitize(n.get("nameWithOwner")) for n in nodes if n.get("nameWithOwner")]


def fetch_starred_releases(since: dt.datetime, skip_repos: set[str], snapshot_path: str) -> None:
    """Fetch releases from all starred repos.

    With auth (gh login or GITHUB_TOKEN/GH_TOKEN belonging to the star owner),
    use a single live GraphQL call and opportunistically refresh the snapshot.
    Without auth (e.g. a headless cloud agent), the `viewer` query cannot run —
    fall back to the snapshot's repo list via the token-free atom feed."""
    try:
        payload = graphql_query(_STARRED_QUERY)
    except Exception as exc:  # noqa: BLE001 — any auth/network failure → snapshot fallback
        print(f"META:starred|||live-failed|||{exc}", file=sys.stderr)
        _starred_from_snapshot(since, skip_repos, snapshot_path)
        return

    repos = (
        payload.get("data", {})
        .get("viewer", {})
        .get("starredRepositories", {})
        .get("nodes", [])
    )
    repo_names: list[str] = []
    for repo in repos:
        name_with_owner = _sanitize(repo.get("nameWithOwner"))
        if name_with_owner:
            repo_names.append(name_with_owner)
        if name_with_owner in skip_repos:
            continue
        for release in repo.get("releases", {}).get("nodes", []):
            published = _parse_iso(str(release.get("publishedAt") or ""))
            if not published or published < since:
                continue
            tag = _sanitize(release.get("tagName"))
            rname = _sanitize(release.get("name") or tag)
            url = _sanitize(release.get("url"))
            body = _sanitize_body(release.get("description") or "")
            print(f"RELEASE:{name_with_owner}|||{published.isoformat()}|||{tag}|||{rname}|||{url}|||{body}")
    print(f"META:starred|||live|||{len(repo_names)} repos")
    write_snapshot(repo_names, snapshot_path)


def fetch_releases(repo: str, since: dt.datetime) -> None:
    url = f"https://api.github.com/repos/{repo}/releases?per_page=30"
    try:
        data = request_json(url)
    except RuntimeError as exc:
        print(f"ERROR:releases:{repo}:{exc}")
        return

    if not isinstance(data, list):
        print(f"ERROR:releases:{repo}:unexpected response")
        return

    for item in data:
        if not isinstance(item, dict):
            continue
        published = _parse_iso(str(item.get("published_at") or ""))
        if not published or published < since:
            continue
        tag = _sanitize(item.get("tag_name"))
        name = _sanitize(item.get("name") or tag)
        html_url = _sanitize(item.get("html_url"))
        body = _sanitize_body(item.get("body") or "")
        print(f"RELEASE:{repo}|||{published.isoformat()}|||{tag}|||{name}|||{html_url}|||{body}")




def _is_github_blog_feed(url: str) -> bool:
    """True for any github.blog changelog RSS feed — the general
    `/changelog/feed/` or a label-scoped one like `/changelog/label/copilot/feed/`.
    github.blog is a distinct domain from github.com/api.github.com and is not
    subject to the Anthropic agent proxy's repository-bound access restriction."""
    stripped = url.rstrip("/")
    return stripped.startswith("https://github.blog/changelog") and stripped.endswith("/feed")


def fetch_github_changelog(name: str, url: str, since: dt.datetime) -> None:
    # Label-scoped feeds (e.g. /changelog/label/copilot/feed/) are already
    # precision-scoped by GitHub's own labeling — only the unscoped general
    # feed needs the keyword filter to cut cross-topic noise.
    apply_keyword_filter = url.rstrip("/") == _GITHUB_RSS_URL.rstrip("/")
    try:
        text = request_text(url)
        root = ET.fromstring(text)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR:{name}:{exc}")
        return

    for item in root.findall(".//item"):
        title = _sanitize(item.findtext("title"))
        link = _sanitize(item.findtext("link"))
        published = _parse_rss_date(item.findtext("pubDate") or "")
        if not published or published < since:
            continue
        if apply_keyword_filter:
            haystack = title.lower()
            if not any(keyword in haystack for keyword in CHANGELOG_KEYWORDS):
                continue
        desc = _sanitize_body(item.findtext("description") or "")
        print(f"CHANGELOG:{name}|||{published.isoformat()}|||{title}|||{link}|||{desc}")


DEFAULT_INDEX = "raw/Updates/01.index.md"


def parse_index(path: str) -> tuple[list[str], list[str], bool]:
    """Parse raw/Updates/01.index.md into (official, repos, starred).

    Replaces the former bash/awk glue in SKILL.md. Sections:
      ## Official changelogs  → '- name|url|tag' lines → official ('name|url|tag')
      ## GitHub repositories  → '- owner/name|tag' lines → repo (owner/name)
      ## GitHub starred       → a 'sync: releases' line → starred=True
    """
    official: list[str] = []
    repos: list[str] = []
    starred = False
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError as exc:
        print(f"ERROR:index:cannot read {path}: {exc}")
        return official, repos, starred

    section = None
    for ln in lines:
        s = ln.strip()
        if s.startswith("## "):
            section = s[3:].strip().lower()
            continue
        if section == "official changelogs":
            if s.startswith("- ") and "|" in s:
                official.append(s[2:].strip())
        elif section == "github repositories":
            if s.startswith("- "):
                repo = s[2:].split("|", 1)[0].strip()
                if re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", repo):
                    repos.append(repo)
        elif section == "github starred":
            compact = s.replace(" ", "").lower()
            if compact.startswith("sync:") and "releases" in compact:
                starred = True
    return official, repos, starred


def main() -> int:
    default_since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7)).date().isoformat()
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", default=default_since, help="YYYY-MM-DD, default: 7 days ago")
    parser.add_argument("--repo", action="append", default=[], help="GitHub repo owner/name; repeatable")
    parser.add_argument("--official", action="append", default=[],
                        help="Official changelog source: 'name|url|tag'; repeatable")
    parser.add_argument("--starred", action="store_true", help="also fetch releases from all starred repos")
    parser.add_argument("--snapshot-path", default=DEFAULT_SNAPSHOT,
                        help=f"starred repos snapshot file (default: {DEFAULT_SNAPSHOT})")
    parser.add_argument("--snapshot-starred", action="store_true",
                        help="refresh the starred snapshot (needs gh/token) and exit; run this locally")
    parser.add_argument("--index", default=None,
                        help=f"parse sources from this index md (default: {DEFAULT_INDEX} when no explicit "
                             "--official/--repo/--starred given)")
    args = parser.parse_args()

    # Standalone snapshot refresh: enumerate stars (needs auth) and persist the
    # list so token-free environments can later check them via the atom feed.
    if args.snapshot_starred:
        try:
            repos = query_starred_repos()
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR:starred:snapshot enumeration failed ({exc}); "
                  "needs gh login or GITHUB_TOKEN/GH_TOKEN")
            return 1
        write_snapshot(repos, args.snapshot_path)
        print(f"META:starred|||snapshot-written|||{len(repos)} repos|||{args.snapshot_path}")
        return 0

    # Source resolution: explicit flags win; otherwise parse the index md.
    # 01.index.md is the single source of truth — the script never hardcodes a tool list.
    index_path = args.index
    if index_path is None and not (args.official or args.repo or args.starred):
        index_path = DEFAULT_INDEX
    if index_path is not None:
        idx_official, idx_repos, idx_starred = parse_index(index_path)
        args.official += idx_official
        args.repo += idx_repos
        args.starred = args.starred or idx_starred

    try:
        since = _parse_date(args.since)
    except ValueError:
        print(f"ERROR:usage:invalid --since date {args.since!r}; expected YYYY-MM-DD")
        return 1

    explicit_repos = args.repo

    # Build official sources from --official args (no hardcoded fallback)
    official_sources: list[tuple[str, str, str]] = []
    for raw in args.official:
        parts = raw.split("|", 2)
        if len(parts) != 3:
            print(f"ERROR:official:invalid format {raw!r}; expected name|url|tag")
            continue
        official_sources.append((parts[0].strip(), parts[1].strip(), parts[2].strip()))

    if not official_sources and not explicit_repos and not args.starred:
        print("ERROR:usage:no sources provided; pass --official, --repo, or --starred "
              "(driven by raw/Updates/01.index.md)")
        return 1

    print(f"META:since|||{since.date().isoformat()}")

    for name, url, tag in official_sources:
        if _is_github_blog_feed(url):
            fetch_github_changelog(name, url, since)
        else:
            print(f"OFFICIAL:{_sanitize(name)}|||{_sanitize(url)}|||{_sanitize(tag)}")

    # Explicit repos always go through REST (token+REST works without gh).
    # This is independent of --starred: the starred GraphQL path needs gh or a
    # token and must never be the sole route to an explicitly tracked repo's releases.
    for repo in explicit_repos:
        if not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", repo):
            print(f"ERROR:repo:{repo}:invalid owner/name")
            continue
        fetch_releases(repo, since)

    if args.starred:
        # Additional starred-only repos via a single GraphQL call
        # (gh, or curl/urllib + GITHUB_TOKEN/GH_TOKEN — the token must belong to
        # the user whose stars are synced, since the query reads `viewer`).
        # Explicit repos are skipped here — they are already covered by REST
        # above — so there are no duplicate RELEASE lines.
        fetch_starred_releases(since, skip_repos=set(explicit_repos), snapshot_path=args.snapshot_path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
