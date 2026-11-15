# Cursor team marketplace

How to install and review **Wicked Sick** plugins in Cursor using this repository.

Official Cursor docs: [Plugins](https://cursor.com/docs/plugins) and [Plugins reference](https://cursor.com/docs/reference/plugins).

## What this repo is

`Wicked-Sick-Ltd/ai-marketplace` is a **catalogue repository**. It lists plugins per host (Claude, Codex, Copilot, Gemini, Cursor) and, for Cursor, contains **vendored copies** of `token-usage`, `publicuniverse`, and `amiga-decoding` under `plugins/`. `pr-flow` is pinned to its own repository.

For marketplace review, the headline install path is:

1. Import **`Wicked-Sick-Ltd/ai-marketplace`** as a Cursor Team Marketplace.
2. Install plugins from the catalog — today **token-usage**, **publicuniverse**, **amiga-decoding** and **obsidian**. Install **pr-flow** by importing `Wicked-Sick-Ltd/pr-flow`.

Upstream source code and releases remain in each plugin's own GitHub repository; vendored trees record the exact commit in `plugins/<name>/VENDORED.md`.

## Why plugins are vendored for Cursor

Claude-style catalogs in this repo pin plugins with a GitHub `repo` + 40-character `sha`. Cursor's published importer does not resolve that shape: each `plugins[].source` it loads must be a **relative path inside the imported git repo**. Cursor then loads:

- `<source>/.cursor-plugin/plugin.json` (Cursor plugin), or
- `<source>/plugin.json` (Agent Plugins 1.0)

So those featured plugins are copied into `plugins/` here (same approach as `plugins/publicuniverse/`). `scripts/validate.py` rejects GitHub SHA pins in the Cursor index except `pr-flow`.

`pr-flow`'s canonical repository is the plugin root. The Cursor entry uses the same whole-repo shape as Claude:

```json
{"source":"github","repo":"Wicked-Sick-Ltd/pr-flow","sha":"54de23f8d48f1c5c706046b068db139867eea474"}
```

Cursor's published team-marketplace importer still resolves `source` as a directory inside the imported repository ([Plugins reference](https://cursor.com/docs/reference/plugins)). Import `https://github.com/Wicked-Sick-Ltd/pr-flow` when the team marketplace must serve that plugin. GitHub access to the private repository is required until it is published.

**Alternative:** Import a plugin's upstream repository directly with **Add to Marketplace** (repo URL). That avoids vendoring but splits installs across multiple marketplace imports. This catalog keeps a **single** import for the vendored plugins.

## Install steps (humans)

### 1. Import the team marketplace

1. Cursor dashboard → **Plugins** → **Team Marketplaces** → **Import from Repo**.
2. Repository: `Wicked-Sick-Ltd/ai-marketplace`.
3. Enable **Auto Refresh** if you want the index to follow new commits (subject to Cursor's refresh interval).

### 2. Access and defaults

1. Assign marketplace access (whole team or groups).
2. Choose **Default Off**, **Default On**, or **Required** per plugin policy.

### 3. Install on a developer machine

1. **Cursor Settings → Plugins** → open the Wicked Sick marketplace.
2. Install **token-usage**, **publicuniverse**, **amiga-decoding** and/or **obsidian**.
3. For **pr-flow**, import `https://github.com/Wicked-Sick-Ltd/pr-flow` (commit `54de23f8d48f1c5c706046b068db139867eea474`). The repository root is the Cursor plugin.
4. Approve bundled MCP servers when Cursor prompts.
5. For **token-usage**, ensure `python3` is on the PATH (hooks and stdio MCP). Cloud Agents do not pick up this install automatically; see the token-usage section below.

Skills are available under the plugin's skill entries; MCP tools appear when the server is connected.

## Featured plugins

### token-usage (0.9.0)

- **Purpose:** Attribute token usage to activities, inspect session and history, optional Cursor hook attribution, read-only MCP tools.
- **Vendored path:** `plugins/token-usage/`
- **Manifest:** `plugins/token-usage/.cursor-plugin/plugin.json`
- **Upstream commit in this tree:** `39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c` (see `plugins/token-usage/VENDORED.md`). The v0.9.0 tag is the earlier `fe998547b0dfa9472e2a80cb9beee9bae3018575`.
- **Logo:** `plugins/token-usage/assets/logo.svg`
- **Category:** monitoring

Costs shown are API list-price **estimates**, not subscription charges.

**Cloud Agents.** A cloud VM does not inherit the developer's Cursor plugins. This vendored copy reports a Cloud Agent export when you pass the `.json` path (`--runtime cursor` or MCP `transcript`). A file without `usage` / `tokenUsage` is `activity_only`. The hook on the VM (`cursor-hook` in `.cursor/hooks.json`, or the plugin if the image has it) is the higher-confidence source, and that ledger stays on the VM. Upstream `main` (`7638fb1b07751f1bfd2d4d6cc535aad71280f905`) adds a separate `cursor-cloud` Admin API runtime. It is not in this directory. Setup, environment variables and limits: [`token-usage.md`](token-usage.md).

### publicuniverse (0.4.2)

- **Purpose:** Astronomy workflows (tonight's sky, lessons, fact-check, and more) via skills and a public HTTP MCP server.
- **Vendored path:** `plugins/publicuniverse/`
- **Manifest:** `plugins/publicuniverse/.cursor-plugin/plugin.json` and `plugins/publicuniverse/plugin.json`
- **Upstream commit in this tree:** `8b1e7b348067194d5a400f6bf16a0144a51d74aa` (see `plugins/publicuniverse/VENDORED.md`)
- **MCP URL in this copy:** `https://api.publicuniverse.net/mcp`
- **Logo:** `plugins/publicuniverse/assets/icon.svg`
- **Category:** education

`https://api.sol.wickedsick.com/mcp` still answers. Claude, Codex and Copilot pins are 0.4.1 and still configure that alias. Positions and catalogue data are approximate and not for telescope pointing.

### pr-flow (1.1.0)

- **Purpose:** Open a finished pull request ready for review, wait until CI and reviewer bots finish, fix or answer every finding, and land the change. Skills: `landing-prs` and `pr`. Helper: `pr-wait.sh`. A draft is only for work still in progress, Critical-tier PRs included (Craig, 5 Nov 2026). A finished PR left as draft is a red flag.
- **Source:** `Wicked-Sick-Ltd/pr-flow` at `54de23f8d48f1c5c706046b068db139867eea474`. Claude, Codex, Copilot and Cursor pin that same commit. Manifests in that tree, including `.cursor-plugin/plugin.json`, are 1.1.0. This repository does not vendor the tree.
- **Cursor install:** import `https://github.com/Wicked-Sick-Ltd/pr-flow`. GitHub access is required while the repository is private.
- **Category:** developer-tools

Requires authenticated `gh`, Bash and `jq`. Review comments from Claude, Bugbot, Copilot, CodeQL and Semgrep are in scope.

### amiga-decoding (1.0.0)

- **Purpose:** Evidence-led Amiga ADF extraction and decompilation to exhaustion, with separate disk, content and semantic coverage. Skill: `amiga-adf-decompile`. Instructions only.
- **Vendored path:** `plugins/amiga-decoding/`
- **Manifest:** `plugins/amiga-decoding/.cursor-plugin/plugin.json` (version 1.0.0)
- **Provenance:** `plugins/amiga-decoding/VENDORED.md` (`5ba30a22df385e75135101e3f886471ee0e9ee9d`). Claude, Codex, Copilot and Gemini install this same directory. No icon.
- **Category:** developer-tools

### obsidian (1.2.0)

- **Purpose:** Vetted Obsidian format skills: Obsidian Flavored Markdown, Bases (`.base`) and JSON Canvas. Skills: `obsidian-markdown`, `obsidian-bases`, `json-canvas`. Instruction-only; no shell, network or credentials.
- **Vendored path:** `plugins/obsidian/`
- **Manifest:** `plugins/obsidian/.cursor-plugin/plugin.json` (version 1.2.0)
- **Provenance:** `plugins/obsidian/VENDORED.md` (`cd51b7076a1207c805cf1d95da4c56cb96bbe859`, `wicked-main` `plugins/obsidian`). Upstream [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills) (MIT, Copyright (c) 2026 Steph Ango). Claude, Codex and Copilot pin that same commit. Gemini installs it from the repository root. No shell tools.
- **Logo:** `plugins/obsidian/assets/icon.png`
- **Category:** productivity

## Catalog file

The Cursor index is `.cursor-plugin/marketplace.json` (`name: wickedsick`). Marketplace owner contact: **hello@wickedsick.com**.

## Local smoke test (optional)

Copy a vendored plugin directory to `~/.cursor/plugins/local/<name>/`, reload Cursor, and confirm **Settings → Plugins** shows skills, hooks (token-usage), and MCP. Enterprise policies may disable local imports.

## Publishing to the public Cursor Marketplace

Public listing at [cursor.com/marketplace/publish](https://cursor.com/marketplace/publish) is separate from team marketplace import. Submit when the team catalog and upstream repos are ready; this document does not perform publication.

## Not in this Cursor catalog

Workflow plugins that live only in private org repos, hook-only fleet templates, and plugins without a Cursor runtime are intentionally omitted from `.cursor-plugin/marketplace.json`. Other hosts may still list them with SHA pins in their index files in this repository.
