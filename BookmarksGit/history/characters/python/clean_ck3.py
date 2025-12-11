import re
import os

def clean_county_history(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        print(f"Read {len(content)} characters. Processing...")

        output_buffer = []
        last_processed_index = 0
        
        # --- PARSER VARIABLES ---
        depth = 0
        in_comment = False
        in_string = False
        block_start_index = -1
        
        # Iterate through file character by character
        i = 0
        while i < len(content):
            char = content[i]

            # 1. Handle Comments (ignore text until newline)
            if in_comment:
                if char == '\n':
                    in_comment = False
            # 2. Handle Strings (ignore braces inside quotes)
            elif in_string:
                if char == '"':
                    in_string = False
                elif char == '\\': # Skip escape characters
                    i += 1 
            # 3. Handle Code Structure
            else:
                if char == '#':
                    in_comment = True
                elif char == '"':
                    in_string = True
                elif char == '{':
                    if depth == 0:
                        block_start_index = i
                    depth += 1
                elif char == '}':
                    depth -= 1
                    # We just closed a top-level block (depth went 1 -> 0)
                    if depth == 0:
                        block_end_index = i + 1
                        
                        # Identify the Title (look backwards from '{' for "c_something =")
                        pre_block_text = content[max(0, block_start_index-200) : block_start_index]
                        key_match = re.search(r'([a-zA-Z0-9_]+)\s*=\s*$', pre_block_text)
                        
                        if key_match:
                            title_key = key_match.group(1)
                            
                            # === LOGIC CHECK: Only clean "c_" (Counties) ===
                            if title_key.startswith('c_'):
                                # 1. Append text leading up to this block (keep comments/spacing intact)
                                output_buffer.append(content[last_processed_index : block_start_index])
                                
                                # 2. Clean the block content
                                raw_block = content[block_start_index : block_end_index]
                                cleaned_block = apply_cleaning_logic(raw_block)
                                output_buffer.append(cleaned_block)
                                
                                last_processed_index = block_end_index
                            else:
                                # Not a county, skip processing
                                pass

            i += 1

        # Append remaining file content
        output_buffer.append(content[last_processed_index:])
        final_content = "".join(output_buffer)

        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(final_content)

        print(f"Done! Saved to: {output_file_path}")

    except FileNotFoundError:
        print(f"Error: The file '{input_file_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def apply_cleaning_logic(text):
    """
    Applies the removal logic safely.
    """
    
    # --- STEP 1: Remove 'holder = 0' ---
    # CHANGED: Removed '.*' from the end. 
    # This ensures we do NOT delete comments or closing brackets '}' on the same line.
    # If a comment remains (e.g. "holder=0 # text"), Step 2 will handle it.
    text = re.sub(r'\s*holder\s*=\s*0\b', '', text)
    
    # --- STEP 2: Remove Empty Date Blocks ---
    # Matches a date block that contains ONLY whitespace OR comments.
    # regex:
    # \s*\d+\.\d+\.\d+\s*=\s*\{   -> Date header
    # (?:[\s]|#[^\n]*)*           -> Content (Whitespace OR Comments, repeated)
    # \}                          -> Closing brace
    date_block_pattern = r'\s*\d+\.\d+\.\d+\s*=\s*\{(?:[\s]|#[^\n]*)*\}'
    
    text = re.sub(date_block_pattern, '', text)
    
    return text

# --- CONFIGURATION ---
input_filename = "00_ASIA_CHINA.txt" 
output_filename = "title_history_cleaned.txt"

if __name__ == "__main__":
    if not os.path.exists(input_filename):
        print("Creating test file with tricky brackets...")
        dummy_data = """
c_safe_test = {
    # This bracket on the same line caused the issue before:
	1200.1.1 = { holder = 0 }
    
    # This comment inside a block should be deleted along with the date
    1201.1.1 = { 
        holder = 0 # Some comment
    }

    # This comment outside should persist
    # Note
}
"""
        with open(input_filename, 'w', encoding='utf-8') as f:
            f.write(dummy_data)

    clean_county_history(input_filename, output_filename)