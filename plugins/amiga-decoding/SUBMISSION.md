# Directory submission: amiga-decoding

Copy-paste fields for plugin directory submissions. Nothing here submits automatically; the repository owner submits by hand.

| Field | Value |
|---|---|
| Name | Amiga Decoding |
| Plugin id | `amiga-decoding` |
| Version | 1.0.0 |
| Repository | https://github.com/Wicked-Sick-Ltd/ai-marketplace |
| Plugin path | `plugins/amiga-decoding/` (manifest `.cursor-plugin/plugin.json`, skill `skills/amiga-adf-decompile/`) |
| Licence | MIT (`LICENSE`, `NOTICE`) |
| Author | Wicked Sick Ltd, craig@wickedsick.com |
| Logo | `assets/logo.svg` (1:1 SVG) |
| Category | Developer Tools |
| Tags | amiga, adf, decompilation, reverse-engineering, preservation, m68k |
| Works with | Grok Bot, Cursor, Claude Code, Codex, GitHub Copilot CLI, Gemini CLI |

## Short description

AI agent plugin that works with any AI agent. Evidence-led Amiga ADF extraction and decompilation to exhaustion, with separate disk, content and semantic coverage.

## Long description

Amiga Decoding gives your AI agent a disciplined process for investigating Amiga disk images (ADF files). It covers extraction, recursive unpacking of packed streams, code and data analysis, and independent validation. The skill requires three separate ledgers: physical bytes, decoded content and semantic coverage. Extraction or automatic disassembly alone can never mark a disk as finished. It incorporates correction logs from Wicked Sick's Deuteros work and original-CPU comparisons from its Supremacy work. It contains instructions only: no scripts, no network access, no credentials. Game images and extracted assets stay in your own workspace.

## Testing instructions

1. Add the plugin from `plugins/amiga-decoding/` in a Grok Bot account.
2. Ask: "Use amiga-adf-decompile to plan an investigation of an ADF disk image I will provide." Confirm the agent loads the skill and proposes the three coverage ledgers.
3. Ask it to declare a disk finished after only running a disassembler. Confirm it refuses and names the missing ledgers.
4. No account, key or sandbox is needed.

## Grok Bot install

Add this repository's `plugins/amiga-decoding` directory as a plugin, or install it from the marketplace once listed. Then ask Grok Bot to use `amiga-adf-decompile`.

## Data handling

Instructions only. Nothing is collected, sent or stored by the plugin.

## Submission route

grok-bot.directory lists shared bots and templates, not plugin repositories. Plugins go through https://x.ai/bot/marketplace/submit-a-plugin (public GitHub repo, short description, testing instructions, 1:1 logo, tested-locally-and-in-app confirmation).
