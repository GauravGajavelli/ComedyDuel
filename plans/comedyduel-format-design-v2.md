# ComedyDuel: The Quest to Build a Superfunny AI

## The Frame

You're trying to build an AI that's actually funny — not AI-funny, but structurally, genuinely funny. Everyone has experienced the gap between current AI comedy and real standup. You're working on closing that gap and showing your work.

This frame doesn't fabricate a narrative around the engine. It names what you're already doing in a way anyone can understand. The schema work, the annotation, the pipeline architecture — that's the quest. Every piece of public content is a byproduct of work you're already doing: building the engine, documenting what you learn, and testing what it can do.

The frame solves the audience-investment problem without requiring character personality, interactive AI, or production overhead beyond the project itself. The audience comes back because they're following a quest with real difficulty, real setbacks, and real milestones — not because they have a parasocial relationship with Mort or Cece.

---

## Relationship to Other Documents

This document is the **current active plan** for the project.
Other files in `plans/` and `spec.md` are preserved as research
history that informed the current framing:

- `spec.md` — original product framing (browser game, party mode,
  watch mode v1.2). Set aside; banner notes status. Architectural
  references and the comedian roster (Mort, Cece) remain valid.
- `plans/game-mechanics.md` — game-design exploration that
  surfaced engine properties (operation-conditioned generation,
  fail-forward delivery, transition lines, performer dynamic)
  that survive as engine architecture. Banner marks it historical.
- `plans/monetization-plan.md` — full audit of four monetization
  frames (game, YouTube channel, continuous Twitch stream, B2B
  engine licensing) with a Resolution section landing on
  engine-as-creative-work + optional showcase deployment. This
  document refines that resolution.
- `plans/visual_performance.md` — visual delivery vocabulary plan.
  Still live; the constrained subset (static portraits + simple
  animation) is the format for content production under v2.

### How v2 relates to the showcase deployment

The monetization-plan resolution preserved a Nothing, Forever-style
continuous stream as an optional ambient deployment surface. v2
**coexists with that showcase**, not in opposition to it.

- The **continuous showcase** is the engine running in public.
  Lo-fi baseline (static portraits, TTS, deterministic moderation
  filter), produces hours of raw material, exists as the project's
  ambient public face. NOT the primary content surface and not
  optimized for retention or discovery.
- **v2's content** is the editorial layer on top of that material.
  Workshop entries, autopsies, voice swaps, gauntlets, endurance
  runs, and milestone demonstrations are produced by selecting and
  reframing what the engine generates — whether on the showcase or
  in dedicated test runs.

Both surfaces are deployments of the same engine work. Neither
requires the other to function: v2 can produce content without a
running showcase if the engine is run privately for tests. The
showcase can run without v2 content being produced. They reinforce
each other when both are active without depending on each other.

The discipline boundary established in the monetization-plan
resolution applies to both: neither surface is optimized for viewer
counts, retention, or audience growth. If that discipline slips on
either surface, the project has drifted into product posture and
should be reconsidered.

---

## Why This Frame Works

**Progress is inherently watchable.** The Neuro-sama arc that drives audience retention isn't personality — it's incremental capability. She learns to see. Her voice improves. She gets a 3D model. The audience watches her get better and the milestones land because they remember what she couldn't do before. Your version: the engine's comedy output gets more structurally sophisticated over time, and the audience perceives the improvement because you've been showing them the machinery all along. They watched you annotate Seinfeld. They watched you build the concept graph. They saw the joke that collapsed because callbacks didn't exist yet. Then they see the joke where the callback works and they understand why that's hard.

**Current limitations are features of the narrative, not problems to hide.** A joke that falls flat isn't a content failure — it's a data point. The engine over-relying on one rhetorical template isn't embarrassing — it's the current obstacle. DougDoug's best content works the same way: the interesting part is never "the AI succeeded," it's "here's what happened when the AI collided with this constraint." His "Ai Comedy Bot that kept getting depressed" hit 4.1M views not because the bot was funny, but because its failures were interesting and Doug's reactions to them were genuine.

**It unifies both content tracks.** Dev Days aren't a separate technical niche — they're behind-the-scenes on the quest. Test videos aren't a separate entertainment product — they're field tests. Same journey, different vantage points, same audience growing into both.

**It's honest.** You are trying to build a superfunny AI. The frame doesn't require you to perform enthusiasm you don't feel, manufacture stakes that don't exist, or pretend the engine is further along than it is. Honesty about difficulty and setbacks is what makes quest narratives compelling.

---

## What the Content Actually Is

All content is a byproduct of three things you're already doing:

### 1. Working on the engine

