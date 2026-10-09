# Gemini CLI

Gemini CLI has no marketplace catalog file. Extensions must have `gemini-extension.json` at the **plugin repository** root, then:

```bash
gemini extensions install https://github.com/Wicked-Sick-Ltd/<plugin>
```

## Ponytail

[Ponytail](https://github.com/DietrichGebert/ponytail) ships a real Gemini
extension: `gemini-extension.json` loads its context, commands and skills.
Install the reviewed 4.10.0 revision:

```bash
gemini extensions install https://github.com/DietrichGebert/ponytail --ref e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156
gemini extensions list
```

Start a new session and use `/ponytail-help` or `/ponytail-review`. It does not
reuse Claude/Codex lifecycle hooks. The CLI supports a commit as `--ref`;
see the [extension reference](https://geminicli.com/docs/extensions/reference/).

## Token usage

The 0.8.0 candidate supplies `gemini-extension.json`, the report skill and a Gemini
JSON/JSONL session adapter. Install the pinned candidate after its release approval:

```bash
gemini extensions install https://github.com/Wicked-Sick-Ltd/token-usage --ref ae989e2cde864447f8c63c1423c0d4ba3b9839df
gemini extensions list
gemini mcp list
```

It reads local recordings and nested agents; unknown model prices stay unknown.
It does not add Claude-style budget nudges. See
[verification and limitations](../docs/token-usage.md) before rolling it out.

## Public Universe (rollout pending)

The astronomy plugin (`publicuniverse` 0.4.0) ships a generated `gemini-extension.json`, one public HTTP MCP server (`publicuniverse`) and seven shared skills. The source repository is being renamed from `solar-plugin` to `Wicked-Sick-Ltd/publicuniverse-plugin` and made public. Live MCP acceptance is blocked until the `/mcp` route is deployed on the API origin. See [rollout evidence](../docs/publicuniverse.md).

```bash
gemini extensions install https://github.com/Wicked-Sick-Ltd/publicuniverse-plugin --ref 6aecc7bdd721b88a5aa5e50bc170f0b11aa76e0e
gemini extensions list
gemini skills list
```

Re-pin `--ref` to the merged 0.4.0 commit before announcing. Windows local installation and discovery of 0.3.0 passed with Gemini CLI 0.62.0 on Node 24.21.0. There are no extension hooks or credentials.

Gallery (public, later): https://geminicli.com/extensions/

`wizzo-fleet-presence` is **not listed for Gemini**. Gemini CLI has no session
lifecycle hook equivalent to Claude Code's `SessionStart`/`Stop` or Codex's
`[[hooks.*]]`, so there is nothing for a presence pack to bind to. Deferred with
Copilot to a later tranche — the vendor enum (`claude-code · codex · cursor ·
copilot · gemini · custom`) and the pack layout already leave room.

The private [ai-gemini-repo](https://github.com/Wicked-Sick-Ltd/ai-gemini-repo)
owns the team setup and validation record. The extension runtime remains in
upstream Ponytail; this repository does not provide a Gemini JSON catalog.
