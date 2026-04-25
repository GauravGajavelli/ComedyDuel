"""
Reclassify batch 1 annotations to schema v0.6.

Changes per annotation:
1. schema_version → "0.6"
2. Add v0_6_reviewed: true
3. Add physical_performance: null to each laugh-point
4. Reclassify setup_frame: establishes_norm → convention/behavior/premise/expectation
5. Reclassify flagged template candidates → monumental_as_mundane or shared_recognition

setup_frame reclassification uses keyword matching on the gloss fields
(setup_expectation, punchline_violation, difficulties) as a heuristic.
Results should be audited by the human reviewer.

Template reclassifications are based on the explicit candidate list from
working/batch1_reclassification_guide.md.
"""

import yaml
import re
import glob
import os

# Template reclassification candidates (from the guide)
MONUMENTAL_AS_MUNDANE = {
    # (file_slug, joke_id_substring): identifies the specific laugh-point
    ("s01e03", "opening_02"): True,   # "isn't it?" closing button
    ("s01e06", "lp6"): True,          # backwards traffic banal complaint
    ("s01e08", "lp2"): True,          # alien outfit committee
    ("s01e10", "lp5"): True,          # Star Trek as living room
    ("s01e10", "lp6"): True,          # aliens as Friday-night visitors
    ("s01e10", "lp7"): True,          # Klingon boxing
}

SHARED_RECOGNITION = {
    # s01e01 LP3 already done manually
    ("s01e04", "lp3"): True,          # Philips head
    ("s01e04", "lp2"): True,          # "Honey, I think Jim's working on something"  -- tag
    ("s01e09", "lp1"): True,          # chip crumbs on sofa
}


def classify_setup_frame(annotation):
    """Reclassify establishes_norm based on gloss content."""
    setup = annotation.get("setup_expectation", "") or ""
    violation = annotation.get("punchline_violation", "") or ""
    difficulties = annotation.get("difficulties", "") or ""
    gloss = (setup + " " + violation + " " + difficulties).lower()

    # Check for establishes_sequence or establishes_anomaly (keep as-is)
    current = annotation.get("setup_frame", "")
    if current in ("establishes_sequence", "establishes_anomaly"):
        return current

    if current != "establishes_norm":
        return current

    # Convention signals: cultural practice, social ritual, institutional norm
    convention_signals = [
        "cultural", "convention", "idiom", "ritual", "institutional",
        "gesture", "insult", "payment", "cheque", "check ", "finger",
        "loaded", "safety", "fence", "register of", "register cues",
        "philosophical", "existential", "how things work",
        "recognized norm", "social norm", "culturally",
    ]

    # Behavior signals: recognizable behavioral pattern
    behavior_signals = [
        "behavior", "behavioral", "people do", "men do", "women do",
        "type of person", "you know this type", "have you ever noticed",
        "drawn to", "magnetically", "men like", "women are",
        "flipping", "channel", "lane", "traffic", "shopping",
        "congregat", "tools", "working on", "driveway",
        "tv", "television", "watching",
    ]

    # Premise signals: accepted claim or hypothetical
    premise_signals = [
        "premise", "accepted", "hypothetical", "established by",
        "preceding", "prior joke", "if ", "what if",
        "fashion will", "won't exist", "body parts as",
        "traffic will", "appetites", "ruining", "cookie",
        "sweepstakes", "honest", "been established",
        "accepted as given", "the norm of", "accepting",
    ]

    # Expectation signals: buildup creating anticipation
    expectation_signals = [
        "escalating", "list of", "building", "investment",
        "proportional", "buildup", "preparation",
        "reason number", "exciting news", "ultimate",
        "psychological test", "expect", "payoff",
    ]

    # Score each category
    scores = {
        "establishes_convention": sum(1 for s in convention_signals if s in gloss),
        "establishes_behavior": sum(1 for s in behavior_signals if s in gloss),
        "establishes_premise": sum(1 for s in premise_signals if s in gloss),
        "establishes_expectation": sum(1 for s in expectation_signals if s in gloss),
    }

    # Pick highest score; default to convention if tied/zero
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "establishes_convention"  # safe default for cultural norms
    return best


