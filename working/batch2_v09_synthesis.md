# Batch 2 Synthesis — v0.9 Re-annotation of Episodes 1-15

Compiled 2026-04-26. Fresh v0.9 annotations of all 14 opening monologues
(episodes 1-15, skipping E12 The Revenge — no monologue). All annotations
are Pass 2 (silent decomposition) only.

## Laugh-point count by episode

| Ep | File ID | Title | Laugh-points |
|---|---|---|---|
| 1 | s01e01 | Good News Bad News | 5 |
| 2 | s01e02 | The Stakeout | 4 |
| 3 | s01e03 | The Robbery | 3 |
| 4 | s01e04 | Male Unbonding | 4 |
| 5 | s01e05 | The Stock Tip | 3 |
| 6 | s02e01 | The Ex-Girlfriend | 5 |
| 7 | s02e02 | The Pony Remark | 4 |
| 8 | s02e03 | The Jacket | 4 |
| 9 | s02e04 | The Phone Message | 4 |
| 10 | s02e05 | The Apartment | 5 |
| 11 | s02e06 | The Statue | 3 |
| 13 | s02e08 | The Heart Attack | 3 |
| 14 | s02e09 | The Deal | 4 |
| 15 | s02e10 | The Baby Shower | 4 |
| **Total** | | | **55** |

## v0.8 → v0.9 comparison: operation distribution

| Operation | v0.8 (71 LP) | v0.9 (55 LP) | Change |
|---|---|---|---|
| reinterpretation | 22 (31%) | 19 (34%) | +3pp — still dominant |
| extension | 21 (30%) | 10 (18%) | -12pp — significant drop |
| articulation | 11 (15%) | 11 (20%) | +5pp — rose with clearer test |
| mapping | 4 (6%) | 8 (14%) | +8pp — significant rise |
| negation | 7 (10%) | 4 (7%) | -3pp — stable |
| transplant | 6 (8%) | 3 (5%) | -3pp — stable |

### Key observations

- **extension dropped from 30% to 18%**: The v0.8 batch included mid-episode
  and closing monologue laugh-points which tend to be multi-beat routines
  (where extension dominates). The v0.9 batch covers opening monologues only
  with 55 laugh-points. Some v0.8 "extension" calls may have been
  reclassified as escalation-template jokes with different operations under
  the sharpened v0.9 layer rules (operation vs template separation).

- **mapping rose from 6% to 14%**: With the v0.9 comparison template
  (formerly false_equivalence) and the clearer mapping vs transplant
  distinction, agents more confidently identified apt-parallel jokes
  (dog whistle, holster, emperor, nesting/hunting) as mapping operations
  within comparison templates.

- **articulation stable at 20%**: The frame-dependency test in v0.9 is
  producing consistent results. Agents consistently applied it (Philips head,
  channel-flipping, appetite-as-renewable, money-changes-with-hunger).

- **reinterpretation at 34%**: Up slightly from 31%. Still below the 40%
  broadness threshold. No sub-species are emerging — the reinterpretations
  span conceptual reframes (E01 "to be out"), literal-reads (E14 one-legged
  pose), evaluative flips (E02 cheque-as-plea), and category reframes
  (E04 construction fence).

## v0.8 → v0.9 comparison: template distribution

| Template | v0.8 (71 LP) | v0.9 (55 LP) | Change |
|---|---|---|---|
| mundane_as_monumental | 27 (42%) | 14 (25%) | -17pp — resolved |
| escalation | 13 (20%) | 12 (21%) | stable |
| comparison (was false_equivalence) | 8 (13%) | 12 (21%) | +8pp — absorbed apt pairings |
| bare_observation (was shared_recognition) | — | 11 (20%) | NEW — absorbing articulation shapes |
| reductio | 14 (22%) | 3 (5%) | -17pp — many reclassified as escalation |
| monumental_as_mundane | — | 3 (5%) | NEW — split from mundane_as_monumental |
| anthropomorphization | 2 (3%) | 0 (0%) | moved to content_moves (correct) |

