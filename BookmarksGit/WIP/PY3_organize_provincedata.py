import re
import os

# Configuration
HISTORY_FILE = 'k_goryeo_updated.txt'
PROVINCE_DATA_FILE = 'Provincedata.txt'
OUTPUT_FILE = 'k_goryeo_organized.txt'

def extract_existing_ids(filepath):
    """Returns a set of all province IDs currently defined in Provincedata."""
    ids = set()
    # Matches a number at the start of a line followed by an equals sign
    pattern = re.compile(r'^\s*(\d+)\s*=')
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                match = pattern.match(line)
                if match:
                    ids.add(match.group(1))
    return ids

def parse_history_blocks(filepath):
    """Parses the history file into a list of (id, full_text_block)."""
    blocks = []
    # Matches the start of a block like '12345 = {'
    id_start_pattern = re.compile(r'^(\d+)\s*=')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    current_id = None
    current_block = []
    brace_level = 0

    for line in lines:
        stripped = line.strip()
        match = id_start_pattern.match(stripped)

        # If we find a new province ID and we aren't currently inside another block
        if match and brace_level == 0:
            current_id = match.group(1)
            current_block = [line]
            brace_level += line.count('{') - line.count('}')
            # If the block is one line long (e.g., 123 = { holding = city }), close it
            if brace_level == 0 and current_id:
                blocks.append((current_id, "".join(current_block)))
                current_id = None
            continue

        if current_id:
            current_block.append(line)
            brace_level += line.count('{') - line.count('}')
            
            if brace_level <= 0:
                blocks.append((current_id, "".join(current_block)))
                current_id = None
                current_block = []
                brace_level = 0
    
    return blocks

def run_organizer():
    print("Reading existing IDs from Province Data...")
    existing_ids = extract_existing_ids(PROVINCE_DATA_FILE)
    
    print("Parsing blocks from Goryeo History...")
    all_blocks = parse_history_blocks(HISTORY_FILE)
    
    already_in_data = []
    new_to_data = []

    for prov_id, block_text in all_blocks:
        if prov_id in existing_ids:
            already_in_data.append(block_text)
        else:
            new_to_data.append(block_text)

    print(f"Organizing {len(all_blocks)} total provinces...")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("#provinces already in provincedata\n\n")
        f.writelines(already_in_data)
        
        f.write("\n\n#provinces new to provincedata\n\n")
        f.writelines(new_to_data)

    print(f"Done! Created: {OUTPUT_FILE}")
    print(f"- Already in data: {len(already_in_data)}")
    print(f"- New to data: {len(new_to_data)}")

if __name__ == "__main__":
    run_organizer()