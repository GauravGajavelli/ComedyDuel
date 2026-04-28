# Game Mechanics — Brainstorm and Concrete Designs

Working document on game-loop design beyond the original "write a joke,
read AI's joke, get judged" loop in `spec.md`. The core concern this
document addresses: passive standup-watching is what people skip in
Seinfeld; the game needs to make comedy interactive in a way that
genuinely produces laughs, not just intellectual appreciation.

This is design exploration, not a commitment. The recommended next step
is at the bottom.

## What other games solve adjacent problems

**Selection-driven comedy (the most underused mechanic):**
- **The Stanley Parable** — the narrator IS the comedian; the player is
  a heckler with a finite door menu. Comedy comes from the narrator's
  *reactions* to disobedience, not from player wit. The single most
  relevant reference for this project.
- **Cards Against Humanity (digital)** — proves people laugh hard at
  *selection*, not creation. Pre-written punchlines, player picks
  juxtapositions.
- **Inscryption** — Leshy is a presenter/showman; the player engages
  mechanics, the character provides comedy. Performer-as-frame.

**Procedural-input + pre-written-voice (the workhorse pattern):**
- **Helldivers 2 / Deep Rock Galactic** — characters have pre-recorded
  voice lines that fire over emergent chaos. The mismatch is funny.
- **Hades** — characters comment on your *recent runs*. Comedy is in
  relational memory, all pre-written.
- **Disco Elysium** — your own skills argue with each other in distinct
  voices. This is the Mort/Cece dynamic, internalized.

**Performance-as-mechanic (the rhythm question):**
- **Hi-Fi Rush** — combat synced to music + irreverent writing. Works
  because *you* feel cool. The character's wit is incidental.
- **Rhythm Heaven / WarioWare** — comedy is in the *constructed
  absurdity of the situation*, not the player's input. Player just times
  button presses.
- **Parappa the Rapper** — recitation/timing of pre-written jokes.
  People laughed in 1996 and don't replay.

**Live-generated TV (the cautionary tales):**
- **Showrunner AI, AI Dungeon, Bandersnatch** — Bandersnatch worked
  because Netflix wrote 5 hours of branches. Showrunner AI was novel for
  20 minutes. Unbounded live generation produces *coherent* output, not
  *funny* output. This is the trap to avoid.

**Comedy under interrupt (Jackbox):**
- **Quiplash / Joke Boat** — writing under time pressure, peer voting.
  Most submissions are mediocre; the room produces a few golds. Works
  because of the *room*, not the writing.

## Hard pushback on the original brainstorm ideas

**Recitation: kill it.** Karaoke works because *singing together is
intrinsically pleasurable* and the songs are universally known. Joke
recitation has neither property. A joke read badly is just unfunny. The
monopolization-by-naturally-funny-person problem alone is fatal.

**Co-op with friends as audience: kill the multi-player version.** The
concern in the brainstorm is correct and structural. Real comedy clubs
work because *the audience paid to be entertained and is socially
primed*. Friends in a living room are competing with you for laughs —
they will not laugh easy, full stop. No clever design rescues this. The
single-player version (you + an AI partner) is interesting and
survives.

**Pure rhythm game: won't work standalone.** The chain "player presses
buttons in time → AI tells joke about airports → joke is funnier" is
too abstract. The player isn't doing the comedic thing; they're being a
metronome whose reward is "Mort's joke landed." Rhythm games work when
*you're* doing the cool thing (Hi-Fi Rush). It only works folded into a
design where the player has content agency too.

**God-mode episode interaction: ambitious but viable if heavily
constrained.** The honest risk is that live-generating
*episode-quality writing* off player input is at the bleeding edge of
what LLMs do well. Showrunner AI tried it; results are watchable for
one viewing. The way this works is to **shrink the live-generation
surface** — pre-write 90% of the scene, let the engine generate only
one character's response to a player-injected perturbation. Then it
becomes Bandersnatch with a smarter branch generator.

**Crowdwork stage: strongest of the original five.** Real performance
challenge, maps cleanly to the engine, naturally adversarial. Develop
this.

## The deeper structural problem in the original spec

Even before standup-watching: the original loop is **a writing
competition judged by an AI**. Writing is slow, lonely, and feels like
work. Jackbox's writing tolerates itself because of time pressure +
peer vote + the room. Solo-vs-AI removes the vote and the room. What's
left is a creative-writing exercise with a robot judge.

The pattern that actually makes comedy games funny across the
references above: **player as selector/director/foil, engine as
performer**. The engine is good at generating; that's its training. The
player is good at choosing, timing, and reacting. Match the labor to
the strength.

This reframes the question. Not "how do we make watching standup
interactive" but "how do we make the player a *participant in* the
engine's performance, not a competitor to it?"

## Three concrete designs

### Design 1 — The Director's Console *(strongest; prototype this first)*

**Loop.** Mort or Cece is on stage. The audience misbehaves: a phone
buzzes, a drunk shouts something, someone says "my grandma told that
one." Each interruption arrives as a text bubble. The player has 4–6
seconds to pick **one of the 6 cognitive operations** from the schema
(negation / reinterpretation / transplant / mapping / extension /
articulation) plus optionally a modifier (reading_switch, scale_shift).
The engine generates the comedian's response in voice, conditioned on
that operation. Critic AI scores the response; player gets a separate
"directing grade" on whether the operation choice was the right call.

