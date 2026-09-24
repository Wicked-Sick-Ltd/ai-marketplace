# Local AI repository migration — broadcast prompt

Verified 24 September 2026: all three GitHub renames preserve their original
repository IDs and private visibility. This prompt authorises per-machine
remotes and eligible folder moves; it is not a fleet deployment or central
inventory apply. Copy the block below to the agents you want to handle each machine.

The plugin version correction is [Claude PR #38](https://github.com/Wicked-Sick-Ltd/ai-claude-repo/pull/38).
Remote/folder work can proceed while it is reviewed; the affected cached plugin
updates wait for that release to land.

```text
Update this machine for the completed Wicked-Sick-Ltd AI repository renames:

- codex-repo -> ai-codex-repo (GitHub repository ID 1373289160)
- cursor-repo -> ai-cursor-repo (GitHub repository ID 1379739987)
- claude-repo -> ai-claude-repo (GitHub repository ID 1263939071)

The repositories remain private. ai-marketplace is unchanged. The new ai-gemini-repo, ai-copilot-repo and ai-grok-repo already exist; clone them only if this machine needs them. Grok templates are now in ai-grok-repo, but originals remain in Cursor pending a separate removal.

You are authorised to update this machine's matching remotes, idle local checkout folder names and their local references. Proceed with safe work; report deferred items individually.

1. Discover the actual local checkout locations and verify their GitHub identity; do not assume a fixed root, OS or clone path. Read each repo's agent/coordination instructions. Record branch, HEAD, dirty/untracked state, remotes (including explicit push URLs), worktrees and dependent hooks, IDE workspaces, scheduled tasks or services. Preserve credentials and redact any credential-bearing URL from reports.

2. Update matching fetch/push remote URLs to the new repository names, preserving SSH versus HTTPS and unrelated fork remotes. Fetch and verify access. Do not reset, clean, auto-stash, discard changes or switch branches. Only fast-forward an idle, clean local default branch if it has not diverged; report all other branch states.

3. Rename idle, non-serving main checkout folders to ai-codex-repo, ai-cursor-repo and ai-claude-repo. Work from outside the folder being moved. Never overwrite an existing destination, move an active agent's checkout, or relocate a running hub/sidecar/service checkout. Update remotes there and defer the folder move with its dependency. Preserve dirty work and linked worktrees; if their safety cannot be established, defer the move. After a main checkout move, run git worktree repair from the new main location and validate every linked worktree. Use git worktree move for eligible linked worktrees; do not blindly move worktrees containing submodules or edit .git files.

4. Update references that actually point to moved folders: local scripts, hooks, IDE workspaces and environment configuration. Do not replace every old-name string. Preserve Codex's codex-repo:begin/end markers, codex-repo-manifest.json, codex-repo-backups, presence-hook managed markers and ownership hashes. Preserve marketplace IDs wicked-sick, wickedsick and wicked-sick-codex; keep plugin names and reviewed third-party pins. Keep historical records intact. Stage tracked/shared changes in a branch/PR.

5. Inspect existing Claude marketplace/plugin registrations. Use the installed CLI's supported workflow to update the wicked-sick source to Wicked-Sick-Ltd/ai-claude-repo while preserving scope and installed choices. Do not blindly remove/re-add marketplaces, edit generated caches or install duplicate plugins. Wait for https://github.com/Wicked-Sick-Ltd/ai-claude-repo/pull/38 to merge before expecting the rename patch releases. Then refresh wicked-sick and update only affected plugins already installed in their existing scope: onboarding 0.1.4, pr-flow 0.1.2, wizzo-twin 0.3.1, session-lifecycle 0.1.1, estate-maintenance 0.1.1 and wizzo-fleet-presence 0.1.1, or later releases. Retain the separate wickedsick catalog's reviewed pins. Verify installed versions and use a fresh Claude session to load updates; do not interrupt another active session.

6. Keep Acsendr's configured policy-checkout path valid. Do not move deployment folders, restart services, change fleet auto-reconcile, merge PRs or edit the central Notion inventory as part of this local task. Route required operational changes through the owning runbook; report dependencies while completing independent local work.

7. Verify remote access, git status, worktree connectivity, local links/hook paths and applicable repository validators. Confirm the migration preserved pre-existing work. Report hostname, repo, old/new local path, remote, branch/HEAD, installed plugin versions, checks and any deferred service/worktree dependencies. Save a secret-free per-machine handoff record; do not report completion for an untested plugin or a deferred move.
```

## Operator notes

- Use one agent per machine/checkout, respecting existing coordination leases.
- Keep central inventory reconciliation in a single controlled run with a reviewed dry-run; a GitHub rename does not finish that step.
- The prompt does not authorise deleting the duplicate Grok source in Cursor, changing trust/credentials, or repinning the public catalog.
- [Git worktree repair](https://git-scm.com/docs/git-worktree) reconnects linked worktrees after a main checkout moves; worktree move has restrictions for main worktrees and submodules.
- [Claude version management](https://code.claude.com/docs/en/plugins-reference#version-management) explains why explicit patch releases are required for versioned cached plugins.
- [Canonical migration record](https://app.notion.com/p/3e44ce0f445181bb8c7dc1ac5eb6ac22).
