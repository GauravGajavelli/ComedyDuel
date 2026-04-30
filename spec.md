# Comedy Duel — Product & Technical Spec (Revised)

*Working title. Solo-first MVP with 2 comedian characters. Party mode deferred to v1.1.*

> **Status (2026-04-29) — current plan is `plans/comedyduel-format-design-v2.md`. This spec is historical.**
>
> The active plan for this project is **`plans/comedyduel-format-design-v2.md`**,
> which frames the project as **the quest to build a superfunny AI** —
> engine work as the primary creative activity, with content produced
> as a byproduct (workshop entries, autopsies, voice swaps,
> gauntlets, endurance runs, milestone demonstrations).
> **Read v2 first.** Everything below is preserved as architectural
> reference and product-thinking history.
>
> This spec describes the original product framing: a browser-based
> comedy game with party-mode v1.1 and watch-mode v1.2 expansions.
> After working through the game design (`plans/game-mechanics.md`)
> and four monetization frames (game, YouTube channel, continuous
> Twitch stream, B2B engine licensing — see
> `plans/monetization-plan.md`), the project has been reframed.
>
> **Primary framing: engine-as-creative-work.** The schema,
> annotations, operation taxonomy, performance-layer integration,
> and concept graph are the work. The motivation is creative
> enjoyment of the structural decomposition of comedy, not
> commercial outcome. Each monetization frame surfaced real
> obstacles the engine wasn't designed to solve, because the
> engine wasn't designed for monetization — it was built because
> the work is intrinsically interesting. Continuing to audition
> product frames was distorting the engine work without changing
> payoff probability materially.
>
> **Optional layer: showcase deployment.** A Nothing, Forever-style
> continuous Mort/Cece standup stream is preserved as a bounded
> low-effort public-facing surface for the engine. Lo-fi static
> portraits with mouth animation, TTS-voiced standup, deterministic
> output filtering for moderation, autonomous performance with no
> real-time human direction. This is essentially a revived form of
> the original spec's v1.2 watch mode, deployed as a showcase
> rather than as a product expansion. It's the closest format to
> what the engine was actually designed for and the lowest-burden
> way to give the engine a public face.
>
> **Three coexisting public surfaces (additive layers above the
> showcase).** The showcase deployment is the lowest-effort
> surface. Above it, two additional content tracks are
> operationalized in `plans/comedyduel-format-design-v2.md`:
>
> - **Dev Days** — Vedal-shape technical content (schema
>   walkthroughs, live annotation, structural decomposition).
>   Replaces the text-form devlog from the monetization-plan
>   resolution as the primary technical-visibility surface.
> - **Narrative Challenges** — DougDoug-shape premise videos
>   (character-driven entertainment with the engine as subject).
>
> The three surfaces coexist without competing. Together with the
> GitHub repo, occasional social posts, comedy-community
> presence, and an optional workshop paper on the schema, they
> form the complete public face of the project. See
> `plans/comedyduel-format-design-v2.md` for the full format
> catalog, the format-prerequisites table (Tier 1 buildable
> today, Tier 2 light extensions, Tier 3 texture-of-sustained-
> performance extensions), and the decision framework for
> evaluating new format ideas.
>
> The discipline boundary is explicit: **the showcase is a
> deployment surface, not a product.** It runs when the engine is
> producing well, gets shut down when it stops being enjoyable to
> maintain, and is not optimized for viewer counts, retention, or
> any other audience-acquisition metric. If audience-acquisition
> work, retention optimization, scheduled content drops, or treating
> viewer counts as success creeps in, the discipline has slipped
> and the showcase has quietly become a product that should be
> reconsidered against the creative-work framing.
>
> This spec remains useful as **architectural reference** and as a
> record of product thinking that informed the engine design.
> Concepts that survive: the comedian roster (Mort, Cece) as
> voice-constraint test cases and as showcase performers; the
> three-stage pipeline as the generation architecture; the schema
> and vocabulary work as the core artifact; v1.2 watch mode as the
> showcase basis. Concepts that are no longer pursued: the game
> modes, party mode, v1.1 party-product expansion, full
> distribution plan, success metrics framed as user counts,
> monetization sequencing.
>
> If a substantive product path opens later (inbound interest, a
> clear shape that hasn't been considered, a collaborator who fits
> a path none of the above), revisit then. Optionality is preserved
> by continuing to build the engine cleanly and by the showcase
> giving the work a public face that can be referenced; active
> product planning is not required to keep that optionality alive.
>
> See `plans/monetization-plan.md` (and its closing Resolution
> section) for the full reasoning on why the four monetization
> frames were considered and set aside, and how the engine-as-
> creative-work + showcase posture was arrived at.

## Product thesis

A browser-based comedy game where a single player competes against AI comedian characters with distinct voices and personalities. Play solo to develop your comedic writing, test yourself against the AI, and build history with specific comedians over time. Party mode (3–8 players) ships as v1.1 expansion.

