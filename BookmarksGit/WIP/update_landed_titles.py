import re
import os

# Configuration
DEFINITION_FILE = 'definition.txt'
TITLES_FILE = 'k_luzhen.txt'
OUTPUT_TITLES = 'k_luzhen_updated.txt'

def update_landed_titles():
    id_map = {}
    
    # 1. Build the mapping from definition.txt
    # This matches the pattern inside your comments: 9863 --> 14204
    mapping_pattern = re.compile(r'(\d+)\s*-->\s*(\d+)')
    
    print("Reading ID mappings from definition.txt...")
    if not os.path.exists(DEFINITION_FILE):
        print(f"Error: {DEFINITION_FILE} not found.")
        return

    with open(DEFINITION_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if "-->" in line:
                match = mapping_pattern.search(line)
                if match:
                    old_id = match.group(1)
                    new_id = match.group(2)
                    id_map[old_id] = new_id

    if not id_map:
        print("No mappings found with '-->' in definition.txt.")
        return
    
    print(f"Loaded {len(id_map)} mappings.")

    # 2. Process 05_goryeo.txt
    # Group 1: 'province = ' (preserves spacing/indentation)
    # Group 2: the ID number
    province_line_pattern = re.compile(r'(province\s*=\s*)(\d+)')
    
    updated_lines = []
    change_count = 0
    warning_count = 0

    print(f"Processing {TITLES_FILE}...")
    if not os.path.exists(TITLES_FILE):
        print(f"Error: {TITLES_FILE} not found.")
        return

    # Using utf-8-sig to handle the potential Byte Order Mark (BOM)
    with open(TITLES_FILE, 'r', encoding='utf-8-sig') as f:
        for line in f:
            match = province_line_pattern.search(line)
            
            if match:
                old_id = match.group(2)
                
                if old_id in id_map:
                    new_id = id_map[old_id]
                    # FIX: Using \g<1> prevents the ID from being read as an octal character code
                    new_line = province_line_pattern.sub(rf"\g<1>{new_id}", line)
                    updated_lines.append(new_line)
                    change_count += 1
                else:
                    # ID not found in the transfer list, add a warning
                    updated_lines.append(line.rstrip() + " # WARNING: ID NOT IN TRANSFER LIST\n")
                    warning_count += 1
            else:
                updated_lines.append(line)

    # 3. Write output
    with open(OUTPUT_TITLES, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print("\nLanded Titles Update Complete:")
    print(f"- Provinces updated to new IDs: {change_count}")
    print(f"- Provinces flagged with warnings: {warning_count}")
    print(f"- Saved result to: {OUTPUT_TITLES}")

if __name__ == "__main__":
    update_landed_titles()