#!/usr/bin/env python3
"""
CK3 Missing Localization Fixer
- Special characters in keys become underscores (Maymún -> Maym_un)
- All keys get a '_MB' suffix (Maym_un_MB).
- Display values preserve accents and capitalization (Maym_un_MB -> "Maymún").
- Detailed console output showing every replacement made.
"""

import argparse
import os
import re
import shutil
import sys
from collections import defaultdict, OrderedDict

# List of character history files to process
CHAR_FILE_NAMES = [
    "00_AFRICA", "00_ASIA_INDOSPHERE", "00_ASIA_JAPAN", "00_ASIA_MIDDLE_EAST",
    "00_ASIA_MONGOLIC", "00_ASIA_NORTHEAST", "00_ASIA_SINOSPHERE", "00_ASIA_TURKIC",
    "00_EUROPE_BALTOSCANDIA", "00_EUROPE_BRITISH_ISLES", "00_EUROPE_EAST",
    "00_EUROPE_ERE", "00_EUROPE_FRANCE", "00_EUROPE_GERMANY", "00_EUROPE_IBERIA",
    "00_EUROPE_ITALY", "00_MB_Asia", "00_Z_UNLANDED",
]

_NAME_SUFFIX_RE = re.compile(r'_name\d*$')

def try_decode_mojibake(s: str) -> str:
    """Fixes UTF-8 characters misread as latin-1."""
    for enc in ('latin-1', 'cp1252'):
        try:
            return s.encode(enc).decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
    return s

def _transliterate_to_underscore(s: str) -> str:
    """Replaces any non-ASCII character with an underscore for the key."""
    out = []
    for ch in s:
        if ord(ch) <= 127:
            out.append(ch)
        else:
            out.append('_')
    return ''.join(out)

def get_display_name(raw: str) -> str:
    """Prepares the human-readable string for the .yml file."""
    s = raw.strip()
    s = _NAME_SUFFIX_RE.sub('', s)
    s = try_decode_mojibake(s)
    s = s.strip()
    if len(s) > 0:
        s = s[0].upper() + s[1:]
    return s

def make_loc_key(raw: str) -> str:
    """Creates the key with underscores and _MB suffix."""
    s = get_display_name(raw)
    s = _transliterate_to_underscore(s)
    s = s.replace(' ', '_')
    s = re.sub(r"['\u2018\u2019\u02bc\u2032`\-\.\(\),;:!?/\\]", '_', s)
    s = re.sub(r'[^\w]', '_', s, flags=re.ASCII)
    s = re.sub(r'_+', '_', s).strip('_')
    return f"{s}_MB" if s else ""

def parse_error_log(path: str) -> list:
    entries, seen = [], set()
    try:
        with open(path, encoding='utf-8', errors='replace') as fh:
            for line in fh:
                m = re.search(r"Missing loc for name '(.+?)' for character '(.+?)'", line)
                if m:
                    pair = (m.group(1), m.group(2))
                    if pair not in seen:
                        seen.add(pair)
                        entries.append(pair)
    except FileNotFoundError:
        sys.exit(f"ERROR: file not found: {path}")
    return entries

def _make_name_regex(search_value: str) -> re.Pattern:
    esc = re.escape(search_value.strip())
    pattern = r'(\bname[ \t]*=[ \t]*)"?[ \t]*' + esc + r'[ \t]*"?(?=[ \t\r\n#]|$)'
    return re.compile(pattern)

def patch_file(filepath: str, replacements: dict, dry_run: bool, backup: bool) -> dict:
    try:
        with open(filepath, encoding='utf-8', errors='replace') as fh:
            original = fh.read()
    except FileNotFoundError:
        return {}

    content = original
    counts = defaultdict(int)
    for search_val in sorted(replacements, key=len, reverse=True):
        loc_key = replacements[search_val]
        pat = _make_name_regex(search_val)
        
        def _sub(m, k=loc_key):
            return f'{m.group(1)}"{k}"'

        new_content, n = pat.subn(_sub, content)
        if n:
            counts[search_val] += n
            content = new_content

    if content != original and not dry_run:
        if backup:
            shutil.copy2(filepath, filepath + '.bak')
        with open(filepath, 'w', encoding='utf-8', newline='') as fh:
            fh.write(content)
    return dict(counts)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--error-log', required=True)
    ap.add_argument('--char-dir', required=True)
    ap.add_argument('--output-loc', required=True)
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--backup', action='store_true')
    args = ap.parse_args()

    print(f"Reading error log: {args.error_log}")
    entries = parse_error_log(args.error_log)
    if not entries:
        print("Nothing to do.")
        return

    name_table = OrderedDict()
    for raw_name, _ in entries:
        if raw_name not in name_table:
            display = get_display_name(raw_name)
            key = make_loc_key(raw_name)
            search = try_decode_mojibake(raw_name.strip())
            if key:
                name_table[raw_name] = (display, key, search)

    # Replacement map for files
    replacements = {}
    for raw_name, (disp, key, search) in name_table.items():
        replacements[search] = key
        if raw_name.strip() not in replacements:
            replacements[raw_name.strip()] = key

    # Scanning Files
    mode_label = "[DRY RUN] Would patch" if args.dry_run else "Patching"
    print(f"\n{mode_label} character files...")
    
    total_changes = 0
    changed_values = defaultdict(int)

    for b in CHAR_FILE_NAMES:
        path = os.path.join(args.char_dir, b + ".txt")
        if not os.path.isfile(path): continue
        
        counts = patch_file(path, replacements, args.dry_run, args.backup)
        if counts:
            print(f"  {b}.txt:")
            for found_val, n in sorted(counts.items()):
                key = replacements.get(found_val, '?')
                print(f"    '{found_val}'  ->  '{key}'  ({n} replacements)")
                changed_values[found_val] += n
                total_changes += n

    # Summary and Loc Write
    print(f"\nTotal replacements made: {total_changes}")

    if not args.dry_run:
        loc_entries = {key: disp for disp, key, search in name_table.values()}
        os.makedirs(os.path.dirname(os.path.abspath(args.output_loc)), exist_ok=True)
        with open(args.output_loc, 'w', encoding='utf-8-sig') as fh:
            fh.write('l_english:\n')
            for key in sorted(loc_entries):
                fh.write(f' {key}: "{loc_entries[key]}"\n')
        print(f"Localization file written: {args.output_loc}")

    # Final Check for names not found in files
    not_found = []
    for raw_name, (disp, key, search) in name_table.items():
        if search not in changed_values and raw_name.strip() not in changed_values:
            not_found.append((raw_name, disp, key))

    if not_found:
        print(f"\nNOTE: {len(not_found)} names from log were NOT found in character files:")
        for rn, disp, k in not_found:
            print(f"  Log: '{rn}' -> Key: '{k}'")

if __name__ == '__main__':
    main()