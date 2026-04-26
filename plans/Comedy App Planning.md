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
- Act-out comedy as a generation strength **[NEW]**
  - Act-outs (comedian plays a character in dialogue) are extremely common in Seinfeld — present in ~60%+ of annotated monologues. They are the same mechanism as conversational roast comedy (Curb Your Enthusiasm, roast battles) performed solo
  - The cognitive process is identical: identify exploitable premise → select a character perspective that maximizes the comedic gap → construct dialogue in that character's register → the register gap between character and reality is an independent humor source
  - Act-outs are EASIER for LLMs to generate than pure observational humor because the character voice gives the LLM a concrete persona to inhabit. "Speak as this character in this situation" is a more constrained (and therefore more reliable) prompt than "make an original observation about the human condition"
  - Schema now captures act-out structure: `joke.structure.act_out` block with `character_type` (authority / everyman / enthusiast / expert / innocent), `character_register` (confident / bewildered / earnest / bureaucratic / casual), and `register_gap` (treats_mundane_as_serious / treats_serious_as_mundane / unaware_of_absurdity / performed_sincerity / none)
  - For Mort: deadpan voice INTRODUCING a character, then committed PERFORMANCE of that character = automatic register gap. This is Norm Macdonald's signature move
  - For Cece: anthropomorphized concepts (the Little Guilt) become characters she voices. The act-out format is the natural vehicle for her Capitalized Proper Noun concepts
  - Act-outs are also where the visual delivery system does its best work — pose_shift, expression_change at character transitions are exactly what Ace Attorney's system was designed for
  - Future application: the critic AI's in-voice reactions to player jokes use the same target-exploitation mechanism — scan player's joke for exploitable features, construct character response

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
  - **WitScript** (Toplyn & Amir 2025, `plans/research/2025.chum-1.8.pdf`) **[NEW]**
    - Hybrid neural-symbolic system: deterministic joke formulas select structural move + key concept, GPT renders surface text under tight constraints, human expert cherry-picks best output
    - Validated: AI jokes elicited statistically equivalent laughter to a professional human comedy writer in live standup performance (Total Laughter metric, N=48 audience members)
    - The funniest single joke (TL: 241) was AI-written
    - Validates our pipeline architecture: deterministic structural selection + LLM rendering = the same approach, different implementation
    - Key difference: WitScript's formulas are hand-coded by a pro comedy writer; our system derives them from annotation. Both work; ours is more extensible but unproven at Toplyn's quality level
    - WitScript doesn't have: concept graph, performer differentiation, subversions, multi-beat routines, or performance layer. Our system is more ambitious = more risk but higher ceiling
