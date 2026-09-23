# AI vendor repository migration implementation plan

> **For agentic workers:** Use superpowers:executing-plans to implement this plan task by task. Checkboxes track execution, not approval to deploy.

**Goal:** Coordinate catalog and documentation changes while keeping this repository an index.

**Architecture:** Vendor repositories own runtime material. This repository links to them using each host's supported catalog format and links to the plans held in each vendor repository.

**Tech stack:** GitHub repositories, JSON catalogs, Markdown, Python catalog validation.

**Spec:** [AI vendor repositories — migration and documentation plan](https://app.notion.com/p/3e44ce0f445181bb8c7dc1ac5eb6ac22).

**Status:** Planned, 2026-09-23. This document records future work. Merging this documentation does not perform a rename, installation, migration or deployment.

## Global constraints

- Standardise private host repositories on ai-<vendor>-repo; keep the public ai-marketplace name and index-only role.
- Preserve marketplace IDs wicked-sick, wickedsick and wicked-sick-codex, plugin identities, hook ownership and installed-state formats.
- Keep existing local checkout paths during the first cutover; change remotes first. Schedule optional directory moves separately.
- Keep credentials, machine-specific trust and private runtime data out of commits. Retain each host's supported schema and list only working runtimes.
- Prepare dependent changes and inventory mapping before renaming; rename Codex, then Cursor, then Claude. Never recreate an old repository slug.
- Recheck current default branches, open PRs, repository IDs, protections, app access and inventory records immediately before execution.

## Repository map

| Current repository | Destination | Work |
| --- | --- | --- |
| claude-repo | ai-claude-repo | Rename; preserve Claude plugin ownership |
| codex-repo | ai-codex-repo | Rename; preserve existing installer state |
| cursor-repo | ai-cursor-repo | Rename; move Grok material to its own private repository |
| New private repository | ai-gemini-repo | [Gemini creation plan](https://github.com/Wicked-Sick-Ltd/ai-gemini-repo/pull/1) |
| New private repository | ai-copilot-repo | [Copilot creation plan](https://github.com/Wicked-Sick-Ltd/ai-copilot-repo/pull/1) |
| New private repository | ai-grok-repo | [Grok creation plan](https://github.com/Wicked-Sick-Ltd/ai-grok-repo/pull/1) |
| ai-marketplace | ai-marketplace | Update references; retain the public index |

Acsendr and wicked-repo-inventory have companion plans in their own docs directories. The community awesome-copilot repository remains separate.

## Repository planning PRs

Each PR adds docs/ai-vendor-repository-migration.md and links it from the repository README. The plans remain pending execution.

| Repository | Planning PR |
| --- | --- |
| claude-repo | [Review plan](https://github.com/Wicked-Sick-Ltd/claude-repo/pull/36) |
| codex-repo | [Review plan](https://github.com/Wicked-Sick-Ltd/codex-repo/pull/8) |
| cursor-repo | [Review plan](https://github.com/Wicked-Sick-Ltd/cursor-repo/pull/3) |
| acsendr | [Review plan](https://github.com/Wicked-Sick-Ltd/acsendr/pull/225) |
| wicked-repo-inventory | [Review plan](https://github.com/Wicked-Sick-Ltd/wicked-repo-inventory/pull/52) |
| ai-gemini-repo | [Review plan](https://github.com/Wicked-Sick-Ltd/ai-gemini-repo/pull/1) |
| ai-copilot-repo | [Review plan](https://github.com/Wicked-Sick-Ltd/ai-copilot-repo/pull/1) |
| ai-grok-repo | [Review plan](https://github.com/Wicked-Sick-Ltd/ai-grok-repo/pull/1) |

## Task 1: Establish the migration baseline

- [ ] Review and land the Ponytail baseline PRs: [marketplace #14](https://github.com/Wicked-Sick-Ltd/ai-marketplace/pull/14), [Claude #35](https://github.com/Wicked-Sick-Ltd/claude-repo/pull/35), [Codex #7](https://github.com/Wicked-Sick-Ltd/codex-repo/pull/7), [Cursor #2](https://github.com/Wicked-Sick-Ltd/cursor-repo/pull/2). Recheck their current status and checks; they were separate, unmerged changes when this plan was written.
- [ ] Record the resulting default-branch commits and resolve any conflicts with this documentation.
- [ ] Verify access and protections for the three owner-created private repositories. Each has a separate documentation PR; creation is complete, runtime integration remains pending.
- [ ] Coordinate inventory page-ID mappings and dependent bootstrap/sidecar changes before the first rename.

## Task 2: Update catalogs after each destination is reachable

Files: .claude-plugin/marketplace.json, .agents/plugins/marketplace.json, .github/plugin/marketplace.json, .cursor-plugin/marketplace.json, gemini/README.md, README.md, AGENTS.md, CONTRIBUTING.md and docs/cursor-integration.md. Include docs/ponytail.md after baseline #14 lands.

- [ ] Change references to renamed first-party source repositories without changing plugin names or marketplace IDs.
- [ ] Keep Claude and Copilot remote entries pinned to full 40-character commits. Verify each pinned commit remains reachable at the new URL.
- [ ] Keep Codex entries as repository URLs: its Agent Plugins schema has no ref/sha field. Record source merge commits in the migration evidence.
- [ ] Keep Cursor entries as in-repo paths only. Point Team Marketplace setup at the repository actually containing the plugin directories; a repository rename does not relocate those directories.
- [ ] Keep Gemini installation instructions in gemini/README.md; do not invent a Gemini JSON catalog.
- [ ] Preserve upstream Ponytail source references unless an independently reviewed upstream update is intended. Do not vendor plugin source here.
- [ ] Align CONTRIBUTING.md's older blanket SHA instruction with the Codex exception already documented in AGENTS.md.
- [ ] Commit the catalog cutover separately from runtime implementation changes.

## Task 3: Verify and publish documentation

    python3 scripts/validate.py
    git diff --check
    rg -n --hidden -g '!.git/**' 'claude-repo|codex-repo|cursor-repo' .

- [ ] Require validator success and classify each old-name match as an active reference to update or intentional history/compatibility text.
- [ ] Verify discovery/install on each listed host in isolated profiles; do not infer runtime support from a manifest alone.
- [ ] Update the Notion knowledgebase, onboarding, governance and inventory links after the corresponding destinations are live. Preserve Notion page IDs and historical deployment evidence.
- [ ] Link completed per-repo execution records from this document and Notion.

## Rollback

Revert a failing catalog/reference cutover through a normal PR, retaining prior pin values and commit evidence. Prefer repairing a caller while retaining the new repository name. Before any rename-back, verify the original slug is still available and refers to the intended repository; never create a replacement at the old slug. Leave new runtime listings unpublished until validation succeeds.

## Completion record

During execution, record the responsible operator, date, source and destination repository IDs, baseline and landed commit SHAs, companion PRs, checks with results, pilot outcome, inventory page IDs and rollback evidence here and in the Notion plan. Until that evidence exists, leave the execution checkboxes open.