The core differentiator: AI comedians that are *actually* different from each other and genuinely competitive opponents, not just flavored LLM outputs.

## Why solo-first

- Cuts multiplayer infrastructure from critical path (saves 2–3 weeks)
- Easier to playtest alone during development
- Cleaner single-URL launch: one user, one experience, no coordination required
- Matches your personal engagement needs (practice mode as a real destination)
- Lower social-cold-start risk (no need to round up 4 friends to try it)
- Produces shareable single-user content (screenshots, result cards) without multiplayer
- Validates the humor engine first; multiplayer adds complexity, not core value

## Execution phasing

This project ships in three phases separated by explicit go/no-go gates. The phasing exists because the risk is structured: the architecture might not describe how jokes actually get made; the implementation might not match the architecture; the product might not reach users. Each phase isolates one risk and refuses to proceed until it's cleared.

The architecture is a multi-stage pipeline, not an LLM wrapper. Current sketch: a **discovery** stage (graph-based, surfaces candidate concepts and observational connections), a **selection/structuring** stage (commits to a joke shape, voice, and structural template, applying subversions where the material invites them), and a **realization** stage (LLM renders the final sentence under tight constraints from the previous stages). The details continue to evolve; the phasing below is designed to accommodate further architecture refinement without wasted implementation work.

**Phase 0 — Architecture validation on paper (~1 week).** No code. Produce a design document for the humor engine, then validate it by hand-tracing 10 prompts through all three stages: play the graph, play the selector, and write the final sentence as the LLM would under your constraints. Compare each hand-traced output against what you'd write freely given the same prompt and voice target. The test is harsh on purpose: if the architecture doesn't reliably produce outputs at least as good as your free-writes, no implementation will save it. If the hand-trace keeps stalling because the schema doesn't cover cases that come up, the abstraction is leaking. This phase also produces the seed artifact you'll need anyway — 15–20 reference jokes decomposed into the pipeline's intermediate representations.

**Gate 1.** Architecture produces hand-traced output at least as good as your free-writes, and the schema covers the joke types you're targeting → proceed. Architecture produces worse output, or fails to cover common cases → iterate on the design or abandon. This is the most consequential gate in the project.

**Phase 1 — Minimal end-to-end implementation (~1–2 weeks focused).** One comedian (Mort), one prompt category, a seed graph of 50–100 nodes, 3–5 structural templates, one voice constraint set, one LLM-as-renderer call. Run it on the same 10 prompts from Phase 0 and verify the implementation's output matches (or justifiably deviates from) the hand-traced output. The purpose is to confirm the architecture actually runs correctly as code — not to build a product. No UI polish, no persistence beyond local files, no second comedian, no critic, no game modes.

**Gate 2.** Implementation agrees with hand-trace and holds up on 30+ unseen prompts → proceed. Implementation consistently diverges from hand-trace, or quality collapses outside the original 10 prompts → debug the pipeline or revisit Phase 0.

**Phase 2 — Full MVP build (~4 weeks focused, or equivalent side-project time).** Everything else: Cece, critic AI, all three game modes, expanded prompt library, result cards, moderation, distribution prep, launch. Because the architecture and its minimal implementation are validated, this phase is execution work rather than exploration.

## Target users

**Primary:** Anyone who wants to test or develop their comedic writing. Includes: aspiring comics, comedy writers, people who want to be funnier in their communications, humor enthusiasts, fidget-adjacent users who'd play a few rounds during downtime.

**Secondary (post-MVP):** Party hosts wanting AI opponents for group play (v1.1).

**Not targeting:** Passive entertainment seekers (go to TikTok), grinders wanting infinite progression, kids.

## Core loop

1. User lands on site, picks a comedian opponent (Mort or Cece)
2. Round begins: prompt appears
3. User writes their response (soft time pressure: 60–90 seconds suggested, not enforced hard)
4. AI submits its response (in character for chosen comedian)
5. Both responses displayed side-by-side
6. Critic AI picks a winner with short reasoning
7. Optional: user can override critic's call if they disagree
8. Comedian character delivers in-voice reaction (1–2 sentences)
9. Round ends; user can play another, switch comedians, or share result

Match structure options:
- **Quick Duel:** Single round, 60–90 seconds total. Default for first-time users.
- **Practice Session:** User-chosen length (3, 5, 7, or 10 rounds). Running score.
- **Gauntlet:** Play through a series against one comedian with escalating prompt difficulty. Endgame highlight reel.

## The comedian roster (MVP: 2 characters)

### Mort

- **Persona:** Dry, world-weary, observational. Norm Macdonald's timing with Mitch Hedberg's brevity. Early 50s, been at it forever, has seen things.
- **Humor style:** Short punchlines, misdirection, gentle absurdism. Prefers literal interpretations of idioms. Willing to deliver a terrible pun with zero apology.
- **Signature moves:** "I'll tell you what" as a setup. Delivers observations as if reporting facts. Occasionally lets a pause do the work.
- **Voice tics:** Understatement, deadpan factual framing, occasional "so there's that."
- **Trash-talk register:** Mild. When he wins: "Yeah, that one worked out." When he loses: "Fair. Good one." Never mean.
- **Subject preferences:** Domestic life, institutions (airports, hospitals, DMV), mundane absurdity.
- **Avoids:** Topical political material, anything requiring energy.

