# Public Universe

Package name `publicuniverse`. Website: https://publicuniverse.net. Upstream: https://github.com/Wicked-Sick-Ltd/public-universe.

The public MCP service answers on two hosts with no redirect:

| Host | Role |
| --- | --- |
| `https://api.publicuniverse.net/mcp` | Advertised URL. Cursor's vendored 0.4.2 copy and upstream `main` use this. |
| `https://api.sol.wickedsick.com/mcp` | Still in service. The 0.4.1 pin used by Claude, Codex, Copilot and the Gemini `--ref` still configures this URL. |

On 2026-11-11 both hosts answered `initialize` with HTTP 200 and no `Location` header. The service still reports MCP `serverInfo.name` `solar-system-db`. The client connection name in the package is `publicuniverse`. Interactive MCP use has no API key. Bulk REST calls send `X-PU-Api-Key`; see the plugin's [fair-use note](../plugins/publicuniverse/docs/fair-use.md).

## What each host installs

| Host | Version | Commit | MCP URL inside that package |
| --- | --- | --- | --- |
| Cursor | 0.4.2, vendored at `plugins/publicuniverse/` | `8b1e7b348067194d5a400f6bf16a0144a51d74aa` (head of [public-universe #9](https://github.com/Wicked-Sick-Ltd/public-universe/pull/9), before the squash) | `https://api.publicuniverse.net/mcp` |
| Claude, Codex, Copilot | 0.4.1 | `bb5919e47e8c8e1eb66c2fc5dcdba9bbc51b2f56` | `https://api.sol.wickedsick.com/mcp` |
| Gemini CLI command in [`gemini/README.md`](../gemini/README.md) | 0.4.1 | the same SHA as `--ref` | the alias URL above |

#9 merged to `main` on 2026-11-12 as `f660a494163def6b3d9e4427eebcf9cf1190f052`. `main` has since moved to `4d7fee039221247817b6ee7251a0a2970b6d66aa` (2026-11-13), which also includes the catalogue notes in #11 and the manifest cleanup in #10. This docs change does not re-pin or re-vendor. The Cursor directory is still the pre-merge #9 tree, not `4d7fee03`.

Seven skills ship with the package: `tonight-sky`, `lesson-builder`, `space-fact-check`, `object-explainer`, `close-approach-watch`, `sky-this-week`, `publicuniverse-data-audit`. Skill `metadata.version` fields in this tree still say `0.4.0`. Positions are approximate and are not for telescope pointing.

## Install

Register `Wicked-Sick-Ltd/ai-marketplace` first.

```sh
codex plugin add publicuniverse@wickedsick
claude plugin install publicuniverse@wickedsick
copilot plugin install publicuniverse@wickedsick
```

Those three commands install 0.4.1 at `bb5919e`. Cursor installs 0.4.2 from `plugins/publicuniverse/` after the team marketplace import in the [README](../README.md).

Remove an old `solar` plugin before enabling `publicuniverse`. From 0.4.0 the MCP server id is `publicuniverse`, not `solar-system-db`, and the audit skill is `publicuniverse-data-audit`. Tool names are unchanged; client prefixes and saved permission allowlists change.

## Earlier rollout notes

The 2026-10-05 checks (Codex 0.160.0, Claude 2.1.273, Copilot 1.0.91, Gemini 0.62.0) discovered the skills. Several of those notes still said the repository rename and the `/mcp` route were pending. Both have since landed: the repository is `Wicked-Sick-Ltd/public-universe`, and both MCP hosts answer. Those October checks are not a fresh acceptance pass of 0.4.2. Official vendor-directory submissions are still separate from this GitHub catalogue.
