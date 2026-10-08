# Multi-vendor validation

Development acceptance record, updated 2026-10-05 for PublicUniverse 0.3.0. Package checks and live service checks are separate.

## PublicUniverse compatibility results (2026-10-05)

The ZIP was extracted into a temporary marketplace and installed into isolated client profiles. No model inference or user-profile configuration changes were needed.

| Client | Evidence | Remaining acceptance |
| --- | --- | --- |
| Codex CLI 0.160.0 | Native marketplace registration and plugin installation succeeded. App-server `plugin/read` reported PublicUniverse 0.3.0 installed/enabled, all seven namespaced skills, `solar-system-db`, descriptions and icon paths. | Live tool execution and conversational workflows. |
| Claude Code 2.1.273 | `claude plugin validate .` accepted the manifest. A model-free stream-JSON initialization with `--plugin-dir` discovered all seven `publicuniverse:` skill commands in an isolated profile and exited 0. | This version predates MCP-entry validation; live tools and conversational workflows remain unverified. |
| Gemini CLI 0.62.0, Node 24.21.0 | Native extension installation exited 0. Extension/skill discovery found all seven skills and the MCP server. | Live tool execution; discovery reports the inaccessible server. Node 25.6.1 hit an installer shutdown assertion after writing the installation; use the tested Node 24 runtime. |
| GitHub Copilot CLI 1.0.91 | Installed the archive with seven skills; `plugin list` and `skill list` confirmed version 0.3.0 and every workflow. | Live tools and VS Code UI acceptance. Direct installs are deprecated by this CLI; prefer the marketplace entry for distribution. |
| Cursor | Root manifests pass the official Agent Plugins 1.0.0 schemas, the format documented by Cursor for skills and MCP. | No Cursor executable available on this machine: desktop discovery and live execution remain unverified. |

Offline package validation passed for all 35 allowlisted files. The 19-test suite passed on Windows with four symlink cases skipped because this account lacks symlink privilege; Linux CI runs those security checks. Both distributable archives build. The root portable manifest carries OpenAI metadata, so a duplicate `.codex-plugin` manifest is unnecessary.

The canonical website returned HTTP 200. MCP initialization still returned HTTP 404 with `{"detail":"Not Found"}` from the existing API host; no live astronomy tool call succeeded. See [submission.md](submission.md) for rollout prerequisites and reviewer scenarios. These results establish package compatibility, not public-directory approval or full end-to-end support.

## Repeatable local checks

```sh
python3 scripts/package.py generate
python3 scripts/package.py check
python3 -m unittest discover -s tests -v
python3 scripts/package.py build
claude plugin validate .
```

The packaging tests cover generated configuration drift, skill/reference inclusion and deterministic archives. CI runs offline; it does not depend on live astronomy data or install into a user's client profile.

Verified locally on 2026-10-02:

- Both portable manifests pass the official Agent Plugins 1.0.0 JSON Schemas using `jsonschema`'s Draft 2020-12 validator. This separate schema check fetches the official schemas; the dependency-free CI checker enforces the repository's structural contract and generated-file consistency.
- Claude Code 2.1.285 accepts the compatibility manifest through `claude plugin validate .`.
- Codex CLI 0.159.3 accepts the Streamable HTTP configuration through a command-line override and `mcp get`; no saved user configuration was changed. This verifies configuration parsing, not a server connection.
- All seven skills pass the Skill Creator YAML/frontmatter validator, and the portable archives build successfully.
- An independent review checked client installation formats, archive contents, symlink handling and the distinction between package checks and live acceptance.

## Live MCP check

### 2026-10-08 (supersedes the WAF diagnosis below)

`POST https://api.sol.wickedsick.com/mcp` with a JSON-RPC `initialize` body returned HTTP 404 `{"detail":"Not Found"}` for browser, curl, AI-agent and MCP-client user agents. Response headers carried no `cf-mitigated` header and no challenge page. Cloudflare analytics for the same requests show the edge passing them to the origin (the zone's "Solar API + MCP" skip rule matched) and the origin itself answering 404. The REST API on the same host (`/healthz`, `/openapi.json`, `/api/v1/stats`, `/api/v1/objects/planet-mars`) returned 200 with live data to every user agent tested. So the MCP failure is origin routing, not the Cloudflare WAF: the `/mcp` path reaches the REST application, which has no such route. Deploying the MCP service and proxy location from `solar-system-db` (`deploy/php01/MCP-ROLLOUT.md`, merged in backend PR #47) is the remaining step.

One edge rule does affect API clients: Browser Integrity Check returns Cloudflare error 1010 (HTTP 403) to the default `Python-urllib/*` user agent on the API and website hosts. Other script user agents (`python-requests`, `Go-http-client`, `node`, `axios`, curl, MCP clients) are allowed.

### Earlier record

The existing public endpoint `https://api.sol.wickedsick.com/mcp` returned HTTP 404 with `{"detail":"Not Found"}` on 2026-10-02 at approximately 21:25 UTC. A Python MCP SDK initialization also failed with `Session terminated`. No tool invocation completed. This is an outstanding service acceptance issue, not a successful connection test.

The trailing-slash `/mcp/` also returned 404, while `/healthz` and `/openapi.json` served the REST API successfully. The backend's checked-in php01 systemd unit launches the REST API alone; its separate Docker/Caddy example routes MCP to a different service on port 8002. Those repository templates did not establish the deployed configuration or explain the public response. On 2026-10-03 the issue was attributed to Cloudflare WAF rules; the 2026-10-08 check above found the edge passing requests through and the origin answering 404, which restores the origin-routing explanation. Keep the existing documented URL until the replacement endpoint is confirmed; repeat initialization and live client acceptance after the domain/WAF work.

[Backend PR #47](https://github.com/Wicked-Sick-Ltd/solar-system-db/pull/47) includes transport metadata/security improvements and optional origin service/proxy templates. It is not a required remedy for the WAF issue. Do not install or replace a service based on the 404 alone: check the existing origin after resolving the edge configuration, and use those templates only if a remaining origin gap is established. No WAF or origin changes are part of the current plugin work.

Repeat a bounded initialization check after the endpoint has been restored:

```sh
curl --max-time 20 -i https://api.sol.wickedsick.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  --data '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"publicuniverse-check","version":"0.4.0"}}}'
```

A healthy result includes negotiated protocol/server capabilities, not just HTTP 200. Then use an MCP client to complete `notifications/initialized`, list tools and call `get_stats` and `get_object` with valid arguments. Follow the returned session/protocol headers where applicable. Check pagination and read-only annotations rather than assuming all advertised tools have the same contract.

## Client acceptance

Before announcing a tested installation for a client, record its version, plugin revision, installation route, actual discovered tools/skills and observed outcomes:

| Scenario | Expected evidence |
| --- | --- |
| Retrieve Mars | Actual catalogue call, source link, units; no fabricated value |
| Tonight from Romsey, explicit date/timezone | Skill loads its references and calls the available sky tools |
| No location supplied | Requests a location before making a local viewing claim |
| Server disconnected or tool missing | Explains the missing capability without claiming live results |
| Fact-check with browsing unavailable | Distinguishes catalogue evidence from an external claim it cannot verify |
| Unrelated coding request | Astronomy skills do not take over the task |

Native ChatGPT, Cursor and Copilot end-to-end acceptance remains pending. Package/schema validation alone is not evidence of those UI flows. No public directory submission, account connection, production deployment or client-wide configuration change is performed by the build.
