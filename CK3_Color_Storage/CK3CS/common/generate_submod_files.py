import sys
import os
import re
from collections import Counter
import glob
from math import floor

'''
Searches your CK3 mod landed titles to generate the various colour storage items in the folder CK3CS.
The items in CK3CS/ folder
'''

acceptable_tiers = ['baronies','counties','duchies','kingdoms','empires']

##### Helper Routines

#Wrapper Class for building a list of items for which to search the database
class BuildItemDatabaseFromFolder:
    '''
    Arguments:
      root_dir: Directory Root Dir
      dir_name: Directory we're search
    Desc
      Pulls the list of items from the database folder
    '''
    def action(self,file):
        print(f"Analyzing file: {file}")
        item_list = []
        file_text = []
        try:
            with open(file,'r', encoding='utf-8') as f:
                file_text = ''.join(f.readlines())
            found_items = re.findall('([e|k|d|c|b]_[A-z_\-]+)[ ]*=[ ]*\{',file_text)
            print(f"Found {len(found_items)} titles in {file}")
            return found_items
        except Exception as e:
            print(f"Error processing file {file}: {str(e)}")
            return []

def task_progress_meter(workDone,totalWork):
    progress_meter_len = 20
    fracWorkDone = floor((workDone/totalWork)*progress_meter_len)
    progress_meter_string = '['+'*'*fracWorkDone+' '*(progress_meter_len-fracWorkDone)+']'
    print('\r'+progress_meter_string,end='')

def compare_file_path_with_item(file_path,re_pattern):
    found_item = False
    file_path = file_path.split('/')
    file_path = file_path[:-1]
    
    for folder in file_path:
        if ( re.search('^'+re_pattern+'$',folder) ):
            found_item |= True
    
    return found_item

def search_over_mod_structure(root_dir,file_keyword,file_action_object,data_object,console_output,
                            database=['common'],
                            check_localization=False):
    if ( len(database)== 0): RuntimeError("Did not provide a database to search in search_over_mod_structure(); failing")
    
    database_items = '('
    for item in database:
        database_items += item
        database_items += '|'
    database_items = database_items[:-1] #Remove the last '|'
    database_items += ')'
    
    print(f"\nSearch parameters:")
    print(f"Root directory: {os.path.abspath(root_dir)}")
    print(f"Looking for files matching: {file_keyword}")
    print(f"In databases: {database}")
    
    # Convert to Windows path style for matching
    root_dir = root_dir.replace('/', '\\')
    
    # Search for all .txt files
    print("\nScanning for files...")
    file_list = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.txt'):
                full_path = os.path.join(root, file)
                file_list.append(full_path)
    
    print(f"Found {len(file_list)} total text files")
    
    if check_localization:
        yml_files = []
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                if file.endswith('.yml'):
                    full_path = os.path.join(root, file)
                    yml_files.append(full_path)
        print(f"Found {len(yml_files)} YAML files")
        file_list.extend(yml_files)
    
    matching_files = []
    for file, index in zip(file_list, range(len(file_list))):
        if console_output:
            task_progress_meter(index, len(file_list))
        if re.search(file_keyword, file):
            matching_files.append(file)
            if isinstance(data_object, list):
                data_object.extend(file_action_object.action(file))
            else:
                data_object = file_action_object.action(file)
    
    print(f"\nFound {len(matching_files)} files matching '{file_keyword}':")
    for file in matching_files:
        print(f"  - {file}")
        
    if console_output:
        task_progress_meter(len(file_list), len(file_list))
    return data_object

def ensure_directory_exists(filepath):
    """Create directory path if it doesn't exist"""
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)

def console_input_parsing(argument_list):
    argument_list.pop(0) #Don't need "python"
    
    print(f"Arguments received: {argument_list}")
    
    # root_dir needs a trailing slash (i.e. /root/dir/)
    root_dir = ''
    if len(argument_list) == 0:
        print("No arguments provided! Please provide mod folder name.")
        sys.exit(1)
        
    #General case of modname/modname/common structure
    if os.path.isdir( './'+str(argument_list[0])+'/' ):
        root_dir = argument_list[0]
    #Case of modname/common
    elif ( os.path.basename(os.getcwd())==argument_list[0] ):
        root_dir = './'
    else:
        print('No folder named '+str(argument_list[0])+' exists; stopping execution')
        print(f"Current directory: {os.getcwd()}")
        print(f"Looking for: {os.path.abspath('./' + str(argument_list[0]))}")
        sys.exit(1)
    argument_list.pop(0) #Remove the root dir from the list
    
    print(f"Using root directory: {os.path.abspath(root_dir)}")
    
    #Get exclusions (if any)
    exclusion_list = []
    for item in argument_list:
        if item in acceptable_tiers:
            exclusion_list.append(item)
    exclusion_list = list(set(exclusion_list))
    
    print(f"Excluding tiers: {exclusion_list}")
    
    return root_dir, exclusion_list

