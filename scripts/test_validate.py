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
import tempfile
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


PR_FLOW_SHA = "be43fc21936ba2054ef084d0193e75a5770b97de"


def cursor_accepts_pr_flow_github_pin() -> None:
    source = {
        "source": "github",
        "repo": "Wicked-Sick-Ltd/pr-flow",
        "sha": PR_FLOW_SHA,
    }
    if validate._cursor_source_path("pr-flow", source) is not None:
        raise SystemExit("pr-flow github pin should not resolve to a local directory")
    expect_fail(
        "pr-flow pointed at another repository",
        "Wicked-Sick-Ltd/pr-flow",
        lambda: validate._cursor_source_path(
            "pr-flow",
            {
                "source": "github",
                "repo": "Wicked-Sick-Ltd/ai-grok-repo",
                "sha": "a" * 40,
            },
        ),
    )
    expect_fail(
        "pr-flow with a short sha",
        "40 lowercase hex chars",
        lambda: validate._cursor_source_path(
            "pr-flow",
            {"source": "github", "repo": "Wicked-Sick-Ltd/pr-flow", "sha": "abc"},
        ),
    )


def pr_flow_pins_dedicated_repo() -> None:
    expected = {
        "claude": {
            "source": "github",
            "repo": "Wicked-Sick-Ltd/pr-flow",
            "sha": PR_FLOW_SHA,
        },
        "cursor": {
            "source": "github",
            "repo": "Wicked-Sick-Ltd/pr-flow",
            "sha": PR_FLOW_SHA,
        },
        "codex": {
            "source": "url",
            "url": "https://github.com/Wicked-Sick-Ltd/pr-flow.git",
            "sha": PR_FLOW_SHA,
        },
        "copilot": {
            "source": "url",
            "url": "https://github.com/Wicked-Sick-Ltd/pr-flow.git",
            "sha": PR_FLOW_SHA,
        },
    }
    descriptions = {
        "claude": "Skills and a Bash/gh/jq helper for creating pull requests, waiting for checks, addressing reviews and landing changes.",
        "codex": "Skills and a Bash/gh/jq helper for creating pull requests, waiting for checks, addressing reviews and landing changes.",
        "copilot": "Skills and a Bash/gh/jq helper for creating pull requests, waiting for checks, addressing reviews and landing changes.",
        "cursor": "Skills and a Bash/gh/jq helper for opening a finished pull request ready for review, waiting for checks, addressing reviews and landing changes.",
    }
    categories = {
        "claude": "productivity",
        "cursor": "developer-tools",
        "codex": "Developer Tools",
        "copilot": "productivity",
    }
    for key, source in expected.items():
        data = json.loads(validate.INDEXES[key].read_text())
        matches = [plugin for plugin in data["plugins"] if plugin.get("name") == "pr-flow"]
        if len(matches) != 1:
            raise SystemExit(f"{key} should list pr-flow once, found {len(matches)}")
        plugin = matches[0]
        if plugin.get("source") != source:
            raise SystemExit(f"{key} pr-flow source is {plugin.get('source')!r}")
        if plugin.get("description") != descriptions[key]:
            raise SystemExit(f"{key} pr-flow description drifted")
        if plugin.get("category") != categories[key]:
            raise SystemExit(f"{key} pr-flow category is {plugin.get('category')!r}")
        if key == "codex":
            policy = plugin.get("policy")
            if policy != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
                raise SystemExit(f"codex pr-flow policy is {policy!r}")
            if "version" in plugin:
                raise SystemExit("codex pr-flow must not grow a version field")
        elif plugin.get("version") != "1.1.2":
            raise SystemExit(f"{key} pr-flow version is {plugin.get('version')!r}")
        blob = json.dumps(plugin)
        if "ai-grok-repo" in blob or "plugins/pr-flow" in blob:
            raise SystemExit(f"{key} pr-flow still points at the old tree")
    if (ROOT / "plugins" / "pr-flow").exists():
        raise SystemExit("plugins/pr-flow must not be vendored")


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
              "path": "plugins/example", "sha": "a" * 40, "ref": "main"}
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
    local_base = {
        "name": "bare",
        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
        "category": "Developer Tools",
    }
    for path in ("", "   ", None, 1):
        expect_fail(
            f"a Codex local source with path {path!r}",
            "missing path",
            lambda path=path: validate.codex_plugin_names(
                {"plugins": [dict(local_base, source={"source": "local", "path": path})]}
            ),
        )
    validate.check_names("Codex", ["token-usage"])


