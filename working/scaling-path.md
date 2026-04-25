# Scaling Path — Annotation & Schema Refinement

Instructions for continuing the annotation and schema refinement process across
Seinfeld episodes (and eventually other comedians). This file is designed to be
self-contained: a new session with cleared context can follow these instructions
without prior conversation history.

## Context

The project is building an annotation schema for decomposing standup comedy
jokes into structured fields that a generation engine can compute on. The
schema has been through v0.5 of iterative refinement, validated against 5
Seinfeld Season 1 opening monologues (episodes 1-5). Five independent
annotation agents confirmed the schema works but surfaced specific ambiguities
and vocabulary gaps that need ongoing monitoring.

## Files to read before starting

Read these files in this order to have full context:

1. `engine/schema.yaml` — the annotation schema (what fields exist, what they mean)
2. `engine/vocabularies/pivot-mechanisms.yaml` — the core humor-mechanism vocabulary
3. `engine/vocabularies/templates.yaml` — rhetorical shape vocabulary
4. `engine/vocabularies/positioning.yaml` — comedian stance vocabulary
5. `engine/vocabularies/subversions.yaml` — anti-formula moves
6. `engine/vocabularies/affect-axes.yaml` — valence/arousal scales
7. `engine/vocabularies/specificity.yaml` — content specificity scale
8. `protocols.md` — operational procedures (multi-pass workflow, weekly review, schema maintenance)
9. `engine/system-prompt.md` — the annotation assistant's system prompt
10. `working/questions.md` — open questions and vocabulary gap tracker
11. `working/schema-changelog.md` — history of schema changes
12. `working/field-usage.md` — field and value usage tracking
13. `working/decision-log.md` — non-obvious judgment calls

Also check for existing annotations:
- `annotations/` directory for any completed annotation files
- `engine/vocabularies/annotated_monologues.yaml` — reference annotations from initial schema exploration (uses older vocabulary; useful for comparison but not authoritative)
- `engine/vocabularies/reclassification-test.yaml` — the 5-episode reclassification under the v0.5 schema (useful as a baseline for comparison)

## Episode source

Seinfeld opening monologue transcripts are in `engine/raw_scripts/`. The
scraping script at `engine/scrape_seinfeld.py` can fetch additional episodes
from seinfeldscripts.com (handles SSL cert issues). To fetch more episodes,
modify the `targets = selected[:5]` line to select different episode indices
from the `episodes` list.

## The batch annotation cycle

Work in batches of 5-10 episodes. Each batch follows this cycle:

### Step 1: Scrape and segment (if needed)

If raw scripts don't exist for the target episodes:
```
python3 engine/scrape_seinfeld.py
```
Modify the script to select the desired episode range first.

Then manually identify the opening monologue boundaries in each raw script
file. The monologue starts at the first `[Scene: Comedy club]` or
`[Setting: Nightclub]` marker and ends at the first scene transition
(`[Scene:` or `[Setting:` with a non-comedy-club location).

### Step 2: Annotate (Pass 2 — silent decomposition)

For each episode's opening monologue, perform a Pass 2 annotation following
the protocol in `protocols.md`. The field order is:

1. GLOSS: `setup_expectation`, `punchline_violation` (reasoning trace)
2. `pivot_locus` (logical / affective / both)
3. `pivot_concept`
4. `pivot_mechanism.operation` — run the TEST from `pivot-mechanisms.yaml`
5. `pivot_mechanism.reading_switch` (default: none)
6. `pivot_mechanism.scale_shift` (default: none)
7. `setup_frame` (establishes_convention | establishes_behavior |
   establishes_expectation | establishes_premise | establishes_anomaly |
   establishes_sequence)
8. `primary_template` from `templates.yaml`
9. Tag difficulties and vocabulary gaps

For each laugh-point, run the operation's test and write down the concrete
artifact (two readings, a negated claim, a source/target pair, etc.). The
value whose test produces the cleanest artifact is the correct classification.

