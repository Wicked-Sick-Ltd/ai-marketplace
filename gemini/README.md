# Google Antigravity & Gemini CLI

Google Antigravity (`agy` CLI, Antigravity 2.0 desktop app, and Antigravity IDE) supersedes the deprecated standalone Gemini CLI workflow across our hosts.

- **Antigravity (`agy` CLI, Antigravity 2.0, IDE):** Global plugins live under `~/.gemini/config/plugins/<name>/` (with `plugin.json`, optional `mcp_config.json`, `hooks.json`, `rules/AGENTS.md`, and `skills/<skill>/SKILL.md`), or can be staged for the CLI via `agy plugin install <local-path>` and verified with `agy plugin list`. Workspace-level plugins can also be declared via `.agents/plugins.json`.
- **Legacy Gemini CLI fallback:** Standalone `gemini` CLI reads `gemini-extension.json` at the plugin repository root (`gemini extensions install https://github.com/Wicked-Sick-Ltd/<plugin> --ref <sha>`).

## Ponytail

[Ponytail](https://github.com/DietrichGebert/ponytail) reviewed baseline is **4.10.0** (`e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156`).

### Antigravity (`~/.gemini/config/plugins/ponytail`)

Install the reviewed 4.10.0 revision into `~/.gemini/config/plugins/ponytail/` (with `plugin.json`, `rules/AGENTS.md`, and `skills/ponytail*/SKILL.md`) or stage a local checkout via `agy plugin install <local-ponytail-path>`. Antigravity loads `rules/AGENTS.md` automatically whenever the `ponytail` plugin is enabled, and exposes `/ponytail`, `/ponytail-review`, `/ponytail-audit`, `/ponytail-debt`, `/ponytail-gain`, and `/ponytail-help`. See the full setup in [ai-gemini-repo/docs/ponytail.md](https://github.com/Wicked-Sick-Ltd/ai-gemini-repo/blob/main/docs/ponytail.md).

### Legacy Gemini CLI

```bash
gemini extensions install https://github.com/DietrichGebert/ponytail --ref e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156
gemini extensions list
```

Start a new session and use `/ponytail-help` or `/ponytail-review`. It does not reuse Claude/Codex lifecycle hooks on standalone Gemini CLI.

## Token usage

`token-usage` supplies an Antigravity plugin bundle (`plugin.json`, `mcp_config.json`, `skills/report/SKILL.md`), an Antigravity `transcript.jsonl` + legacy Gemini JSON/JSONL session adapter (`--runtime gemini`), and a legacy `gemini-extension.json`.

### Antigravity (`~/.gemini/config/plugins/token-usage` or `agy plugin install`)

From a pinned checkout of `Wicked-Sick-Ltd/token-usage`, copy or link the plugin into `~/.gemini/config/plugins/token-usage` (or run `agy plugin install <path-to-token-usage>` and `agy plugin list` when using the `agy` CLI). Antigravity discovers both the `report` skill and the `token-usage` stdio MCP server (`session_cost`, `history`, `insights`, `diff`, `top_consumers`), reading Antigravity transcripts under `~/.gemini/antigravity*/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` as well as legacy `~/.gemini/tmp/*/chats/` recordings.

### Legacy Gemini CLI

```bash
gemini extensions install https://github.com/Wicked-Sick-Ltd/token-usage --ref 39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c
gemini extensions list
gemini mcp list
```

It reads local recordings and nested agents; unknown model prices stay unknown. It does not add Claude-style budget nudges. See [verification and limitations](../docs/token-usage.md) before rolling it out.

## Public Universe (rollout pending)

The astronomy plugin (`publicuniverse` 0.4.1) ships `plugin.json`, `gemini-extension.json`, one public HTTP MCP server (`publicuniverse`) and seven shared skills. The source repository is being renamed from `solar-plugin` to `Wicked-Sick-Ltd/public-universe` and made public. Live MCP acceptance is blocked until the `/mcp` route is deployed on the API origin. See [rollout evidence](../docs/publicuniverse.md).

```bash
# Legacy Gemini CLI
gemini extensions install https://github.com/Wicked-Sick-Ltd/public-universe --ref bb5919e47e8c8e1eb66c2fc5dcdba9bbc51b2f56
gemini extensions list
gemini skills list
```

Re-pin `--ref` to the merged 0.4.1 commit before announcing. Windows local installation and discovery of 0.3.0 passed with Gemini CLI 0.62.0 on Node 24.21.0. There are no extension hooks or credentials.

## Fleet presence & workflow plugins (`ai-gemini-repo`)

Unlike standalone Gemini CLI (which had no session lifecycle hooks), **Google Antigravity natively supports `<plugin_dir>/hooks.json`** with `SessionStart`, `PreInvocation`, `PostInvocation`, `PreToolUse`, `PostToolUse`, and `Stop` events. Antigravity fleet-presence hooks bind `SessionStart`, `PreInvocation`, and `Stop` to `coordctl.py --vendor gemini`. Standalone Gemini CLI remains unsupported for `wizzo-fleet-presence`.

The private [ai-gemini-repo](https://github.com/Wicked-Sick-Ltd/ai-gemini-repo) (`ecae8ed7404c5b9029c8b97744fd18bb8f5ad455`) ships the compiled Antigravity workflow plugins (`session-lifecycle`, `pr-flow`, `product-lifecycle`, `estate-maintenance`, `onboarding`, `wizzo-fleet-presence`, `amiga-decoding`) under `plugins/<name>/`. The Ponytail runtime remains in upstream Ponytail; this repository does not provide a Gemini JSON catalog.
