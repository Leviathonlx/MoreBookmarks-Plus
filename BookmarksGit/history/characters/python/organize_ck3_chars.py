import re
import argparse
from collections import defaultdict
import sys

def parse_character_data(file_content):
    """
    Parses the raw file content to extract individual character blocks using a
    brace-counting method to ensure blocks are correctly bounded.

    Args:
        file_content (str): The full string content of the character file.

    Returns:
        list: A list of dictionaries, each representing a character with their
              id, raw text block, birth_date, dynasty, and culture.
    """
    # Remove standalone comments first
    content = re.sub(r'^\s*#.*$', '', file_content, flags=re.MULTILINE)
    
    characters = []
    # *** FIX ***: Added a period '.' to the character set in the regex to find IDs with periods.
    char_start_pattern = re.compile(r'^\s*([a-zA-Z0-9_.]+)\s*=\s*\{', re.MULTILINE)
    
    cursor = 0
    while cursor < len(content):
        match = char_start_pattern.search(content, cursor)
        if not match:
            break
        
        char_id = match.group(1)
        block_start_pos = match.start()
        
        brace_level = 0
        scan_pos = block_start_pos
        
        # More robust brace counting from the start of the block
        while scan_pos < len(content):
            char = content[scan_pos]
            if char == '{':
                brace_level += 1
            elif char == '}':
                if brace_level > 0: # only decrement if we are inside a block
                    brace_level -= 1
            if brace_level == 0 and match.end() < scan_pos: # ensure we have a full block
                break
            scan_pos += 1
        
        block_end_pos = scan_pos + 1
        block_text = content[block_start_pos:block_end_pos].strip()

        # Extract vital info from the correctly-bounded block
        birth_block_match = re.search(r'^\s*(\d{1,4}\.\d{1,2}\.\d{1,2})\s*=\s*\{(?:.|\n)*?birth\s*=', block_text, re.MULTILINE)
        dynasty_match = re.search(r'^\s*(?:dynasty|dynasty_house)\s*=\s*(\w+)', block_text, re.MULTILINE)
        culture_match = re.search(r'^\s*culture\s*=\s*"?(\w+)"?', block_text, re.MULTILINE)

        birth_date = birth_block_match.group(1) if birth_block_match else "9999.1.1"
        dynasty = dynasty_match.group(1) if dynasty_match else "no_dynasty"
        culture = culture_match.group(1) if culture_match else "no_culture"

        characters.append({
            "id": char_id,
            "text": block_text,
            "birth_date": tuple(map(int, birth_date.split('.'))),
            "dynasty": dynasty,
            "culture": culture
        })
        
        cursor = block_end_pos

    return characters

def format_character_block(block_text):
    """
    Cleans and reformats a single character block with consistent indentation
    and fixes old date formats. This version correctly handles inline comments
    on the block's first line.

    Args:
        block_text (str): The raw text of one character block.

    Returns:
        str: The fully cleaned and formatted character block.
    """
    reformatted_text = re.sub(r'death\s*=\s*"\d{1,4}\.\d{1,2}\.\d{1,2}"', 'death = yes', block_text)

    final_lines = []
    indent_level = 0
    
    for line in reformatted_text.split('\n'):
        line = line.strip()
        if not line:
            continue

        if line.startswith('}'):
            indent_level = max(0, indent_level - 1)
        
        parts = line.split('#', 1)
        code = parts[0].strip()
        comment = f" #{parts[1].strip()}" if len(parts) > 1 else ""

        final_lines.append('\t' * indent_level + code + comment)
        
        if code.endswith('{'):
            indent_level += 1
            
    return "\n".join(final_lines)

def main(input_file, output_file):
    """
    Main function to read, process, and write the character file with improved
    output logic for dynonyless characters.
    """
    try:
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_file}'")
        sys.exit(1)

    print("Parsing character data...")
    characters = parse_character_data(content)
    
    if not characters:
        print("No character data found in the file. Exiting.")
        return

    print("Determining dynasty cultures...")
    dynasty_cultures = {}
    sorted_by_birth = sorted(characters, key=lambda c: c['birth_date'])
    for char in sorted_by_birth:
        if char['dynasty'] != "no_dynasty" and char['dynasty'] not in dynasty_cultures:
            dynasty_cultures[char['dynasty']] = char['culture']

    print("Grouping characters by culture and dynasty...")
    organized_data = defaultdict(lambda: defaultdict(list))
    for char in characters:
        dynasty = char['dynasty']
        culture = dynasty_cultures.get(dynasty, char['culture'])
        organized_data[culture][dynasty].append(char)

    print("Sorting and writing final data...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Character file organized by script\n\n")
        
        sorted_cultures = sorted(organized_data.keys())
        for culture in sorted_cultures:
            f.write(f"#==================================================================================================#\n")
            f.write(f"################################################## CULTURE: {culture.upper()}\n")
            f.write(f"#==================================================================================================#\n\n")
            
            culture_dynasties = organized_data[culture]
            
            no_dynasty_chars = culture_dynasties.pop('no_dynasty', [])
            no_dynasty_chars.sort(key=lambda c: c['birth_date'])

            sorted_dynasties = sorted(culture_dynasties.keys())
            for dynasty in sorted_dynasties:
                f.write(f"####################################### Dynasty: {dynasty} #######################################\n")
                culture_dynasties[dynasty].sort(key=lambda c: c['birth_date'])
                for char in culture_dynasties[dynasty]:
                    formatted_block = format_character_block(char['text'])
                    f.write(formatted_block + '\n\n')

            if no_dynasty_chars:
                f.write(f"################################################# No Dynasty #################################################\n")
                for char in no_dynasty_chars:
                    formatted_block = format_character_block(char['text'])
                    f.write(formatted_block + '\n\n')
    
    print("Done!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Organize Crusader Kings 3 character files by culture and dynasty.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("input_file", help="Path to the input character file.")
    parser.add_argument("output_file", help="Path for the new, organized output file.")

    args = parser.parse_args()
    main(args.input_file, args.output_file)