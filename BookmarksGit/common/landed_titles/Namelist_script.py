import re
import os

# ================= CONFIGURATION =================
# The namelist you want to copy FROM
SOURCE_NAMELIST = "name_list_persian_turkish"

# The namelist you want to CREATE
TARGET_NAMELIST = "name_list_persian_turkish_anatolian"

# The file to process (you can use a single file or a folder)
# Change this to the path of your landed_titles file
INPUT_FILE = "00_landed_titles.txt" 
# =================================================

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    new_lines = []
    changes_made = 0

    # Regex explanation:
    # ^(\s+)        -> Captures leading indentation
    # {SOURCE}      -> The source namelist key
    # \s*=\s*       -> The equals sign with optional spaces
    # ([a-zA-Z0-9_]+) -> The value (the actual name key like cn_kangal)
    pattern = re.compile(rf'^(\s+){SOURCE_NAMELIST}(\s*=\s*)([a-zA-Z0-9_]+)')

    # We also check if the target already exists to avoid duplicates
    check_pattern = re.compile(rf'^\s+{TARGET_NAMELIST}\s*=')

    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        match = pattern.search(line)
        if match:
            indent = match.group(1)
            equals = match.group(2)
            value = match.group(3)
            
            # Look ahead to see if target already exists to prevent doubling up
            exists = False
            if i + 1 < len(lines):
                if check_pattern.search(lines[i+1]):
                    exists = True
            
            if not exists:
                # Construct the new line using the same indentation and value
                new_entry = f"{indent}{TARGET_NAMELIST}{equals}{value}\n"
                new_lines.append(new_entry)
                changes_made += 1
        
        i += 1

    if changes_made > 0:
        with open(file_path, 'w', encoding='utf-8-sig') as f:
            f.writelines(new_lines)
        print(f"Success: {file_path} updated with {changes_made} new entries.")
    else:
        print(f"No changes needed for {file_path}.")

if __name__ == "__main__":
    if os.path.exists(INPUT_FILE):
        process_file(INPUT_FILE)
    else:
        print(f"Error: Could not find file '{INPUT_FILE}'")