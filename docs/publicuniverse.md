# PublicUniverse rollout

> **2026-10-08 update (0.4.0):** source repository renamed to `Wicked-Sick-Ltd/publicuniverse-plugin` (pending), MCP server id is now `publicuniverse`, and Cursor is listed through the vendored copy at `plugins/publicuniverse/`. Entries are pinned to the 0.4.0 PR head and must be re-pinned to the merged commit. The live MCP 404 is an origin routing gap (Cloudflare passes the request), not the WAF.

Package: `publicuniverse` 0.3.0. Replaces the old `solar` listing. Website: https://publicuniverse.net.

The catalog changes are a release preparation, not a live-service acceptance claim. Keep the PR in draft until the repository transfer, visibility and service gates below are resolved.

## Catalogs and evidence

| Host | Distribution | Verification on 2026-10-05 |
| --- | --- | --- |
| Codex | `.agents/plugins/marketplace.json`, SHA-pinned portable package | CLI 0.160.0 installed the archive; app-server discovered all seven skills, MCP configuration and listing metadata. |
| Claude | `.claude-plugin/marketplace.json`, replaces `solar` | CLI 2.1.273 installed the pinned HTTPS source from the catalog and listed it enabled; model-free initialization discovered all seven namespaced skills. Live tool acceptance remains pending. |
| Copilot | `.github/plugin/marketplace.json`, SHA-pinned portable package | CLI 1.0.91 installed/listed PublicUniverse from the Git-hosted catalog branch and discovered seven skills. VS Code acceptance remains pending. |
| Gemini | [Pinned extension command](../gemini/README.md#publicuniverse-rollout-pending) | CLI 0.62.0 on Node 24.21.0 installed and discovered all seven skills and the MCP configuration. |
| Cursor | Import the final plugin repository directly, or install its portable package locally | Agent Plugins 1.0.0 schema checks passed; desktop acceptance remains pending. No remote-source entry is added to this repository's path-only Cursor index. |

The source package includes complete installation guides, an allowlisted ZIP/`.plugin`, regression tests, icons and submission scenarios. See its [validation record](https://github.com/Wicked-Sick-Ltd/solar-plugin/blob/8647a5e6e8a78f8426b03280b268370223a7599c/docs/validation.md) and [submission checklist](https://github.com/Wicked-Sick-Ltd/solar-plugin/blob/8647a5e6e8a78f8426b03280b268370223a7599c/docs/submission.md). These links require organisation access until the repository becomes public.

Use the explicit HTTPS source for Claude: its GitHub shorthand attempted SSH on the test machine and failed host-key verification. No SSH trust settings were changed. Copilot's local-directory marketplace mode pruned its downloaded plugin on the next command; importing `https://github.com/Wicked-Sick-Ltd/ai-marketplace.git#feat/publicuniverse` into an isolated profile exercised the intended Git-hosted route successfully. Use the default branch after rollout.

## Release gates

1. Confirm the exact repository name in `public-universe`. Transfer first, then make public, following Craig's requested sequence.
2. Update plugin metadata, these three catalog source URLs and the Gemini command to the confirmed destination; pin the final reviewed package commit. Verify anonymous Git access before public rollout.
3. Restore MCP initialization and tool calls at the confirmed production URL. The existing `https://api.sol.wickedsick.com/mcp` returned 404 on 2026-10-05; the website itself returned 200. DNS/WAF/origin work belongs to the service rollout.
4. Complete outstanding client acceptance, CI and reviews. Official vendor-directory submissions have separate review/identity/policy requirements; this GitHub catalog does not confer approval.

After rollout, install with:

```sh
codex plugin add publicuniverse@wickedsick
claude plugin install publicuniverse@wickedsick
copilot plugin install publicuniverse@wickedsick
```

Register `Wicked-Sick-Ltd/ai-marketplace` with each client first. Existing `solar` users should disable/remove that package before enabling `publicuniverse`; the MCP identifier remains `solar-system-db`, and the renamed audit skill is `publicuniverse-data-audit`.
