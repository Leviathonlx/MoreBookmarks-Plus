# Second
# Script to update province id's in province file from definitions file
# Specifically looks for --> in the defintions file so remove those after it's complete
import re
import os

# Configuration - Make sure these filenames match your files exactly
DEFINITION_FILE = 'definition.txt'
HISTORY_FILE = 'k_goryeo.txt'
OUTPUT_HISTORY = 'k_goryeo_updated.txt'

def update_history_ids():
    id_map = {}
    
    # 1. Parse definition.txt for the mapping
    # This regex looks for the [OldID] --> [NewID] pattern inside your comments
    mapping_pattern = re.compile(r'(\d+)\s*-->\s*(\d+)')
    
    print("Building ID mapping from definition.txt...")
    if not os.path.exists(DEFINITION_FILE):
        print(f"Error: {DEFINITION_FILE} not found!")
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

    print(f"Loaded {len(id_map)} ID mappings.")

    # 2. Process k_goryeo.txt
    # This matches lines like "9858 = {" or "9858={" at the start of a line
    block_pattern = re.compile(r'^(\d+)\s*=')
    
    updated_lines = []
    found_count = 0
    missing_count = 0

    print(f"Updating {HISTORY_FILE}...")
    if not os.path.exists(HISTORY_FILE):
        print(f"Error: {HISTORY_FILE} not found!")
        return

    with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            # We strip leading whitespace to find the ID
            match = block_pattern.match(line.strip())
            
            if match:
                old_id = match.group(1)
                
                if old_id in id_map:
                    new_id = id_map[old_id]
                    # Replace only the specific ID at the start of the line
                    new_line = line.replace(old_id, new_id, 1)
                    updated_lines.append(new_line)
                    found_count += 1
                else:
                    # Append a comment to help you find IDs that weren't in the definition list
                    updated_lines.append(line.rstrip() + " # WARNING: ID NOT IN TRANSFER LIST\n")
                    missing_count += 1
            else:
                updated_lines.append(line)

    # 3. Write the output
    with open(OUTPUT_HISTORY, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print("\nProcessing Complete:")
    print(f"- Successfully transferred: {found_count} provinces")
    print(f"- Flagged as missing: {missing_count} provinces")
    print(f"- Results saved to: {OUTPUT_HISTORY}")

if __name__ == "__main__":
    update_history_ids()