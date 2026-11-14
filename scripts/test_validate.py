#!/usr/bin/env python3
"""Smoke tests for marketplace catalog validation."""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "scripts" / "validate.py"

sys.path.insert(0, str(ROOT / "scripts"))
import validate  # noqa: E402


def expect_fail(what: str, expected: str, call) -> None:
    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        try:
            call()
        except SystemExit:
            if expected not in buf.getvalue():
                raise SystemExit(f"wrong error for {what}: {buf.getvalue()}")
            return
    raise SystemExit(f"validator accepted {what}")


def run_validate() -> None:
    proc = subprocess.run(
        [sys.executable, str(VALIDATE)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"validate.py failed:\n{proc.stdout}\n{proc.stderr}")
    if "ok: marketplace catalogs are valid" not in proc.stdout:
        raise SystemExit(f"unexpected validate.py output:\n{proc.stdout}")


def cursor_rejects_github_source() -> None:
    expect_fail(
        "a Cursor GitHub SHA source",
        "in-repo path",
        lambda: validate._cursor_source_path(
            "token-usage",
            {
                "source": "github",
                "repo": "Wicked-Sick-Ltd/token-usage",
                "sha": "67164452fb51eff2e76df65b937dd3e725b75103",
            },
        ),
    )


def codex_shape_validates() -> None:
    names = validate.codex_plugin_names(
        {
            "plugins": [
                {
                    "name": "wizzo-fleet-presence",
                    "source": {
                        "source": "url",
                        "url": "https://github.com/Wicked-Sick-Ltd/ai-codex-repo.git",
                        "sha": "a" * 40,
                    },
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    "category": "Developer Tools",
                }
            ]
        }
    )
    if names != ["wizzo-fleet-presence"]:
        raise SystemExit(f"unexpected codex_plugin_names result: {names}")


def claude_catalog(source: object) -> dict:
    return {"plugins": [{"name": "wizzo-fleet-presence", "source": source}]}


def sha_pin_is_enforced() -> None:
    expect_fail(
        "a Claude source object with no sha",
        "40 lowercase hex chars",
        lambda: validate.plugin_names(
            claude_catalog(
                {
                    "source": "git-subdir",
                    "url": "https://github.com/Wicked-Sick-Ltd/claude-repo.git",
                    "path": "plugins/wizzo-fleet-presence",
                }
            ),
            require_sha=True,
        ),
    )
    expect_fail(
        "a Claude entry with no source",
        "source object pinned to a sha",
        lambda: validate.plugin_names(claude_catalog(None), require_sha=True),
    )
    expect_fail(
        "a Claude entry whose source is a bare string",
        "source object pinned to a sha",
        lambda: validate.plugin_names(
            claude_catalog("plugins/wizzo-fleet-presence"), require_sha=True
        ),
    )
    expect_fail(
        "a Claude github source with no repo",
        "github source missing repo",
        lambda: validate.plugin_names(
            claude_catalog(
                {
                    "source": "github",
                    "sha": "0cb15af9a28adac61f0c7e9ffc709f96b5d92576",
                }
            ),
            require_sha=True,
        ),
    )


def duplicate_names_fail_on_every_catalog() -> None:
    for label in ("Claude", "Cursor", "Codex", "Copilot"):
        expect_fail(
            f"duplicate names in the {label} catalog",
            f"duplicate plugin names in {label} catalog",
            lambda label=label: validate.check_names(
                label, ["wizzo-fleet-presence", "wizzo-fleet-presence"]
            ),
        )
    validate.check_names("Copilot", ["token-usage"])
    validate.check_names("Gemini", ["token-usage"])
    expect_fail(
        "token-usage on an unverified host",
        "without a supported runtime",
        lambda: validate.check_names("Unverified", ["token-usage"]),
    )


def codex_native_sources():
    source = {"source": "git-subdir", "url": "https://github.com/Wicked-Sick-Ltd/ai-codex-repo.git",
              "path": "plugins/pr-flow", "sha": "a" * 40, "ref": "main"}
    entry = {"name": "pr-flow", "source": source,
             "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
             "category": "Developer Tools"}
    assert validate.codex_plugin_names({"plugins": [entry]}) == ["pr-flow"]
    for key, value, error in [("sha", "main", "40 lowercase"),
                              ("path", "", "missing path"),
                              ("path", "../outside", "inside the source"),
                              ("ref", "", "non-empty")]:
        bad = dict(entry, source=dict(source, **{key: value}))
        expect_fail(f"invalid Codex {key}", error,
                    lambda: validate.codex_plugin_names({"plugins": [bad]}))
    missing_pin = dict(entry, source={k: v for k, v in source.items() if k != "sha"})
    expect_fail("unversioned Codex source", "pinned to a sha",
                lambda: validate.codex_plugin_names({"plugins": [missing_pin]}))
    validate.check_names("Codex", ["token-usage"])


def vendored_relative_source_is_allowed() -> None:
    names = validate.plugin_names(
        {"plugins": [{"name": "pr-flow", "source": "./plugins/pr-flow"}]},
        require_sha=True,
    )
    if names != ["pr-flow"]:
        raise SystemExit(f"relative Claude source was rejected: {names}")
    codex_names = validate.codex_plugin_names(
        {
            "plugins": [
                {
                    "name": "pr-flow",
                    "source": "./plugins/pr-flow",
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    "category": "Developer Tools",
                }
            ]
        }
    )
    if codex_names != ["pr-flow"]:
        raise SystemExit(f"relative Codex source was rejected: {codex_names}")
    expect_fail(
        "a missing vendored directory",
        "not a directory",
        lambda: validate.plugin_names(
            {"plugins": [{"name": "missing", "source": "./plugins/missing-plugin"}]},
            require_sha=True,
        ),
    )
    expect_fail(
        "a vendored source outside plugins/",
        "under ./plugins/",
        lambda: validate.plugin_names(
            {"plugins": [{"name": "docs", "source": "./docs"}]},
            require_sha=True,
        ),
    )


def amiga_decoding_is_public() -> None:
    description = (
        "Evidence-led Amiga ADF extraction and decompilation to exhaustion, "
        "with separate disk, content and semantic coverage."
    )
    private = (
        "ai-grok-repo",
        "ai-codex-repo",
        "ai-claude-repo",
        "ai-copilot-repo",
        "ai-cursor-repo",
        "ai-gemini-repo",
        "code-catalog",
        "Proprietary",
    )
    # SHA-256 of personal tokens that must not appear. Plaintext is not stored.
    forbidden_sha256 = {
        "0cf548e7d1b66f356aa4be3ef8884f0ec14158a3c09300fb08ed9651f39ddd25",
        "6c2a806e0d9ad255834ea0e03f159be06346c0d7718d6e1e31c330243509fdd6",
    }
    token_re = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|[A-Za-z0-9]+")
    for key, path in validate.INDEXES.items():
        data = json.loads(path.read_text())
        matches = [plugin for plugin in data["plugins"] if plugin.get("name") == "amiga-decoding"]
        if len(matches) != 1:
            raise SystemExit(f"{key} should list amiga-decoding once, found {len(matches)}")
        plugin = matches[0]
        if plugin.get("description") != description:
            raise SystemExit(f"{key} description drifted: {plugin.get('description')!r}")
        blob = json.dumps(plugin)
        for token in private:
            if token in blob:
                raise SystemExit(f"{key} amiga-decoding still contains {token}")
        for token in token_re.findall(blob):
            digest = hashlib.sha256(token.encode()).hexdigest()
            if digest in forbidden_sha256:
                raise SystemExit(f"{key} amiga-decoding contains a forbidden token")
        source = plugin.get("source")
        if key == "cursor":
            if source != "plugins/amiga-decoding":
                raise SystemExit(f"cursor source is {source!r}")
        elif source != "./plugins/amiga-decoding":
            raise SystemExit(f"{key} source is {source!r}")
        if key != "codex" and plugin.get("version") != "1.0.0":
            raise SystemExit(f"{key} version is {plugin.get('version')!r}")
        if not plugin.get("category"):
            raise SystemExit(f"{key} amiga-decoding is missing category")
    manifest = ROOT / "plugins" / "amiga-decoding" / ".claude-plugin" / "plugin.json"
    version = json.loads(manifest.read_text())["version"]
    if version != "1.0.0":
        raise SystemExit(f"plugin.json version is {version!r}")
    extension = ROOT / "plugins" / "amiga-decoding" / "gemini-extension.json"
    if not extension.is_file():
        raise SystemExit("gemini-extension.json must sit at the plugin root")
    if "contextFileName" in extension.read_text():
        raise SystemExit("gemini-extension.json must not set contextFileName")
    plugin_text = "\n".join(
        path.read_text() for path in (ROOT / "plugins" / "amiga-decoding").rglob("*") if path.is_file()
    )
    for token in token_re.findall(plugin_text):
        digest = hashlib.sha256(token.encode()).hexdigest()
        if digest in forbidden_sha256:
            raise SystemExit("vendored amiga-decoding contains a forbidden token")


def main() -> None:
    run_validate()
    vendored_relative_source_is_allowed()
    amiga_decoding_is_public()
    cursor_rejects_github_source()
    codex_shape_validates()
    codex_native_sources()
    sha_pin_is_enforced()
    duplicate_names_fail_on_every_catalog()
    print("ok: validate tests passed")


if __name__ == "__main__":
    main()
