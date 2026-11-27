"""
extract_descendants.py

Extracts a character and all their male-line descendants from a Paradox (CK3/CK2)
character history file. Edit the three variables below, then run:

    python extract_descendants.py

Daughters are included but their children are not followed.
"""

import re
import sys

# ── Configuration ─────────────────────────────────────────────────────────────

INPUT_FILE  = "00_JAPAN_1.txt"
OUTPUT_FILE = "ExtractedCharacters.txt"
ROOT_ID     = "japanese_yamato_163"

# ──────────────────────────────────────────────────────────────────────────────


def parse_file(filepath):
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    blocks = re.split(r'\n(?=\w+\s*=\s*\{)', content)

    characters = {}
    fathers = {}
    is_female = {}

    char_id_pattern = re.compile(r'^(\w+)\s*=\s*\{')

    for block in blocks:
        m = char_id_pattern.match(block.strip())
        if not m:
            continue
        cid = m.group(1)
        characters[cid] = block.strip()

        father = re.search(r'^\s*father\s*=\s*(\S+)', block, re.MULTILINE)
        fathers[cid] = father.group(1) if father else None
        is_female[cid] = bool(re.search(r'^\s*female\s*=\s*yes', block, re.MULTILINE))

    children = {}
    for cid, father_id in fathers.items():
        if father_id:
            children.setdefault(father_id, []).append(cid)

    return characters, children, is_female


def get_descendants(root, characters, children, is_female):
    if root not in characters:
        return None

    visited = set()
    queue = [root]
    order = []

    while queue:
        node = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        if not is_female.get(node, False):
            for child in children.get(node, []):
                queue.append(child)

    return order


def get_name(block):
    m = re.search(r'name\s*=\s*"([^"]+)"', block)
    return m.group(1) if m else '?'


def main():
    print(f"Parsing {INPUT_FILE}...")
    try:
        characters, children, is_female = parse_file(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: '{INPUT_FILE}' not found.")
        sys.exit(1)

    print(f"  Loaded {len(characters)} characters.")

    if ROOT_ID not in characters:
        print(f"Error: '{ROOT_ID}' not found in file.")
        sys.exit(1)

    order = get_descendants(ROOT_ID, characters, children, is_female)
    print(f"  Found {len(order)} characters (including root).\n")

    for cid in order:
        block = characters.get(cid, '')
        name = get_name(block)
        female_tag = ' [F]' if is_female.get(cid) else ''
        print(f"  {cid}{female_tag} - {name}")

    result = '\n\n'.join(characters[cid] for cid in order if cid in characters)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"\nWritten to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()