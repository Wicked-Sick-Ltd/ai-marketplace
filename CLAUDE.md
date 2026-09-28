# Claude Code instructions

@AGENTS.md

## Repository custom properties

Live **2026-09-28** on `Wicked-Sick-Ltd` and `wizmediagg` (identical schema). Same vocabulary as [`AGENTS.md`](AGENTS.md). Longer form: [`docs/repository-custom-properties.md`](docs/repository-custom-properties.md). Snapshot: [`docs/repo-schema-2026-09-28.json`](docs/repo-schema-2026-09-28.json). Notion: [custom properties](https://app.notion.com/p/3d84ce0f44518161afedf5ed02383eb4), [issue-label standards](https://app.notion.com/p/3d24ce0f445181ecaffee111caeb67af).

A property gates which repos a Claude workflow touches. Use these names and allowed values. When a property already expresses the gate, skip parallel tags and hard-coded repo allowlists. A new behavior is a new allowed value on both orgs, documented here the same day.

Repo values are still mostly empty. Empty means unassigned. The schema has no default. `automation_groups_claude` is the Claude field: freeform `string` until its enum is named, then `multi_select` (the API rejects an empty `multi_select` allowed list).

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
