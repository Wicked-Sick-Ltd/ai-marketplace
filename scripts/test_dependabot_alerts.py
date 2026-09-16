#!/usr/bin/env python3
"""Smoke tests for scripts/dependabot_alerts.py (no live GitHub required)."""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dependabot_alerts.py"


def load_module():
    spec = importlib.util.spec_from_file_location("dependabot_alerts", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class DependabotAlertsScriptTests(unittest.TestCase):
    def test_resolve_token_prefers_gh_token(self) -> None:
        mod = load_module()
        env = {
            "GH_TOKEN": "gh_first",
            "GITHUB_TOKEN": "github_second",
            "GITHUB_PAT": "pat_third",
        }
        with mock.patch.dict(os.environ, env, clear=False):
            name, value = mod.resolve_token()
        self.assertEqual(name, "GH_TOKEN")
        self.assertEqual(value, "gh_first")

    def test_resolve_token_falls_back_to_github_pat(self) -> None:
        mod = load_module()
        cleaned = {
            key: value
            for key, value in os.environ.items()
            if key not in ("GH_TOKEN", "GITHUB_TOKEN", "GITHUB_PAT")
        }
        cleaned["GITHUB_PAT"] = "pat_only"
        with mock.patch.dict(os.environ, cleaned, clear=True):
            name, value = mod.resolve_token()
        self.assertEqual(name, "GITHUB_PAT")
        self.assertEqual(value, "pat_only")

    def test_check_prints_permission_guidance_on_403(self) -> None:
        mod = load_module()

        def fake_api_get(url: str, token: str):
            return (
                403,
                {"x-accepted-github-permissions": "vulnerability_alerts=read"},
                {"message": "Resource not accessible by personal access token"},
            )

        with mock.patch.dict(os.environ, {"GH_TOKEN": "test-token"}, clear=False):
            with mock.patch.object(mod, "api_get", side_effect=fake_api_get):
                with self.assertRaises(SystemExit) as raised:
                    mod.main(["--check"])
        self.assertEqual(raised.exception.code, 3)

    def test_cli_missing_token_exits_nonzero(self) -> None:
        env = os.environ.copy()
        for key in ("GH_TOKEN", "GITHUB_TOKEN", "GITHUB_PAT"):
            env.pop(key, None)
        proc = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"],
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("No GitHub token found", proc.stderr)


if __name__ == "__main__":
    unittest.main()