def should_be_monumental_as_mundane(filepath, joke_id):
    """Check if this laugh-point is a monumental_as_mundane candidate."""
    slug = os.path.basename(filepath).replace("_pass2_decomposition.yaml", "")
    for (file_slug, id_substr), _ in MONUMENTAL_AS_MUNDANE.items():
        if file_slug in slug and id_substr in (joke_id or "").lower():
            return True
    return False


def should_be_shared_recognition(filepath, joke_id):
    """Check if this laugh-point is a shared_recognition candidate."""
    slug = os.path.basename(filepath).replace("_pass2_decomposition.yaml", "")
    for (file_slug, id_substr), _ in SHARED_RECOGNITION.items():
        if file_slug in slug and id_substr in (joke_id or "").lower():
            return True
    return False


def process_file(filepath):
    """Process one annotation file."""
    with open(filepath) as f:
        content = f.read()

    # Skip if already processed
    if "v0_6_reviewed" in content:
        return 0, filepath

    data = yaml.safe_load(content)
    changes = 0

    # 1. Update schema version
    if data.get("schema_version") != "0.6":
        data["schema_version"] = "0.6"
        changes += 1

    # 2. Add v0_6_reviewed
    data["v0_6_reviewed"] = True
    changes += 1

    # 3-5. Process each annotation
    annotations = data.get("annotations", [])
    for ann in annotations:
        joke_id = ann.get("joke_id", "")

        # Add physical_performance if missing
        if "physical_performance" not in ann:
            ann["physical_performance"] = None
            changes += 1

        # Reclassify setup_frame
        old_frame = ann.get("setup_frame", "")
        if old_frame == "establishes_norm":
            new_frame = classify_setup_frame(ann)
            ann["setup_frame"] = new_frame
            changes += 1

        # Reclassify template candidates
        old_template = ann.get("primary_template", "")
        if should_be_monumental_as_mundane(filepath, joke_id):
            if old_template == "mundane_as_monumental":
                ann["primary_template"] = "monumental_as_mundane"
                changes += 1
        elif should_be_shared_recognition(filepath, joke_id):
            if old_template in ("mundane_as_monumental", "false_equivalence"):
                ann["primary_template"] = "shared_recognition"
                changes += 1

    # Write back
    # Use custom dumper to preserve readability
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                  width=80, sort_keys=False)

    return changes, filepath


# Process all files
total_changes = 0
for filepath in sorted(glob.glob("annotations/*.yaml")):
    changes, path = process_file(filepath)
    if changes > 0:
        print(f"  UPDATED {os.path.basename(path)}: {changes} changes")
    else:
        print(f"  skip    {os.path.basename(path)}")

print(f"\nTotal changes across all files: {total_changes}")

# Validation: count the distribution
print("\n--- setup_frame distribution ---")
frame_counts = {}
template_counts = {}
for filepath in sorted(glob.glob("annotations/*.yaml")):
    data = yaml.safe_load(open(filepath))
    for ann in data.get("annotations", []):
        sf = ann.get("setup_frame", "unknown")
        frame_counts[sf] = frame_counts.get(sf, 0) + 1
        pt = ann.get("primary_template", "unknown")
        template_counts[pt] = template_counts.get(pt, 0) + 1

total = sum(frame_counts.values())
for k, v in sorted(frame_counts.items(), key=lambda x: -x[1]):
    print(f"  {k:30s} {v:3d}  ({v/total*100:.0f}%)")

print(f"\n--- template distribution ---")
for k, v in sorted(template_counts.items(), key=lambda x: -x[1]):
    print(f"  {k:30s} {v:3d}  ({v/total*100:.0f}%)")
