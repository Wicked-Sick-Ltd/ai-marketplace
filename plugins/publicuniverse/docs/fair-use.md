# Fair use

Public Universe (https://publicuniverse.net) is free for everyone. This
plugin repository does not serve the website or the REST API.

| Surface | Repository |
| --- | --- |
| Public site, `/fair-use`, `/api-access`, footer, `robots.txt` | [Wicked-Sick-Ltd/solar-system-web](https://github.com/Wicked-Sick-Ltd/solar-system-web) |
| REST API key tiers | [Wicked-Sick-Ltd/solar-system-db](https://github.com/Wicked-Sick-Ltd/solar-system-db) (`api/fair_use.py`) |
| This plugin | MCP client package. Interactive use does not need a key. |

Cloudflare applies its own edge limits. It exempts any request that carries
the `X-PU-Api-Key` header from a stricter anonymous rule, whether or not the
value is a real key. Cloudflare Pro still caps all traffic, keyed or not, at
300 requests per minute per IP. The access form can store egress CIDR ranges
so operators can allowlist a high-volume institution. The API
therefore treats a missing, blank, unknown, or revoked key exactly like
anonymous traffic: the per-IP anonymous limit, HTTP 429, and
`X-PU-Key-Tier: anonymous`. Unknown and revoked keys are also rate-limited
per IP. Valid keys are counted on their own budget and send
`X-PU-Key-Tier: free` or `X-PU-Key-Tier: institution`.

Anonymous defaults are 60 requests per minute and 1,000 per day per IP. A
free key is higher. An institution key defaults to 100,000 calls per day
(`PU_INSTITUTION_PER_DAY` on the API host), pending a final decision. A 429
includes `Retry-After` and a link to https://publicuniverse.net/api-access.

Keys are stored as hashes. Do not commit secrets.

## API host environment

Set these on the API deploy (`solar-system-db`). Unset `PU_API_KEYS` is a no-op.

| Variable | Purpose |
| --- | --- |
| `PU_API_KEYS_PATH` | SQLite file of key hashes and counters. |
| `PU_API_KEY_PEPPER` | Extra hash input. Changing it invalidates existing keys. |
| `PU_INSTITUTION_PER_DAY` | Institution ceiling. Default `100000`. |
| `PU_API_ACCESS_URL` | Link in HTTP 429. Default `https://publicuniverse.net/api-access`. |
| `PU_ANON_PER_MINUTE`, `PU_ANON_PER_DAY` | Anonymous per-IP budget. Defaults 60 and 1000. |
| `PU_FREE_PER_MINUTE`, `PU_FREE_PER_DAY` | Free-key budget. Defaults 300 and 10000. |
| `PU_INSTITUTION_PER_MINUTE` | Institution burst. Default 5000. |
| `PU_INVALID_KEY_PER_MINUTE` | Per-IP cap on unknown or revoked keys. Default 30. |
| `PU_TRUSTED_PROXIES` | Extra proxies allowed to supply a client IP. Loopback is always trusted. |
| `PU_API_KEYS` | Optional JSON bootstrap. Leave unset. |

## Site environment

Set these on the website deploy (`solar-system-web`). Each unset value is a no-op.

| Variable | Purpose |
| --- | --- |
| `PU_SITES_SLACK_WEBHOOK_URL` | Slack incoming webhook for `#sites-publicuniverse`. |
| `PU_ASANA_ACCESS_TOKEN` | Asana token. No task is created without it. |
| `PU_ASANA_PROJECT_ID` | Asana project. Use `1220017034322863`. |

The MCP server in `solar-system-db` is not on these key tiers. It remains the
unauthenticated endpoint this plugin connects to.
