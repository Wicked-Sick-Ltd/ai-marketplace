# Wicked Sick AI marketplace

Cross-host catalogue for agent plugins published by [Wicked Sick Ltd](https://wickedsick.com). This repository is the **headline marketplace** for Cursor team marketplace review: import `Wicked-Sick-Ltd/ai-marketplace` and install the featured Cursor plugins from paths inside this repo.

Plugin behaviour lives in each plugin's own upstream repository. For Cursor, we **vendor** copies of the featured packages under `plugins/` so the Team Marketplace can resolve them as in-repo paths (Cursor does not SHA-pin remote Git sources in `.cursor-plugin/marketplace.json`). See each plugin's `VENDORED.md` for the upstream repo and commit.

Other hosts (Claude Code, Codex, Copilot, Gemini) use commit-pinned remote sources in their index files in this same repository.

## Featured plugins (Cursor)

| Plugin | What it does | Upstream |
| --- | --- | --- |
| **token-usage** | Token profiler for Cursor (and other agents): attribute usage to activities, query history via MCP, optional hook-based attribution. Estimates API list prices; not a subscription bill. | [token-usage](https://github.com/Wicked-Sick-Ltd/token-usage) |
| **publicuniverse** | Astronomy skills and a public MCP server: tonight's sky, lessons, fact-checking, and catalogue exploration. No API key required for the public MCP endpoint. | [public-universe](https://github.com/Wicked-Sick-Ltd/public-universe) |

Vendored paths: `plugins/token-usage/`, `plugins/publicuniverse/`.

## Install in Cursor (team marketplace)

1. **Admin:** In the Cursor dashboard, open **Plugins → Team Marketplaces → Import from Repo** and import `https://github.com/Wicked-Sick-Ltd/ai-marketplace`.
2. Turn on **Auto Refresh** if you want the catalog to track new commits on this repo.
3. Grant your team access to the marketplace.
4. **Developers:** **Cursor Settings → Plugins**, open the Wicked Sick marketplace, and install **token-usage** and/or **publicuniverse**. Enable the bundled MCP servers when prompted.

Detailed Cursor notes (formats, vendoring rationale, verification): [`docs/cursor-integration.md`](docs/cursor-integration.md).

**Requirements:** Python 3.9+ on the PATH for **token-usage** (stdio MCP and hooks). **publicuniverse** uses a remote HTTP MCP server documented in the plugin README.

## Other agents

```bash
# Claude Code (also used by Grok Build for this catalog)
claude plugin marketplace add Wicked-Sick-Ltd/ai-marketplace

# Codex CLI
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace --sparse .agents/plugins
```

Then install plugins by name from that marketplace (for example `claude plugin install token-usage@wickedsick`). Copilot CLI, Gemini, and Codex workflow details are in the host-specific index files listed below.

## Catalog indexes

| Client | File | Notes |
| --- | --- | --- |
| Cursor | `.cursor-plugin/marketplace.json` | Path-based; featured plugins vendored under `plugins/` |
| Claude Code / Grok | `.claude-plugin/marketplace.json` | GitHub SHA pins |
| ChatGPT / Codex | `.agents/plugins/marketplace.json` | Native Codex packages, SHA pins |
| Copilot CLI | `.github/plugin/marketplace.json` | SHA pins |
| Gemini | [`gemini/README.md`](gemini/README.md) | Upstream extension installs |

## Validation

```bash
python3 scripts/validate.py
```

CI runs the same check on every pull request.

## Demo app

A small Next.js + Prisma app lives in this tree for Cursor Cloud Agent environments. It is not part of the plugin catalog. See [`docs/demo-app.md`](docs/demo-app.md).

## Contributing

- [Contributor guide](CONTRIBUTING.md)
- [Agent instructions](AGENTS.md)
- [Security policy](SECURITY.md)

MIT licensed; see [LICENSE](LICENSE). Preserve third-party notices in vendored plugin directories.

Contact: [hello@wickedsick.com](mailto:hello@wickedsick.com)
