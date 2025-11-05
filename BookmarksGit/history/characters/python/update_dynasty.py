import re
from collections import defaultdict

### --- CONFIGURATION --- ###
# ID of the character who will be the progenitor of the new dynasty house.
PROGENITOR_ID = '11004557'

# The new name for the dynasty_house.
NEW_DYNASTY_HOUSE = 'house_fujiwara_yamakage'

# The original dynasty_house name that you are replacing.
ORIGINAL_DYNASTY_HOUSE = 'house_fujiwara_uona'

# The name of your source file.
INPUT_FILENAME = 'Japan.txt'

# The name of the new file that will be created with the changes.
OUTPUT_FILENAME = 'Japan_modified.txt'
### ----------------------- ###


def update_dynasty_for_descendants():
    """
    Parses a character file to change the dynasty_house for a specific character
    and all of his descendants based on the settings in the CONFIGURATION block.
    """
    # This regex is now built dynamically from your configuration
    target_line_regex = re.compile(rf'(\s*dynasty_house\s*=\s*){ORIGINAL_DYNASTY_HOUSE}(.*)')

    # --- Step 1: Parse the file to build a family tree ---
    parent_child_map = defaultdict(list)
    try:
        with open(INPUT_FILENAME, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: The file '{INPUT_FILENAME}' was not found.")
        print("Please make sure the script is in the same directory as your text file.")
        return

    # Regex to find all character blocks
    character_blocks = re.finditer(r'(\d+)=\{(.*?)\}', content, re.DOTALL)

    for block in character_blocks:
        char_id = block.group(1)
        char_data = block.group(2)
        
        # Find the father's ID within the character data
        father_match = re.search(r'father=(\d+)', char_data)
        if father_match:
            father_id = father_match.group(1)
            parent_child_map[father_id].append(char_id)

    # --- Step 2: Find all descendants of the progenitor ---
    ids_to_modify = {PROGENITOR_ID}
    queue = [PROGENITOR_ID]
    
    head = 0
    while head < len(queue):
        current_id = queue[head]
        head += 1
        
        if current_id in parent_child_map:
            children = parent_child_map[current_id]
            for child_id in children:
                if child_id not in ids_to_modify:
                    ids_to_modify.add(child_id)
                    queue.append(child_id)

    print(f"Progenitor ID: {PROGENITOR_ID}")
    print(f"Found {len(ids_to_modify) - 1} descendant(s).")
    print(f"Total characters to modify: {len(ids_to_modify)}.")
    print(f"Changing '{ORIGINAL_DYNASTY_HOUSE}' to '{NEW_DYNASTY_HOUSE}'.")


    # --- Step 3: Read the file again and write the changes ---
    with open(INPUT_FILENAME, 'r', encoding='utf-8') as f_in, open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f_out:
        current_char_id = None
        for line in f_in:
            # Check if the line marks the beginning of a new character block
            char_id_match = re.match(r'^\s*(\d+)=\s*\{', line)
            if char_id_match:
                current_char_id = char_id_match.group(1)

            # Check if the current character is one we need to modify
            if current_char_id in ids_to_modify:
                match = target_line_regex.match(line)
                if match:
                    # If it's the dynasty line, replace it
                    indentation = match.group(1)
                    comment = match.group(2) # Preserves any existing comments on the line
                    f_out.write(f"{indentation}{NEW_DYNASTY_HOUSE}{comment}\n")
                    continue
            
            # If no changes are needed, write the original line
            f_out.write(line)

    print(f"\nProcessing complete!")
    print(f"The modified file has been saved as '{OUTPUT_FILENAME}'.")

# --- Run the script ---
if __name__ == "__main__":
    update_dynasty_for_descendants()