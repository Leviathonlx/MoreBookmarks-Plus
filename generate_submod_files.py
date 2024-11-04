import sys
import os
import re
from collections import Counter
import glob
from math import floor

def task_progress_meter(workDone, totalWork):
    progress_meter_len = 20
    fracWorkDone = floor((workDone/totalWork)*progress_meter_len)
    progress_meter_string = '['+'*'*fracWorkDone+' '*(progress_meter_len-fracWorkDone)+']'
    print('\r'+progress_meter_string, end='')

class BuildItemDatabaseFromFolder:
    def action(self, file):
        print(f"Analyzing file: {file}")
        try:
            with open(file, 'r', encoding='utf-8') as f:
                file_text = ''.join(f.readlines())
            found_items = re.findall(r'^\s*([ekdcb]_[A-Za-z_\-]+)\s*=\s*\{', file_text, re.MULTILINE)
            print(f"Found {len(found_items)} titles in {file}")
            found_items = list(dict.fromkeys(found_items))
            return found_items
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")
            return []

def search_over_mod_structure(root_dir, file_keyword, file_action_object, data_object, console_output,
                            database=['common'],
                            check_localization=False):
    if len(database) == 0:
        raise RuntimeError("Did not provide a database to search in search_over_mod_structure(); failing")
    
    print(f"\nSearch parameters:")
    print(f"Root directory: {os.path.abspath(root_dir)}")
    
    landed_titles_dir = os.path.join(root_dir, 'common', 'landed_titles')
    if not os.path.exists(landed_titles_dir):
        print(f"Warning: Landed titles directory not found at {landed_titles_dir}")
        return []
        
    print(f"Searching in: {landed_titles_dir}")
    
    file_list = glob.glob(os.path.join(landed_titles_dir, '*.txt'))
    print(f"Found {len(file_list)} landed titles files")
    
    title_dict = {}
    
    for file, index in zip(file_list, range(len(file_list))):
        if console_output:
            task_progress_meter(index, len(file_list))
        found_titles = file_action_object.action(file)
        for title in found_titles:
            if title not in title_dict:
                title_dict[title] = []
            title_dict[title].append(os.path.basename(file))
    
    print("\nTitle sources:")
    duplicate_titles = {title: sources for title, sources in title_dict.items() if len(sources) > 1}
    if duplicate_titles:
        print("\nTitles found in multiple files:")
        for title, sources in duplicate_titles.items():
            print(f"  {title}: {', '.join(sources)}")
    
    return list(title_dict.keys())

def ensure_directory_exists(filepath):
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_titles_to_keep(title_list, exclusion_list):
    print(f"\nProcessing {len(title_list)} total titles found")
    
    filtered_titles = []
    excluded_variants = []
    
    variant_suffixes = ['_dan', '_fin', '_nor', '_swe', '_color', '_crusader', 
                       '_nordic', '_norman', '_norse', '_titular', '_french',
                       '_spanish', '_islam', '_meroving', '_slovien', '_band',
                       '_company', '_league', '_republic', '_east', '_west']
    
    for title in title_list:
        if any(suffix in title for suffix in variant_suffixes):
            excluded_variants.append(title)
            continue
        filtered_titles.append(title)
    
    print(f"Excluded {len(excluded_variants)} variant titles")
    if excluded_variants:
        print("Sample of excluded titles:")
        for title in excluded_variants[:5]:
            print(f"  - {title}")
    
    barony_list = [item for item in filtered_titles if item[0]=='b']
    county_list = [item for item in filtered_titles if item[0]=='c']
    duchy_list = [item for item in filtered_titles if item[0]=='d']
    kingdom_list = [item for item in filtered_titles if item[0]=='k']
    empire_list = [item for item in filtered_titles if item[0]=='e']
    
    print(f"\nFound by tier after filtering:")
    print(f"  Baronies: {len(barony_list)}")
    print(f"  Counties: {len(county_list)}")
    print(f"  Duchies: {len(duchy_list)}")
    print(f"  Kingdoms: {len(kingdom_list)}")
    print(f"  Empires: {len(empire_list)}")
    
    duchy_list = [item for item in duchy_list if item != 'd_emblem']
    empire_list = [item for item in empire_list if item not in ['e_on_partition','e_names']]
    
    titles_to_process = []
    if 'baronies' not in exclusion_list: titles_to_process.extend(barony_list)
    if 'counties' not in exclusion_list: titles_to_process.extend(county_list)
    if 'duchies' not in exclusion_list: titles_to_process.extend(duchy_list)
    if 'kingdoms' not in exclusion_list: titles_to_process.extend(kingdom_list)
    if 'empires' not in exclusion_list: titles_to_process.extend(empire_list)
    
    print(f"\nProcessing {len(titles_to_process)} titles after exclusions")
    return titles_to_process

