#!/usr/bin/env python3
"""List Dependabot alerts via the GitHub REST API.

Cloud Agent App install tokens (ghs_) cannot read Dependabot alerts. Prefer a
fine-grained PAT with Repository permission "Dependabot alerts: Read", injected
as GH_TOKEN (or GITHUB_TOKEN). See docs/github-security-api-access.md.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

DEFAULT_REPO = "Wicked-Sick-Ltd/ai-marketplace"
API_VERSION = "2022-11-28"
TOKEN_ENV_PREFERENCE = ("GH_TOKEN", "GITHUB_TOKEN", "GITHUB_PAT")


def fail(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def resolve_token() -> tuple[str, str]:
    for name in TOKEN_ENV_PREFERENCE:
        value = os.environ.get(name, "").strip()
        if value:
            return name, value
    fail(
        "No GitHub token found. Set GH_TOKEN (preferred) to a fine-grained PAT "
        "with Dependabot alerts: Read. See docs/github-security-api-access.md."
    )


def api_get(url: str, token: str) -> tuple[int, dict[str, str], Any]:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": API_VERSION,
            "User-Agent": "ai-marketplace-dependabot-alerts",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return resp.status, headers, json.loads(body) if body else None
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        headers = {k.lower(): v for k, v in exc.headers.items()} if exc.headers else {}
        try:
            payload: Any = json.loads(body) if body else {"message": body}
        except json.JSONDecodeError:
            payload = {"message": body}
        return exc.code, headers, payload


def permission_hint(headers: dict[str, str], payload: Any) -> str:
    needed = headers.get("x-accepted-github-permissions", "")
    message = ""
    if isinstance(payload, dict):
        message = str(payload.get("message") or "")
    lines = [
        "Dependabot alerts API returned 403.",
        f"GitHub message: {message or '(none)'}",
    ]
    if needed:
        lines.append(f"Required permission header: {needed}")
    lines.extend(
        [
            "",
            "Fix:",
            "  1. Edit your fine-grained PAT → Repository permissions →",
            "     Dependabot alerts = Read-only.",
            "  2. Inject that PAT as Cloud Agent secret GH_TOKEN",
            "     (not GITHUB_PAT — gh ignores that name).",
            "  3. Re-run: python3 scripts/dependabot_alerts.py",
            "",
            "Details: docs/github-security-api-access.md",
        ]
    )
    return "\n".join(lines)


def list_alerts(owner_repo: str, state: str, token: str) -> list[dict[str, Any]]:
    owner, _, repo = owner_repo.partition("/")
    if not owner or not repo:
        fail(f"Invalid repo {owner_repo!r}; expected owner/name")

    alerts: list[dict[str, Any]] = []
    page = 1
    while True:
        query = urllib.parse.urlencode(
            {"state": state, "per_page": "100", "page": str(page)}
        )
        url = f"https://api.github.com/repos/{owner}/{repo}/dependabot/alerts?{query}"
        status, headers, payload = api_get(url, token)
        if status == 403:
            fail(permission_hint(headers, payload), code=3)
        if status == 404:
            fail(
                f"Repo not found or Dependabot alerts disabled for {owner_repo}. "
                f"API payload: {payload}"
            )
        if status != 200:
            fail(f"GitHub API HTTP {status}: {payload}")
        if not isinstance(payload, list):
            fail(f"Unexpected API payload type: {type(payload).__name__}")
        alerts.extend(payload)
        if len(payload) < 100:
            break
        page += 1
    return alerts


def summarize(alert: dict[str, Any]) -> dict[str, Any]:
    advisory = alert.get("security_advisory") or {}
    vuln = alert.get("security_vulnerability") or {}
    package = vuln.get("package") or {}
    patched = vuln.get("first_patched_version") or {}
    return {
        "number": alert.get("number"),
        "state": alert.get("state"),
        "severity": advisory.get("severity"),
        "package": package.get("name"),
        "ecosystem": package.get("ecosystem"),
        "vulnerable_range": vuln.get("vulnerable_version_range"),
        "first_patched": patched.get("identifier"),
        "ghsa": advisory.get("ghsa_id"),
        "summary": advisory.get("summary"),
        "html_url": alert.get("html_url"),
    }


def main(argv: list[str]) -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY", DEFAULT_REPO),
        help=f"owner/name (default: {DEFAULT_REPO})",
    )
    parser.add_argument(
        "--state",
        default="open",
        choices=("open", "dismissed", "fixed", "auto_dismissed", "all"),
        help="Alert state filter (default: open)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print full summarized JSON instead of a table",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 0 if API access works (even with zero alerts); non-zero on auth failure",
    )
    args = parser.parse_args(argv)

    token_name, token = resolve_token()
    alerts = list_alerts(args.repo, args.state, token)
    rows = [summarize(a) for a in alerts]

    if args.check:
        print(
            f"ok: Dependabot alerts API accessible via {token_name} "
            f"({len(rows)} {args.state} alert(s) on {args.repo})"
        )
        return 0

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    print(
        f"# Dependabot alerts ({args.state}) for {args.repo} via {token_name}: "
        f"{len(rows)}"
    )
    if not rows:
        return 0

    for row in rows:
        print(
            f"- #{row['number']} [{row['severity']}] {row['package']} "
            f"{row['vulnerable_range']} → {row['first_patched'] or '?'} "
            f"| {row['ghsa']} | {row['summary']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
