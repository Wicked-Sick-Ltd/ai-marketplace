#!/usr/bin/env python3
"""Smoke tests for marketplace catalog validation."""

from __future__ import annotations

import contextlib
import io
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
                        "url": "https://github.com/Wicked-Sick-Ltd/codex-repo.git",
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
    expect_fail(
        "token-usage on the Cursor catalog",
        "must not list Claude-only plugins",
        lambda: validate.check_names("Cursor", ["token-usage"]),
    )


def main() -> None:
    run_validate()
    cursor_rejects_github_source()
    codex_shape_validates()
    sha_pin_is_enforced()
    duplicate_names_fail_on_every_catalog()
    print("ok: validate tests passed")


if __name__ == "__main__":
    main()
