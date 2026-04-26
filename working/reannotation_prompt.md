# Re-annotation Prompt

Paste this into a new Claude Code session to re-annotate existing episodes under the current schema version.

---

## Instruction to paste:

Re-annotate all Seinfeld opening monologues that already have annotations in `annotations/`. The existing annotations may be under an older schema version and need updating to the current schema.

**Before doing anything, read these files in order:**
1. `engine/schema.yaml` — read the version number, the "Architectural levels" section, and the "Reproducibility" section
2. `engine/vocabularies/pivot-mechanisms.yaml` — 6 operations + 4 modifiers
3. `engine/vocabularies/templates.yaml` — current template list
4. `engine/vocabularies/positioning.yaml` — 4 positioning values
5. `engine/concepts/_registry.yaml` — concept registry with aliases
6. `working/scaling-path.md` — the agent prompt template and field order
7. `working/questions.md` — known open issues

**Check what needs re-annotation:**
```
ls annotations/*.yaml
```

**IMPORTANT: Do NOT read the raw script files yourself. Let the subagents read them.** Some script files trigger content filtering when read by the parent session. Each subagent reads its own files directly.

**Back up existing annotations first:**
```
cp -r annotations/ annotations_backup_$(date +%Y%m%d)/
```

**Launch agents in sub-batches of 5 episodes.**

Each agent's prompt should instruct it to:
1. Read the schema, vocabulary files, and concept registry itself (give file paths)
2. Read the EXISTING annotation file for its assigned episode from `annotations/`
3. Read the raw script from `engine/raw_scripts/` to access the original transcript
4. Produce a FRESH annotation under the current schema — not a patch, a full rewrite
5. Write the new annotation to `annotations/`, overwriting the old one

**Agent prompt structure** (give file paths, NOT file contents):

```
You are re-annotating a Seinfeld opening monologue under the current
schema version.

READ THESE FILES FIRST (in order):
1. /Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/schema.yaml
2. /Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/vocabularies/pivot-mechanisms.yaml
3. /Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/vocabularies/templates.yaml
4. /Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/concepts/_registry.yaml

THEN read the existing annotation at:
/Users/gauravgajavelli/Documents/GitHub/ComedyDuel/annotations/[EPISODE_ID]_opening_pass2.yaml

AND the raw script at:
/Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/raw_scripts/[FILENAME].txt
IMPORTANT: Read ONLY the first 200 lines (use offset: 0, limit: 200).
The opening monologue is always in this range. Reading the full script
may trigger content filtering on later sitcom scenes.

Identify the opening monologue from the raw script (starts at
[Setting: Night club] or [Scene: Comedy club] or "Jerry's opening
monologue:", ends at next scene transition).

Produce a FRESH annotation — do not patch the old one. Use the current
schema structure. Key requirements:

- Concepts: use node_ids from the registry. Check aliases. Do NOT use
  mechanism descriptions (absurdity, comparison, etc.) as concepts.
- scale_shift STRICT test: "Could I SWAP direction (expansion ↔
  contraction) while keeping the same operation?" If inconceivable → none.
- operation_alternative (v0.9.2): when two operations produce plausible
  test artifacts, record the runner-up. null if one test clearly won.
  Set confidence to medium or low when populated. Expected non-null
  rate: ~15-35% for observational comedy.
- setup_frame: "Would the audience hold this belief WITHOUT the comedian
  stating it?" Yes → convention. No → premise.
- Templates: 6 values (mundane_as_monumental, monumental_as_mundane,
  bare_observation, escalation, reductio, comparison). If joke
  anthropomorphizes, that's content_moves, not template.
- act_out: character_type + register_gap in joke.structure.
  character_register goes in performance layer, not here.
- Subversions: structural_refusal | meta_structural | specificity_subversion
  ONLY. register_break → performance. anti_callback → narrative.
- joke.relational: positioning, audience_implication, shared_experience,
  performed_relatability.present (these are JOKE properties).

Write the complete annotation to:
/Users/gauravgajavelli/Documents/GitHub/ComedyDuel/annotations/[EPISODE_ID]_opening_pass2.yaml

FIELD ORDER (schema v0.9.2):
1. setup_expectation (GLOSS)
2. punchline_violation (GLOSS)
3. pivot_locus: logical | affective | both
4. pivot_concept
5. pivot_mechanism.operation — run the TEST, write artifact
6. pivot_mechanism.operation_alternative — runner-up or null
7. pivot_mechanism.reading_switch: none | figurative_to_literal | literal_to_figurative
8. pivot_mechanism.scale_shift: none | expansion | contraction
9. pivot_mechanism.wordplay: none | phonemic_pair | portmanteau | collocation_disruption
10. setup_frame
11. primary_template
12. content_moves, act_out, joke.relational, tag_operation, subversions
13. difficulties
```

**After agents complete:**
1. Verify files: `ls annotations/*.yaml`
2. Validate: `python3 -c "import yaml, glob; [yaml.safe_load(open(f)) for f in glob.glob('annotations/*.yaml')]"`
3. Compare old vs new: check the backup directory against new annotations. Note where classifications changed.
4. Check concept registry usage: are agents using node_ids or ad-hoc strings?
5. Check scale_shift non-none rate: should be ~30% (down from 47% in batch 2)
6. Check operation_alternative non-null rate: should be ~15-35%
7. **Reproducibility validation:** `python3 engine/validate_annotations.py`
   - Checks: concepts resolve to registry, valid operations/templates, no mechanism descriptions as concepts, operation_alternative validity, structural field placement
   - Fix ERRORS before proceeding. WARNINGS should be addressed.
8. Produce synthesis: operation/template/setup_frame distributions, vocabulary gaps
9. Update `working/questions.md` with any new findings
