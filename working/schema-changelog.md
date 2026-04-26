# Schema Changelog

Every change to `engine/schema.yaml`, to `engine/vocabularies/*.yaml`, or
to `engine/concepts/` (other than normal concept-node creation) is logged
here. The changelog exists so that annotations can be interpreted in the
context of the schema version that produced them, and so that changes
with downstream impact can be audited.

## Format

```
## [date] v[N.M] - [short description]

**Changed:** What file/field/value changed.
**From:** Prior state (or "(new)" for additions).
**To:** New state (or "(removed)" for deletions).
**Rationale:** Why the change was made. For field additions, include
  answers to the five structural questions. For vocabulary additions,
  include the full definition block. For removals, include usage data.
**Invalidates:** Which prior annotations (if any) need re-review as a
  result of this change.
```

## Rules

- Every schema/vocabulary change requires an entry BEFORE the change is
  committed. Changes without entries aren't allowed.
- Invalidation is serious. If a change invalidates prior annotations,
  list the joke IDs and flag them for re-review during the next weekly
  review session.
- Version numbers follow semantic intent: bump major (v1 → v2) for
  changes that invalidate many prior annotations; bump minor (v0.1 →
  v0.2) for additive or non-invalidating changes.
- During Phase 0, expect frequent changes. Don't hesitate to log small
  ones — the record is more useful than the overhead is costly.

---

## 2026-04-21 v0.1 — Initial schema

**Changed:** Initial creation of schema.yaml, protocols.md, and starter
vocabularies (incongruity-types, templates, positioning, subversions,
affect-axes).

**From:** (new)

**To:**
- schema.yaml with nine-layer decomposition (content, logic, structure,
  performance, voice, affective, narrative, relational, meta)
- joke/performance structural split
- multi-pass annotation workflow with annotation_status tracking
- pivot_locus field (logical | affective | both)
- affective trajectories anchored to structural events
- concept nodes as typed references, not bare strings
- gloss vs structured field distinction
- commutation test using field-paths for structured reference

**Rationale:** Captures all architectural decisions from the initial
design conversation. This version is provisional — expect revision after
the first 5–10 annotations surface issues the initial design didn't
anticipate.

**Invalidates:** None (no prior annotations exist).

---

## 2026-04-22 v0.2 — Incongruity types restructured; routine support added

**Changed:** engine/vocabularies/incongruity-types.yaml (restructure) and
engine/schema.yaml (narrative layer additions).

**From:**
- incongruity-types had `reframe` as a selectable value alongside sub-kinds
  (literalization, figuration, category_error), which meant every joke
  could plausibly be classified as reframe because the sub-kinds were all
  species of it.
- narrative layer had no explicit support for routines (sequences of
  one-pivot jokes that form a sustained bit). First real annotation
  revealed a Seinfeld bit that is six sub-jokes sharing a premise, and
  the current schema would force them into a single annotation,
  flattening internal structure.

**To:**
- `reframe` removed as a selectable incongruity_type value. Header comment
  added explaining that every value in the vocabulary is a specific kind
  of reframe; if a joke doesn't fit any, that's either unfinished analysis
  or a new sub-kind.
- Added `register_deflation` (setup establishes elevated register; punchline
  delivers register-deflated non-answer or trivial content within the same
  elevated frame) as a new incongruity type.
- Added `scope_expansion` (specific observation promoted to universal law,
  or vice versa) as a new incongruity type.
- narrative layer gained `routine_id`, `position_in_routine`, and
  `routine_total_jokes` fields. `position_in_set` retained but scope
  narrowed — it now describes position within a larger performance,
  while routine position is its own tighter field.
- Introduced `engine/routines/` directory for routine-level metadata
  (shared source, running premise, ordered list of joke_ids).

**Rationale:**
Both changes were prompted by attempting the first real annotation (a
Seinfeld "going out" bit from Season 3). The reframe-as-catchall problem
was a design error in v0.1: making a genus selectable alongside its
species produced systematic misclassification. The routine problem
exposed a gap between the spec's "unit of composition is the joke" claim
and the schema's inability to link jokes into tight sequences beyond the
loose `running_premise` field.

