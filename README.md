# Wicked Sick AI marketplace

GitHub catalogs for the agent plugins we actually install. Plugins are **not** vendored here; each index points at a source repo, pinned by commit SHA.

This is not a Traefik module and not a substitute for `CLAUDE.md` / `AGENTS.md` in product repos. See the plan in [traefik-laravel-forge](https://github.com/Wicked-Sick-Ltd/traefik-laravel-forge/blob/master/docs/cross-ai-marketplace-plan.md).

## Add the marketplace

```bash
# Claude Code (Grok Build reads this catalog too)
claude plugin marketplace add Wicked-Sick-Ltd/ai-marketplace

# ChatGPT Work / Codex CLI
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace --sparse .agents/plugins
```

- **Cursor:** Teams or Enterprise → marketplace → connect this GitHub repository.
- **Copilot:** `"chat.plugins.marketplaces": ["Wicked-Sick-Ltd/ai-marketplace"]`
- **Gemini CLI:** no catalog file. Install from the plugin repo: see [`gemini/README.md`](gemini/README.md).
- **Grok:** add the Claude marketplace above. A Grok-native index is omitted on purpose.

Then install individual plugins (Claude):

```bash
claude plugin install token-usage@wickedsick
```

## Indexes

| Client | File | Plugins listed today |
| --- | --- | --- |
| Claude Code / Grok | `.claude-plugin/marketplace.json` | `token-usage` (pinned) |
| Cursor | `.cursor-plugin/marketplace.json` | none yet |
| ChatGPT / Codex | `.agents/plugins/marketplace.json` | none yet |
| Copilot | `.github/plugin/marketplace.json` | none yet |
| Gemini | [`gemini/README.md`](gemini/README.md) | none yet |

`token-usage` is Claude-only until it can parse that host's session logs (or the listing is explicitly "Claude transcripts only"). Workflow skills can be added to every Agent Skills catalog.

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
2. Pin a **full 40-character commit SHA** (and a tag `ref` when one exists). Do not float on `main`.
3. List it only on marketplaces where it has a real runtime.
4. Run `python3 scripts/validate.py`.

Owner: Wicked Sick Ltd (`craig@wickedsick.com`).
