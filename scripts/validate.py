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
        if require_sha:
            if not isinstance(source, dict):
                fail(f"plugin {name!r} needs a source object pinned to a sha")
            sha = source.get("sha")
            if not isinstance(sha, str) or not SHA_RE.match(sha):
                fail(f"plugin {name!r} sha must be 40 lowercase hex chars")
            source_type = source.get("source")
            if source_type == "github" and not source.get("repo"):
                fail(f"plugin {name!r} github source missing repo")
            if source_type == "git-subdir" and not source.get("url"):
                fail(f"plugin {name!r} git-subdir source missing url")
    return names


CODEX_SOURCE_TYPES = {"url", "local", "git-subdir"}


def codex_plugin_names(data: dict) -> list[str]:
    """Codex's Agent Plugins schema has no ref/sha field: an entry names a
    repo URL (or an in-repo/local path) and Codex resolves it directly —
    there is nothing to pin to. Validate that shape instead of requiring
    a Claude-style sha.
    """
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
        if not isinstance(source, dict):
            fail(f"Codex plugin {name!r} missing source")
        if "sha" in source:
            fail(f"Codex plugin {name!r} source must not carry a sha (Codex has no ref/sha field)")
        source_type = source.get("source")
        if source_type not in CODEX_SOURCE_TYPES:
            fail(f"Codex plugin {name!r} source.source must be one of {sorted(CODEX_SOURCE_TYPES)}")
        if source_type in ("url", "git-subdir") and not source.get("url"):
            fail(f"Codex plugin {name!r} source is missing url")
        if source_type == "local" and not source.get("path"):
            fail(f"Codex plugin {name!r} local source is missing path")
        policy = plugin.get("policy")
        if (
            not isinstance(policy, dict)
            or not policy.get("installation")
            or not policy.get("authentication")
        ):
            fail(f"Codex plugin {name!r} missing policy.installation/policy.authentication")
        if not plugin.get("category"):
            fail(f"Codex plugin {name!r} missing category")
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


def check_names(label: str, names: list[str], *, allow_claude_only: bool = False) -> None:
    dupes = sorted({name for name in names if names.count(name) > 1})
    if dupes:
        fail(f"duplicate plugin names in {label} catalog: {dupes}")
    if allow_claude_only:
        return
    leaked = sorted(CLAUDE_ONLY.intersection(names))
    if leaked:
        fail(f"{label} catalog must not list Claude-only plugins: {leaked}")


def check_gemini_readme() -> None:
    path = ROOT / "gemini" / "README.md"
    if not path.is_file():
        fail("missing gemini/README.md")
    text = path.read_text()
    for name in sorted(CLAUDE_ONLY):
        if name not in text:
            fail(f"gemini/README.md must say why {name!r} is not listed for Gemini")


def main() -> None:
    catalogs = {key: load(path) for key, path in INDEXES.items()}

    claude = catalogs["claude"]
    if claude.get("name") != "wickedsick":
        fail("Claude marketplace name must be wickedsick")
    claude_names = plugin_names(claude, require_sha=True)
    if "token-usage" not in claude_names:
        fail("Claude catalog must list token-usage")
    check_names("Claude", claude_names, allow_claude_only=True)

    cursor = catalogs["cursor"]
    if cursor.get("name") != "wickedsick":
        fail("Cursor marketplace name must be wickedsick")
    check_names("Cursor", cursor_plugin_names(cursor))
    check_names("Codex", codex_plugin_names(catalogs["codex"]))
    check_names("Copilot", plugin_names(catalogs["copilot"], require_sha=True))

    check_gemini_readme()

    print("ok: marketplace catalogs are valid")


if __name__ == "__main__":
    main()
