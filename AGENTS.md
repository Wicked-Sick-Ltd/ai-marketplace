# Agent instructions

This repository is an **index**. It lists plugins; it does not contain plugin code.

- Do not vendor plugin sources here.
- Claude entries are pinned to a full 40-character commit SHA (`git-subdir` + `sha`). Codex's Agent Plugins schema has no ref/sha field, so Codex entries name the repo URL and Codex resolves its default branch; the SHA of record for a Codex pack is that repo's merge commit, not anything in the index.
- Cursor's `.cursor-plugin/marketplace.json` uses **in-repo paths** only (`source` is a directory in this git tree, optionally under `metadata.pluginRoot`). Do not copy Claude `github`/`sha` source objects there. Cursor Team Marketplace should import the repo that contains the plugin directories (`ai-claude-repo`), not vendor those plugins here.
- List a plugin only on the catalogs where it has a real runtime.
- `token-usage` stays on the Claude index until other hosts have a parser or an honest "Claude transcripts only" listing.
- After catalog edits, run `python3 scripts/validate.py`.

A Next.js + Prisma demo app also lives in this tree, in-tree so the Cursor Cloud Agent environment has something to install and run ([`docs/demo-app.md`](docs/demo-app.md)). Do not treat its listings UI as plugin source or as a catalog — catalog edits are still edits to the index files above, followed by `python3 scripts/validate.py`. CI runs that Python validation only, so the demo app is unenforced there.

Product-repo agent rules (Forge, Yaegi, Traefik) live in those repos, not here.

## Cursor Cloud: Dependabot API access

The built-in Cloud Agent GitHub App token cannot call the Dependabot alerts API. For triage, inject a fine-grained PAT as `GH_TOKEN` with **Dependabot alerts: Read**, then run `python3 scripts/dependabot_alerts.py --check`. Details: [`docs/github-security-api-access.md`](docs/github-security-api-access.md).

## Repository custom properties

Live **2026-09-28** on `Wicked-Sick-Ltd` and `wizmediagg` (identical schema). This is the estate control plane for Cursor, Grok, Claude, Actions, and Copilot. Longer form, UI map, and limits: [`docs/repository-custom-properties.md`](docs/repository-custom-properties.md). Snapshot: [`docs/repo-schema-2026-09-28.json`](docs/repo-schema-2026-09-28.json). Notion: [custom properties](https://app.notion.com/p/3d84ce0f44518161afedf5ed02383eb4), [issue-label standards](https://app.notion.com/p/3d24ce0f445181ecaffee111caeb67af).

A property gates which repos an automation or session touches. Use these names and allowed values. When a property already expresses the gate, skip parallel tags and hard-coded repo allowlists. A new behavior is a new allowed value on both orgs, documented here the same day.

Repo values are still mostly empty. Empty means unassigned. The schema has no default.

### Three GitHub objects

| Object | Attaches to | Use |
| --- | --- | --- |
| Issue labels | Issues and pull requests | Work triage inside a repo. Governance set: `priority:high`, `priority:medium`, `priority:low`, `tech-debt`, `dependencies`, plus GitHub defaults. |
| Repository custom properties | A repository | This control plane. `GET /orgs/{org}/properties/schema` defines these fields. |
| Organization custom properties | An organization | Metadata about the org. Enterprise → Organizations → Custom properties. |

`/orgs/{org}/properties/schema` is the repository-property schema. Organization-object properties never write repository values. `gh label create` applies to the governance label set, not these property names.

### Live schema

Readers below are the snapshot's `readers` field. Notion names the hosts for `lifecycle`, `service_tier`, and `stack`.

| property_name | value_type | allowed_values | readers |
| --- | --- | --- | --- |
| `automation_groups` | `multi_select` | `daily-issue-pr-automation`, `weekly-general-improvements`, `weekly-performance-improvements`, `weekly-reporting`, `deployment`, `release`, `security-scanning`, `dependency-updates` | Copilot/Actions/shared automation |
| `automation_groups_cursor` | `multi_select` | `cursor-issue-pr-triage`, `cursor-performance`, `cursor-security`, `cursor-add-environment`, `cursor-bugbot` | Cursor + Grok Bot |
| `automation_groups_claude` | `string` | freeform until an enum is named; then `multi_select` | Claude |
| `git-rules` | `multi_select` | `main-only`, `dev-main`, `dev-staging-main` | rulesets/branch automation |
| `lifecycle` | `single_select` | `archived`, `maintenance`, `experimental`, `pre-launch`, `production`, `ramp-up` | Automation intensity; skip `archived` |
| `service_tier` | `single_select` | `best-efforts`, `internal`, `standard`, `critical` | Spend gating and draft-PR / review strictness |
| `priority` | `single_select` | `P0`, `P1`, `P2`, `P3` | daily sweep / Grok hygiene |
| `stack` | `multi_select` | `laravel-fluxui`, `laravel-forge`, `laravel`, `typescript`, `node`, `python`, `nextjs`, `react`, `php`, `go`, `static` | Stack-specific logic, Env Steward, props-detect |

`automation_groups_claude` is a string because the API rejects an empty `multi_select` allowed list. `git-rules` is the branch workflow (`dev-staging-main` is bounceiq-style). `priority` replaces the `daily-sweep-policy.json` P0 list once sweep code reads values.

### Values API

| Action | Route |
| --- | --- |
| Read definitions | `GET /orgs/{org}/properties/schema` |
| Read values | `GET /repos/{owner}/{repo}/properties/values` |
| Set values | `PATCH /repos/{owner}/{repo}/properties/values` |

`GET` returns `200` and `[{ "property_name", "value" }]`. `PATCH` returns `204`. `value` is a string (`single_select`, `string`), an array (`multi_select`), or `null` (unset). Batch repository writes: `PATCH /orgs/{org}/properties/values` with `repository_names` (max 30) and `properties`. That batch route still targets repositories.

```bash
gh api orgs/Wicked-Sick-Ltd/properties/schema
gh api repos/Wicked-Sick-Ltd/<repo>/properties/values
```
