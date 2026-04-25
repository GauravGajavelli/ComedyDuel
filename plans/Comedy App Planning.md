# Planning

## Strategy

- Mort = Seinfeld
  - Observational comedy maps well
- Automate the annotation and schema evolution **[UPDATED]**
  - Sort of recursive because you have to update everything once the schema changes
  - Schema is now at v0.6 with 6 pivot operations, 7 templates, 6 setup_frame values
  - Automated pipeline: scrape transcripts → parallel agent annotation (5 episodes at a time) → extract to disk → synthesis with gap tracking
  - Schema evolves through vocabulary gap tracker (3-occurrence threshold for new values, 40%-after-30 broadness check for splitting)
  - See: `working/scaling-path.md` for full batch annotation cycle
- Manually audit the annotation quality **[UPDATED]**
  - Three data streams collected in parallel during audit:
    - Laugh-point verification from audio → `working/laugh_points.md`
    - Annotation review (structural) → `working/batch1_reclassification_guide.md`
    - Physical performance observations (visual) → `working/physical_performance_notes.md`
  - See audit checklist in conversation history (laugh-point segmentation, operation classification, v0.6 reclassifications, scale_shift sanity check)
- Have it create prompts to take the annotation and generate them (with performance notes)
  - Compare them to the funniness of the original to gauge generative sufficiency
- Once I have generative sufficiency then work about concept expansion **[UPDATED]**
  - Concept graph expansion strategies (ordered most to least principled):
    - Attestation-driven growth (default — every annotation adds concepts)
    - Adjacency expansion (note dimensional gaps when creating nodes)
    - Dimension-guided sourcing (query graph for sparse regions, annotate material that fills them)
    - Concept decomposition (split coarse concepts used by 5+ jokes for different purposes)
    - Concept merging (combine duplicates found during weekly review)
    - Cross-concept synthesis (post-Phase-0 — derive new concepts from adjacency intersections)
  - Re-evaluate the same way as with generative sufficiency, but with blind comparisons between generated and real jokes
- I think the big things I have to add eventually
  - Long-term planning and callbacks across multiple jokes
  - Breaking the rules: jokes can't seem formulaic, or at the very least formula breakers should be a big part of the mold
    - Already partially addressed: `subversions.yaml` has 5 anti-formula moves (structural_refusal, meta_structural, register_break, specificity_subversion, anti_callback) **[NEW]**
    - And breaker breakers and breaker breaker breakers, etc.
    - The formula can be the basis for a joke; then you do tweaks and alterations in structure and presentation to keep the audience on their toes
      - Example from an observation on my own jokes: https://gemini.google.com/share/0187fb80a315
      - And another joke generation/generalization: https://gemini.google.com/share/8cfd68d23fb5
- Visual delivery and performance **[NEW]**
  - The performer, not just the joke, carries things — need to avoid "HAL 9000 effect"
  - Three visual delivery modes: visual as punctuation, visual as performer, visual as independent comedy layer
  - Rive-based character avatars (web-native, tiny files, state machines map to visual cue vocabulary)
  - MVP fallback: VN sprite sets (8-10 expressions per character)
  - Art styles differ per comedian (Mort: flat/minimal; Cece: saturated/expressive)
  - Physical performance observations from Seinfeld ground the visual device vocabulary empirically
  - See: plan at `.claude/plans/partitioned-exploring-fox.md`

## Phase 0 Steps **[NEW — replaces implicit workflow]**

- Current state: 14/~140 episodes annotated (71 laugh-points), schema v0.6 validated
  - Episodes 1-15 have automated Pass 2 annotations (agent-generated)
  - Episodes 1-15 still need: human audit (laugh points, physical performance, annotation review)
  - No concept graph nodes populated yet

### Immediate next steps (episodes 1-15 audit)

