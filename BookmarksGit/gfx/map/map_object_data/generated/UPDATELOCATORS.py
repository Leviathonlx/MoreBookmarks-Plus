import re
import os

# ================= CONFIGURATION =================
INPUT_FILENAME = "tree_pine_impassable_01_a_generator_1.txt"  # Change this to your actual file name
OUTPUT_FILENAME = "tree_pine_impassable_01_a_generator_1_FIXED.txt"
# =================================================

def adjust_transform_coordinates():
    if not os.path.exists(INPUT_FILENAME):
        print(f"Error: Could not find '{INPUT_FILENAME}' in the current folder.")
        return

    print(f"Processing '{INPUT_FILENAME}'...")

    with open(INPUT_FILENAME, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    # Pattern: Matches transform=" up to the next "
    # We capture the content inside the quotes to process it.
    pattern = r'(transform\s*=\s*")([^"]*)(")'

    def replacement_function(match):
        prefix = match.group(1)   # transform="
        inner_text = match.group(2)
        # We don't use group 3 in the logic, we manually reconstruct the end.

        # Split text into tokens (ignoring original newlines/spaces)
        tokens = inner_text.split()
        
        if not tokens:
            return match.group(0)

        new_tokens = []
        for i, token in enumerate(tokens):
            # Z is at index 2, 12, 22... (every 10th number)
            if (i % 10) == 2:
                try:
                    val = float(token)
                    val += 512.0
                    new_tokens.append("{:.6f}".format(val))
                except ValueError:
                    new_tokens.append(token)
            else:
                new_tokens.append(token)

        # Formatting: 
        # Paradox files usually like having the closing quote on a new line 
        # or at least separated to ensure the following '}' isn't lost.
        
        formatted_lines = []
        current_line = []
        
        for token in new_tokens:
            current_line.append(token)
            if len(current_line) == 10:
                formatted_lines.append(" ".join(current_line))
                current_line = []
        
        if current_line:
            formatted_lines.append(" ".join(current_line))

        # Join the numbers with newlines
        new_inner_text = "\n".join(formatted_lines)
        
        # KEY FIX: Add a newline before the closing quote.
        # This ensures the closing " is on its own line (or start of one), 
        # pushing the subsequent '}' to a clean position.
        return f'{prefix}{new_inner_text}\n"'

    # Apply the replacement
    new_content = re.sub(pattern, replacement_function, content)

    with open(OUTPUT_FILENAME, 'w', encoding='utf-8-sig') as f:
        f.write(new_content)

    print(f"Success! Created '{OUTPUT_FILENAME}'.")

if __name__ == "__main__":
    adjust_transform_coordinates()