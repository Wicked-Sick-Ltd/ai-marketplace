---
name: amiga-adf-decompile
description: Exhaustively extract, unpack, reverse engineer, and validate Amiga ADF disk images with byte provenance and explicit semantic coverage. Use for disk preservation, game decompilation, and faithful remake research.
---

# Amiga disk decompilation

Aim to decode to exhaustion. A successful file extraction, attractive asset preview,
or large automatic decompilation is a milestone, never the completion criterion.
Read [the process](references/process.md) before a new investigation. Keep the
original disks immutable and work in the user's chosen project.

Maintain three separate coverage ledgers: physical disk bytes, recursively decoded
content, and understood behavior. Every unknown gets a concrete next experiment;
every claimed result gets an evidence pointer and its validation limits. Continue
with available experiments rather than stopping at the first successful layer.

Treat earlier projects as method examples, not address/format authorities for a
different game. Prefer actual loader and consumer instructions over filenames,
signature guesses, plausible loop bounds, and unreviewed decompiler output.

Preserve differing releases and overlapping runtime images separately. Record
corrections explicitly; duplicated notes do not constitute independent evidence.
Never fill missing original bytes with invented or unrelated replacement data.
