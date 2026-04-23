# Unresolved Questions

Questions hit during annotation that weren't resolved in-session. Reviewed
during weekly review; questions appearing 3+ times or blocking annotation
get addressed each week.

## Format

Each entry:

```
### [date] - [short title]
**Context:** Joke ID(s) where this came up, and what you were trying to do.
**Question:** The question itself, stated precisely.
**Why it's not resolvable in-session:** Why you punted rather than deciding.
**Weekly review notes:** (fill in when reviewed)
**Resolution:** (fill in when resolved)
```

## Rules

- Log the question even if you think you'll remember. You won't.
- Don't edit questions after they're logged. If your understanding
  changes, add a new entry that references the old one.
- Resolved entries stay in the file (for history). Move them under a
  `## Resolved` section after resolution.
- If a question has appeared 3+ times across different annotations,
  mark it high-priority for the next weekly review by prefixing the
  title with `[!]`.

---

## Open

### 2026-04-23 - Laugh architecture: should the schema capture where laughs fall?
**Context:** Cross-agent annotation of S01E01–S01E05 opening monologues. Agents
segmented at laugh points but used structural inference (punchline syntax,
act-out boundaries, topic pivots, rhetorical punctuation like "right?" and
"isn't it?") rather than acoustic evidence. The schema currently has no field
for laugh placement.
**Question:** Should the structure layer include a `laugh_architecture` field
capturing where the primary laugh falls (punchline / tag / topper / act_out)
and whether it sustains through subsequent elements? This matters for
generation — tag timing and topper landing depend on knowing where the laugh
is. The performance layer has `pause_placement` but that describes the
comedian's pauses, not the audience's response. These are correlated but not
identical.
**Why it's not resolvable in-session:** Needs real annotation data (with audio)
to determine whether the field discriminates in practice. Possible shape:
```yaml
laugh_architecture:
  primary_laugh_at: ""      # punchline | tag | topper | act_out
  laugh_sustain: null        # null | through_tag | through_act_out
```
But this might not survive contact with real performance data.
**Weekly review notes:**
**Resolution:**

### 2026-04-23 - ~~Template gap: monumental_as_mundane~~ RESOLVED
**Resolution:** Added to templates.yaml in v0.6. Full definition block with
criterion, positive example (E06), negative example (E08), distinguished_from.
**Why it's not resolvable in-session:** Needs the 3-occurrence threshold.
**Weekly review notes:**
**Resolution:**

### 2026-04-23 - ~~Template gap: pure articulation shape~~ RESOLVED
**Resolution:** Added as `shared_recognition` to templates.yaml in v0.6. Full
definition block. The shape IS the naming of shared truth, no secondary scaffolding.
**Why it's not resolvable in-session:** Near the threshold but not over it.
**Weekly review notes:**
**Resolution:**

### 2026-04-23 - ~~Template gap: false_equivalence vs apt mapping~~ RESOLVED
**Resolution:** false_equivalence criterion broadened in v0.6 to cover both
mismatch pairings and apt pairings. No split needed — the template describes the
shape (two things explicitly compared), not the direction of the humor. Added
dog-whistle example for the apt direction.
**Why it's not resolvable in-session:** At threshold — should be addressed at
next weekly review. The question is whether to split or broaden.
**Weekly review notes:**
**Resolution:**

