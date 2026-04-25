# Laugh Point Partitions

Ground-truth segmentation from audio/video, collected during audit pass.
The monologue text is partitioned into contiguous segments where each
segment boundary falls at a laugh point. Every word belongs to exactly
one segment. The full monologue is the concatenation of all segments.

Multiple annotation layers are captured per segment so you only need to
watch each performance once.

## Format

```yaml
episode: S01E__
title: ""
segments:
  - text: "[verbatim text of this segment]"

    # --- Laugh layer (from audio) ---
    laugh: big | medium | small | chuckle | none
    #   none = this segment ends not at a laugh but at the start of a
    #   new setup or transition. Use for segments between laugh points.

    # --- Structural layer (compare against agent annotation) ---
    structural_event: premise | setup | punchline | tag | topper | act_out | connector
    agent_match: yes | split | merged | missed
    #   yes    = agent segmentation matches yours
    #   split  = you hear two laughs where agent had one laugh-point
    #   merged = agent split this into two but it's one sustained laugh
    #   missed = agent didn't identify this as a laugh-point

    # --- Physical performance layer (from video) ---
    physical_state: "[what the body is doing DURING this segment]"
    #   e.g., "standing center, relaxed stance" / "leaning on mic stand"
    #   This is the baseline — capture it even when unremarkable.
    physical_change: "[what changes at or near the segment boundary]"
    #   e.g., "freezes expression" / "shifts to character posture" /
    #   "scans audience" / "none"
    physical_load: supports | carries | independent | null
    #   Only populate when physical_change is notable. null otherwise.
    #   supports    = reinforces text; joke works without it
    #   carries     = IS the comedy; text alone would be flat
    #   independent = funny on its own, separate from text

    # --- Performance mode layer ---
    performance_mode: direct | character | narrative | rhetorical | physical
    #   Note transitions within a segment with →
    #   e.g., "direct → character" if comedian switches mid-segment

    # --- Energy layer ---
    energy: low | medium | high
    #   Rough perceived energy. Note shifts with →
    #   e.g., "low → medium" for a segment that builds
```

## What to capture

- **Every segment**, including unremarkable ones (the baseline data matters)
- `physical_state` even when it's "conversational default" — this tells us
  what "normal" looks like so deviations are meaningful
- `agent_match` for every segment — forces systematic comparison with the
  agent annotations in `annotations/`

## What `physical_load: carries` means

This is the highest-value observation. It means: if you read this segment
as text only (no video), the joke would fall flat. The physical delivery
IS the comedy. These observations directly identify where the visual
delivery system must do work in the game — text alone won't cut it.

## After collection

After 3-5 episodes:
1. Review `physical_change` entries across episodes — cluster into categories
2. Review `carries` entries — what visual devices would the game need to
   replicate what the comedian's body is doing?
3. Compare laugh partition boundaries against agent laugh-point segmentation —
   where do they disagree and why?
4. Feed clusters into visual device vocabulary design

---

## Episodes

_(Add one section per episode as you audit. Copy the segment template above.)_