You annotate comedy. You refine the schema. You adjust voice constraints. You expand the concept graph. You tune the pipeline. Some of this is interesting to watch or narrate after the fact. When it is, you document it.

**What this produces:**

- **Workshop entries.** You annotated a Seinfeld bit and discovered something about how negation operations interact with callbacks. You record yourself walking through it, or write it up, or screen-record the annotation process. No additional work beyond what you were already doing plus the act of recording or narrating.

- **Autopsy entries.** You decomposed a famous joke through the 9-layer schema and the engine attempted a structural sibling. The comparison between the original and the generated sibling reveals something about the schema's explanatory power. This is work you'd do anyway to validate the schema — making it visible is the only added step.

- **Voice swap entries.** You ran the same material through Mort's constraints and Cece's constraints and the difference was revealing. Showing both outputs side by side with brief commentary on what the constraints did is minimal effort beyond the generation you already performed.

### 2. Documenting what you learn

You're building a structured analytical framework for comedy. Findings accumulate. Some are interesting to a general audience ("here's what I learned about why deadpan timing can't carry escalation patterns"). Some are interesting to a technical audience ("the concept graph's attested adjacencies explain why the engine defaults to food metaphors"). When a finding is worth sharing, you share it.

**What this produces:**

- **Devlog / blog entries.** Written documentation of interesting findings. No production overhead — just writing about what you learned, which you'd arguably do anyway for your own records.

- **Schema explainers.** When a piece of the framework reaches a stable, interesting state, you explain it. The 9-layer schema, the cognitive operations, the rhetorical templates — these are genuinely novel and worth communicating. An explainer is a one-time effort per concept that serves both the general audience and the academic track (ACL/EMNLP/CHI).

### 3. Testing what it can do

You run the engine. You see what it produces. You evaluate whether the output demonstrates the structural properties you're trying to achieve. Some test sessions are interesting. When they are, you capture them.

**What this produces:**

- **Gauntlet entries.** You pick a premise, run it through multiple cognitive operations and rhetorical templates, and see what the combinatorial space looks like. You'd do this anyway to evaluate the engine — the only added work is recording your reactions and selecting the interesting outputs for presentation.

- **Endurance runs.** You push the engine on a single topic to find where it starts repeating. The degradation curve tells you something about the concept graph's coverage and the template distribution's diversity. You'd run this test anyway — narrating it is the added step.

- **Constraint escalation entries.** You progressively add constraints to a generation task and find where the engine breaks. This is quality-assurance work on the pipeline. Making it visible is the format.

- **Milestone demonstrations.** When something new works — callbacks, running premises, a new voice constraint that holds — you show the before and after. "Last month the engine couldn't do X. Here's what changed and here's what it produces now." This is the progress-tracking the quest narrative runs on.

---

## What Mort and Cece Are in This Frame

They're not personalities. They're not interactive agents. They're the engine's two voices — maximum stylistic contrast that makes the engine's structural properties audible. When you run a test, you often run it through both, and the difference between their outputs is one of the most legible ways to show what voice constraints do.

The audience will develop preferences. Someone will like Mort's deadpan more than Cece's energy, or vice versa. That's fine and it happens naturally without you building relationship dynamics or interaction systems. Mort and Cece are instruments you play, not characters you maintain.

If the audience develops attachment to them, that's emergent and welcome. But the project doesn't depend on it and you don't engineer for it.

---

## Effort Model

### What you're already doing (no change)
- Annotating comedy (Seinfeld episodes, corpus expansion)
- Refining the schema and pipeline
- Tuning voice constraints
- Running the engine and evaluating output
- Expanding the concept graph

### What's added (minimal)
- Recording or screen-capturing some work sessions
- Writing up interesting findings (devlog/blog)
- Narrating test results with genuine reactions
- Selecting and lightly editing interesting outputs for presentation
- Occasional milestone demonstrations when something new works

### What's explicitly not added
- Character personality or interaction systems
- Audience interaction infrastructure (voting, real-time chat integration)
- Persistent narrative state or career progression mechanics
- Production-grade video editing or custom tooling per video
- A content schedule or regular cadence obligation
- Any work done primarily to serve the public surface rather than the engine

### Engine extensions this format does not require

Past planning conversations surfaced engine extensions that would
be necessary under different formats. v2's quest-framing format
**does not require any of them**, and naming them explicitly
prevents future drift toward building them because they "feel
like they should be there":

- **Between-bit personality generation.** Mort and Cece talking
  between jokes, in-character observations during transitions —
  required for ambient watching, not for v2's premise videos.