- If there are specific areas (like relatable insight generation) that LLMs struggle on when testing generative sufficiency (i.e., it's the model not the data), think about tuning an open-source model or SLM initially
  - Articulation (shared-truth humor, 15% of corpus) is the hardest to generate — AI must predict what the audience knows-but-hasn't-said, which is different from what training data contains **[NEW]**
  - For instance, Seinfeld used a bunch of great neologisms, which I sort of doubt an LLM could match the quality of consistently
    - Gemini actually make decent standup (given good material) via: https://gemini.google.com/share/e49a04253b53

### Humor critic model **[NEW]**

- **Priority 1 — build this first, it unblocks everything else**
- Thinking AI models can reliably RANK joke funniness (ordinal signal) even when they can't RATE it (cardinal signal). Ordinal is sufficient — need "A is funnier than B," not "A is 7.3/10"
- Clean comedy won't trip guardrails — real advantage over edgy humor systems
- Approach options (ordered by effort):
  1. **Zero-shot ranking**: Test Llama 3.1 70B (or similar open-source) with a ranking prompt against your own ordinal judgments of the 14 annotated episodes. If Spearman rank correlation >0.7, it's useful as-is
  2. **Fine-tuned ranker**: Fine-tune on 500-1000 paired humor comparisons. Training data: generate multiple realization candidates for the same structural spec, have humans rank them
  3. **WitScript-style Total Laughter proxy**: If you ever get live audience data, train on actual laughter measurements (dB × time, per the WitScript paper's methodology)
- What the critic enables:
  - **Automated candidate selection**: Realization stage generates N candidates per structural spec, critic ranks them, top-k go forward. This replaces WitScript's manual cherry-picking
  - **Concept graph validation**: Entity ablation — remove a concept, regenerate jokes, see if critic scores drop
  - **Realization prompt iteration**: Rapidly test different constraint formulations without manual evaluation

### Graph ML for concept graph expansion **[NEW]**

- **Priority 3 — after critic is validated and generation pipeline works**
- The concept graph starts with ~200 attested nodes. Graph ML techniques can expand it beyond what annotation alone provides
- **Entity ablation** (automated commutation test):
  - For each concept node, generate 10 jokes referencing it, score with critic
  - Remove the node, regenerate same jokes with nearest adjacency substituted, score again
  - Delta = the node's humor contribution. Zero/negative delta = dead weight, candidate for removal
  - This is the generation-side equivalent of Pass 4's commutation test
- **Link prediction** for unadjacent concept pairs:
  - Train on existing attested adjacencies to predict which concept pairs SHOULD be adjacent
  - Concepts with predicted-but-unattested adjacencies are candidates for the discovery stage to explore
  - This automates the "cross-concept synthesis" expansion strategy
- **Node embedding** for coverage gap detection:
  - Learn dense embeddings from node dimensions + adjacency structure
  - Concepts with similar embeddings but no adjacency edge = unexplored productive pairings
  - Sparse regions in embedding space = systematic coverage gaps
- **Graph attention networks** for edge weighting:
  - Weight adjacency edges by humor contribution (from ablation scores)
  - High-weight edges = productive pairings the discovery stage should prioritize
  - Low-weight edges = noise the discovery stage should deprioritize
- This is NOT a GAN — it's closer to a **graph-based evolutionary algorithm with a learned fitness function**: evolve the symbolic graph structure using neural critic scores as the fitness signal

### Deep RL for sequential comedy decisions **[NEW]**

- **Priority 5 — defer to Phase 2+ when pipeline works and data exists**
- Markov property concern is valid: optimal next joke depends on full history (prior jokes, audience expectations, established patterns), not just current state
- Reward signal is sparse and delayed: a callback's funniness depends on the setup joke from 5 minutes ago — temporal credit assignment is hard
- **Where RL could work (narrower scope):**
  - **Subversion timing**: When to deploy structural_refusal vs. playing it straight. This IS a sequential decision with clearer state (jokes since last subversion, template pattern so far). RL agent could learn optimal subversion frequency
  - **Concept selection across a set**: Given performer profile + set-length target, which concept sequence produces the best overall set? Closer to a recommendation system; policy gradient methods could optimize the trajectory
  - **Realization candidate selection**: Given N renderings of the same spec, learn a selection policy. This is a bandit problem (simpler than full RL) where the critic is the reward signal
- **Recommendation**: The simpler loop (generate candidates → rank with critic → keep best) gets 80% of the value without RL infrastructure. RL adds value specifically for sequential decisions (set construction, subversion timing) which need a working pipeline first

### Priority ordering for generation/expansion work **[NEW]**

1. **Humor critic** — test open-source model ranking ability against your judgments. Unblocks automated evaluation. (Can start during annotation Phase 0)
2. **Realization prompt engineering** — write and test 3 prompts on existing 14 annotations. De-risks the hardest technical problem. (Start now)
3. **Critic-driven candidate selection** — generate N, rank, keep top-k. First practical use of the critic. (After critic validated)
4. **Entity ablation on concept graph** — automated commutation test using critic scores. Validates graph quality. (After ~200 concept nodes)
5. **Graph ML for link prediction + coverage gaps** — expand graph beyond attestation. (After ablation validates the graph has enough signal)
6. **RL for sequential decisions** — subversion timing, set construction. (Phase 2+, after pipeline works end-to-end)

- Consider using data mining techniques on the annotated jokes to find patterns
  - 71 laugh-points already show: reinterpretation 31%, extension 30%, articulation 15%, negation 10%, transplant 8%, mapping 6% **[NEW]**
  - Also consider deep reinforcement learning, but first consider if this meets the criterion laid out in 490 like the Markov property (doubtful — see RL section above for nuanced assessment)
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
8. WitScript paper **[NEW]**
   - Toplyn & Amir 2025: "Can AI Make Us Laugh? Comparing Jokes Generated by Witscript and a Human Expert"
   - `plans/research/2025.chum-1.8.pdf`
   - Key result: AI jokes = human expert jokes in live audience laughter (Total Laughter metric)
   - Key method: hybrid neural-symbolic (deterministic formulas + LLM rendering + human cherry-picking)
   - Key metric: Total Laughter = area under dB curve of audience response (better than numerical ratings)
9. Comedy theory grounding **[NEW]**
   - Incongruity theory (Kant, Schopenhauer) — negation, reinterpretation, transplant
   - Bisociation (Koestler 1964) — mapping operation
   - Benign Violation Theory (McGraw & Warren 2010) — articulation operation
   - Social bonding theory — affiliative laughter from recognition
   - GTVH / General Theory of Verbal Humor (Attardo & Raskin) — script opposition framework
   - Schema does not assume all humor is incongruity-based; articulation is grounded in benign violation of the norm of silence