Both changes are pre-Phase-0-annotation, so no existing annotations are
invalidated. Going forward, any annotation of a joke that's part of a
routine should fill in routine_id, position_in_routine, and
routine_total_jokes.

**Invalidates:** None (no prior annotations exist).

---

## 2026-04-22 v0.3 — Specificity vocabulary added; template/concept distinction clarified

**Changed:**
- engine/vocabularies/specificity.yaml (new file)
- protocols.md (pre-session checklist expanded; template/concept rule added to during-any-pass rules; specificity field reference updated)
- system-prompt.md (rule 20 added: template/concept distinction enforcement; specificity.yaml added to vocabulary file list)

**From:**
- Specificity field existed in the schema but had no anchor definitions. The verification guide referenced anchors that didn't exist.
- Protocols implied but didn't state the distinction between concepts (what the joke is about) and templates (how the joke operates). First annotation session revealed genuine confusion about whether `mundane_as_monumental` was a concept or a template.
- Pre-session checklist didn't explicitly reference two-stage capture or the batching-across-jokes default.

**To:**
- specificity.yaml defines a 1–5 scale with anchor descriptions and positive examples for each level, plus calibration notes.
- Protocols include an explicit during-any-pass rule: concepts are *subjects* (things the joke is about); templates are *moves* (how the joke operates on those subjects). The test is whether the item could be applied to many different subjects (template) or is itself a subject many moves could operate on (concept).
- Pre-session checklist expanded from six to seven items, explicitly referencing two-stage capture, batching default, and vocabulary-file-open discipline.
- System prompt rule 20 requires the assistant to flag template-ish values being proposed as concepts, rather than silently accepting.

**Rationale:** Triggered by the same first-annotation session as v0.2. The template/concept confusion produced a specific failure mode: ideas like `mundane_as_monumental` being proposed as concepts when they're templates, which would corrupt the knowledge graph if not caught. Better to make the distinction explicit in protocols and enforce it in the assistant than to rely on careful reading of the schema's technical term usage.

**Invalidates:** None (no prior annotations exist).

---

## 2026-04-22 v0.4 — incongruity_type becomes primary/secondary

**Changed:**
- engine/schema.yaml: `logic.incongruity_type` changes from single-valued string to a sub-block with `primary` (required, single-valued) and `secondary` (optional, multi-valued).
- protocols.md: Pass 2 field-order updated; new subsection "Secondary incongruity types: when to populate" added after two-stage capture; per-field verification guide split into primary and secondary entries; Pass 4 updated to commutation-check secondary entries; weekly review gains a secondary-usage ratio check.
- system-prompt.md: Pass 2 sequence updated to distinguish primary from secondary and to require the three-part discipline before accepting secondary values.

**From:** `incongruity_type: ""` (single string, forced single classification).

**To:**
```yaml
incongruity_type:
  primary: ""        # single required value
  secondary: []      # optional, multi-valued; governed by
                     # simultaneity/commutation/independence discipline
```

**Rationale:** A joke can legitimately have two mechanisms operating simultaneously at the same pivot (Case 1 in the design discussion): the Hedberg "Watch for children" joke is arguably both literalization AND category_error at once. The previous single-valued schema forced an arbitrary pick, losing the co-occurrence signal the engine could otherwise learn from.

However, two failure modes needed to be blocked: (1) using primary+secondary to encode *uncertainty* (which pollutes co-occurrence data) and (2) using secondary to encode *plausible alternative readings* that aren't actually doing work in the joke. Both are blocked by the three-part discipline (simultaneity, commutation weakening, independence) that each secondary entry must survive. Pass 4's commutation test rechecks secondary entries; entries that fail are removed.

Target frequency for secondary population is ≤15% of annotations. >30% is flagged during weekly review as evidence the discipline is slipping.

