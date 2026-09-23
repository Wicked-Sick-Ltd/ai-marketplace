# Contributing

This repo is a catalog. Plugin behaviour changes belong in the plugin's own repository.

## Listing a plugin

1. Confirm the plugin has a real runtime on that host (skills/MCP that actually work there).
2. Add an entry to the matching index only:
   - Claude / Grok: `.claude-plugin/marketplace.json`
   - Cursor: `.cursor-plugin/marketplace.json` (in-repo path `source`; see below)
   - ChatGPT / Codex: `.agents/plugins/marketplace.json`
   - Copilot: `.github/plugin/marketplace.json`
   - Gemini: a row in `gemini/README.md` (no JSON catalog)
3. For Claude / Copilot remotes: set `source.sha` to a full 40-character commit. Prefer a release tag as `ref` when one exists; SHA still wins. Codex entries use a repo URL without `ref` or `sha`; record the reviewed upstream revision in the integration documentation.
4. For Cursor: `source` must be a relative directory in this repository (string, or `{ "path": "…" }`). Cursor does not clone a GitHub SHA from this file. Plugin shims (`.cursor-plugin/plugin.json`, root `mcp.json`) belong in the plugin's own repo. Team Marketplace import of `claude-repo` is documented in `docs/cursor-integration.md`.
5. Run `python3 scripts/validate.py`.

Do not copy plugin files into this repository.

## The in-tree demo app

The Next.js + Prisma demo app in this tree exists so the Cursor Cloud Agent environment has something to install and run ([`docs/demo-app.md`](docs/demo-app.md)). Its listings UI is not a catalog and editing it never changes what a host installs; catalog changes are edits to the index files above plus `python3 scripts/validate.py`. CI validates the catalogs only, so demo-app changes are unenforced there — run `npm run lint` / `npm run typecheck` yourself.
