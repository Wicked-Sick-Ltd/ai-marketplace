# Wicked Sick AI marketplace

Repository migration: [plan and execution record](docs/ai-vendor-repository-migration.md).

For each machine: [local migration broadcast prompt](docs/local-ai-repository-migration-prompt.md).

GitHub catalogs for the agent plugins we actually install. Plugins are **not** vendored here. Claude, Codex and Copilot indexes pin source repositories by commit SHA. Codex selects native packages with `url` or `git-subdir` sources. Cursor indexes use in-repo paths; the Team Marketplace imports the git repo that actually contains the plugin directories.

This is not a Traefik module and not a substitute for `CLAUDE.md` / `AGENTS.md` in product repos. See the plan in [traefik-laravel-forge](https://github.com/Wicked-Sick-Ltd/traefik-laravel-forge/blob/master/docs/cross-ai-marketplace-plan.md).

## Repository custom properties

`Wicked-Sick-Ltd` and `wizmediagg` share one **repository** custom-property schema (live 2026-09-28). Plugins and sessions use those property names and allowed values — automation membership, stack, lifecycle, service tier, sweep priority, and branch workflow — instead of a private tag list.

Repository custom properties, issue labels, and organization-object properties are three different GitHub objects. Vocabulary, the values API, and the split: [`docs/repository-custom-properties.md`](docs/repository-custom-properties.md). Sessions also load it from [`AGENTS.md`](AGENTS.md) and [`CLAUDE.md`](CLAUDE.md).

The tree also holds a small Next.js + Prisma **demo app**, in-tree so the Cursor Cloud Agent environment has something to install and run. It is not plugin source, and its listings UI is not a catalog — the catalogs are the JSON indexes below. CI validates those catalogs only, so the demo app is unenforced there. Setup and commands: [`docs/demo-app.md`](docs/demo-app.md).

## Vendor ownership

| Host | Private repository |
| --- | --- |
| Claude | [ai-claude-repo](https://github.com/Wicked-Sick-Ltd/ai-claude-repo) |
| Codex | [ai-codex-repo](https://github.com/Wicked-Sick-Ltd/ai-codex-repo) |
| Cursor | [ai-cursor-repo](https://github.com/Wicked-Sick-Ltd/ai-cursor-repo) |
| Gemini | [ai-gemini-repo](https://github.com/Wicked-Sick-Ltd/ai-gemini-repo) |
| Copilot | [ai-copilot-repo](https://github.com/Wicked-Sick-Ltd/ai-copilot-repo) |
| Grok | [ai-grok-repo](https://github.com/Wicked-Sick-Ltd/ai-grok-repo) |

These repositories own host setup and first-party workflow material. Third-party
Ponytail runtime source remains upstream; the indexes below remain the discovery
surface. Private guides require organisation access.

## Add the marketplace

```bash
# Claude Code (Grok Build reads this catalog too)
claude plugin marketplace add Wicked-Sick-Ltd/ai-marketplace

# ChatGPT Work / Codex CLI
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace --sparse .agents/plugins
```

- **Cursor:** do **not** expect Claude-style GitHub SHA pins in `.cursor-plugin/marketplace.json`. Cursor Team Marketplaces import a git repo and resolve each plugin as a **path inside that repo**. Import [`ai-claude-repo`](https://github.com/Wicked-Sick-Ltd/ai-claude-repo) once those plugins have Cursor/Agent Plugins manifests. This catalog's Cursor index stays empty until we host a Cursor pack here. Details: [`docs/cursor-integration.md`](docs/cursor-integration.md).
- **Copilot:** `"chat.plugins.marketplaces": ["Wicked-Sick-Ltd/ai-marketplace"]`
- **Gemini CLI:** no catalog file. Install from the plugin repo: see [`gemini/README.md`](gemini/README.md).
- **Grok:** add the Claude marketplace above. A Grok-native index is omitted on purpose.

Then install individual plugins (Claude):

```bash
claude plugin install token-usage@wickedsick
claude plugin install wizzo-fleet-presence@wickedsick
claude plugin install ponytail@wickedsick
```

Then install the Codex workflows:

```bash
codex plugin add onboarding@wickedsick
codex plugin add session-lifecycle@wickedsick
codex plugin add pr-flow@wickedsick
codex plugin add estate-maintenance@wickedsick
codex plugin add product-lifecycle@wickedsick
codex plugin add token-usage@wickedsick
codex plugin add ponytail@wickedsick
# Optional, on machines participating in the fleet:
codex plugin add wizzo-fleet-presence@wickedsick
```

First-party workflows require access to the private `ai-codex-repo`; token-usage
and Ponytail use their public upstream repositories. Review hooks with `/hooks`,
then start a new session. Each machine needs its own authentication and hook
trust. Install each plugin from one marketplace to avoid duplicate hooks.
The vendor repository owns [setup, prerequisites and migration](https://github.com/Wicked-Sick-Ltd/ai-codex-repo/blob/main/docs/codex-plugin-parity.md).

Installation troubleshooting and tested package behavior: [Codex integration](docs/codex-integration.md).

## Indexes

| Client | File | Plugins listed today |
| --- | --- | --- |
| Claude Code / Grok | `.claude-plugin/marketplace.json` | `token-usage`, `wizzo-fleet-presence`, `ponytail` (pinned; Ponytail's Grok runtime is skills-only) |
| Cursor | `.cursor-plugin/marketplace.json` | none here (path-based catalog; live plugins stay in `ai-claude-repo`; the `wizzo-fleet-presence` Cursor pack is a hooks template in `acsendr`, not a plugin) |
| ChatGPT / Codex | `.agents/plugins/marketplace.json` | `onboarding`, `session-lifecycle`, `pr-flow`, `estate-maintenance`, `product-lifecycle`, `token-usage`, `ponytail`, `wizzo-fleet-presence` (native packages, pinned) |
| Copilot CLI | `.github/plugin/marketplace.json` | `ponytail` (pinned; Copilot-specific commands, skills and hooks) |
| Gemini | [`gemini/README.md`](gemini/README.md) | `ponytail` (upstream extension) |

Ponytail setup, vendor ownership, revision tracking and runtime limitations:
[`docs/ponytail.md`](docs/ponytail.md).

`token-usage` has native Claude Code (and Cowork), Codex and Cursor runtimes. Codex
token counts use recorded usage; costs are labelled API estimates, not subscription
charges. Its Cursor package (`.cursor-plugin/plugin.json`) lives in the token-usage
repository, so add that repository to a Cursor Team Marketplace with **Add to
Marketplace**; this repo's path-based Cursor index cannot point at another repository.
It is not listed for hosts without a supported runtime (Copilot, Gemini).

Codex workflow skills are maintained in
[`ai-codex-repo`](https://github.com/Wicked-Sick-Ltd/ai-codex-repo), using
`ai-claude-repo` as their reference. This index only selects those packages.
The fleet plugin replaces the older config-hook installer: remove its managed
presence block before trusting the native plugin, so events are not sent twice.
Other host ports retain their vendor-specific requirements; see
[`docs/cursor-integration.md`](docs/cursor-integration.md).

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
2. Pin a **full 40-character commit SHA** on Claude, Codex and Copilot remotes. A release tag `ref` may accompany it; SHA wins. Codex supports both repository-root and `git-subdir` packages. Cursor entries use in-repo paths; see [`docs/cursor-integration.md`](docs/cursor-integration.md).
3. List it only on marketplaces where it has a real runtime.
4. Run `python3 scripts/validate.py`.

Owner: Wicked Sick Ltd (`craig@wickedsick.com`).

<!-- repository-guidance:begin -->
## Contributing and agent guidance

- [Contributor guide](CONTRIBUTING.md): development workflow and validation.
- [Agent instructions](AGENTS.md): shared guidance for Codex and other coding agents.
- [Security policy](SECURITY.md): private vulnerability reporting.

## Repository license

MIT licensed; see [LICENSE](LICENSE). Preserve third-party notices.
<!-- repository-guidance:end -->