**Structural-question answers for this field change:**
1. Can it take multiple simultaneous values? YES — that's the point. Hence primary+secondary split.
2. Does it change across joke duration? NO — simultaneity rules out trajectory representation (different mechanisms at different events means different pivots, which means different jokes).
3. Are values ordered? YES — primary outranks secondary by commutation load. The ordering is meaningful.
4. Do absent and low-intensity differ? NO — either the mechanism is operating or it isn't.
5. Does meaning depend on another field? Partially — secondary's legitimacy is verified by Pass 4 commutation data, which is another field. The dependency is explicit and checked at commutation time.

**Invalidates:** None (no prior annotations exist). If annotations already existed, they'd migrate as `incongruity_type: "X"` → `incongruity_type: {primary: "X", secondary: []}` — trivially.

---

## 2026-04-22 v0.5 — Replace incongruity_type with pivot_mechanism; anchor unanchored scales

**Changed:**
- engine/schema.yaml: `logic.incongruity_type` (primary/secondary) and
  `logic.incongruity_operates_on` replaced by `logic.pivot_mechanism`
  (operation + reading_switch + scale_shift) and `logic.setup_frame`.
  `performed_relatability.intensity` changed from 0.0-1.0 float to 0-3
  integer. Anchor descriptions added to `vulnerability.personal_exposure`,
  `vulnerability.emotional_risk`, `shared_experience.comprehensibility_
  without_experience`, and `performed_relatability.intensity`. Inline
  criteria added to `editorializes.kind`.
- engine/vocabularies/pivot-mechanisms.yaml (new file): defines 6
  pivot_operation values (negation, reinterpretation, transplant, mapping,
  extension, articulation), 3 reading_switch values (none, figurative_to_
  literal, literal_to_figurative), and 3 scale_shift values (none,
  expansion, contraction). Each operation has a concrete TEST that produces
  a written artifact.
- engine/vocabularies/incongruity-types.yaml: deprecated. Retained with
  migration mapping header.
- engine/vocabularies/templates.yaml: `reductio.distinguished_from.
  literalization` updated to reference reading_switch. `false_equivalence.
  distinguished_from.category_error` replaced with mapping_pivot_operation
  and transplant_pivot_operation. Note added to reductio distinguishing
  template (shape) from extension (operation).
- protocols.md: Pass 2 field order updated. "Secondary incongruity types"
  section replaced with "Pivot mechanism: the three sub-dimensions."
  Per-field verification guide updated. Weekly review's secondary
  incongruity check replaced with modifier usage check.
- engine/system-prompt.md: bumped to v0.2. Pass 2 field sequence updated.
  Vocabulary reference list updated.

**From:**
```yaml
incongruity_type:
  primary: ""      # reversal | literalization | figuration |
                   # category_error | register_deflation | scope_expansion
  secondary: []
incongruity_operates_on:
  setup_frame: null
  punchline_action: null
  reading_switch: null
```
6 compound types that mixed operation, reading mode, and scale into one
pick. Secondary slot needed for cases that were really "operation + modifier."
punchline_action and reading_switch sub-fields partially overlapped with
the top-level types.

**To:**
```yaml
pivot_mechanism:
  operation: ""         # negation | reinterpretation | transplant |
                        # mapping | extension | articulation
  reading_switch: none  # none | figurative_to_literal | literal_to_figurative
  scale_shift: none     # none | expansion | contraction
setup_frame: null       # establishes_norm | establishes_anomaly |
                        # establishes_category | establishes_sequence
```
3 orthogonal sub-dimensions. Secondary slot eliminated — most secondary
cases were "primary + modifier" which the decomposition now captures
natively. punchline_action removed — its information is now in
pivot_mechanism.operation (negation ≈ negates, reinterpretation ≈
redirects, etc.). reading_switch promoted from sub-field to explicit
modifier. setup_frame retained and promoted to top-level field.

**Rationale:**

Tested against 33 humor moments across 5 Seinfeld Season 1 opening
monologues. Under the old system, 76% of moments had low confidence
classifications and 67% had no clean type at all. Seinfeld's dominant
moves — reinterpretation (36%), mapping (27%), articulation (21%),
extension (15%) — were either absent from or poorly served by the old
vocabulary. Under the new system, 100% of moments classified with high
confidence.

