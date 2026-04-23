# Batch 1 Reclassification Guide

Targeted fixes for 71 annotations under schema v0.6. NOT a full re-annotation —
only fields affected by the v0.6 changes need review.

## How to use this file

During your audit of each annotation, check two things:
1. **setup_frame**: Does the old `establishes_norm` map to convention, behavior,
   or premise? Use the agent's gloss to decide.
2. **primary_template**: Is this a candidate for monumental_as_mundane or
   shared_recognition? Check the agent's difficulty notes.

Mark each annotation as reviewed by adding `v0.6_reviewed: true` to the YAML.

## setup_frame reclassification rules

| Old value | New value | When to use | Gloss signal |
|---|---|---|---|
| establishes_norm | establishes_convention | Setup references a cultural practice, social ritual, institutional norm, or "how things work" | "the norm of the middle finger as insult," "the norm of paying by cheque," "construction fences as safety" |
| establishes_norm | establishes_behavior | Setup references a recognizable behavioral pattern — "people do this" | "men congregating near tools," "women holding dresses up," "channel flipping," "lane changing" |
| establishes_norm | establishes_premise | Setup accepts a claim or hypothetical that the bit builds on | "body parts as insults," "fashion will disappear," "traffic will get worse," "appetites are ruinable" |
| establishes_norm | establishes_expectation | Setup builds anticipation of a proportional payoff | "escalating preparation list," "reason number one," "the ultimate psychological test" |
| establishes_anomaly | establishes_anomaly | (unchanged) Setup presents something puzzling | "something about a cheque is not masculine" |
| establishes_sequence | establishes_sequence | (unchanged) Setup is an ordered progression | "out-back-sleep-up cycle," "paint getting closer" |

## Template review candidates

These annotations were flagged by agents as potentially misclassified.
Check during audit — reclassify if the new template fits better.

### monumental_as_mundane candidates (were mundane_as_monumental)
- S01E03 LP6: "that's really insulting to get the toe, isn't it?" — closing
  button that treats the absurd toe-insult scenario with casual "isn't it?"
  register. Agent noted the joke deflates rather than elevates.
- S01E06 LP6: "Boy, this is some really bad traffic now" — backwards traffic
  met with banal complaint. Agent explicitly flagged "inverted
  mundane_as_monumental."
- S01E08 LP2: "This is going to be our outfit... That's it." — civilization-
  wide aesthetic choice treated with committee-meeting casualness. Agent noted
  the mismatch direction is deflation.
- S01E10 LP5-LP7: Star Trek bridge reread as living room, aliens as Friday-
  night visitors. Agent flagged "revealing the monumental AS mundane."

### shared_recognition candidates (were mundane_as_monumental or false_equivalence)
- S01E01 LP3: "Did you ring? I can't find him" — phone call act-out. Agent
  noted "no frame shift, pure recognition humor" and forced
  mundane_as_monumental as default.
- S01E04 LP3: "What are you using, the Philips head?" — the canonical
  articulation example. Agent noted template was awkward fit.
- S01E09 LP1: "sliding off the sofa with potato chip crumbs" — pure
  articulation of the TV-watching posture. Agent chose false_equivalence
  but flagged poor fit.
- S01E04 LP2 tag: "Honey, I think Jim's working on something over there" —
  performed shared recognition of the exact excited announcement.

### Annotations that are fine as-is (no template change needed)
All annotations NOT listed above retain their current template classification.
The false_equivalence broadening means those classifications are now valid under
the wider criterion — no changes needed.

## Validation check after reclassification

After completing the reclassification, count:

**setup_frame distribution (expected):**
- establishes_convention: ~20-25 (28-35%)
- establishes_behavior: ~20-25 (28-35%)
- establishes_premise: ~8-12 (11-17%)
- establishes_expectation: ~4-6 (6-8%)
- establishes_anomaly: ~4 (6%)
- establishes_sequence: ~6 (8%)

If any single value exceeds 40%, the split didn't work for that value —
log in questions.md.

**template distribution (expected after reclassification):**
- mundane_as_monumental: ~23 (32%) — down from 42%
- monumental_as_mundane: ~4-6 (6-8%)
- shared_recognition: ~4-5 (6-7%)
- reductio: ~14 (20%)
- escalation: ~13 (18%)
- false_equivalence: ~8 (11%)
- anthropomorphization: ~2 (3%)

mundane_as_monumental dropping from 42% to ~32% confirms the split worked.
If it's still above 40%, some candidates were missed or the new templates'
criteria are too narrow.