def get_titles_to_keep(title_list,exclusion_list):
    print(f"\nProcessing {len(title_list)} total titles found")
    
    barony_list  = [item for item in title_list if item[0]=='b']
    county_list  = [item for item in title_list if item[0]=='c']
    duchy_list   = [item for item in title_list if item[0]=='d']
    kingdom_list = [item for item in title_list if item[0]=='k']
    empire_list  = [item for item in title_list if item[0]=='e']
    
    print(f"Found by tier:")
    print(f"  Baronies: {len(barony_list)}")
    print(f"  Counties: {len(county_list)}")
    print(f"  Duchies: {len(duchy_list)}")
    print(f"  Kingdoms: {len(kingdom_list)}")
    print(f"  Empires: {len(empire_list)}")
    
    #Catch obvious errors
    duchy_list  = [item for item in duchy_list if item != 'd_emblem']
    empire_list = [item for item in empire_list if item not in ['e_on_partition','e_names']]
    
    #Build new list without exclusions
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
    
    # Create base directories
    base_dir = './CK3_Color_Storage/CK3CS'
    
    #common/coat_of_arms/coat_of_arms/CK3CS_titles.txt
    filepath = f'{base_dir}/common/coat_of_arms/coat_of_arms/CK3CS_titles.txt'
    ensure_directory_exists(filepath)
    print(f"Writing to {filepath}")
    with open(filepath, 'w') as f:
        for title in titles_to_process:
            f.write('d_'+title+'_color = { pattern = "pattern_solid.dds" color1 = "white"  color2 = "white" }\n')
    
    #common/landed_titles/CK3CS_titles.txt
    filepath = f'{base_dir}/common/landed_titles/CK3CS_titles.txt'
    ensure_directory_exists(filepath)
    print(f"Writing to {filepath}")
    with open(filepath, 'w') as f:
        for title in titles_to_process:
            f.write('d_'+title+'_color = { definite_form = yes color ={0 0 0} can_create = { always = no } }\n')
    
    #localization/*/CK3CS_titles_l_*.yml
    for language in languages:
        filepath = f'{base_dir}/localization/{language}/CK3CS_titles_l_{language}.yml'
        ensure_directory_exists(filepath)
        print(f"Writing to {filepath}")
        with open(filepath, 'w') as f:
            f.write('l_'+language+':\n')
            for title in titles_to_process:
                f.write('d_'+title+'_color: ""\n')
    
    #common/on_action/000_CK3CS_titles.txt
    filepath = f'{base_dir}/common/on_action/CK3CS_titles.txt'
    ensure_directory_exists(filepath)
    print(f"Writing to {filepath}")
    with open(filepath, 'w') as f:
        f.write('#NB: prepended with 000 because this needs to fire off before things like tributaries are assigned\n')
        f.write('\n')
        f.write('on_game_start = {\n')
        f.write('\ton_actions = {\n')
        f.write('\t\tCK3CS_build_color_variable_refs\n')
        f.write('\t\tCK3CS_set_color_title_colors\n')
        f.write('\t}\n')
        f.write('}\n')
        f.write('\n')
        f.write('#Associate every title in question with a color storage title\n')
        f.write('CK3CS_build_color_variable_refs = {\n')
        f.write('\teffect = {\n')
        for title in titles_to_process:
            f.write('\t\ttitle:'+title+' = { set_variable = { name = color_storage value = title:d_'+title+'_color } }\n')
        f.write('\t}\n')
        f.write('}\n')
        f.write('\n')
        f.write('#Reset the actual color storage title\n')
        f.write('CK3CS_set_color_title_colors = {\n')
        f.write('\teffect = {\n')
        for title in titles_to_process:
            f.write('\t\ttitle:d_'+title+'_color = { set_color_from_title = title:'+title+' }\n')
        f.write('\t}\n')
        f.write('}\n')
        f.write('\n')

def generate_files(root_dir,exclusion_list,console_output=False):
    print(f"Current working directory: {os.getcwd()}")
    
    #Get the list of all items in the database requested
    if(console_output): print('Building Database')
    database_build = BuildItemDatabaseFromFolder()
    title_list = search_over_mod_structure(root_dir,'landed_titles',database_build,[],console_output)
    if(console_output): print('\n')
    
    #Split list by tiers
    title_list.sort()
    titles_to_process = get_titles_to_keep(title_list,exclusion_list)
    del title_list #Don't need these anymore...
    generate_output_files(titles_to_process)

if __name__ == '__main__':
    root_dir,exclusion_list = console_input_parsing(sys.argv)
    generate_files(root_dir,exclusion_list,True)