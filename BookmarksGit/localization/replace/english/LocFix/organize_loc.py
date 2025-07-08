import os

def organize_localization_file(input_filename="new 1.txt", output_filename="organized_religion_localizations.txt"):
    """
    Organizes a Paradox-style localization file by separating 'doctrine'
    localizations, sorting them alphabetically, and placing them at the
    top of a new file.
    """
    if not os.path.exists(input_filename):
        print(f"Error: Input file '{input_filename}' not found.")
        return

    doctrine_lines = []
    other_lines = []

    print(f"Reading from '{input_filename}'...")

    # Use utf-8-sig to handle the BOM (Byte Order Mark) that sometimes appears
    # at the beginning of Paradox files.
    with open(input_filename, 'r', encoding='utf-8-sig') as f:
        for line in f:
            stripped_line = line.strip()
            
            # Preserve comments and empty lines in the 'other' section
            if not stripped_line or stripped_line.startswith('#'):
                other_lines.append(line)
                continue

            # Check if it's a valid key-value line
            if ':' in line:
                key = line.split(':', 1)[0].strip()
                # Check if the key indicates a doctrine localization
                if 'doctrine' in key:
                    doctrine_lines.append(line)
                else:
                    other_lines.append(line)
            else:
                # If a line has content but no colon, treat it as 'other'
                other_lines.append(line)

    # Sort the doctrine lines alphabetically by their key
    # The key for sorting is the part of the string before the first colon
    print(f"Found {len(doctrine_lines)} doctrine lines to sort.")
    doctrine_lines.sort(key=lambda line: line.split(':', 1)[0].strip())

    print(f"Writing organized content to '{output_filename}'...")

    with open(output_filename, 'w', encoding='utf-8') as f:
        # Write the sorted doctrines section
        f.write("# --- Doctrines (Alphabetically Sorted) ---\n\n")
        f.writelines(doctrine_lines)
        
        # Write the rest of the localizations
        f.write("\n\n# --- Other Localizations ---\n\n")
        f.writelines(other_lines)

    print("Organization complete!")

if __name__ == "__main__":
    organize_localization_file()