### Cece

- **Persona:** High-energy absurdist. Maria Bamford's range with a pinch of Demetri Martin's geometric whimsy. Late 20s, caffeinated, sees the world sideways.
- **Humor style:** Surreal juxtaposition, maximum imagery, sentences that start reasonable and end in sincere weirdness. Will commit fully to a bit.
- **Signature moves:** Escalation through specific absurd details. Anthropomorphizing objects. Pretending a feeling is a small animal living in a cupboard.
- **Voice tics:** Exclamation, sudden specificity, capitalized proper nouns for absurd concepts ("the Little Guilt that lives in my kitchen drawer").
- **Trash-talk register:** Enthusiastic. When she wins: "HA! I KNEW it! I KNEW that was going to land!" When she loses: "Oh that's so good I'm furious." Never bitter.
- **Subject preferences:** Internal mental states, inanimate objects with personalities, minor household chaos.
- **Avoids:** Dry factual observations (her territory is the opposite).

**Why these two specifically:** Maximum stylistic contrast with minimum moderation risk. A user trying Mort and then Cece back-to-back should feel like different opponents in ways that matter structurally, not just cosmetically.

## Unlock and progression structure (MVP)

Both comedians available from first session. No unlock gate for MVP scope.

*Forward-looking note (v1.1+): When more comedians are added, practice mode may gate newer comedians behind first-match completion with existing ones. Party mode will always have all comedians unlocked for hosts. This keeps party mode welcoming while giving solo mode light progression hooks later.*

## Game modes (MVP)

### Quick Duel
Entry point for new users. One round, one comedian, result card at the end. Shareable via unique URL. Designed for cold-start virality: a friend sends the link, someone plays once, either shares or converts to Practice Session.

### Practice Session
User-chosen length (3, 5, 7, or 10 rounds). Pick one comedian for the whole session or let them alternate. Running score. Session ends with highlight reel of user's best submissions and favorite comedian moments.

### Gauntlet
One comedian, 10 rounds, prompts escalate in difficulty (from fill-in-blank to multi-beat scenarios). Points multiply in later rounds. Ends with "you beat Mort in the Gauntlet" or similar achievement. More ambitious session, ~15 minutes.

## Prompt library

MVP target: **60 hand-curated prompts at launch**, organized by type:

- **Fill-in-the-blank** (~15): "The absolute worst thing to say on a first date is ___"
- **Scenario completion** (~15): "Describe the ad campaign for a cereal made entirely of sadness"
- **Reverse premise** (~10): "Pitch me on why cats are objectively worse than dogs"
- **Advice column** (~10): "A reader writes: my coworker keeps microwaving fish. Advise them."
- **Testimonial/review** (~10): "Write the 1-star Yelp review for heaven"

Every prompt hand-written. No generated prompts at launch.

Each prompt tagged for:
- **Category** (structure type)
- **Register** (clean / medium — no edgy tier for MVP)
- **Character fit** (which comedian this prompt suits)
- **Difficulty** (for Gauntlet progression)

## Judging (Critic AI)

A separate "critic" character — not Mort, not Cece — picks winners in solo mode.

- Short reasoning for the verdict (1–2 sentences)
- Honest about close calls ("these were both good, but X edged it because...")
- Never sycophantic; willing to say "Mort's was better"
- The reasoning is part of the entertainment, not just a verdict

User can override the critic's verdict with a "nah, mine was better" button. This isn't cheating — it's honest user feedback. Capture both the critic's pick and the user's pick as data.

## Shareability

Every round produces a shareable result card:

- Prompt at top
- User's response
- Comedian's response (labeled with their portrait)
- Critic's verdict + reasoning
- Small branding / URL

Cards are square format, Twitter/iMessage-friendly. Generated server-side via Satori or @vercel/og.

Session-level shares: "I played 5 rounds against Mort and won 3 of them" with the 3 winning submissions.

A public feed at `/greatest-hits` shows the week's best user submissions (with opt-in) and the week's best comedian lines. This is free content marketing and gives the comedians their own evolving persona through their best outputs.

## Humor engine architecture

The engine is a three-stage pipeline, not an LLM wrapper. Each stage has a distinct job, a distinct representation, and a distinct failure mode.

### Stages

**Discovery** surfaces candidate conceptual ingredients from a seed graph given a prompt. The graph encodes concepts, their feature-axis coordinates (domain, specificity level, register, emotional valence, physicality), and attested adjacencies drawn from annotated reference jokes. Discovery retrieves concepts and concept pairings that share comedically productive axes with the prompt. Edges are sparse and attestation-based rather than enumerated; retrieval is by feature proximity rather than exhaustive traversal. Output: ranked conceptual ingredients with their feature tags.

