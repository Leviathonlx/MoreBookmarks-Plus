import argparse
import os

def clean_paradox_file(input_path: str, output_path: str, indent_char: str = '\t'):
    """
    Cleans a Paradox-style script file by fixing inconsistent indentation.
    This version correctly handles commented-out lines and single-line blocks.

    Args:
        input_path (str): The path to the file to clean.
        output_path (str): The path to write the cleaned file to.
        indent_char (str, optional): The character(s) to use for one level of indentation. Defaults to a tab ('\t').
    """
    try:
        with open(input_path, 'r', encoding='utf-8-sig') as f_in:
            lines = f_in.readlines()
    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'")
        return

    cleaned_lines = []
    indent_level = 0

    for line in lines:
        trimmed_line = line.strip()

        # Preserve blank lines
        if not trimmed_line:
            cleaned_lines.append('\n')
            continue

        # Get the part of the line that is actual code, ignoring comments
        code_part = trimmed_line.split('#', 1)[0].strip()

        # Count braces only in the code part to determine net change
        open_braces = code_part.count('{')
        close_braces = code_part.count('}')

        # A line that closes a block should be un-indented *before* it is written.
        # This handles lines that only contain '}'
        if close_braces > open_braces:
            indent_level -= (close_braces - open_braces)
            # Failsafe against negative indentation from malformed files
            indent_level = max(0, indent_level)

        # Write the line with the (potentially new) current indentation level
        current_indent = indent_char * indent_level
        cleaned_lines.append(f"{current_indent}{trimmed_line}\n")
        
        # A line that opens a new block increases the indent for the *next* line.
        if open_braces > close_braces:
            indent_level += (open_braces - close_braces)

    # Write the cleaned content to the output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f_out:
            f_out.writelines(cleaned_lines)
    except IOError as e:
        print(f"Error: Could not write to output file at '{output_path}'. Reason: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean up indentation in Paradox-style script files (e.g., CK3 history).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "input_file",
        help="Path to the input file to be cleaned."
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to the output file. If not provided, a new file with '_cleaned' suffix will be created."
    )
    parser.add_argument(
        "-i", "--in-place",
        action="store_true",
        help="Modify the input file directly (overwrite). Use with caution."
    )
    parser.add_argument(
        "--indent",
        default='\t',
        help="Character(s) to use for indentation. Use '    ' for four spaces. Default is a tab '\\t'."
    )
    
    args = parser.parse_args()

    if args.in_place:
        output_file_path = args.input_file
        print(f"Cleaning file '{args.input_file}' in-place...")
    elif args.output:
        output_file_path = args.output
        print(f"Cleaning '{args.input_file}' and saving to '{output_file_path}'...")
    else:
        # Create a default output name
        base, ext = os.path.splitext(args.input_file)
        output_file_path = f"{base}_cleaned{ext}"
        print(f"Cleaning '{args.input_file}' and saving to '{output_file_path}'...")

    clean_paradox_file(args.input_file, output_file_path, args.indent)
    print("Done!")