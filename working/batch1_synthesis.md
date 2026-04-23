# Batch 1 Synthesis — Episodes 1-15 (14 monologues)

Compiled 2026-04-23. Covers episodes 1-15 (skipping E12 The Revenge which
has no opening monologue). All 14 episodes complete.

## Laugh-point count by episode

| Ep | Title | Laugh-points | Agent confidence |
|---|---|---|---|
| 1 | Good News Bad News | 6 | high (5/6), medium (1/6) |
| 2 | The Stakeout | 5 | high (4/5), medium (1/5) |
| 3 | The Robbery | 2 | high |
| 4 | Male Unbonding | 5 | high (4/5), medium (1/5) |
| 5 | The Stock Tip | 4 | high (3/4), medium (1/4) |
| 6 | The Ex-Girlfriend | 7 | high (5/7), medium (2/7) |
| 7 | The Pony Remark | 4 | high |
| 8 | The Jacket | 4 | high (3/4), medium (1/4) |
| 9 | The Phone Message | 3 | high (2/3), medium (1/3) |
| 10 | The Apartment | 8 | high (6/8), medium (2/8) |
| 11 | The Statue | 5 | high (4/5), medium (1/5) |
| 13 | The Heart Attack | 5 | high (4/5), medium (1/5) |
| 14 | The Deal | 6 | high (5/6), medium (1/6) |
| 15 | The Baby Shower | 7 | high (6/7), medium (1/7) |
| **Total** | | **71** | **high: 84%, medium: 16%** |

## Operation distribution (64 laugh-points)

| Operation | Count | Percentage | Notes |
|---|---|---|---|
| reinterpretation | 22 | 31% | Dominant but below 40% threshold |
| extension | 21 | 30% | Second most common — higher than pilot (15%) |
| articulation | 11 | 15% | Stable with disambiguation rule |
| negation | 7 | 10% | Stable |
| transplant | 6 | 8% | Grew with E15 (anachronistic transplants) |
| mapping | 4 | 6% | Low — Seinfeld uses fewer explicit comparisons than expected |

### Key observations

- **reinterpretation at 33%**: Below the 40% broadness threshold but
  worth watching. No clear sub-species emerged — the reinterpretations
  span conceptual reframes (E01 "to be out"), evaluative flips (E13
  "ruining appetite" as achievement), geometric reframes (E14 "get
  behind the clothes"), and register deflations (E09 "it's a can of
  soda"). These feel genuinely different but may resist clean sub-typing.

- **extension surged to 30%**: Much higher than the 5-episode pilot
  (15%). This is because the new episodes include several sustained-
  premise routines (E08 earth outfit, E11 sweepstakes honesty, E13
  appetite economics, E14 man trying on suit) where Jerry builds a
  premise and runs it for multiple beats. Extension is Seinfeld's
  second-favorite tool for multi-beat bits.

- **mapping dropped to 6%**: The pilot's 27% was inflated by the Male
  Unbonding episode (zombies, dog whistle, holster) which was
  comparison-heavy. Across a broader sample, explicit A-is-like-B
  comparisons are less common than premise-following. Mapping may be
  more characteristic of specific bit styles than of Seinfeld generally.

- **transplant appeared cleanly**: E07 (leisure police/arrest framework),
  E08 (committee/boardroom framework applied to alien fashion), and
  E06 (existential-crisis framework applied to lane choice). These
  were classified with high confidence — the mismatch test worked cleanly.

## Modifier usage

| Modifier | Non-none count | Percentage | Expected |
|---|---|---|---|
| reading_switch | 3/64 | 5% | ≤10% — within range |
| scale_shift | 22/64 | 34% | ≤30% — slightly over |

### scale_shift breakdown
- contraction: 15 (23%)
- expansion: 7 (11%)

**Concern**: scale_shift: contraction at 23% is high. Multiple agents
flagged that contraction often accompanies reinterpretation automatically
(when you reframe something grand as trivial, contraction is inherent).
Pass 4 commutation tests should verify which of these are independently
load-bearing. The heuristic ("could the operation work without the scale
change?") may need strengthening — agents applied it inconsistently.

## setup_frame distribution

| Value | Count | Percentage |
|---|---|---|
| establishes_norm | 51 | 80% |
| establishes_sequence | 6 | 9% |
| establishes_anomaly | 4 | 6% |
| establishes_category | 3 | 5% |

**Confirmed**: establishes_norm at 80% across 64 laugh-points. This field
is not discriminating. The vocabulary needs expansion or the field needs
removal. See questions.md entry.

## Template distribution

| Template | Count | Percentage |
|---|---|---|
| mundane_as_monumental | 27 | 42% |
| reductio | 14 | 22% |
| escalation | 13 | 20% |
| false_equivalence | 8 | 13% |
| anthropomorphization | 2 | 3% |

**mundane_as_monumental at 42%**: Exceeds the 40% broadness threshold.
This is Seinfeld's signature rhetorical shape, but at 42% it risks being
a genus. Possible sub-species:
- **elevation**: mundane thing given elevated frame (classic definition)
- **deflation/monumental_as_mundane**: monumental thing given mundane
  treatment (flagged by E03, E06, E10 agents)
Needs evaluation at weekly review.

## Vocabulary gap tracker (updated tallies)

| Gap | Appearances | Threshold | Status |
|---|---|---|---|
| [!] reinterpretation/articulation boundary | 8+ | 3 | OVER — needs resolution |
| monumental_as_mundane template | 4 | 3 | **OVER — ready for addition** |
| false_equiv vs revealed_equivalence | 3 | 3 | AT THRESHOLD — review |
| pure articulation template | 3 | 3 | AT THRESHOLD — review |
| setup_frame: establishes_norm at 80% | confirmed | — | needs expansion |
| valence_flip modifier (bad→good on same act) | 1 | 3 | tracking |
| "counterfactual staging" device | 1 | 3 | tracking |
| "corporate personification" lighter than anthropomorphization | 1 | 3 | tracking |
| "premise saturation" (sustained commitment as load-bearing) | 1 | 3 | tracking |
| "anachronistic transplant" (temporal domain separation) | 1 | 3 | tracking |
| performance-dependent laugh-points awkward in Pass 2 | 2 | 3 | tracking |

## Actionable items for weekly review

1. **ADD monumental_as_mundane to templates.yaml** — 4 appearances across
   3 episodes (E03 finger, E06 backwards traffic, E08 alien committee,
   E10 Star Trek as living room). Full vocabulary definition needed.

2. **RESOLVE reinterpretation/articulation boundary** — 8+ occurrences of
   agents flagging this as the hardest call. The frame-dependency test
   was provided but agents applied it inconsistently. Needs to be
   formalized in the vocabulary file with worked examples.

3. **EVALUATE false_equivalence split** — 3 appearances of "apt pairing"
   being forced into a "mismatch pairing" template. Consider splitting
   into false_equivalence (humor in mismatch) and revealed_equivalence
   (humor in aptness), or broadening false_equivalence's criterion.

4. **EVALUATE pure articulation template** — 3 appearances of jokes
   where the rhetorical shape IS the stating of shared truth, with no
   secondary structural move. mundane_as_monumental was forced as default.

5. **EVALUATE setup_frame expansion** — 80% establishes_norm confirmed
   across 64 laugh-points. Either expand vocabulary or flag for removal.

6. **WATCH mundane_as_monumental** — at 42%, exceeds broadness threshold.
   Evaluate whether elevation vs deflation sub-species are viable.

7. **WATCH scale_shift: contraction** — at 23%, may be over-applied.
   Commutation tests in Pass 4 should verify independence from operation.