### 2026-04-23 - [!] reinterpretation/articulation boundary is soft
**Context:** Flagged independently by all 5 episode agents. Seinfeld's
observational comedy sits exactly on the boundary — the audience half-knows the
truth being stated but sees it from a new angle. The articulation test ("would
it still be funny if you knew?") is conceptually clear but many observations
pass it AND involve a frame shift. The two operations aren't cleanly mutually
exclusive for observational comedy.
**Question:** Should the distinguished_from be sharpened with a frame-dependency
test: "Does the humor REQUIRE the audience to shift frames, or does it work
within a single frame?" If removing the frame shift kills the joke →
reinterpretation. If the joke survives within the existing frame → articulation.
**Appearances:** 10+ (nearly every episode in both pilot and batch 1).
**Status:** PARTIALLY RESOLVED in v0.6. Frame-dependency test formalized in
pivot-mechanisms.yaml with 3 worked examples and a general rule ("Is the
OBSERVATION the joke, or is the ANGLE on the observation the joke?").
Needs validation: does the sharpened test reduce disagreement in practice?
Re-check after batch 2 annotations.
**Why it's not fully resolved:** The worked examples cover the clearest cases
but the boundary may still be soft for mid-range observational humor. Track
whether agents using the v0.6 vocabulary produce fewer flags on this boundary.
**Weekly review notes:**
**Resolution:**

### 2026-04-23 - setup_frame "establishes_norm" captures ~80% of jokes
**Context:** S01E01 agent flagged that establishes_norm was the default for most
beats across all 5 monologues. The 4 values (norm / anomaly / category /
sequence) don't discriminate enough. ~80% establishes_norm suggests the field
isn't doing useful work.
**Question:** Should the setup_frame vocabulary be expanded? Candidate additions
from the 5-episode corpus: establishes_convention (a cultural practice or social
norm, not just a behavioral regularity), establishes_expectation (a promise or
buildup that creates specific anticipation), establishes_frame (an interpretive
lens, like a philosophical question's register). Or should setup_frame be removed
if it can't discriminate?
**Appearances:** Structural — applies to every annotation.
**Why it's not resolvable in-session:** Now confirmed at 80% across 64
laugh-points (batch 1). Pattern is not a small-sample artifact. Ready for
evaluation at weekly review.
**Weekly review notes:**
**Resolution:**

### 2026-04-23 - Potential modifier gap: valence_flip (bad→good evaluative reversal)
**Context:** S02E04 (Heart Attack) — "intentionally ruin my entire appetite"
reframes appetite-ruining from transgression to achievement. The evaluative
charge of the act flips without any change in scope, gravity, or reading mode.
Neither reading_switch nor scale_shift captures this.
**Question:** Should the pivot_mechanism system include a valence_flip modifier
for cases where the punchline reverses the evaluative charge (good↔bad,
desirable↔undesirable) of the same act without changing its scope or frame?
**Appearances:** 1 (S02E04 LP2). Needs 2 more before adding.
**Why it's not resolvable in-session:** Single occurrence.
**Weekly review notes:**
**Resolution:**

### 2026-04-23 - Potential gap: "counterfactual staging" device
**Context:** S02E05 (The Deal) — "You never see a guy take a suit off the rack,
put his head in the neck" constructs a hypothetical scenario to stress-test a
premise by applying it somewhere it visibly fails. Sits between extension and
transplant.
**Question:** Is this a distinct device worth tracking, or is it adequately
captured by extension (following the premise's logic into a new garment type)?
**Appearances:** 1 (S02E05 LP4). Needs 2 more.
**Why it's not resolvable in-session:** Single occurrence; currently handled by
extension.
**Weekly review notes:**
**Resolution:**

### 2026-04-23 - mundane_as_monumental at 42% — broadness check
**Context:** Batch 1 synthesis. mundane_as_monumental is the most-used template
at 42% across 64 laugh-points, exceeding the 40% broadness threshold.
**Question:** Should this be split into sub-species? Candidate split:
elevation (mundane given grand frame — classic definition) vs deflation
(monumental given trivial treatment — the monumental_as_mundane gap). Or is
42% acceptable for Seinfeld's dominant rhetorical move?
**Appearances:** Structural — applies to template distribution.
**Why it's not resolvable in-session:** Needs determination of whether the
elevation/deflation split is a clean sub-typing or if the current template
adequately covers both directions once monumental_as_mundane is added as a
separate value (which would pull the deflation cases out and reduce
mundane_as_monumental to ~35%).
**Weekly review notes:**
**Resolution:**

---

## Resolved

_(No entries yet.)_