**Why it works.** Player labor shifts from creation to selection —
fast, low writing burden, suited to live pacing. The schema's
vocabulary becomes the game vocabulary; players literally *learn comedy
theory* through play. Bad operation choices are obviously funny ("you
tried to map a phone heckle to airport bureaucracy — Mort's confused;
the bit died"). Good ones feel like wins because they're real comedy
moves. High skill ceiling without high writing ceiling.

**Engine demands (concrete).** Operation must become a *generation
input*, not just an annotation field — currently the schema records
what jokes did; the pipeline would need to take "do a transplant" as a
constraint at the selection stage. Discovery has to take
heckler-text-as-context (currently it's prompt-only). Latency target
≤3s end-to-end. Honest test: blind-generate from
`voice + heckler + operation` for all 6 × Mort/Cece × 30 hecklers and
see whether the operation actually produces distinguishable outputs.

**Risk.** If operation-conditioned generation produces outputs that
aren't audibly different by operation type, the gameplay collapses
(every choice feels the same). This is *exactly the kind of thing
Phase 0's hand-trace should pressure-test before any code*.

### Design 2 — Episode Loops (god-mode, constrained)

**Loop.** A 90-second pre-written scene plays — Mort and Cece riffing
in a writers' room, or a faux-sitcom snippet. Audience laughs at
scripted beats; this is the baseline. Then the player gets *three
perturbation cards* and a rewind: "Mort delivers this line, but
anthropomorphize the coffee." "Cece responds with a register break."
The engine regenerates only the affected lines. Surrounding scene
unchanged. Player tries to beat baseline. Critic compares. Replays
produce different cuts of the same scene.

**Why it works.** Pre-written scaffolding caps quality risk — 90% of
the scene is reliable. Engine generates 1–2 lines per attempt, a small,
tractable surface. The TV-shaped format pulls in users who'd never
write a joke. Replay is structural: same scene, infinite cuts. Connects
directly to v1.2 watch mode in the spec.

**Engine demands.** Single-line generation under joint constraint
(voice + scene context + perturbation card). Voice attribution must be
airtight — a Mort line dropped into a pre-written Cece exchange must
read as Mort. Continuity: the surrounding pre-written lines have to
still make sense after one line shifts. This is the *hardest* of the
three on the engine. The operation_alternative branching (v0.9.2) is
exactly the kind of variety mechanism that helps here.

**Risk.** Authoring perturbation cards that consistently produce
funnier-than-baseline output requires real comedy-writing discipline at
design time. If the cards are too open ("make this funnier"), the
output is LLM smoothing. If they're too narrow, the result is one-trick
replays. The card design *is* the game design.

### Design 3 — The Stage *(rhythm folded into selection + delivery)*

**Loop.** Prompt arrives. Engine generates 3 candidate jokes (different
operations/templates). Player picks one — content choice. Performance
phase: timing minigame on a rhythm track showing pauses, register
shifts, callback-trigger windows from the joke's `performance` layer.
Audience laugh-meter is `joke_quality × performance_accuracy`. A bombed
delivery cools the audience for the next round; a great one warms
them. Set is 5 jokes; final score is laugh integral.

**Why it works.** Player has agency on two axes — content and
delivery. The performance layer of the schema (cadence,
pause_placement, vocal_register_shifts) becomes UI. Hi-Fi Rush proves
the kinaesthetic satisfaction of nailing timing is real. The cold/warm
audience adds session arc and reading-the-room as a meta-mechanic.

**Engine demands.** Engine must output *multiple diverse candidates*
per prompt (current pipeline is single-output). Engine must emit
cadence annotations as part of generation, not as post-hoc analysis.
Audience-laugh function can be a simple heuristic, not a model —
quality_score × timing_accuracy, decay term for repeated misses.

**Risk.** The bridge from "good timing" to "I laughed harder" is
cognitive, not kinaesthetic. The result may be a music game wearing
comedy clothes — players have fun *playing*, but don't experience the
comedy as funnier when timed well. Mitigation: heavy audio feedback
(canned laugh quality scales with timing) sells the connection even if
it's partly illusion.

## Solo recommended next step

Prototype **Design 1 (Director's Console)** first.

1. It uses the engine surface already built most directly — operations
   become verbs.
2. Smallest engine extension needed (operation as input ≈ a few weeks;
   episode-line-replacement ≈ months).
3. The genuine differentiator: it teaches comedy theory as gameplay,
   which no other product does.
4. It survives Phase 0's hand-trace test — sit down with paper today
   and generate "what would Mort do with negation on this heckler" for
   20 inputs and see if the outputs feel distinct.
5. Failure mode is informative: if operation-conditioned generation
   produces undifferentiated outputs, that's a Gate-1 finding about the
   engine, not just about the game.

Design 2 is the right *second* prototype if Design 1 works — it
leverages the same operation-as-input infrastructure and starts
converting the roster investment into TV-shaped content (the v1.2
thesis).

Design 3 to hold. Not because it's bad, but because the
rhythm-to-comedy bridge is the kind of thing only verifiable by
building, and Designs 1 and 2 give more learning per week of build.

The thread tying all three together: **stop asking the player to be
funny. Make them the director, the foil, or the editor of a performer
who is.** The engine wants to perform. Let it.

---

# Solo improvements from party-mode work

The party-mode design surfaced several mechanisms that materially
improve solo Design 1 (Director's Console). The solo design as
originally drafted was op-pick-only with the critic giving a single
verdict; party mode forced through questions about contribution
gradient, session arc, and shareable artifacts that solo benefits
from too.

This section is the back-port: the party mechanisms that transfer
to solo, and the ones that don't.

## What ports

### 1. Hybrid input (op pick + optional freeform)

Solo Design 1 as originally drafted is op-pick-only: player picks
negation/transplant/etc. and the engine generates everything from
op + voice. Add the **optional freeform input** from party mode.
Player picks op, then optionally types a word, phrase, or sentence
to anchor the joke. Engine interprets:

- *Empty* → engine generates from op + voice (current Design 1 behavior)
- *Word* → becomes the `pivot_concept`
- *Phrase* → fills the operation's slot
- *Sentence* → respected verbatim, engine adds performance scaffolding

This keeps the "selection > creation" principle intact (the op pick
remains the universal labor) but adds an expressive axis for
players who want to push further. A solo player who's getting
comfortable starts adding inputs; a beginner ignores the box. The
contribution gradient is now solo-relevant.

The pedagogical value is also bigger: the player can *test* whether
their input was load-bearing by running the same prompt + op with
and without the input and seeing what changes. That's
comedy-theory laboratory work.

### 2. Two-axis critic feedback

Currently the critic gives one verdict ("this landed" or "this
didn't"). Split it:

- **Joke quality** — did the output actually work as comedy?
- **Directorial taste** — was your op pick the right call for this
  prompt/heckler, regardless of how the output turned out?

This is a much stronger pedagogical loop. The player learns:
"my op pick was right but the engine's output was weak (try again
with the same op)" vs "my op pick was wrong but the engine
produced something funny anyway (got lucky; don't internalize the
choice as correct)" vs "both right" vs "both wrong." Currently the
player can't separate these signals, so they over-credit good luck
or under-credit good taste.

This is also where the engine's `operation_alternative` field
(v0.9.2) earns its keep: when the critic notes "you picked
transplant, but mapping was the cleaner call," the player gets
explicit comedy-theory feedback grounded in the schema's own
boundary cases. The two-axis split is the party mode's two-axis
voting (best joke + best craft) collapsed onto a single judge.

### 3. Topic anchor for Gauntlet

The Gauntlet is currently 10 prompts in a row, escalating
difficulty, but the prompts are unrelated. Apply the party-mode
topic-anchor:

- Lobby (or first-round) selection: "Tonight's set: airports."
  Engine offers 3 curated topics from concepts with annotated jokes.
- All 10 prompts drawn from that domain.
- Invisible arc: openers, builders, closer (engine handles).
- Callback opportunities surface around round 6 and 9 ("reference
  an earlier bit").
- Engine's narrative layer (callbacks_to, running_premise,
  position_in_set) finally has somewhere to compute.

This converts the Gauntlet from a difficulty ladder into a *real
comedy set*. The engine's strongest features come online. The
session has arc and identity, not just a score.

Practice Session is shorter (3/5/7 rounds per the spec) so the
topic anchor is optional — the player picks "free" or "themed."
Quick Duel stays single-round and doesn't need a topic anchor.

### 4. Cold/warm audience meter for session arc

Currently solo has no inter-round dynamic — bombs don't carry
consequences across rounds. Add the cold/warm meter:

- A bombed round visibly cools the audience. Next round, prompts
  feel harder; the engine performs Mort with more reluctance,
  longer pauses, more skeptical reactions.
- A hit warms the room. Subsequent rounds get easier; Mort gets
  generous; the audience laughs at borderline jokes.
- Closer rounds in Gauntlet become high-stakes — arrive cold and
  the closer needs to be a save; arrive warm and Mort can risk a
  weird structural choice.

This gives solo a *session feel* instead of a string of disconnected
rounds. It also makes the bomb-as-content mechanism (in-character
reactions, recovery rounds) carry weight beyond the single round
where it happened.

### 5. Replay as performed set after Gauntlet

The spec mentions Gauntlet ends with "you beat Mort in the Gauntlet
or similar achievement." That's a score. Replace it with a
*performed artifact*:

- Player's 10 directorial choices (op picks + inputs) get stitched
  into a continuous Mort or Cece set, performed end-to-end with
  transitions, full visual cue treatment, and chapter framing if
  needed.
- Three-tier output, same as party:
  - **Your full cut** (5–7 min) — local souvenir, watch back later.
  - **Highlight reel** (45–90 sec auto-edited) — top 3 moments +
    best bomb. The shareable.
  - **Personal highlight** (15–30 sec) — single best moment. The
    one-tap share.

This makes the Gauntlet produce *content*, not just a verdict. The
session-level shares already in the spec ("I played 5 rounds against
Mort and won 3 of them") become full performed routines instead of
text screenshots.

Practice Session optionally produces a shorter cut. Quick Duel
produces only the result card (current spec behavior).

### 6. Fail-forward delivery and in-character bomb reactions

Already implied by good engine design but worth being explicit. The
engine should never produce a *boring* bomb in solo. Mort's deadpan
acknowledgment of a flop is itself entertainment. The cold/warm
meter gives bombs structural consequence; the in-character reaction
gives them comedic content. Solo benefits from this just as much
as party.

The schema's between-round reactions (in spec) already cover this;
the requirement is just that bomb-reactions are *as comedic* as
win-reactions, not afterthoughts.

### 7. Recovery rounds (optional)

Bombed submission triggers an optional 5-second second pass with a
different op. Half the time the save lands and earns bonus credit;
half the time it bombs harder. Solo benefits because it adds a
chosen risk-taking moment after failure — the player can accept the
bomb and move on, or commit to a save attempt that may dig the hole
deeper. Either choice produces content.

### 8. Engine-curated op pre-filter (as beginner mode setting)

Party mode pre-filters to 3 ops to keep selection legible at speed.
Solo's differentiator is teaching all 6 ops, but a beginner-mode
setting can pre-filter the same way for first-time players. Settings
options:

- **Show suggested 3** (default for new players) — engine surfaces
  the 3 ops most likely to land for this prompt
- **Show all 6** (default for experienced players) — full choice
- **Speedrun** (advanced) — engine picks one op; player commits or
  rejects without alternatives

Lets the solo player ramp into the full vocabulary without being
overwhelmed in the first session.

## What doesn't port

A few party mechanisms don't transfer to solo:

- **Plain-language op verbs.** Solo's differentiator is teaching
  comedy theory, so showing the technical schema names (with
  tooltip definitions) IS the feature. Plain verbs would dilute
  the pedagogical value.
- **Tag round.** Splits one player's contribution into two
  (setup + tag), loses solo's speed advantage. Skip.
- **Bomb-by-design round.** Works in party because the room laughs
  together at deliberate bombs. Solo with no audience makes
  deliberate-bombing feel like writing a bad joke for a robot.
  Probably skip.
- **Pre-vote elimination.** No votes in solo. The critic AI can
  serve a similar role by flagging weak rounds for omission from
  the highlight reel auto-edit.
- **Turn-based visual editing.** Only one player. Either they edit
  everything (give them a post-Gauntlet editor mode) or the engine
  handles it via performer profile defaults. The constraint that
  drove turn-based editing in party (many players, finite bits)
  doesn't exist.
- **Special crowd-work round as distinct format.** Solo Design 1
  *is* crowd-work in structure (heckler injection + op response),
  so making it a "special round" within solo would be redundant.

## Updated solo Design 1 summary

Solo Design 1, after the party-mode back-port:

**Per round:**
- Heckler/prompt arrives
- Player picks op (full 6 by default, or 3 in beginner mode)
- Player optionally types freeform input (word/phrase/sentence)
- Engine generates response in voice, conditioned on op + input
- Engine performs response with full live visual treatment
- Critic gives two-axis verdict: joke quality + directorial taste
- Optional recovery round on bombs
- Cold/warm meter updates

**Per session (Gauntlet):**
- Optional topic anchor at start
- Invisible arc shapes prompt difficulty/closer-stakes
- Callback opportunities surface around rounds 6 and 9
- Cold/warm carries across rounds
- End: full cut performed end-to-end + highlight reel + personal
  highlight

**Engine demands beyond original Design 1:**
- TTS + cadence/pause/register pipeline must accept arbitrary
  player input text (same demand as party)
- Critic must produce two-axis output (joke quality + directorial
  taste), grounded in the operation_alternative field for the
  taste dimension
- Engine must compute cold/warm state and condition performance on
  it (longer pauses when cold, looser delivery when warm)
- Engine must emit transition lines for the Gauntlet replay
  (conditioned on prior_joke + next_joke + voice)
- Engine must distinguish live-rendered visuals (constrained
  subset) from replay-rendered (full vocabulary), same as party

These are the same engine extensions party mode requires, with the
exception of multi-candidate generation calibrated-to-the-room
(which is party-specific). Building solo with these extensions
*reduces* the marginal cost of building party later.

## Sequencing implication

The original recommendation was: prototype Design 1 first as the
solo MVP. That stands. But the back-ported Design 1 above is
substantially richer than the original — and the engine extensions
it requires (arbitrary-text TTS, two-axis critic, cold/warm state,
transitions, two-tier visuals) are the same extensions party mode
requires. Building solo at this level of richness is the right
investment because party mode will reuse all of it.

The phasing becomes:
- Phase 0 (architecture validation, per spec) — unchanged.
- Phase 1 (minimal end-to-end) — implement original op-only Design 1
  to prove operation-conditioned generation works. Do not build
  the back-ported features yet.
- Phase 2 (full MVP) — build the back-ported Design 1 with the
  engine extensions above. This *is* the solo MVP.
- v1.1 (party mode) — most engine work is already done; party mode
  becomes UI + multiplayer infrastructure + the party-specific
  mechanics (Option B performance, two-axis voting, topic-curation,
  multi-candidate calibration).

This sequencing makes party mode genuinely cheaper to add later
than building it from scratch would be, because solo has done the
shared engine work.

---

# Party mode (revised)

The original spec defers party mode to v1.1 as a resource decision
(multiplayer infrastructure cost), not a design weakness. After working
through the solo brainstorm, the honest reassessment is that **party
mode is structurally a stronger game than solo** because the room
restores the two pieces missing from solo: the peer vote (replacing the
AI critic) and the social context (replacing the lonely blank page).
Party mode is therefore the natural shape of the product; solo is the
warm-up.

Party mode in this section is NOT solo Design 1 scaled up. It's a
distinct mechanic that shares the engine. The two should ship as
sibling products of the same generation pipeline.

## Why party mode is structurally strong

The original spec's deferral was infrastructure cost, not design
weakness. Re-examined against the solo brainstorm's critiques:

- *"Writing competition judged by AI"* → becomes "writing competition
  judged by *the room*." Peer vote replaces the AI critic, which was
  the single biggest weakness of the solo loop.
- *"Watching standup is what people skip"* → doesn't apply. There's no
  standup to watch; submissions display side-by-side, including Mort's.
- *"Writing is lonely"* → not in a room. Jackbox proved this works.
  Time pressure + voting + laughter is well-trodden.
- The naturally-funny-person monopolization problem (which kills solo
  recitation) is muted because anonymity-until-reveal flattens the
  social hierarchy each round.

What the AI comedians earn in party that they don't in solo: in solo,
Mort and Cece are the opponent — one at a time, central. In party,
they're *ringers in the lineup*. Eight submissions show up, one is
Mort's, the room votes blind, then the reveal: "submission 4 was Mort,
and three of you got beat by him." The "guess the AI" meta-game is
the spec's strongest under-developed asset.

## The performance asymmetry problem and the Option B fix

The asymmetry: the engine has full performance metadata (cadence,
pause placement, register shifts, visual cues); players write text.
If everyone reads submissions as plain text, the engine's performance
advantages are wasted. If the engine performs only AI submissions,
Mort wins every round on delivery alone.

**Resolution: the engine performs everyone's text.** All submissions
— human and AI — are read aloud by Mort's or Cece's TTS, with the
engine applying cadence, pauses, register shifts, and visual cues to
whatever text was submitted. The round announces "tonight Cece is
performing your bits." Players write *targeting* her voice. Vote
happens after the staged performance.

This works because:

- Levels the delivery field — every submission gets the same
  performance treatment.
- Turns "write in Cece's voice" into the constraint, which is
  comedy-positive (constraints sharpen output).
- The performance layer applies to *all* submissions, not just AI's.
- The host TV becomes a real performance stage; phones become the
  writers' room.
- Failure mode is funny: a flat human submission delivered as Cece's
  enthusiastic absurdism *exposes itself* — that's part of the bit.
- Mort and Cece become hosts/performers, not just opponents — which
  is how comedy clubs actually work.

Engine demand: the TTS + cadence/pause/register pipeline must take
*arbitrary input text* (player submissions), not just engine-generated
text. This is a real extension distinct from anything Design 1 needs.

## Contribution gradient — the "selection vs creation" reconciliation

The solo brainstorm argued "selection > creation." That principle was
context-dependent: writing wins when the room is present (Jackbox's
empirical proof) and loses when it isn't (solo). Party restores the
room, so writing becomes viable again.

But the principle still cuts. Two clean party variants exist:

- **Option B (writing + engine performance):** comedy comes from
  *humans being weird in different ways*, filtered through Mort's or
  Cece's performance. Engine is a force multiplier. Best for groups
  confident in their writing. Risks exposing weak writers — the
  Jackbox flaw.
- **Design-1-as-party (selection-only directing):** comedy comes from
  *the engine's wit*, filtered through player direction choices.
  Engine is centerpiece; player is shaper. Inclusive of weak writers,
  faster rounds, lower social risk.

The strongest synthesis is a **hybrid with operation-constrained
freeform input**, which is the recommended party design.

### How the hybrid works

1. **Op pick is mandatory and prior to typing.** Player picks an
   operation first (rendered as plain-language verb in party UI: see
   selection legibility section). The op is the universal labor —
   same decision, same time, same stakes for every player regardless
   of writing skill.
2. **Single freeform input box afterward.** Player types whatever
   they want — a word, a phrase, a full punchline, or nothing. No
   mode switch. The engine adapts to what was given.
3. **Engine interprets the input by depth:**
   - *Empty* → engine generates everything from op + voice. Shy-player
     escape hatch. Authorship still credited via the op pick.
   - *One word* → that word becomes the `pivot_concept` (load-bearing
     by the schema's own definition). The joke literally pivots on
     what the player wrote.
   - *Phrase* → fills the slot the chosen op needs (source-domain
     detail in transplant, literalization target in reading_switch,
     etc.).
   - *Full sentence* → engine treats it as the punchline. Performs it.
     Adds only performance scaffolding. Text preserved verbatim.
4. **All submissions performed in voice** (the Option B move).
5. **Visible attribution.** After performance, before voting, the
   screen shows each submission with the input highlighted in the
   joke and the op chosen. "Sarah picked TRANSPLANT, wrote 'tax
   forms.' Cece performed: '...the espresso machine started filing
   its *tax forms* with the customers...'"

### Why this satisfies effort universality

Every player does three things, regardless of writing skill:

1. Picks an op — same decision, same time, same stakes.
2. Commits something — empty box is socially worse than typing one
   word, so they type. Time pressure forces commitment.
3. Sees their contribution in the output — bolded, attributed,
   performed.

Every player gets three things:

1. Performance reward — Cece reads their thing in voice, in front of
   the room.
2. Two shots at winning (see two-axis voting below).
3. Social proof of contribution — the room sees what they submitted
   before voting.

The contribution gradient is invisible to the room. The labor is in
the *taste* of the pick, not the volume of the type. Minimum-effort
contributions are still load-bearing (they become the pivot).
Maximum-effort contributions get full credit (text preserved
verbatim). Nobody is purely carried; nobody is purely robbed.

## Two-axis voting

A single "best joke" vote rewards writing skill and punishes weak
writers regardless of taste. The fix:

- **Best joke** — room reacts to what landed when performed.
- **Best craft** — room rewards the cleverest pick + input combo
  regardless of whether it landed.

The funny-instinct player wins one category; the writer-craft player
wins the other; the player who nails both sweeps. A player who wrote
a great line that the room didn't laugh at still gets validation in
"best craft." A player who wrote one perfect word that turned into a
killer joke gets validation in "best joke."

This is the critical safety net for taste-strong-but-writing-weak
players. Without two-axis voting, writers monopolize. With it, op +
input *taste* is recognized independent of execution.

## Selection legibility (party UI)

The schema's vocabulary (negation/reinterpretation/transplant/
mapping/extension/articulation) is technical. A drunk friend reading
"transplant" with a 4-second timer will not commit. The schema names
are fine for solo (lower pace, tooltips, motivated player) but party
needs reskinning.

**Plain-language verbs in party UI.** Map the 6 operations to
one-word imperatives — *Flip / Reframe / Misapply / Mirror / Push /
Name-it* (or similar). Schema names live behind the scenes; the
party UI never shows them. Comedy-theory teaching remains solo's job.

**Op pre-filtering.** The engine surfaces 3 ops most likely to land
for *this specific* heckle/prompt, not all 6. Player picks from
those 3. Reduces decision space without removing agency, and the
engine's pre-filter is itself a real feature — it's making a
judgment call about what the moment wants. "More" reveals the full
6 if the player wants; the default is curated.

**Tutorial round.** First round of the night is non-scoring; the
timer is generous (15s); each op shown with a one-line worked
example. Then real timer kicks in.

**Icons + verb, not paragraphs.** No prose explanations live.
1-second hover reveals one-sentence tooltip; otherwise the icon and
verb carry it.

The honest assessment: 3 ops with plain verbs + 4-second timer is
playable. 6 ops with technical names is not. The pre-filter is
doing real design work, not just usability work.

## Continuity scaffolding — topic anchor and arc

The schema's strongest features (callbacks, running_premise,
position_in_set, narrative layer) all assume *accumulation*. The
engine produces one-off jokes well, but Mort's actual comedic
identity emerges across a routine. Party-mode-as-rapid-prompt-cycle
would render the engine in its weakest mode.

Light scaffolding focuses without constraining:

- **Topic anchor for the night.** Lobby setting: "tonight's set is
  about: airports / dating / domestic chaos." All prompts and
  hecklers drawn from that domain. Activates the engine's
  concept-graph adjacencies.
- **Engine-curated topic suggestion, room override.** Engine offers
  3 topics drawn from concepts that already have annotated jokes
  (i.e., topics it knows it can be funny on). Room picks. Grounds
  selection in actual capability, avoids cold-start friction.
- **Invisible set arc.** Engine knows: round 1 openers (low-stakes,
  looser), middle rounds build, final round closer (high-stakes).
  Engine adjusts selection toward the arc — saves stronger
  pivot_concepts for closers. Players don't see this; it just
  happens.
- **Per-round prompts within the topic.** Drawn from the existing
  prompt library (60 prompts at launch in the spec) filtered by
  topic tag.

### On-topic priming and rewarding (without punishing)

**Don't penalize off-topic.** Penalty creates fear, fear kills
creative risk-taking, and the best comedy is the surprising swerve.
Hard topic rules would kill the great absurdist tangent.

**Do prime on-topic, three layers:**

- *Visible during input.* Topic stays in UI prominently during the
  submission window. Above the input box, in color: "Tonight's set:
  AIRPORTS." Reminded constantly, not constrained.
- *Engine-suggested concept anchors.* Within the topic, the engine
  surfaces 2-3 concepts the player could use: "Try: TSA / boarding
  / lost luggage." Drawn from the topic's adjacency cluster.
  Scaffolding for the blank-page player; ignorable.
- *Soft nudge on apparent drift.* If input has clearly drifted (graph
  distance from topic exceeds threshold), small notice: "topic:
  airports — sure?" One-click confirm. Doesn't block; respects
  deliberate drift.

**Do reward on-topic, three layers:**

- *Tiebreaker priority.* When two submissions tie on votes, the
  on-topic one gets the canonical Room's Cut slot. Off-topic only
  wins by *outright winning the vote* — has to be better, not just
  tied.
- *End-of-night superlatives.* "Most On-Topic: Marcus — five for
  five on airports." Lightweight social recognition.
- *Theme-commitment metadata in Personal Cut.* Self-acknowledgment
  reward.

**Do reward off-topic when it lands.** The room's vote is supreme. A
great off-topic submission that the room loves wins outright, gets
the canonical slot, no penalty. Topic preference resolves *ties*
only.

**Engine move on detected off-topic drift:** the engine can register
the drift in voice. Mort delivers an off-topic submission with a
deadpan acknowledgment ("I'm not sure how this connects to airports,
but here we are"). Cece's version: "Wait — were we doing airports?
Was airports a thing?" The off-topic-ness becomes the bit;
meta-acknowledgment is comedy. This converts off-topic from problem
into comedic frame and signals to the room that the system is in
on it.

**Off-topic isn't a bomb; it's a different bit.** The bomb is
"submission didn't land at all." Off-topic submissions either land
(and win) or don't (and bomb like any other). Topic is a frame;
landing is the standard.

## Special round types

Five distinct round types provide variety in a 6-round session
without overwhelming. Topic anchor stays constant across the night;
round types vary.

- **Standard round.** Op pick + freeform input + performance + vote.
  The default. Most rounds are this.
- **Tag round.** Pair players. Player A submits a setup; player B
  writes a tag (the follow-up line — extends, reframes, or undercuts
  the punchline). Two contributions per round, both credited.
  Leverages the schema's `tag_operation` and `has_tag` fields
  directly. Real comedy structure — tags extract second laughs from
  the same setup.
- **Crowd-work round.** Pre-written heckler injects mid-round; player
  must respond to *the heckler*, not the original prompt. Tighter
  timer (3s). Ports the original Idea 4 — crowd-work as real
  performance challenge under engine constraint. Place mid-set,
  higher difficulty.
- **Callback round.** One player per session is offered the callback
  opportunity: their submission must reference a prior winning bit
  from tonight. Engine populates the narrative layer
  (`callbacks_to`) explicitly. Creative-positive — a tool, not a
  constraint. Place before the closer.
- **Bomb-by-design round.** Inverted scoring: vote for the worst
  joke. Releases competitive pressure, exposes the absurd lengths
  people go to be deliberately unfunny, almost always the
  loudest-laugh round of any party game. Place once per session,
  mid-late, as a release valve.

The closer (final round) is just the standard format with stakes
scaled and stronger prompts — handled invisibly by the arc, not as
a distinct round type the players see.

## Bombing as positive content

Don't add decoy or intentionally-bad ops. Comedy is taste, not
gotcha mechanics. But bad *fits* produce bad output naturally —
picking "Push" (extension) on a heckle that doesn't extend produces
output that visibly doesn't land. **The engine should not refuse
off-fit op picks; it should generate transparently bad output.** The
bomb is legible, attributable, and content.

Three mechanisms turn bombs into entertainment:

- **In-character reactions.** Mort to a bomb: "Yeah, that one went
  somewhere and didn't come back." Cece: "I'm going to think about
  this on the drive home and that's not your problem." The schema's
  between-round reactions are exactly this. Bombs become
  reaction-fuel for the comedians, who are themselves the comedy.
- **Audience cold/warm meter.** A bomb visibly cools the room. Next
  player has a harder mountain. Thawing a cold room is visibly
  satisfying when it lands. Bombs gain stakes — they're not neutral;
  they're affecting the room.
- **Recovery rounds (optional).** Bombed submission triggers an
  optional 5-second second pass with a different op. Half the time
  the save lands and earns bonus credit ("recovered from disaster");
  half the time it bombs harder. Both outcomes are entertainment.

**Fail-forward delivery requirement.** When a submission is weak and
bombs, Mort's *delivery of the bomb* must still be entertaining (the
deadpan registration that it didn't work, the in-character recovery
line). The engine should never produce a *boring* bomb. A flatly-
failed joke without entertaining acknowledgment is the only truly
bad outcome.

## Party-size cap and flow management

Real math: 8 players × 5 rounds × 12-second performance = 8 minutes
of pure listening per session, before voting and transitions.
Multiple consecutive bombs would kill momentum.

**Mechanisms to manage flow at scale:**

- **Pre-vote elimination.** All submissions display as text first.
  Room picks top 3 to actually *perform*. Bottom submissions get a
  one-line auto-roast from Mort and move on. Cuts performance time
  ~60%; preserves the *interesting* bombs (almost-worked ones); trims
  the unfunny ones.
- **Performance budget per round (~90s).** Engine clips weak
  submissions early — Mort starts a line, registers it's not
  working, trails off. Bombing-as-performance is itself a comedic
  format.
- **Tiered performance.** Top 2 get full performance + visuals.
  Middle tier gets text-only delivery. Bottom tier gets dismissed.
  Harsh but preserves room energy.

**Honest party-size cap:** 3–5 players for full performance per
submission. 6–8 needs pre-vote elimination. Beyond 8 needs team
play (different game).

## Replay artifacts — three cuts, three audiences

A 5–7 minute Room's Cut is too long for social sharing. The
session should produce three distinct artifacts:

- **The Room's Cut (5–7 min).** Souvenir for the room. They watched
  it together; that was the experience. Saved to host's account.
  Not the share asset.
- **Highlight reel (45–90 sec, auto-edited).** Top 2 winning bits +
  the best bomb + a closer line, with chapter framing. *This* is
  the share asset. Posts to social with comedian persona. Connects
  to the spec's content-flywheel strategy.
- **Personal highlight (15–30 sec per player).** Each player's
  single best moment from their submissions. Texted to them after
  the session. Bone for non-winners — everyone leaves with shareable
  proof of contribution.

Plus the **Personal Cut** at full length per player (their
submissions across all rounds, performed in voice). Local, not the
shareable, but preserves every contribution end-to-end. The funny
loser still has a complete set in their voice to keep.

**Winner-take-all per round is fine** because the Personal Cut layer
guarantees nobody is shut out. The Room's Cut is canonical (room's
collective best); each player's Personal Cut features their own
submissions for every round.

**Tied or split-vote rounds.** Both winners go into The Room's Cut
as alternative takes; the editing phase chooses or includes both as
"extended cut." Convert ambiguity into content rather than
discarding it.

## Live vs replay visual scope

The visual_performance plan defines 16 visual devices across 4
categories with timing and content_rule layers. Player attention
during live rounds is split across watching, choosing, and voting —
and rendering complex visuals fast is itself a constraint. So:

**Live performance during rounds — constrained subset:**

- Expression changes
- Text emphasis (bold, color, shake on key words)
- One camera move per joke (zoom in/out, snap)
- Stock image drops on punchlines (Cece)
- Stillness/pause (Mort)

**Full visual treatment — reserved for the Room's Cut and highlight
reel.** Cut-ins, screen shake, vfx_overlay, transition_effect,
text_style_break, etc. The replay is where the visual investment
pays off most — viewers watching attentively, render time available.

Visual cue *generation* stays author-side (engine's job, per
performer profiles in `engine/performers/`). Player-controlled
visuals during rounds would fragment performer identity and add
vocabulary load on a 4-second timer. Where the audience does
control visuals: turn-based editing in replay, below.

## Incoherence handling — transitions first, episodic fallback

If round 1's winning bit is about coffee, round 2's about taxes,
round 3's about a haunted dishwasher, the "set" doesn't flow. The
topic anchor handles ~70% of this; the remaining drift needs
explicit treatment.

**Primary fix: transition lines between bits in the replay.** The
engine generates 1–2 sentence bridges in voice, conditioned on
(prior_joke + next_joke + voice). "Speaking of which..." / "And
don't get me started on..." / "It's like — okay, picture this."
Cheap to generate, leverages the narrative layer of the schema,
creates the *illusion of routine flow* even when content is varied.
Real standup uses these constantly.

**Fallback: chapter framing as sketch lineup.** If transitions
don't smooth enough, frame the cut as a sketch show — title cards
between bits ("Bit 4: The Tax Form Incident"), a closer outro from
Mort. SNL Weekend Update is this format and it works. Don't
pretend the room produced a unified routine if it didn't —
chapter framing makes the incoherence a feature.

Ship transitions first. Episodic fallback is the safety net.

## Turn-based visual editing in replay

Audience visual control during simultaneous rounds doesn't time
well with many players. The fix: distribute visual editing across
turns, anchored to joke partitions in the replay.

**Structure:**

- Each player is assigned ONE bit from the cut to direct visually.
  Assignment order: winning submission's author goes first, then
  by descending vote total, then engine-defaults for unowned bits.
- Per-bit direction is **3 pre-curated choices**, not free design.
  "Camera move for the punchline?" with three visual previews.
  "Pacing on the tag — quick, normal, slow burn?" "Visual punch —
  stock image, screen shake, or none?" 30 seconds per player per
  bit.
- Other players watch as each picks; choices preview live so the
  room sees the cut take shape.
- Then the full cut performs with everyone's edits applied.

**Co-credit in the Room's Cut.** Make this explicit: "Bit 3 —
Written by Marcus, Directed by Sarah." Sarah's visual choices
appear in the canonical artifact she didn't write, but her
direction is named. Makes the visual editing role feel like real
authorship, not consolation. Non-winners become collaborators on
winners' bits.

**Edge cases:**

- More players than bits → players who didn't get to direct get an
  "audience reaction" role (they pick whether the imaginary
  audience laughs/groans/applauds at specific moments). Smaller
  authorship but still a turn.
- Fewer players than bits → owners pick multiple, or engine handles
  unowned bits with defaults from the performer profile.

This solves the contribution-gradient problem at the *visual* layer
the same way Personal Cut solves it at the *content* layer: every
player has one explicit, attributed creative slot in the final
product.

## Agency audit — does every player get enough?

Per session, every player gets:

- 5 op picks (own decisions)
- 5 input commits (own text, even if minimal)
- 5 performances of their submissions (their text, in Mort's or
  Cece's voice)
- One visual editing turn in replay (3 pre-curated choices on one
  bit, co-credited)
- Two voting axes (best joke + best craft)
- Personal Cut + Personal Highlight at the end
- Visible attribution on every output (text bolded, op shown)

That's 13 distinct moments of authorship. The persistent-loser at
the room-vote level still leaves with: their personal cut performed
in voice, their visual editorial credit on one canonical bit, their
text bolded in 5 performances, and one shareable highlight. The
shy player has the empty-text-input + op-only path. The
persistent-bomber has the bomb-by-design round (where they likely
win), in-character reaction roasts, and recovery rounds.

The contribution gradient is invisible. The labor is universal (op
pick + commit). The satisfaction is universal (performance +
attribution + Personal Cut + at least one editorial slot).

## Engine demands specific to party mode

Distinct from anything Design 1 needs in solo:

- TTS + cadence/pause/register pipeline must take *arbitrary input
  text* (player submissions), not just engine-generated text.
- Engine must fail-forward — produce entertaining bomb deliveries
  on weak/off-fit submissions, never boring failures.
- Engine must output multiple plausible candidates (Mort's own
  submissions need to be calibrated to roughly match a decent
  human player; the `operation_alternative` branching from v0.9.2
  is useful here — generate two candidates, pick the one that fits
  the room rather than the strongest one).
- Engine must register off-topic drift in voice (Mort's deadpan
  acknowledgment, Cece's bewilderment) without refusing to perform.
- Engine must generate transition lines between bits in replay
  (conditioned on prior_joke + next_joke + voice).
- Engine must compute graph-distance from topic for the soft-nudge
  drift detector.
- Visual cue generation must distinguish live-rendered (constrained
  subset) from replay-rendered (full vocabulary).

These extensions are real, but each maps to existing schema
features (narrative layer, performer profiles, operation_
alternative, concept graph adjacencies). The architecture supports
them; the implementation just hasn't reached for them yet.

## Recommended sequencing

The original spec sequences solo MVP → v1.1 party → v1.2 watch
mode. The reassessment doesn't change the sequence, but it
*reframes* it:

- Solo (Design 1, Director's Console) is the **engine validation
  ground** — proves operation-conditioned generation works and
  teaches comedy theory as a differentiator.
- Party mode is the **engine-leverage ground** — fully exercises
  the performance layer, narrative layer, and visual cues; produces
  shareable content; the strongest standalone product.
- Watch mode (v1.2) is the **roster monetization ground** — pure
  pre-generated content, weekly cadence, parasocial payoff.

Solo-first remains correct as resource sequencing. Party mode is
where the engine's investment finally compounds.
