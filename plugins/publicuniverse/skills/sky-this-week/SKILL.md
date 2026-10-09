---
name: sky-this-week
description: >
  This skill should be used when the user asks to "write this week's sky roundup", "draft a PublicUniverse blog post",
  "social posts about what's up this month", "newsletter for PublicUniverse subscribers", "SEO content for publicuniverse.net",
  or wants publishable astronomy content built from live PublicUniverse data that links back to PublicUniverse pages.
metadata:
  version: "0.4.0"
---

# Sky this week: content for PublicUniverse

Produce accurate, publishable content (blog post, newsletter, or social posts) that drives people to publicuniverse.net.

## Client compatibility

Use the connected PublicUniverse MCP server (`publicuniverse`); clients may prefix or namespace its tool names. Match the tools below to the names and argument schemas actually exposed by the client. If the connection or a required tool is unavailable, explain what cannot be checked and ask the user to connect it; do not invent live results. Read references relative to this skill's directory. If browsing or file creation is unavailable, state that limit and provide the supported part of the result.

## 1. Brief
Confirm the following, and use the defaults if the user doesn't say:
- **Period**: the next 7 days
- **Location**: UK (London 51.51, −0.13 as the reference)
- **Audience**: families and beginners
- **Format**: blog post and 3 social posts
- **Length**: blog about 500–700 words, newsletter about 250, social under 280 characters each

## 2. Gather live data (PublicUniverse MCP `publicuniverse`)
- Planets: `get_sky_position` for each planet at 21:00 local on the first evening, plus a pre-dawn check. Note oppositions (elongation near 180°), and planets too close to the Sun (elongation under about 15°).
- Meteor showers: `list_meteor_showers(established_only=True, active_on=<each date>)`.
- Flybys: `find_close_approaches` for the period (max_dist_au 0.05). Pick the one or two most notable.
- One "object of the week" from `search` or `get_object` (a comet at perihelion, a named asteroid, a moon), with a hook.
- Read `references/data-caveats.md`. Never publish exact counts that change nightly.

## 3. Write
- **Headline** with the main hook and the period (e.g. "Saturn at its best: the sky this week, 5–11 October").
- **Blog structure**: short intro, "Planets this week" (each with where, when and what it looks like), "Also up", "Object of the week", "How to use PublicUniverse", and a sign-off.
- **Links**: link every object named to its PublicUniverse page `https://publicuniverse.net/objects/<id>`. Link `/orrery` once and `/planets` once. Use descriptive anchor text ("Saturn's live position"), never "click here".
- **SEO**: give a title tag (≤60 characters), meta description (≤155 characters), a URL slug, and 3–5 natural target phrases (e.g. "what planets can I see tonight UK"). Don't stuff keywords.
- **Social posts**: one hook each, one link, and at most 2 hashtags. For UK timing, say BST or GMT.
- **Tone**: warm, curious and accurate, in UK English. Always include the Sun-safety line in anything about daytime or telescope viewing.

## 4. Check before handing over
Run each factual sentence against the data you gathered. If any claim isn't backed by a tool result, remove it or rewrite it. Finish with a list of the claims and the tool calls behind them, so the user can review quickly.
