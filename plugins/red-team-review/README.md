# Red-team review

Use `$red-team-review` before shipping a claim, public copy, pricing, legal or
investor statement, launch, cutover or big merge. The skill is an adversarial
fact-check and a pre-mortem. The reviewer did not write the thing under review
and does not fix it.

The [skill](skills/red-team-review/SKILL.md) is an instruction-only package. It
ships no tool, network client or credential file. Carrying out the review may
still use the host's tools and the network to read code, live behaviour and
official documentation. It does not read credentials. For code, pair it with an
independent code review.

## Install

Install **red-team-review** from the public Wicked Sick marketplace in this
repository (`Wicked-Sick-Ltd/ai-marketplace`, catalog name `wickedsick`).

```sh
# Claude Code
claude plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
claude plugin install red-team-review@wickedsick

# Cursor
# Import Wicked-Sick-Ltd/ai-marketplace as a Team Marketplace, then install red-team-review.

# Codex
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
codex plugin add red-team-review@wickedsick

# GitHub Copilot CLI
copilot plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
copilot plugin install red-team-review@wickedsick

# Gemini CLI, after cloning this repository
gemini extensions install /path/to/ai-marketplace/plugins/red-team-review

# Antigravity, same directory
agy plugin install /path/to/ai-marketplace/plugins/red-team-review
agy plugin list
```

Inside a Claude Code session the same install is `/plugin install red-team-review@wickedsick`. Gemini CLI and Antigravity both install the plugin directory itself. `plugin.json` and `gemini-extension.json` are at the root of `plugins/red-team-review/`. Antigravity can also copy that directory to `~/.gemini/config/plugins/red-team-review`. The host guide is `gemini/README.md`.

Add the marketplace as a full checkout of this repository. A sparse checkout
that omits `plugins/red-team-review` cannot see this plugin: every catalog entry
points at that directory.
