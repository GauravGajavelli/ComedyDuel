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
7. `setup_frame`
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
- Known candidates: `reinterpretation` (36% in pilot), `establishes_norm`
  (~80% in pilot).

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

The current schema was derived from 5 Seinfeld Season 1 openings — a single
comedian's narrow stylistic range (observational, lateral_observer positioning,
anthropological register). As annotation expands to:

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

2. Launch one agent per episode with this prompt template:
   - Include the full pivot-mechanisms.yaml vocabulary (the 6 operations
     with their tests)
   - Include the templates.yaml vocabulary
   - Include the Pass 2 field order (9 steps above)
   - Include the raw transcript for that episode only
   - Ask for YAML output with one entry per laugh-point
   - Ask them to tag difficulties and vocabulary gaps

3. When agents complete, compare their classifications. Disagreements are
   data — they reveal boundary softness in the vocabulary.

4. Run the batch review checks (Step 4) on the combined results.

## Known open issues (as of 2026-04-23)

These are tracked in `working/questions.md` with appearance counts:

- **[!] reinterpretation/articulation boundary** (5+ appearances) — HIGH
  PRIORITY. Proposed fix: frame-dependency test. Needs validation on 10+
  annotations.
- **false_equivalence vs revealed_equivalence** (3 appearances) — AT
  THRESHOLD. Should be addressed at next weekly review.
- **template gap: monumental_as_mundane** (1 appearance) — needs 2 more.
- **template gap: pure articulation shape** (2 appearances) — needs 1 more.
- **setup_frame: establishes_norm at ~80%** — needs 30+ annotations to
  confirm.
- **laugh architecture field** — flagged for investigation, needs audio data.
- **reinterpretation at 36%** — watch for broadness at 30+ annotations.
