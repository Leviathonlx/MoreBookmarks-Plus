import re
import sys

def organize_localization_file(input_filename, output_filename):
    try:
        with open(input_filename, 'r', encoding='utf-8-sig') as f: # utf-8-sig to handle BOM
            file_content_arg = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_filename}' not found.")
        return
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    lines = file_content_arg.strip().split('\n')
    
    processed_data = {} 
    l_english_header = ""
    unrecognized_lines_for_manual_check = []
    
    # Define patterns for comments/headers that should go into the manual review section
    manual_review_comment_patterns = [
        "#######################################################################################################################TFE",
        "#######################################################################################################################MB/Vanilla",
        "Claude Output.    Claude >>>>>>> ChatGPT",
        "#SOURCES",
        "# Prefixes",
        "# Names",
        "#Albanian", "#Coptic", "#Adhari", "#Udi", "#Carantanian", "#Crimean Gothic", "#Dalmatian",
        "#End################################################################################################################################################################################################################################################################################################",
        "#New Albanian", "#Romansh", "#Old East Slavic", "#Carantanian diacritics", 
        "# PATRONYMS — PREFIXES AND SUFFIXES",
        "####################", "#CIRCASSIAN/KASSOGI#", "################", "#AVAR/DAGESTANI#",
        "#######################################################################################################################################################################################################################################################################################################",
        "# Kven", "#Celtic tribes", "#Northern Germans", "#Patronymic naming", "#Dynasty naming", "#Tuareg", "#Jukun", "#Omotic",
        "#Oromo", "#Sidama", "#Agrobba", "#Harla", "#Kanuri-Kanem - from Dierk Lange", "#Hausa", "#7 founding dynasties",
        "#other hausa dynasties", "#regional groups", "#Gaunche", "# Yoruba", "#Edo", "#Igbo", "#Nupe", "#Baatonu", "# Sorko",
        "#Gur", "#Akan", "#Serer/Wolof", "#Fulbe", "#Kanuri", "#Daju", "#Nubian", "#Aquitanian dynasties",
        "#Persian dynasties", "#Indian", "#Roman", "#Berber", "##Gothic", "##Turkic", "## Bedouin",
        "# White Hun/Hephthalite/Kidarite/Xionite/etc", "# Bactrian", "# Yeniseian", "# Xiongnu", "# Di", "# Xianbei",
        "# Other Dunhuang/Tarim Basin", "# Frankish", "# Baltic", "## LEVANTINE", "#Punic", "#Hebrew", "# Wusun",
        "# Improved Pre-Islamic Persian names credits to Amir Immortal", "############################################",
        "# Eajbongshi/Meitei Dynasties", "# h", "# Livonians", "# South Arabian Names (from RICE/cybrxkhan)",
        "#New NB#", "# FP2", "#Oriya", "# Sicily", "#FP3", "#FP3 East Bantu", "########################################",
        "#### Estonian", "#### Galindian", "#### Goliadian", "#### Latvian", "#### Lithuanian", "#Vanilla", "#### Prussian",
        "#### Vepsian", "#### Additional prussian", "#### Additional latgalian", "#### Additional sami",
        "#### Additional estonian", "#### Additional karelian", "#### Additional vepsian", "#### Additional pictish",
        "#### Additional cornish", "#### Additional cumbrian", "#### Additional visigothic", "#### Additional lombard",
        "#### Additional baloch", "#### Additional samoyed (=Bjarmian)", "#### Additional khanty (=Ostyak)",
        "#### Additional khazar", "#### Additional bolghar", "#### Additional laktan", "#### Additional kirghiz",
        "#### Additional kipchak, kimek", "#### Additional cuman", "#### Additional bashkir", "#### Additional mordvin",
        "#### Additional merya", "#### Additional meshchera & muroma", "#### Additional mari", "#### Additional tamil",
        "#### Additional telugu", "#### Additional kannada", "#### Additional bengali & assamese",
        "#### Additional hindustani & rajput & sindhi", "#### Additional gujarati", "#### Additional punjabi",
        "#### Additional marathi", "#### Additional kashmiri", "#### Additional sinhala", "# Burman", "# Iberian",
        "# Sardinian", "# Chuvash", "# Africa", "# Italian", "#Mongolic - mongol", "#Mongolic - buryat",
        "#Mongolic - oirat", "#Mongolic - naiman", "#Mongolic - kerait", "#Turkic - uriankhai",
        "#Minamoto, Seiwa-Gen Ji", "#Chiba", "#Uesugi", "#Ashikaga", "#Hosokawa", "#Imagawa", "#Takeda",
        "#Hatakeyama", "#Murakami Genji [Minamoto]", "#Shimazu", "#Kono", "#Akamatsu", "#Yamana", "#Ogasawara",
        "#Sasaki", "#Nagao", "#Muto", "#Otomo", "#Matsura", "#Daijo", "#Utsunomiya", "#Date", "#Kasai", "#Shiba",
        "#Nambu", "#Chosokabe", "#Miyoshi", "#Ouchi", "#Kikuchi", "#Oda", "#Toki", "#Yuki", "#Matsudaira", "#Suwa",
        "#Ando", "#Asakura", "#Misawa", "#Mori", "#Kikkawa", "#Kobayakawa", "#Sano", "#Ashina", "#Hatta & Oda",
        "#Sogdian_Mi", "#Sogdian_Yi", "#Nanman-Bai", "#Nanman-Yi", "#Nanman-Pu", "#Khitan", "#Kumo Xi", "#Xianbei",
        "#Tangut", "#Tunguse", "#Goryeo", "#Lanxang", "#Malay", "#Karnuk", "#Iohulu", "#Gingciri", "#Vietnamese",
        "#Ly", "#Tran", "#Khuc", "#Duong", "#Kieu", "#Ngo", "#Dinh", "#Le", "#Mai", "#Ce", "#Annam", "#Champa",
        "#Mahidharapura", "#Oc Eo", "#Pegu", "#Thaton", "#Hariphunchai", "#Lavo", "#Suphannaphum", "#Phimai",
        "#Mergui", "#Bagan", "#Arakan", "#Pyu", "#Mon", "#Tai", "#Formosan", "#Yami", "#Paiwan", "#Rukai",
        "#Puyuma", "#Tsou", "#Saaroa", "#Kanakanabu", "#Bunun", "#Amis", "#Atayal", "#Seediq", "#Malay",
        "#Batak", "#Nias", "#Japanese Adventurers", "#German Adventurers", "#English Adventurers",
        "#Dutch Adventurers", "#French Adventurers", "#Italian Adventurers", "#Roman Adventurers",
        "#Basque Adventurers", "#Castilian Adventurers", "#Portuguese Adventurers", "#Khitan Adventurers",
        "#Russian Adventurers", "#Japanese Historical Characters", "#Okinawan", "#Ainu",
        "##############", "#NAKH/VAINAKH#", " ####", "###YAMATO###", "#Shogunate",
        "#End#", "# Vanilla" # Make sure these very short specific comments are also included if needed
    ]
    
    standard_comment_prefix = "#"

    for line_num, line_content_orig in enumerate(lines):
        line_stripped = line_content_orig.strip()
        
        if not line_stripped: 
            continue
        
        if line_stripped.lower() == "l_english:":
            if not l_english_header: 
                 l_english_header = line_content_orig 
            continue
            
        is_manual_review_comment = False
        if line_stripped.startswith(standard_comment_prefix):
            for pattern in manual_review_comment_patterns:
                if line_stripped == pattern: 
                    is_manual_review_comment = True
                    break
            if is_manual_review_comment:
                 unrecognized_lines_for_manual_check.append(line_content_orig)
            continue

        colon_index = line_stripped.find(':')
        if colon_index != -1:
            key_part = line_stripped[:colon_index]
            value_part = line_stripped[colon_index+1:].lstrip() 
            key = key_part.strip()
            
            if not re.match(r"^[a-zA-Z0-9_':-]+$", key): # Allow apostrophe and hyphen in key
                 unrecognized_lines_for_manual_check.append(f"# Potentially malformed key: {line_content_orig}")
                 continue
            processed_data[key] = value_part 
        else:
            unrecognized_lines_for_manual_check.append(line_content_orig)
            
    cat1_dynn_dynasty = {}
    cat2_dynnpat = {}
    cat3_other = {}

    for key, value_str in processed_data.items():
        if key.startswith("dynn_") or key.startswith("dynasty_"):
            cat1_dynn_dynasty[key] = value_str
        elif key.startswith("dynnpat_"):
            cat2_dynnpat[key] = value_str
        else:
            cat3_other[key] = value_str
            
    sorted_cat1_keys = sorted(cat1_dynn_dynasty.keys())
    sorted_cat2_keys = sorted(cat2_dynnpat.keys())
    sorted_cat3_keys = sorted(cat3_other.keys())

    output_content = []
    if l_english_header:
        output_content.append(l_english_header)
    else: 
        output_content.append("l_english:")
    
    output_content.append("\n################################################################################")
    output_content.append("# SECTION 1: Keys starting with dynn_ or dynasty_")
    output_content.append("################################################################################")
    for key in sorted_cat1_keys:
        output_content.append(f' {key}:{cat1_dynn_dynasty[key]}')

    output_content.append("\n################################################################################")
    output_content.append("# SECTION 2: Keys starting with dynnpat_")
    output_content.append("################################################################################")
    for key in sorted_cat2_keys:
        output_content.append(f' {key}:{cat2_dynnpat[key]}')

    output_content.append("\n################################################################################")
    output_content.append("# SECTION 3: Other keys")
    output_content.append("################################################################################")
    for key in sorted_cat3_keys:
        output_content.append(f' {key}:{cat3_other[key]}')
        
    if unrecognized_lines_for_manual_check:
        output_content.append("\n################################################################################")
        output_content.append("# SECTION 4: Unrecognized/Header lines for manual review")
        output_content.append("################################################################################")
        unique_unrecognized_lines = []
        seen_lines = set()
        for line_content in unrecognized_lines_for_manual_check:
            stripped_line = line_content.strip()
            if stripped_line and stripped_line not in seen_lines: 
                if not stripped_line.startswith("#"):
                     unique_unrecognized_lines.append(f"# {stripped_line}") 
                else:
                     unique_unrecognized_lines.append(line_content) 
                seen_lines.add(stripped_line)
        output_content.extend(unique_unrecognized_lines)
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(output_content))
        print(f"Successfully organized content into '{output_filename}'")
    except Exception as e:
        print(f"Error writing to output file: {e}")
        print("\nPrinting to console as fallback:\n")
        print("\n".join(output_content))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py <input_file.yml> <output_file.yml>")
    else:
        input_f = sys.argv[1]
        output_f = sys.argv[2]
        organize_localization_file(input_f, output_f)