TREE_HASH_ONLY = (
    "- Skill tree at that commit: `cef77bef9a6706476bd5fdae6cb42d534fac676e`.\n"
)
UPSTREAM_SHA = "5ba30a22df385e75135101e3f886471ee0e9ee9d"


def relative_source_records_provenance() -> None:
    """A directory source names a labeled upstream commit or the first-party form."""
    if validate.provenance_recorded(UPSTREAM_SHA):
        raise SystemExit("a bare hash must not count as an upstream commit")
    if validate.provenance_recorded(TREE_HASH_ONLY):
        raise SystemExit("a tree hash must not count as an upstream commit")
    if validate.upstream_commit_recorded(TREE_HASH_ONLY):
        raise SystemExit("a tree-hash line must not match an upstream-commit label")
    for labeled in (
        f"- Source commit: `{UPSTREAM_SHA}`\n",
        f"- Content source: `Wicked-Sick-Ltd/example` `plugins/name` at `{UPSTREAM_SHA}` (`main`).\n",
        f"- Pinned checkout: `Wicked-Sick-Ltd/example` `plugins/name` at `{UPSTREAM_SHA}`.\n",
    ):
        if not validate.provenance_recorded(labeled):
            raise SystemExit(f"labeled upstream commit was rejected: {labeled}")
    if not validate.provenance_recorded(
        "Provenance: first-party. There is no separate upstream pin."
    ):
        raise SystemExit("the first-party statement must count as provenance")
    if validate.provenance_recorded("This package declares nothing about provenance."):
        raise SystemExit("a VENDORED.md without a commit or the statement must fail")
    if validate.provenance_recorded("short sha 5ba30a22 is not a pin"):
        raise SystemExit("a short hex string must not count as an upstream commit")
    amiga = (ROOT / "plugins" / "amiga-decoding" / "VENDORED.md").read_text()
    if not validate.upstream_commit_recorded(amiga):
        raise SystemExit("amiga-decoding VENDORED.md must record an upstream commit")
    without_source = "\n".join(
        line for line in amiga.splitlines() if "Content source:" not in line
    )
    if validate.provenance_recorded(without_source):
        raise SystemExit("amiga-decoding provenance must not survive on its skill-tree hash")
    for name in ("token-usage", "publicuniverse", "obsidian"):
        text = (ROOT / "plugins" / name / "VENDORED.md").read_text()
        if not validate.upstream_commit_recorded(text):
            raise SystemExit(f"{name} VENDORED.md must identify an upstream commit")
    red_team = (ROOT / "plugins" / "red-team-review" / "VENDORED.md").read_text()
    if validate.NO_UPSTREAM_PIN not in red_team.lower():
        raise SystemExit("red-team-review VENDORED.md must state there is no separate upstream pin")
    if validate.upstream_commit_recorded(red_team):
        raise SystemExit("red-team-review VENDORED.md must not invent an upstream commit")


def _cursor_package(plugin_dir: Path, vendored: str | None) -> None:
    manifest_dir = plugin_dir / ".cursor-plugin"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    (manifest_dir / "plugin.json").write_text("{}\n")
    if vendored is not None:
        (plugin_dir / "VENDORED.md").write_text(vendored)


