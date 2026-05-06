#!/usr/bin/env python3
"""Prepend a markup cheat sheet to all audit sheet files."""

import glob
import os

CHEAT_SHEET = """\
<!-- MARKUP CHEAT SHEET

PASS 1 — Laugh + Structure (1.5x speed, just listening)
  Insert after the line where a laugh occurs:

  Laugh size:    [big]  [medium]  [small]  [chuckle]
  If no laugh where agent predicted one:  [none]
  If laugh where agent missed:            [missed]

  Agent mismatch (only note when it DOESN'T match):
    [split]   — you hear two laughs where agent had one
    [merged]  — agent split this but it's one sustained laugh

  Structural event (optional, only if agent got it wrong):
    [premise]  [setup]  [punchline]  [tag]  [topper]  [act_out]  [connector]

PASS 2 — Physical Performance (normal speed, 5 priority episodes)
  Add in curly braces after notable moments:

  {physical_state — physical_change — load}

  physical_state:  what body is doing (free text)
    e.g. "standing center, relaxed" / "leaning on mic stand"

  physical_change: what changes at/near the laugh (free text)
    e.g. "freezes expression" / "shifts to character posture" /
    "scans audience" / "delayed blink" / "none"

  load:  supports | carries | independent
    supports    = reinforces text; joke works without it
    carries     = IS the comedy; text alone flat
    independent = funny on its own, separate from text
    (skip if physical_change is unremarkable)

  performance_mode:  direct | character | narrative | rhetorical | physical
    Use arrow for transitions: "direct -> character"

  energy:  low | medium | high
    Use arrow for shifts: "low -> high"

  Examples:
    Some punchline text here. [big]
    {center stage, still — freezes expression, slight head tilt — carries}
    {direct -> character, medium -> high}

    Setup text here.
    {conversational default}

-->

"""

files = sorted(glob.glob(
    os.path.join(os.path.dirname(__file__), "audit_sheets", "*_markup.md")
))

for fpath in files:
    with open(fpath, "r") as f:
        content = f.read()

    if "MARKUP CHEAT SHEET" in content:
        print(f"  SKIP (already has cheat sheet): {os.path.basename(fpath)}")
        continue

    with open(fpath, "w") as f:
        f.write(CHEAT_SHEET + content)

    print(f"  OK: {os.path.basename(fpath)}")

print(f"\nDone — {len(files)} files processed.")