**Scale_shift heuristic:** Populate only when you can imagine the same
operation WITHOUT the scale change. If `reinterpretation + none` would still
describe the joke fully, leave scale_shift as none. If removing the scale
change loses a meaningful aspect of the humor, populate it.

**Reinterpretation vs articulation:** If both seem to fit, apply the frame-
dependency test: "Does the humor REQUIRE the audience to shift frames, or
does it work within a single frame?" If removing the frame shift kills the
joke, it's reinterpretation. If the joke survives within the audience's
existing frame, it's articulation.

**When mapping becomes extension in a routine:** Within a multi-beat bit,
a tag/topper can have a different operation than the joke it extends. If the
initial joke establishes a mapping and a subsequent beat follows that mapping's
internal logic to an absurd destination, the tag is extension. Test: "Could
this beat work without referencing the second domain — stated purely in terms
of the target domain's logic?" If yes, it's extension wearing the mapping's
costume.

Save annotations to `annotations/{joke_id}.yaml` or batch them in
`annotations/{episode_slug}_pass2.yaml`.

### Step 2b: Extract and persist agent annotations

When using parallel subagents, some agents write annotation files to disk
and others return them inline in their result messages. After all agents
complete, run the extraction script to ensure all annotations are persisted:

```
python3 engine/extract_annotations.py
```

