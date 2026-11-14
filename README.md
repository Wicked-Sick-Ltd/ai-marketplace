# Wicked Sick AI marketplace

Cross-host catalogue for agent plugins published by [Wicked Sick Ltd](https://wickedsick.com). This repository is the **headline marketplace** for Cursor team marketplace review: import `Wicked-Sick-Ltd/ai-marketplace` and install the featured Cursor plugins from paths inside this repo.

Plugin behaviour lives in each plugin's own upstream repository. For Cursor, we **vendor** copies of the featured packages under `plugins/` so the Team Marketplace can resolve them as in-repo paths (Cursor does not SHA-pin remote Git sources in `.cursor-plugin/marketplace.json`). See each plugin's `VENDORED.md` for the upstream repo and commit. Those copies can lag upstream `main`; the `VENDORED.md` files say when they do.

Other hosts (Claude Code, Codex, Copilot, Gemini) use commit-pinned remote sources in their index files in this same repository. **amiga-decoding** is the exception: every host installs the vendored directory in this public repository, because the upstream checkouts are private. A host's version can differ from the Cursor copy when the pins do.

## Featured plugins (Cursor)

| Plugin | Version in this tree | What it does | Upstream |
| --- | --- | --- | --- |
| **token-usage** | 0.9.0 at `39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c` | Token profiler: attribute usage to activities, query history via MCP, optional hook-based attribution. Estimates API list prices; not a subscription bill. This copy reads an explicit Cursor Cloud Agent export `.json`. It does not include upstream's unreleased `cursor-cloud` Admin API runtime. | [token-usage](https://github.com/Wicked-Sick-Ltd/token-usage) |
| **publicuniverse** | 0.4.2 at `8b1e7b348067194d5a400f6bf16a0144a51d74aa` | Astronomy skills and a public MCP server: tonight's sky, lessons, fact-checking, and catalogue exploration. This copy calls `https://api.publicuniverse.net/mcp`. No API key for interactive MCP. | [public-universe](https://github.com/Wicked-Sick-Ltd/public-universe) |
| **pr-flow** | 1.1.0 (catalogue copy) | Pull-request lifecycle skills (`landing-prs`, `pr`) and `pr-wait.sh`. A finished PR is opened ready for review. Waits for CI and reviewer bots, then fixes or answers every finding. | [ai-grok-repo `plugins/pr-flow`](https://github.com/Wicked-Sick-Ltd/ai-grok-repo/tree/main/plugins/pr-flow) |
| **amiga-decoding** | 1.0.0 | Evidence-led Amiga ADF extraction and decompilation to exhaustion, with separate disk, content and semantic coverage. Instructions only. | This repository, `plugins/amiga-decoding/` |

Vendored paths: `plugins/token-usage/`, `plugins/publicuniverse/`, `plugins/pr-flow/`, `plugins/amiga-decoding/`.

Claude, Codex and Copilot do not install the token-usage, publicuniverse, or pr-flow directories. They install the SHAs in the inventory below. For `pr-flow` that pin is still 1.0.0 at `62272ec3ec8eba9059fd43ce9a9d1f913e317fbb`, which does not contain the ready-for-review rule. For `publicuniverse` that pin is 0.4.1, whose MCP URL is still `https://api.sol.wickedsick.com/mcp`. Both Public Universe hosts answer; there is no redirect. **amiga-decoding** is the other way around: every host installs `plugins/amiga-decoding/` from this public repository.

## Install in Cursor (team marketplace)

1. **Admin:** In the Cursor dashboard, open **Plugins → Team Marketplaces → Import from Repo** and import `https://github.com/Wicked-Sick-Ltd/ai-marketplace`.
2. Turn on **Auto Refresh** if you want the catalog to track new commits on this repo.
3. Grant your team access to the marketplace.
4. **Developers:** **Cursor Settings → Plugins**, open the Wicked Sick marketplace, and install **token-usage**, **publicuniverse**, **pr-flow**, and/or **amiga-decoding**. Enable the bundled MCP servers when prompted.

Detailed Cursor notes (formats, vendoring rationale, Cloud Agents, verification): [`docs/cursor-integration.md`](docs/cursor-integration.md).

**Requirements:** Python 3.9+ on the PATH for **token-usage** (stdio MCP and hooks). **publicuniverse** uses the remote HTTP MCP server in the plugin README. **pr-flow** needs authenticated `gh`, Bash and `jq`. **amiga-decoding** is instructions only.

Cloud Agents do not inherit a laptop's Cursor plugins. See [Token usage and Cloud Agents](docs/token-usage.md#cursor-cloud-agents).

## Other agents

```bash
# Claude Code (also used by Grok Build for this catalog)
claude plugin marketplace add Wicked-Sick-Ltd/ai-marketplace

# Codex CLI
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace --sparse .agents/plugins
```

Then install plugins by name from that marketplace (for example `claude plugin install token-usage@wickedsick`, or `/plugin install amiga-decoding@wickedsick`). Copilot CLI, Gemini, and Codex workflow details are in the host-specific index files listed below. **amiga-decoding** is a directory in this checkout. A Codex `--sparse .agents/plugins` add omits `plugins/amiga-decoding`; add the full marketplace before installing that plugin.

## Catalog indexes

| Client | File | Notes |
| --- | --- | --- |
| Cursor | `.cursor-plugin/marketplace.json` | Path-based; featured plugins vendored under `plugins/`. Marketplace `metadata.version` is `0.4.0`. |
| Claude Code / Grok | `.claude-plugin/marketplace.json` | GitHub SHA pins, except amiga-decoding at `./plugins/amiga-decoding`. Marketplace name `wickedsick`. |
| ChatGPT / Codex | `.agents/plugins/marketplace.json` | Native Codex packages, SHA pins, except amiga-decoding at `./plugins/amiga-decoding` |
| Copilot CLI | `.github/plugin/marketplace.json` | SHA pins, except amiga-decoding at `./plugins/amiga-decoding`. Marketplace `metadata.version` is `0.1.0`. |
| Antigravity / Gemini | [`gemini/README.md`](gemini/README.md) | Antigravity (`~/.gemini/config/plugins/`, `agy plugin`) and legacy Gemini CLI. No JSON catalog. |

## Catalog inventory

Versions and SHAs are the values in the index files and `VENDORED.md` files on this branch. They are not a claim that upstream `main` is the same commit.

| Plugin | Claude | Codex | Copilot | Cursor | Gemini |
| --- | --- | --- | --- | --- | --- |
| token-usage | 0.9.0 `39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c` | same SHA | 0.9.0, same SHA | 0.9.0 vendored at that SHA | `--ref` that SHA |
| publicuniverse | 0.4.1 `bb5919e47e8c8e1eb66c2fc5dcdba9bbc51b2f56` | same SHA | 0.4.1, same SHA | 0.4.2 vendored at `8b1e7b348067194d5a400f6bf16a0144a51d74aa` | `--ref` the 0.4.1 SHA |
| pr-flow | 1.0.0 `62272ec3ec8eba9059fd43ce9a9d1f913e317fbb` | same SHA, no version field | 1.0.0, same SHA | 1.1.0, this directory | not in this index; `ai-gemini-repo` ships its own copy |
| amiga-decoding | 1.0.0, `./plugins/amiga-decoding` | same directory, no version field | 1.0.0, same directory | 1.0.0, this directory | this directory (`gemini/README.md`) |
| ponytail | 4.10.0 `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156` | same SHA | 4.10.0, same SHA | not listed | install guide only |
| wizzo-fleet-presence | 0.1.0 `a41deeb46c1bb016676ec55821dc3fb985586b0f` (`ai-claude-repo` `plugins/wizzo-fleet-presence`) | `06f5c0a19808e91ccc53bba9111346fdbb86ee23` (`ai-codex-repo` `plugins/wizzo-fleet-presence`) | not listed | not listed | not in this index |
| estate-maintenance, onboarding, product-lifecycle, session-lifecycle | not listed | each `git-subdir` of `ai-codex-repo` at `06f5c0a19808e91ccc53bba9111346fdbb86ee23` | not listed | not listed | not in this index |

Codex descriptions, from `.agents/plugins/marketplace.json`:

- **estate-maintenance** — repository maintenance, findings triage and scanning setup. Dry-run by default.
- **onboarding** — check prerequisites, installed Codex plugins and portfolio setup.
- **product-lifecycle** — product scope, research, opportunity scoring, pricing, go-to-market and inventory updates.
- **session-lifecycle** — startup and shutdown skills, a portable handoff log, and native lifecycle hooks.
- **wizzo-fleet-presence** — optional fleet-presence hooks. Presence is self-reported; install and trust on each machine.
- **amiga-decoding** — evidence-led Amiga ADF extraction and decompilation to exhaustion, with separate disk, content and semantic coverage. Installed from `plugins/amiga-decoding/` in this repository.

`wizzo-fleet-presence` on Claude is the same idea for Claude Code hooks. It is fail-open. The hub credential stays in the operator's local config and is not in this repository.

Host write-ups: [`docs/token-usage.md`](docs/token-usage.md), [`docs/cursor-integration.md`](docs/cursor-integration.md), [`docs/codex-integration.md`](docs/codex-integration.md), [`docs/publicuniverse.md`](docs/publicuniverse.md), [`docs/ponytail.md`](docs/ponytail.md), [`plugins/pr-flow/README.md`](plugins/pr-flow/README.md).

## Validation

```bash
python3 scripts/validate.py
python3 scripts/test_validate.py
python3 scripts/test_dependabot_alerts.py
```

CI (`.github/workflows/validate.yml`) runs those three on every pull request. It does not lint or build the demo app.

`scripts/dependabot_alerts.py` lists Dependabot alerts. Cloud Agent app tokens cannot read that API; see [`docs/github-security-api-access.md`](docs/github-security-api-access.md).

## Demo app

A small Next.js 15.5.28 + Prisma app lives in this tree for Cursor Cloud Agent environments. It is not part of the plugin catalog. See [`docs/demo-app.md`](docs/demo-app.md).

## Contributing

- [Contributor guide](CONTRIBUTING.md)
- [Agent instructions](AGENTS.md)
- [Security policy](SECURITY.md)

MIT licensed; see [LICENSE](LICENSE). Preserve third-party notices in vendored plugin directories.

Contact: [hello@wickedsick.com](mailto:hello@wickedsick.com)
