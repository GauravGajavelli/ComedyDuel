# Field Usage Tracking

Running count of which schema fields are actually used in completed
annotations. The purpose is to catch schema bloat — fields that get
defined in theory but never used in practice are candidates for removal,
and fields that always take the same value may not be discriminating
anything.

## When to update

- After the first 30 annotations are complete
- Every 20 annotations thereafter
- Any time a vocabulary value or field is a candidate for removal (to
  get the current count)

## How to count

For each field:
- **Populated:** annotations where the field has a meaningful,
  non-default, non-null value.
- **Total:** total completed annotations.
- **Ratio:** populated / total.

For vocabulary values:
- **Uses:** annotations where this value was selected.
- **Total:** total annotations where the containing field was populated.
- **Ratio:** uses / total.

## Thresholds

- **< 20% populated after 30+ annotations** → candidate for removal.
  Flag here; act only after two consecutive checks confirm.
- **100% populated with always-the-same-value** → suspect for
  discriminating nothing. Review whether the field is carrying
  information.
- **Single vocabulary value > 80% usage** → either that value is the
  norm (fine) or neighboring values are under-defined and getting
  collapsed into it (not fine — investigate).

## Format

Each check gets its own dated section. Don't edit prior checks; add
new ones.

```
## [date] — after N annotations

### Fields

| field_path | populated | total | ratio | notes |
|---|---|---|---|---|
| joke.content.primary_domain | 30 | 30 | 1.00 | — |
| joke.content.specificity.trajectory | 6 | 30 | 0.20 | borderline |
| ...

### Vocabulary value usage

#### incongruity_type
| value | uses | total | ratio |
|---|---|---|---|
| reversal | 11 | 30 | 0.37 |
| reframe | 8 | 30 | 0.27 |
| ...

### Candidates flagged

- joke.content.specificity.trajectory: 20% usage — first flag, watch
  next check
- performed_relatability.intensity: 10% usage — first flag

### Actions taken

(none this check / removed X after second flag / ...)
```

---

_(No checks yet. First check expected after the first 30 annotations.)_
