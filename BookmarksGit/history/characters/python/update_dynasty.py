import re
from collections import defaultdict

### --- CONFIGURATION --- ###
# --- Fill in your details for the Yorinobu -> Kawachi branch ---

# ID of the character who will be the progenitor of the new house.
PROGENITOR_ID = '10120013'

# The property KEY and VALUE you want to find and replace.
ORIGINAL_PROPERTY_KEY = 'dynasty'
ORIGINAL_PROPERTY_VALUE = 'japanese_minamoto_seiwa'

# The new property KEY and VALUE you want to write.
NEW_PROPERTY_KEY = 'dynasty_house'
NEW_PROPERTY_VALUE = 'house_minamoto_kawachi'

# The name of your source file.
INPUT_FILENAME = '00_JAPAN_1.txt' # Using the file you provided

# The name of the new file that will be created with the changes.
OUTPUT_FILENAME = 'Output.txt'
### ----------------------- ###


def update_dynasty_for_descendants():
    """
    Parses a character file line-by-line to change a dynasty property for a
    specific character and all of their descendants. This version uses a robust
    state-tracking method that is immune to previous parsing failures.
    """
    
    # --- Step 1: Build Family Tree ---
    parent_child_map = defaultdict(list)
    try:
        # Use 'utf-8-sig' to automatically handle and skip the BOM character
        with open(INPUT_FILENAME, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{INPUT_FILENAME}' was not found.")
        return

    # This regex is flexible and handles spacing around the '='
    character_blocks_finder = re.finditer(r'(\d+)\s*=\s*\{(.*?)\}', content, re.DOTALL)
    for block in character_blocks_finder:
        char_id, char_data = block.groups()
        father_match = re.search(r'father=(\d+)', char_data)
        if father_match:
            parent_child_map[father_match.group(1)].append(char_id)

    # --- Step 2: Identify All Descendants ---
    ids_to_modify = {PROGENITOR_ID}
    queue = [PROGENITOR_ID]
    head = 0
    while head < len(queue):
        current_id = queue[head]; head += 1
        if current_id in parent_child_map:
            for child_id in parent_child_map[current_id]:
                if child_id not in ids_to_modify:
                    ids_to_modify.add(child_id)
                    queue.append(child_id)

    print(f"Progenitor ID: {PROGENITOR_ID}")
    print(f"Found {len(ids_to_modify) - 1} descendant(s). Total characters to modify: {len(ids_to_modify)}.")
    print(f"Changing '{ORIGINAL_PROPERTY_KEY} = {ORIGINAL_PROPERTY_VALUE}' to '{NEW_PROPERTY_KEY} = {NEW_PROPERTY_VALUE}'.")

    # --- Step 3: Process File Line by Line and Write Changes ---
    lines_changed = 0
    with open(INPUT_FILENAME, 'r', encoding='utf-8-sig') as f_in, open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f_out:
        current_char_id = None
        
        # This regex correctly finds the start of a character block, allowing spaces around '='
        char_id_finder = re.compile(r'^\s*(\d+)\s*=\s*\{')
        
        for line in f_in:
            # Check if this line starts a new character block
            char_id_match = char_id_finder.match(line)
            if char_id_match:
                current_char_id = char_id_match.group(1)

            line_was_changed = False
            # Only attempt to change lines if we are inside a character we care about
            if current_char_id in ids_to_modify and '=' in line:
                try:
                    # Safely parse the line
                    indentation = line[:len(line) - len(line.lstrip())]
                    comment_part = ''
                    code_part = line
                    if '#' in line:
                        code_part, comment_part = line.split('#', 1)
                        comment_part = '#' + comment_part
                    
                    key, value = code_part.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Check if the parsed key and value match our target
                    if key == ORIGINAL_PROPERTY_KEY and value == ORIGINAL_PROPERTY_VALUE:
                        new_line = f"{indentation}{NEW_PROPERTY_KEY} = {NEW_PROPERTY_VALUE}{comment_part.rstrip()}\n"
                        f_out.write(new_line)
                        line_was_changed = True
                        lines_changed += 1
                except ValueError:
                    # Ignore lines with '=' that aren't simple key-value pairs
                    pass

            if not line_was_changed:
                f_out.write(line)

    print(f"\nProcessing complete!")
    print(f"Successfully changed {lines_changed} line(s).")
    print(f"The modified file has been saved as '{OUTPUT_FILENAME}'.")

# --- Run the script ---
if __name__ == "__main__":
    update_dynasty_for_descendants()