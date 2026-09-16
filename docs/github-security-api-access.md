# GitHub Dependabot / security API access for Cloud Agents

## Problem

Listing Dependabot alerts fails with:

```text
HTTP 403 Resource not accessible by integration
X-Accepted-Github-Permissions: vulnerability_alerts=read
```

or, with a fine-grained PAT that lacks the right repo permission:

```text
HTTP 403 Resource not accessible by personal access token
```

### Why

| Credential | Behavior |
| --- | --- |
| Cursor Cloud Agent App install token (`ghs_…`) | Can push/PR on the repo, but is **not** granted `vulnerability_alerts`. Dependabot **PRs** may still be visible; the **alerts API** is not. |
| GraphQL `repository.vulnerabilityAlerts` with that token | Often returns `totalCount: 0` **without** an error — do not treat that as “no alerts”. |
| Secret named `GITHUB_PAT` | `gh` **ignores** this name and keeps using the App token unless you export `GH_TOKEN=…` yourself. |
| Fine-grained PAT without **Dependabot alerts** permission | REST Dependabot endpoints return 403 even if the user is a repo admin. |

## Fix

1. Create or edit a **fine-grained PAT** for a user who can see security alerts on this repo.
2. Repository permissions → **Dependabot alerts** → **Read-only** (use Read and write only if agents must dismiss alerts).
   - Permission API name: `vulnerability_alerts`.
   - **Not** “Dependabot secrets” (`dependabot_secrets`) and **not** “Code scanning alerts” (`security_events`) — those are different and will still 403 the Dependabot alerts API.
3. Resource owner / repository access must include `Wicked-Sick-Ltd/ai-marketplace` (or all repos).
4. Add the token to the Cloud Agent environment secrets as **`GH_TOKEN`** (preferred) or `GITHUB_TOKEN`.
5. Do **not** rely on `GITHUB_PAT` for `gh`; rename/copy the secret to `GH_TOKEN`.

Classic PATs need the `security_events` scope (or broader `repo`) instead of the fine-grained Dependabot alerts permission.

If `scripts/dependabot_alerts.py --check` still exits `3` after you add `GH_TOKEN`, the token almost always lacks **Dependabot alerts** specifically — recreate/edit the PAT and replace the secret value.

## Verify

```bash
python3 scripts/dependabot_alerts.py --check
python3 scripts/dependabot_alerts.py            # open alerts
python3 scripts/dependabot_alerts.py --state all --json
```

`--check` exits `0` when the API is reachable (including zero open alerts) and `3` on a permission 403.

## Related

- Security alerts UI: https://github.com/Wicked-Sick-Ltd/ai-marketplace/security/dependabot
- GitHub REST: [List Dependabot alerts for a repository](https://docs.github.com/en/rest/dependabot/alerts#list-dependabot-alerts-for-a-repository)
