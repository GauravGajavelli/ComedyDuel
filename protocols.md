# Comedy Duel — Operational Protocols

*Companion to spec.md. This document holds procedures; the spec holds architecture.*

This file is for you-in-the-moment, about to start an annotation session or about to review the week's work. It's deliberately short. Each protocol is an actual checklist you read before the relevant work, not background reading.

If this document grows past ten minutes of total reading time, it has become too much to be useful. Prune rather than expand.

---

## Pre-session checklist (30 seconds, before every annotation session)

Read these six lines before starting. They prime attention; don't rely on memory during the session.

1. Which pass am I doing? (1: transcription / 2: silent decomposition / 3: aloud performance / 4: commutation / 5: adversarial). Stay in that mode.
2. The assistant proposes nothing. If it suggests a value and I agree, that's a data leak.
3. Log anything I can't justify in `working/decision-log.md` with the joke ID.
4. If something belongs in a different pass, log it in notes and address it later. Don't context-switch.
5. If the schema doesn't fit something, note it in `working/questions.md`. Don't force-fit.
6. Update `annotation_status` at session end for every joke touched.

---

## Annotation workflow: the multi-pass model

Annotation is not a single activity. Five distinct passes, each in a different mental mode, each operating on a different subset of the schema. Running them separately costs less total effort than one "complete" pass because each pass runs in a narrow mode it can sustain without fatigue. Single-pass annotation is high-switching-cost; multi-pass is low-switching-cost done in batches aligned with available attention.

The passes, and what each one does:

**Pass 1 — Transcription (batched, low energy).** Clerical. Get the exact text, source attribution, performer, performance context (specific show/special if identifiable) into a stub file. No analysis. Batch 5–10 jokes in a sitting when attention is mediocre. Updates `annotation_status.transcription: complete`.

**Pass 2 — Silent read, decomposition (focused).** Read on the page. Populate joke-level layers only: content (domain, concepts, pivot, specificity), logic (setup expectation, punchline violation, incongruity type, pivot_locus), structure (template, subversions, tags), narrative (callbacks, position in set). Focus on what the joke *is*. Updates `annotation_status.decomposition: complete`.

**Pass 3 — Aloud read, performance (sensory).** Read the joke aloud at least twice before committing any fields. Populate performance-level layers: performance (cadence, pauses, repetition, duration), affective (default register plus any trajectory anchored to structural events), voice (deviations from the performer's default — see split 4), relational (positioning, audience implication, shared-experience dimensions). Focus on how the joke *goes*. Updates `annotation_status.performance: complete`.

**Pass 4 — Commutation test (analytical, deliberate).** Do not combine with Pass 2 or 3. Against the completed annotation, test each element independently: remove the pivot concept — does the joke still work? Remove the affect shift — does it still land? Remove the tag? Populate `load_bearing_element` and `removable_elements`. If you can't cleanly identify which elements are load-bearing, the decomposition is incomplete; return to Pass 2 or 3. Updates `annotation_status.commutation: complete`.

**Pass 5 — Adversarial review (critical).** Try to break your own annotation. Could someone read this joke and argue for a different pivot? Is the template choice the only defensible one? Log counterarguments in the annotation's `notes` field. Commit only if you can defend the choice. If you can't, either revise the annotation or log the ambiguity in `working/questions.md` and move on with the best guess. Updates `annotation_status.adversarial_review: complete`.

**Cross-cutting pass — Voice attribution (run weekly, not per-joke).** Separate pass across all completed annotations: for each roster member (Mort, Cece), review jokes not yet tagged for that performer and mark portable/not-portable/with-adaptation. Fast, bounded, low-cognitive-load. Updates `annotation_status.voice_attribution: complete`.

**Maintainer pass — Performer defaults.** Voice-level facts (Mort's default affect, his editorialization policy, his characteristic sentence shapes) live in `engine/performers/mort.yaml`, not in per-joke annotations. Per-joke performance annotation records *deviations from the performer's default*. When you notice a pattern across 3+ jokes that should be part of a performer's default, promote it to the performer file and remove it from the individual annotations. This is done during weekly review.

### Passes are independent; don't chain them in one session

The discipline is keeping modes clean. Doing Pass 2 and Pass 3 back-to-back on the same joke lets the cadence you "hear" mid-transcription corrupt the silent-read decomposition, and vice versa. Separate sessions, or at minimum a clear break between them.

A reasonable weekly rhythm: one transcription batch (produces stubs), two or three silent-read sessions (produces decomposed jokes), two or three aloud-read sessions (produces performance annotations), one commutation-test session, one adversarial-review session, one voice-attribution sweep. Order within the week is flexible; dependencies matter (Pass 4 requires Pass 2 and 3 complete for the joke).

---

## During-any-pass rules

Held separately from pass-specific work because these apply regardless of which pass you're in.

- When the assistant asks a clarifying question, notice whether the question embeds a hypothesis. "What's the pivot?" is neutral. "Is the pivot the memory thing?" is not. If you notice the latter, answer the neutral version of the question instead and flag it in the decision log.
- If you're uncertain between two vocabulary values, pick one and add a note. Don't stall. Stalling means the schema under-specifies something and that's information for the changelog, not a reason to freeze.
- When fuzzy words come up ("kind of a callback," "sort of reversal"), force yourself to sharpen before committing to a field. Either it's a callback or it isn't. "Sort of" in notes is a signal the schema may need a partial/hybrid value.
- Don't mix passes mid-session. If you're doing Pass 3 and notice a structural issue that belongs in Pass 2, log it in the joke's notes and address it in the next Pass 2 session.

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
