# Wicked Sick AI marketplace

GitHub catalogs for the agent plugins we actually install. Plugins are **not** vendored here. Claude / Copilot indexes pin a source repo by commit SHA; Codex's Agent Plugins schema has no ref/sha field, so its entries name a repo URL and Codex resolves the default branch. Cursor indexes use in-repo paths; the Team Marketplace imports the git repo that actually contains the plugin directories.

This is not a Traefik module and not a substitute for `CLAUDE.md` / `AGENTS.md` in product repos. See the plan in [traefik-laravel-forge](https://github.com/Wicked-Sick-Ltd/traefik-laravel-forge/blob/master/docs/cross-ai-marketplace-plan.md).

The tree also holds a small Next.js + Prisma **demo app**, in-tree so the Cursor Cloud Agent environment has something to install and run. It is not plugin source, and its listings UI is not a catalog — the catalogs are the JSON indexes below. CI validates those catalogs only, so the demo app is unenforced there. Setup and commands: [`docs/demo-app.md`](docs/demo-app.md).

## Add the marketplace

```bash
# Claude Code (Grok Build reads this catalog too)
claude plugin marketplace add Wicked-Sick-Ltd/ai-marketplace

# ChatGPT Work / Codex CLI
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace --sparse .agents/plugins
```

- **Cursor:** do **not** expect Claude-style GitHub SHA pins in `.cursor-plugin/marketplace.json`. Cursor Team Marketplaces import a git repo and resolve each plugin as a **path inside that repo**. Import [`claude-repo`](https://github.com/Wicked-Sick-Ltd/claude-repo) once those plugins have Cursor/Agent Plugins manifests. This catalog's Cursor index stays empty until we host a Cursor pack here. Details: [`docs/cursor-integration.md`](docs/cursor-integration.md).
- **Copilot:** `"chat.plugins.marketplaces": ["Wicked-Sick-Ltd/ai-marketplace"]`
- **Gemini CLI:** no catalog file. Install from the plugin repo: see [`gemini/README.md`](gemini/README.md).
- **Grok:** add the Claude marketplace above. A Grok-native index is omitted on purpose.

Then install individual plugins (Claude):

```bash
claude plugin install token-usage@wickedsick
claude plugin install wizzo-fleet-presence@wickedsick
```

## Indexes

| Client | File | Plugins listed today |
| --- | --- | --- |
| Claude Code / Grok | `.claude-plugin/marketplace.json` | `token-usage`, `wizzo-fleet-presence` (pinned) |
| Cursor | `.cursor-plugin/marketplace.json` | none here (path-based catalog; live plugins stay in `claude-repo`; the `wizzo-fleet-presence` Cursor pack is a hooks template in `acsendr`, not a plugin) |
| ChatGPT / Codex | `.agents/plugins/marketplace.json` | `wizzo-fleet-presence` (repo URL into `codex-repo`; Codex has no sha field, so this isn't a pin — see `AGENTS.md`) |
| Copilot | `.github/plugin/marketplace.json` | none yet |
| Gemini | [`gemini/README.md`](gemini/README.md) | none — no session-lifecycle hooks to bind to |

`token-usage` is Claude-only until it can parse that host's session logs (or the listing is explicitly "Claude transcripts only"). `.cursor/environment.json` on a plugin repo is Cloud Agent setup, not a Cursor plugin.

The Codex `wizzo-fleet-presence` installer (`codex-repo/scripts/install-presence-hooks.py`) also takes `--home <codex-home>` and `--coordctl <path>` when acsendr isn't at one of its two default locations.

Workflow skills (`session-lifecycle`, `estate-maintenance`, `product-lifecycle`) live in [`claude-repo`](https://github.com/Wicked-Sick-Ltd/claude-repo) today with Claude manifests only. Port them with Agent Skills + `.cursor-plugin/plugin.json` (and root `mcp.json` where needed), then list them on a Cursor Team Marketplace — see [`docs/cursor-integration.md`](docs/cursor-integration.md). After that, the same portable floor can go on every Agent Skills catalog (Codex, Copilot, Gemini).

## Horses for courses

| Job | Default agent |
| --- | --- |
| Day-to-day coding, Cloud Agents | Cursor |
| Claude-native plugins, Cowork, hooks | Claude Code |
| ChatGPT app / native CLI | ChatGPT Work + Codex CLI |
| VS Code, PRs | Copilot |
| Gemini CLI / Google-shaped work | Gemini |
| Terminal agent that can reuse Claude plugins | Grok |

## Add a plugin

1. Keep the plugin in its own repository.
2. Pin a **full 40-character commit SHA** (and a tag `ref` when one exists) on Claude / Copilot remotes. Do not float on `main`. Codex's Agent Plugins schema has no ref/sha field — its entries name the repo URL and resolve the default branch instead; the SHA of record is the source repo's merge commit. Cursor entries use in-repo paths, not SHA pins — [`docs/cursor-integration.md`](docs/cursor-integration.md).
3. List it only on marketplaces where it has a real runtime.
4. Run `python3 scripts/validate.py`.

Owner: Wicked Sick Ltd (`craig@wickedsick.com`).
