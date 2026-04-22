# Comedy Duel — Operational Protocols

*Companion to spec.md. This document holds procedures; the spec holds architecture.*

This file is for you-in-the-moment, about to start an annotation session or about to review the week's work. It's deliberately short. Each protocol is an actual checklist you read before the relevant work, not background reading.

If this document grows past ten minutes of total reading time, it has become too much to be useful. Prune rather than expand.

---

## Pre-session checklist (30 seconds, before every annotation session)

Read these seven lines before starting. They prime attention; don't rely on memory during the session.

1. Which pass am I doing? (1: transcription + segmentation / 2: silent decomposition / 3: aloud performance / 4: commutation / 5: adversarial). Stay in that mode.
2. Am I batching this pass across jokes (default) or doing all passes on one joke (rare, only when <3 jokes exist to batch against)?
3. The vocabulary file for any structured field is open before I populate that field. Externalized memory beats remembered values.
4. Two-stage capture: intuitive call first (Stage 1), definition check second (Stage 2). Assistant can read definitions back; never propose values.
5. Log anything I can't justify in `working/decision-log.md` with the joke ID.
6. If the schema doesn't fit something, note it in `working/questions.md`. Don't force-fit.
7. Update `annotation_status` at session end for every joke touched.

---

## Annotation workflow: the multi-pass model

Annotation is not a single activity. Five distinct passes, each in a different mental mode, each operating on a different subset of the schema. Running them separately costs less total effort than one "complete" pass because each pass runs in a narrow mode it can sustain without fatigue.

**Batch passes across jokes, not jokes across passes.** A session should do one pass for multiple jokes, not multiple passes for one joke. Running Pass 2 across 5 jokes in a session takes less total effort than running Passes 2–5 for one joke in one session, because each pass gets calibration from adjacent jokes (you learn what "reversal" feels like across several examples, instead of agonizing over whether a single joke is reversal or something else). Single-joke-through-all-passes is a fallback for the very first 1–2 annotations when you have nothing to batch against; once 3+ jokes are at the same pass-complete state, switch to batching.

**Routines are transcribed and segmented once, then processed as sequences.** When a transcription reveals a sustained bit (multiple laugh points on a shared premise, like a Seinfeld opener), segment it during Pass 1 into its component sub-jokes, assign a `routine_id` and sequential `position_in_routine`, and create individual joke stubs for each sub-joke. Subsequent passes operate on the sub-jokes individually. The routine file in `engine/routines/{routine_id}.yaml` holds the shared context (source, running_premise, ordered list of joke_ids).

The passes, and what each one does:

**Pass 1 — Transcription and routine segmentation (batched, low energy).** Clerical work with one judgment call. Get the exact text, source attribution, performer, performance context into stub files. For material that's a sustained bit rather than a single joke: segment it into sub-jokes at laugh points, create a routine file, and produce one stub per sub-joke with shared routine metadata. Batch 5–10 jokes per session. Updates `annotation_status.transcription: complete` on each resulting stub.

**Pass 2 — Silent read, decomposition (focused).** Read on the page. Populate joke-level layers: content, logic, structure, narrative. Focus on what the joke *is*. Batch 3–5 jokes per session where possible. Updates `annotation_status.decomposition: complete`.

Within Pass 2, fill fields in this order:

1. `logic.setup_expectation` and `logic.punchline_violation` (GLOSS). Write the joke's logic in prose first. These function as your reasoning trace.
2. `logic.pivot_locus` (logical / affective / both). The gloss fields usually make this obvious.
3. `joke.content.pivot_concept`. Which concept node does the turn anchor on? Null if purely affective.
4. `logic.incongruity_type.primary`. With the gloss in hand, consult `vocabularies/incongruity-types.yaml` and pick the value whose criterion matches your gloss. Default to primary-only (leave secondary empty); only add secondary values under the discipline described in §"Secondary incongruity types: when to populate" below.
5. `logic.incongruity_operates_on` sub-block. The structured companion to the gloss.
6. `joke.structure.primary_template`. Consult `vocabularies/templates.yaml`. This is informed by the logic but is its own question.
7. `joke.structure.subversions_applied`, `has_tag`, `tag_function`.
8. `joke.narrative.*` — callback references, routine position, etc.
9. `joke.content.concepts` and `specificity` last. Specificity sometimes only becomes clear once the structural move is named.

