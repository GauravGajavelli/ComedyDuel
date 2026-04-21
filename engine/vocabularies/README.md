# Controlled Vocabularies — Definition Format and Maintenance

This directory holds the controlled vocabularies referenced by `schema.yaml`. Each vocabulary lives in its own file (`incongruity-types.yaml`, `templates.yaml`, etc.) and defines the legal values for a structured field.

## Why strict definitions

Vocabulary values are how the engine discriminates jokes. If "reversal" and "reframe" are vague in the annotator's head, they'll be applied inconsistently across annotations, and the engine will learn patterns that don't exist (or miss patterns that do). Consistent annotation requires strict-enough definitions that two readings of the same joke, months apart, produce the same value.

Strict definitions also defend against a specific failure mode: **category drift**. Over time, without anchoring, "reversal" slowly absorbs near-miss cases until it means "anything with a turn," and the category stops carrying information. Strict definitions with near-miss negative examples hold the edges.

## Definition format

Every vocabulary value is defined with four required elements:

```yaml
value_name:
  criterion: |
    One or two sentences stating what makes a joke fit this value.
    Should be prescriptive enough to make edge cases decidable.

  positive_example: |
    A real joke (ideally from an annotated source) that clearly fits
    this value, with a brief note on WHY it fits.

  negative_example: |
    A near-miss — a joke that looks like it could be this value but
    is actually a neighboring value. Include WHICH neighboring value
    it actually is and WHY.

  distinguished_from:
    neighboring_value_1: |
      The specific line drawn between this value and its nearest
      neighbor. Include a decision procedure: "test: if X, classify as
      this value; if Y, classify as neighbor."
    neighboring_value_2: |
      Same for each near-neighbor in the vocabulary.
```

### Why each element matters

The **criterion** must be prescriptive, not descriptive. "Reversal is when something gets flipped" is descriptive and useless. "The punchline affirms the negation of what the setup established" is prescriptive — it tells you what to check.

The **positive example** anchors the criterion in a real joke. If no real joke clearly fits the criterion, the value probably shouldn't exist.

The **negative example** is the most important field. It must be a near-miss, not an obvious non-case. A negative example of "reversal" isn't "the sky is blue" — it's a joke that superficially resembles reversal but is actually reframe. Near-miss negatives train the annotator's eye for the distinction.

The **distinguished_from** block is where the real work of definition lives. For every neighboring value in the vocabulary, the line between them is drawn explicitly, with a decision procedure embedded. When annotation hits an ambiguous joke, this is what you consult.

## When to add a value

During annotation, if a joke doesn't fit any existing value in a vocabulary, don't force-fit. Add the value to the vocabulary, with all four required elements, and log in `working/schema-changelog.md`. The added value must come with its full definition block including contrast pairs against its nearest neighbors. Adding a value without this block is not allowed — it produces drift immediately.

If you can't construct a negative example (near-miss), the value may not be distinct enough from existing values to earn its place. Consider whether it's really a sub-type or feature of an existing value.

## When to revise a value

During weekly review, if multiple annotations have been inconsistent in applying a value, the definition is too loose. Tighten the criterion, or add another neighboring value to the distinguished_from block. Revisions are logged in changelog with the annotations they invalidate.

## When to merge or remove a value

Values below ~15% usage after 30+ annotations are candidates for removal. Values consistently confused with a neighbor are candidates for merger. Both are high-cost operations requiring re-annotation of every joke using the affected values. Do during weekly review, log carefully.

## Vocabularies that resist this format

Some schema values aren't enumerated categories and can't be defined with contrast pairs:

- **Affect axes** (valence, arousal) are numeric scales. Defined with anchor-point descriptions at the extremes and midpoints, not with positive/negative example jokes.
- **Subject-matter domains** are intentionally overlap-tolerant (jokes span multiple domains). Defined functionally, not contrastively.
- **Concept adjacencies** can't be pre-defined at all. They emerge from annotation co-occurrence data.

For these, see the individual vocabulary files; they have their own formats documented at the top of each file.

## Starter vocabularies

The following files ship with starter definitions covering the most important 3–5 values in each. During Phase 0, extend them by adding new values as real jokes demand them. Don't pre-populate with theoretical values; let the jokes drive the vocabulary.

Starter vocabularies provided:
- `incongruity-types.yaml` — mechanisms by which the punchline violates the setup
- `templates.yaml` — rhetorical shapes of jokes
- `positioning.yaml` — comedian's stance relative to audience
- `subversions.yaml` — moves that deliberately break expectations (formulaic defenses)
- `affect-axes.yaml` — numeric scales for affective register (different format)

Vocabularies NOT shipped with starter values — to be populated entirely from annotation:
- `domains.yaml` — subject-matter domains
- `cadence.yaml` — delivery rhythm patterns
- `registers.yaml` — voice register values
- `persona-markers.yaml` — specific voice identity markers
- `media.yaml` — source media types
- `register-shifts.yaml` — types of vocal register shifts
- `incongruity-operates-on.yaml` sub-vocabularies (setup_frame, punchline_action, reading_switch) — starter values only in the schema comment; populate here if they expand

These are deliberately left empty because starter values for them would be either too obvious (media: stand_up, podcast...) or too theory-driven (cadence patterns from drama studies) to earn their place without real jokes attesting them.
