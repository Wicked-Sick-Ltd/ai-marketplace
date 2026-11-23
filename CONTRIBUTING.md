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
3. For Claude, Codex and Copilot remotes: set `source.sha` to a full 40-character commit. Prefer a release tag as `ref` when one exists; SHA still wins. Codex uses `url` for a root package and `git-subdir` with `path` for a native package inside a vendor repository. Verify installation with the actual Codex CLI in a temporary `CODEX_HOME`. A plugin vendored in this public repository because its upstream is private (`amiga-decoding`) uses a relative source instead: `./plugins/<name>` on Claude, Codex and Copilot, and `plugins/<name>` on Cursor. Its `VENDORED.md` records the upstream commit. A first-party package published in this repository (`red-team-review`) uses that same relative source. Its `VENDORED.md` records that this directory is the published copy and that there is no separate upstream pin. Do not invent a SHA for it, and do not point the catalogs at a private sibling checkout. An upstream commit is the backtick sha on that file's `Content source`, `Source commit`, or `Pinned checkout` line. A hash on another line, including a skill-tree hash, is not the pin. Cursor checks the same file after `metadata.pluginRoot` is applied. `pr-flow` is a root package of `Wicked-Sick-Ltd/pr-flow`: Claude uses `github` + `repo` + `sha`, and Codex and Copilot use `url` + `sha`, with no subdirectory.
4. For Cursor: `source` must be a relative directory in this repository (string, or `{ "path": "…" }`), except `pr-flow`, whose source is the same whole-repo `github` pin as Claude. Cursor's published importer still resolves `source` as a directory in the imported repository; importing `https://github.com/Wicked-Sick-Ltd/pr-flow` is how a team installs that plugin in Cursor. The other featured packages are the vendored trees under `plugins/`, recorded in each `VENDORED.md`. Team Marketplace import of this repository is documented in `docs/cursor-integration.md`.
5. Run `python3 scripts/validate.py` and `python3 scripts/test_validate.py`.

Do not add a plugin directory except as a Cursor vendored package with a `VENDORED.md`, or as a first-party package published in this repository whose `VENDORED.md` records that there is no separate upstream pin. Do not edit vendored runtime files in place. The published first-party skill is edited here.

## The in-tree demo app

The Next.js 15.5.28 + Prisma demo app in this tree exists so the Cursor Cloud Agent environment has something to install and run ([`docs/demo-app.md`](docs/demo-app.md)). Its listings UI is not a catalog and editing it never changes what a host installs; catalog changes are edits to the index files above plus `python3 scripts/validate.py`. CI runs that validator and the two Python smoke tests, so demo-app changes are unenforced there — run `npm run lint` / `npm run typecheck` yourself.