The core problem: the old types mixed three independent questions (what
operation, what reading-mode switch, what scale shift) into one
mutually-exclusive pick. register_deflation was often "reinterpretation +
contraction." scope_expansion was often "[any operation] + expansion."
These aren't single types; they're combinations of an operation and a
modifier. Decomposing into orthogonal dimensions eliminates the forced
choice.

New operation values fill genuine gaps:
- mapping: captures analogy (apt parallel between domains). Old system
  force-fitted these into category_error, which requires MISapplication —
  the opposite of what analogy does.
- extension: captures premise-accepted-and-followed-to-absurd-conclusion.
  Had no home in old vocabulary whatsoever.
- articulation: captures single-script humor (shared truth verbalized).
  Old system assumed all humor involves incongruity; articulation doesn't.

Scale and anchor changes address a secondary ambiguity finding:
- vulnerability (0-5 x 2), comprehensibility (0-5), and relatability
  intensity had no anchor descriptions, making calibration impossible.
  Each now has anchor text at each integer value.
- performed_relatability.intensity changed from 0.0-1.0 float to 0-3
  integer because the float invited false precision with no anchors to
  calibrate against.
- editorializes.kind (strong/weak/ironized) had no criteria despite being
  a structured enum. Inline criteria added.

**Structural-question answers for pivot_mechanism:**
1. Can it take multiple simultaneous values? NO for each sub-dimension
   (single-valued within each). The orthogonal decomposition handles what
   secondary used to handle.
2. Does it change across joke duration? NO — the pivot is a single event.
3. Are values ordered? NO for operation (nominal categories). YES for
   scale_shift (contraction < none < expansion is an ordering).
4. Do absent and low-intensity differ? YES for reading_switch and
   scale_shift — "none" means the dimension isn't active, not that it's
   at low intensity.
5. Does meaning depend on another field? operation is independent.
   reading_switch and scale_shift are modifiers that refine but don't
   depend on operation.

**Invalidates:** None (no prior annotations exist).

---

## 2026-04-23 v0.6 — Batch 1 review: templates, setup_frame, boundary sharpening

**Triggered by:** Batch 1 synthesis (71 laugh-points across 14 Seinfeld
episodes 1-15). Seven actionable items from cross-agent annotation.

**Changed:**

1. **engine/vocabularies/templates.yaml**:
   - Added `monumental_as_mundane` (4 appearances: E03, E06, E08, E10).
     Directional inverse of mundane_as_monumental. Full definition block.
   - Added `shared_recognition` (3 appearances: E01, E04, E09). Shape IS
     the naming of shared truth, no secondary structural scaffolding.
   - Broadened `false_equivalence` criterion to cover apt pairings (humor
     in surprising similarity) as well as mismatch pairings. Resolves the
     "revealed_equivalence" gap without a vocabulary split.

2. **engine/schema.yaml**: `setup_frame` expanded from 4 to 6 values.
   `establishes_norm` (80% of annotations) split into `establishes_convention`
   (cultural norms), `establishes_behavior` (behavioral patterns), and
   partially into `establishes_premise` (accepted hypotheticals).
   `establishes_category` replaced by `establishes_premise`.
   `establishes_expectation` added (buildup creating anticipation).
   `establishes_anomaly` and `establishes_sequence` retained.

3. **engine/vocabularies/pivot-mechanisms.yaml**: articulation/reinterpretation
   `distinguished_from` sharpened. Frame-dependency test formalized with 3
   worked examples and a general rule for observational comedy.

4. **protocols.md**: setup_frame reference updated. scale_shift independence
   test added as annotation-time heuristic with worked examples.

**Rationale:** All changes empirically driven by 71 annotations. Every new
value crossed the 3-occurrence threshold. The reinterpretation/articulation
boundary was the most-flagged ambiguity (10+ agents).

**Invalidates:** Batch 1 annotations should have setup_frame re-evaluated
(old `establishes_norm` maps to convention, behavior, or premise). Template
classifications should be reviewed for monumental_as_mundane and
shared_recognition candidates.

