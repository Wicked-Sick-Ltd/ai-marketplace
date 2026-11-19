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

`token-usage` **0.9.0** at `39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c` supplies an Antigravity plugin bundle (`plugin.json`, `mcp_config.json`, `skills/report/SKILL.md`), an Antigravity `transcript.jsonl` + legacy Gemini JSON/JSONL session adapter (`--runtime gemini`), and a legacy `gemini-extension.json`. That commit does not include the unreleased `cursor-cloud` runtime on upstream `main`. See [token-usage](../docs/token-usage.md).

### Antigravity (`~/.gemini/config/plugins/token-usage` or `agy plugin install`)

From a pinned checkout of `Wicked-Sick-Ltd/token-usage`, copy or link the plugin into `~/.gemini/config/plugins/token-usage` (or run `agy plugin install <path-to-token-usage>` and `agy plugin list` when using the `agy` CLI). Antigravity discovers both the `report` skill and the `token-usage` stdio MCP server (`session_cost`, `history`, `insights`, `diff`, `top_consumers`), reading Antigravity transcripts under `~/.gemini/antigravity*/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` as well as legacy `~/.gemini/tmp/*/chats/` recordings.

### Legacy Gemini CLI

```bash
gemini extensions install https://github.com/Wicked-Sick-Ltd/token-usage --ref 39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c
gemini extensions list
gemini mcp list
```

It reads local recordings and nested agents; unknown model prices stay unknown. It does not add Claude-style budget nudges. See [verification and limitations](../docs/token-usage.md) before rolling it out.

## Public Universe

The astronomy plugin ships `plugin.json`, `gemini-extension.json`, one public HTTP MCP server (`publicuniverse`) and seven shared skills. The source repository is `Wicked-Sick-Ltd/public-universe`. See [catalogue notes](../docs/publicuniverse.md).

The command below matches the Claude, Codex and Copilot pin: **0.4.1** at `bb5919e47e8c8e1eb66c2fc5dcdba9bbc51b2f56`. That tree's `mcp.json` still says `https://api.sol.wickedsick.com/mcp`. The alias answers. Cursor's vendored copy is 0.4.2 and advertises `https://api.publicuniverse.net/mcp`. Upstream `main` (`4d7fee039221247817b6ee7251a0a2970b6d66aa`) also advertises the new host. This command is not that commit.

```bash
# Legacy Gemini CLI — same SHA as the Claude/Codex/Copilot catalogs
gemini extensions install https://github.com/Wicked-Sick-Ltd/public-universe --ref bb5919e47e8c8e1eb66c2fc5dcdba9bbc51b2f56
gemini extensions list
gemini skills list
```

Windows local installation and discovery of 0.3.0 passed with Gemini CLI 0.62.0 on Node 24.21.0. That check is not a 0.4.2 acceptance pass. There are no extension hooks or credentials.

## PR Flow