**Selection and structuring** commits to one joke shape. It chooses a structural template from a hand-authored library (escalation, reversal, literalization, mundane-as-monumental, false-equivalence, anthropomorphization, etc.), selects which subversions if any to apply, and applies the comedian's voice as a filter over both concepts and templates. Voice here is a *constraint set*, not a style — Mort's voice rejects anthropomorphization-of-feelings entirely regardless of how well the material would support it. Selection also consults recent session history and applies novelty pressure against recently used structural moves, defending against the formulaic trap at the distributional level rather than the per-joke level. Output: concepts + template + voice-move list + any subversion markers.

**Realization** renders the final sentence. This is the only LLM call in the critical path. It receives a tight contract — use these concepts, in this structural template, with these voice moves, without editorializing — and is expected to produce surface form only, not creative decisions. The LLM is a renderer; if it's making structural or selection choices, the contract is too loose.

### Why this split

The formulaic-joke failure mode in current AI systems comes from conflating these stages. LLMs given a voice and a prompt will smooth toward fluency, which is what they were trained for — and fluency is the enemy of comedic surprise. Separating discovery from selection from realization keeps each stage legible, debuggable, and non-magical; each can fail in known ways and be fixed at its own level.

### Representation of joke mechanics

Jokes are decomposed into nine layers: content (domain, concepts, pivot, specificity), logic (setup expectation, punchline violation, incongruity type), structure (template, subversions, tags), performance (cadence, pauses, repetition, duration), voice (persona markers, register, editorialization policy), affective (emotional valence of the joke itself — detached-to-vulnerable, cool-to-agitated, warm-to-cold — rated on bounded axes, with both the comedian's default register and the specific joke's register captured when they diverge), narrative (callbacks, running premises, position in set), relational (positioning, audience implication, vulnerability level, shared-experience requirement and its universality), and meta (form commentary, fourth-wall breaks).

The affective layer is distinct from voice. Voice is identity — who the comedian is while telling the joke. Affect is register — the emotional tone the joke itself inhabits. Jerry's default voice is observational-lateral; Jerry's default affect is detached-and-cool. Maria Bamford's default affect is vulnerable-and-agitated; the same structural template in her voice produces very different outputs from the same template in his. A given joke can also deviate from a comedian's default affect, and those deviations are often where the most interesting humor lives.

A joke annotation is a record across all nine layers. Every field is marked as either **structured** (drawn from controlled vocabularies, bounded scales, enumerated categories, or typed references — the engine computes on these) or **gloss** (free text describing the specific content of this joke, for human readability only — the engine does not use these). The generative sufficiency test operates against structured fields only; gloss fields exist as scaffolding for human review and as a diagnostic for schema holes (a joke whose distinctiveness lives entirely in gloss has revealed a missing structured field). The schema is maintained as YAML for readability, with controlled vocabularies per field maintained in separate reference files under `engine/vocabularies/`. Each vocabulary value is defined by a criterion, a positive example, a near-miss negative example, and contrast pairs against nearest neighbors — see `vocabularies/README.md`.

Concepts in the content layer are typed references to nodes in a knowledge graph (`engine/concepts/`), not bare strings. Each concept node carries its own structured dimensions (domain, specificity, register, valence, arousal, physicality, typicality, era) and accumulates attested adjacencies — concepts that have co-occurred in annotated jokes, with their shared feature axes. Adjacencies are populated from annotation data, not hand-authored. The knowledge graph grows as annotations reference new concepts, and the graph's edges are emergent rather than specified.

Each annotation also records a commutation test: which element is load-bearing (removing it kills the joke, captured as a dotted field-path into the annotation), which elements are removable, and a `voice_portability` field marking whether the joke's moves could be delivered by other voices in the roster.

Annotation itself is assisted by a conversational interface against a tightly-constrained system prompt that captures the annotator's analysis into YAML without proposing content of its own. Annotation runs as a multi-pass workflow (transcription, silent decomposition, aloud performance, commutation test, adversarial review) with each pass operating on a distinct subset of the schema; an `annotation_status` block in each joke's YAML tracks per-pass completion. The schema additionally supports a joke/performance split, optional affective trajectories anchored to structural events, and a `pivot_locus` field distinguishing logical from affective pivots. The system prompt, annotation protocol, pass definitions, and operational procedures are maintained as separate living artifacts alongside the spec rather than inline here — see Working Artifacts below.

### Dependencies and interaction between layers

Layer dependencies are **discovered, not imposed**. The annotation schema stores layers in parallel without encoding which fields constrain which; dependencies are surfaced after sufficient annotation volume by querying for co-occurrence patterns (e.g., "when positioning is lateral_observer, what does editorializes take?"). Discovered dependencies then migrate into the selection stage as constraints. This ordering matters: imposing dependencies before data reveals them tends to encode the annotator's assumptions rather than the comedian's actual patterns.

### Schema evolution principles