The gloss-before-structured ordering is the most important principle: writing the logic in prose first makes the structured classification almost mechanical. When the structured field resists, revisit the gloss — it's usually the gloss that's unsharp.

**Pass 3 — Aloud read, performance (sensory).** Read each joke aloud at least twice before committing any fields. Populate performance-level layers: delivery, affective (default register plus any trajectory anchored to structural events), voice (deviations from performer default), relational (positioning, audience implication, shared-experience dimensions). Focus on how the joke *goes*. Batch 3–5 jokes per session. Updates `annotation_status.performance: complete`.

Within Pass 3, fill fields in this order:

1. Read aloud twice, minimum.
2. `performance.delivery.cadence` and `pause_placement`. These are most directly observable from the aloud read.
3. `performance.affective.default_register` (valence, arousal). The "how did that sound" question.
4. `performance.affective.trajectory` if register shifts were audible. This is where aloud reading pays off.
5. `performance.voice.*` deviations from performer default.
6. `performance.relational.positioning`. Tends to need the affect read first.
7. `performance.relational.shared_experience` and `performed_relatability` fields.

**Pass 4 — Commutation test (analytical, deliberate).** Against each completed annotation, test each element independently: remove the pivot concept — does the joke still work? Remove the affect shift? Remove the tag? Populate `load_bearing_element` (as field_path), `removable_elements`, and `uncertain_elements`. If you can't cleanly identify which elements are load-bearing, the decomposition is incomplete; return to Pass 2 or 3. Additionally, if `incongruity_type.secondary` is populated, apply the commutation criterion to each entry: would removing this mechanism weaken the joke? If no, remove the entry. Batch several jokes per session. Updates `annotation_status.commutation: complete`.

**Pass 5 — Adversarial review (critical).** For each joke, try to break your own annotation. Propose the strongest alternative reading for non-obvious classifications; defend the current choice or revise. Capture counterarguments in the `adversarial` block. This pass benefits from batching because adjacent adversarial passes sharpen your skeptical eye. Updates `annotation_status.adversarial_review: complete`.

**Cross-cutting pass — Voice attribution (run weekly, not per-joke).** Across all completed annotations, tag each for portability to each roster member. Fast, bounded, low-cognitive-load. Updates `annotation_status.voice_attribution: complete`.

**Maintainer pass — Performer defaults.** When a property appears in 3+ jokes as an explicit "deviation from performer default" for the same performer, promote it to `engine/performers/{performer}.yaml` and remove from individual annotations. Done during weekly review.

### The two-stage capture rule (for Pass 2 and Pass 5)

During Pass 2, when classifying into structured fields (especially incongruity_type and primary_template), use two-stage capture:

**Stage 1 — Intuitive call.** Write your best guess into the structured field, plus the gloss fields (`setup_expectation`, `punchline_violation`) in your own words. Confidence is allowed to be low. The gloss fields are your reasoning trace — articulating the setup/punchline relationship often makes the structured classification obvious.

**Stage 2 — Definition check.** Open the vocabulary file for the field you just populated. Read the criterion and the `distinguished_from` block for your chosen value and its nearest neighbors. Ask: does your chosen value's criterion fit your gloss? Does a neighboring value's criterion fit better?

Three outcomes from Stage 2:

- **Definition confirms your call.** Commit. This is the normal case.
- **Definition reveals you misapplied it** (e.g., you called something reversal but the criterion says reversal requires a truth-value flip and your gloss describes a scope change). Revise to the correct value and log in the decision log: "revised from X to Y after re-reading Y's criterion." This is the legitimate use of checking your work.
- **No definition fits well.** Either your gloss isn't sharp enough (try Stage 1 again), or the vocabulary has a gap (log in `questions.md`, pick the closest value with a note, move on).

The assistant can help with Stage 2 but only in a specific way: it can *read the criterion back to you* and ask whether it fits your gloss. It cannot propose which value is correct. If the assistant proposes a value, that's a data leak — log in decision log. The rule is that your intuitive call in Stage 1 is authoritative for classification; the assistant is authoritative only for pointing out when you've misapplied a definition that's written down and checkable.

### Secondary incongruity types: when to populate

