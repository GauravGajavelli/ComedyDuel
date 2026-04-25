"""
Fix reclassification for files that use 'jokes' instead of 'annotations'
as the list key, and handle remaining establishes_norm and establishes_category.
"""
import yaml, glob, os

def classify_from_gloss(ann):
    """Reclassify establishes_norm/establishes_category based on gloss."""
    setup = (ann.get("setup_expectation", "") or "").lower()
    violation = (ann.get("punchline_violation", "") or "").lower()
    difficulties = (ann.get("difficulties", "") or "").lower()
    text = (ann.get("text", ann.get("text_span", "")) or "").lower()
    gloss = setup + " " + violation + " " + difficulties + " " + text

    # Convention: cultural practice, social ritual, institutional norm
    if any(w in gloss for w in [
        "culturally loaded", "cultural", "convention", "idiom",
        "gesture", "insult as", "the finger", "middle finger",
        "safety barrier", "institutional", "cheque", "check at",
        "supermarket", "payment method",
    ]):
        return "establishes_convention"

    # Premise: accepted claim or hypothetical the bit builds on
    if any(w in gloss for w in [
        "premise", "accepted", "hypothetical", "prior joke",
        "preceding", "established by", "mapping", "been established",
        "continuing the", "established that", "prior material",
        "the norm of", "norm has been", "already established",
        "historical premise",
    ]):
        return "establishes_premise"

    # Behavior: recognizable behavioral pattern
    if any(w in gloss for w in [
        "behavioral", "behavior", "people do", "men ", "women ",
        "type of person", "have you ever", "drawn to", "tools",
        "working on", "driveway", "lane", "traffic", "flipping",
        "channel", "shopping", "tv", "television", "watching",
        "stereotype", "fumbling", "disorganized",
    ]):
        return "establishes_behavior"

    # Expectation: buildup creating anticipation
    if any(w in gloss for w in [
        "escalating", "building", "investment", "proportional",
        "buildup", "preparation", "reason number", "exciting news",
        "ultimate", "psychological test", "payoff", "anticipat",
    ]):
        return "establishes_expectation"

    # Default
    return "establishes_convention"


changes = 0
for filepath in sorted(glob.glob("annotations/*.yaml")):
    with open(filepath) as f:
        data = yaml.safe_load(f)

    # Find the annotations list regardless of key name
    anns = data.get("annotations", data.get("jokes", []))
    if not anns:
        continue

    modified = False
    for ann in anns:
        sf = ann.get("setup_frame", "")

        # Fix establishes_norm
        if sf == "establishes_norm":
            new_sf = classify_from_gloss(ann)
            ann["setup_frame"] = new_sf
            modified = True
            changes += 1
            print(f"  {ann.get('joke_id','?'):40s} norm → {new_sf}")

        # Fix establishes_category → establishes_premise
        elif sf == "establishes_category":
            ann["setup_frame"] = "establishes_premise"
            modified = True
            changes += 1
            print(f"  {ann.get('joke_id','?'):40s} category → establishes_premise")

        # Add physical_performance if missing
        if "physical_performance" not in ann:
            ann["physical_performance"] = None
            modified = True

    # Update schema version and reviewed flag
    if "schema_version" not in data or data["schema_version"] != "0.6":
        data["schema_version"] = "0.6"
        modified = True
    if "v0_6_reviewed" not in data:
        data["v0_6_reviewed"] = True
        modified = True

    if modified:
        with open(filepath, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                      width=80, sort_keys=False)

print(f"\nTotal setup_frame reclassifications: {changes}")

# Final distribution
print("\n--- FINAL setup_frame distribution ---")
frame_counts = {}
template_counts = {}
total = 0
for filepath in sorted(glob.glob("annotations/*.yaml")):
    data = yaml.safe_load(open(filepath))
    for ann in data.get("annotations", data.get("jokes", [])):
        total += 1
        sf = ann.get("setup_frame", "unknown")
        frame_counts[sf] = frame_counts.get(sf, 0) + 1
        pt = ann.get("primary_template", "unknown")
        template_counts[pt] = template_counts.get(pt, 0) + 1

for k, v in sorted(frame_counts.items(), key=lambda x: -x[1]):
    print(f"  {k:30s} {v:3d}  ({v/total*100:.0f}%)")

print(f"\n--- FINAL template distribution ---")
for k, v in sorted(template_counts.items(), key=lambda x: -x[1]):
    print(f"  {k:30s} {v:3d}  ({v/total*100:.0f}%)")