def provenance_is_required_for_cursor_and_relative_sources() -> None:
    """Missing and unlabeled provenance fail on Claude, Codex, and Cursor."""
    saved = validate.ROOT
    try:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            validate.ROOT = root
            bare = root / "plugins" / "bare"
            _cursor_package(bare, None)
            claude = {"plugins": [{"name": "bare", "source": "./plugins/bare"}]}
            codex_local = {
                "plugins": [
                    {
                        "name": "bare",
                        "source": {"source": "local", "path": "./plugins/bare"},
                        "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                        "category": "Developer Tools",
                    }
                ]
            }
            expect_fail(
                "a relative source with no VENDORED.md",
                "needs",
                lambda: validate.plugin_names(claude, require_sha=True),
            )
            expect_fail(
                "a Cursor package with no VENDORED.md",
                "needs",
                lambda: validate.cursor_plugin_names(
                    {"plugins": [{"name": "bare", "source": "plugins/bare"}]}
                ),
            )
            expect_fail(
                "a Codex local source with no VENDORED.md",
                "needs",
                lambda: validate.codex_plugin_names(codex_local),
            )
            _cursor_package(bare, TREE_HASH_ONLY)
            expect_fail(
                "a relative source whose only hash is a tree hash",
                "must identify an upstream commit",
                lambda: validate.plugin_names(claude, require_sha=True),
            )
            expect_fail(
                "a Cursor package whose only hash is a tree hash",
                "must identify an upstream commit",
                lambda: validate.cursor_plugin_names(
                    {"plugins": [{"name": "bare", "source": "plugins/bare"}]}
                ),
            )
            expect_fail(
                "a Codex local source whose only hash is a tree hash",
                "must identify an upstream commit",
                lambda: validate.codex_plugin_names(codex_local),
            )
            (bare / "VENDORED.md").write_text("")
            expect_fail(
                "a Cursor package with an empty VENDORED.md",
                "must identify an upstream commit",
                lambda: validate.cursor_plugin_names(
                    {"plugins": [{"name": "bare", "source": "plugins/bare"}]}
                ),
            )
            resolved = root / "vendor" / "plugins" / "bare"
            _cursor_package(resolved, "There is no separate upstream pin.\n")
            (bare / "VENDORED.md").write_text(TREE_HASH_ONLY)
            names = validate.cursor_plugin_names(
                {
                    "metadata": {"pluginRoot": "vendor"},
                    "plugins": [{"name": "bare", "source": "plugins/bare"}],
                }
            )
            if names != ["bare"]:
                raise SystemExit(f"Cursor provenance ignored pluginRoot: {names}")
            (resolved / "VENDORED.md").write_text(TREE_HASH_ONLY)
            (bare / "VENDORED.md").write_text(
                f"- Source commit: `{UPSTREAM_SHA}`\n"
            )
            expect_fail(
                "a Cursor package whose resolved directory has only a tree hash",
                "must identify an upstream commit",
                lambda: validate.cursor_plugin_names(
                    {
                        "metadata": {"pluginRoot": "vendor"},
                        "plugins": [{"name": "bare", "source": "plugins/bare"}],
                    }
                ),
            )
    finally:
        validate.ROOT = saved


def vendored_relative_source_is_allowed() -> None:
    names = validate.plugin_names(
        {"plugins": [{"name": "amiga-decoding", "source": "./plugins/amiga-decoding"}]},
        require_sha=True,
    )
    if names != ["amiga-decoding"]:
        raise SystemExit(f"relative Claude source was rejected: {names}")
    codex_names = validate.codex_plugin_names(
        {
            "plugins": [
                {
                    "name": "amiga-decoding",
                    "source": "./plugins/amiga-decoding",
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    "category": "Developer Tools",
                }
            ]
        }
    )
    if codex_names != ["amiga-decoding"]:
        raise SystemExit(f"relative Codex source was rejected: {codex_names}")
    local_names = validate.codex_plugin_names(
        {
            "plugins": [
                {
                    "name": "amiga-decoding",
                    "source": {"source": "local", "path": "./plugins/amiga-decoding"},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    "category": "Developer Tools",
                }
            ]
        }
    )
    if local_names != ["amiga-decoding"]:
        raise SystemExit(f"Codex local source was rejected: {local_names}")
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
        "AI agent plugin that works with any AI agent. Evidence-led Amiga ADF extraction and decompilation to exhaustion, "
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


OBSIDIAN_SHA = "cd51b7076a1207c805cf1d95da4c56cb96bbe859"
OBSIDIAN_DESCRIPTION = (
    "Vetted Obsidian format skills: Obsidian Flavored Markdown, Bases (.base) "
    "and JSON Canvas. Instruction-only; no shell, network or credentials."
)
OBSIDIAN_SKILLS = ("json-canvas", "obsidian-bases", "obsidian-markdown")
OBSIDIAN_HELD = ("defuddle", "knap", "obsidian-cli", "obsidian-headless")