### Key observations

- **mundane_as_monumental dropped from 42% to 25%**: The v0.8 broadness
  concern is resolved. Three factors: (1) monumental_as_mundane split off
  (~5%), (2) bare_observation absorbed pure-naming jokes that were forced
  into mundane_as_monumental (~10%), (3) comparison absorbed jokes where the
  rhetorical shape was pairing, not elevation (~5%).

- **bare_observation at 20%**: This new template (v0.6) is doing useful work.
  It captures Seinfeld's signature "just name the truth" shape cleanly,
  co-occurring with articulation as expected.

- **reductio dropped from 22% to 5%**: Many v0.8 "reductio" classifications
  were actually escalation (building across beats without a strict
  logical-argument chain). The v0.9 layer rules clarify that reductio requires
  a logical chain to absurd conclusion, not just escalating specificity.

## setup_frame distribution — v0.9

| Value | Count | Percentage |
|---|---|---|
| establishes_premise | 21 | 38% |
| establishes_behavior | 12 | 21% |
| establishes_convention | 10 | 18% |
| establishes_expectation | 7 | 12% |
| establishes_anomaly | 3 | 5% |
| establishes_sequence | 2 | 3% |

**Improvement**: The v0.8 setup_frame was 80% `establishes_norm`. The v0.6
vocabulary expansion (splitting norm into convention/behavior/premise) is now
distributing cleanly. No single value exceeds 40%. The field is doing useful
discriminating work.

## Modifier usage

| Modifier | Count | Percentage |
|---|---|---|
| scale_shift: none | 29 | 52% |
| scale_shift: contraction | 14 | 25% |
| scale_shift: expansion | 12 | 21% |
| reading_switch: none | 53 | 96% |
| reading_switch: figurative_to_literal | 1 | 1% |
| reading_switch: literal_to_figurative | 1 | 1% |
| wordplay: (all none) | 55 | 100% |

**scale_shift at 47% non-none**: Still high (was 34% in v0.8). The heuristic
("could the operation work without the scale change?") needs reinforcement.
Pass 4 commutation tests should verify independence.

## New v0.9 fields — relational layer

| Field | Distribution |
|---|---|
| positioning: lateral_observer | 51/55 (92%) |
| positioning: with | 2/55 (3%) |
| positioning: below | 2/55 (3%) |
| audience_implication: co_observer | 48/55 (87%) |
| audience_implication: accomplice | 6/55 (10%) |
| audience_implication: witness | 1/55 (1%) |
| performed_relatability.present: true | 34/55 (61%) |
| shared_experience.required: true | 53/55 (96%) |

**Concern**: positioning at 92% lateral_observer and audience_implication at
87% co_observer — both are near-universal for Seinfeld's observational style.
These fields will discriminate more for confessional/character comics. For
Seinfeld, the few non-defaults (positioning: "with" in E04 when Jerry uses
"we", positioning: "below" in E06) are interesting edge cases.

## Act-out usage

26 of 55 laugh-points (47%) include act-outs. This is higher than expected
and reflects Seinfeld's heavy use of character voices in early monologues.
The v0.9 act-out block split (character_type + register_gap in joke,
character_register in performance) is working — agents consistently populated
the joke-side fields.

## Vocabulary gaps — new entries for questions.md

1. **establishes_premise at 38%** — not yet at broadness threshold (40%)
   but trending. May need watching. The value is doing real work (capturing
   hypothetical premises that subsequent beats build on) but could be
   over-applied to cases that are really establishes_convention.

2. **No concept nodes exist** — agents used informal string references for
   concepts. The engine/concepts/ directory needs population for the
   structured fields to function.

3. **scale_shift independence** — 47% non-none is high. Several agents noted
   that contraction "comes along for free" with reinterpretation. The
   independence heuristic needs strengthening or the field may be capturing
   a natural consequence of the operation rather than an independent modifier.