---

## 2026-04-25 v0.7 — Act-out structure block added

**Changed:** `engine/schema.yaml` — added `joke.structure.act_out` sub-block
with 4 fields: `present` (boolean), `character_type`, `character_register`,
`register_gap`, and `character_gloss`.

**From:** Act-outs were marked only by `performance_mode: character` in the
annotations (from the earlier joke_annotation_schema.yaml work). The schema
had no structural description of WHAT the character is or HOW the act-out
produces humor — only THAT it happens.

**To:**
```yaml
act_out:
  present: false
  character_type: null    # authority | everyman | enthusiast | expert | innocent
  character_register: null  # confident | bewildered | earnest | bureaucratic | casual
  register_gap: null      # treats_mundane_as_serious | treats_serious_as_mundane |
                          # unaware_of_absurdity | performed_sincerity | none
  character_gloss: ""     # [GLOSS]
```

**Rationale:** Act-outs appear in ~60%+ of annotated Seinfeld monologues and
are the most performance-dependent laugh-points (flagged by 2+ agents as
"performance-carried"). The block captures the structural information the
realization stage needs to GENERATE act-outs: what kind of character to
create, what register they speak in, and what gap between their register and
reality produces the humor. This is also the mechanism underlying
conversational roast comedy (Curb Your Enthusiasm, roast battles) —
identifying an exploitable premise, selecting a character perspective that
maximizes the comedic gap, and constructing dialogue in that register.

For generation: act-outs are easier for LLMs than pure observation because
the character voice constrains the output productively. "Speak as this
character in this situation" is a more reliable prompt pattern than "make an
original observation."

**Structural-question answers:**
1. Multiple simultaneous values? NO — one act-out per joke. Multi-character
   act-outs (two characters in dialogue) are the comedian switching between
   two act-outs sequentially, not one act-out with multiple values.
2. Changes across duration? The character_type and register are constant
   within a single act-out. If the character's register shifts, that's a
   register_break subversion, not a trajectory.
3. Ordered values? NO for character_type and character_register (nominal).
   register_gap could be argued as ordered but is better treated as nominal.
4. Absent vs. low-intensity? YES — `present: false` means no act-out at all;
   `register_gap: none` means an act-out exists but the character's register
   matches the situation. These are different.
5. Meaning depends on other fields? character_register and register_gap
   interact (the gap is defined relative to the register), but this is
   explicit in the field definitions rather than hidden.

**Invalidates:** Batch 1 annotations that have `performance_mode: character`
in the earlier annotated_monologues.yaml should have the act_out block
populated during audit. Known candidates from batch 1:
- S01E01: phone call act-out (everyman, bewildered, none)
- S01E02: cheque-book woman (everyman, confident, treats_mundane_as_serious)
- S01E02: mother's note voice (authority, earnest, none)
- S01E05: emperor/diner (enthusiast, confident, treats_mundane_as_serious)
- S01E05: mystified diner (everyman, bewildered, unaware_of_absurdity)
- S01E06: lane expert (enthusiast, earnest, treats_mundane_as_serious)
- S01E06: backwards-traffic driver (everyman, casual, treats_serious_as_mundane)
- S01E07: leisure police (authority, bureaucratic, treats_mundane_as_serious)
- S01E08: alien fashion committee (authority, confident, treats_mundane_as_serious)
- S01E08: earth-outfit voter (everyman, casual, treats_serious_as_mundane)

---

## 2026-04-26 v0.8 — Wordplay added as 4th modifier sub-dimension

**Triggered by:** Cross-reference of Toplyn's WitScript patent taxonomy (US
10,642,939 / 10,878,817 / 11,080,485) against the schema's pivot operations.
Analysis of all 3 patents revealed that phonemic humor (puns, portmanteaus,
near-homophones) was a genuine gap. Initially added as a 7th operation, but
immediately corrected: wordplay is a DELIVERY VEHICLE for an underlying
cognitive operation, not an operation itself. A joke like "Tinderella" is
mapping (the parallel between dating apps and fairy tales) + portmanteau
(the phonemic blend that delivers the parallel). The cognitive operation
(mapping) and the lexical mechanism (portmanteau) are orthogonal —
wordplay belongs as a modifier alongside reading_switch and scale_shift.

