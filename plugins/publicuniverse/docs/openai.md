# ChatGPT and Codex

These instructions follow official OpenAI documentation checked on 2026-10-02. Start with the [connection status](validation.md): a valid plugin package does not establish that the public server is reachable.

## Codex

### Tools and local skills

This route works without publishing a plugin. Register the public Streamable HTTP server:

```sh
codex mcp add publicuniverse --url https://api.sol.wickedsick.com/mcp
codex mcp list
```

Alternatively, merge [clients/codex.toml](../clients/codex.toml) into your existing `~/.codex/config.toml`. Keep existing settings and avoid adding the same server twice. Codex's IDE MCP settings offer a Streamable HTTP connection too. See [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

Copy each desired **whole directory** from `skills/` into your project's `.agents/skills/`, or `~/.agents/skills/` for personal use. For example, `.agents/skills/tonight-sky/` must contain both `SKILL.md` and `references/`. Compare any existing same-name skill before replacing it. Start a fresh session and invoke `$tonight-sky` with a town, date and timezone. These are the documented [local skill discovery locations](https://learn.chatgpt.com/docs/build-skills).

### Full portable plugin

Current Codex supports root `plugin.json`, `mcp.json` and `skills/`. The [OpenAI package guide](https://developers.openai.com/plugins/build/plugins) describes local and Git-backed marketplaces.

The public catalog is [Wicked-Sick-Ltd/ai-marketplace](https://github.com/Wicked-Sick-Ltd/ai-marketplace). Once its PublicUniverse entry is merged and the source repository is public:

```sh
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace --sparse .agents/plugins
codex plugin add publicuniverse@wickedsick
```

[clients/openai-marketplace.json](../clients/openai-marketplace.json) is a standalone development example, not a second public catalog. Its `main` reference works only after the plugin change is merged; for review, replace it with the tested revision. Production catalog entries must pin the full reviewed commit SHA. The repository is `https://github.com/Wicked-Sick-Ltd/publicuniverse-plugin` (renamed from `solar-plugin`; GitHub redirects the old URL). See [submission readiness](submission.md).

For a fully local test, replace the entry's source with `{"source":"local","path":"./plugins/publicuniverse"}` and place the whole plugin at `plugins/publicuniverse` inside the marketplace root. Paths start with `./` and must stay inside that root. Use either the full plugin or the manual MCP/skills route to avoid duplicates.

## ChatGPT

### Connect the tools

Where your account and workspace policy allow developer mode:

1. Open **Settings → Security and login → Developer mode**.
2. Open [ChatGPT Plugins](https://chatgpt.com/plugins), choose the plus button, and name the connection **Public Universe**.
3. Enter `https://api.sol.wickedsick.com/mcp` as the public MCP URL. The intended public service needs no authentication.
4. Review the discovered tools, then start a new conversation and enable the connection from the tools menu.
5. Ask it to retrieve Mars's catalogue record and cite its source. Verify that a tool actually ran.

The official [connection and testing guide](https://developers.openai.com/plugins/deploy/connect-chatgpt) documents this flow and policy-dependent availability. A 404 during initialization means the `/mcp` route is not deployed on the origin yet (checked 2026-10-08: Cloudflare passes the request and the API application answers 404). It is not an authentication problem; see the [validation record](validation.md).

### Add the workflows

An MCP connection supplies tools. It does not automatically import this repository's seven skill folders. The portable package supplies both components on surfaces supporting local/repository plugins. Use the marketplace route above on supported desktop surfaces; local-source availability varies by surface.

For a ChatGPT test using a registered MCP connection, follow the official [local plugin with MCP setup](https://developers.openai.com/plugins/build/plugins#create-and-test-a-plugin-locally-with-an-mcp-server): obtain the actual registered connection ID, then map that ID in a local `.app.json` and the manifest's `extensions.com.openai.apps` field. The repository deliberately contains no invented connection ID or account-specific mapping. Keep that local mapping out of a public commit.

Public directory distribution is a separate [submission and review process](https://developers.openai.com/plugins/deploy/submission). This development package has not been submitted or approved, and does not make local skill installation available on every ChatGPT surface.
