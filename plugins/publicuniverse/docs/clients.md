# Install in Claude Code, Cursor, Copilot, Gemini CLI or Grok

Use a checkout containing this version's root `plugin.json`, `mcp.json` and `skills/` directory. See the [README](../README.md) for obtaining the correct version, and [OpenAI setup](openai.md) for ChatGPT and Codex. Instructions below were checked against vendor documentation on 2026-10-02; installed client versions and organization settings may differ.

The full plugin supplies the astronomy tools and all seven workflows. An MCP-only connection supplies tools; it does not install the skill instructions or their references. Choose one installation route per client to avoid duplicate tools and skills. The public service needs no API key.

## Cursor: full plugin

Cursor supports the portable Agent Plugins format directly. No separate `.cursor-plugin` manifest is needed for this package.

1. Create a **new** directory `~/.cursor/plugins/local/publicuniverse`.
2. Copy the plugin contents into it, including hidden compatibility files. The result must include `~/.cursor/plugins/local/publicuniverse/plugin.json`, `mcp.json` and `skills/tonight-sky/SKILL.md`; avoid adding an extra `publicuniverse-plugin/` nesting level.
3. Restart Cursor or run **Developer: Reload Window**.
4. Open **Customize** and check for the Public Universe skills and `publicuniverse` MCP server.