def obsidian_pin_is_the_merge_commit() -> None:
    """Catalogs pin wicked-main's merge, and the Cursor copy is that same tree."""
    for key, path in validate.INDEXES.items():
        data = json.loads(path.read_text())
        matches = [plugin for plugin in data["plugins"] if plugin.get("name") == "obsidian"]
        if len(matches) != 1:
            raise SystemExit(f"{key} should list obsidian once, found {len(matches)}")
        plugin = matches[0]
        if plugin.get("description") != OBSIDIAN_DESCRIPTION:
            raise SystemExit(f"{key} obsidian description drifted: {plugin.get('description')!r}")
        if not plugin.get("category"):
            raise SystemExit(f"{key} obsidian is missing category")
        blob = json.dumps(plugin)
        for held in OBSIDIAN_HELD:
            if held in blob:
                raise SystemExit(f"{key} obsidian entry names held skill {held}")
        source = plugin.get("source")
        if key == "cursor":
            if source != "plugins/obsidian":
                raise SystemExit(f"cursor obsidian source is {source!r}")
            if plugin.get("version") != "1.2.0":
                raise SystemExit(f"cursor obsidian version is {plugin.get('version')!r}")
            continue
        if not isinstance(source, dict):
            raise SystemExit(f"{key} obsidian source must be an object")
        if source.get("sha") != OBSIDIAN_SHA:
            raise SystemExit(f"{key} obsidian sha is {source.get('sha')!r}")
        if source.get("path") != "plugins/obsidian":
            raise SystemExit(f"{key} obsidian path is {source.get('path')!r}")
        if source.get("ref") != "wicked-main":
            raise SystemExit(f"{key} obsidian ref is {source.get('ref')!r}")
        if key == "copilot":
            if source.get("source") != "github":
                raise SystemExit(f"{key} obsidian source type is {source.get('source')!r}")
            if source.get("repo") != "Wicked-Sick-Ltd/obsidian-skills":
                raise SystemExit(f"{key} obsidian repo is {source.get('repo')!r}")
        else:
            if source.get("url") != "https://github.com/Wicked-Sick-Ltd/obsidian-skills.git":
                raise SystemExit(f"{key} obsidian url is {source.get('url')!r}")
            if source.get("source") != "git-subdir":
                raise SystemExit(f"{key} obsidian source type is {source.get('source')!r}")
        if key != "codex" and plugin.get("version") != "1.2.0":
            raise SystemExit(f"{key} obsidian version is {plugin.get('version')!r}")
        if key == "codex" and "version" in plugin:
            raise SystemExit("codex obsidian must not set version")
    skills_dir = ROOT / "plugins" / "obsidian" / "skills"
    found = tuple(sorted(path.name for path in skills_dir.iterdir() if path.is_dir()))
    if found != OBSIDIAN_SKILLS:
        raise SystemExit(f"vendored obsidian skills are {found}")
    vendored = (ROOT / "plugins" / "obsidian" / "VENDORED.md").read_text()
    if OBSIDIAN_SHA not in vendored:
        raise SystemExit("VENDORED.md is missing the obsidian pin")
    if (ROOT / "plugins" / "obsidian" / "held").exists():
        raise SystemExit("vendored obsidian contains held/")
    for held in OBSIDIAN_HELD:
        if (skills_dir / held).exists():
            raise SystemExit(f"vendored obsidian skills contain {held}")
    gemini = (ROOT / "gemini" / "README.md").read_text()
    if OBSIDIAN_SHA not in gemini or "obsidian" not in gemini:
        raise SystemExit("gemini/README.md must pin obsidian")


AGENT_WORKFLOWS_CURSOR_SHA = "9e38413cdd81bd5491dedebc99991910447d66ad"
AGENT_WORKFLOWS_HOST_REPOS = {
    "claude": "ai-claude-repo",
    "cursor": "ai-cursor-repo",
    "codex": "ai-codex-repo",
    "copilot": "ai-copilot-repo",
}


