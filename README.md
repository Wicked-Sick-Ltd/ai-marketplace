# Wicked Sick AI marketplace

Cross-host catalogue for agent plugins published by [Wicked Sick Ltd](https://wickedsick.com). This repository is the **headline marketplace** for Cursor team marketplace review: import `Wicked-Sick-Ltd/ai-marketplace` and install the featured Cursor plugins from paths inside this repo.

Plugin behaviour lives in each plugin's own upstream repository. For Cursor, we **vendor** `token-usage`, `publicuniverse`, and `amiga-decoding` under `plugins/` so the Team Marketplace can resolve them as in-repo paths (Cursor's published importer resolves `source` as a directory in this repository). See each plugin's `VENDORED.md` for the upstream repo and commit. Those copies can lag upstream `main`; the `VENDORED.md` files say when they do. **pr-flow** is not vendored: every host pins [Wicked-Sick-Ltd/pr-flow](https://github.com/Wicked-Sick-Ltd/pr-flow) at `c73608143e9fcf1dd5a916d02957dc91ffe9c1e4`.

Other hosts (Claude Code, Codex, Copilot, Gemini) use commit-pinned remote sources in their index files in this same repository. **amiga-decoding** is the exception: every host installs the vendored directory in this public repository, because the upstream checkouts are private. **red-team-review** is first-party and published in this repository; every host installs `plugins/red-team-review/`. Its `VENDORED.md` records that there is no separate upstream pin. A host's version can differ from the Cursor copy when the pins do.

## Featured plugins (Cursor)

