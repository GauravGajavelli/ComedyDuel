"""
Merge act_out blocks into existing annotation YAML files.

Reads act_out data from a YAML file (agent output), matches by joke_id,
and injects the act_out block into each joke entry in the annotation files.

Usage:
    python3 engine/merge_act_out.py <act_out_data.yaml> <annotation_dir>

Or import and call merge_act_out_into_file() directly.
"""

import yaml
import os
import sys
import re


def load_act_out_data(yaml_text):
    """Parse act_out data from YAML text. Returns dict of joke_id -> act_out block."""
    data = yaml.safe_load(yaml_text)
    if not data:
        return {}
    result = {}
    for entry in data:
        jid = entry.get('joke_id')
        ao = entry.get('act_out', {})
        if jid:
            result[jid] = ao
    return result


def merge_act_out_into_file(annotation_path, act_out_map):
    """Add act_out blocks to jokes in an annotation file.

    Reads the annotation YAML, finds each joke by joke_id, adds act_out
    if not already present, writes back.

    Returns count of jokes updated.
    """
    with open(annotation_path, 'r') as f:
        content = f.read()

    data = yaml.safe_load(content)
    if not data:
        return 0

    # Find the jokes list - could be at top level or nested
    jokes = None
    if isinstance(data, dict):
        if 'jokes' in data:
            jokes = data['jokes']
        elif 'annotations' in data:
            jokes = data['annotations']
    elif isinstance(data, list):
        jokes = data

    if not jokes:
        return 0

    updated = 0
    for joke in jokes:
        jid = joke.get('joke_id')
        if jid and jid in act_out_map:
            joke['act_out'] = act_out_map[jid]
            updated += 1

    with open(annotation_path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True,
                  width=80, sort_keys=False)

    return updated


def extract_yaml_from_agent_output(filepath):
    """Extract the YAML block from an agent output file."""
    import json
    with open(filepath, 'r') as f:
        content = f.read()

    yaml_blocks = []
    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

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

        pattern = r'```yaml\s*\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        yaml_blocks.extend(matches)

    if yaml_blocks:
        return max(yaml_blocks, key=len)
    return None


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 engine/merge_act_out.py <agent_output_file> <annotation_dir>")
        print("  Extracts act_out YAML from agent output and merges into annotation files.")
        sys.exit(1)

    agent_file = sys.argv[1]
    annotation_dir = sys.argv[2]

    print(f"Extracting act_out data from {agent_file}...")
    yaml_text = extract_yaml_from_agent_output(agent_file)
    if not yaml_text:
        print("ERROR: No YAML block found in agent output")
        sys.exit(1)

    act_out_map = load_act_out_data(yaml_text)
    print(f"  Found {len(act_out_map)} act_out entries")

    total_updated = 0
    for fname in sorted(os.listdir(annotation_dir)):
        if not fname.endswith('.yaml'):
            continue
        fpath = os.path.join(annotation_dir, fname)
        count = merge_act_out_into_file(fpath, act_out_map)
        if count > 0:
            print(f"  {fname}: updated {count} jokes")
            total_updated += count

    print(f"\nDone: {total_updated} jokes updated across all files")
