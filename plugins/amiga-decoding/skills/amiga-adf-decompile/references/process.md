# Process and exhaustion criteria

## 1. Establish identity and prior evidence

Inventory every supplied disk, including byte length, SHA-256, signatures, release
labels, and duplicate identities. Record tool versions and scripts' hashes. Search
relevant existing projects and follow project-directory symlinks deliberately;
exclude AppleDouble `._` companions from disk inputs. Read corrections and later
handoffs as well as summaries. Distinguish local findings revalidated now from
historical claims. Keep a source inventory with paths and hashes.

Use half-open byte ranges. Label each address explicitly: disk offset, extracted
file offset, hunk-relative offset, analysis address, runtime address, or device
register. Supply the transformations between them; an assigned analysis base is
not evidence of original placement.

## 2. Recover the entire physical disk

Classify standard OFS/FFS, extended ADF, and custom track layouts from bytes.
For standard filesystems validate boot/root metadata, metadata checksums, parent
links, name safety, hash chains, extension tables, data ownership/sequence,
payload sizes, next links, bitmap allocation, and global crosslinks. A data-only
disk may have no boot root pointer; validate the conventional root separately.
Unsupported types and corrupt entries become explicit recovery work, not silent
omissions. A checksum can remain valid when an entire wrong sector was copied.

Account for every sector and every file tail: boot, metadata, live payload,
slack, free zero space, free nonzero remnants, orphan allocations, custom data,
and unresolved regions. Preserve raw anomalous sectors. Scan unused regions for
deleted headers, signatures, repeated tracks and displaced owner/sequence pairs.
Map extracted byte ranges back to their individual physical fragments. Do not
assume a file is contiguous on disk. Compare a second filesystem reader when
available and report its actual scope and failures.

For custom disks trace boot/track reads into RAM and recover every loaded range.
WHDLoad slaves can suggest layout and version-specific patches, but verify them
against the supplied release and original instructions. A normal ADF lacks raw
flux/protection details; do not manufacture those details.

## 3. Trace loading and recursively unpack

Read boot code, startup scripts and every chained loader. Resolve disk swaps,
memory allocation, relocation, supervisor transitions, overlays, callbacks and
interrupt vectors. Preserve separate runtime epochs when addresses are reused.
Separate original game code, OS utilities, crack additions and damaged candidates
only when their provenance/control flow supports the distinction.

Derive custom codecs from producer/consumer instructions. Preserve integer widths,
carry/extend flags, DBF's count-plus-one behavior, byte order, backward streams,
overlapping copies and escape cases. Record exact input consumption, output size,
trailing bytes and reads outside the recovered source. Enforce bounds in portable
decoders; unexplained tails remain evidence, not padding by default. Unpack nested
and individually compressed records as well as whole files.

Run the original codec instructions independently where possible and compare every
output byte against the portable decoder. A plausible output length or magic
signature is structural evidence, not an independent proof. Preserve input memory
before emulation: emulator backing arrays may mutate.

## 4. Map code and data

Import executable hunks with relocation tables or raw code with loader-established
bases. Use Ghidra (or equivalent) listings, cross-references and per-function
exports. Seed dynamic targets from actual jump/callback tables, exception setup,
and interrupt registration. Do not linear-disassemble all data and count the
result as code. Track unreachable candidates and invalid/later-CPU instructions.

For each interpreted table/routine record its producers, consumers, accessed
state, native arithmetic, call order and confidence. Names and familiar shapes
are search anchors only: Deuteros audio and mining were both mistaken for combat.
Function boundaries and pseudo-C are hypotheses until checked against assembly.

## 5. Recover all content families

Cover maps, scenarios, unit/terrain tables, strings and font encodings, sprites,
palettes, masks, planar layout, raster/copper changes, animation commands/deltas,
samples, music sequences and drivers. Decode every record in each family. Keep
native bytes, structured data, rendered previews and provenance together. Document
which palette, stride, transparency, sample rate and timing are established versus
assumed. Parse concatenated containers and unused/alternate assets too.

Cover mutable state, initialization, input, UI transitions, simulation cadence,
economy, movement, AI, combat, RNG, saves, endings, errors and restart paths.
Correlate saves and runtime snapshots with actual reads/writes. Preserve signedness,
overflow, rounding, update order and source bugs. Avoid implementing a remake as
a substitute for finishing the requested investigation.

## 6. Validate progressively

Use independently implemented readers, original-instruction execution, native
emulator captures, save round trips, framebuffer equality, register-write traces
and audio PCM comparisons as appropriate. A round trip alone can preserve a shared
mistake. Cover boundaries, alternate branches, all table IDs, RNG progression and
multiple uninterrupted transitions. Synthetic states test semantics but do not
establish gameplay reachability. Bounded CPU fixtures do not prove cycle-accurate
hardware or whole-game equivalence.

Check tool limitations before blaming the original: past Ghidra harnesses exposed
MOVEM.W, DIVU overflow, indexed jumps, RTE and supervisor-stack limitations.
Record any shim, stub, seeded memory, device assumption or omitted interrupt.
Use an independent native CPU implementation to adjudicate disagreements.

## 7. Iterate until evidence supports stopping

After every pass regenerate these inventories:

| Ledger | Required accounting |
| --- | --- |
| Physical | All source bytes, allocated/free status, metadata/payload/slack/remnant classification, anomalies |
| Content | All files/records, nested streams, consumed/trailing bytes, formats, output hashes, decoder and validation |
| Semantic | Entrypoints, functions, tables, state fields, transitions, hardware paths, confidence, independent checks |

Prioritize unresolved regions by their loaders and consumers. Revisit earlier
labels when new cross-references contradict them. Keep a corrections log and a
work queue with the next command/experiment, prerequisites and expected evidence.

Completion requires all recoverable material decoded and every remaining unknown
supported by an explicit exhaustion record: avenues tried, results, unavailable
evidence/tooling and the precise new evidence needed to proceed. Zero-filled or
free bytes can be physically classified without semantic interpretation. Unknown
code cannot be declared understood because no more automatic functions appear.
If executable paths, formats or verification experiments remain accessible,
continue. Report partial milestones honestly without calling the goal complete.

## Finding record

Use stable IDs and include: claim; source SHA-256; typed byte/address ranges;
derivation and consumer sites; output/script hashes; reproducible command;
confidence (observed, instruction-backed, structural candidate, open, superseded);
independent check and tested domain; unresolved issues; next experiment.