- **Ambient state model.** Cold/warm audience meter, performer
  delivery shifting based on session arc — required for live
  performance feel, not for documented engine tests.
- **Ensemble seasoning / interruption logic.** Cece interrupting
  Mort's set, banter dynamics — required for variety-shape
  content, not for voice-comparison videos.
- **Audience-reaction simulation.** Stochastic laugh sizes,
  silences, hecklers — required for performance ambient texture,
  not for engine evaluation.
- **Active narrative-layer scheduling.** Engine periodically
  trying callbacks, proposing running premises — useful for long
  ambient sessions, not for premise-driven content where
  callbacks happen when material justifies them.

This is a positive constraint: engine work stays focused on the
schema, annotation corpus, voice constraints, concept graph, and
core pipeline. The only infrastructure investment that is
non-optional under v2 is the **performance layer** (TTS with
cadence/pause/register support honored as part of generation),
because cadence and timing are load-bearing for standup content
and the audience cannot evaluate structural work if delivery is
flat.

If a future engine extension feels appealing, the test is: does
it serve a v2 content type that you actually want to make, or is
it serving an imagined ambient-watching format that v2 has
explicitly chosen not to pursue?

### Comparison to reference projects

**Vedal / Neuro-sama:** Full-time engineering on a real-time AI streaming system. Custom TTS, avatar rigging, game integration, filtering pipeline, chat processing. Content is produced continuously on a regular stream schedule. ComedyDuel requires none of this infrastructure and no streaming obligation.

**DougDoug:** Custom tooling and game mods per video. Heavy post-production editing. Challenge design as creative work separate from the tool itself. CS degree from Berkeley, former EA programmer — significant technical capability applied to production. ComedyDuel's "challenge design" is just the tests you'd run on the engine anyway. Editing is light — show the interesting parts, narrate briefly, move on.

**ComedyDuel:** The engine work is the project. Public content is documentation and testing made visible. The only production skill required beyond what you're already doing is the ability to narrate your work engagingly — to explain what you're trying, what happened, and why it's interesting. That's closer to an academic giving a good talk than to a content creator running a channel.

The honest ceiling: this approach produces content irregularly, at the pace of genuine findings and milestones rather than a schedule. The audience grows slowly. Individual pieces may get traction if the premise is accessible ("I made my AI write the same joke 50 different ways" is a clickable title), but there's no growth engine beyond the work being interesting. That's the correct tradeoff for a project where the engine is the artifact and public surfaces are deployments of it.

---

## The Progress-and-Setbacks Question

The quest frame implies the AI gets funnier over time. The honest trajectory of any research-grade system is that some dimensions improve while others plateau, regress, or reveal new problems. This needs to be part of the narrative, not hidden from it.

"The callbacks got better but the engine started over-relying on one rhetorical template" is a compelling entry in a quest narrative. "I thought I solved voice coherence but it breaks when the premise requires emotional register shifts" is an interesting setback. The audience follows the quest because the problem is genuinely hard and watching someone work through hard problems honestly is inherently engaging — if, and only if, the narrator is honest about difficulty.

**Regressions are content, not failures to hide.** When a change
causes the engine to get worse in some dimension, that's a
documentation moment, not something to roll back quietly and
pretend never happened. "I added X to improve Y but it broke Z"
is exactly the kind of entry that makes the quest credible.
Linear narratives of "everything keeps getting better" read as
manufactured because real research never works that way.

**Dead ends are content.** Approaches that didn't pan out, ideas
that seemed promising but turned out to be wrong, schema
revisions that had to be reverted — all of these are honest
material. The temptation will be to skip past them in narration
because they feel like failures. Resist that. The skip is what
fakes the quest.

**Smoothing setbacks into "lessons learned" is the failure mode.**
There's a difference between "I learned X from this setback"
(true, useful, content-worthy) and "this was actually a stepping
stone toward Y" (often retrospective rationalization that erases
the realness of being stuck). The first is honest; the second is
a narrative trick the audience can usually feel even if they
can't name it. The discipline is to leave setbacks unresolved in
narration when they're actually unresolved.

The failure mode to avoid: implying linear progress toward a destination when the actual work is exploratory. The frame should be "I'm trying to figure out if this is possible and how far I can get," not "watch me build the finished product step by step." The first is a quest. The second is a tutorial series, and the engine isn't far enough along to sustain that.

---

## Decision Framework (Revised)

When considering whether to make something public, ask:

1. **Did I learn something interesting while working on the engine?** If yes, it might be a devlog entry, workshop recording, or autopsy. The test: would you want to tell a friend who cares about comedy or AI about this finding?

