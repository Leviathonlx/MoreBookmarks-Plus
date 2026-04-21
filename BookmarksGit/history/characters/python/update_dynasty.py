import re
from collections import defaultdict

### --- CONFIGURATION --- ###
PROGENITOR_ID = '1406899' # The founder character for the new dynasty
ORIGINAL_PROPERTY_VALUE = 'chen_9673_101' # The original dynasty of the character
NEW_PROPERTY_KEY = 'dynasty_house' # What key should be used dynasty or dynasty_house
NEW_PROPERTY_VALUE = 'house_nanchang_chen' # The new dynasty id
INPUT_FILENAME = '00_SINOSPHERE.txt' # The input file
OUTPUT_FILENAME = 'Output.txt' # The output file
### ----------------------- ###

def update_dynasty_for_descendants():
    parent_child_map = defaultdict(list)
    
    # Regex patterns
    # Matches "ID = {" at the start of a line
    char_start_re = re.compile(r'^([\w\d_.-]+)\s*=\s*\{')
    # Matches "father = ID" anywhere in a line
    father_re = re.compile(r'\bfather\s*=\s*([\w\d_.-]+)')

    # --- Step 1: Build Family Tree ---
    print(f"Scanning {INPUT_FILENAME} to build family tree...")
    try:
        with open(INPUT_FILENAME, 'r', encoding='utf-8-sig') as f:
            current_char_id = None
            for line in f:
                # Check if we entered a new character block
                start_match = char_start_re.match(line)
                if start_match:
                    current_char_id = start_match.group(1)
                    continue
                
                # Check for father definitions within a character block
                if current_char_id:
                    f_match = father_re.search(line)
                    if f_match:
                        father_id = f_match.group(1)
                        parent_child_map[father_id].append(current_char_id)
    except FileNotFoundError:
        print(f"Error: The file '{INPUT_FILENAME}' was not found.")
        return

    # --- Step 2: Identify All Descendants (BFS) ---
    ids_to_modify = {PROGENITOR_ID}
    queue = [PROGENITOR_ID]
    index = 0
    while index < len(queue):
        parent = queue[index]
        index += 1
        if parent in parent_child_map:
            for child in parent_child_map[parent]:
                if child not in ids_to_modify:
                    ids_to_modify.add(child)
                    queue.append(child)

    print(f"Progenitor ID: {PROGENITOR_ID}")
    print(f"Found {len(ids_to_modify) - 1} descendant(s). Total characters to modify: {len(ids_to_modify)}.")

    # --- Step 3: Process and Write Changes ---
    lines_changed = 0
    with open(INPUT_FILENAME, 'r', encoding='utf-8-sig') as f_in, \
         open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f_out:
        
        current_char_id = None
        for line in f_in:
            # Track which character block we are in
            start_match = char_start_re.match(line)
            if start_match:
                current_char_id = start_match.group(1)

            line_was_changed = False
            if current_char_id in ids_to_modify and '=' in line:
                # Logic to find 'dynasty' or 'dynasty_house'
                # Splits by # to handle comments safely
                parts = line.split('#', 1)
                code_part = parts[0]
                comment_part = f"#{parts[1]}" if len(parts) > 1 else ""

                if '=' in code_part:
                    key_val = code_part.split('=', 1)
                    key = key_val[0].strip()
                    val = key_val[1].strip()

                    if (key == 'dynasty' or key == 'dynasty_house') and val == ORIGINAL_PROPERTY_VALUE:
                        indent = line[:line.find(key)]
                        new_line = f"{indent}{NEW_PROPERTY_KEY} = {NEW_PROPERTY_VALUE} {comment_part}".rstrip() + "\n"
                        f_out.write(new_line)
                        line_was_changed = True
                        lines_changed += 1

            if not line_was_changed:
                f_out.write(line)

    print(f"\nProcessing complete!")
    print(f"Successfully changed {lines_changed} line(s).")
    print(f"The modified file has been saved as '{OUTPUT_FILENAME}'.")

if __name__ == "__main__":
    update_dynasty_for_descendants()