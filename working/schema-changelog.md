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