**Changed:**

1. **engine/vocabularies/pivot-mechanisms.yaml**: Added `wordplay` as
   SUB-DIMENSION 4 (modifier, not operation) with 3 values: phonemic_pair,
   portmanteau, collocation_disruption. Full vocabulary definitions with
   criterion, test, positive example, distinguished_from. Added combined
   classification examples showing operation + wordplay co-occurrence
   (mapping + portmanteau, transplant + collocation_disruption,
   reinterpretation + collocation_disruption). Updated theoretical
   grounding header to clarify wordplay is a modifier not an operation.
   Removed wordplay from the operations section. Kept 6 operations.

2. **engine/schema.yaml** (v0.8): Removed `wordplay` from operation enum
   (stays at 6 operations). Added `wordplay` as a 4th modifier sub-field
   in pivot_mechanism (none | phonemic_pair | portmanteau |
   collocation_disruption). Independent of operation — a joke can be
   mapping + portmanteau, transplant + collocation_disruption, etc.
   The specific pun words are NOT recorded.

**From:** 6 pivot operations + 3 modifier sub-dimensions (reading_switch,
scale_shift). No phonemic humor capability.

**To:** 6 pivot operations (unchanged) + 4 modifier sub-dimensions
(+wordplay). Wordplay is orthogonal to operation — it describes HOW the
pivot is delivered lexically, not WHAT cognitive shift occurs.

**Rationale:**

The Toplyn patent cross-reference revealed that his formula taxonomy
operates at the LEXICAL level (how to construct funny words) while our
operations are COGNITIVE (what the punchline does to the frame). These are
orthogonal, not alternatives. Wordplay is a delivery vehicle: "Tinderella"
is mapping (dating app ↔ fairy tale parallel) + portmanteau (phonemic
blend). Making wordplay a 7th operation was a category error — it would
have been mutually exclusive with the cognitive operations when in fact
it co-occurs with them.

Key design decision: the annotation records the PATTERN (which sub-type,
which domains), not the specific words:
1. Recording specific pun words isn't useful for generating ORIGINAL puns
2. The realization stage needs "make a portmanteau from domains X and Y"
   not "use the word 'Zikachu'"
3. Toplyn's phonemic-matching algorithms (edit distance, stop consonant
   scoring, alliteration) are realization-stage tools that generate the
   specific words from the pattern specification

The 3 sub-types map directly to Toplyn's patent types:
- phonemic_pair → Toplyn Type #1 (two words with phonemic similarity)
- portmanteau → Toplyn Types #2/#4 (blended neologism from two domains)
- collocation_disruption → Toplyn Type #4 (known phrase with word swapped)

**Structural-question answers (for wordplay as modifier):**
1. Multiple simultaneous values? NO — one wordplay sub-type per joke.
2. Changes across duration? NO — the phonemic collision is instantaneous.
3. Ordered values? NO — the three sub-types are nominal categories.
4. Absent vs. low-intensity? YES — `wordplay: none` means no phonemic
   mechanism is used. This is different from "weak wordplay."
5. Meaning depends on other fields? Independent of operation — wordplay
   can co-occur with any of the 6 cognitive operations. The combination
   (e.g., mapping + portmanteau) is the full classification.

**Invalidates:** No existing annotations use wordplay (Seinfeld's monologues
have almost no puns). The modifier will begin appearing when the corpus
expands beyond Seinfeld to comedians who use wordplay (Hedberg, Wright)
or when the generation pipeline produces pun-based jokes.

---

## 2026-04-26 v0.9 — Comprehensive level-assignment audit

**Triggered by:** Three parallel audit agents checked every field in the
schema for correct block (joke vs performance), layer, and level placement.
The wordplay correction (v0.8) showed that level-assignment errors are real.
The audit found systemic issues, primarily in the performance.relational
layer which was almost entirely misplaced.