| Plugin | Version in this tree | What it does | Upstream |
| --- | --- | --- | --- |
| **token-usage** | 0.9.0 at `39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c` | Token profiler: attribute usage to activities, query history via MCP, optional hook-based attribution. Estimates API list prices; not a subscription bill. This copy reads an explicit Cursor Cloud Agent export `.json`. It does not include upstream's unreleased `cursor-cloud` Admin API runtime. | [token-usage](https://github.com/Wicked-Sick-Ltd/token-usage) |
| **publicuniverse** | 0.4.2 at `8b1e7b348067194d5a400f6bf16a0144a51d74aa` | Astronomy skills and a public MCP server: tonight's sky, lessons, fact-checking, and catalogue exploration. This copy calls `https://api.publicuniverse.net/mcp`. No API key for interactive MCP. | [public-universe](https://github.com/Wicked-Sick-Ltd/public-universe) |
| **pr-flow** | 1.1.3 at `c73608143e9fcf1dd5a916d02957dc91ffe9c1e4` (not vendored) | Pull-request lifecycle skills (`landing-prs`, `pr`) and `pr-wait.sh`. A finished PR is opened ready for review. Waits for CI and reviewer bots, then fixes or answers every finding. | [pr-flow](https://github.com/Wicked-Sick-Ltd/pr-flow) |
| **amiga-decoding** | 1.0.0 | Works with any AI agent. Evidence-led Amiga ADF extraction and decompilation to exhaustion, with separate disk, content and semantic coverage. Instructions only. | This repository, `plugins/amiga-decoding/` |
| **obsidian** | 1.2.0 at `cd51b7076a1207c805cf1d95da4c56cb96bbe859` | Vetted Obsidian format skills: Obsidian Flavored Markdown, Bases (`.base`) and JSON Canvas. Instruction-only; no shell, network or credentials. | [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills) (MIT, Copyright (c) 2026 Steph Ango). This catalog pins the reviewed fork [Wicked-Sick-Ltd/obsidian-skills](https://github.com/Wicked-Sick-Ltd/obsidian-skills) `plugins/obsidian` on `wicked-main`. |
| **red-team-review** | 1.0.0 | Adversarial fact-check and pre-mortem for a claim, plan, launch or merge. The reviewer did not author the work and does not fix it. Instructions only. | This repository, `plugins/red-team-review/` |

Vendored paths: `plugins/token-usage/`, `plugins/publicuniverse/`, `plugins/amiga-decoding/`, `plugins/obsidian/`, `plugins/red-team-review/`.

Claude, Codex and Copilot do not install the token-usage or publicuniverse directories. They install the SHAs in the inventory below. `pr-flow` is the same SHA on every host, `c73608143e9fcf1dd5a916d02957dc91ffe9c1e4` (manifests 1.1.3). For `publicuniverse` that pin is 0.4.1, whose MCP URL is still `https://api.sol.wickedsick.com/mcp`. Both Public Universe hosts answer; there is no redirect. **amiga-decoding** is the other way around: every host installs `plugins/amiga-decoding/` from this public repository. **red-team-review** is the same shape: every host installs `plugins/red-team-review/` from this public repository. **obsidian** is pinned at `cd51b7076a1207c805cf1d95da4c56cb96bbe859` on `wicked-main`, path `plugins/obsidian`. Claude, Codex and Copilot install that remote subdirectory. Cursor installs the vendored copy of the same commit. Upstream is [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills) (MIT, Copyright (c) 2026 Steph Ango).

## Install in Cursor (team marketplace)

1. **Admin:** In the Cursor dashboard, open **Plugins → Team Marketplaces → Import from Repo** and import `https://github.com/Wicked-Sick-Ltd/ai-marketplace`.
2. Turn on **Auto Refresh** if you want the catalog to track new commits on this repo.
3. Grant your team access to the marketplace.
4. **Developers:** **Cursor Settings → Plugins**, open the Wicked Sick marketplace, and install **token-usage**, **publicuniverse**, **amiga-decoding**, **obsidian**, and/or **red-team-review**. Enable the bundled MCP servers when prompted.
5. **pr-flow:** import `https://github.com/Wicked-Sick-Ltd/pr-flow` as well. The catalog entry records that commit, and Cursor's importer still loads plugin files from the imported repository. GitHub access to that private repository is required until it is published.

Detailed Cursor notes (formats, vendoring rationale, Cloud Agents, verification): [`docs/cursor-integration.md`](docs/cursor-integration.md).

**Requirements:** Python 3.9+ on the PATH for **token-usage** (stdio MCP and hooks). **publicuniverse** uses the remote HTTP MCP server in the plugin README. **pr-flow** needs authenticated `gh`, Bash, `jq`, and GitHub access to `Wicked-Sick-Ltd/pr-flow`. **amiga-decoding**, **obsidian**, and **red-team-review** are instructions only.

Cloud Agents do not inherit a laptop's Cursor plugins. See [Token usage and Cloud Agents](docs/token-usage.md#cursor-cloud-agents).

## Other agents

```bash
# Claude Code (also used by Grok Build for this catalog)
claude plugin marketplace add Wicked-Sick-Ltd/ai-marketplace

# Codex CLI
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace --sparse .agents/plugins
```

Then install plugins by name from that marketplace (for example `claude plugin install token-usage@wickedsick`, or `/plugin install amiga-decoding@wickedsick`). Copilot CLI, Gemini, and Codex workflow details are in the host-specific index files listed below. **amiga-decoding** and **red-team-review** are directories in this checkout. A Codex `--sparse .agents/plugins` add omits `plugins/amiga-decoding` and `plugins/red-team-review`; add the full marketplace before installing those plugins.

### Upgrade everything on a machine

`scripts/upgrade-agents.sh` upgrades each agent CLI that is installed (Claude Code, Codex, Antigravity `agy`, Copilot CLI, `cursor-agent`), then adds these marketplaces where missing, installs the essential plugins and updates the installed ones. Antigravity has no marketplace command, so its plugins are installed from the `ai-gemini-repo` `plugins.json` catalog at the pinned commits. It runs on macOS, Linux and Windows under Git Bash. `--dry-run` prints the commands without running them; `--help` lists the options and the plugin sets. A copy installed with Homebrew or Chocolatey is also upgraded through that package manager. `--install-missing` also installs any of those CLIs that is absent, with the vendor's own installer (PowerShell or WinGet on Windows). Verified on macOS with Claude Code, Codex, `agy` and `cursor-agent`; the Copilot steps, the Windows path, and `--install-missing` for anything but the Cursor CLI are untested.

## Catalog indexes

| Client | File | Notes |
| --- | --- | --- |
| Cursor | `.cursor-plugin/marketplace.json` | In-repo paths for vendored plugins. `pr-flow` is a `github` pin of `Wicked-Sick-Ltd/pr-flow`. Marketplace `metadata.version` is `0.4.0`. |
| Claude Code / Grok | `.claude-plugin/marketplace.json` | GitHub SHA pins, except amiga-decoding at `./plugins/amiga-decoding` and red-team-review at `./plugins/red-team-review`. Marketplace name `wickedsick`. |
| ChatGPT / Codex | `.agents/plugins/marketplace.json` | Native Codex packages, SHA pins, except amiga-decoding at `./plugins/amiga-decoding` and red-team-review at `./plugins/red-team-review` |
| Copilot CLI | `.github/plugin/marketplace.json` | SHA pins, except amiga-decoding at `./plugins/amiga-decoding` and red-team-review at `./plugins/red-team-review`. Marketplace `metadata.version` is `0.1.0`. |
| Antigravity / Gemini | [`gemini/README.md`](gemini/README.md) | Antigravity (`~/.gemini/config/plugins/`, `agy plugin`) and legacy Gemini CLI. No JSON catalog. |

## Catalog inventory

Versions and SHAs are the values in the index files and `VENDORED.md` files on this branch. They are not a claim that upstream `main` is the same commit.

| Plugin | Claude | Codex | Copilot | Cursor | Gemini |
| --- | --- | --- | --- | --- | --- |
| token-usage | 0.9.0 `39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c` | same SHA | 0.9.0, same SHA | 0.9.0 vendored at that SHA | `--ref` that SHA |
| publicuniverse | 0.4.1 `bb5919e47e8c8e1eb66c2fc5dcdba9bbc51b2f56` | same SHA | 0.4.1, same SHA | 0.4.2 vendored at `8b1e7b348067194d5a400f6bf16a0144a51d74aa` | `--ref` the 0.4.1 SHA |
| pr-flow | 1.1.3 `c73608143e9fcf1dd5a916d02957dc91ffe9c1e4` | same SHA, no version field | 1.1.3, same SHA | 1.1.3, same SHA | `--ref` that SHA |
| amiga-decoding | 1.0.0, `./plugins/amiga-decoding` | same directory, no version field | 1.0.0, same directory | 1.0.0, this directory | this directory (`gemini/README.md`) |
| obsidian | 1.2.0 `cd51b7076a1207c805cf1d95da4c56cb96bbe859` (`wicked-main` `plugins/obsidian`) | same SHA, no version field | 1.2.0, same SHA | 1.2.0 vendored at that SHA | `--ref` that SHA (`gemini/README.md`) |
| red-team-review | 1.0.0, `./plugins/red-team-review` | same directory, no version field | 1.0.0, same directory | 1.0.0, this directory | this directory (`gemini/README.md`) |
| ponytail | 4.10.0 `e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156` | same SHA | 4.10.0, same SHA | not listed | install guide only |
| wizzo-fleet-presence | 0.1.0 `a41deeb46c1bb016676ec55821dc3fb985586b0f` (`ai-claude-repo` `plugins/wizzo-fleet-presence`) | `06f5c0a19808e91ccc53bba9111346fdbb86ee23` (`ai-codex-repo` `plugins/wizzo-fleet-presence`) | not listed | not listed | not in this index |
| estate-maintenance, onboarding, product-lifecycle, session-lifecycle | not listed | each `git-subdir` of `ai-codex-repo` at `06f5c0a19808e91ccc53bba9111346fdbb86ee23` | not listed | not listed | not in this index |
| agent-workflows (`ultracode`, `ultrareview`) | not listed (`ai-claude-repo` excluded: Claude Code has ultracode built in) | not listed (`plugins/agent-workflows` is absent from `ai-codex-repo` `main` `08aed9053b480bc7d9c54be5d9c0195874d04114`) | not listed | `ai-cursor-repo` `plugins/agent-workflows` at `9e38413cdd81bd5491dedebc99991910447d66ad` ([#10](https://github.com/Wicked-Sick-Ltd/ai-cursor-repo/pull/10)); omitted from this Cursor JSON | no SHA; see [`gemini/README.md`](gemini/README.md) |

Codex descriptions, from `.agents/plugins/marketplace.json`:

- **estate-maintenance** — repository maintenance, findings triage and scanning setup. Dry-run by default.
- **onboarding** — check prerequisites, installed Codex plugins and portfolio setup.
- **product-lifecycle** — product scope, research, opportunity scoring, pricing, go-to-market and inventory updates.
- **session-lifecycle** — startup and shutdown skills, a portable handoff log, and native lifecycle hooks.
- **wizzo-fleet-presence** — optional fleet-presence hooks. Presence is self-reported; install and trust on each machine.
- **amiga-decoding** — evidence-led Amiga ADF extraction and decompilation to exhaustion, with separate disk, content and semantic coverage. Installed from `plugins/amiga-decoding/` in this repository.
- **red-team-review** — adversarial fact-check and pre-mortem for a claim, plan, launch or merge. The reviewer did not author the work and does not fix it. Installed from `plugins/red-team-review/` in this repository. Instructions only.
- **obsidian** — vetted Obsidian format skills: Obsidian Flavored Markdown, Bases (`.base`) and JSON Canvas. Instruction-only. Upstream [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills) (MIT, Copyright (c) 2026 Steph Ango). Codex installs `plugins/obsidian` from [Wicked-Sick-Ltd/obsidian-skills](https://github.com/Wicked-Sick-Ltd/obsidian-skills) at `cd51b7076a1207c805cf1d95da4c56cb96bbe859` (`wicked-main`).

`wizzo-fleet-presence` on Claude is the same idea for Claude Code hooks. It is fail-open. The hub credential stays in the operator's local config and is not in this repository.

`agent-workflows` 1.0.0 is skills only. `ultracode` is a planned parallel-agent fan-out with scope, understand, change and verify stages. `ultrareview` is an adversarial review council with a rebuttal round and a judge, read-only by default. This index points at `plugins/agent-workflows` in the host repositories and does not copy the skill files. `ai-claude-repo` is excluded because Claude Code has ultracode built in, so `.claude-plugin/marketplace.json` has no entry. Cursor's published importer loads an in-repo directory, and `pr-flow` is the only whole-repo GitHub pin, so `.cursor-plugin/marketplace.json` omits it. Install the Cursor package from [ai-cursor-repo](https://github.com/Wicked-Sick-Ltd/ai-cursor-repo) `plugins/agent-workflows` at `9e38413cdd81bd5491dedebc99991910447d66ad` (pull request [#10](https://github.com/Wicked-Sick-Ltd/ai-cursor-repo/pull/10), branch `feat/agent-workflows-ultracode-ultrareview`). That commit is manifest 1.0.0 and is not `main`. Codex, Copilot and Gemini have no SHA in this index. On 2026-11-19 `plugins/agent-workflows` was absent from `ai-codex-repo` `main` `08aed9053b480bc7d9c54be5d9c0195874d04114`, `ai-copilot-repo` `main` `84183a63f994003414ccb8df47c8e092662bfe27`, `ai-gemini-repo` `main` `81834fe79dbc8194696d32e712d1ec7e7ef374ad`, `ai-grok-repo` `main` `1fdca99bc808ad79587445bfa801107395aa46d7` and `ai-repo` `main` `5d67becf095bb362b8b4f3bc643323cb23e567ae`. A pin on those commits would resolve to a missing directory.

Host write-ups: [`docs/token-usage.md`](docs/token-usage.md), [`docs/cursor-integration.md`](docs/cursor-integration.md), [`docs/codex-integration.md`](docs/codex-integration.md), [`docs/publicuniverse.md`](docs/publicuniverse.md), [`docs/ponytail.md`](docs/ponytail.md), [pr-flow](https://github.com/Wicked-Sick-Ltd/pr-flow#readme).

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
