# New Episode Annotation Prompt

Paste this into a new Claude Code session to annotate episodes that haven't been annotated yet.

---

## Instruction to paste:

Annotate Seinfeld opening monologues for episodes that don't yet have annotations in `annotations/`. Follow the v0.9 schema.

**Before doing anything, read these files in order:**
1. `engine/schema.yaml` — the annotation schema (v0.9). Read the "Architectural levels" section — it defines what goes where.
2. `engine/vocabularies/pivot-mechanisms.yaml` — 6 operations + 4 modifiers (read the tests for each operation)
3. `engine/vocabularies/templates.yaml` — 6 templates: mundane_as_monumental, monumental_as_mundane, bare_observation, escalation, reductio, comparison
4. `engine/vocabularies/positioning.yaml` — 4 positioning values
5. `working/scaling-path.md` — the full annotation workflow including the agent prompt template
6. `working/questions.md` — known open issues to watch for

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
Manually identify the opening monologue boundaries in each new raw script. The monologue starts at `[Setting: Night club]` or `[Scene: Comedy club]` and ends at the next non-comedy scene transition. Some episodes (like The Phone Message) use `Jerry's opening monologue:` instead. Some episodes have no opening monologue — skip those.

**Annotate in sub-batches of 5 episodes using parallel agents.**

For each agent, use the prompt template from `working/scaling-path.md` (the "Agent prompt template" section). Before launching, read the CURRENT vocabulary files and insert their values into the template's placeholders — do not hardcode values from memory.

Each agent produces a complete v0.9 annotation with these fields:
1. setup_expectation + punchline_violation (GLOSS)
2. pivot_locus
3. pivot_concept
4. pivot_mechanism: operation + reading_switch + scale_shift + wordplay
5. setup_frame (6 values)
6. primary_template (6 values — if joke anthropomorphizes, that's content_moves not template)
7. act_out: character_type + register_gap (character_register is Pass 3)
8. subversions: structural_refusal | meta_structural | specificity_subversion ONLY
9. tag_operation: extends | reframes | undercuts
10. joke.relational: positioning, audience_implication, shared_experience, performed_relatability.present
11. joke.narrative: callbacks, routine position, tag_callbacks_to, anti_callback
12. difficulties + vocabulary gaps

**After agents complete:**
1. Update `AGENT_MAP` in `engine/extract_annotations.py` with the new agent IDs
2. Run `python3 engine/extract_annotations.py` to persist to disk
3. Validate: `python3 -c "import yaml, glob; [yaml.safe_load(open(f)) for f in glob.glob('annotations/*.yaml')]"`
4. Produce a sub-batch synthesis: operation distribution, template distribution, setup_frame distribution, any new vocabulary gaps
5. Update gap tallies in `working/questions.md`

**Key things to watch for (from prior batches):**
- scale_shift was at 47% non-none in batch 2. Apply the independence test strictly: "could the operation work without the scale change?" If the joke dies, set scale_shift to none.
- establishes_premise was at 38%. Check whether any should really be establishes_convention.
- reinterpretation/articulation boundary: use the frame-dependency test. "Is the OBSERVATION the joke, or is the ANGLE on the observation the joke?"
- Seinfeld has almost no wordplay — wordplay modifier will almost always be none.
- The laugh-point count should be approximately 3-6 per episode opening. If an agent finds significantly more or fewer, the segmentation may be off.