`incongruity_type` has `primary` (required, single-valued) and `secondary` (optional, multi-valued). Default to primary-only. Secondary is for the specific case where two mechanisms operate **simultaneously at the same pivot**, each doing distinct work.

**Three patterns that look like "multiple incongruity types" but aren't:**

1. **Uncertainty between values.** If you can't decide whether the mechanism is X or Y, that's one mechanism you can't identify — not two mechanisms. Pick the value you'd defend if pressed, log the alternative in `adversarial.counterarguments_considered` with why you rejected it, and set `adversarial.confidence: low`. Do **not** put both into primary + secondary; that encodes uncertainty as if it were layering and pollutes co-occurrence data.

2. **Mechanisms at different structural events.** If setup uses one mechanism and punchline uses another, you probably have two pivots, which means two jokes. This is a signal to segment into sub-jokes linked in a routine, not a signal to list multiple incongruity types.

3. **Plausible alternative readings.** If you can construct a reading of the joke under mechanism Y but the joke *also* works without Y — Y is a plausible lens, not an active mechanism — don't list Y as secondary. The test is the commutation criterion below.

**Secondary-use discipline (all three must hold):**

- **Simultaneity.** The mechanism operates at the same pivot as the primary, not at a different structural event.
- **Commutation weakening.** If you remove this mechanism (imagine the joke without it), does the joke become *weaker but still functional*? If yes, it's secondary. If removing kills the joke, it's primary, not secondary. If removal changes nothing, the mechanism isn't really operating — don't list it.
- **Independence.** The secondary mechanism is doing work the primary isn't doing. If you find yourself describing both as "the same kind of thing said differently," you've got one mechanism under two names.

**Expected frequency.** Most jokes have a clean single mechanism. Secondary should be populated in roughly **15% or fewer** of annotations in a healthy corpus. If you're populating secondary in more than 30% of jokes early on, the field is being over-used and the discipline above is not being applied. Weekly review tracks this ratio.

**Pass 4 verification.** During the commutation test, each secondary entry is checked by asking "would the joke be weaker without this mechanism being active?" Entries that fail get removed. This is the structural check that makes secondary genuinely useful rather than decorative.

### Passes are independent; don't chain them within a single joke

The discipline is keeping modes clean. Doing Pass 2 and Pass 3 back-to-back on the same joke lets the cadence you "hear" mid-transcription corrupt the silent-read decomposition, and vice versa. Separate passes into separate sessions (or at minimum, clear breaks between them), and batch across jokes within each pass.

A reasonable weekly rhythm: one transcription batch (produces stubs, including routine segmentation if any), two or three silent-read sessions (produces decomposed jokes in batches), two or three aloud-read sessions (produces performance annotations in batches), one commutation-test session, one adversarial-review session, one voice-attribution sweep. Order within the week is flexible; dependencies matter (Pass 4 requires Pass 2 and 3 complete for the joke).

---

## During-any-pass rules

Held separately from pass-specific work because these apply regardless of which pass you're in.

- **Vocabulary file open before any vocabulary-backed field is populated.** If you're filling `incongruity_type`, `vocabularies/incongruity-types.yaml` is visible. No exceptions. The vocabulary is externalized memory — trying to name values from memory guarantees you'll miss distinctions the file contains. This defends against the "I wouldn't have thought of mundane_as_monumental" failure mode.
- **Concepts vs. templates — don't conflate them.** "Concept" in the schema is a technical term scoped to the content layer: it means *what the joke is about* (parking garages, memory, airline food). "Template" means *how the joke operates* on its concepts (mundane_as_monumental, reversal, escalation). The test: could this be applied to many different subjects (template) or is it a subject that many different moves could be applied to (concept)? "Mundane_as_monumental" is a template because you can apply it to any trivial subject. "Parking garages" is a concept because you can reversal it, escalate it, anthropomorphize it, or treat it as mundane_as_monumental. If you catch yourself wanting to add an idea like "mundane_as_monumental" to `concepts`, it's a template and belongs in `structure.primary_template` instead.
- When the assistant asks a clarifying question, notice whether the question embeds a hypothesis. "What's the pivot?" is neutral. "Is the pivot the memory thing?" is not. If you notice the latter, answer the neutral version of the question instead and flag it in the decision log.
- If you're uncertain between two vocabulary values, pick one and add a note. Don't stall. Stalling means the schema under-specifies something and that's information for the changelog, not a reason to freeze.
- When fuzzy words come up ("kind of a callback," "sort of reversal"), force yourself to sharpen before committing to a field. Either it's a callback or it isn't. "Sort of" in notes is a signal the schema may need a partial/hybrid value.
- Don't mix passes mid-session. If you're doing Pass 3 and notice a structural issue that belongs in Pass 2, log it in the joke's notes and address it in the next Pass 2 session.

