---
name: publicuniverse-data-audit
description: >
  This skill should be used when the PublicUniverse team asks to "audit the PublicUniverse data", "check the catalogue for errors",
  "run a data quality check", "why does Saturn show 316 moons", "sanity-check last night's build",
  or wants the PublicUniverse catalogue compared against official figures with fixes proposed.
metadata:
  version: "0.4.0"
---

# PublicUniverse data audit

Check PublicUniverse's catalogue for errors, drift from official sources and presentation traps. Report findings with evidence and proposed fixes.

## Client compatibility

Use the connected PublicUniverse MCP server (`publicuniverse`); clients may prefix or namespace its tool names. Match the tools below to the names and argument schemas actually exposed by the client. If the connection or a required tool is unavailable, explain what cannot be checked and ask the user to connect it; do not invent live results. Read references relative to this skill's directory. If browsing or file creation is unavailable, state that limit and provide the supported part of the result.

## 1. Build snapshot
`get_stats` and `get_sources` give the build time, row counts and source timestamps. `get_download_info` gives the artefact date, schema version and sha256. Flag a build older than 36 hours, or a schema version behind what the website expects (exoplanets need v4).

## 2. Checks (run all; see `references/audit-checklist.md` for the details and expected values)
1. **Counts**: planets 8, dwarf planets 5, Earth 1 moon, Mars 2. Compare moon counts for Jupiter, Saturn, Uranus, Neptune and Pluto with the latest IAU/MPC figures (search the web and cite the source) and with JPL's satellite table.
2. **Ghost rows**: moons (especially provisional `S/…` designations) with no orbital elements or source. List them.
3. **Planet facts**: compare radius, mass, period and semi-major axis for each planet with the NASA fact sheet values in the checklist. Flag differences over 1%.
4. **Definitions**: `surface_gravity_m_s2` is GM/R². Check the site labels it clearly, and look at rotation vs length-of-day signs and values.
5. **Positions**: `compute_position("Earth", today)` should put Earth about 0.983–1.017 AU from the Sun. Check `get_sky_position("Sun", …)` against a known sunrise time for London (within about 5 minutes).
6. **Close approaches and showers**: `find_close_approaches` for the next 7 days returns rows. `list_meteor_showers(established_only=True)` returns about 100 or more.
7. **Spot checks**: 1P/Halley's next perihelion falls in 2061. Ceres is a dwarf planet with a ≈ 2.77 AU. Pluto's parent is the Sun, with 5 moons.
8. **Public surface**: the REST `/api/v1/stats` response must not expose server paths (`db_path`) or other internal details.

## 3. Report
- A summary line such as "8 checks · 6 pass · 2 need fixing".
- A table with columns: Check · Result · Evidence (tool and value) · Severity (High = wrong public fact, Medium = misleading label, Low = cosmetic) · Proposed fix.
- For each fix, name the likely place in the code, e.g. `scripts/seed_moons.py`, `scripts/ingest_sats.py`, `scripts/verify.py`, `solar_db/data_access.py`, or the web DTO or view in `solar-system-web`. Suggest a `verify.py` check so the problem can't come back.
- Keep to what the evidence shows. Where the MCP can't answer (e.g. what the website displays), say so and suggest checking manually.
