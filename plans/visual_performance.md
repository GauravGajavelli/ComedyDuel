# Plan: Visual Delivery Vocabulary for ComedyDuel

## Context

The annotation schema (v0.6) captures WHY jokes are funny (operations, templates) and has a performance layer for AUDIO delivery (cadence, pause_placement, vocal_register_shifts, affect). But the game needs multimodal delivery — visual devices that carry comedy alongside the text. The user observed from watching performances that the performer, not just the joke, carries things. A structurally correct joke with flat visual delivery will produce the "HAL 9000 effect."

The spec currently says "static character portraits" for MVP and defers animation. This plan designs the vocabulary and architecture for visual delivery so it can be implemented incrementally (static sprites → Rive avatars) while the structural framework stays stable.

## Design Decisions

### Should visuals align with joke content?

**It depends on the performer and the structural event.** This is formalized as a `content_rule` field on each visual cue:

- `content_aligned` — visual depicts what the text says (Cece at punchlines: she describes "the Little Guilt," visual shows it)
- `register_aligned` — visual matches energy/mood, not content (Mort: his face is the visual, not an illustration of his topics)
- `contrasting` — visual opposes text for comedic effect (deadpan face during escalating absurdity)
- `punctuating` — rhythm/emphasis only, no semantic relationship (screen shake at any punchline)
- `meta_commentary` — visual comments on the joke-telling format itself

