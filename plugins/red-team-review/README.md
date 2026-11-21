# Red-team review

Use `$red-team-review` before shipping a claim, public copy, pricing, legal or
investor statement, launch, cutover or big merge. The skill is an adversarial
fact-check and a pre-mortem. The reviewer did not write the thing under review
and does not fix it.

The [skill](skills/red-team-review/SKILL.md) is instructions only. It does not
run tools, call a network or read credentials. For code, pair it with an
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
```

Inside a Claude Code session the same install is `/plugin install red-team-review@wickedsick`. Gemini CLI installs the plugin directory itself. `gemini-extension.json` is at the root of `plugins/red-team-review/`.

Add the marketplace as a full checkout of this repository. A sparse checkout
that omits `plugins/red-team-review` cannot see this plugin: every catalog entry
points at that directory.
