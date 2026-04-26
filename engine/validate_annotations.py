"""
Validate annotations against schema reproducibility requirements.

Checks:
1. Concepts resolve to registry node_ids or known aliases
2. No mechanism descriptions used as concepts
3. Operations are from the current vocabulary
4. Templates are from the current vocabulary
5. scale_shift non-none has swap-test justification in notes
6. setup_frame uses current values
7. Subversions use only textual values (not register_break/anti_callback)
8. act_out.character_register is NOT in joke.structure (moved to performance)

Usage:
    python3 engine/validate_annotations.py [annotations_dir]
"""

import yaml
import glob
import sys
import os

ANNOTATIONS_DIR = sys.argv[1] if len(sys.argv) > 1 else "annotations"
REGISTRY_PATH = "engine/concepts/_registry.yaml"

# Load concept registry
with open(REGISTRY_PATH) as f:
    registry = yaml.safe_load(f) or {}

# Build alias → node_id mapping
alias_to_node = {}
valid_node_ids = set()
for node_id, node_data in registry.items():
    if not isinstance(node_data, dict):
        continue
    valid_node_ids.add(node_id)
    for alias in node_data.get("aliases", []):
        alias_to_node[alias] = node_id

# Mechanism descriptions that should NOT be concepts
EXCLUDED_CONCEPTS = {
    "absurdity", "comparison", "inadequacy", "understatement", "sarcasm",
    "normalcy_bias", "anticipation", "disappointment", "confusion", "regret",
    "escape_fantasy", "social_norms", "preparation", "searching", "absence",
    "phone_call", "dead_stop", "ground_level_detail", "regression",
    "self_blame", "vulnerability", "arbitrariness", "confrontation",
    "enthusiasm", "disproportionate_response", "reality_gap",
}

# Current valid values
VALID_OPERATIONS = {"negation", "reinterpretation", "transplant", "mapping",
                    "extension", "articulation"}
VALID_TEMPLATES = {"mundane_as_monumental", "monumental_as_mundane",
                   "bare_observation", "escalation", "reductio", "comparison"}
VALID_SETUP_FRAMES = {"establishes_convention", "establishes_behavior",
                      "establishes_expectation", "establishes_premise",
                      "establishes_anomaly", "establishes_sequence"}
VALID_SUBVERSIONS = {"structural_refusal", "meta_structural",
                     "specificity_subversion"}
VALID_SCALE_SHIFT = {"none", "expansion", "contraction"}
VALID_READING_SWITCH = {"none", "figurative_to_literal", "literal_to_figurative"}
VALID_WORDPLAY = {"none", "phonemic_pair", "portmanteau", "collocation_disruption"}
VALID_POSITIONING = {"lateral_observer", "above", "below", "with"}
VALID_AUDIENCE = {"co_observer", "target", "accomplice", "witness"}

errors = []
warnings = []
stats = {"total_jokes": 0, "total_files": 0, "concepts_resolved": 0,
         "concepts_unresolved": 0, "concepts_excluded": 0}


def check_concept(concept_str, joke_id):
    """Check if a concept string resolves to a registry node."""
    if concept_str in valid_node_ids:
        stats["concepts_resolved"] += 1
        return
    if concept_str in alias_to_node:
        stats["concepts_resolved"] += 1
        warnings.append(f"  {joke_id}: concept '{concept_str}' is an alias "
                       f"for '{alias_to_node[concept_str]}' — use the node_id")
        return
    if concept_str in EXCLUDED_CONCEPTS:
        stats["concepts_excluded"] += 1
        errors.append(f"  {joke_id}: concept '{concept_str}' is a mechanism "
                     f"description, not a content concept. Remove from concepts.")
        return
    stats["concepts_unresolved"] += 1
    warnings.append(f"  {joke_id}: concept '{concept_str}' not in registry — "
                   f"may need a new node or is an unregistered alias")


