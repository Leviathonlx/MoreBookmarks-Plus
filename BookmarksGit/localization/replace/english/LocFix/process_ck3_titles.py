import re

def process_and_sort_colors_file(file_content):
    lines = file_content.splitlines()

    all_entries = {}
    
    # Process all lines to populate all_entries, handling duplicates (keeping the last)
    # This also skips empty lines or lines that are just comments in the parsing
    for line in lines:
        stripped_line = line.strip()
        # Regex to match a key followed by a colon
        match = re.match(r'^(\S+):', stripped_line)
        if match:
            key = match.group(1)
            all_entries[key] = stripped_line # Store the stripped line

    # Collect all entries into a list and sort alphabetically
    sorted_entries = sorted(list(all_entries.values()))

    # Reconstruct the file content
    output_lines = []

    # Add a header comment
    output_lines.append("# Culture Colors (sorted alphabetically, duplicates removed)")
    
    # Add the sorted entries
    for entry_line in sorted_entries:
        output_lines.append(f" {entry_line}") # Add a space for consistent indentation
        
    # Join all lines and return
    return "\n".join(output_lines)

# Read the content of the uploaded file with UTF-8 encoding
with open('culture_colors.txt', 'r', encoding='utf-8') as f:
    file_content = f.read()

processed_content = process_and_sort_colors_file(file_content)

# Save to the new file with UTF-8 encoding
output_filename = 'culture_colors_processed.txt'
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(processed_content)

print(f"Processing complete. Check '{output_filename}'")