**Meta rules formalized:** Added "Architectural levels" section to schema
header with 6 cross-level validation tests (block test, layer test, mutual
exclusivity test, orthogonality test, shape-not-content test, redundancy
test). These govern all future field additions.

**Tier 1 changes (block/layer reclassifications):**

1. **NEW joke.relational layer** — created to house textually-determined
   relational properties that were incorrectly in performance.relational.
   Moved: positioning (default + trajectory), audience_implication,
   shared_experience (required, universality, comprehensibility),
   performed_relatability.present. These are properties of the joke's
   text — same value regardless of performer.

2. **performance.relational reduced** — now contains only performer-variable
   properties: vulnerability (personal_exposure, emotional_risk),
   performed_relatability.intensity, and new positioning_deviation field.

3. **act_out split** — character_type and register_gap stay in
   joke.structure (textually determined). character_register moved to
   performance.delivery.act_out_voice (performer varies how they voice
   the character).

4. **register_break moved** from subversions (joke.structure) to
   performance.delivery.register_break. It is performer-specific — what's
   a register break for Mort is baseline for Cece.

5. **anti_callback moved** from subversions (joke.structure) to
   joke.narrative.anti_callback. It is context-dependent — depends on
   what was performed earlier in the set.

**Tier 2 changes (vocabulary quality):**

6. **false_equivalence renamed to comparison** in templates.yaml. The
   actual structural feature is juxtaposition/pairing of two things,
   not a specific logical error. The renamed version foregrounds the
   discourse shape ("the joke unfolds as a comparison") rather than
   overclaiming a logical relationship.

7. **anthropomorphization removed from templates** and moved to
   joke.content.content_moves. It is a content-level technique (what
   the joke does with its subject), not a rhetorical shape (how the
   joke unfolds). Jokes that anthropomorphize now get their actual
   rhetorical shape as the template (escalation, reductio, comparison)
   plus content_moves: [anthropomorphization].

8. **shared_recognition renamed to bare_observation** in templates.yaml.
   It describes the absence of rhetorical scaffolding, not a positive
   shape. The rename clarifies that this is the minimal/null template
   value for jokes whose shape IS the observation itself.

**Tier 3 changes (documentation):**

9. **Articulation documented as "null operation"** in schema header meta
   rules. It describes cognitive RECOGNITION, not a frame shift. Its
   theoretical grounding (social bonding / benign violation of silence)
   is explicitly noted as different from the other 5 operations.

10. **reading_switch entanglement documented** — gravitates toward
    reinterpretation, near-incompatible with articulation. Documented
    in schema header and in the reading_switch field comment.

11. **scale_shift independence test added** to field comment — "If I
    removed the scale change but kept the operation, would the joke
    still work at reduced effectiveness?" If the joke dies entirely,
    the scale change IS the operation.

12. **tag_function split** into tag_operation (extends | reframes |
    undercuts) and tag_callbacks_to (joke_id, moved to narrative layer).
    The prior value callbacks_earlier conflated the tag's relationship
    to its own punchline with the tag's relationship to a prior joke.

**Templates after v0.9:** mundane_as_monumental, monumental_as_mundane,
bare_observation, escalation, reductio, comparison (6 values).

**Subversions after v0.9:** structural_refusal, meta_structural,
specificity_subversion (3 values — register_break and anti_callback
moved to their correct locations).

**Invalidates:** All 71 batch 1 annotations need:
- template: any `shared_recognition` → `bare_observation`
- template: any `false_equivalence` → `comparison`
- template: any `anthropomorphization` → actual rhetorical shape + content_moves
- positioning, audience_implication, shared_experience → move from performance to joke.relational
- act_out.character_register → move to performance.delivery.act_out_voice
- tag_function: callbacks_earlier → split to tag_operation + narrative.tag_callbacks_to
- subversions: register_break → move to performance.delivery.register_break
- subversions: anti_callback → move to joke.narrative.anti_callback

---
