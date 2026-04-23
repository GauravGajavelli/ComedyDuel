"""
Validate the joke annotation schema against the 5 Seinfeld monologues.

Tests:
  1. Schema consistency: every component has required fields
  2. Mutual exclusivity: each dimension's value comes from its enum
  3. Reconstruction: concatenated component text approximates the original
  4. Coverage stats: distribution across all taxonomic dimensions
"""

import yaml
import os
from collections import Counter

SCHEMA_PATH = "/Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/vocabularies/joke_annotation_schema.yaml"
ANNOTATIONS_PATH = "/Users/gauravgajavelli/Documents/GitHub/ComedyDuel/engine/vocabularies/annotated_monologues.yaml"

with open(SCHEMA_PATH) as f:
    schema = yaml.safe_load(f)

with open(ANNOTATIONS_PATH) as f:
    annotations = yaml.safe_load(f)

# Extract valid enums from schema
VALID_ROLES = set(schema['structural_role'].keys())
VALID_MECHANISMS = set(schema['mechanism'].keys())
VALID_PERF_MODES = set(schema['performance_mode'].keys())
VALID_REGISTERS = set(schema['observational_register'].keys())
VALID_TOPICS = set(schema['topic_domain'].keys())
MECHANISM_ROLES = {'punchline', 'tag', 'topper'}

print("=" * 70)
print("SCHEMA VALIDATION REPORT")
print("=" * 70)

errors = []
warnings = []

# Counters for coverage
role_counts = Counter()
mechanism_counts = Counter()
perf_counts = Counter()
register_counts = Counter()
topic_counts = Counter()

total_components = 0
total_beats = 0
total_bits = 0

for routine in annotations['routines']:
    print(f"\n--- {routine['episode']} ---")
    reconstructed_parts = []

    for bit in routine['bits']:
        total_bits += 1

        # Check topic_domain
        td = bit.get('topic_domain')
        if td not in VALID_TOPICS:
            errors.append(f"  [{routine['episode']}] Invalid topic_domain: {td}")
        else:
            topic_counts[td] += 1

        for beat in bit['beats']:
            total_beats += 1

            # Check observational_register
            oreg = beat.get('observational_register')
            if oreg not in VALID_REGISTERS:
                errors.append(f"  [{beat['beat_id']}] Invalid register: {oreg}")
            else:
                register_counts[oreg] += 1

            for comp in beat['components']:
                total_components += 1

                # Check structural_role
                role = comp.get('structural_role')
                if role not in VALID_ROLES:
                    errors.append(f"  [{beat['beat_id']}] Invalid role: {role}")
                else:
                    role_counts[role] += 1

                # Check performance_mode
                pm = comp.get('performance_mode')
                if pm not in VALID_PERF_MODES:
                    errors.append(f"  [{beat['beat_id']}] Invalid performance_mode: {pm}")
                else:
                    perf_counts[pm] += 1

                # Check mechanism (required for punchline/tag/topper)
                mech = comp.get('mechanism')
                if role in MECHANISM_ROLES:
                    if mech is None:
                        errors.append(f"  [{beat['beat_id']}] Missing mechanism for {role}")
                    elif mech not in VALID_MECHANISMS:
                        errors.append(f"  [{beat['beat_id']}] Invalid mechanism: {mech}")
                    else:
                        mechanism_counts[mech] += 1
                elif mech is not None:
                    warnings.append(f"  [{beat['beat_id']}] Mechanism '{mech}' on non-humor role '{role}' (ignored)")

                # Collect text for reconstruction
                text = comp.get('text', '')
                sd = comp.get('stage_direction', '')
                if text:
                    reconstructed_parts.append(text)
                if sd:
                    reconstructed_parts.append(sd)

    # Show reconstruction preview
    full_text = ' '.join(reconstructed_parts)
    preview = full_text[:200] + '...' if len(full_text) > 200 else full_text
    print(f"  Bits: {len(routine['bits'])}")
    print(f"  Reconstruction preview: {preview}")

# Report
print("\n" + "=" * 70)
print("VALIDATION RESULTS")
print("=" * 70)

if errors:
    print(f"\nERRORS ({len(errors)}):")
    for e in errors:
        print(f"  {e}")
else:
    print("\n  No errors found.")

if warnings:
    print(f"\nWARNINGS ({len(warnings)}):")
    for w in warnings:
        print(f"  {w}")

print(f"\n--- COVERAGE STATISTICS ---")
print(f"Total routines: {len(annotations['routines'])}")
print(f"Total bits: {total_bits}")
print(f"Total beats: {total_beats}")
print(f"Total components: {total_components}")

print(f"\nStructural roles:")
for role, cnt in role_counts.most_common():
    print(f"  {role:20s} {cnt:3d}  ({cnt/total_components*100:.0f}%)")

print(f"\nMechanisms (on punchlines/tags/toppers only):")
for mech, cnt in mechanism_counts.most_common():
    print(f"  {mech:20s} {cnt:3d}")

print(f"\nPerformance modes:")
for pm, cnt in perf_counts.most_common():
    print(f"  {pm:20s} {cnt:3d}")

print(f"\nObservational registers:")
for oreg, cnt in register_counts.most_common():
    print(f"  {oreg:20s} {cnt:3d}")

print(f"\nTopic domains:")
for td, cnt in topic_counts.most_common():
    print(f"  {td:20s} {cnt:3d}")

# Check for unused schema values
print(f"\n--- UNUSED SCHEMA VALUES ---")
unused_roles = VALID_ROLES - set(role_counts.keys())
unused_mechs = VALID_MECHANISMS - set(mechanism_counts.keys())
unused_perfs = VALID_PERF_MODES - set(perf_counts.keys())
unused_regs = VALID_REGISTERS - set(register_counts.keys())
unused_topics = VALID_TOPICS - set(topic_counts.keys())

for name, unused in [('Roles', unused_roles), ('Mechanisms', unused_mechs),
                      ('Perf modes', unused_perfs), ('Registers', unused_regs),
                      ('Topics', unused_topics)]:
    if unused:
        print(f"  {name}: {', '.join(sorted(unused))}")
    else:
        print(f"  {name}: (all used)")

print("\n" + "=" * 70)
print("DONE")
print("=" * 70)
