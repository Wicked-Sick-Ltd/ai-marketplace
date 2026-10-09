---
name: tonight-sky
description: >
  This skill should be used when the user asks "what can I see tonight", "is Saturn up tonight",
  "which planets are visible", "when does Jupiter rise", "stargazing plan for this weekend",
  "where do I look for Mars", or wants a viewing plan for a place and date using live PublicUniverse data.
metadata:
  version: "0.4.0"
---

# Tonight's sky

Build a clear, practical viewing plan for a specific place and evening, using the PublicUniverse MCP (`publicuniverse`) tools.

## Client compatibility

Use the connected PublicUniverse MCP server (`publicuniverse`); clients may prefix or namespace its tool names. Match the tools below to the names and argument schemas actually exposed by the client. If the connection or a required tool is unavailable, explain what cannot be checked and ask the user to connect it; do not invent live results. Read references relative to this skill's directory. If browsing or file creation is unavailable, state that limit and provide the supported part of the result.

## 1. Pin down place and time
- **Location**: accept a town, postcode, coordinates or a what3words address. The MCP needs `lat`/`lon`, so convert a town or postcode to approximate coordinates (2 decimal places is plenty). If the user gives a what3words address, point them to publicuniverse.net (it converts what3words on the object pages) or ask for a nearby town. Never guess a location. Ask if none is given.
- **Date**: default to tonight. Use the user's local timezone. For the UK, BST is UTC+1 from the last Sunday in March to the last Sunday in October.
- **Viewing window**: default to one hour after local sunset. Find sunset with `get_sky_position("Sun", date, lat, lon)`, which gives the `set_utc` field. Also check around 22:00 local, and before dawn if the user is an early riser.

## 2. Query the planets
Call `get_sky_position` for Mercury, Venus, Mars, Jupiter, Saturn, Uranus and Neptune at the chosen time (ISO datetime in UTC). For each one, record:
- `observer.is_up`, `observer.is_dark`, `altitude_deg`, `azimuth_deg`
- `rise_utc`, `transit_utc`, `set_utc`, `constellation.name`, `elongation_deg`

Classify each planet:
- **Good**: up, dark, and altitude of 15° or more
- **Low**: up but below 15°
- **Morning only**: rises after midnight and is up before dawn
- **Not visible**: elongation below about 15° (lost in the Sun's glare), or below the horizon all night

Mention that Uranus needs binoculars and Neptune needs a telescope.

## 3. Optional extras
- **Meteor showers**: `list_meteor_showers(established_only=True, active_on=<date>)`. Mention only well-known, established showers, and say activity windows are approximate.
- **Bright comet or asteroid**: only if the user asks. Use `search` and then `get_sky_position`.
- **Weather**: the MCP has no weather data. Point to the cloud outlook on the object page at publicuniverse.net, or suggest the user checks a forecast.

## 4. Output format
Lead with a one-line verdict, e.g. "Two planets are easy tonight: Saturn and Jupiter." Then give a compact table in local time:

| Planet | Best time | Look | Height | Notes |
|---|---|---|---|---|
| Saturn | 21:00–03:00 | South-east → south | 20–40° | Steady, creamy "star" in Cetus |

- Convert azimuth to compass words (N, NE, E, SE, S, SW, W, NW). Convert altitude to fists at arm's length (one fist is about 10°).
- End with a link to each planet's page, such as `https://publicuniverse.net/objects/planet-saturn`, so the user can check the live panel and the cloud outlook.
- For children, use simple words, one "wow" fact per planet, and a reminder to go out with a grown-up.
- Always include: **never look at the Sun**, even with sunglasses, binoculars or a telescope.

## Accuracy
Positions come from a two-body model and are good to about a degree, so round times to 5–10 minutes. See `references/data-caveats.md` for UTC handling and other caveats.
