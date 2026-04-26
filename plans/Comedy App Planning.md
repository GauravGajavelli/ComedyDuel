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
    - Commonsense KB-assisted expansion (see COMET-ATOMIC section below) **[NEW]**
    - Dimension-guided sourcing (query graph for sparse regions, annotate material that fills them)
    - Concept decomposition (split coarse concepts used by 5+ jokes for different purposes)
    - Concept merging (combine duplicates found during weekly review)
    - Cross-concept synthesis (post-Phase-0 — derive new concepts from adjacency intersections)
  - Re-evaluate the same way as with generative sufficiency, but with blind comparisons between generated and real jokes
  - **Commonsense knowledge base for graph enrichment** **[NEW]**
    - The concept graph currently captures concepts and their dimensional co-occurrence adjacencies. What it lacks: the commonsense RELATIONS between concepts (causal, temporal, social — "restaurants HasProperty bills," "bills CausesDesire complaining"). These chains are what underlie observational and articulation humor — the shared knowledge the audience holds
    - **COMET-ATOMIC 2020** (Hwang et al. 2021) is a commonsense knowledge graph with typed relations (causes, effects, attributes, desires, reactions). It can generate inferences like "PersonX goes to restaurant → PersonX wants to order food → PersonX receives a bill → PersonX feels surprised by the total"
    - Use COMET-ATOMIC (or a successor — see research task below) as a **proposal engine for candidate nodes and edges**, NOT as direct graph population. The workflow: (1) query COMET-ATOMIC for relations adjacent to existing attested concepts, (2) present candidates to the annotator/system, (3) accept only candidates that pass a humor-relevance filter (either human judgment or critic model score). This keeps the graph empirically grounded while using the KB to surface candidates that pure attestation would miss
    - **Research task: identify COMET-ATOMIC successor or alternative.** COMET-ATOMIC 2020 was built on GPT-2 / BART. Newer commonsense KBs may offer richer relation types or better coverage. Candidates to evaluate:
      - COMET-ATOMIC 2022 or later versions
      - ConceptNet 5.5+ (broader but less inferential)
      - ATOMIC-10x or other scaled versions
      - LLM-based commonsense inference (prompt a large model directly for relations, compare quality to KB lookup)
      - Evaluate on: relation type coverage (does it have the causal/social chains that comedy needs?), inference quality, API availability, and whether it can be run locally
    - The KB is especially valuable for articulation-type humor: the commonsense chains ARE the shared knowledge that the comedian articulates. If the KB knows "everyone experiences X → everyone feels Y about X → nobody says Y out loud," that's an articulation opportunity the discovery stage can surface
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
- **Multi-candidate generation with structural diversity** **[NEW]**
  - WitScript 3 proves that generating candidates via different mechanisms and selecting the best works. Our system has 6 operations (vs. WitScript's 3) and richer constraints
  - For each prompt: generate one candidate per plausible operation type (e.g., one via extension, one via reinterpretation, one via mapping), then let the critic rank them
  - Structural diversity of candidates is higher than WitScript's because our conditioning signal (full annotation spec) is richer
- **Specialized realization model (from WitScript 2's approach)** **[NEW]**
  - WitScript 2's core idea: fine-tune a small model (BERT) on ~16,700 actual joke punch lines, use it for masked-token filling at the punch position. The model learns distributional patterns of what words tend to appear in the punch position given a topic
  - Our version: fine-tune a small model on the annotated corpus's punch-line text, conditioned on operation type + template + performer. This learns "what words Seinfeld uses at the punch position of an extension joke" vs. "what words for a reinterpretation joke"
  - This is more targeted than prompting a general LLM and more empirically grounded than WitScript's approach because our conditioning signal is richer
  - Could work alongside the general LLM: the specialized model proposes punch-line word candidates, the general LLM constructs the full sentence around them
  - Requires ~50+ annotated jokes per operation type to have enough training data — achievable after 50 episodes (~250 laugh-points)
- **Toplyn's phonemic-matching techniques for wordplay realization** **[NEW]**
  - When the selection stage specifies `operation: wordplay` with a sub-type, the realization stage needs specific word-construction tools. Toplyn's patents provide these:
    - **Phonemic pair**: use CMU Pronouncing Dictionary + edit distance scoring to find word pairs with high phonemic similarity across the two selected concept domains. Toplyn's composite score: 0.5 - 0.40*(edit_distance) + 0.50*(stop_consonant_count) + 0.10*(alliteration). Stop consonants (p, t, k, b, d, g) are funnier — the "hard k" comedy principle
    - **Portmanteau**: decompose multi-token candidate words into sub-tokens, find phonemic matches with words from the other domain, fuse into blended neologism. Filter: the substituted token and the replacing word should share part-of-speech
    - **Collocation disruption**: retrieve known phrases/collocations associated with one concept domain (from a phrase database or n-gram model), find component words with phonemic proximity to words from the other domain, swap
  - These are deterministic algorithms, not LLM prompting — they could run as a pre-realization module that proposes pun candidates, which the LLM then wraps in natural-sounding setup/bridge text
- **Toplyn's forward/backward bridge generation for setup construction** **[NEW]**
  - Toplyn's bridge connects topic to punchline. Our system needs to connect setup to punchline. His bidirectional approach (forward LM generates setup candidates via beam search, backward LM scores for punchline-to-setup coherence) is directly applicable
  - The backward model is especially useful: given a known punchline, score candidate setups by how naturally they lead to it. This prevents the "the setup doesn't earn the punchline" failure mode

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
  - **WitScript system** (3 papers + 1 evaluation, `plans/research/`) **[UPDATED]**
    - Three papers document the evolution: WitScript 1 (wordplay, 2021), WitScript 2 (common sense without wordplay, 2022), WitScript 3 (hybrid of 3 mechanisms, 2023). Plus the 2025 live-performance evaluation
    - **How it actually works** — Toplyn's Basic Joke-Writing Algorithm (5 steps):
      1. Select a topic (one attention-getting sentence)
      2. Select two topic handles (most attention-getting words/phrases)
      3. Generate associations of each handle (what the audience thinks of)
      4. Create a punch line (link an association of one handle to an association of the other, surprisingly)
      5. Generate an angle (text bridging topic to punch line naturally)
    - **Three joke production mechanisms:**
      - WitScript 1: phonemic wordplay (CMU dictionary, edit distance, alliteration/assonance)
      - WitScript 2: common-sense association via Google Word2Vec + BERT fine-tuned on ~16,700 late-night monologue jokes. Key: BERT fills masked tokens in punch-line templates, having learned distributional patterns of actual joke punch lines
      - WitScript 3: generates one candidate per mechanism, GPT-3 selects the funniest
    - **Honest results across papers:**
      - AMT evaluations: WitScript output rated as "a joke" ~44% of the time. Mean quality roughly halfway between raw LLM (GPT-LOL baseline, ~25%) and professional human (~70-85%)
      - 2025 live performance: equivalent Total Laughter to human expert — but used cherry-picked outputs (human expert selected best from multiple generations). Cherry-picking is doing significant work
    - **What validates our approach:** deterministic structural selection + LLM rendering = the same architecture. WitScript proves the hybrid neural-symbolic approach works
    - **What WitScript lacks that we have:** concept graph, performer differentiation, multi-beat routines, subversions, act-out structure, performance layer, audience modeling (shared_experience, universality fields)
    - **What WitScript has that we should learn from:**
      - Association generation via COMET-ATOMIC = concept graph adjacency proposals (see concept expansion section)
      - Fine-tuned BERT for punch-line word selection = specialized realization component (see realization section below)
      - Multi-candidate generation with mechanism diversity (WitScript 3) = our multi-operation candidate approach
      - Internal fitness/filtering function = proto-critic model
    - **Patent cross-reference COMPLETED** **[UPDATED]**
      - Toplyn's patents define 5 joke types + ML bridge generation across 3 patents
      - Punch-line production mechanisms: wordplay/pun (phonemic pair), portmanteau (blended neologism), definition bridge (root definition + template), word chunk substitution (phrase-level swap), semantic incongruity detection, collocation disruption, predicted phrase violation
      - **Key finding: Toplyn's formulas are LEXICAL production mechanisms (how to construct funny words), not COGNITIVE mechanisms (what the punchline does to the setup's frame).** They operate at a different level of the stack than our pivot operations. Toplyn answers "how do I make a funny word?" Our schema answers "what does the punchline do to the audience's frame?"
      - **These are complementary, not competing.** Toplyn's techniques belong in the REALIZATION stage as word-construction methods. Our operations belong in the SELECTION stage as structural decisions. A negation joke could use a Toplyn portmanteau as the vehicle; an extension joke has no Toplyn equivalent because extension requires multi-step reasoning
      - **One genuine gap found: WORDPLAY was absent from our schema.** Phonemic humor (puns, portmanteaus, near-homophones) was not captured by any of the 6 operations. Initially added as a 7th operation, but CORRECTED: wordplay is a DELIVERY VEHICLE for an underlying cognitive operation, not an operation itself. "Tinderella" is mapping + portmanteau (the parallel between dating app and fairy tale, delivered via blended neologism). "Rash Mountain" is transplant + collocation_disruption (disease framework imported into theme park, delivered via phrase substitution). Now added as a 4th modifier sub-dimension alongside reading_switch and scale_shift. Schema v0.8
      - **What to annotate vs. what to generate:** For wordplay jokes, the annotation captures: (1) the cognitive OPERATION (mapping, reinterpretation, transplant, etc.), (2) the wordplay SUB-TYPE (phonemic_pair, portmanteau, collocation_disruption), and (3) the two semantic domains (via concepts). The specific pun words are NOT recorded — they're realization-stage output. The realization stage uses Toplyn's phonemic-matching techniques (edit distance, stop consonant scoring, alliteration) to generate NEW pun words that follow the same pattern
      - Toplyn's book (*Comedy Writing for Late-Night TV*, 2014) remains useful as a source of additional formula patterns not fully described in the patents
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
  - **WitScript as baseline comparison** **[NEW]**: Run WitScript (or a WitScript-equivalent one-liner completion endpoint) on the same game prompts alongside your pipeline. Use the critic to rank your output vs. WitScript's. If your pipeline consistently wins, the architecture is adding value. If WitScript wins on certain prompt types, those are the areas to focus improvement. WitScript is available for licensing — could literally be a baseline module

### Graph ML for concept graph expansion **[NEW]**

- **Priority 3 — after critic is validated and generation pipeline works**
- The concept graph starts with ~200 attested nodes. Graph ML techniques can expand it beyond what annotation alone provides
- **Commonsense KB as proposal engine for candidate nodes/edges** **[NEW]**
  - Use COMET-ATOMIC (or successor — see research task in concept expansion strategy above) to PROPOSE candidate nodes and edges, not to populate them directly
  - Workflow: (1) for each attested concept, query the KB for related concepts via causal/temporal/social relations, (2) filter candidates through the critic model (generate a joke using the candidate pairing, score it — does it produce humor?), (3) accept only candidates that pass the humor-relevance threshold
  - This is the principled middle ground between pure attestation (slow, biased toward annotation choices) and speculative seeding (fast, ungrounded). The KB proposes; the critic validates; the graph stays empirically grounded
  - Especially valuable for articulation: the KB's commonsense chains ("everyone experiences X → everyone feels Y → nobody says Y") surface articulation opportunities the discovery stage can exploit
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

### Priority ordering for generation/expansion work **[UPDATED]**

1. **Humor critic** — test open-source model ranking ability against your judgments. Unblocks automated evaluation. (Can start during annotation Phase 0)
2. **Realization prompt engineering** — write and test 3 prompts on existing 14 annotations. De-risks the hardest technical problem. (Start now)
3. **Multi-candidate generation** — generate one candidate per plausible operation type, critic ranks, top-k go forward. WitScript 3 proves this approach works. (After critic validated)
4. **Research COMET-ATOMIC successor** — evaluate current commonsense KBs for relation type coverage, inference quality, local availability. Need: causal/social chains for articulation humor + entity relations for concept proposals. (Can start during Phase 0 as background research)
5. **Entity ablation on concept graph** — automated commutation test using critic scores. Validates graph quality. (After ~200 concept nodes)
6. **Commonsense KB as concept proposal engine** — COMET-ATOMIC proposes candidate nodes/edges, critic validates humor relevance, graph stays empirically grounded. (After KB selected and critic validated)
7. **Graph ML for link prediction + coverage gaps** — expand graph beyond attestation + KB proposals. (After ablation validates the graph has enough signal)
8. **Specialized realization model** — fine-tune small model on annotated punch-line text, conditioned on operation + template + performer. Requires ~250+ laugh-points. (After 50 episodes annotated)
9. **Toplyn's formula cross-reference** — COMPLETED. Wordplay added as 7th operation. Toplyn's lexical techniques integrated as realization-stage tools. His book remains useful for additional patterns. (Done)
10. **RL for sequential decisions** — subversion timing, set construction. (Phase 2+, after pipeline works end-to-end)

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
8. WitScript papers (all in `plans/research/`) **[UPDATED]**
   - `2302.02008v1.pdf` — WitScript 1 (2021/2022): wordplay-based system, phonemic similarity, CMU dictionary. Mean rating 2.28, 41.5% judged as jokes. Introduces the Basic Joke-Writing Algorithm
   - `2302.03036v1.pdf` — WitScript 2 (2022): common-sense jokes WITHOUT wordplay. Word2Vec + BERT fine-tuned on 16,700 late-night monologue jokes. Mean rating 2.34, 46.2% judged as jokes. Key innovation: fine-tuned BERT for masked punch-line token filling
   - `2301.02695v1.pdf` — WitScript 3 (2023): hybrid of 3 mechanisms (wordplay + common sense + knowledge candidate). Generates 3 candidates, GPT-3 selects best. Mean rating 2.36, 44.1% judged as jokes
   - `2025.chum-1.8.pdf` — Live performance evaluation (2025): cherry-picked WitScript jokes performed by comedian = equivalent Total Laughter to professional human comedy writer. Key metric: Total Laughter = area under dB curve of audience response
   - Key technical details: uses COMET-ATOMIC for commonsense associations, Google Word2Vec for semantic proximity, Pyrhyme for phonemic matching, internal fitness function for filtering. All driven by Toplyn's Basic Joke-Writing Algorithm (5 steps: topic → handles → associations → punch line → angle)
   - Toplyn's book: *Comedy Writing for Late-Night TV* (2014) — source of the joke formulas. Patents: US 10,642,939; US 10,878,817; US 11,080,485
9. Commonsense knowledge bases **[NEW]**
   - COMET-ATOMIC 2020 (Hwang et al. 2021): commonsense KG with typed relations (causes, effects, attributes, desires, reactions). Used by WitScript for association generation
   - Research task: evaluate successors (COMET-ATOMIC 2022+, ConceptNet 5.5+, ATOMIC-10x, LLM-based commonsense inference). Criteria: relation type coverage for comedy (causal/social chains), inference quality, API/local availability
10. Comedy theory grounding **[NEW]**
   - Incongruity theory (Kant, Schopenhauer) — negation, reinterpretation, transplant
   - Bisociation (Koestler 1964) — mapping operation
   - Benign Violation Theory (McGraw & Warren 2010) — articulation operation
   - Social bonding theory — affiliative laughter from recognition
   - GTVH / General Theory of Verbal Humor (Attardo & Raskin) — script opposition framework
   - Schema does not assume all humor is incongruity-based; articulation is grounded in benign violation of the norm of silence