The script reads agent output files from the tasks directory, extracts
YAML blocks from ```yaml fences in assistant messages, and writes them to
`annotations/`. It skips episodes already on disk.

**Before running**, update the `AGENT_MAP` dictionary in the script to map
each agent's ID to its episode identifier. Agent IDs are printed when
agents are launched (the `agentId` in the launch confirmation). The
mapping format is:

```python
AGENT_MAP = {
    "agent_id_here": ("s01e06", "The Ex-Girlfriend"),
    ...
}
```

Also update `ALREADY_ON_DISK` to list episode IDs that agents already
wrote to `annotations/` directly.

After extraction, verify:
1. All expected files exist: `ls annotations/*.yaml`
2. All files are valid YAML: run the validation loop from the script
3. No files are truncated: check line counts are reasonable (200-500 lines
   per episode is typical)

### Step 3: Log gaps and difficulties

After each annotation session, update:
- `working/questions.md` — log any vocabulary gaps with joke_id. Update
  appearance counts for existing gaps.
- `working/decision-log.md` — log any forced choices or close calls.

### Step 4: Batch review (after each batch of 5-10 episodes)

Run these checks after completing each batch:

**4a. Vocabulary gap tally.** Check `working/questions.md` for gaps that
have reached 3 occurrences. For each:
- Can you provide the full definition block (criterion, positive example,
  near-miss negative, distinguished_from)?
- If yes: add the value to the appropriate vocabulary file, log in
  `working/schema-changelog.md`, bump schema version.
- If no: the gap may be a boundary problem in an existing value rather than
  a missing value. Log this assessment.

**4b. Value broadness check.** Count the distribution of each vocabulary's
values across the batch's annotations. If any single value exceeds 40%:
- Collect all jokes classified under that value.
- Look for clusters — do they subdivide into 2-3 groups?
- If yes, draft sub-species with full vocabulary discipline.
- If no, note and re-check at next interval.
- Known candidate: `reinterpretation` (31% in batch 1 — below threshold
  but watch). `establishes_norm` was resolved in v0.6 by splitting into
  convention/behavior/premise. `mundane_as_monumental` was 42% in batch 1,
  resolved by adding `monumental_as_mundane` (expected to drop to ~32%).

**4c. Cross-annotator consistency.** If multiple annotators (or parallel
agents) annotated the same episodes, compare their operation classifications.
Disagreements reveal boundary softness. Document the disagreement patterns.

**4d. Emergence of new operation types.** If jokes repeatedly fail all 6
operation tests (none produce a clean artifact), a new operation may be
needed. Requirements for adding a new pivot_mechanism.operation:
- 3+ jokes that don't fit any existing operation
- A testable criterion that produces a concrete artifact
- Positive example, near-miss negative, distinguished_from for nearest
  neighbors
- The new operation must be grounded in a describable cognitive mechanism
  (see "Comedy theory grounding" below)
- Log in schema-changelog with full rationale

**4e. Template check.** Same procedure as 4a/4b but for template values.

### Step 5: Update schema (if warranted)

Apply any vocabulary additions, field changes, or value splits identified
in Step 4. Follow the schema maintenance procedures in `protocols.md`:
- Every change requires a `schema-changelog.md` entry
- New fields require the 5 structural questions
- New values require the full definition block
- Bump schema version

### Step 6: Re-annotate spot-check

Pick 2-3 annotations from the previous batch and re-annotate them cold under
the updated schema. Compare with the original. This catches both schema drift
and annotator drift.

## Comedy theory grounding for new operations

The current 6 pivot operations are grounded in different theoretical traditions:

| Operation | Theoretical basis | What it captures |
|---|---|---|
| negation | Incongruity theory (truth-value flip) | Setup claim is contradicted |
| reinterpretation | Incongruity theory (frame switch) | Same material, different frame |
| transplant | Incongruity theory (domain violation) | Foreign framework misapplied |
| mapping | Bisociation (Koestler) | Two domains share hidden structure |
| extension | Logic of the absurd (reductio) | Premise accepted, logic followed past reason |
| articulation | Social bonding / benign violation of silence | Shared truth verbalized |

The schema does NOT assume all humor is incongruity-based. Articulation is
grounded in benign violation theory (McGraw & Warren 2010) — the violation is
of the norm of silence around shared truths — and social bonding theory. This
is a deliberate choice: the schema describes what jokes actually do, not what
a single theory predicts they should do.

When proposing new operations, identify:
1. **What cognitive operation** the punchline performs (the mechanism)
2. **Which theory** best explains why it's funny (the grounding)
3. **What test** an annotator can run to identify it (the artifact)
4. **Why existing operations don't cover it** (the gap)

A new operation doesn't need to fit incongruity theory. It needs to describe
a real, recurring, distinguishable mechanism that the existing 6 don't capture.
The theoretical grounding helps explain WHY it works but doesn't gate WHETHER
it's included.

## Scaling beyond Seinfeld

The schema has been validated against 14 Seinfeld episodes (Seasons 1-2,
71 laugh-points). As annotation expands to:

- **Later Seinfeld** (Seasons 3-9): Expect the existing operations to
  hold but templates and subversions to become more relevant as the material
  matures.
- **Other observational comics** (Hedberg, Wright): Expect literalization
  (reinterpretation + figurative_to_literal) and negation to become more
  common. Articulation may drop.
- **Character/confessional comics** (Bamford, Mulaney): Expect the
  vulnerability and positioning scales to get their first real workout.
  New operations may surface for self-deprecation mechanics.
- **Absurdist comics** (Cece-style): Expect extension and transplant to
  dominate. Anthropomorphization template should surface. New operations
  may be needed for surreal/non-sequitur humor.

The 6 current operations should be treated as provisional. Expect 1-2
additions by the time 50 jokes are annotated, and possible splitting of
reinterpretation if sub-species emerge.

## Parallel annotation with subagents

To annotate a batch in parallel using Claude Code subagents:

1. Prepare: for each episode, have the raw transcript and the manually
   identified monologue boundaries ready.

2. Launch one agent per episode using the prompt template below.
   **IMPORTANT**: Before launching, read the CURRENT versions of
   `engine/vocabularies/pivot-mechanisms.yaml` and
   `engine/vocabularies/templates.yaml` and include their values in the
   prompt. Do NOT hardcode values from a prior session — the vocabularies
   evolve. The template below marks where to insert current values.

3. When agents complete, run `python3 engine/extract_annotations.py`
   (after updating the AGENT_MAP) to persist all annotations to disk.
   Verify all files exist and are valid YAML.

4. Compare agent classifications. Disagreements are data — they reveal
   boundary softness in the vocabulary.

5. Run the batch review checks (Step 4) on the combined results.

### Agent prompt template

Copy this template for each agent. Replace `[PLACEHOLDERS]` with current
values from the vocabulary files.

```
You are performing a Pass 2 (silent decomposition) annotation on a
Seinfeld opening monologue. Produce YAML with one entry per distinct
laugh-point.

## FIELD ORDER (follow exactly)
1. setup_expectation (GLOSS — your reasoning trace)
2. punchline_violation (GLOSS)
3. pivot_locus: logical | affective | both
4. pivot_concept
5. pivot_mechanism.operation — run the TEST below, write down the artifact
6. pivot_mechanism.reading_switch: none | figurative_to_literal | literal_to_figurative
7. pivot_mechanism.scale_shift: none | expansion | contraction
8. setup_frame: establishes_convention | establishes_behavior |
   establishes_expectation | establishes_premise | establishes_anomaly |
   establishes_sequence
9. primary_template: [INSERT CURRENT TEMPLATE VALUES FROM templates.yaml]
10. physical_performance: null
11. difficulties (tag ambiguities, vocabulary gaps, forced choices)

## OPERATION TESTS
[INSERT THE 6 OPERATIONS AND THEIR TESTS FROM pivot-mechanisms.yaml]

## DISAMBIGUATION RULES
- reinterpretation vs articulation: Does humor REQUIRE a frame shift?
  If removing the shift kills it → reinterpretation. If it works within
  one frame → articulation. Ask: "Is the OBSERVATION the joke, or is
  the ANGLE on the observation the joke?"
- scale_shift: Only populate if you can imagine the same operation
  WITHOUT the scale change and it would lose something specific.
  If the scale change IS the operation, leave as none.
- mapping vs transplant: Would joke work if the framework genuinely
  fit? Yes → mapping (aptness). No → transplant (mismatch).

## setup_frame GUIDE
- establishes_convention: cultural practice, social ritual,
  institutional norm ("how things work")
- establishes_behavior: recognizable human behavioral pattern
  ("people do this")
- establishes_expectation: buildup creating specific anticipation
  of a proportional payoff
- establishes_premise: accepted claim or hypothetical that subsequent
  jokes build on
- establishes_anomaly: something unusual or puzzling needing explanation
- establishes_sequence: ordered progression creating momentum

## TRANSCRIPT — [EPISODE ID] "[TITLE]"
[INSERT MONOLOGUE TEXT]

Report YAML then under 300 words of commentary noting: which operations
dominated, hardest classification call, any vocabulary gaps.
```

## Known open issues (as of 2026-04-23, schema v0.6)

These are tracked in `working/questions.md` with appearance counts.
Items marked RESOLVED were addressed in v0.6; they're listed here for
context so future sessions understand what was already tried.

**Open:**
- **reinterpretation/articulation boundary** (10+ appearances) — PARTIALLY
  RESOLVED in v0.6. Frame-dependency test + worked examples added to
  pivot-mechanisms.yaml. Needs validation: does the sharpened test reduce
  disagreement in batch 2?
- **laugh architecture field** — flagged for investigation, needs audio data.
- **reinterpretation at 31%** — below 40% threshold but watch.
- **valence_flip modifier** (1 appearance) — tracking.
- **counterfactual staging device** (1 appearance) — tracking.
- **anachronistic transplant sub-type** (1 appearance) — tracking.
- **performance-dependent laugh-points** (2 appearances) — awkward in Pass 2.

**Resolved in v0.6:**
- monumental_as_mundane template — added (4 appearances).
- shared_recognition template — added (3 appearances).
- false_equivalence broadened to cover apt pairings (3 appearances).
- setup_frame expanded from 4 to 6 values (80% establishes_norm confirmed).
- scale_shift independence heuristic added to protocols.