Fields evolve empirically during annotation. Each field earns its representation by a set of structural questions applied when it's added, revised, or reviewed during weekly review:

- Can this field take more than one simultaneous value in a single joke? If yes, multi-valued or split.
- Does the value meaningfully change across the duration of the joke? If yes, trajectory representation (start → end, or short sequence) rather than a single value.
- Are the values genuinely ordered, or is a scale being used because it's easy? If not ordered, enumerated kinds.
- Do the "absent" cases and the "low intensity" cases mean different things? If yes, presence + intensity rather than a single scale.
- Does the field's meaning change depending on the value of another field? If yes, split into context-specific sub-fields or encode the dependency explicitly.

Schema decisions at this level of detail (specific field representations, which scales split into orthogonal axes, which booleans become qualified enumerations) live in `engine/schema.yaml` and its changelog, not in this spec. The spec records only the principles.

The schema grows only as long as it earns its complexity. The guardrail is the **fields-used to fields-defined ratio** tracked during weekly review: after a sufficient annotation volume, if many fields are default or blank in most jokes, the schema is overfit to rare cases and the common cases are being starved. Complexity is added when load-bearing for reconstruction, not when theoretically interesting. See `protocols.md` for the tracking procedure.

### Complexity growth

Not all layers are in scope for Phase 0 or the MVP. Complexity grows in a defined order, and each addition has its own gate.

- **Phase 0 / MVP core:** content, logic, structure, voice, affective layers. Sufficient for single-joke output within a single round, with both structural and emotional-register differentiation between Mort and Cece.
- **Phase 2 additions:** performance layer (cadence markers useful even for text-only output), relational layer (already implicit in voice and affective constraints; made explicit for Cece vs Mort differentiation and shared-experience handling).
- **Post-MVP additions:** narrative layer (callbacks across rounds within a session), meta layer (form-commentary subversions), tag generation (smaller follow-up lines appended to main punchlines).

Callbacks deserve specific treatment because they blur the line between "one joke" and "one routine." A callback is not recursion into another joke; it's a *reference* from one joke's narrative layer to a prior joke's identifier, with the referring joke's structure incorporating the prior joke's pivot as a compressed signifier. Session memory holds recently delivered joke signatures; selection can opportunistically propose a callback-template when current material permits. Callback isn't recursion, and the engine shouldn't be built to handle it recursively — it's retrieval plus reference, which is flat.

The unit of composition is the joke (roughly one pivot per unit). Multi-beat routines are *sequences* of jokes linked at the narrative layer, not recursive structures. This keeps the engine's core unit stable even as narrative complexity grows.

### Out-of-distribution output

The graph stores decomposed moves, not jokes. A move learned from Seinfeld ("apply bureaucratic-patience logic to domestic-life situation") applied to concepts Seinfeld never touched produces output that is structurally informed by him but not reproducible from him. The defense against parroting lives at the *concept distribution* level: the graph must be deliberately seeded with concepts beyond any single source's subject matter, or the outputs will feel derivative even when structurally novel. When more comedians' reference jokes are added to the corpus in future phases, each adds both moves and concepts, increasing the compositional space multiplicatively.

## Technical architecture

### Stack
- **Frontend:** Next.js 14+ (App Router), TypeScript, Tailwind
- **Backend:** Next.js API routes
- **LLM:** Claude Sonnet 4.6 as primary. GPT-5 as fallback/comparison during development.
- **Storage:** Postgres via Supabase (free tier sufficient for MVP)
- **Image generation:** @vercel/og for result cards
- **Hosting:** Vercel
- **Analytics:** Plausible or simple self-hosted (avoid Google Analytics for launch)

### Why this stack
No multiplayer = no PartyKit needed. Everything fits on Vercel's free tier at MVP scale. Supabase handles auth-free session storage. Stack is familiar and boring on purpose — save innovation for the humor engine, not the infrastructure.

### LLM integration

Each comedian = system prompt + 8–12 few-shot examples + sampling config (temperature, top-p).

```
System prompt: [Character definition: Mort's persona, voice, constraints, what he won't do]
Few-shot examples: [8-12 prompt-response pairs showing Mort's range]
Current round prompt: [The user's prompt]
Output constraint: [Single response, no meta, stay in voice]
```

Critic AI is a separate call with different system prompt (judge, not performer).

Between-round reactions are short second calls to the same comedian model, conditioned on round outcome.

### Content moderation
- Input moderation on user submissions (OpenAI moderation endpoint)
- Output moderation on AI submissions (check before display)
- No user-generated prompts for MVP (removes a whole class of moderation problems)
- Report button on any round; logs to a review queue

### Storage needs
- Prompts table (fixed, editable)
- Comedian configs (fixed, versionable)
- Sessions table (round-by-round log)
- Shared cards table (for persistent share URLs)
- Report queue

No user accounts at MVP. Session-based, cookie-identified. Users can optionally claim a handle to appear on leaderboards.

## Distribution plan