---

## Per-field verification guide

For each structured field, the question below is safe to ask the assistant once you've populated your intuitive call in Stage 1. The assistant's answer can only confirm, flag a definition mismatch, or say "the definition doesn't clearly decide this." It cannot propose a value. If it proposes one, log in decision log.

**Read the assistant's questions as neutral checks, not as suggestions.** The pattern is always: you state your call and your gloss, the assistant reads the relevant definition, the assistant asks whether the definition's criterion fits your gloss.

### Logic layer

- `setup_expectation` / `punchline_violation` (GLOSS). No verification needed — these are your reasoning, not classifications. The assistant should not comment on their content, only flag if they're missing.
- `pivot_locus`. Ask: "I called this {logical|affective|both}. Here's my gloss. Does the turn happen at the level of meaning (logical), emotional register (affective), or both?" The assistant reads back your gloss and asks whether the turn's locus matches.
- `pivot_concept`. Ask: "I named {concept} as the pivot concept. Does my gloss describe the turn as anchoring on that concept, or on something else?"
- `incongruity_type.primary`. Ask: "I classified this as {value}. The criterion for {value} is {X} and the distinguished_from for the nearest neighbor {Y} says {Z}. Does my gloss fit the {value} criterion, or does it fit {Y} better?" This is the most common place for definition mismatches; the two-stage capture is designed for this field in particular.
- `incongruity_type.secondary` (only if populated). Ask: "For each secondary mechanism I listed: does my gloss describe this mechanism as operating at the same pivot as the primary (simultaneity)? Would removing this mechanism weaken but not kill the joke (commutation)? Is this mechanism doing work the primary isn't already doing (independence)? Any 'no' means the entry should be removed." See §"Secondary incongruity types: when to populate".
- `incongruity_operates_on` sub-block. Ask: "Given my gloss, does the setup establish a norm, anomaly, category, or sequence? Does the punchline affirm, negate, redirect, literalize, figurize, or recategorize?" The assistant walks through each sub-field against the gloss.

### Structure layer

- `primary_template`. Ask: "I called this {value}. The criterion is {X}. Does my gloss describe a joke that does what {value}'s criterion requires? Is there a neighboring template whose criterion fits better?"
- `secondary_templates`. Ask: "Given my primary template choice, does my gloss also describe moves that fit any of these other templates? If so, which?"
- `subversions_applied`. Ask: "Does my gloss describe a move that breaks an expected structural pattern? If yes, at which structural event (setup, pivot, punchline, tag)? Which subversion value fits the move I described?"
- `has_tag` / `tag_function`. Ask: "Is there a line after the main punchline that extends the laugh? If yes, does it extend, reframe, undercut, or callback the punchline?"

### Content layer

- `primary_domain`. Ask: "Given the concepts in my gloss, which domains from `domains.yaml` cover them? Use multi-select if the joke spans multiple."
- `concepts`. Ask: "For each concept I named, is there an existing node in the registry that matches (exactly or via near-match)? If none exists, I need to create a new node — here are its domain and specificity; confirm the node_id is normalized."
- `pivot_concept`. See logic layer.
- `specificity.default_level`. Ask: "Given my gloss and concepts, what level of specificity (1–5) is the joke operating at? Check the anchor descriptions in `specificity.yaml`."
- `specificity.trajectory`. Ask: "Does the specificity change across the joke's structural events? Only populate if yes and if the shift is load-bearing (commutation test will confirm later). If so, record as list of {at, level} pairs."

### Narrative layer

- `callbacks_to`. Ask: "Does my gloss describe the joke as referencing a prior joke in the corpus? If so, which joke_ids?"
- `routine_id` / `position_in_routine`. Usually set in Pass 1; only populated here if segmentation was deferred.
- `position_in_set`. Ask: "In the context of this performance, is this joke an opener, mid-set, closer, or standalone?"

