# Audit checklist: expected values

## Reference planet values (NASA Planetary Fact Sheet)
| Planet | Mean radius km | Mass kg | a (AU) | Period (days) |
|---|---|---|---|---|
| Mercury | 2,439.7 | 3.30e23 | 0.387 | 87.97 |
| Venus | 6,051.8 | 4.87e24 | 0.723 | 224.70 |
| Earth | 6,371.0 | 5.97e24 | 1.000 | 365.26 |
| Mars | 3,389.5 | 6.42e23 | 1.524 | 686.98 |
| Jupiter | 69,911 | 1.898e27 | 5.203 | 4,332.6 |
| Saturn | 58,232 | 5.68e26 | 9.537 | 10,759 |
| Uranus | 25,362 | 8.68e25 | 19.19 | 30,689 |
| Neptune | 24,622 | 1.02e26 | 30.07 | 60,182 |

NASA's quoted equatorial surface gravity (m/s², at 1 bar for the giants): Mercury 3.7, Venus 8.87, Earth 9.80, Mars 3.71, Jupiter 24.79, Saturn 10.44, Uranus 8.87, Neptune 11.15. PublicUniverse's GM/R² values are higher for the giants. That is expected, but it must be labelled.

## Moon counts: last known reference points
- IAU MPC announcement, 16–26 March 2026: **Saturn 285**, **Jupiter 101** confirmed.
- JPL satellite elements table, Sept 2026: Saturn 291, Jupiter 115, Uranus 30 rows (Puck is listed twice, so 29 unique), Neptune 16, Pluto 5, Mars 2, Earth 1.
- Always re-check the web for newer announcements before reporting.

## Known issue history
- **Sept 2026, ghost moons.** `scripts/seed_moons.py` auto-generated 73 Saturn provisional designations "to round out the count". 25 of them didn't exist in JPL's table, which added 25 empty moons to Saturn (316 shown). S/2003 J 5 was also a ghost for Jupiter (116 shown). Fix: stop generating designations, and add a `verify.py` warning for provisional moons without orbital elements.
- **Sept 2026, path leak.** `/api/v1/stats` returned `db_path` (the server's home directory). Fix: remove the field and add tests.
- **Sept 2026, deploy lag.** The live API ran an old checkout without the meteor-shower and exoplanet endpoints, while the website's navigation already linked to Exoplanets.

## Useful queries
- Ghosts: `list_moons(planet)`, then filter rows where `orbital_period_days` is null and the name starts with `S/`.
- Build freshness: `get_stats` → `last_build.finished_at`.
- Schema version: `get_download_info` → `schema_version`.
