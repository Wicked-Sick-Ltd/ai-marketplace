# Directory submission: obsidian (Wicked Sick reviewed fork)

Copy-paste fields for plugin directory submissions. Nothing here submits automatically; the repository owner submits by hand.

**Duplicate warning.** The Grok Bot plugin catalog already lists an Obsidian plugin from the upstream project (catalog id 88871845). This fork is a strict subset of it: the three skills below are byte-for-byte upstream, and the four skills upstream also ships (obsidian-cli, obsidian-headless, defuddle, knap) are removed. It adds no capability. Do not submit it as "Obsidian" or as an official plugin. See the recommendation in the pull request.

| Field | Value |
|---|---|
| Name | Obsidian Format Skills (Wicked Sick reviewed fork) |
| Plugin id | `obsidian` |
| Version | 1.2.0 (upstream 1.2.0) |
| Repository | https://github.com/Wicked-Sick-Ltd/ai-marketplace |
| Plugin path | `plugins/obsidian/` (manifest `.cursor-plugin/plugin.json`, skills `skills/*`) |
| Fork source | https://github.com/Wicked-Sick-Ltd/obsidian-skills, branch `wicked-main`, commit `cd51b7076a1207c805cf1d95da4c56cb96bbe859` |
| Upstream | https://github.com/obsidianmd/obsidian-skills |
| Licence | MIT, Copyright (c) 2026 Steph Ango (@kepano) (`LICENSE`, `NOTICE`) |
| Original author | Steph Ango / Obsidian |
| Maintainer of this fork | Wicked Sick Ltd |
| Logo | `assets/icon.png` (Obsidian's; use only if the owner permits) |
| Tags | obsidian, markdown, bases, canvas, pkm, notes |
| Works with | Grok Bot, Cursor, Claude Code, Codex, Gemini CLI |

## Short description

Unofficial Wicked Sick fork of the Obsidian skills that works with any AI agent: Obsidian Flavored Markdown, Bases and JSON Canvas files. Format guidance only, with no shell, network or credentials.

## Long description

Three instruction-only skills for working with Obsidian vault files: obsidian-markdown (wikilinks, embeds, callouts, properties), obsidian-bases (.base files with views, filters, formulas and summaries) and json-canvas (.canvas files with nodes, edges and groups). This is Wicked Sick's reviewed fork of Steph Ango's MIT-licensed obsidianmd/obsidian-skills. The skill text is unchanged. The command-line and web-extraction skills from upstream are left out, so nothing in this plugin runs a program. It is not an official Obsidian release and is not endorsed by Obsidian.

## Testing instructions

1. Add the plugin from `plugins/obsidian/` in a Grok Bot account.
2. Ask: "Create a note with a status property, two wikilinks and a warning callout." Confirm Obsidian syntax is used.
3. Ask: "Create a reading-list Base with table and card views." Confirm a valid `.base` YAML file.
4. Ask: "Make a Canvas linking three ideas with labelled edges." Confirm valid JSON Canvas.
5. No account or key is needed.

## Grok Bot install

Add this repository's `plugins/obsidian` directory as a plugin, or install it from the marketplace once listed. Then ask Grok Bot for Obsidian notes, Bases or Canvas files.

## Submission route

grok-bot.directory lists shared bots and templates, not plugin repositories. Plugins go through https://x.ai/bot/marketplace/submit-a-plugin.