### Phase 0: Personal playtest (Week 5)
- Play 50+ rounds yourself across both comedians
- Identify prompt problems, character voice drift, boring patterns
- Iterate hard on the system prompts

### Phase 1: Friend playtest (Week 6)
- 10–20 friends play Quick Duel. Watch over their shoulder via Zoom or in person.
- Collect qualitative feedback. "When did you laugh? When did you roll your eyes?"
- Iterate on prompts and character voices

### Phase 2: Soft launch (Week 7)
- Post to r/ArtificialInteligence, r/comedy, HackerNews Show HN
- Tweet thread with best playtest moments
- Tell 50 specific people who might care (comedy Twitter, AI Twitter, tech friends)
- No paid marketing

### Phase 3: Content flywheel (Months 2–3)
- @mortcomedy and @cece_comedy accounts posting best lines from matches
- Weekly "match of the week" highlight
- User-submitted funniest-moments threads
- If any one post or review gets traction, lean in hard

## Timeline

Work splits across the three phases from "Execution phasing." Week-by-week guidance below is in focused-work units; calendar time depends on whether you're working full-time, side-project, or something between. Each phase has a gate; don't cross a gate before it passes.

### Phase 0: Architecture validation (~1 week)

No code. The artifact is a design doc plus hand-traced walkthroughs.

- Draft the three-stage pipeline in detail: what nodes and edges the graph represents, what the selection stage decides, what constraints the LLM receives at realization, how voice is modeled, how subversions attach to templates
- Draft the annotation schema across the eight layers (content, logic, structure, performance, voice, narrative, relational, meta) with controlled vocabularies as separate reference files; expect the schema to iterate throughout the week
- Build a seed corpus of 15–20 reference jokes across Mort's and Cece's target registers; annotate each into the schema
- Use annotation as a pressure test: where the schema doesn't fit, revise it. Free-text notes fields capture what's still missing; repeated patterns across notes signal new fields to add
- Hand-trace 10 new prompts through the pipeline end-to-end, producing intermediate representations and final output text
- Compare hand-traced final output to what you'd write freely given the same prompt and target voice

**Generative sufficiency check.** After annotating the first 5 jokes, perform a blind reconstruction test: read only the annotations (not the original jokes) and ask whether they contain enough information to reconstruct comparable jokes. If not, the schema is missing load-bearing information. Re-run this check after every 10 jokes as a guard against schema drift.

**Gate 1.** Architecture produces output at least as good as free-writing on most of the 10 prompts; the schema passes the blind-reconstruction test; the schema covers the joke types you care about → proceed. Otherwise → iterate on design or abandon.

### Phase 1: Minimal end-to-end implementation (~1–2 weeks focused)

Conditional on Gate 1.

- Build the seed knowledge graph in code (50–100 nodes from Phase 0 annotations) with whatever adjacency/edge semantics the design uses
- Implement the discovery stage: traversal, candidate ranking, return of conceptual ingredients
- Encode 3–5 structural templates from the design
- Encode Mort's voice as a selection filter over templates and concepts
- Implement the realization call: LLM as renderer with tight input contract (concepts + template + voice) and a constrained output format
- Run the 10 Phase 0 prompts through the implementation; compare outputs to hand-trace; debug divergences until implementation is faithful to design
- Stress-test with 30+ unseen prompts; document failure modes

**Gate 2.** Implementation agrees with hand-trace, and stress-test outputs hold quality → proceed. Otherwise → debug pipeline or revisit Phase 0.

### Phase 2: Full MVP build (~4 weeks focused, or side-project equivalent)

Conditional on Gate 2.

**Week 1 — Infrastructure + Cece + critic**
- Next.js + Supabase + Vercel deployment pipeline
- Database schema (prompts, sessions, shares)
- Extend pipeline to Cece: second voice constraint set, Cece-fit templates, graph weighting for her subject preferences
- Critic AI (separate pipeline stage or separate LLM call with its own system contract)
- Character portraits (commission or generate; static is fine)
- Between-round reaction generation

**Week 2 — Prompts + session modes**
- Hand-write 60 prompts across categories
- Implement Practice Session (multi-round, score tracking)
- Implement Gauntlet
- Session persistence

**Week 3 — Polish + playtest**
- Result card generation
- Share URL system
- Input/output moderation
- Personal playtest: 50+ rounds; fix rough edges

**Week 4 — Launch**
- Friend playtest (10–20 users, watch-over-shoulder where possible)
- Distribution prep (screenshots, demo video, launch posts)
- Soft launch to targeted channels
- Monitor, respond, iterate

## v1.1 Party mode (post-launch, weeks 7–10)

Only if MVP shows traction signal. Adds:
- PartyKit (or similar) room infrastructure
- QR code joining
- Host view + player views
- Multiplayer voting
- End-of-match highlight reel

Build this as a separate mode that reuses the comedian characters, prompt library, and critic infrastructure from solo. The foundation work in MVP makes v1.1 faster than it would be standalone.

## v1.2+ Watch mode (future expansion)