- **Start with your audit of the 14 already-annotated episodes** before annotating more
  - You have agent-generated Pass 2 annotations in `annotations/*.yaml`
  - Audit = watch the performance + collect 3 data streams simultaneously
  - Suggested audit order (for physical performance variety):
    1. **E01 Good News Bad News** — baseline; Jerry relatively still, short monologue
    2. **E03 The Robbery** — extended act-out (the toe bit), lots of physicality
    3. **E07 The Pony Remark** — character voices (leisure police), posture shifts
    4. **E08 The Jacket** — sustained premise (earth outfit), mid-level physicality
    5. **E11 The Statue** — sustained premise (sweepstakes), escalation through performance
    6. Then remaining episodes in any order (E02, E04, E05, E06, E09, E10, E13, E14, E15)
  - After auditing 5 episodes: review physical performance notes, validate/adjust the proposed visual device categories
  - After auditing all 14: first batch review — update gap tallies, apply v0.6 reclassifications

### Annotation expansion (episodes 16-50)

- Scrape and annotate in batches of 5 (agent-parallelized)
- Audit each batch before moving to the next
- Episodes 16-50 span Seinfeld Seasons 2-4, where the standup openings are most substantial
  - Some later episodes have shorter or no openings — check boundaries before annotating
- Target: ~250 total laugh-points, ~200 concept nodes

### Steps to Phase 0 gate (~50 episodes, ~20 hours of audit time)

  1. Audit episodes 1-15 (already annotated — ~4-5 hours)
  2. Annotate + audit episodes 16-50 in batches of 5 (~15 hours)
  3. Populate concept graph from annotations (~200 nodes needed for graph traversal)
  4. Derive performer structural fingerprints from annotation distributions
  5. Hand-trace 10 prompts through full pipeline (discovery → selection → realization)
  6. Gate: hand-traced output at least as good as free-writes → proceed to Phase 1

### De-risk early: realization stage prompt engineering

- **Don't wait for 50 episodes.** Write 3 realization prompts now and test them on the 14 annotated episodes
- The realization prompt takes a structured annotation (concepts + template + voice constraints) and produces a rendered joke sentence
- If the prompt can't produce funny output from a well-annotated joke, more annotations won't fix that
- This is the highest-risk technical problem — the schema is necessary but not sufficient; the LLM has to be funny at the word level
- You'll know within a day whether the architecture's hardest problem is solvable

### Feasibility risks to watch

- **Realization stage is underspecified.** The plan says "hand-trace 10 prompts" but the realization prompt itself hasn't been designed. This is the hardest single task and might take a week of iteration.
- **Concept graph density.** ~200 nodes with ~600 adjacency edges may produce obvious rather than surprising concept pairs. Won't know until you try the discovery stage. If the ratio of productive-to-trivial adjacencies is low, need more annotations or targeted dimension-guided sourcing.
- **Subversion sequencing.** The schema has the subversion *moves* but not the *game theory* of when to deploy them. Every third joke using structural_refusal would itself be formulaic. This is a Phase 1 problem but worth being aware of.
- **Visual delivery is most speculative.** Depends on physical performance observations (not yet collected), Rive authoring (not yet costed), and untested device-to-event mappings. VN sprite fallback is the right hedge — may be the permanent answer if visual vocabulary turns out to be less load-bearing than audio delivery.

### Parallel work during annotation (no dependency)

- Game UI scaffolding, prompt library, TTS evaluation, character art/rigs
- Realization prompt prototyping (de-risk early — see above)

### Key files

- `engine/schema.yaml` — annotation schema
- `engine/vocabularies/pivot-mechanisms.yaml` — 6 humor operations with testable criteria
- `engine/vocabularies/templates.yaml` — 7 rhetorical shapes
- `protocols.md` — multi-pass annotation workflow
- `working/scaling-path.md` — batch annotation cycle instructions for new sessions
- `working/batch1_synthesis.md` — results from first 14 episodes
- `working/questions.md` — open vocabulary gaps with occurrence tracking
- `working/batch1_reclassification_guide.md` — targeted fixes for v0.6 changes
- `working/laugh_points.md` — template for laugh-point verification
- `working/physical_performance_notes.md` — template for physical performance observations
- `annotations/*.yaml` — 14 Pass 2 annotations on disk

