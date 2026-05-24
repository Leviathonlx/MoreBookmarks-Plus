import os
import re

# All the unique broken IDs from your error log
BAD_IDS = {
    "marinid_1", "dabbabid_1", "fadlid_1", "fadlid_3", "naiman_guchugud_1", "mpo_mongol_1",
    "bookmark_huang_chao", "li_674E_zhuye_1", "he_4F55_30_1", "han_3310", "han_7308", 
    "han_7436", "viet_ly_10", "dali_duan_12", "tangut_liang_1", "tangut_liang_2", 
    "han_7897", "han_12371", "han_12084", "han_11957", "han_8052", "su_82CF_1", 
    "jurchen_tudan_1", "khmer_varman_9", "dayak_segara_11", "javanese_sanjaya_07", 
    "haripunjaya_ruler_7", "japanese_taira_kanmu_16", "japanese_taira_kanmu_32", 
    "japanese_taira_kanmu_34", "japanese_taira_kanmu_36", "japanese_taira_kanmu_65", 
    "japanese_taira_kanmu_68", "japanese_minamoto_seiwa_3", "japanese_minamoto_seiwa_5", 
    "japanese_minamoto_seiwa_6", "japanese_minamoto_seiwa_9", "japanese_minamoto_seiwa_10", 
    "japanese_minamoto_seiwa_21", "japanese_minamoto_seiwa_59", "japanese_minamoto_seiwa_139", 
    "japanese_minamoto_seiwa_205", "japanese_minamoto_seiwa_207", "japanese_minamoto_seiwa_208", 
    "japanese_minamoto_seiwa_365", "japanese_fujiwara_9", "japanese_fujiwara_84", 
    "japanese_fujiwara_132", "japanese_fujiwara_460", "japanese_fujiwara_461", 
    "japanese_fujiwara_497", "japanese_fujiwara_498", "japanese_fujiwara_500", 
    "japanese_fujiwara_511", "japanese_fujiwara_514", "japanese_fujiwara_516", 
    "japanese_fujiwara_530", "japanese_fujiwara_577", "japanese_fujiwara_1122", 
    "japanese_kiyohara_12", "japanese_kiyohara_15", "japanese_kiyohara_16", "han_12651", 
    "han_30000", "japanese_yamato_26", "japanese_yamato_35", "japanese_yamato_45", 
    "japanese_yamato_50", "japanese_yamato_51", "japanese_yamato_54", "japanese_yamato_192", 
    "japanese_yamato_376", "japanese_minamoto_murakami_12", "japanese_minamoto_murakami_13", 
    "japanese_nakahara_kiso_5", "japanese_sakanoue_1", "easteregg_magne_skjaeran", 
    "easteregg_fredrik_wester", "EPE_easter_egg_2", "EPE_easter_egg_3", "EPE_easter_egg_4", 
    "EPE_easter_egg_6", "EPE_easter_egg_7", "EPE_easter_egg_8", "EPE_easter_egg_9", 
    "RICE_kurdish_pagan_001", "10000115", "10010406", "10017016", "10017018", "10017020", 
    "10026050", "10026052", "10029011", "10029105", "10031001", "10032402", "10040004", 
    "10040008", "10041924", "10044207", "10050084", "10050085", "10055606", "10057612", 
    "10060030", "10064017", "10064327", "10064411", "10064525", "10066479", "12154000", 
    "12154001", "12187041", "12187043", "12271425", "12360740", "12360741", "12361035", 
    "12385055", "12425118", "12430055", "12661463", "12666030"
}

# Pre-format what the text looks like so we can do exact matches
BAD_REFERENCES = [f"character:{char_id}" for char_id in BAD_IDS]

def clean_ck3_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    depth = 0
    block_starts = {}
    blocks_to_delete = []

    in_quote = False
    in_comment = False
    i = 0
    
    # Parse file character by character to track CK3 formatting depths perfectly
    while i < len(content):
        char = content[i]
        
        if in_comment:
            if char == '\n':
                in_comment = False
        elif in_quote:
            if char == '"':
                in_quote = False
        else:
            if char == '#':
                in_comment = True
            elif char == '"':
                in_quote = True
            elif char == '{':
                depth += 1
                block_starts[depth] = i
            elif char == '}':
                # Depth 2 is the Date block (e.g. 1380.1.1 = { ... }) 
                # Depth 1 is the character ID, Depth 3 is the effect/employer tag
                if depth == 2:
                    start_idx = block_starts[depth]
                    end_idx = i
                    
                    block_text = content[start_idx:end_idx+1]
                    
                    # Check if any bad reference is inside this specific block
                    for bad_ref in BAD_REFERENCES:
                        # Use regex boundary \b to ensure we don't accidentally match 
                        # character:10 inside character:100
                        if re.search(re.escape(bad_ref) + r'\b', block_text):
                            
                            # Trace backwards to capture the date line itself (e.g. "1380.1.1 = {")
                            line_start = content.rfind('\n', 0, start_idx)
                            if line_start == -1:
                                line_start = 0
                            else:
                                line_start += 1 # Move past the newline char
                                
                            blocks_to_delete.append((line_start, end_idx + 1))
                            break # Once marked for deletion, no need to check other IDs in this block
                depth -= 1
        i += 1

    # Delete blocks from the bottom of the file upwards to avoid shifting our index targets
    if blocks_to_delete:
        print(f"Found {len(blocks_to_delete)} broken date blocks in '{os.path.basename(filepath)}'. Cleaning...")
        for start, end in reversed(blocks_to_delete):
            # Clean up the trailing whitespace/newline so no empty spaces are left
            if end < len(content) and content[end] == '\n':
                end += 1
            elif end + 1 < len(content) and content[end:end+2] == '\r\n':
                end += 2
                
            content = content[:start] + content[end:]

        # Save back to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Cleanup Complete! File successfully overwritten.")
    else:
        print(f"No broken references found in '{os.path.basename(filepath)}'.")


if __name__ == "__main__":
    
    # --- SPECIFY YOUR TARGET FILE HERE ---
    TARGET_FILE = "00_MONGOLIC.txt" 
    
    print(f"Targeting file: {TARGET_FILE}")
    print("WARNING: Make sure you have backed up your file before running this!")
    
    choice = input("Press Enter to continue or 'q' to quit: ")
    if choice.lower() != 'q':
        if os.path.isfile(TARGET_FILE):
            clean_ck3_file(TARGET_FILE)
        else:
            print(f"ERROR: Could not find '{TARGET_FILE}'.")
            print("Make sure this script is in the same folder as the text file, or provide the full file path.")