from __future__ import annotations

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from typing import Any


TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def _github_get(url: str, token: str | None) -> Any:
    request = urllib.request.Request(url)
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("User-Agent", "copilot-sre")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _window_start(started_at: str, lookback_hours: int) -> str:
    timestamp = datetime.strptime(started_at, TIME_FORMAT) - timedelta(hours=lookback_hours)
    return timestamp.strftime(TIME_FORMAT)


def _fetch_commits(repo: str, since: str, token: str | None) -> list[dict[str, str]]:
    encoded_since = urllib.parse.quote(since)
    url = f"https://api.github.com/repos/{repo}/commits?since={encoded_since}&per_page=5"
    items = _github_get(url, token)
    if not items:
        items = _github_get(f"https://api.github.com/repos/{repo}/commits?per_page=5", token)
    commits: list[dict[str, str]] = []
    for item in items:
        commit = item.get("commit", {})
        author = commit.get("author", {}).get("name") or item.get("author", {}).get("login") or "unknown"
        commits.append(
            {
                "sha": item.get("sha", "")[:7],
                "author": author,
                "message": (commit.get("message") or "").splitlines()[0],
            }
        )
    return commits


def _fetch_pull_requests(repo: str, token: str | None) -> list[dict[str, str | int]]:
    url = f"https://api.github.com/repos/{repo}/pulls?state=closed&sort=updated&direction=desc&per_page=5"
    items = _github_get(url, token)
    prs: list[dict[str, str | int]] = []
    for item in items:
        prs.append(
            {
                "number": item.get("number", 0),
                "title": item.get("title", ""),
                "author": (item.get("user") or {}).get("login", "unknown"),
                "state": "merged" if item.get("merged_at") else item.get("state", "closed"),
                "updated_at": item.get("updated_at", ""),
                "url": item.get("html_url", ""),
            }
        )
    return prs


def enrich_incident_from_github(
    incident_data: dict[str, Any],
    repo: str,
    token_env: str,
    lookback_hours: int,
) -> dict[str, Any]:
    token = os.environ.get(token_env)
    started_at = incident_data["started_at"]
    since = _window_start(started_at, lookback_hours)

    try:
        commits = _fetch_commits(repo, since, token)
        pull_requests = _fetch_pull_requests(repo, token)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API request failed with status {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"GitHub API request failed: {exc.reason}") from exc

    enriched = dict(incident_data)
    enriched["source_repo"] = repo
    enriched["commits"] = commits
    enriched["pull_requests"] = pull_requests
    return enriched
