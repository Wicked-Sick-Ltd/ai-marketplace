# Amiga Decoding

Use `$amiga-adf-decompile` to investigate Amiga disk images through extraction,
recursive unpacking, code/data analysis and independent validation.

The [skill](skills/amiga-adf-decompile/SKILL.md) links to the full process. It
requires separate physical-byte, decoded-content and semantic-coverage ledgers;
extraction or automatic disassembly alone cannot establish completion. The process
incorporates Deuteros correction logs and Supremacy original-CPU comparisons.

It contains instructions only. Python disk utilities are not part of this plugin.
Game images, extracted assets and project-specific addresses stay in their own
investigation workspaces.

## Install

Install **amiga-decoding** from the public Wicked Sick marketplace in this
repository (`Wicked-Sick-Ltd/ai-marketplace`, catalog name `wickedsick`).

```sh
# Claude Code
claude plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
claude plugin install amiga-decoding@wickedsick

# Cursor
# Import Wicked-Sick-Ltd/ai-marketplace as a Team Marketplace, then install amiga-decoding.

# Codex
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
codex plugin add amiga-decoding@wickedsick

# GitHub Copilot CLI
copilot plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
copilot plugin install amiga-decoding@wickedsick

# Gemini CLI, after cloning this repository
gemini extensions install /path/to/ai-marketplace/plugins/amiga-decoding
```

Inside a Claude Code session the same install is `/plugin install amiga-decoding@wickedsick`. Gemini CLI installs the plugin directory itself. `gemini-extension.json` is at the root of `plugins/amiga-decoding/`.

Add the marketplace as a full checkout of this repository. A sparse checkout
that omits `plugins/amiga-decoding` cannot see this plugin: every catalog entry
below points at that directory.
