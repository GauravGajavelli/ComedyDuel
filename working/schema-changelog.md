# Schema Changelog

Every change to `engine/schema.yaml`, to `engine/vocabularies/*.yaml`, or
to `engine/concepts/` (other than normal concept-node creation) is logged
here. The changelog exists so that annotations can be interpreted in the
context of the schema version that produced them, and so that changes
with downstream impact can be audited.

## Format

```
## [date] v[N.M] - [short description]

**Changed:** What file/field/value changed.
**From:** Prior state (or "(new)" for additions).
**To:** New state (or "(removed)" for deletions).
**Rationale:** Why the change was made. For field additions, include
  answers to the five structural questions. For vocabulary additions,
  include the full definition block. For removals, include usage data.
**Invalidates:** Which prior annotations (if any) need re-review as a
  result of this change.
```

## Rules

- Every schema/vocabulary change requires an entry BEFORE the change is
  committed. Changes without entries aren't allowed.
- Invalidation is serious. If a change invalidates prior annotations,
  list the joke IDs and flag them for re-review during the next weekly
  review session.
- Version numbers follow semantic intent: bump major (v1 → v2) for
  changes that invalidate many prior annotations; bump minor (v0.1 →
  v0.2) for additive or non-invalidating changes.
- During Phase 0, expect frequent changes. Don't hesitate to log small
  ones — the record is more useful than the overhead is costly.

---

## 2026-04-21 v0.1 — Initial schema

**Changed:** Initial creation of schema.yaml, protocols.md, and starter
vocabularies (incongruity-types, templates, positioning, subversions,
affect-axes).

**From:** (new)

**To:**
- schema.yaml with nine-layer decomposition (content, logic, structure,
  performance, voice, affective, narrative, relational, meta)
- joke/performance structural split
- multi-pass annotation workflow with annotation_status tracking
- pivot_locus field (logical | affective | both)
- affective trajectories anchored to structural events
- concept nodes as typed references, not bare strings
- gloss vs structured field distinction
- commutation test using field-paths for structured reference

**Rationale:** Captures all architectural decisions from the initial
design conversation. This version is provisional — expect revision after
the first 5–10 annotations surface issues the initial design didn't
anticipate.

**Invalidates:** None (no prior annotations exist).

---

_(Subsequent entries below as changes accumulate.)_