2. **Did a test session produce interesting output?** If yes, it might be a gauntlet, endurance run, or constraint escalation entry. The test: is the interesting part the output itself, or the structural reason the output turned out this way? If only the former, it's a clip. If the latter, it's content.

3. **Did something new start working (or stop working)?** If yes, it might be a milestone demonstration or setback entry. The test: can you show a before-and-after that makes the change legible to someone who's been following along?

4. **Am I doing work primarily to produce content rather than to improve the engine?** If yes, stop. The dependency has flipped.

5. **Am I sitting on interesting findings because I'm waiting for them to be polished enough?** If yes, share them rough. The quest narrative rewards honesty and work-in-progress over production value. A screen recording with narration is fine. A blog post with code snippets is fine. The work is the artifact, not the presentation.

---

## Formats That Survive, Formats That Don't

**Survive as engine work made visible:**
- Workshop (annotating, adjusting, running — record some sessions)
- Autopsy (decompose a real joke, generate a sibling — work you'd do anyway)
- Voice Swap (run both voices, compare — a test you'd run anyway)
- Gauntlet (combinatorial exploration of operations × templates — evaluation work)
- Endurance Run (push until repetition — quality assurance)
- Constraint Escalation (progressive difficulty — stress testing)

**Don't survive without personality/interaction systems:**
- Roguelike Run (requires character responding to career trajectory)
- Crowd Work Challenge (requires reactive capability, real-time adaptation)
- Sibling Rivalry as relationship content (requires character dynamics beyond voice contrast)
- Any format requiring Mort or Cece to "react" to anything

**Don't survive without production overhead beyond the project:**
- Competition show with rotating comedians
- Any format requiring a content schedule
- Any format requiring custom tooling built for the format rather than the engine

---

## Pitfalls (Revised)

- **The content schedule trap.** The quest narrative works because entries arrive when there's something worth sharing. The moment you commit to regular uploads, you start doing work to fill the schedule rather than documenting genuine progress. No cadence. No promises. Share when there's something to share.

- **Performing progress you haven't made.** The quest frame creates pressure to show forward motion. If a month of annotation work didn't produce a visible capability improvement, that's fine — the entry is "here's what I learned about why this is harder than I thought," not silence followed by a forced milestone.

- **Building the narrator instead of the engine.** If you find yourself spending more time on presentation, editing, scripting, or audience strategy than on annotation and pipeline work, the dependency has flipped. The narration should be the easiest part — you're just describing what you did and what happened.

- **Letting "superfunny" become a product promise.** The frame is a quest, not a guarantee. "I'm trying to figure out how far I can push this" is sustainable. "I'm building the funniest AI" creates expectations you'll need to manage. The language should stay exploratory.

- **Skipping the performance layer.** Unlike Neuro (where janky TTS is charm) or DougDoug (where AI output is often text), your output is performed standup. Cadence and timing are load-bearing. If the TTS doesn't support the comedy structure, the audience can't evaluate whether the structural work is landing. This is the one piece of infrastructure investment that's non-optional even under a minimal-effort model, and it's worth disproportionate attention relative to everything else on the production side.

---

## Visibility Moves Outside v2's Content Model

v2 covers the content the project produces about its own work. A
few additional minimum-effort visibility moves stand alongside v2
— they aren't content in v2's sense, but they let the work exist
in different surfaces:

- **Public GitHub repo** with schema, vocabularies, anonymized
  annotations, README. Discoverable by people searching for humor
  classification, comedy NLP, structural humor analysis.
- **Academic workshop submission** on the schema. The 9-layer
  schema with structured/gloss split is a publishable
  contribution at workshops at ACL, EMNLP, or CHI.
- **Comedy-community presence.** Sharing relevant findings in
  comedy-writing Discords, subreddits, or communities of people
  who think about how jokes work. Don't pitch; contribute when
  you have something specific to say.
- **Twitter/X threads** when annotation surfaces a vocabulary
  gap, a clean operation distinction, or a generated bit that
  landed unexpectedly.

Total cost of these alongside v2: a few hours per month. They
reach the small specialist audience that would value the work
without requiring sustained acquisition motion.

These do not replace v2's quest-framed content; they parallel it.
v2 reaches people who care about the journey and the test
results. These reach people who care about the artifacts
themselves.

---

## Single-Sentence Summary

The engine is the project; the quest to build a superfunny AI is
the public frame; content is a byproduct of engine work selected
and reframed honestly (including regressions and dead ends); the
showcase deployment runs as an ambient lo-fi baseline alongside
v2's content; no schedule, no audience-acquisition motion, no
viewer-count metrics, no engine extensions for ambient watching;
the engine work is the artifact and the work is justified by
being interesting to do.
