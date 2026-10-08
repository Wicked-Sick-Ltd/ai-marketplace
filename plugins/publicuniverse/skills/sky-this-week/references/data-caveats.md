# PublicUniverse data caveats

Known ways PublicUniverse's numbers can legitimately differ from textbooks, NASA pages or news stories. Check this list before calling a mismatch an error.

## Moon counts
- PublicUniverse lists every satellite in JPL's satellite elements table. That table is **more inclusive** than the IAU/MPC "confirmed" tally. In March 2026 the MPC total was Saturn 285 and Jupiter 101, while JPL listed about 291 and 115.
- Builds before the Sept 2026 seed fix also contained 26 "ghost" provisional moons with no orbital elements: 25 for Saturn (S/2004 S 1–23, S/2006 S 2–8, S/2007 S 1, and similar) and S/2003 J 5 for Jupiter. That pushed Saturn to 316 and Jupiter to 116. If `list_moons` returns provisional moons with a null period, count them separately.
- In classroom materials, say "more than 280 moons" for Saturn and "about 100" for Jupiter, or give PublicUniverse's number with a note. New moons are announced regularly.

## Gravity
- `surface_gravity_m_s2` is **GM/R²** using the mean radius, and it ignores rotation. For the gas giants this is higher than NASA's quoted "surface gravity" at the 1-bar equator: Jupiter 25.9 vs 24.8, and Saturn 11.2 vs 10.4. Earth 9.82 vs 9.80 is negligible.

## Length of day
- `rotation_period_hours` is the **sidereal** rotation. A negative value means retrograde spin (Venus, Uranus, Pluto).
- `length_of_day_hours` is the **solar day**, i.e. sunrise to sunrise.
- Venus: rotation 243 Earth days is *longer* than its 224.7-day year, but its solar day of about 117 days is *shorter*. Always say which one a fact means.

## Positions and sky
- Positions use **two-body Keplerian propagation**, accurate to about 1° for the planets. That's enough to name the constellation and say whether something is up, but not for telescope pointing, occultations or precise timings.
- All times from the tools are **UTC**. Convert to the user's local time (UK: BST = UTC+1 from the last Sunday in March to the last Sunday in October, otherwise GMT = UTC).
- `get_sky_position` for a moon returns its parent planet's position (`resolved_from`).
- The tool doesn't model the Moon's phase or atmospheric refraction. Rise and set times can be a few minutes out.

## Sizes of small bodies
- Most asteroids have no measured radius. Estimate diameter from absolute magnitude H with D(km) = 1329 / √p × 10^(−H/5), using albedo p = 0.14 unless it's known. Give a range for p = 0.05–0.25 and say it's an estimate.

## Counts that change nightly
- Object totals such as asteroids (about 1.56 m) and comets (about 4,077) grow with each nightly build. Quote them as "more than 1.5 million" and similar, not exact figures, in anything that will be printed.

## Not astrology
- PublicUniverse is an astronomy catalogue. Never frame outputs in zodiac or horoscope terms. Constellations are IAU boundary regions only.
