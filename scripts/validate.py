#!/usr/bin/env python3
"""Validate Wicked Sick marketplace catalogs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHA_RE = re.compile(r"^[0-9a-f]{40}$")

INDEXES = {
    "claude": ROOT / ".claude-plugin" / "marketplace.json",
    "cursor": ROOT / ".cursor-plugin" / "marketplace.json",
    "codex": ROOT / ".agents" / "plugins" / "marketplace.json",
    "copilot": ROOT / ".github" / "plugin" / "marketplace.json",
}

CLAUDE_ONLY = {"token-usage"}


def fail(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} must be a JSON object")
    return data


def plugin_names(data: dict) -> list[str]:
    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        fail("plugins must be an array")
    names = []
    for i, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            fail(f"plugins[{i}] must be an object")
        name = plugin.get("name")
        if not name:
            fail(f"plugins[{i}] missing name")
        names.append(name)
        source = plugin.get("source")
        if isinstance(source, dict):
            sha = source.get("sha")
            if not sha:
                fail(f"plugin {name!r} source is missing sha")
            if not SHA_RE.match(sha):
                fail(f"plugin {name!r} sha must be 40 lowercase hex chars")
            if source.get("source") == "github" and not source.get("repo"):
                fail(f"plugin {name!r} github source missing repo")
    return names


def main() -> None:
    for path in INDEXES.values():
        load(path)

    claude = load(INDEXES["claude"])
    if claude.get("name") != "wickedsick":
        fail("Claude marketplace name must be wickedsick")
    names = plugin_names(claude)
    if "token-usage" not in names:
        fail("Claude catalog must list token-usage")
    if len(names) != len(set(names)):
        fail("duplicate plugin names in Claude catalog")

    for label in ("cursor", "codex", "copilot"):
        listed = plugin_names(load(INDEXES[label]))
        leaked = CLAUDE_ONLY.intersection(listed)
        if leaked:
            fail(f"{label} catalog must not list Claude-only plugins: {sorted(leaked)}")

    gemini = ROOT / "gemini" / "README.md"
    if not gemini.is_file():
        fail("missing gemini/README.md")

    print("ok: marketplace catalogs are valid")


if __name__ == "__main__":
    main()
