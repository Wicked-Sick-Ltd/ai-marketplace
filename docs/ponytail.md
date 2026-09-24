# Ponytail across our AI workflows

[Ponytail](https://github.com/DietrichGebert/ponytail) supplies minimal-code
guidance, review skills and host-specific activation. We reuse its upstream
runtimes. No plugin source lives in this index.

Reviewed version: **4.10.0**, commit
`e3ba2aa6f1e6f0bc4d69eb09c9f0d0a93af56156`.
Claude and Copilot entries pin that commit. Codex resolves upstream's default
branch; this review records a revision, but does not pin Codex installs.

| Host | Configuration home | Runtime |
| --- | --- | --- |
| Claude Code | `ai-claude-repo` marketplace, bootstrap and fleet policy; also this index | Upstream `.claude-plugin/plugin.json`, skills and Node lifecycle hooks |
| Codex | `ai-codex-repo/.agents/plugins/marketplace.json`; also this index | Upstream `.codex-plugin/plugin.json`, skills and Node lifecycle hooks |
| Copilot CLI | This index's `.github/plugin/marketplace.json` | Copilot commands, skills and `hooks/copilot-hooks.json` |
| Cursor | `ai-cursor-repo/integrations/ponytail` (pinned upstream submodule) | Native hooks installer; project rule alternative for Cloud Agents |
| Gemini CLI | [Gemini install guide](../gemini/README.md) | Upstream `gemini-extension.json`, context, commands and skills |
| Grok Build | Upstream native plugin; setup documented in [ai-grok-repo](https://github.com/Wicked-Sick-Ltd/ai-grok-repo) | Skills only; no lifecycle context injection |

## Claude Code

```sh
claude plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
claude plugin install ponytail@wickedsick
```

Machines using `ai-claude-repo` should instead update `wicked-sick` and install
`ponytail@wicked-sick`; both onboarding profiles include it. Choose one
marketplace per host to avoid duplicate skills or hooks. Fleet reconciliation
remains controlled by the existing `auto_reconcile` policy.

## Codex

```sh
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace --sparse .agents/plugins
codex plugin add ponytail@wickedsick
```

Alternatively use `ponytail@wicked-sick-codex` from `ai-codex-repo` as documented
there. Review and trust the hooks through `/hooks`, then start a new thread;
restart the desktop app after installing. Plugin installation and hook trust
are per machine; the portable permissions installer does not grant hook trust.

## Copilot CLI

```sh
copilot plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
copilot plugin install ponytail@wickedsick
```

The catalog explicitly selects Copilot's hook and command paths: the root
upstream `plugin.json` is Grok's minimal manifest, which Copilot discovers
before `.github/plugin/plugin.json`. Keep those catalog paths when updating.
See [Copilot's manifest and marketplace reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference).

Use `/ponytail:ponytail full` and `/ponytail:ponytail-review`. This is a
Copilot **CLI** listing; it does not promise automatic activation in every
Copilot editor integration.

## Cursor, Gemini and Grok

Cursor setup belongs in `ai-cursor-repo`; see [Cursor integration](cursor-integration.md).
There is no Cursor entry here because native hook installation is not an
in-repo marketplace plugin. Cursor Cloud Agents need the project rule
alternative or explicit mode activation through project hooks; they do not
run `sessionStart`. Cursor subagents do not receive Ponytail's injected rules.

Gemini uses the pinned extension command in [its guide](../gemini/README.md).
Grok Build installs the upstream skill-only plugin; its lifecycle hooks do not
inject Ponytail context. Do not infer Grok hook support from the Claude catalog.

## Operation and updates

Node.js must be on the host's non-interactive PATH for activation hooks.
Ponytail defaults to `full`; `lite`, `ultra` and `off` are available on hosts
with mode switching. Start with `full`, retain repo-specific requirements,
and use the review skill to identify unnecessary code. Validation, security,
accessibility and data-loss handling remain required.

For an update, inspect the new upstream manifests and relevant adapter tests,
then update the Claude/Copilot SHA and version, the Cursor submodule pointer,
the Gemini install reference and the revision recorded here. Update Claude's
marketplace and fleet minimum version together. Codex follows upstream's
default branch independently. Run `python3 scripts/validate.py` after index
edits and each vendor repo's checks before landing its changes.

## Host setup ownership

The private [Gemini](https://github.com/Wicked-Sick-Ltd/ai-gemini-repo),
[Copilot](https://github.com/Wicked-Sick-Ltd/ai-copilot-repo) and
[Grok](https://github.com/Wicked-Sick-Ltd/ai-grok-repo) repositories maintain
host-specific setup, update, rollback and validation records. Repository
creation or a guide alone does not establish that a live profile was tested.
