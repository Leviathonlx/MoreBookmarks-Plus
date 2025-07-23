import re
from datetime import datetime
import sys

def parse_character_blocks(file_content):
    """
    Parses the raw text of a CK3 file to extract individual character blocks.
    A character block is identified by a pattern like 'id = { ... }'.
    This is designed to be robust against nested curly braces.
    """
    # Regex to find character blocks. It looks for an identifier, an equals sign,
    # and a block enclosed in curly braces.
    # It's non-greedy and handles any characters, including newlines.
    char_pattern = re.compile(r"^\s*([\w\d.-]+)\s*=\s*{(.*?)\n}\s*$", re.MULTILINE | re.DOTALL)
    
    matches = char_pattern.finditer(file_content)
    
    characters = []
    for match in matches:
        char_id = match.group(1).strip()
        # Reconstruct the full block for later processing
        full_text = f"{char_id} = {{\n{match.group(2).strip()}\n}}"
        characters.append(full_text)
        
    return characters

def get_character_details(char_block_text):
    """Extracts dynasty and birth date from a character block string."""
    dynasty = None
    birth_date = datetime.max # Use max date for characters without a birth date to sort them last

    # Prioritize dynasty_house, then dynasty
    dynasty_house_match = re.search(r"dynasty_house\s*=\s*(\w+)", char_block_text)
    if dynasty_house_match:
        dynasty = dynasty_house_match.group(1)
    else:
        dynasty_match = re.search(r"dynasty\s*=\s*(\w+)", char_block_text)
        if dynasty_match:
            dynasty = dynasty_match.group(1)

    if not dynasty:
        dynasty = "No Dynasty" # Group for characters without a specified dynasty

    # Find birth date (e.g., 830.1.2 = { birth = yes })
    birth_match = re.search(r"(\d{1,4}\.\d{1,2}\.\d{1,2})\s*=\s*{\s*birth\s*=", char_block_text)
    if birth_match:
        try:
            date_str = birth_match.group(1)
            birth_date = datetime.strptime(date_str, '%Y.%m.%d')
        except ValueError:
            # Handle cases where the date might be malformed, though unlikely with this data
            pass
            
    return dynasty, birth_date

def clean_and_format_block(char_block_text):
    """
    Cleans up and properly indents a single character block.
    - Standardizes birth/death entries.
    - Fixes all indentation.
    - Preserves inline comments.
    """
    # 1. Standardize birth/death entries (e.g., death = "1227.12.2" -> death = yes)
    # This regex finds 'birth =' or 'death =' followed by a quoted date and replaces it.
    char_block_text = re.sub(r'(birth\s*=\s*)"\d{1,4}\.\d{1,2}\.\d{1,2}"', r'\1yes', char_block_text)
    char_block_text = re.sub(r'(death\s*=\s*)"\d{1,4}\.\d{1,2}\.\d{1,2}"', r'\1yes', char_block_text)

    # 2. Re-indent the entire block
    formatted_lines = []
    indent_level = 0
    
    # Split while preserving inline comments
    lines = char_block_text.split('\n')
    
    for i, line in enumerate(lines):
        # Split line to separate code from comment
        parts = line.split('#', 1)
        code = parts[0].strip()
        comment = f" #{parts[1].strip()}" if len(parts) > 1 else ""

        if not code:
            continue

        # Adjust indentation level based on braces
        if '}' in code:
            indent_level = max(0, indent_level - code.count('}'))

        # Add the line with proper indentation
        if i == 0: # First line (ID = {) has no indent
            formatted_lines.append(code + comment)
        else:
            formatted_lines.append(('\t' * indent_level) + code + comment)

        if '{' in code:
            indent_level += code.count('{')
            
    return "\n".join(formatted_lines)

def main(input_filename="mongol.txt", output_filename="mongol_organized.txt"):
    """
    Main function to read, process, and write the character file.
    """
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        sys.exit(1)
        
    # First, remove all standalone comments from the original file content
    lines = content.split('\n')
    filtered_lines = [line for line in lines if not line.strip().startswith('#')]
    content_no_comments = "\n".join(filtered_lines)

    # Parse all character blocks from the cleaned content
    char_blocks = parse_character_blocks(content_no_comments)
    
    if not char_blocks:
        print("No character blocks found in the file. Exiting.")
        return

    # Group characters by dynasty
    dynasties = {}
    for block in char_blocks:
        dynasty, birth_date = get_character_details(block)
        if dynasty not in dynasties:
            dynasties[dynasty] = []
        dynasties[dynasty].append({'text': block, 'birth_date': birth_date})

    # Write the organized and formatted output
    with open(output_filename, 'w', encoding='utf-8') as f:
        # Sort dynasties alphabetically for consistent output order
        for dynasty_name in sorted(dynasties.keys()):
            f.write(f"#############################################\n# Dynasty: {dynasty_name}\n#############################################\n\n")
            
            # Sort characters within the dynasty by birth date
            sorted_chars = sorted(dynasties[dynasty_name], key=lambda x: x['birth_date'])
            
            for char_data in sorted_chars:
                formatted_block = clean_and_format_block(char_data['text'])
                f.write(formatted_block + "\n\n")
                
    print(f"Successfully organized {len(char_blocks)} characters into '{output_filename}'.")


if __name__ == "__main__":
    # You can run this script from your terminal.
    # It will use 'mongol.txt' as input and create 'mongol_organized.txt'.
    # Example: python organize_ck3_chars.py
    main()