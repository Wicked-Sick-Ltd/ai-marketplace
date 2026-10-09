---
name: space-fact-check
description: >
  This skill should be used when the user asks to "fact-check this", "check these space facts",
  "is this right about Saturn's moons", "verify the numbers in my worksheet/brochure/post",
  "check what the AI said about the planets", or pastes astronomy claims to verify against live PublicUniverse data.
metadata:
  version: "0.4.0"
---

# Space fact-check

Verify astronomy claims against PublicUniverse's live catalogue, and explain any legitimate reasons a number might differ.

## Client compatibility

Use the connected PublicUniverse MCP server (`publicuniverse`); clients may prefix or namespace its tool names. Match the tools below to the names and argument schemas actually exposed by the client. If the connection or a required tool is unavailable, explain what cannot be checked and ask the user to connect it; do not invent live results. Read references relative to this skill's directory. If browsing or file creation is unavailable, state that limit and provide the supported part of the result.

## Steps
1. **Extract claims.** List every checkable claim from the text or file: numbers, comparisons, dates, "biggest/fastest/only" statements and positions ("Saturn is up all night in October").
2. **Read `references/data-caveats.md`** before judging anything. It covers moon counts, gravity, Venus's two kinds of day, the accuracy of positions, and counts that change nightly.
3. **Check each claim with the PublicUniverse MCP** (`publicuniverse`):
   - Physical and orbital facts: `get_object`
   - Moon counts: `list_moons` (count separately any provisional moons with a null period)
   - Comet returns: `next_perihelion` (convert JD to a calendar date)
   - Visibility and positions: `get_sky_position` (with lat/lon for a location) or `compute_position`
   - Catalogue totals: `get_stats`
   - Discovery facts: `get_discovery`
   - Close approaches: `get_close_approaches` or `find_close_approaches`
   Do the arithmetic yourself for derived claims, e.g. "1,300 Earths fit in Jupiter" is (R_J/R_E)³.
4. **Cross-check external sources when PublicUniverse isn't the authority.** For recently announced moons or official IAU counts, search the web (IAU, MPC, NASA) and cite the source.

## Verdicts
Give each claim one verdict:
- ✅ **Correct**, with PublicUniverse's value
- ⚠️ **Needs wording**: true only under one definition, or it will go out of date (suggest safer wording)
- ❌ **Wrong**: give the correct value and its source
- ❓ **Can't check with PublicUniverse**: say what would be needed

## Output
A table with columns: Claim · Verdict · PublicUniverse says · Suggested wording. Put the ❌ and ⚠️ items at the top. For anything that will be printed (brochures, worksheets), prefer wording that won't go out of date ("more than 280 moons", "over 1.5 million asteroids").

If the check shows a problem in PublicUniverse's own data (not just a definition difference), say so clearly and suggest running the `publicuniverse-data-audit` skill.