A passive consumption mode where users watch the comedians *perform* rather than competing against them. Serves a different user need: ambient entertainment, second-screen viewing, parasocial engagement with the characters, lower-energy interaction for tired users or those multitasking.

### Why this matters

- Complements the duel's participatory nature (duel requires energy; watch doesn't)
- Deepens character relationships (watching Mort and Cece develops a user's parasocial bond in ways that competing against them doesn't)
- Opens the second-screen attention-economy gap (ambient comedy during other activities)
- Produces content that's directly shareable to non-users (clips, not just result cards)
- Gives the characters a performance life beyond the game context

### Format priorities

**Primary format: Duo segments.** Mort and Cece in conversation, riffing off each other on a theme. 2–4 minutes each. The contrast between their voices creates comedy that neither character alone can produce — Mort's dryness grounds Cece's absurdism; Cece's energy lifts Mort's understatement. This is the format most uniquely enabled by the character roster and least imitable by generic LLM output.

**Secondary format: Solo stand-up sets.** Each comedian delivers a short structured set (3–5 min) on a topic. More conventional, more tractable, useful for establishing each character's independent voice before pairing them in duos.

**Tertiary format: Reactive bits.** Characters react in voice to a specific input (a user-submitted scenario, a piece of everyday absurdity, a prompt card). Shorter than stand-up sets, closer to the duel prompts but performed rather than competed against.

**Deferred for later consideration:** Live/always-on streaming (Nothing-Forever-style). High engagement ceiling but brittle failure modes, serious moderation overhead, and operational complexity that isn't worth it until watch mode is established in pre-generated form.

### Technical approach

**Pre-generated, curated, release-scheduled.** Not live generation. This provides:
- Quality control (you can reject bad takes before release)
- Moderation safety (nothing ships without review)
- Reliable content cadence (weekly or twice-weekly drops rather than continuous)
- Lower operational burden

**Text-first, audio-enhanced, static-visual.**
- Text transcripts are the foundation and ship first
- TTS layer (ElevenLabs, Cartesia, or similar) adds audio in a second pass
- Static character portraits during playback; no animation for v1.2
- Animated mouths / simple character motion deferred to v1.3+ if signal warrants

**Generation pipeline for duo segments:**
1. Seed topic or scenario (hand-picked or user-voted)
2. Generate a structured outline — who opens, key beats, callback opportunity
3. Generate the full exchange conditioned on both system prompts and the outline
4. Quality review pass: does each character sound like themselves? Does it build? Does it land?
5. If it passes review, pipeline to audio generation and release
6. If not, regenerate or shelve

A segment that doesn't pass review is discarded, not salvaged. The point is only to release strong output.

### Content cadence and structure

**Weekly release schedule.** A new Mort & Cece duo segment every Tuesday, for example. Cadence creates anticipation and return visits without demanding always-on infrastructure.

**Seasonal arcs (optional).** Across a month of releases, a loose narrative thread can emerge — Mort and Cece developing a recurring bit, an ongoing disagreement, a running joke. This requires more careful curation but dramatically increases parasocial engagement. Comparable to how a podcast develops lore.

**Specials.** Occasional longer-form content for milestones — holiday specials, one-year anniversaries, reaction to a specific cultural moment. Higher production value, lower frequency.

### Shareability

Short clips from each segment (15–45 seconds) designed for social sharing. Users can clip-and-share any moment from a watched segment, generating a standalone shareable video/audio asset. This converts passive consumption into distribution.

### How this fits the roster

Watch mode makes the roster investment pay off much more than solo-duel alone does. In duel mode, each comedian is used in parallel (pick one, play). In watch mode, they're used *together*, and the gestalt of the roster is the product. More comedians = richer watch mode. This creates a strategic reason to invest in character variety over time.

### MVP exclusions for watch mode

When eventually built, the v1.2 version should explicitly NOT include:
- Live or always-on streaming
- User-generated script inputs (moderation overhead)
- Animated characters (scope creep)
- Voice cloning of real comedians (legal/ethical minefield)
- Full episode formats over 10 minutes (user tolerance is lower than you think for AI comedy)

### Timing

Do not build watch mode until:
- MVP duel has validated the characters as worth investing in further
- At least 2,000 users have used the duel, giving you a signal on character preferences
- Party mode (v1.1) has either shipped or been deliberately deferred
- You have capacity for weekly content curation (this is an ongoing commitment, unlike the duel which runs itself)

Realistic earliest timing: 4–6 months after MVP launch, assuming positive signal.

## Success metrics

**Validation threshold (necessary to continue):**
- 500+ distinct users try Quick Duel in the first month
- 150+ complete a Practice Session or Gauntlet
- At least one comedian has a "signature line" that a user shares unprompted
- Organic share count >20 (result cards shared to social)

**Encouraging (worth serious continuation):**
- 2,000+ users in first three months
- 25%+ of users return within a week
- One piece of user-generated content (tweet, screenshot, video) gets 10K+ views
- Direct requests for additional comedians or features

