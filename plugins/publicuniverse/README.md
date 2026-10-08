# Public Universe plugin

Free astronomy tools and seven reusable workflows for **Claude Code, Cursor, Codex, ChatGPT, Gemini CLI, GitHub Copilot, Grok and any MCP client**. Explore catalogue data, prepare lessons, explain objects and plan an evening of stargazing with [Public Universe](https://publicuniverse.net), a pro bono astronomy service by Wicked Sick Ltd.

- Plugin / package name: **`publicuniverse`** (display name: Public Universe)
- MCP server name: **`publicuniverse`**
- Repository: `https://github.com/Wicked-Sick-Ltd/publicuniverse-plugin` (formerly `solar-plugin`; GitHub redirects the old URL)
- Licence: MIT, © Wicked Sick Limited. Please credit "Wicked Sick Ltd" when you reuse it (see [NOTICE](NOTICE)).

## Remote MCP server

| Setting | Value |
| --- | --- |
| Name | `publicuniverse` |
| Transport | Streamable HTTP |
| URL | `https://api.sol.wickedsick.com/mcp` |
| Authentication | None (free public service) |

> **Status:** the REST API behind this server is live, but the `/mcp` endpoint is not yet routed on the production origin (it returns HTTP 404 from the API application, not from Cloudflare). Skills install and load everywhere; live tool calls work once the endpoint is deployed. See the [validation record](docs/validation.md). The planned long-term URL is `https://api.publicuniverse.net/mcp`; this package will switch only after that host is live.

## Install

Pick **one** route per client: the full plugin (tools + skills) or MCP-only (tools only). Don't install both.

### Claude Code

```sh
/plugin marketplace add https://github.com/Wicked-Sick-Ltd/publicuniverse-plugin.git
/plugin install publicuniverse@publicuniverse
```

Or via the Wicked Sick catalogue: `/plugin marketplace add Wicked-Sick-Ltd/ai-marketplace` then `/plugin install publicuniverse@wickedsick`. Local checkout: `claude --plugin-dir /path/to/publicuniverse-plugin`. MCP only:

```sh
claude mcp add --transport http publicuniverse https://api.sol.wickedsick.com/mcp
```

Try `/publicuniverse:tonight-sky`. Details: [docs/clients.md](docs/clients.md#claude-code).

### Cursor

Install from the Cursor marketplace once listed, or import `Wicked-Sick-Ltd/ai-marketplace` as a team marketplace. Local: copy this repository to `~/.cursor/plugins/local/publicuniverse/` and reload. MCP only: merge [clients/cursor.json](clients/cursor.json) into `~/.cursor/mcp.json`. Details: [docs/clients.md](docs/clients.md#cursor-full-plugin).

### Codex (CLI, desktop, IDE)

```sh
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace --sparse .agents/plugins
codex plugin add publicuniverse@wickedsick
```

MCP only: `codex mcp add publicuniverse --url https://api.sol.wickedsick.com/mcp`, or merge [clients/codex.toml](clients/codex.toml) into `~/.codex/config.toml`. Details: [docs/openai.md](docs/openai.md#codex).

### ChatGPT

Developer mode → add an MCP connection named **Public Universe** with the URL above (no auth). Skills are not imported by an MCP connection. Details: [docs/openai.md](docs/openai.md#chatgpt).

### Gemini CLI

```sh
gemini extensions install https://github.com/Wicked-Sick-Ltd/publicuniverse-plugin
```

Pin a reviewed release with `--ref <tag-or-sha>`. Details: [docs/clients.md](docs/clients.md#gemini-cli).

### GitHub Copilot (CLI and VS Code)

```sh
copilot plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
copilot plugin install publicuniverse@wickedsick
```

VS Code MCP only: merge [clients/vscode.json](clients/vscode.json) into `.vscode/mcp.json`. Details: [docs/clients.md](docs/clients.md#github-copilot-cli-full-plugin).

### Grok (Grok CLI, grok.com, xAI API)

Grok CLI reads Claude Code marketplaces and plugins, so the Claude route above works as is. Or:

```sh
grok plugin install Wicked-Sick-Ltd/publicuniverse-plugin   # full plugin (or a local path)
grok mcp add --transport http publicuniverse https://api.sol.wickedsick.com/mcp   # tools only
```

On grok.com, add a custom MCP connector with the URL above. Via the xAI API, add `{"type": "mcp", "server_url": "https://api.sol.wickedsick.com/mcp", "server_label": "publicuniverse"}` to `tools`. Details: [docs/clients.md](docs/clients.md#grok).

### Any other MCP client

Add a remote **Streamable HTTP** server named `publicuniverse` with the URL above and no authentication. Most clients accept:

```json
{ "mcpServers": { "publicuniverse": { "type": "http", "url": "https://api.sol.wickedsick.com/mcp" } } }
```

To use the skills without a plugin system, copy whole folders from `skills/` into your client's Agent Skills directory (see [docs/clients.md](docs/clients.md#skills-without-a-full-plugin)).

## Skills

| Skill | Use it for |
| --- | --- |
| `tonight-sky` | A viewing plan for a place and evening |
| `lesson-builder` | UK key-stage lessons and worksheets using live values |
| `space-fact-check` | Check astronomy claims and explain definition differences |
| `object-explainer` | Explain catalogue objects at a chosen reading level |
| `close-approach-watch` | Explain upcoming asteroid and comet flybys |
| `sky-this-week` | Draft a sourced sky roundup or social copy |
| `publicuniverse-data-audit` | Compare catalogue data with official sources |

Every skill carries its own reference files, so it can be installed independently. Workflows distinguish unavailable tools from verified results and never invent live values.

## Upgrading from `solar`

- Remove the old `solar` plugin before enabling `publicuniverse`.
- The MCP server name changed from `solar-system-db` to `publicuniverse` in 0.4.0. Tool names are unchanged, but client prefixes change (for example Claude's `mcp__…solar-system-db__get_object` becomes `mcp__…publicuniverse__get_object`); update any saved permission allowlists.
- `/solar:…` commands are now `/publicuniverse:…`; `solar-data-audit` is now `publicuniverse-data-audit`.

## Develop and package

Python 3.11+, no third-party dependencies:

```sh
python3 scripts/package.py generate   # regenerate client files from plugin.json + mcp.json
python3 scripts/package.py check
python3 -m unittest discover -s tests -v
python3 scripts/package.py build      # dist/publicuniverse-<version>.zip and .plugin
```

Edit only root `plugin.json` (metadata) and `mcp.json` (connection). `generate` writes the Claude manifest and marketplace, `.mcp.json`, `gemini-extension.json`, the MCP Registry `server.json` and the `clients/` profiles; `check` rejects drift. See [validation](docs/validation.md) and [listings](docs/listings.md).

## Data, safety and licence

This is astronomy, not astrology. Keep the source, retrieval date, units, method and limitations with derived answers. These workflows don't control telescopes or certify pointing accuracy. Never look at the Sun through binoculars or a telescope without proper solar filters and supervision.

The plugin is MIT licensed, © 2026 Wicked Sick Limited; please credit "Wicked Sick Ltd" ([NOTICE](NOTICE)). Catalogue datasets keep their own terms, including credit to NASA/JPL and the IAU Minor Planet Center where applicable.

Built by [Wicked Sick Ltd](https://wickedsick.com). Feedback: hello@wickedsick.com.
