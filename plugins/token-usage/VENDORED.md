# Vendored copy: token-usage plugin

Cursor team marketplaces resolve plugin sources as directories inside this catalogue repository, so this directory holds a copy of the token-usage Cursor plugin package.

- Upstream: https://github.com/Wicked-Sick-Ltd/token-usage
- Version in the manifests at this commit: 0.9.0
- Source commit: `39cbb737084bf4f8aaa0c17b8cd1c560f6a0a47c` (2026-10-21, #27). The v0.9.0 tag is the earlier `fe998547b0dfa9472e2a80cb9beee9bae3018575` (2026-10-18, #26). #27 adds the Antigravity plugin bundle and multi-runtime report skill. This copy reads an explicit Cursor Cloud Agent export `.json`. It has no `cursor-cloud` runtime and does not call the Cursor Admin API.
- Upstream `main` on 2026-11-14: `7638fb1b07751f1bfd2d4d6cc535aad71280f905` (2026-11-13, #34). That unreleased commit adds `cursor-cloud` (`CURSOR_ADMIN_API_KEY`, `cursor-cloud-sync`). Commits after this pin also add an opt-in activity-stream bridge. This directory was not re-vendored to `main`.
- Contents: `.cursor-plugin/`, `skills/report/`, `hooks/hooks-cursor.json`, `scripts/`, `data/pricing.json`, `assets/logo.svg`, `LICENSE`, and `NOTICE` — the files required for the Cursor plugin runtime at that commit. `README.md` in this directory is a catalogue note, not a file from the upstream commit.

Do not edit these files here. To update: check out the reviewed upstream commit, replace this directory's contents (except this file), and update the commit above.
