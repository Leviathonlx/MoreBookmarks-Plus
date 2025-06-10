import re
import os

def get_indentation(line):
    """Returns the leading whitespace of a line."""
    return re.match(r'^\s*', line).group(0)

def reorder_and_cleanup_barony_block(header, content_lines):
    """
    Parses the content of a barony block, removes blank lines,
    and reorders its elements.

    Args:
        header (str): The starting line of the block (e.g., "b_name = {").
        content_lines (list): A list of strings representing the block's content.

    Returns:
        str: The formatted and reordered block as a single string.
    """
    base_indent = get_indentation(header)
    content_indent = base_indent + '\t' # Assuming tabs for indentation

    province_line = None
    color_line = None
    cultural_names_block = []
    other_lines = []

    # State machine for parsing the cultural_names nested block
    in_cultural_names = False
    brace_count = 0
    
    # First pass: Extract the key elements
    i = 0
    while i < len(content_lines):
        line = content_lines[i]
        stripped_line = line.strip()

        if not stripped_line: # Skip blank lines
            i += 1
            continue

        if in_cultural_names:
            cultural_names_block.append(line)
            brace_count += line.count('{')
            brace_count -= line.count('}')
            if brace_count <= 0:
                in_cultural_names = False
        elif stripped_line.startswith('province ='):
            province_line = stripped_line
        elif stripped_line.startswith('color ='):
            color_line = stripped_line
        elif stripped_line.startswith('cultural_names = {'):
            in_cultural_names = True
            brace_count = line.count('{') - line.count('}')
            cultural_names_block.append(line)
            # If the block closes on the same line
            if brace_count <= 0:
                 in_cultural_names = False
        else:
            # Preserve any other lines that aren't the closing brace
            if stripped_line != '}':
                other_lines.append(line)
        i += 1

    # Second pass: Assemble the block in the desired order
    output_lines = [header]
    
    if province_line:
        output_lines.append(f"{content_indent}{province_line}\n")
    
    if color_line:
        output_lines.append(f"{content_indent}{color_line}\n")
        
    if cultural_names_block:
        # The cultural_names block should already have its original indentation
        output_lines.extend(cultural_names_block)
        
    if other_lines:
        # Add any other properties we found
        output_lines.extend(other_lines)

    output_lines.append(f"{base_indent}}}\n")
    
    return "".join(output_lines)


def process_landed_titles_file(input_filename="00_landed_titles.txt"):
    """
    Reads the landed titles file, identifies barony blocks, and passes them
    to a helper function for cleanup and reordering.
    """
    output_filename = input_filename.replace('.txt', '_reorganized.txt')
    barony_start_pattern = re.compile(r'^\s*b_\w+\s*=\s*{')

    print(f"Reading from '{input_filename}'...")
    
    try:
        with open(input_filename, 'r', encoding='utf-8-sig') as infile:
            lines = infile.readlines()

        with open(output_filename, 'w', encoding='utf-8') as outfile:
            in_barony_block = False
            brace_count = 0
            block_header = ""
            block_content = []

            for line in lines:
                if not in_barony_block:
                    if barony_start_pattern.search(line):
                        in_barony_block = True
                        brace_count = 1
                        block_header = line.rstrip() + '\n'
                        block_content = []
                    else:
                        outfile.write(line)
                else: # We are inside a barony block
                    # Don't add the header line again
                    if line.strip() != block_header.strip():
                         block_content.append(line)

                    brace_count += line.count('{')
                    brace_count -= line.count('}')

                    if brace_count <= 0:
                        reordered_block = reorder_and_cleanup_barony_block(block_header, block_content)
                        outfile.write(reordered_block)
                        
                        # Reset for the next block
                        in_barony_block = False
                        brace_count = 0
                        block_header = ""
                        block_content = []

        print(f"Reorganization complete. Output saved to '{output_filename}'")

    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if os.path.exists("00_landed_titles.txt"):
        process_landed_titles_file()
    else:
        print("Could not find '00_landed_titles.txt' in the current directory.")