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

## PublicUniverse (rollout pending)

The astronomy plugin ships a generated `gemini-extension.json`, one public HTTP MCP server and seven shared skills. The reviewed source remains internal pending transfer to the `public-universe` organisation; update this URL after the destination is confirmed. Live MCP acceptance is blocked by HTTP 404. See [rollout evidence](../docs/publicuniverse.md).

For authorised reviewers with repository access:

```bash
gemini extensions install https://github.com/Wicked-Sick-Ltd/solar-plugin --ref d44a5765a1b37b3036fa13564d6820227343abea
gemini extensions list
gemini skills list
```

Windows local installation and discovery passed with Gemini CLI 0.62.0 on Node 24.21.0. All seven skills were discovered; the configured MCP server reported its existing 404. There are no extension hooks or credentials. Public installation must wait for the repository and service rollout.

`token-usage` reads Claude Code, Codex and Cursor sessions only. It is not a Gemini extension until that repo ships `gemini-extension.json` and a Gemini session adapter.

Gallery (public, later): https://geminicli.com/extensions/

`wizzo-fleet-presence` is **not listed for Gemini**. Gemini CLI has no session
lifecycle hook equivalent to Claude Code's `SessionStart`/`Stop` or Codex's
`[[hooks.*]]`, so there is nothing for a presence pack to bind to. Deferred with
Copilot to a later tranche — the vendor enum (`claude-code · codex · cursor ·
copilot · gemini · custom`) and the pack layout already leave room.

The private [ai-gemini-repo](https://github.com/Wicked-Sick-Ltd/ai-gemini-repo)
owns the team setup and validation record. The extension runtime remains in
upstream Ponytail; this repository does not provide a Gemini JSON catalog.