### Delivery layer (Pass 3)

- `cadence`. Ask: "Based on the aloud read, which cadence value from `cadence.yaml` fits? If no existing value fits, I need to create a new one with full definition block."
- `pause_placement`. Ask: "Where did I naturally pause when reading aloud? Which of the enumerated placements fit?"
- `repetition`. Ask: "Was there a phrase repeated for effect? Capture the phrase gloss, count, and which structural events it appeared at."
- `vocal_register_shifts`. Ask: "Did my voice shift mid-joke in a way that felt load-bearing? If yes, at which event and in which direction from the register-shifts vocabulary?"
- `estimated_duration_seconds`. No verification; direct observation.

### Voice layer (Pass 3)

- `persona_markers`. Ask: "Are there voice markers in this joke that deviate from the performer's default? Check `engine/performers/{performer}.yaml` — only list deviations."
- `signature_phrases`. GLOSS; no verification.
- `register`. Ask: "Does this joke's voice register match the performer default, or deviate? If deviate, which value from `registers.yaml`?"
- `editorializes.present` / `editorializes.kind`. Ask: "Does the joke pass judgment on its content? If yes, is the editorialization strong (explicit judgment), weak (tonal only), or ironized (performing the opposite of sincere judgment)?"

### Affective layer (Pass 3)

- `default_register.valence` / `arousal`. Ask: "Where on each axis does this joke sit? Check the anchor descriptions in `affect-axes.yaml`. Orthogonal axes — don't collapse them."
- `trajectory`. Ask: "Does the affective register shift across structural events? Only populate if yes and if the shift is load-bearing."
- `shifts_are_load_bearing`. Ask: "If I imagine the joke without the affective shift, does it still work the same? If yes, shifts aren't load-bearing."
- `deviates_from_performer_default`. Ask: "Does the joke's affect match the performer's default, or is this a deviation?"

### Relational layer (Pass 3)

- `positioning.default`. Ask: "Is the comedian positioned as above, below, with, or lateral to the audience for this joke? Check `positioning.yaml` criteria."
- `positioning.trajectory`. Only populate if positioning shifts mid-joke.
- `audience_implication`. Ask: "Does the joke treat the audience as co-observer, target, accomplice, or witness?"
- `vulnerability.personal_exposure` / `emotional_risk`. Ask: "On a 0–5 scale, how much of self is revealed (exposure)? How affected is the performer by what's revealed (risk)? Orthogonal — don't collapse."
- `shared_experience.required` / `universality` / `comprehensibility_without_experience`. Ask: "Does the joke require the audience to have had the experience? How universal is the experience? Can someone who hasn't had it still find it funny (0–5)?"
- `performed_relatability.present` / `intensity`. Ask: "Does the joke perform a relatability gesture ('you know when you...') for an experience that might not actually be shared? If yes, what intensity (0–1)?"

### Meta layer

- `comments_on_form`. Ask: "Does the joke acknowledge the form it's in? At the joke level (written), the performance level, both, or not at all?"
- `breaks_fourth_wall`. Same structure.

### Analysis

- `commutation.load_bearing_element.field_path`. Ask: "Walking through each populated element, which one — when removed — kills the joke? Give the field path."
- `commutation.removable_elements`. Ask: "Which elements can be removed without killing the joke? List field paths."
- `commutation.uncertain_elements`. Ask: "For which elements was the commutation test ambiguous?"
- `voice_portability.{performer}`. Ask: "Could {performer} deliver this joke in their own voice? Portable, not portable, or portable with adaptation?"
- `adversarial.counterarguments_considered`. Each entry: "What's a defensible alternative reading of my classifications? Why did I reject it?"
- `adversarial.confidence`. Low / medium / high — how defensible is the annotation under scrutiny?

---

## Post-session review (5 minutes, after every session)

Skim the session transcript. Look for exactly three things:

1. **LLM proposals you agreed with.** If the assistant proposed a value and you said "yeah, sure" without independent reasoning, log it in `working/decision-log.md` with the joke ID and the proposal. This is the most corrosive failure mode; catch it early.
2. **Classifications you couldn't justify.** Any field where your reasoning was "felt right" rather than articulated. Log these too. If the same field keeps appearing in the log, the schema under-specifies it.
3. **Schema gaps.** Anything that didn't fit. Log in `working/questions.md` with enough context to recover later.

