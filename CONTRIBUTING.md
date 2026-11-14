# Contributing

This repo is a catalog. Plugin behaviour changes belong in the plugin's own repository.

## Listing a plugin

1. Confirm the plugin has a real runtime on that host (skills/MCP that actually work there).
2. Add an entry to the matching index only:
   - Claude / Grok: `.claude-plugin/marketplace.json`
   - Cursor: `.cursor-plugin/marketplace.json` (in-repo path `source`; see below)
   - ChatGPT / Codex: `.agents/plugins/marketplace.json`
   - Copilot: `.github/plugin/marketplace.json`
   - Antigravity / Gemini: a section in `gemini/README.md` (no shared remote JSON catalog)
3. For Claude, Codex and Copilot remotes: set `source.sha` to a full 40-character commit. Prefer a release tag as `ref` when one exists; SHA still wins. Codex uses `url` for a root package and `git-subdir` with `path` for a native package inside a vendor repository. Verify installation with the actual Codex CLI in a temporary `CODEX_HOME`. A plugin vendored in this public repository because its upstream is private (`amiga-decoding`) uses a relative source instead: `./plugins/<name>` on Claude, Codex and Copilot, and `plugins/<name>` on Cursor.
4. For Cursor: `source` must be a relative directory in this repository (string, or `{ "path": "…" }`). Cursor does not clone a GitHub SHA from this file. Featured packages are the vendored trees under `plugins/`, recorded in each `VENDORED.md`. Team Marketplace import of this repository is documented in `docs/cursor-integration.md`.
5. Run `python3 scripts/validate.py` and `python3 scripts/test_validate.py`.

Do not add a plugin directory except as a Cursor vendored package with a `VENDORED.md`. Do not edit vendored runtime files in place.

## The in-tree demo app

The Next.js 15.5.28 + Prisma demo app in this tree exists so the Cursor Cloud Agent environment has something to install and run ([`docs/demo-app.md`](docs/demo-app.md)). Its listings UI is not a catalog and editing it never changes what a host installs; catalog changes are edits to the index files above plus `python3 scripts/validate.py`. CI runs that validator and the two Python smoke tests, so demo-app changes are unenforced there — run `npm run lint` / `npm run typecheck` yourself.
