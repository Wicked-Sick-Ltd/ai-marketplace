# pr-flow

Skills and a Bash helper for opening a pull request, waiting until CI and
reviewer bots finish, answering every finding, and landing the change.

Canonical source: [`plugins/pr-flow`](https://github.com/Wicked-Sick-Ltd/ai-grok-repo/tree/main/plugins/pr-flow)
in `Wicked-Sick-Ltd/ai-grok-repo`. This directory is the catalogue copy.
See [VENDORED.md](VENDORED.md) for the upstream commit.

## Install

From the Wicked Sick marketplace (`Wicked-Sick-Ltd/ai-marketplace`):

```sh
# Claude Code (Grok Build reads this marketplace too)
claude plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
claude plugin install pr-flow@wickedsick

# Cursor
# Import Wicked-Sick-Ltd/ai-marketplace as a Team Marketplace, then install pr-flow.

# Codex
codex plugin marketplace add Wicked-Sick-Ltd/ai-marketplace --sparse .agents/plugins
codex plugin add pr-flow@wickedsick

# GitHub Copilot CLI
copilot plugin marketplace add Wicked-Sick-Ltd/ai-marketplace
copilot plugin install pr-flow@wickedsick
```

Choose one marketplace per plugin to avoid duplicate skills. Start a new
session after installation.

Two skills and the Bash helper implement the PR lifecycle:

- [pr](skills/pr/SKILL.md): `create|watch|merge|land|status|sweep` with an
  optional PR number/URL and `--repo owner/name`.
- [landing-prs](skills/landing-prs/SKILL.md): policy for plain-language requests
  to open, monitor, review or land a change.
- [pr-wait.sh](skills/landing-prs/pr-wait.sh): wait for registered check runs
  and commit statuses, then print checks, reviews, unresolved threads and
  comments in a digest. One GraphQL query per poll, default every 90 seconds
  (minimum 60). Sleeps until the GraphQL rate-limit reset when fewer than 500
  points remain.

`watch` stops after triage; `land` includes merging when authorized. Preserve
repository branch rules and the Critical/sensitive-work draft requirement.
The helper's zero exit code means checks passed: callers must also inspect
`unresolved_threads` in its SUMMARY before merging. The same line reports
`mergeable` and `merge_state` from that poll.

Review comments from Claude, Bugbot, Copilot, CodeQL and Semgrep are in scope.
Every finding is fixed or answered, and every thread is resolved, before the
PR counts as done.

## Dependencies

Requires authenticated `gh`, Bash and `jq`. On Windows use Git Bash or WSL with
those tools available in that shell. Resolve the helper from the installed skill
folder; the interactive shell need not have `PLUGIN_ROOT` set.