## Technical areas

- Comparisons
  - Look at contemporary/SOTA humor engines and see if they could be integrated somehow to address weaknesses
- If there are specific areas (like relatable insight generation) that LLMs struggle on when testing generative sufficiency (i.e., it's the model not the data), think about tuning an open-source model or SLM initially
  - Articulation (shared-truth humor, 15% of corpus) is the hardest to generate — AI must predict what the audience knows-but-hasn't-said, which is different from what training data contains **[NEW]**
  - For instance, Seinfeld used a bunch of great neologisms, which I sort of doubt an LLM could match the quality of consistently
    - Gemini actually make decent standup (given good material) via: https://gemini.google.com/share/e49a04253b53
- Consider using data mining techniques on the annotated jokes to find patterns
  - 71 laugh-points already show: reinterpretation 31%, extension 30%, articulation 15%, negation 10%, transplant 8%, mapping 6% **[NEW]**
  - Also consider deep reinforcement learning, but first consider if this meets the criterion laid out in 490 like the Markov property (doubtful)
- Use a similar tech stack coding style to my team at Toast to ensure that I'm getting the most out of the project
- Long-term strategy
  - If the game works, pivot to the other ideas that need more traction (like business comedy API)
    - Use virality via Chatbase LinkedIn posts/interview

---

# Reference Material

1. Seinfeld book, specials, interviews, etc.
   - https://claude.ai/share/0e5e98d8-b51c-4951-a112-95d766c93adf
     - See latest response for details, lots of other resources also in the early responses
2. Dunkey comment sections
   - I swear to god it's all just people making jokes
3. Siivagunner
4. Arrested Development, Curb, Nathan For You, Simpsons, The Office, Parks and Rec, all of the funniest shows
   - https://www.youtube.com/watch?v=Ry-06Q8V3qU
   - Video essays are probably big
   - Find transcripts online: https://tvshowtranscripts.ourboard.org/viewforum.php?f=1095
5. Clean comedy
   - https://www.thegrablegroup.com/comedy-humor/top-clean-comedians/
6. Project repository reference files **[NEW]**
   - Schema & vocabularies: `engine/schema.yaml`, `engine/vocabularies/*.yaml`
   - Protocols & workflow: `protocols.md`, `working/scaling-path.md`
   - Annotations: `annotations/*.yaml` (14 episodes)
   - Synthesis & tracking: `working/batch1_synthesis.md`, `working/questions.md`
   - Visual delivery plan: `.claude/plans/partitioned-exploring-fox.md`
   - Spec: `spec.md` (architecture, phasing, characters, tech stack)
7. Visual delivery game references **[NEW]**
   - Phoenix Wright / Ace Attorney — pose transitions, screen shakes, text speed
   - Persona 5 — cut-in system, UI disruption as comedy
   - Undertale / Deltarune — character-specific fonts, text effects, portrait swaps
   - West of Loathing — stick-figure simplicity as comedic register
   - Low-effort YouTube editing (JonTron, Dunkey, Internet Historian, Scott the Woz)
   - VTuber/Live2D expression systems, Rive state machines
8. Comedy theory grounding **[NEW]**
   - Incongruity theory (Kant, Schopenhauer) — negation, reinterpretation, transplant
   - Bisociation (Koestler 1964) — mapping operation
   - Benign Violation Theory (McGraw & Warren 2010) — articulation operation
   - Social bonding theory — affiliative laughter from recognition
   - GTVH / General Theory of Verbal Humor (Attardo & Raskin) — script opposition framework
   - Schema does not assume all humor is incongruity-based; articulation is grounded in benign violation of the norm of silence
