# New Episode Annotation Prompt

Paste this into a new Claude Code session to annotate episodes that haven't been annotated yet.

---

## Instruction to paste:

Annotate Seinfeld opening monologues for episodes that don't yet have annotations in `annotations/`. Follow the v0.9.2 schema.

**Before doing anything, read these files in order:**
1. `engine/schema.yaml` — the annotation schema (v0.9.2). Read the "Architectural levels" and "Reproducibility" sections.
2. `engine/vocabularies/pivot-mechanisms.yaml` — 6 operations + 4 modifiers (read the tests for each operation)
3. `engine/vocabularies/templates.yaml` — 6 templates: mundane_as_monumental, monumental_as_mundane, bare_observation, escalation, reductio, comparison
4. `engine/vocabularies/positioning.yaml` — 4 positioning values
5. `engine/concepts/_registry.yaml` — concept registry with aliases. Agents must use node_ids from here, not ad-hoc strings.
6. `working/scaling-path.md` — the full annotation workflow including the agent prompt template
7. `working/questions.md` — known open issues to watch for

**Check what's already annotated:**
```
ls annotations/*.yaml
```
Only annotate episodes NOT already in that directory.

**Scrape new episodes if needed:**
Edit `engine/scrape_seinfeld.py` to select the desired episode range (`targets = selected[START:END]`), then run:
```
python3 engine/scrape_seinfeld.py
```

**IMPORTANT: Do NOT read the raw script files yourself. Let the subagents read them.** Some script files trigger content filtering when read by the parent session. Each subagent should read its own episode's script file directly and identify the monologue boundaries itself.

**Annotate in sub-batches of 5 episodes using parallel agents.**

Each agent's prompt should instruct it to:
1. Read the schema and vocabulary files itself (list the file paths)
2. Read the concept registry (`engine/concepts/_registry.yaml`) and use node_ids from it
3. Read its assigned raw script file from `engine/raw_scripts/` directly
4. Identify the opening monologue boundaries (starts at `[Setting: Night club]` or `[Scene: Comedy club]` or `Jerry's opening monologue:`, ends at next scene transition)
5. If no opening monologue exists, report that and stop
6. Annotate following the v0.9.2 field order
7. Write the annotation to `annotations/` directly

**Context load optimization:** Each subagent reads ~50-70K tokens of reference
files (schema + 3 vocabularies + registry + script). On Opus 4.6 with 1M
context this is ~6% of the window — not a bottleneck. To reduce redundant
reads, inline the key vocabulary values directly in the agent prompt (operation
tests, template names, setup_frame values) rather than having each agent read
the full files independently. The agent prompt template below does this.

**Agent prompt structure** (do NOT paste transcript text — give file paths):

```
You are performing a Pass 2 annotation on a Seinfeld opening monologue.

READ THESE FILES FIRST (in order):
1. /Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/schema.yaml
2. /Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/vocabularies/pivot-mechanisms.yaml
3. /Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/vocabularies/templates.yaml
4. /Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/concepts/_registry.yaml

THEN read the raw script at:
/Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/raw_scripts/[FILENAME].txt
IMPORTANT: Read ONLY the first 200 lines (use offset: 0, limit: 200).
The opening monologue is always in this range. Reading the full script
may trigger content filtering on later sitcom scenes.

Identify the opening monologue (starts at [Setting: Night club] or
[Scene: Comedy club] or "Jerry's opening monologue:", ends at next
scene transition). If no opening monologue exists, report that and stop.

For concepts: look up the concept registry FIRST. Use existing node_ids
where they match. If a concept is genuinely new, use a normalized string
(lowercase, underscores). Do NOT use mechanism descriptions (absurdity,
comparison, anticipation) as concepts — those belong in structural fields.

Apply the STRICT scale_shift test: "Could I SWAP the direction
(expansion ↔ contraction) while keeping the same operation?" If
swapping is inconceivable, set scale_shift to none.

Write the complete annotation to:
/Users/gauravgajavelli/Documents/GitHub/ComedyDuel/annotations/[EPISODE_ID]_opening_pass2.yaml

## FIELD ORDER (schema v0.9.2)
1. setup_expectation (GLOSS — reasoning trace)
2. punchline_violation (GLOSS)
3. pivot_locus: logical | affective | both
4. pivot_concept
5. pivot_mechanism.operation — run the TEST, write down the artifact
6. pivot_mechanism.operation_alternative — if two operations produced
   plausible artifacts, record the runner-up. null if one test clearly won.
   Set confidence to medium or low when populated.
7. pivot_mechanism.reading_switch: none | figurative_to_literal | literal_to_figurative
8. pivot_mechanism.scale_shift: none | expansion | contraction
9. pivot_mechanism.wordplay: none | phonemic_pair | portmanteau | collocation_disruption
10. setup_frame: establishes_convention | establishes_behavior |
    establishes_expectation | establishes_premise | establishes_anomaly |
    establishes_sequence
11. primary_template: mundane_as_monumental | monumental_as_mundane |
    bare_observation | escalation | reductio | comparison
    NOTE: if joke anthropomorphizes, put that in content_moves, not template
12. act_out: present? character_type + register_gap (NOT character_register)
13. subversions: structural_refusal | meta_structural | specificity_subversion ONLY
14. tag_operation: extends | reframes | undercuts
15. joke.relational: positioning, audience_implication, shared_experience,
    performed_relatability.present
16. difficulties (tag ambiguities, vocabulary gaps, forced choices)
```

**After agents complete:**
1. Verify annotation files exist: `ls annotations/*.yaml`
2. YAML validation: `python3 -c "import yaml, glob; [yaml.safe_load(open(f)) for f in glob.glob('annotations/*.yaml')]"`
3. **Reproducibility validation:** `python3 engine/validate_annotations.py`
   - Checks: concepts resolve to registry, no mechanism descriptions as concepts, valid operations/templates/setup_frames, no removed subversion values in wrong locations, operation_alternative validity
   - Fix any ERRORS before proceeding. WARNINGS (alias usage, unresolved concepts) should be addressed but don't block.
4. Produce a sub-batch synthesis: operation distribution, template distribution, setup_frame distribution, scale_shift non-none rate, operation_alternative non-null rate, any new vocabulary gaps
5. Update gap tallies in `working/questions.md`

**Key things to watch for (from prior batches, 65 LPs across 14 episodes):**
- scale_shift non-none rate was 30% after strict swap test (down from 47%). If above 35%, the test may need tightening.
- establishes_premise was at 36%. Use the decision procedure: "Would the audience hold this belief WITHOUT the comedian stating it?" Yes → convention. No → premise.
- reinterpretation/articulation boundary: "Is the OBSERVATION the joke, or is the ANGLE on the observation the joke?" When both operations produce plausible test artifacts, record the runner-up in operation_alternative.
- operation_alternative non-null rate should be ~15-35% for observational comedy. Below 15% = suppressing genuine ambiguity. Above 35% = vocabulary boundaries need sharpening.
- Seinfeld has almost no wordplay — wordplay modifier will almost always be none.
- Concepts must resolve to registry node_ids or be flagged as genuinely new. Mechanism descriptions as concepts are a reproducibility failure.
- Laugh-point count should be approximately 3-7 per episode opening.