def agent_workflows_points_at_source_repos() -> None:
    """Pins name the host repo path. Claude is excluded. Cursor JSON stays an in-repo catalog."""
    readme = (ROOT / "README.md").read_text()
    gemini = (ROOT / "gemini" / "README.md").read_text()
    cursor_doc = (ROOT / "docs" / "cursor-integration.md").read_text()
    codex_doc = (ROOT / "docs" / "codex-integration.md").read_text()
    for label, text in (
        ("README.md", readme),
        ("gemini/README.md", gemini),
        ("docs/cursor-integration.md", cursor_doc),
        ("docs/codex-integration.md", codex_doc),
    ):
        for needle in ("agent-workflows", "ultracode", "ultrareview", "plugins/agent-workflows"):
            if needle not in text:
                raise SystemExit(f"{label} is missing {needle}")
        if "Claude Code has ultracode built in" not in text:
            raise SystemExit(f"{label} must record the ai-claude-repo exclusion")
    if AGENT_WORKFLOWS_CURSOR_SHA not in readme or AGENT_WORKFLOWS_CURSOR_SHA not in cursor_doc:
        raise SystemExit("catalogue must cite the ai-cursor-repo agent-workflows commit")
    inventory = next(
        (line for line in readme.splitlines() if line.startswith("| agent-workflows")),
        "",
    )
    if "ai-claude-repo" not in inventory or "ai-cursor-repo" not in inventory:
        raise SystemExit("README agent-workflows row must name ai-claude-repo and ai-cursor-repo")
    for key, path in validate.INDEXES.items():
        data = json.loads(path.read_text())
        matches = [plugin for plugin in data["plugins"] if plugin.get("name") == "agent-workflows"]
        if key in ("claude", "cursor") and matches:
            raise SystemExit(f"{key} catalog must not list agent-workflows")
        if len(matches) > 1:
            raise SystemExit(f"{key} lists agent-workflows more than once")
        for plugin in matches:
            blob = json.dumps(plugin)
            if "ai-claude-repo" in blob:
                raise SystemExit(f"{key} agent-workflows points at ai-claude-repo")
            source = plugin.get("source")
            if not isinstance(source, dict):
                raise SystemExit(f"{key} agent-workflows source must point at a repository")
            if source.get("path") != "plugins/agent-workflows":
                raise SystemExit(f"{key} agent-workflows path is {source.get('path')!r}")
            sha = source.get("sha")
            if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
                raise SystemExit(f"{key} agent-workflows sha is {sha!r}")
            host_repo = AGENT_WORKFLOWS_HOST_REPOS[key]
            pointer = json.dumps(source)
            if host_repo not in pointer:
                raise SystemExit(f"{key} agent-workflows source must name {host_repo}")


RED_TEAM_DESCRIPTION = (
    "Adversarial fact-check and pre-mortem for a claim, plan, launch or merge. "
    "The reviewer did not author the work and does not fix it. Instructions only."
)