Use a real directory: Cursor skips symlinks whose target is outside its local plugins directory. If `publicuniverse` is already present, compare versions before replacing it. An installed marketplace plugin with the same name takes precedence. Organization policy may disable local plugin imports. These are documented [Cursor installation rules](https://prod.cursor.com/docs/plugins#test-plugins-locally).

For tools only, merge the server entry from [clients/cursor.json](../clients/cursor.json) into project `.cursor/mcp.json` or user `~/.cursor/mcp.json`. Preserve other entries. Cursor's standalone configuration uses `mcpServers` and a remote `url`; see its [MCP configuration documentation](https://prod.cursor.com/docs/mcp#configuration-locations).

## GitHub Copilot CLI: full plugin

Install the reviewed local checkout, replacing the example path:

```sh
copilot plugin install /absolute/path/to/publicuniverse-plugin
copilot plugin list
```

Copilot CLI 1.0.91 warns that direct installs will be removed in a future release. For public distribution, after the catalog entry is merged and the source is public:

```sh
copilot plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
copilot plugin install publicuniverse@wickedsick
```

Start a new Copilot session and inspect its plugin/skills and MCP views. The CLI accepts local plugin directories and discovers portable skills from `skills/` and tools from `mcp.json`. Both portable JSON files must declare the matching Agent Plugins schema version; this repository supplies them. See the [Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference).

For tools only, merge [clients/copilot-cli.json](../clients/copilot-cli.json) into `~/.copilot/mcp-config.json`, or project `.github/mcp.json`. Keep the `mcpServers` envelope. The `tools` list selects exposed tools; it is not permission to bypass tool approvals. Copilot CLI does **not** read `.vscode/mcp.json`. Project MCP configurations require a trusted workspace. See [adding MCP servers for Copilot CLI](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers).

## GitHub Copilot in VS Code: full plugin

Add these entries to your existing VS Code user `settings.json`, using your checkout's absolute path:

```json
{
  "chat.plugins.enabled": true,
  "chat.pluginLocations": {
    "/absolute/path/to/publicuniverse-plugin": true
  }
}
```

Merge settings instead of replacing the file. On Windows, use a valid JSON path such as `C:/Users/you/publicuniverse-plugin`. Reload VS Code, open the agent customizations/skills view and MCP server list, and confirm the plugin's components appear. VS Code recognizes the root Agent Plugins manifest and registers the local directory through `chat.pluginLocations`. See [VS Code local plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins#use-local-plugins).

For tools only, merge [clients/vscode.json](../clients/vscode.json) into the workspace's `.vscode/mcp.json`. This format uses **`servers`**, not `mcpServers`, with `type: "http"`. Start the server from its editor controls and review the trust prompt. See [VS Code MCP configuration](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

These instructions target Copilot CLI and VS Code. Installing locally does not configure GitHub-hosted cloud agents or other IDEs.

## Claude Code

The repository is its own Claude marketplace (`.claude-plugin/marketplace.json`, generated from the portable manifests alongside `.claude-plugin/plugin.json` and `.mcp.json`). Install it permanently:

```sh
/plugin marketplace add https://github.com/Wicked-Sick-Ltd/publicuniverse-plugin.git
/plugin install publicuniverse@publicuniverse
```

The explicit HTTPS URL avoids an SSH host-key prompt that the `owner/repo` shorthand can trigger. Version 0.3.0 renamed the plugin from `solar` to `publicuniverse`; 0.4.0 renamed the MCP server from `solar-system-db` to `publicuniverse`. Or load a reviewed checkout for one session:

```sh
claude --plugin-dir /absolute/path/to/publicuniverse-plugin
```

This [local plugin route](https://code.claude.com/docs/en/plugins) does not require a marketplace. Try `/publicuniverse:tonight-sky` and inspect `/mcp`. For a manifest check, run:

```sh
claude plugin validate /absolute/path/to/publicuniverse-plugin
```

MCP-entry validation requires Claude Code 2.1.281 or newer; see the [manifest validation reference](https://code.claude.com/docs/en/plugins-reference#validate-the-manifest). Marketplace availability and versions are separate from this local installation.

For tools only, merge [clients/claude.json](../clients/claude.json) into your project's `.mcp.json`. Keep any existing servers and review Claude's project-server approval prompt. Claude requires an explicit remote transport type; the supplied profile uses `http`. See [Claude MCP configuration](https://code.claude.com/docs/en/mcp#option-1-add-a-remote-http-server).

## Gemini CLI

The generated root `gemini-extension.json` registers the same public MCP endpoint using Gemini's `httpUrl` transport. Gemini discovers the shared `skills/` directory without copies or a context-file shim.

Install the reviewed local checkout:

```sh
gemini extensions install /absolute/path/to/publicuniverse-plugin
gemini extensions list
gemini skills list
```

Review the installation prompt, restart Gemini and check that PublicUniverse and all seven skills appear. Repository installs use `gemini extensions install https://github.com/Wicked-Sick-Ltd/publicuniverse-plugin --ref <reviewed-tag-or-sha>` once the repository is public. The pinned command belongs in the existing `ai-marketplace/gemini/README.md`; Gemini does not use a marketplace JSON catalog.

The tested Windows runtime is Gemini CLI 0.62.0 with Node 24.21.0. Node 25.6.1 produced a shutdown assertion after installation; repeat with Node 24 if you encounter that client error.

See the official [extension format and installation reference](https://geminicli.com/docs/extensions/reference/). A listed extension verifies local discovery; a successful live tool call is still required for service acceptance.

## Grok

Grok CLI reads Claude Code marketplaces, plugins, skills and `.mcp.json` files with no extra setup, so the Claude Code route above also installs Public Universe for Grok. Other routes:

```sh
grok plugin install Wicked-Sick-Ltd/publicuniverse-plugin   # or a local checkout path; add @<tag> to pin
grok plugin validate /absolute/path/to/publicuniverse-plugin
grok mcp add --transport http publicuniverse https://api.sol.wickedsick.com/mcp
grok mcp doctor publicuniverse
```

For tools only you can also merge [clients/grok.toml](../clients/grok.toml) into `~/.grok/config.toml`. Skills alone can be copied into `~/.grok/skills/` or `.grok/skills/`. Grok CLI 1.0.46 validated this package (`grok plugin validate`: manifest valid, skills and MCP server found) and discovered the `publicuniverse` HTTP server from the project `.mcp.json` on 2026-10-08. See [Grok MCP servers](https://docs.x.ai/build/features/mcp-servers) and [skills, plugins and marketplaces](https://docs.x.ai/build/features/skills-plugins-marketplaces).

**grok.com:** add a custom MCP connector with the server URL; no authentication is needed. **xAI API:** add a remote MCP tool to a Responses API request:

```json
{"type": "mcp", "server_url": "https://api.sol.wickedsick.com/mcp", "server_label": "publicuniverse", "server_description": "Public Universe astronomy catalogue (read-only)"}
```

See [xAI remote MCP tools](https://docs.x.ai/developers/tools/remote-mcp). xAI connects from its own servers, so the endpoint must be publicly reachable.

## Generic MCP clients

Add a remote Streamable HTTP server named `publicuniverse` at `https://api.sol.wickedsick.com/mcp` with no authentication. The MCP Registry entry is generated in [server.json](../server.json).

## Skills without a full plugin

If using an MCP-only connection, copy each desired **whole skill directory** from this repository's `skills/` into one supported location:

| Client | Project location | Personal location |
| --- | --- | --- |
| [Cursor](https://prod.cursor.com/docs/skills#skill-directories) | `.cursor/skills/` | `~/.cursor/skills/` |
| [Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) | `.github/skills/` | `~/.copilot/skills/` |
| [Copilot in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills#create-a-skill) | `.github/skills/` | `~/.copilot/skills/` |
| [Claude Code](https://code.claude.com/docs/en/skills#where-skills-live) | `.claude/skills/` | `~/.claude/skills/` |
| [Grok CLI](https://docs.x.ai/build/features/skills-plugins-marketplaces) | `.grok/skills/` | `~/.grok/skills/` |
| Codex / generic Agent Skills | `.agents/skills/` | `~/.agents/skills/` |

For example, copy `skills/tonight-sky/` to `.github/skills/tonight-sky/`, keeping both `SKILL.md` and `references/`. Keep directory names unchanged, do not flatten references, and do not overwrite a same-name local skill without comparing it first. Restart the client or start a new session after copying. Personal directories on your computer do not automatically configure hosted sessions.

## Check the connection

Ask: **“Use Public Universe to retrieve Mars's catalogue record, cite the source, and distinguish a catalogue value from a computed estimate.”** Confirm an actual MCP tool call appears. Then invoke `tonight-sky` through the client's skills menu with a location, date and timezone. Skill names may be namespaced differently across clients.

If tools appear but skills do not, check the installation layout and skill view. If neither appears, check the client version, enabled plugin setting and organization policy. A successful manifest check establishes package validity; it does not establish that your client has connected to the public endpoint.
