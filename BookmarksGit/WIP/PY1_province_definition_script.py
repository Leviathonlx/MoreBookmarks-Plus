# First
# Script for changing colors in province map and updating province definitions in definitions file
# Specifically looks for # NEEDS DONE comment. Changes colors to unused colors that are named b_test_*
import os
import re
from PIL import Image

# Configuration
DEFINITION_FILE = 'definition.txt'
PROVINCE_MAP = 'provincesreplace.png'
OUTPUT_MAP = 'provinces_new.png'
OUTPUT_DEF = 'definition_updated.txt'

def process_transfer():
    with open(DEFINITION_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    needs_done = []
    available_slots = []
    
    # 1. Parse the file for Source provinces and Available new slots
    # Pattern for #9863;93;192;31;... # NEEDS DONE
    source_pattern = re.compile(r'^#(\d+);(\d+);(\d+);(\d+);([^;]+);x;\s*#\s*([^#]+)#\s*NEEDS DONE')
    # Pattern for available slots: #14204;221;215;99;b_test_14204;x
    slot_pattern = re.compile(r'^#(\d+);(\d+);(\d+);(\d+);b_test_\d+;x')

    for i, line in enumerate(lines):
        source_match = source_pattern.match(line.strip())
        slot_match = slot_pattern.match(line.strip())
        
        if source_match:
            needs_done.append({
                'index': i,
                'old_id': source_match.group(1),
                'old_rgb': (int(source_match.group(2)), int(source_match.group(3)), int(source_match.group(4))),
                'name': source_match.group(5),
                'comment': source_match.group(6).strip()
            })
        elif slot_match:
            available_slots.append({
                'index': i,
                'new_id': slot_match.group(1),
                'new_rgb': (int(slot_match.group(2)), int(slot_match.group(3)), int(slot_match.group(4)))
            })

    if not needs_done:
        print("No provinces marked '# NEEDS DONE' found.")
        return

    if len(available_slots) < len(needs_done):
        print(f"Warning: Only {len(available_slots)} slots available for {len(needs_done)} provinces.")
    
    # 2. Create Mappings
    color_map = {} # Mapping old RGB to new RGB for the image
    
    print(f"Processing {min(len(needs_done), len(available_slots))} provinces...")

    for src, slot in zip(needs_done, available_slots):
        # Update the Definition Text Line
        # Format: ID;R;G;B;NAME;x; # Comment # OldID -> NewID -- TRANSFERRED
        new_line = f"{slot['new_id']};{slot['new_rgb'][0]};{slot['new_rgb'][1]};{slot['new_rgb'][2]};{src['name']};x; # {src['comment']} # {src['old_id']} --> {slot['new_id']} -- TRANSFERRED\n"
        lines[src['index']] = new_line
        
        # Comment out the used slot so it isn't used again next run
        lines[slot['index']] = f"# USED: {lines[slot['index']]}"
        
        # Add to image color swap map
        color_map[src['old_rgb']] = slot['new_rgb']

    # 3. Update the Image
    print("Updating province map image (this may take a moment)...")
    img = Image.open(PROVINCE_MAP).convert('RGB')
    pixels = img.load()
    width, height = img.size

    for y in range(height):
        for x in range(width):
            current_rgb = pixels[x, y]
            if current_rgb in color_map:
                pixels[x, y] = color_map[current_rgb]

    img.save(OUTPUT_MAP)
    
    # 4. Write new definition file
    with open(OUTPUT_DEF, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"Done! Created {OUTPUT_DEF} and {OUTPUT_MAP}")

if __name__ == "__main__":
    process_transfer()