#!/usr/bin/env python3
"""Smoke tests for marketplace catalog validation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATE = ROOT / "scripts" / "validate.py"


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
    import contextlib
    import io

    sys.path.insert(0, str(ROOT / "scripts"))
    import validate  # noqa: E402

    buf = io.StringIO()
    with contextlib.redirect_stderr(buf):
        try:
            validate._cursor_source_path(
                "token-usage",
                {
                    "source": "github",
                    "repo": "Wicked-Sick-Ltd/token-usage",
                    "sha": "67164452fb51eff2e76df65b937dd3e725b75103",
                },
            )
        except SystemExit:
            if "in-repo path" not in buf.getvalue():
                raise SystemExit(f"wrong Cursor error: {buf.getvalue()}")
            return
    raise SystemExit("Cursor validator accepted a GitHub SHA source")


def codex_shape_validates() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    import validate  # noqa: E402

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


def claude_entry_without_sha_fails() -> None:
    sys.path.insert(0, str(ROOT / "scripts"))
    import validate  # noqa: E402

    try:
        validate.plugin_names(
            {
                "plugins": [
                    {
                        "name": "wizzo-fleet-presence",
                        "source": {
                            "source": "git-subdir",
                            "url": "https://github.com/Wicked-Sick-Ltd/claude-repo.git",
                            "path": "plugins/wizzo-fleet-presence",
                        },
                    }
                ]
            },
            require_sha=True,
        )
    except SystemExit:
        return
    raise SystemExit("Claude validator accepted a plugin source with no sha")


def main() -> None:
    run_validate()
    cursor_rejects_github_source()
    codex_shape_validates()
    claude_entry_without_sha_fails()
    print("ok: validate tests passed")


if __name__ == "__main__":
    main()