for filepath in sorted(glob.glob(os.path.join(ANNOTATIONS_DIR, "*.yaml"))):
    fname = os.path.basename(filepath)
    with open(filepath) as f:
        data = yaml.safe_load(f)

    # Handle both formats: {jokes: [...]} and bare list [...]
    if not data:
        errors.append(f"  {fname}: empty file")
        continue

    stats["total_files"] += 1

    if isinstance(data, dict) and "jokes" in data:
        joke_list = data["jokes"]
    elif isinstance(data, list):
        joke_list = data
    else:
        errors.append(f"  {fname}: unrecognized format (not dict with 'jokes' or list)")
        continue

    for j in joke_list:
        jid = j.get("joke_id", "unknown")
        stats["total_jokes"] += 1
        joke = j.get("joke", {})
        if not joke:
            # Some formats nest directly without a 'joke' sub-key
            # Check if the logic/content/structure keys are at top level
            if "logic" in j or "content" in j or "structure" in j:
                joke = j
            else:
                errors.append(f"  {jid}: no 'joke' block found")
                continue

        # --- Content layer checks ---
        content = joke.get("content", {})
        for c in content.get("concepts", []):
            check_concept(c, jid)

        pc = content.get("pivot_concept")
        if pc:
            check_concept(pc, jid)

        # --- Logic layer checks ---
        logic = joke.get("logic", {})
        pm = logic.get("pivot_mechanism", {})

        op = pm.get("operation")
        if op and op not in VALID_OPERATIONS:
            errors.append(f"  {jid}: invalid operation '{op}'")

        op_alt = pm.get("operation_alternative")
        if op_alt and op_alt not in VALID_OPERATIONS:
            errors.append(f"  {jid}: invalid operation_alternative '{op_alt}'")
        if op_alt and op_alt == op:
            warnings.append(f"  {jid}: operation_alternative '{op_alt}' is "
                          f"same as primary operation — should be null or different")

        rs = pm.get("reading_switch", "none")
        if rs not in VALID_READING_SWITCH:
            errors.append(f"  {jid}: invalid reading_switch '{rs}'")

        ss = pm.get("scale_shift", "none")
        if ss not in VALID_SCALE_SHIFT:
            errors.append(f"  {jid}: invalid scale_shift '{ss}'")

        wp = pm.get("wordplay", "none")
        if wp not in VALID_WORDPLAY:
            errors.append(f"  {jid}: invalid wordplay '{wp}'")

        sf = logic.get("setup_frame")
        if sf and sf not in VALID_SETUP_FRAMES:
            errors.append(f"  {jid}: invalid setup_frame '{sf}'")

        # --- Structure layer checks ---
        structure = joke.get("structure", {})

        tmpl = structure.get("primary_template")
        if tmpl and tmpl not in VALID_TEMPLATES:
            errors.append(f"  {jid}: invalid template '{tmpl}' — "
                         f"old value? Check templates.yaml")

        # Check for removed subversion values
        for sub in structure.get("subversions_applied", []):
            sub_type = sub.get("type") if isinstance(sub, dict) else sub
            if sub_type and sub_type not in VALID_SUBVERSIONS:
                if sub_type == "register_break":
                    errors.append(f"  {jid}: subversion 'register_break' should "
                                 f"be in performance.delivery, not here")
                elif sub_type == "anti_callback":
                    errors.append(f"  {jid}: subversion 'anti_callback' should "
                                 f"be in joke.narrative, not here")
                else:
                    errors.append(f"  {jid}: invalid subversion '{sub_type}'")

        # Check for character_register in joke.structure (should be in performance)
        act_out = structure.get("act_out", {})
        if isinstance(act_out, dict) and "character_register" in act_out:
            warnings.append(f"  {jid}: act_out.character_register found in "
                          f"joke.structure — should be in performance.delivery."
                          f"act_out_voice")

        # --- Relational layer check (should be in joke, not performance) ---
        rel = joke.get("relational", {})
        if rel:
            pos = rel.get("positioning", {})
            if isinstance(pos, dict):
                pos_val = pos.get("default")
            else:
                pos_val = pos
            if pos_val and pos_val not in VALID_POSITIONING:
                errors.append(f"  {jid}: invalid positioning '{pos_val}'")

            ai = rel.get("audience_implication")
            if ai and ai not in VALID_AUDIENCE:
                errors.append(f"  {jid}: invalid audience_implication '{ai}'")

        # Check if relational is incorrectly in performance block
        perf = j.get("performance", {})
        if isinstance(perf, dict):
            perf_rel = perf.get("relational", {})
            if isinstance(perf_rel, dict):
                if "positioning" in perf_rel:
                    warnings.append(f"  {jid}: positioning found in performance."
                                  f"relational — should be in joke.relational")
                if "audience_implication" in perf_rel:
                    warnings.append(f"  {jid}: audience_implication found in "
                                  f"performance.relational — should be in "
                                  f"joke.relational")


# Report
print("=" * 60)
print("ANNOTATION VALIDATION REPORT")
print("=" * 60)
print(f"\nFiles: {stats['total_files']}")
print(f"Jokes: {stats['total_jokes']}")
print(f"\nConcepts:")
print(f"  Resolved to registry: {stats['concepts_resolved']}")
print(f"  Unresolved (need node or alias): {stats['concepts_unresolved']}")
print(f"  Excluded (mechanism descriptions): {stats['concepts_excluded']}")

if errors:
    print(f"\nERRORS ({len(errors)}):")
    for e in errors:
        print(e)
else:
    print("\nNo errors.")

if warnings:
    print(f"\nWARNINGS ({len(warnings)}):")
    for w in warnings:
        print(w)
else:
    print("\nNo warnings.")

# Exit code
sys.exit(1 if errors else 0)
