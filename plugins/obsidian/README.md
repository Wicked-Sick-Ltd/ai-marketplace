# Obsidian

Skills for Obsidian Flavored Markdown, Bases, and JSON Canvas.

## Install

Clone `wicked-main` and point the tool at that checkout. The repository default branch is `main`, which still contains the held skills, so an `owner/repo` marketplace add installs those too.

```sh
git clone --branch wicked-main --single-branch https://github.com/Wicked-Sick-Ltd/obsidian-skills.git
cd obsidian-skills
claude --plugin-dir "$PWD"
codex plugin marketplace add "$PWD"
```

In Cursor, open that checkout. Project skills are linked at `.cursor/skills/`. See [docs/PORTING.md](../../docs/PORTING.md).

## Included skills

- obsidian-markdown: Obsidian links, properties, callouts, and embeds.
- obsidian-bases: Bases files, views, filters, formulas, and summaries.
- json-canvas: Canvas files with nodes, edges, groups, and connections.

These skills describe file formats. They do not run shell commands.

## Held back

Upstream also ships `obsidian-cli`, `obsidian-headless`, `defuddle`, and `knap`. This fork keeps that text in `held/` and does not link it into the plugin. The reasons are in [REVIEW.md](../../REVIEW.md).

## Scope

This plugin contains skills only, with no MCP server, hooks, or background processes.

Upstream: https://github.com/obsidianmd/obsidian-skills
