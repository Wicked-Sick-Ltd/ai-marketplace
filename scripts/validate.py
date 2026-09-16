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


def plugin_names(data: dict, *, require_sha: bool) -> list[str]:
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
        if require_sha and isinstance(source, dict):
            sha = source.get("sha")
            if not sha:
                fail(f"plugin {name!r} source is missing sha")
            if not SHA_RE.match(sha):
                fail(f"plugin {name!r} sha must be 40 lowercase hex chars")
            if source.get("source") == "github" and not source.get("repo"):
                fail(f"plugin {name!r} github source missing repo")
    return names


def _cursor_source_path(name: str, source: object) -> Path:
    """Cursor catalogs resolve source as a directory inside this git repo."""
    if isinstance(source, str):
        rel = source
    elif isinstance(source, dict):
        if source.get("source") == "github" or "sha" in source or "repo" in source:
            fail(
                f"Cursor plugin {name!r} must use an in-repo path, not a GitHub SHA pin "
                "(see docs/cursor-integration.md)"
            )
        rel = source.get("path")
        if not rel:
            fail(f"Cursor plugin {name!r} source object is missing path")
    else:
        fail(f"Cursor plugin {name!r} source must be a relative path string or {{path}} object")
    if not isinstance(rel, str) or not rel.strip():
        fail(f"Cursor plugin {name!r} source path must be a non-empty string")
    if rel.startswith("/") or rel.startswith("~") or ".." in Path(rel).parts:
        fail(f"Cursor plugin {name!r} source path must be relative and stay in-repo")
    return ROOT / rel


def cursor_plugin_names(data: dict) -> list[str]:
    names = plugin_names(data, require_sha=False)
    plugin_root = ""
    metadata = data.get("metadata")
    if isinstance(metadata, dict):
        plugin_root = metadata.get("pluginRoot") or ""
        if plugin_root and (
            str(plugin_root).startswith("/") or ".." in Path(str(plugin_root)).parts
        ):
            fail("Cursor metadata.pluginRoot must be a relative in-repo path")
    for plugin in data["plugins"]:
        name = plugin["name"]
        source = plugin.get("source")
        if source is None:
            fail(f"Cursor plugin {name!r} missing source")
        plugin_dir = _cursor_source_path(name, source)
        if plugin_root:
            plugin_dir = ROOT / plugin_root / plugin_dir.relative_to(ROOT)
        if not plugin_dir.is_dir():
            fail(f"Cursor plugin {name!r} source is not a directory: {plugin_dir.relative_to(ROOT)}")
        cursor_manifest = plugin_dir / ".cursor-plugin" / "plugin.json"
        agent_manifest = plugin_dir / "plugin.json"
        if not cursor_manifest.is_file() and not agent_manifest.is_file():
            fail(
                f"Cursor plugin {name!r} needs {cursor_manifest.relative_to(ROOT)} "
                f"or {agent_manifest.relative_to(ROOT)}"
            )
    return names


def main() -> None:
    for path in INDEXES.values():
        load(path)

    claude = load(INDEXES["claude"])
    if claude.get("name") != "wickedsick":
        fail("Claude marketplace name must be wickedsick")
    names = plugin_names(claude, require_sha=True)
    if "token-usage" not in names:
        fail("Claude catalog must list token-usage")
    if len(names) != len(set(names)):
        fail("duplicate plugin names in Claude catalog")

    cursor = load(INDEXES["cursor"])
    if cursor.get("name") != "wickedsick":
        fail("Cursor marketplace name must be wickedsick")
    cursor_names = cursor_plugin_names(cursor)
    leaked = CLAUDE_ONLY.intersection(cursor_names)
    if leaked:
        fail(f"cursor catalog must not list Claude-only plugins: {sorted(leaked)}")

    for label in ("codex", "copilot"):
        listed = plugin_names(load(INDEXES[label]), require_sha=True)
        leaked = CLAUDE_ONLY.intersection(listed)
        if leaked:
            fail(f"{label} catalog must not list Claude-only plugins: {sorted(leaked)}")

    gemini = ROOT / "gemini" / "README.md"
    if not gemini.is_file():
        fail("missing gemini/README.md")

    print("ok: marketplace catalogs are valid")


if __name__ == "__main__":
    main()
