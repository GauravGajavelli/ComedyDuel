#!/usr/bin/env python3
"""
Build an audit markup sheet for S02E10 from the raw script and annotation.
Extracts the opening monologue, formats one clause per line, appends
agent laugh-points from the annotation YAML.
"""

import re
import yaml

SCRIPT_PATH = "../engine/raw_scripts/The_Baby_Shower.txt"
ANNOTATION_PATH = "../annotations/s02e10_opening_pass2.yaml"
OUTPUT_PATH = "audit_sheets/s02e10_markup.md"

# --- Read script (first 200 lines only) ---
with open(SCRIPT_PATH, "r") as f:
    lines = [line.rstrip() for line in f.readlines()[:200]]

# --- Find monologue boundaries ---
# Starts at [Setting: Night club], ends at (Scene ends) or next [Setting:]
start = None
end = None
for i, line in enumerate(lines):
    if re.search(r"\[Setting:\s*Night\s*club\]", line, re.IGNORECASE):
        start = i + 1
    elif start is not None and (
        re.search(r"\(Scene ends\)", line, re.IGNORECASE)
        or (re.search(r"\[Setting:", line) and i > start)
    ):
        end = i
        break

if start is None:
    raise RuntimeError("Could not find [Setting: Night club] in first 200 lines")
if end is None:
    end = len(lines)

# --- Extract and clean monologue text ---
raw_block = " ".join(lines[start:end])
# Remove speaker labels
raw_block = re.sub(r"JERRY:\s*", "", raw_block)
# Collapse whitespace
raw_block = re.sub(r"\s+", " ", raw_block).strip()

# Split into sentences/clauses for markup
# Split on sentence-ending punctuation, keeping the punctuation
clauses = re.split(r'(?<=[.!?"])\s+', raw_block)

# Group into premise blocks by looking for natural topic shifts
# For this monologue: men flipping / act-out / women / nest-hunt / kings / king act-out
premise_keywords = [
    "Women don't do this",
    "Because women",
    "before there was flipping",
    "I always wonder",
    "Just go",
]

output_lines = []
for clause in clauses:
    # Check if this clause starts a new premise
    for kw in premise_keywords:
        if kw in clause:
            output_lines.append("")  # blank line = premise break
            break
    output_lines.append(clause)

# --- Read annotation for laugh-points ---
with open(ANNOTATION_PATH, "r") as f:
    jokes = yaml.safe_load(f)

laugh_points = []
for i, joke in enumerate(jokes, 1):
    joke_id = joke.get("joke_id", f"joke_{i}")
    logic = joke.get("joke", {}).get("logic", {})
    setup = logic.get("setup_expectation", "")
    pivot = logic.get("pivot_mechanism", {})
    operation = pivot.get("operation", "unknown")
    template = joke.get("joke", {}).get("structure", {}).get("primary_template", "")
    act_out = joke.get("joke", {}).get("structure", {}).get("act_out", {})
    has_act_out = act_out.get("present", False) if act_out else False

    # Get a short text anchor from the punchline_violation
    pv = logic.get("punchline_violation", "")
    anchor = pv[:80] + "..." if len(pv) > 80 else pv

    label = f"{i}. [{operation}] [{template}]"
    if has_act_out:
        label += " [act-out]"
    label += f" — {anchor}"
    laugh_points.append(label)

# --- Write markup sheet ---
with open(OUTPUT_PATH, "w") as f:
    f.write("# S02E10 — \"The Baby Shower\" — Men vs Women Channel Flipping + Ancient Kings\n\n")
    for line in output_lines:
        f.write(line + "\n")
    f.write("\n---\n\n")
    f.write("## Agent laugh-points (from annotation, for comparison)\n\n")
    for lp in laugh_points:
        f.write(lp + "\n")
    f.write("")

print(f"Written to {OUTPUT_PATH}")