def generate_output_files(titles_to_process):
    if not titles_to_process:
        print("No titles to process! Output files will be empty.")
        return
        
    print(f"\nGenerating output files for {len(titles_to_process)} titles")
    languages = ['english','french','german','korean','russian','simp_chinese','spanish']
    
    base_dir = './CK3_Color_Storage/CK3CS'

    filepath = f'{base_dir}/common/coat_of_arms/coat_of_arms/CK3CS_titles.txt'
    ensure_directory_exists(filepath)
    print(f"Writing coat of arms file: {filepath}")
    with open(filepath, 'w', encoding='utf-8') as f:
        for title in titles_to_process:
            f.write(f'd_{title}_color = {{ pattern = "pattern_solid.dds" color1 = "white" color2 = "white" }}\n')
    
    filepath = f'{base_dir}/common/landed_titles/CK3CS_titles.txt'
    ensure_directory_exists(filepath)
    print(f"Writing landed titles file: {filepath}")
    with open(filepath, 'w', encoding='utf-8') as f:
        for title in titles_to_process:
            f.write(f'd_{title}_color = {{ definite_form = yes color ={{0 0 0}} can_create = {{ always = no }} }}\n')
    
    print("Writing localization files...")
    for language in languages:
        filepath = f'{base_dir}/localization/{language}/CK3CS_titles_l_{language}.yml'
        ensure_directory_exists(filepath)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f'l_{language}:\n')
            for title in titles_to_process:
                f.write(f'd_{title}_color: ""\n')
    
    filepath = f'{base_dir}/common/on_action/CK3CS_titles.txt'
    ensure_directory_exists(filepath)
    print(f"Writing on_action file: {filepath}")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('#NB: prepended with 000 because this needs to fire off before things like tributaries are assigned\n\n')
        
        f.write('on_game_start = {\n')
        f.write('    on_actions = {\n')
        f.write('        CK3CS_build_color_variable_refs\n')
        f.write('        CK3CS_set_color_title_colors\n')
        f.write('    }\n')
        f.write('}\n\n')
        
        f.write('#Associate every title in question with a color storage title\n')
        f.write('CK3CS_build_color_variable_refs = {\n')
        f.write('    effect = {\n')
        for title in titles_to_process:
            f.write(f'        title:{title} = {{ if = {{ limit = {{ exists = this }} }} set_variable = {{ name = color_storage value = title:d_{title}_color }} }}\n')
        f.write('    }\n')
        f.write('}\n\n')
        
        f.write('#Reset the actual color storage title\n')
        f.write('CK3CS_set_color_title_colors = {\n')
        f.write('    effect = {\n')
        for title in titles_to_process:
            f.write(f'        title:d_{title}_color = {{ set_color_from_title = title:{title} }}\n')
        f.write('    }\n')
        f.write('}\n')

def console_input_parsing(argument_list):
    argument_list.pop(0)
    
    print(f"Arguments received: {argument_list}")
    
    if len(argument_list) == 0:
        print("No arguments provided! Please provide mod folder name.")
        sys.exit(1)
        
    root_dir = ''
    if os.path.isdir('./'+str(argument_list[0])+'/'):
        root_dir = argument_list[0]
    elif os.path.basename(os.getcwd()) == argument_list[0]:
        root_dir = './'
    else:
        print('No folder named '+str(argument_list[0])+' exists; stopping execution')
        print(f"Current directory: {os.getcwd()}")
        print(f"Looking for: {os.path.abspath('./' + str(argument_list[0]))}")
        sys.exit(1)
        
    argument_list.pop(0)
    print(f"Using root directory: {os.path.abspath(root_dir)}")
    
    acceptable_tiers = ['baronies', 'counties', 'duchies', 'kingdoms', 'empires']
    exclusion_list = [item for item in argument_list if item in acceptable_tiers]
    exclusion_list = list(set(exclusion_list))
    
    print(f"Excluding tiers: {exclusion_list}")
    
    return root_dir, exclusion_list

def generate_files(root_dir, exclusion_list, console_output=False):
    print(f"Current working directory: {os.getcwd()}")
    
    if(console_output): print('Building Database')
    database_build = BuildItemDatabaseFromFolder()
    title_list = search_over_mod_structure(root_dir, 'landed_titles', database_build, [], console_output)
    
    title_list.sort()
    titles_to_process = get_titles_to_keep(title_list, exclusion_list)
    del title_list
    
    generate_output_files(titles_to_process)
    print("\nFile generation complete!")

if __name__ == '__main__':
    root_dir, exclusion_list = console_input_parsing(sys.argv)
    generate_files(root_dir, exclusion_list, True)