def red_team_review_is_public() -> None:
    """The public skill is listed on every host and names no private source."""
    private = (
        "ultracode",
        "ultrareview",
        "ai-grok-repo",
        "ai-codex-repo",
        "ai-claude-repo",
        "ai-copilot-repo",
        "ai-cursor-repo",
        "ai-gemini-repo",
        "skills-port",
        "code-catalog",
    )
    forbidden_sha256 = {
        "0cf548e7d1b66f356aa4be3ef8884f0ec14158a3c09300fb08ed9651f39ddd25",
        "6c2a806e0d9ad255834ea0e03f159be06346c0d7718d6e1e31c330243509fdd6",
    }
    token_re = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|[A-Za-z0-9]+")
    for key, path in validate.INDEXES.items():
        data = json.loads(path.read_text())
        matches = [plugin for plugin in data["plugins"] if plugin.get("name") == "red-team-review"]
        if len(matches) != 1:
            raise SystemExit(f"{key} should list red-team-review once, found {len(matches)}")
        plugin = matches[0]
        if plugin.get("description") != RED_TEAM_DESCRIPTION:
            raise SystemExit(f"{key} red-team-review description drifted: {plugin.get('description')!r}")
        blob = json.dumps(plugin)
        for token in private:
            if token in blob:
                raise SystemExit(f"{key} red-team-review still contains {token}")
        for token in token_re.findall(blob):
            digest = hashlib.sha256(token.encode()).hexdigest()
            if digest in forbidden_sha256:
                raise SystemExit(f"{key} red-team-review contains a forbidden token")
        source = plugin.get("source")
        if key == "cursor":
            if source != "plugins/red-team-review":
                raise SystemExit(f"cursor source is {source!r}")
        elif source != "./plugins/red-team-review":
            raise SystemExit(f"{key} source is {source!r}")
        if key == "codex":
            if "version" in plugin:
                raise SystemExit("codex red-team-review must not set version")
            if plugin.get("category") != "Developer Tools":
                raise SystemExit(f"codex category is {plugin.get('category')!r}")
        else:
            if plugin.get("version") != "1.0.0":
                raise SystemExit(f"{key} version is {plugin.get('version')!r}")
            if plugin.get("category") != "developer-tools":
                raise SystemExit(f"{key} category is {plugin.get('category')!r}")
    manifest = ROOT / "plugins" / "red-team-review" / ".claude-plugin" / "plugin.json"
    version = json.loads(manifest.read_text())["version"]
    if version != "1.0.0":
        raise SystemExit(f"plugin.json version is {version!r}")
    extension = ROOT / "plugins" / "red-team-review" / "gemini-extension.json"
    if not extension.is_file():
        raise SystemExit("gemini-extension.json must sit at the plugin root")
    if "contextFileName" in extension.read_text():
        raise SystemExit("gemini-extension.json must not set contextFileName")
    skill = ROOT / "plugins" / "red-team-review" / "skills" / "red-team-review" / "SKILL.md"
    skill_text = skill.read_text()
    if "an independent code review" not in skill_text:
        raise SystemExit("skill must pair code review with an independent review")
    if "fresh, isolated contexts" not in skill_text or "same conversation" not in skill_text:
        raise SystemExit("skill must require fresh isolated prosecutor and defender contexts")
    if "independent session" not in skill_text:
        raise SystemExit("skill must ask for independent sessions when the host cannot isolate contexts")
    if "or passes" in skill_text:
        raise SystemExit("skill must not offer a same-conversation pass as isolation")
    if "the fallback when neither HOLDS nor FAILS is established" not in skill_text:
        raise SystemExit("UNPROVEN must be the fallback when neither HOLDS nor FAILS is established")
    if "material objection" not in skill_text:
        raise SystemExit("UNPROVEN must cover an unanswered material objection")
    if "ultracode" in skill_text or "ultrareview" in skill_text:
        raise SystemExit("skill must not name unpublished review workflows")
    package_readme = (ROOT / "plugins" / "red-team-review" / "README.md").read_text()
    if "does not run tools" in package_readme or "call a network" in package_readme:
        raise SystemExit("package README must not guarantee the review avoids tools or the network")
    if "Carrying out the review may" not in package_readme:
        raise SystemExit("package README must distinguish the package from the review")
    if "agy plugin install" not in package_readme:
        raise SystemExit("package README must include the Antigravity install")
    plugin_text = "\n".join(
        path.read_text() for path in (ROOT / "plugins" / "red-team-review").rglob("*") if path.is_file()
    )
    for token in private:
        if token in plugin_text:
            raise SystemExit(f"red-team-review plugin contains {token}")
    for token in token_re.findall(plugin_text):
        digest = hashlib.sha256(token.encode()).hexdigest()
        if digest in forbidden_sha256:
            raise SystemExit("red-team-review plugin contains a forbidden token")
    readme = (ROOT / "README.md").read_text()
    if not any(line.startswith("| red-team-review |") for line in readme.splitlines()):
        raise SystemExit("README inventory is missing red-team-review")
    gemini = (ROOT / "gemini" / "README.md").read_text()
    if "plugins/red-team-review" not in gemini:
        raise SystemExit("gemini/README.md must document red-team-review")
    section = gemini.split("## Red-team review", 1)[-1].split("\n## ", 1)[0]
    if "agy plugin install" not in section or "gemini extensions install" not in section:
        raise SystemExit("gemini/README.md must give Antigravity and Gemini CLI install steps")


def main() -> None:
    run_validate()
    relative_source_records_provenance()
    provenance_is_required_for_cursor_and_relative_sources()
    vendored_relative_source_is_allowed()
    amiga_decoding_is_public()
    red_team_review_is_public()
    pr_flow_pins_dedicated_repo()
    cursor_accepts_pr_flow_github_pin()
    obsidian_pin_is_the_merge_commit()
    cursor_rejects_github_source()
    codex_shape_validates()
    codex_native_sources()
    sha_pin_is_enforced()
    duplicate_names_fail_on_every_catalog()
    agent_workflows_points_at_source_repos()
    print("ok: validate tests passed")


if __name__ == "__main__":
    main()
