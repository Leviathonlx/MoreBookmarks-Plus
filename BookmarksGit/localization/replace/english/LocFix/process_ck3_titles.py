import re

def process_names_localization_file(file_content):
    lines = file_content.splitlines()

    all_entries = {}
    
    # Process all lines to populate all_entries, handling duplicates (keeping the last)
    for line in lines:
        stripped_line = line.strip()
        # Regex to match a key followed by a colon
        match = re.match(r'^(\S+):', stripped_line)
        if match:
            key = match.group(1)
            all_entries[key] = stripped_line # Store the stripped line

    # Categories for sorting
    dynn_entries = []
    other_name_entries = []

    # Populate categories
    for key, value in all_entries.items():
        if key.startswith('dynn_'):
            dynn_entries.append(value)
        else:
            other_name_entries.append(value)

    # Sort each category alphabetically
    dynn_entries.sort()
    other_name_entries.sort()

    # Reconstruct the file content
    output_lines = []

    # Add other name entries block
    if other_name_entries:
        output_lines.append("# Other Name Entries (sorted alphabetically)")
        for entry_line in other_name_entries:
            output_lines.append(f" {entry_line}") # Add a space for consistent indentation
        output_lines.append("") # Add a newline after the block

    # Add dynn_ entries block
    if dynn_entries:
        output_lines.append("# dynn_ Entries (to be easily copied/pasted out - sorted alphabetically)")
        for entry_line in dynn_entries:
            output_lines.append(f" {entry_line}") # Add a space for consistent indentation
        output_lines.append("") # Add a newline after the block
            
    # Join all lines and return
    return "\n".join(output_lines)

# Read the content of the uploaded file with UTF-8 encoding
with open('0_MB_Names_l_english.yml', 'r', encoding='utf-8') as f:
    file_content = f.read()

processed_content = process_names_localization_file(file_content)

# Save to the new file with UTF-8 encoding
output_filename = '0_MB_Names_l_english_processed.yml'
with open(output_filename, 'w', encoding='utf-8') as f:
    f.write(processed_content)

print(f"Processing complete. Check '{output_filename}'")