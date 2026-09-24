# Cursor team marketplace

How Wicked Sick gets **Cursor** (IDE, Cloud Agents, CLI) onto the same plugins
and skills we already run on Claude Code — without copying plugin source into
this catalog repo.

Convention for *how we work* stays in
[`ai-claude-repo/CONVENTIONS.md`](https://github.com/Wicked-Sick-Ltd/ai-claude-repo/blob/main/CONVENTIONS.md)
(session bookends, PRs, Risk Tier, `.remember/`, estate plugins). Product-repo
rules stay in each product's `AGENTS.md` / `CLAUDE.md`. This repo only **lists**
installable plugins.

Cursor's public docs: [Plugins](https://cursor.com/docs/plugins) and
[Plugins reference](https://cursor.com/docs/reference/plugins).

## Where we are (2026-09-16)

| Surface | State |
| --- | --- |
| Org catalog repo | `Wicked-Sick-Ltd/ai-marketplace` exists. Claude index lists `token-usage` pinned to SHA `67164452…`. Cursor / Codex / Copilot indexes are **empty**. |
| Working Claude marketplace | [`ai-claude-repo`](https://github.com/Wicked-Sick-Ltd/ai-claude-repo) still ships the plugins people actually install (`onboarding`, `session-lifecycle`, `estate-maintenance`, `product-lifecycle`, `wizzo-twin`, plus remote `token-usage`). |
| Cloud Agent compatibility | Several plugin repos have `.cursor/environment.json`. That is **Cloud Agent VM setup**, not a Cursor plugin. It does not put skills on Customize → Plugins. |
| Cursor plugin shims | None. No repo has `.cursor-plugin/plugin.json` or a root Agent Plugins `plugin.json` / `mcp.json`. |
| This catalog's Cursor file | `.cursor-plugin/marketplace.json` is a valid empty Team Marketplace stub (`name: wickedsick`). Connecting it in the dashboard today would install **zero** plugins. |

Rollout steps 1–2 from
[cross-ai-marketplace-plan.md](https://github.com/Wicked-Sick-Ltd/traefik-laravel-forge/blob/master/docs/cross-ai-marketplace-plan.md)
are done. Step 5 (Cursor team marketplace with a *portable* workflow plugin) is
not.

## Two Cursor formats (pick one per plugin)

### Ponytail (2026-09-23)

Ponytail's native Cursor hook adapter is held as a pinned upstream submodule at
`Wicked-Sick-Ltd/ai-cursor-repo/integrations/ponytail`. That repo's
`docs/ponytail.md` covers initialization, user/project installation, verification,
Cloud Agent rules and uninstall. Its source is not copied into this index, and
the hook adapter is not listed as a Cursor marketplace plugin here.

The adapter preserves existing hooks. It needs Node.js on Cursor's PATH and a
stable checkout path. Cloud Agents do not run `sessionStart`, so use the
documented project rule alternative or explicitly activate a mode through
project hooks. Subagents do not receive the injected context.

### Plugin formats

Cursor loads both. Team marketplaces can distribute either.

| Format | Manifest | Ships | Use when |
| --- | --- | --- | --- |
| **Agent Plugins 1.0** | Root `plugin.json` (`$schema` from agent-plugins.org) + `skills/` + optional `mcp.json` | Skills + MCP only | The plugin is a workflow skill or remote MCP we also want on Copilot / Codex. |
| **Cursor Plugin** | `.cursor-plugin/plugin.json` | Skills, MCP, **rules**, **agents**, **commands**, **hooks**, **variables** | We need slash-style `commands/`, Cursor hooks, or dashboard variables (API tokens). |

Portable floor: **one** `skills/<id>/SKILL.md` (Agent Skills) plus **one**
`mcp.json` at the plugin root. Claude keeps `.claude-plugin/plugin.json`. Do not
fork the skill body per host.

Cursor expands `${CURSOR_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_ROOT}` in MCP
`command` / `cwd`. It does **not** expand Agent Plugins `${PLUGIN_ROOT}`. For
stdio MCP, use `${CURSOR_PLUGIN_ROOT}`.

## Why this catalog cannot SHA-pin Cursor plugins the Claude way

Claude's `.claude-plugin/marketplace.json` accepts a GitHub `source` object
(`repo` + 40-char `sha`). Cursor's `.cursor-plugin/marketplace.json` does not.

Cursor resolves each `plugins[].source` as a **path inside the imported git
repo** (optionally prefixed by `metadata.pluginRoot`). Parser then looks for
`<source>/.cursor-plugin/plugin.json` (Cursor Plugin) or a root `plugin.json`
(Agent Plugin). Official template:
[fieldsphere/cursor-team-marketplace-template](https://github.com/fieldsphere/cursor-team-marketplace-template).

So:

- **Do not** copy Claude `{"source":"github","repo":"…","sha":"…"}` into the
  Cursor index. `scripts/validate.py` rejects that.
- **Do not** vendor plugin trees here to satisfy Cursor. Plugin behaviour stays
  in `ai-claude-repo` / `token-usage`.
- **Do** import the repo that *contains* the plugin directories as the Cursor
  Team Marketplace.

## Recommended org wiring

### Daily driver: import `ai-claude-repo`

Dashboard → Plugins → Team Marketplaces → **Import from Repo** →
`Wicked-Sick-Ltd/ai-claude-repo` (Teams: one marketplace; Enterprise: unlimited).

That repo already uses `plugins/<name>/` plus skills and `commands/` — the same
layout Cursor discovers. After each plugin gets a Cursor/Agent Plugins manifest,
add a Cursor catalog **in `ai-claude-repo`**:

```json
{
  "name": "wickedsick",
  "owner": { "name": "Wicked Sick Ltd", "email": "craig@wickedsick.com" },
  "metadata": {
    "description": "Wicked Sick plugins for Cursor",
    "pluginRoot": "plugins"
  },
  "plugins": [
    { "name": "session-lifecycle", "source": "session-lifecycle" }
  ]
}
```

Turn on **Auto Refresh** (Cursor GitHub App on the repo) so pushes re-index at
most every 10 minutes.

`token-usage` is a **different git repo**. Add it to the same Team Marketplace
with **Add to Marketplace** (individual plugin URL), or keep it off Cursor
until it can parse Cursor session logs (see matrix below).

### This repo (`ai-marketplace`)

Keep `.cursor-plugin/marketplace.json` as the **cross-AI stub** so the org
catalog file exists at the path Cursor documents. List a plugin here only if we
later choose to host a Cursor-native pack *in this repo* (still no vendored
upstream). Until then the array stays empty on purpose.

### `wizzo-fleet-presence` — hooks, not a plugin

Fleet presence for Cursor is a **hooks template**, not a Cursor plugin, so it
does not appear in any `plugins[]` array. Source of truth:
`Wicked-Sick-Ltd/acsendr` at `mcp/hooks/cursor/` — a `.cursor/hooks.json`
binding `sessionStart` / `preToolUse` / `postToolUse` / `sessionEnd`, plus
`.cursor/hooks/coordctl-hook.sh`, which calls `coordctl <verb> --vendor cursor`.

Two install modes, and there is no third: a `CURSOR_CONFIG_DIR`-rooted
`hooks.json` silently does not fire, so Cursor hook discovery is project-level
or user-level only.

1. **Interactive, on a human's box** — copy the template to `~/.cursor/hooks.json`
   (and its script to `~/.cursor/hooks/`), then restart Cursor.
2. **Headless, in a sidecar worktree** — nothing to install by hand. The sidecar
   writes the template into each worktree at spawn, adds it to the worktree's
   `.git/info/exclude` so it never reaches the agent's diff or its PR, and
   removes it with the worktree.

Two Cursor-specific notes carried from the executor spike: `beforeSubmitPrompt`
and `stop` do not fire in headless `-p` runs, so the liveness signal is
`postToolUse` cadence, rate-limited client-side to at most one call per 60 s.
And headless Cursor workers get **no hub MCP** this tranche — the sidecar
performs claim/verify/complete/escalate on the worker's behalf, so no bearer
token needs to touch a worktree. Interactive users manage their own
`~/.cursor/mcp.json`.

Verify either mode the same way: `coordctl status` shows the box with the
`cursor` vendor tag.

### Public Cursor Marketplace

`cursor.com/marketplace/publish` is last, after the team catalog works. Same
rule as Claude's official directory.

## Conversion recipe (in the plugin source repo)

Do this in `ai-claude-repo` / `token-usage`, then bump the pin in this catalog's
Claude index if the Claude listing changes.

1. **Keep** `skills/<name>/SKILL.md`. Strip or omit Claude-only `allowed-tools`
   (`mcp__plugin_…`) so Cursor/Gemini are not bound to dead tool names. Trigger
   language in `description` stays.
2. **Keep** `commands/*.md` where they exist — Cursor discovers `commands/` on
   Cursor Plugins. Claude slash commands and Cursor commands can share the same
   files.
3. Add **`.cursor-plugin/plugin.json`** (`name` required; copy description /
   version / author from the Claude manifest).
4. If there is MCP: add root **`mcp.json`**. Move HTTP servers from Claude
   `.mcp.json`. Declare secrets under `variables` in the Cursor manifest; put
   only `${VAR}` placeholders in `mcp.json`. For stdio, `cwd` /
   `command` use `${CURSOR_PLUGIN_ROOT}`.
5. Optional portable floor: root **`plugin.json`** with
   `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` so Copilot and
   Codex can load the same skills+MCP without Cursor extras.
6. **Do not** port Claude `hooks/hooks.json` by copying it. Cursor hook event
   names differ (`sessionEnd` vs Claude `Stop`). Rebuild or skip.
7. Test locally: copy the plugin dir to `~/.cursor/plugins/local/<name>/`,
   reload, confirm Customize shows skills/commands/MCP.
   Enterprise: **Allow Local Plugin Imports** may be off.
8. Only then list it on a Cursor catalog (in `ai-claude-repo`, or Add to
   Marketplace from the plugin repo).

## Plugin matrix (what to ship on Cursor)

Live Claude plugins today: `ai-claude-repo` marketplace + `token-usage`.

| Plugin | Cursor? | Shape | Notes |
| --- | --- | --- | --- |
| `session-lifecycle` | **Yes — first portable skill** | Cursor Plugin: existing `skills/` + `commands/startup.md` + `commands/shutdown.md` | Portfolio `.remember/` workflow from CONVENTIONS.md. Host-neutral git/shell. Best first Team Marketplace listing. |
| `estate-maintenance` | **Yes** | Cursor Plugin (skills + commands) | Skills call scripts in `wicked-repo-inventory`. Confirm those scripts run from Cursor Cloud Agents (inventory access, `gh`, dry-run defaults). |
| `product-lifecycle` | **Yes** | Cursor Plugin (`commands/product-*.md` + any skills) | Prompt library; Notion writes. No Claude-only parser. |
| `onboarding` | **Partial** | Skill yes; bootstrap later | `/onboard` + `CONVENTIONS.md` check ports. `scripts/bootstrap.sh` is Claude-marketplace (`/plugin marketplace add ai-claude-repo`). Cursor equivalent is Team Marketplace import + Default On, not that script. |
| `token-usage` | **Not yet** | — | Skill + MCP + Stop hook are Claude/Cowork transcript-shaped (`~/.claude/projects`, `${CLAUDE_PLUGIN_ROOT}`). Listing it on Cursor without a Cursor log parser is a lie. Cloud `environment.json` does not fix that. Revisit when a Cursor parser exists, or with an explicit "Claude transcripts only" listing. |

Workflow skills belong on every Agent Skills catalog **after** the shims above.
Host-specific observability stays on the host that produces the logs.

## Codex / Copilot / Gemini (same portable floor)

Once a plugin has root `plugin.json` + `skills/` + `mcp.json`:

| Host | Catalog in this repo | Extra shim |
| --- | --- | --- |
| ChatGPT Work / Codex | `.agents/plugins/marketplace.json` | Often reads Agent Plugins; `.codex-plugin/` only if needed |
| Copilot | `.github/plugin/marketplace.json` | Optional `com.github.copilot/` |
| Gemini CLI | `gemini/README.md` row | `gemini-extension.json` at the **plugin repo** root |
| Grok | Claude catalog | Already reads `.claude-plugin/` |

Pin remotes on those JSON catalogs with a full SHA, same as Claude.

## Team Marketplace install (humans)

1. Admin: Dashboard → Plugins → import `ai-claude-repo` (after Cursor manifests exist).
2. Set access (whole team or Organisation Groups).
3. Per plugin: Default Off / Default On / Required. Suggest Default On for
   `session-lifecycle`; Required only for policy plugins
   Off and owner-group restricted.
4. Developers: Customize → team marketplace → install. Skills also via
   `/skill-name`.
5. Optional: members can Publish a personal `~/.cursor/skills/` skill to the
   **Default** marketplace. That is *not* a substitute for `ai-claude-repo` PRs.
   Canonical skills still land in git.

## Checklist (when we implement)

- [ ] Add `.cursor-plugin/plugin.json` (and root `mcp.json` where needed) to
      `session-lifecycle` in `ai-claude-repo`; local-load test.
- [ ] Add `.cursor-plugin/marketplace.json` to `ai-claude-repo` with `pluginRoot: plugins` and only plugins that have a real Cursor runtime.
- [ ] Import that repo as the Cursor Team Marketplace; Auto Refresh on.
- [ ] Repeat for `estate-maintenance`, `product-lifecycle`.
- [ ] Decide Cursor story for `onboarding` (skill vs skip bootstrap).
- [ ] Leave `token-usage` off Cursor until logs or an honest Claude-only label.
- [ ] Add Agent Plugins `plugin.json` on plugins we also list on Codex/Copilot.
- [ ] Point this repo's Cursor index at in-repo paths only if we ever host a Cursor pack here; keep it empty until then.