Save YAML outputs to `annotations/` if not already there. Update `annotation_status` for each joke touched in the session. Do not review substance yet — that's for weekly review.

---

## Weekly review (20 minutes, once per week)

Once a week, walk through these files in order:

**`working/questions.md`.** Any question that has appeared three or more times, or any single question that's blocking annotation, deserves attention this week. Either resolve it (by pulling in relevant literature, running a focused sub-analysis, or updating the schema) or explicitly defer it with a note. Stale questions are worse than resolved ones.

**`working/decision-log.md`.** Look for patterns. If the same kind of judgment keeps appearing — same field, same ambiguity, same kind of LLM proposal — it's a signal the schema or the system prompt needs adjustment, not a signal that you need to try harder.

**`working/schema-changelog.md`.** Review what changed this week. For each change, ask: did this change invalidate prior annotations? If yes, flag the affected annotation IDs for re-review. Schema drift is real and catches up with you.

**Field-usage ratio check.** After the first 30 annotations, and every 20 annotations thereafter, run a quick count: for each field in the schema, how many annotations have a meaningful (non-default, non-null) value? Record in `working/field-usage.md` as a table with field name, annotation count using it, and total annotation count. Fields below roughly 20% usage are candidates for removal or merger — they're either overfit to rare cases or redundant with fields that carry similar information. Fields at 100% that always take the same value are also suspect; they may not be discriminating anything. Log candidates here; act on them only after two consecutive checks confirm the pattern.

**Secondary incongruity usage check.** Specifically watch the rate at which `incongruity_type.secondary` is populated. Target is roughly ≤15% of annotations; >30% suggests the field is being over-used and the simultaneity/commutation/independence discipline is slipping. If over-used, re-read §"Secondary incongruity types: when to populate" and spot-check the last 5 secondary populations against the three-part discipline.

**A re-annotation spot-check.** Pick one annotation from 1–2 weeks ago and re-annotate it cold, without looking at the prior version. Compare. High agreement means the schema and your application of it are stable. Low agreement means either the schema has evolved (fine, update the old annotation) or your intuitions are drifting (not fine, needs attention).

**Performer default promotion.** Scan recent annotations for patterns that keep appearing as "deviations from performer default" but aren't actually deviations — they're showing up so often they should *be* the default. If a property has appeared in 3+ jokes as an explicit performance-level value for the same performer, consider promoting it to `engine/performers/{performer}.yaml` and removing it from the individual annotations. Log in schema-changelog.

**Voice attribution sweep.** Run the cross-cutting voice-attribution pass on all annotations completed this week. For each, mark portability to each roster member (portable / not-portable / portable-with-adaptation). Updates `annotation_status.voice_attribution` on each joke.

**Concept dimension completion.** For each concept node created this week with incomplete dimensions (only node_id, gloss, domain, specificity filled in), populate the remaining dimensions (register, valence, arousal, physicality, typicality, era) based on how the concept has been used across the week's jokes. Dimensions based on observed usage are more accurate than dimensions set at concept-creation time.

**System prompt behavior check.** Skim one session transcript from this week. Is the assistant following its constraints, or has it started drifting into proposals? If the latter, update the system prompt (see below).

---

## System prompt review

The annotation assistant's system prompt lives at `engine/system-prompt.md`. It's a living document.

**When to update:**
- When transcript review shows the assistant proposing content (tighten the relevant rule or add an example of the failure)
- When the schema changes (the schema section of the prompt needs to match)
- When controlled vocabularies change (update the reference section)
- When you find yourself repeatedly reminding the assistant of something mid-session (add it to the prompt)

**When not to update:**
- Mid-session. Finish the session, log the issue, update during weekly review.
- In response to a single instance of a failure mode. Wait for a pattern before changing the prompt; over-tuning on one bad session makes the prompt worse.

Keep a revision history in comments at the top of the system prompt file. When you revert a change, note why.

---

## Schema maintenance

The schema lives at `engine/schema.yaml`. Controlled vocabularies live at `engine/vocabularies/`.

**Before adding or revising a field, run the structural question-set:**

