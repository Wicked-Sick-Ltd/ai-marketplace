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
3. For Claude / Codex / Copilot remotes: set `source.sha` to a full 40-character commit. Prefer a release tag as `ref` when one exists; SHA still wins.
4. For Cursor: `source` must be a relative directory in this repository (string, or `{ "path": "…" }`). Cursor does not clone a GitHub SHA from this file. Plugin shims (`.cursor-plugin/plugin.json`, root `mcp.json`) belong in the plugin's own repo. Team Marketplace import of `claude-repo` is documented in `docs/cursor-integration.md`.
5. Run `python3 scripts/validate.py`.

Do not copy plugin files into this repository.
