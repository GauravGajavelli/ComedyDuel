# Decision Log

Non-obvious judgment calls you made during annotation, for delayed
self-review. The point is not to remember every decision — it's to catch
patterns of drift in your own annotation behavior over time.

## What to log

Log any of these:

- A classification where your reasoning was "felt right" rather than
  articulated (why did it feel right? what would the alternative have
  been?)
- An instance where the annotation assistant proposed a value and you
  agreed with it (this is the most corrosive failure mode — log aggressively)
- A case where you picked between two vocabulary values and the choice
  wasn't obvious (note both candidates and what tipped the decision)
- An annotation you're genuinely uncertain about (note the specific
  uncertainty)

## What NOT to log

- Obvious classifications where the schema and vocabulary pointed to one
  answer
- Pure clerical decisions (transcription choices, formatting)
- Disagreements with the assistant that you resolved by pushing back —
  those are working as intended

## Format

```
### [date] - [joke_id] - [field_path]
**Decision:** What you wrote to the field.
**Alternative considered:** What else it could have been.
**Reasoning (as best you can articulate):** Why the chosen value won.
**Flag type:** assistant_proposal_agreed_with | felt_right_not_articulated |
               close_call | uncertain
**Weekly review notes:** (fill in when reviewed)
```

## Rules

- Log during post-session review (5-minute pass), not mid-annotation.
- Don't smooth or clean up log entries before committing. The messy
  version is the honest version.
- Entries stay in the file forever. Don't delete.

---

_(No entries yet.)_
