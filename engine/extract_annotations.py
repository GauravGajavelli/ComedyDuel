"""
Extract YAML annotation blocks from agent output files and write them
to annotations/ directory.

Agent output files are JSON-lines conversation logs. The YAML blocks
are embedded in assistant messages between ```yaml and ``` fences.
"""

import json
import re
import os

TASKS_DIR = "/private/tmp/claude-501/-Users-gauravgajavelli-Documents-GitHub-ComedyDuel/0f08dd8b-c04e-461c-95e2-8bf54e0e7b23/tasks"
OUT_DIR = "/Users/gauravgajavelli/Documents/GitHub/ComedyDuel/annotations"

# Map agent IDs to episode info (from the conversation)
AGENT_MAP = {
    # Pilot batch (episodes 1-5) - first round
    "a79beabc83c219aee": ("s01e01", "Good News Bad News"),      # already on disk
    "adf9edf37929f41f7": ("s01e02", "The Stakeout"),
    "add8794e9d40d8356": ("s01e03", "The Robbery"),
    "a568b314d89c7884a": ("s01e04", "Male Unbonding"),
    "ac1898c0f03554a86": ("s01e05", "The Stock Tip"),
    # Sub-batch A (episodes 6-10)
    "aa0c3be1d84aed000": ("s01e06", "The Ex-Girlfriend"),
    "ae2c30c6a501de056": ("s01e07", "The Pony Remark"),         # already on disk
    "a41e4de309bd502f1": ("s01e08", "The Jacket"),
    "a45cc7fa9cd136a2f": ("s01e09", "The Phone Message"),
    "a65e3d8e13fb887d0": ("s01e10", "The Apartment"),           # already on disk
    # Sub-batch B (episodes 11-15)
    "a8c9288d045d0adf5": ("s02e02", "The Statue"),              # already on disk
    "a0d777df04edad0bf": ("s02e04", "The Heart Attack"),
    "a388a8a7c6a5e1343": ("s02e05", "The Deal"),
    "a96dccd729644fef1": ("s02e06", "The Baby Shower"),         # already on disk
}

# Episodes already on disk
ALREADY_ON_DISK = {"s01e01", "s01e07", "s02e02", "s01e10", "s02e06"}

def extract_yaml_from_output(filepath):
    """Extract YAML blocks from agent output file."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except:
        return None

    # Agent outputs are newline-delimited JSON
    yaml_blocks = []
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Look for assistant messages with YAML content
        if obj.get('type') != 'assistant':
            continue

        msg = obj.get('message', {})
        content_parts = msg.get('content', [])
        if isinstance(content_parts, str):
            text = content_parts
        elif isinstance(content_parts, list):
            text = ' '.join(
                p.get('text', '') for p in content_parts
                if isinstance(p, dict) and p.get('type') == 'text'
            )
        else:
            continue

        # Extract ```yaml ... ``` blocks
        pattern = r'```yaml\s*\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        yaml_blocks.extend(matches)

    # Return the longest YAML block (the main annotation)
    if yaml_blocks:
        return max(yaml_blocks, key=len)
    return None


os.makedirs(OUT_DIR, exist_ok=True)
extracted = 0
skipped = 0
failed = 0

for agent_id, (ep_id, title) in AGENT_MAP.items():
    if ep_id in ALREADY_ON_DISK:
        print(f"  SKIP {ep_id} ({title}) — already on disk")
        skipped += 1
        continue

    filepath = os.path.join(TASKS_DIR, f"{agent_id}.output")
    if not os.path.exists(filepath):
        print(f"  MISS {ep_id} ({title}) — output file not found")
        failed += 1
        continue

    yaml_content = extract_yaml_from_output(filepath)
    if yaml_content:
        outpath = os.path.join(OUT_DIR, f"{ep_id}_pass2_decomposition.yaml")
        with open(outpath, 'w') as f:
            f.write(yaml_content)
        print(f"  OK   {ep_id} ({title}) -> {outpath} ({len(yaml_content)} chars)")
        extracted += 1
    else:
        print(f"  FAIL {ep_id} ({title}) — no YAML block found in output")
        failed += 1

print(f"\nDone: {extracted} extracted, {skipped} skipped (on disk), {failed} failed")