Canonical package: [Wicked-Sick-Ltd/pr-flow](https://github.com/Wicked-Sick-Ltd/pr-flow) **1.1.0** at `54de23f8d48f1c5c706046b068db139867eea474`, the same commit Claude, Codex, Copilot and Cursor pin. This repository does not vendor that tree and does not add a Gemini JSON catalog. GitHub access to the private repository is required until it is published.

### Legacy Gemini CLI

```bash
gemini extensions install https://github.com/Wicked-Sick-Ltd/pr-flow --ref 54de23f8d48f1c5c706046b068db139867eea474
gemini extensions list
```

### Antigravity

From a checkout of that commit, copy or link the repository into `~/.gemini/config/plugins/pr-flow`, or run `agy plugin install <path-to-pr-flow>` and `agy plugin list`. The tree ships `plugin.json` and `skills/`.

## Fleet presence & workflow plugins (`ai-gemini-repo`)

Unlike standalone Gemini CLI (which had no session lifecycle hooks), **Google Antigravity natively supports `<plugin_dir>/hooks.json`** with `SessionStart`, `PreInvocation`, `PostInvocation`, `PreToolUse`, `PostToolUse`, and `Stop` events. Antigravity fleet-presence hooks bind `SessionStart`, `PreInvocation`, and `Stop` to `coordctl.py --vendor gemini`. Standalone Gemini CLI remains unsupported for `wizzo-fleet-presence`.

## Obsidian

`obsidian` **1.2.0** at `cd51b7076a1207c805cf1d95da4c56cb96bbe859` is the Wicked Sick review of [obsidianmd/obsidian-skills](https://github.com/obsidianmd/obsidian-skills) (MIT, Copyright (c) 2026 Steph Ango). The pin is `Wicked-Sick-Ltd/obsidian-skills` on `wicked-main`, path `plugins/obsidian`. That commit is the merge of pull request #1. It installs three instruction-only skills: `obsidian-markdown`, `obsidian-bases`, and `json-canvas`. No shell, network, or credentials.

`gemini-extension.json` is at the repository root. The `skills` symlink there points at `plugins/obsidian/skills/`. Use this commit. The repository default branch is not this review.

### Antigravity (`~/.gemini/config/plugins/obsidian` or `agy plugin install`)

From a checkout of that commit, install `plugins/obsidian` (it has `plugin.json` and `skills/`). Copy or link it to `~/.gemini/config/plugins/obsidian`, or run `agy plugin install <path-to-plugins/obsidian>` and `agy plugin list`.

### Legacy Gemini CLI

```bash
gemini extensions install https://github.com/Wicked-Sick-Ltd/obsidian-skills --ref cd51b7076a1207c805cf1d95da4c56cb96bbe859
gemini extensions list
gemini skills list
```

## Amiga decoding

`amiga-decoding` 1.0.0 is the vendored directory `plugins/amiga-decoding/` in this repository (skill `amiga-adf-decompile`). `gemini-extension.json` is at the root of that directory. It is instructions only. Python disk utilities are not part of the plugin.

Clone this repository, then install that directory:

```bash
gemini extensions install /path/to/ai-marketplace/plugins/amiga-decoding
gemini extensions list
```

The private [ai-gemini-repo](https://github.com/Wicked-Sick-Ltd/ai-gemini-repo) ships the compiled Antigravity workflow plugins (`session-lifecycle`, `product-lifecycle`, `estate-maintenance`, `onboarding`, `wizzo-fleet-presence`) under `plugins/<name>/`. An earlier note in this file cited checkout `ecae8ed7404c5b9029c8b97744fd18bb8f5ad455`. On 2026-11-14 `main` was `58a0ff0f20caead17107d8a0ecd0c1413c7b1c7e` (ready-for-review rule, #8). This repository does not pin that repo in a JSON catalog. `pr-flow` installs from `Wicked-Sick-Ltd/pr-flow` at the commit in the section above. The Ponytail runtime remains in upstream Ponytail.

## Agent workflows

`agent-workflows` 1.0.0 is skills only. `ultracode` is a planned parallel-agent fan-out with scope, understand, change and verify stages. `ultrareview` is an adversarial review council with a rebuttal round and a judge, read-only by default.

The Gemini package path is `plugins/agent-workflows` in [ai-gemini-repo](https://github.com/Wicked-Sick-Ltd/ai-gemini-repo). On 2026-11-19 `main` was `81834fe79dbc8194696d32e712d1ec7e7ef374ad` and that path was absent, so this page does not give a `--ref`. This repository does not copy the skills and does not add a JSON catalog entry. `ai-claude-repo` is excluded because Claude Code has ultracode built in.

The skill text that exists today is the Cursor package in [ai-cursor-repo](https://github.com/Wicked-Sick-Ltd/ai-cursor-repo) `plugins/agent-workflows` at `9e38413cdd81bd5491dedebc99991910447d66ad` (pull request [#10](https://github.com/Wicked-Sick-Ltd/ai-cursor-repo/pull/10)). That tree is a Cursor plugin (`.cursor-plugin/plugin.json` 1.0.0). It is a pointer for readers, and it is not a Gemini install.
