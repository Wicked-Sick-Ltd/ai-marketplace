---
name: lesson-builder
description: >
  This skill should be used when a teacher asks to "plan a space lesson", "make a worksheet about the planets",
  "Year 5 Earth and space lesson", "KS3 gravity activity", "GCSE space physics starter", "A-level Kepler practical",
  "STEM club activity using real NASA data", or wants any classroom activity built from live PublicUniverse data for a UK key stage.
metadata:
  version: "0.4.0"
---

# Lesson builder

Create a ready-to-teach lesson or activity that uses **real values pulled live from PublicUniverse**, pitched for the right UK key stage.

## Client compatibility

Use the connected PublicUniverse MCP server (`publicuniverse`); clients may prefix or namespace its tool names. Match the tools below to the names and argument schemas actually exposed by the client. If the connection or a required tool is unavailable, explain what cannot be checked and ask the user to connect it; do not invent live results. Read references relative to this skill's directory. If browsing or file creation is unavailable, state that limit and provide the supported part of the result.

## 1. Clarify (ask only for what's missing)
- Key stage or year group: KS1, LKS2, UKS2, KS3, KS4/GCSE, KS5/A-level, or a club.
- Topic, e.g. planets and order, day and night, orbits, gravity and weight, scale, comets, asteroids, Kepler's laws, or data and statistics.
- Length (starter of 5–10 minutes, full lesson of about 50–60 minutes, or homework), plus any SEN or EAL needs.
- Output: lesson plan, worksheet, or both. Default to both.

## 2. Pull the data
Use the PublicUniverse MCP (`publicuniverse`) and never type values from memory.
- Planet facts: `get_object("<Planet>")`, which returns `physical.radius_km`, `physical.surface_gravity_m_s2`, `physical.length_of_day_hours`, `orbital.semi_major_axis_au`, `orbital.orbital_period_days`, `physical.axial_tilt_deg` and `physical.mass_kg`.
- Moons: `list_moons`. Comets: `search`, `next_perihelion`, `get_object`. Near-Earth asteroids: `find_close_approaches`. Where things are now: `compute_position` and `get_sky_position`.
- Read `references/data-caveats.md` before using gravity, day length or moon counts. These are the usual traps (e.g. the two kinds of "day" on Venus, and gravity given as GM/R²).
- Round for the age group: KS1–2 use whole numbers or "about", KS3 uses 2–3 significant figures, and KS4–5 uses standard form with units.

## 3. Build the lesson
Use `references/curriculum-map.md` to pick an accurate National Curriculum (England) link. Don't invent statutory wording or exam-board spec codes. Name the topic area only.

Structure:
1. **Title, key stage, time, learning objective** (one sentence, "Pupils will…").
2. **Starter** (5 minutes): a hook using a live fact, e.g. "Is Saturn up tonight?" or "How many Earths fit in Jupiter?".
3. **Main activity**: steps for the teacher, with the exact PublicUniverse pages to show (e.g. `https://publicuniverse.net/orrery`, `/planets`, `/objects/planet-saturn`).
4. **Worksheet**: questions graded from easier to harder, with a data table filled with the live values. For KS4–5, include one data-analysis or graph task.
5. **Answers**: worked answers calculated from the same data. Show the working for calculations.
6. **Differentiation**: support and stretch ideas.
7. **Safety** where relevant: never look at the Sun. Supervise outdoor observing.
8. **Data note**: "Data from PublicUniverse (NASA/JPL, IAU MPC), retrieved <date>."

## 4. Deliver
- Worksheets for print: A4, with page numbers, a clear title and a name/date line. Make a .docx or PDF when asked for a file. Otherwise produce a document.
- Keep KS1–2 language short and concrete. Use a friendly tone with no jargon, or explain any word you do use.
- Offer to make a matching version for another key stage.
