# Repository custom properties

Live schema date: **2026-09-28**. Defined on **Wicked-Sick-Ltd** and **wizmediagg** with the same names and allowed values. This page is the marketplace vocabulary for Cursor, Grok, Claude, Actions, and Copilot.

Machine-readable copy of that snapshot: [`repo-schema-2026-09-28.json`](repo-schema-2026-09-28.json).

Human source of record: [GitHub custom properties (org vs repo)](https://app.notion.com/p/3d84ce0f44518161afedf5ed02383eb4). Issue-label governance stays on [Repository Standards & Governance](https://app.notion.com/p/3d24ce0f445181ecaffee111caeb67af).

Sessions load the same names from [`AGENTS.md`](../AGENTS.md) and [`CLAUDE.md`](../CLAUDE.md).

## One control plane

A property gates which repos an automation, sweep, or agent touches. Membership, stack, lifecycle, service tier, sweep priority, and branch workflow are repository custom properties.

When one of these properties already expresses the gate, use it. A new behavior gets a new allowed value on this schema (both orgs, same day) and a same-day edit here and on the Notion page. Parallel tag sets and hard-coded repo allowlists are outside this vocabulary.

Values on individual repos are still mostly empty. An empty value is unassigned. The schema sets no default, so client code must not invent one.

## Three GitHub objects

GitHub uses similar names for three different objects. Pick the object by what it attaches to.

| Object | Attaches to | What it is for |
| --- | --- | --- |
| **Issue labels** | Issues and pull requests (catalog stored per repo) | Triage of work *inside* a repo. Estate governance set: `priority:high`, `priority:medium`, `priority:low`, `tech-debt`, `dependencies`, plus GitHub's default labels. |
| **Repository custom properties** | A **repository** | This control plane. Stack, automation groups, sweep priority, lifecycle, service tier, branch workflow. Targetable by **repository** rulesets. |
| **Organization custom properties** | An **organization** (`Wicked-Sick-Ltd`, `wizmediagg`, …) | Metadata about the org as a whole. Targetable by **enterprise organization** rulesets. |

`/orgs/{org}/properties/schema` defines **repository** properties for that org. It does not describe the organization object.

Organization-object properties are edited at Enterprise → **Organizations** → Custom properties. That surface never writes repository values. Historical organization-object definitions from the 2026-09-28 export are not this schema. Leave them unused for repo automation; delete them once Craig confirms they are unused.

Issue-label creation (`gh label create`) is for the governance set on the standards page. These property names are not labels.

### Where you are in the UI

| If you are looking at… | You are editing… |
| --- | --- |
| Enterprise → **Policies** → Custom properties | **Repository** property definitions (and promotion of org-defined repo properties) |
| Enterprise → **Organizations** → Custom properties | **Organization** property definitions and values on orgs |
| Org → Settings → Repository → Custom properties | Repo property definitions local to that org, plus **Set values** on its repos |
| Repo → Settings → Custom properties | Values on that one repo |
| Repo → Issues → Labels | Issue labels |

## Definition site and value site

Defining a field does not assign it on repos.

1. **Define the field** (name, type, allowed values) on each org. The 2026-09-28 schema was written with `PUT /orgs/{org}/properties/schema/{name}` on both `Wicked-Sick-Ltd` and `wizmediagg`. Enterprise → Policies → Custom properties is the place when a field must exist in every org.
2. **Set the value on repositories** with the values API below, Org Settings → Repository → Custom properties → **Set values**, or the repo's own Custom properties page.

An enterprise definition fills a repo only when the property is required and has a default. Every property in this schema is optional and has no default.

Official references: [enterprise repository properties](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-accounts-and-repositories/managing-repositories-in-your-enterprise/managing-custom-properties-for-repositories-in-your-enterprise), [organization repository properties](https://docs.github.com/en/organizations/managing-organization-settings/managing-custom-properties-for-repositories-in-your-organization), [organization-object properties](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-accounts-and-repositories/managing-organizations-in-your-enterprise/managing-custom-properties-for-organizations).

## Live schema (2026-09-28)

Verify with `gh api orgs/Wicked-Sick-Ltd/properties/schema` and `gh api orgs/wizmediagg/properties/schema`.

`readers` is the snapshot field when present. Notes for `lifecycle`, `service_tier`, and `stack` come from the Notion page, which is where those hosts are named.

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

`automation_groups_claude` stays a string because the API rejects an empty `multi_select` allowed list. Convert it to `multi_select` once the enum is named.

`git-rules` is the branch workflow for rulesets. It replaces the old workflow 1 / 2 / 3 labels: `main-only`, `dev-main`, and `dev-staging-main` (bounceiq-style).

`priority` is the daily-sweep and Grok residual-hygiene order. `daily-repo-sweep.py` still uses `daily-sweep-policy.json` as a temporary fallback. The next code change reads `priority`, `automation_groups`, `automation_groups_cursor`, `automation_groups_claude`, `stack`, `lifecycle`, and `service_tier` from repository property values.

Grok Bot PR hygiene, hot-repo listeners, Env Steward, and Bugbot take their repo set from `automation_groups_cursor`, `priority`, and `service_tier` once those listeners read property values. Until then, a hard-coded repo list in those tools is a fallback, not a second vocabulary.

## Values API

These three routes are the control-plane API from the 2026-09-28 snapshot. They read and write **repository** properties.

| Action | Route |
| --- | --- |
| Read definitions | `GET /orgs/{org}/properties/schema` |
| Read values | `GET /repos/{owner}/{repo}/properties/values` |
| Set values | `PATCH /repos/{owner}/{repo}/properties/values` |

`GET` values returns `200` and an array of `{ "property_name", "value" }`. Readers with repository read access can call it. `value` is a string, an array, or null.

`PATCH` values returns `204`. Repository admins, and anyone with the repository fine-grained permission **edit custom property values**, can call it. Body:

```json
{
  "properties": [
    {"property_name": "priority", "value": "P2"},
    {"property_name": "stack", "value": ["nextjs", "typescript"]},
    {"property_name": "lifecycle", "value": null}
  ]
}
```

Value shape follows `value_type`:

| value_type | `value` |
| --- | --- |
| `single_select` | one allowed string |
| `string` | a string (`automation_groups_claude`) |
| `multi_select` | an array of allowed strings |
| unset | `null` removes the value |

A batch write of the same repository values uses `PATCH /orgs/{org}/properties/values` with `repository_names` (at most 30) and `properties`. That route still targets repositories. It does not set organization-object properties.

Read examples:

```bash
gh api orgs/Wicked-Sick-Ltd/properties/schema
gh api orgs/wizmediagg/properties/schema
gh api repos/Wicked-Sick-Ltd/<repo>/properties/values
```

REST reference: [repository custom property values](https://docs.github.com/en/rest/repos/custom-properties), [organization repository properties](https://docs.github.com/en/rest/orgs/custom-properties).

## Limits

GitHub limits, as recorded on the Notion page:

- Up to 100 property definitions per enterprise.
- Allowed-value lists up to 200 items.
- Names: `a-z`, `A-Z`, `0-9`, `_`, `-`, `$`, `#`. No spaces. At most 75 characters.
- Values: printable ASCII except `"`.
- Types: `string`, `single_select`, `multi_select`, `true_false`. Repository properties also allow `url` in the API.

## Change process

1. Change the field in GitHub (enterprise first when it should exist in every org). Keep `Wicked-Sick-Ltd` and `wizmediagg` identical.
2. Set or update **values** on repositories.
3. Update this page, [`AGENTS.md`](../AGENTS.md), [`CLAUDE.md`](../CLAUDE.md), [`repo-schema-2026-09-28.json`](repo-schema-2026-09-28.json), and the Notion page the same day.