1. Can this field take more than one simultaneous value in a single joke? If yes, multi-valued or split.
2. Does the value meaningfully change across the duration of the joke? If yes, trajectory representation rather than a single value.
3. Are the values genuinely ordered, or is a scale being used because it's easy? If not ordered, enumerated kinds.
4. Do the "absent" cases and the "low intensity" cases mean different things? If yes, presence + intensity rather than a single scale.
5. Does the field's meaning change depending on the value of another field? If yes, split into context-specific sub-fields or encode the dependency.

Answer these before committing the field shape. Most field-design errors come from skipping this step.

**Adding a field.** Allowed any time, but every addition requires a note in `schema-changelog.md` explaining why, plus the answers to the five questions above. If the reason is "one joke needed it," wait until at least two more jokes need it before committing the change.

**Removing a field.** Only during weekly review, and only after field-usage ratio has flagged it for two consecutive checks. Log in changelog with the usage numbers that justified removal.

**Adding a vocabulary value.** Every new vocabulary value requires a full definition block per `vocabularies/README.md`: a criterion (prescriptive, not descriptive), a positive example (real joke), a near-miss negative example (joke that looks like this value but is actually a neighbor — name which neighbor), and `distinguished_from` entries for each nearest neighbor with a decision procedure. Values without this full definition are not allowed — they produce drift immediately. If you can't construct a near-miss negative example, the value may not be distinct enough to earn its place; consider whether it's really a sub-type or feature of an existing value. Log in changelog.

**Adding a concept node.** When a joke references a concept not yet in `engine/concepts/_registry.yaml`, create the node with node_id (normalized: lowercase, underscores, plural for countable concepts), gloss, and at minimum a domain and specificity dimension. Other dimensions (register, valence, arousal, physicality, typicality, era) can be filled in during weekly review if not immediately obvious. Check the registry before creating — a near-match ("parking_garage" vs existing "parking_garages") should either reuse the existing node or be added as an alias, not as a new node. Log in changelog.

**Renaming or merging values.** High-cost operation. Requires updating every existing annotation that used the old value (for vocabulary values) or every annotation referencing the old node_id (for concepts). Do this during weekly review, not mid-session, and only after the confusion or overlap has appeared at least three times.

---

## The annotation assistant system prompt

Maintained at `engine/system-prompt.md`. Current version below; copy to that file and evolve there.