**Breakout (pivot toward commercial / party mode):**
- 10,000+ users
- Organic sharing drives majority of new users
- Requests for hosted / corporate / custom versions
- v1.1 party mode decision becomes obvious

## Monetization (not MVP)

MVP: free, no monetization. Validation is the only goal.

Phase 2 (v1.1+): If traction warrants, explore:
- Free solo mode forever
- Party mode as one-time purchase ($15) or subscription
- Additional comedians as DLC or subscription benefits
- Custom content for corporate / private events

This is hypothetical until the usage data exists.

## Risks specific to solo-first MVP

- **AI quality ceiling is the whole product.** If Mort and Cece aren't meaningfully different and genuinely funny, the product fails. This is where 60% of your effort should go.
- **Solo retention is harder than party retention.** Without social hooks, users can leave after one session and not return. Mitigation: Gauntlet mode, sharable result cards, comedian "best of" feeds.
- **Prompt library runs thin fast.** 60 prompts might feel repetitive within 2–3 sessions per user. Plan for ongoing prompt additions post-launch.
- **The critic's judgment is subjective and will frustrate users.** Override button helps. Transparent reasoning helps. Accept that some users will think the critic is wrong; that's fine.
- **Distribution cold start remains.** Solo-first doesn't solve this; it just moves the problem. You still need people to try the link.

## What this spec does NOT include

- Party mode (explicitly deferred to v1.1)
- Mobile native apps
- User accounts / login (session cookies only for MVP)
- Voice output
- Animated comedians (static portraits only)
- User-generated prompts
- Third comedian (Harlan) — post-MVP
- Leaderboards across users (optional addition if time permits)
- Tournament / seasonal content

## What to do first

Phase 0 starts with the design doc, not code. In order:

1. Sketch the three-stage pipeline in detail — what the graph represents, what the selection stage decides, what constraints the LLM receives at realization, how voice is modeled as a filter over templates and concepts
2. Collect 15–20 reference jokes (Mort-adjacent: Mitch Hedberg, Norm Macdonald, early Seinfeld openings; Cece-adjacent: Maria Bamford, Demetri Martin, John Mulaney absurdist bits) and annotate each one by decomposing it into the pipeline's intermediate representations — concepts, pivot, structural template, voice moves, subversions applied
3. Use the annotation process itself to pressure-test the schema — if jokes keep not fitting, the schema is wrong and needs revision before proceeding
4. Hand-trace 10 new prompts through the pipeline on paper, playing all three stages
5. Compare hand-traced outputs against what you'd write freely given the same prompts and voice targets. Be honest.

Everything else is blocked on Gate 1. If the architecture doesn't produce good output when you run it yourself on paper, no amount of code will save it. Better to discover that in week 1 of design than week 6 of implementation.

## Working artifacts

The spec describes architecture and phasing. Operational procedures, schema details, and the annotation assistant's system prompt are maintained as separate living files alongside this spec so they can evolve without making the spec stale.

```
comedy-duel/
  spec.md                          # this document
  protocols.md                     # annotation protocol, session checklists, review cadence
  engine/
    schema.yaml                    # the nine-layer annotation schema (living)
    system-prompt.md               # annotation assistant's system prompt (living)
    vocabularies/                  # controlled vocab files per field
      README.md                    # definition format and maintenance rules
      incongruity-types.yaml       # starter: 5 values
      templates.yaml               # starter: 5 values
      positioning.yaml             # starter: 4 values
      subversions.yaml             # starter: 5 values
      affect-axes.yaml             # starter: scale anchor points
      domains.yaml                 # populated from annotation
      cadence.yaml                 # populated from annotation
      registers.yaml               # populated from annotation
      persona-markers.yaml         # populated from annotation
      ...
    concepts/                      # concept nodes (knowledge graph)
      _registry.yaml               # canonical list of all concept node_ids
      {node_id}.yaml               # one file per concept, with dimensions
                                   #   and attested-in data
    routines/                      # routine-level metadata for multi-joke bits
      {routine_id}.yaml            # shared source, running_premise,
                                   #   ordered list of member joke_ids
    performers/                    # voice-level defaults per roster member
      mort.yaml
      cece.yaml
  annotations/                     # one YAML per annotated joke
  working/
    questions.md                   # unresolved questions accumulated during annotation
    decision-log.md                # non-obvious judgment calls, for delayed self-review
    schema-changelog.md            # what changed in the schema, when, and why
    field-usage.md                 # running count of fields used vs defined, checked on cadence
```

The spec changes only when architecture or phasing changes. The schema, system prompt, and protocols change as the work teaches you what they should be. The `working/` files exist because keeping procedural vigilance in your head is unsustainable — surface it in files, review on cadence, don't try to remember everything.

---

*Phase 0 in ~1 week; Phase 1 in ~1–2 focused weeks if architecture validates; Phase 2 in ~4 weeks of focused or side-project time if implementation validates. v1.1 party mode follows if MVP gets signal.*