**Default per performer:** Mort defaults to `register_aligned` (his visual IS his stillness; illustrating content would compete with deadpan). Cece defaults to `content_aligned` at punchlines (her comedy is imagistic — the audience wants to see what she's describing).

### Should art styles differ per comedian?

**Yes — same technology (Rive), different aesthetics and state machine complexity.**

- **Mort**: Flat palette, minimal linework, more negative space. Small state machine (6-8 poses, 10-12 expressions). The visual restraint IS the comedy — when his expression changes, it means something precisely because the baseline is so still. Think: a character who barely reacts to their own jokes. Visual equivalent of his deadpan vocal register.

- **Cece**: Saturated palette, expressive linework, more detail. Larger state machine (12-16 poses, 18-24 expressions). Her visual should feel like her comedy — escalating, specific, surprising. Visual equivalent of her high-energy vocal register.

The difference should be noticeable but not jarring within the same game UI — like two illustrators with different sensibilities drawing for the same publication.

### Why Rive over alternatives?

| Technology | Pros | Cons | Verdict |
|---|---|---|---|
| **Rive** | Web-native WASM renderer, tiny file sizes (50-200KB/character), state machine system maps directly to visual cue vocabulary, parameter-driven expressions | No out-of-box game engine integration (fine — this is browser-based) | **Primary choice** |
| **Live2D** | Parameter-based like Rive, industry standard for VTubers | Heavier runtime, not web-optimized, licensing costs | Too heavy for browser |
| **Spine** | Robust skeletal animation, wide game engine support | WebGL renderer needed, heavier than Rive | Overkill for this |
| **VN sprite sets** | Simplest to implement, cheapest to author | Static — no idle animation, no parameter interpolation | **MVP fallback** |

**Phased approach**: MVP uses VN sprite sets (8-10 expression swaps per character). V1.1 migrates to Rive avatars. The visual cue vocabulary and performer profiles stay the same across both phases — only the renderer changes.

### Other character expression approaches (avoiding uncanny 3D)

All of these avoid the uncanny valley while supporting comedy:

1. **Modular VN sprites** (brow + eyes + mouth layers recombined) — 5 components × 3 variants = 15+ unique expressions without drawing each separately. Used by most visual novels.
2. **Rive state machines** — parameter-driven (mouth form, eye position, brow angle). Smooth interpolation between discrete states. Best for reactive characters.
3. **Ace Attorney pose system** — discrete pose states with sharp transitions at emotional beats. The transition itself is the visual event, not smooth animation.
4. **Undertale approach** — character-specific fonts + text speed/shake effects do most of the expressive work; portraits are simple and change infrequently. The text IS the performance.
5. **West of Loathing approach** — deliberately simple art (stick figures) where the visual simplicity is itself a comedic register. Contrast between innocent visuals and dark/absurd text.

## Step 0: Empirical Data Collection (before creating vocabulary files)

The visual device vocabulary should be derived from observed performance data,
following the same principle as the audio vocabularies (cadence, registers,
register-shifts are empty and populated from annotation). Before creating the
vocabulary files, the user collects physical performance observations from
Seinfeld episodes to ground the categories empirically.

### What the user collects

For each episode being audited, note every moment where the comedian's body
does something notable. Use this format:

```
episode: S01E__
at: [structural event — premise/setup/punchline/tag/topper/act_out/connector]
text: "[the line being delivered]"
physical: [what the comedian does — be specific: "leans forward," "freezes expression," "shifts to character posture," "scans audience"]
timing: [before | on | after | during] the text
load: [supports | carries | independent]
```

The `load` field is critical:
- **supports** — physical move reinforces the text. Gesture illustrates the
  act-out. Joke works without it but lands harder with it.
- **carries** — physical move IS the comedy. Text alone would be flat. The
  laugh requires the delivery. This is where the visual system MUST do work.
- **independent** — physical move is funny on its own, separate from text
  content. A physical bit between structural events.

`carries` observations are the highest-value data — they identify exactly
where text-only delivery fails.

### What to watch for

**Capture:**
1. Text-thin, laugh-big moments — text is flat on the page, big laugh in
   performance. What is the body doing?
2. Deliberate stillness — comedian's physical state DOESN'T change where
   you'd expect a reaction. Note as `physical: stillness/no change` with
   `load: carries` if doing work.
3. Act-out physicality — posture/voice shift to become a character. How much
   is physical vs. vocal?
4. Physical timing relative to laugh — does the gesture come before the
   punchline word (anticipatory), on it (synchronous), or after (reactive)?
5. Recurring physical patterns across jokes — physical "signature moves."
6. Audience scan / check-in moments — comedian breaks from material to look
   at audience mid-bit.

**Skip:**
- General stage movement (walking, mic adjusting) unless timed to structural
  events
- Natural conversational hand gestures that aren't distinctively timed
- Audience interaction outside the bit structure

### Episode selection for sample

Pick 3-5 episodes for variety:
- One where Jerry is relatively still (early Season 1)
- One with extended act-outs (E03 "The Robbery" — the toe bit)
- One with character voices (E07 "The Pony Remark" — leisure police)
- One with a sustained premise (E08 "The Jacket" or E11 "The Statue")

### How the data feeds into the vocabulary

After collection, cluster the physical observations:
1. Group by type of physical move (expression changes, posture shifts,
   stillness, audience interaction, etc.)
2. Note which clusters map to which structural events most often
3. Note which clusters are `carries` vs. `supports`
4. These clusters become the empirical basis for the visual device categories

The 16 devices listed below are the current theoretical proposal. The
empirical data may confirm them, reveal gaps, or show that some proposed
devices don't actually occur in practice. The vocabulary files should NOT
be finalized until the sample data is collected.

### Integration with the audit protocol

Physical performance observations are collected DURING the existing audit
pass (when the user is already watching performances to verify laugh points
and check annotations). They are a third data stream alongside:
1. Laugh-point verification (audio)
2. Annotation review (text/structural)
3. Physical performance observations (visual) ← new

These observations are saved to `working/physical_performance_notes.md`
(one section per episode) and reviewed after the sample is complete to
derive the vocabulary categories.

## What to Create (after Step 0 data collection)

### File 1: `engine/vocabularies/visual-devices.yaml`

16 visual devices across 4 categories, each with full vocabulary definition (criterion, positive_example from a game/editing technique, negative_example, distinguished_from).

**Expression & Pose (3 devices):**
- `pose_shift` — character transitions between discrete pose states (Ace Attorney witness breakdowns)
- `expression_change` — facial expression changes via modular layers (VN sprite swaps)
- `idle_break` — brief reactive motion interrupting idle (blink, twitch, shrug)

**Camera & Frame (5 devices):**
- `zoom` — camera toward/away from focal point. Params: direction (in/out), speed (snap/ease)
- `screen_shake` — frame vibrates. Param: intensity (subtle/medium/strong)
- `cut_in` — panel/inset intrudes into frame, Persona-5-style (aggressive spatial disruption)
- `split_frame` — screen divides to show two things simultaneously
- `freeze_frame` — action halts for beat/pause punctuation

**Text & Typography (4 devices):**
- `text_speed_change` — text reveal speed changes (Undertale's primary comedy tool)
- `text_emphasis` — specific words get visual treatment (bold, color, size, shake)
- `text_style_break` — overall text style shifts (font change, all-caps, handwritten)
- `text_overlay` — text as spatial element on scene (floating labels, JonTron-style)

**Environmental & Supplementary (4 devices):**
- `stock_image_drop` — contextual or contrasting image appears in frame
- `sound_sting` — brief sound effect synchronized to visual moment
- `transition_effect` — stylized scene transition (the transition itself can be comedic)
- `vfx_overlay` — visual effect layer (speed lines, impact stars, sweat drops — manga/anime visual language)

### File 2: `engine/vocabularies/visual-timing.yaml`

6 timing values that anchor visual devices to structural events:
- `on_event` — fires when structural event begins (synchronous)
- `before_event` — fires during pause/gap before event (anticipatory)
- `after_event` — fires after event has landed (reactive, post-laugh)
- `during_event` — sustained throughout event's duration
- `on_pivot` — fires at the specific pivot word/phrase (finer than on_event)
- `sustained` — persists across multiple events (start + end params)

### File 3: `engine/vocabularies/visual-content-rules.yaml`

5 content alignment values (described above): `content_aligned`, `register_aligned`, `contrasting`, `punctuating`, `meta_commentary`.

### File 4: `engine/performers/mort.yaml`

Audio defaults (from existing annotations and spec characterization) + visual defaults:
- Signature visual moves: stillness-as-comedy (no expression change at punchline), delayed blink, slow zoom-out, text pause delivery
- Forbidden visual devices in default register: vfx_overlay, cut_in, text_style_break
- Register-break visual devices: screen_shake, snap_zoom (reserved for subversion moments)

### File 5: `engine/performers/cece.yaml`

Audio defaults + visual defaults:
- Signature visual moves: escalation cascade (stacking devices across beats), cut-in reveal (at sudden specificity), stock image literalization (for anthropomorphized concepts), text-as-entity (Capitalized Proper Nouns get special treatment), energy spike (multi-device burst at punchline)
- No forbidden devices — Cece can use everything
- Register-break visual devices: deliberate stillness, long text pauses (her subversion is going quiet)

### File 6: Schema update in `engine/schema.yaml`

Add `performance.visual` block with:
```yaml
visual:
  cues: []            # list of {device, at, timing, parameters, content_rule, gloss}
  performer_visual_profile: ""
  deviates_from_performer_visual_default: null
```

Note: Visual cues for the game's AI comedians are GENERATED by the
realization stage. But for annotations of human standup, a GLOSS sub-field
captures observed physical performance moves. This observed data grounds
the generative vocabulary — the game's visual devices are derived from
real comedian physical performance, not invented theoretically.

```yaml
visual:
  physical_performance: ""   # [GLOSS] observed physical moves from source
                             #   performance, anchored to structural events.
                             #   Populated during Pass 3 (audit/performance).
                             #   Format: "{at}: {physical move} ({timing}, {load})"
  cues: []                   # [STRUCTURED] generated visual direction for
                             #   AI comedian delivery. Null for source
                             #   material annotations.
  performer_visual_profile: ""
  deviates_from_performer_visual_default: null
```

### File 7: Schema changelog entry (v0.7)

Log all additions with structural question answers.

### File 8: Update `working/scaling-path.md`

Add visual delivery vocabulary to the file-read list and note that visual cues are generated, not annotated.

## Structural Event → Visual Device Default Mappings

These go in the performer profiles as default cue sequences.

**Mort defaults:**

| Event | Devices | Content Rule |
|---|---|---|
| premise | `expression_change: neutral` | register_aligned |
| setup | `text_speed_change: measured_pace` | register_aligned |
| punchline | `text_speed_change: pause_before` + deliberate stillness | contrasting |
| tag | `idle_break: blink` (after) | punctuating |
| topper | `zoom: out, slow` (after) | register_aligned |
| act_out | `pose_shift` (rare — this IS a register break for Mort) | content_aligned |

**Cece defaults:**

| Event | Devices | Content Rule |
|---|---|---|
| premise | `expression_change: curious` + `text_speed_change: moderate` | register_aligned |
| setup | `pose_shift: leaning_in` + `text_emphasis: selective` | register_aligned |
| punchline | `zoom: in, snap` + `expression_change: peak` + `sound_sting` + `vfx_overlay` | content_aligned |
| tag | `cut_in` or `stock_image_drop` | content_aligned |
| topper | `screen_shake` + `text_style_break` | content_aligned |
| act_out | `pose_shift: full_commitment` + `vfx_overlay: speed_lines` | content_aligned |

## Verification

1. **Vocabulary completeness**: Take 3 annotated jokes (one articulation, one extension, one mapping) and hand-trace them through BOTH performer profiles. Can the vocabulary express every visual choice you'd want to make? If a choice falls outside the 16 devices, the vocabulary has a gap.

2. **Game reference check**: Can the vocabulary express the key visual comedy moments from Ace Attorney (objection pose + screen shake), Persona 5 (cut-in + screen tear), and Undertale (text speed change + expression swap)? If not, identify the missing device.

3. **Low-effort editing check**: Can the vocabulary express JonTron's stock-image-drop-at-punchline, Dunkey's freeze-frame-zoom, and Internet Historian's deadpan-narration-over-chaos? These are the `stock_image_drop`, `freeze_frame` + `zoom`, and `contrasting` content rule respectively.

4. **YAML validation**: All new vocabulary files parse as valid YAML.

5. **Schema coherence**: The visual block follows the same STRUCTURED/GLOSS conventions and the same performer-default/deviation pattern as the existing performance layer.

## Implementation Order

**Phase A: Data collection (user-driven, during audit)**

1. User audits batch 1 annotations, collecting three data streams in parallel:
   - Laugh-point verification (audio) → `working/laugh_points.md`
   - Annotation review (structural) → v0.6 reclassifications per `working/batch1_reclassification_guide.md`
   - Physical performance observations (visual) → `working/physical_performance_notes.md`
2. After 3-5 episodes of observations, review the physical performance data
   together. Cluster the observations into categories. Compare clusters
   against the 16 proposed devices — confirm, gap-fill, or prune.

**Phase B: Vocabulary creation (after data validates categories)**

3. Create `visual-devices.yaml` — finalized device list with full definitions,
   grounded in the observed physical performance data
4. Create `visual-timing.yaml` and `visual-content-rules.yaml`
5. Create `mort.yaml` and `cece.yaml` performer profiles (audio + visual defaults)
6. Add `performance.visual` block to `schema.yaml`
7. Log in `schema-changelog.md` (v0.7)
8. Update `scaling-path.md` and `protocols.md`

**Phase C: Validation**

9. Hand-trace 3 annotated jokes through both performer profiles — can the
   vocabulary express every visual choice? Do the `carries` observations
   from Step 0 all have corresponding visual devices?
10. Cross-check against game references (Ace Attorney, Persona, Undertale)
    and low-effort editing references (JonTron, Dunkey)
11. YAML validation on all new files