```
You are an annotation assistant helping a researcher decompose jokes into a
structured schema for a comedy-generation project. Your role is to capture the
researcher's analysis into YAML, not to perform analysis yourself. You are a
stenographer with domain knowledge of the schema, not a collaborator on the
substance.

## Your rules

1. The researcher's judgments are authoritative. Never propose content values
   (what the pivot is, what template applies, what voice moves are present).
   If they haven't specified a field, ask them about it directly — do not
   suggest an answer.

2. Ask clarifying questions only to:
   - Disambiguate which field something belongs in ("is that a voice move or
     a structural move?")
   - Resolve controlled-vocabulary choices ("you said 'twist' — in the schema
     that could be 'reversal' or 'reframe'; which fits?")
   - Prompt for required fields not yet filled ("you haven't said anything
     about the relational layer yet — what's the positioning?")
   - Surface potential inconsistencies with prior annotations the researcher
     has shared in this session ("earlier you classified a similar structure
     as X; is this the same or different?")

3. Never ask questions that embed your own hypothesis. Bad: "would you say
   the pivot is the memory of location?" Good: "what's the pivot for this one?"

4. When the researcher articulates something fuzzy, reflect it back neutrally
   and ask them to sharpen it. Do not sharpen it for them.

5. Output current YAML state after every meaningful update, so the researcher
   can see what's captured. Mark fields as {UNSPECIFIED} when not yet filled.

6. Never add values not drawn from the controlled vocabularies the researcher
   provides. If they use a term outside the vocabulary, do not accept it
   silently — ask whether to map it to an existing value or to add it as a
   new vocabulary value. Adding a new vocabulary value requires the researcher
   to provide: a criterion, a positive example, a near-miss negative example,
   and distinguished_from entries for nearest neighbors. If they can't provide
   all four, the value is not added — propose using an existing value instead
   and note the imperfect fit in the joke's notes field.

6a. For concepts: before accepting a concept reference, check the concept
    registry. If the term matches an existing node_id (exactly or near-match
    like plural/singular variation), reference the existing node. If it's
    genuinely new, create a registry entry with node_id (normalized), gloss,
    and at minimum domain and specificity dimensions.

7. If the researcher explicitly asks for your opinion on something substantive
   — "what do you think the pivot is?" — decline and redirect: "I shouldn't
   propose content; what's your read?"

8. If the researcher seems stuck, offer procedural help (suggest a layer to
   examine next, re-read the joke aloud, check the commutation test) but
   never propose specific values.

9. At session start, ask the researcher which pass they're doing (1 transcription /
   2 silent decomposition / 3 aloud performance / 4 commutation / 5 adversarial).
   Only ask about fields belonging to that pass. If the researcher brings up a
   field that belongs to a different pass, note it in the joke's free-text notes
   and redirect: "that sounds like a pass 3 concern; want me to note it for later
   or are you switching passes?"

10. For each joke worked on, read the existing annotation file if one exists
    (from prior passes) before starting. Do not overwrite fields populated in
    prior passes without explicit confirmation.

11. At session end, update `annotation_status` on each joke touched, marking
    the completed pass. Output final YAML for each joke.

12. Pass-specific prompts at session start:
    - Pass 1: ask for text, source, performer, performance context
    - Pass 2: ask for content, logic, structure, narrative layer fields
    - Pass 3: ask researcher to read aloud first; then ask about performance,
      affective (with trajectory if present), voice deviations, relational
    - Pass 4: walk through each element in the annotation and ask what happens
      if removed; capture load_bearing_element and removable_elements
    - Pass 5: play devil's advocate on the existing annotation's choices;
      capture counterarguments in notes; only commit revisions the researcher
      actively endorses

13. **Two-stage capture enforcement.** The researcher populates structured
    fields in two stages: Stage 1 is an intuitive call written into the field,
    Stage 2 is a definition check. Your role in Stage 2 is strictly as a
    definition-checker:
    - You read the criterion and distinguished_from block for the value the
      researcher chose, and for its nearest neighbors.
    - You ask whether the researcher's gloss matches the chosen value's
      criterion, or whether a neighboring value's criterion fits better.
    - You never propose which value is correct. You only check whether the
      researcher's reasoning matches the written definition of the value
      they already chose.
    - If the researcher's gloss clearly mismatches the chosen value's
      criterion, flag the mismatch and ask them to either revise the
      classification or revise the gloss. Do not propose the correct value;
      that's their judgment.
    - If no definition clearly fits the gloss, tell the researcher the
      vocabulary may have a gap. They log in questions.md; you don't propose
      a new value.

14. **Per-field verification answers.** When the researcher asks you to verify
    a field, follow the pattern in protocols.md "Per-field verification
    guide." Your answer has four possible shapes:
    - "Definition {X}'s criterion says {exact text}. Your gloss describes
      {paraphrase of gloss}. These match." — confirms the call.
    - "Definition {X}'s criterion says {exact text}, but {Y}'s criterion says
      {exact text}. Your gloss describes {paraphrase}. The criterion for {Y}
      fits more closely. Revise or defend?" — flags a mismatch.
    - "Definition {X}'s criterion says {exact text}. Your gloss describes
      {paraphrase}. I can't tell whether these match — the gloss may be
      underspecified." — asks for sharpening.
    - "None of the existing definitions clearly fit your gloss. This is a
      vocabulary gap. Log in questions.md?" — flags the gap.
    You do NOT propose values. You do NOT recommend between options. You read
    definitions and ask whether they fit.

## Schema

[Reference engine/schema.yaml]

## Controlled vocabularies

[Reference engine/vocabularies/*.yaml]
```

---

## Anti-patterns to watch for

Things that sound like progress but aren't. Flag in decision log if you notice yourself doing any of these.

**Annotation velocity as a goal.** Fast annotation is good when it reflects a stable schema. Fast annotation is bad when it reflects skipping layers or accepting assistant proposals to save time.

**Schema expansion as a habit.** Every missing-fit is not a new field. Some are signals that existing fields need sharper definitions. Default to tightening before adding.

**Treating the weekly review as overhead.** The weekly review is where most of the actual learning happens. Annotation is data collection; review is the analysis. Skipping review means annotating blind.

**Smoothing transcripts.** When a session went poorly, the urge to clean up the decision log and questions file before committing is strong. Don't. The messy version is the honest version, and the honest version is what you need for the next weekly review.
