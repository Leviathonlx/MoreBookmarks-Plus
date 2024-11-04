import sys
import os
import re
from collections import Counter

import glob

from math import floor

'''
Searches your CK3 mod landed titles to generate the various colour storage items in the folder CK3CS.
The items in CK3CS/ folder

NOTE:
This code uses regular expressions and thus if you're code isn't properly matched, it'll fail to find
titles. Alternatively, it is possible that non-titles will be caught, so parse the results with some care.

All titles should match one of the following patterns:
    ([e|k|d|c|b]_[A-z_\-]+)[ ]*=[ ]*\{
In natural language:
    Starts with one of e,k,d,c,b, followed by A-Z,a-z, underscores, or hyphens and is followed by one
        of these patterns:  " = {","= {"," ={","={"
    And remove the trailing pattern

A few known failures:
* e_on_partition
* d_emblem
* e_names

Meant to be launched from your top level git folder with structure

i.e., ./MOD/, where

./MOD/
    |- MOD/
        |- common/
        |- events/
        |- gfx/
        |- gui/
        |- localization
        |- music/

is the expected sort of underlying structure. Will need some tweaks to run under other directory structures.

Arg 1 is mod folder name

Additional arguments specify which title tiers for which the code *will not* generate colour storage
dummy titles. Acceptable inputs are:

    baronies
    counties
    duchies
    kingdoms
    empires

No entry, therefore, means all titles will have colour storage dummy titles generated.

Example run command: "python3 .CK3_Color_Storage/generate_submod_files.py MY_MOD_NAME baronies counties"

The above will check your mod structure and will create dummy titles for duchies, kingdoms, and empires
Duplicates will have no effect, so additional arguments should be considered a set
'''

''' License: BSD Zero Clause
Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN
AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
OF THIS SOFTWARE.
'''

#TODO:
# Remove WtWSMS *in toto*
# Remove Color_Submod_Files, except for top folder

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
        item_list = []
        file_text = []
        with open(file,'r') as f:
            file_text = ''.join(f.readlines())
        return re.findall('([e|k|d|c|b]_[A-z_\-]+)[ ]*=[ ]*\{',file_text)

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

'''
search_over_mod_structure
Arguments:
  root_dir: Directory Root Dir
  file_keyword: file keyword to search for in the file name (e.g., either the item type or '.+' 
    (everything in the database)
  file_action_object: class building the data object (a dictionary or a list, depending). Must have method action
    which takes a file name as an argument
  database: Which database to search; default is "common/", "events/", and "history/" top level folders
  check_localization: if the *.yml files should be searched; default is False
Desc:
  Finds a list of text files based on comparison of dir_name to item_type and does file_action
  (making a list of items to search over OR a dictionary of database instance counts)
  
  Note 1:
  Why wouldn't we add localization files? Because removal of other database items might void localization
  items. So stuff that's used in only in localization (like 'clan_government_levies_max_possible') should
  be an exclusion instead
'''
def search_over_mod_structure(root_dir,file_keyword,file_action_object,data_object,console_output,\
                              database=['common'],\
                              check_localization=False):
    if ( len(database)== 0): RuntimeError("Did not provide a database to search in search_over_mod_structure(); failing")
    
    database_items = '('
    for item in database:
        database_items += item
        database_items += '|'
    database_items = database_items[:-1] #Remove the last '|'
    database_items += ')'
    
    file_list = [y for x in os.walk(root_dir) for y in glob.glob(os.path.join(x[0], '*.txt'))]
    
    if ( check_localization ):
        file_list.extend([y for x in os.walk(root_dir) for y in glob.glob(os.path.join(x[0], '*.yml'))])
    for file,index in zip(file_list,range(len(file_list))):
        if ( console_output ): task_progress_meter(index,len(file_list))
        if ( re.search(file_keyword,file) and \
             compare_file_path_with_item(file,database_items) ):
            if ( isinstance(data_object,list) ):
                data_object.extend(file_action_object.action(file))
            else:
                data_object = file_action_object.action(file)
    if ( console_output ): task_progress_meter(len(file_list),len(file_list))
    return data_object

#argument_list should be sys.argv
def console_input_parsing(argument_list):
    argument_list.pop(0) #Don't need "python"
    
    # root_dir needs a trailing slash (i.e. /root/dir/)
    root_dir = ''
    #General case of modname/modname/common structure
    if os.path.isdir( './'+str(argument_list[0])+'/' ):
        root_dir = argument_list[0]
    #Case of modname/common
    elif ( os.path.basename(os.getcwd())==argument_list[0] ):
        root_dir = './'
    else:
        print('No folder named '+str(argument_list[0])+' exists; stopping execution')
        sys.exit(1)
    argument_list.pop(0) #Remove the root dir from the list
    #Get exclusions (if any)
    exclusion_list = []
    for item in argument_list:
        if item in acceptable_tiers:
            exclusion_list.append(item)
    exclusion_list = list(set(exclusion_list))
    return root_dir, exclusion_list

def get_titles_to_keep(title_list,exclusion_list):
    barony_list  = [item for item in title_list if item[0]=='b']
    county_list  = [item for item in title_list if item[0]=='c']
    duchy_list   = [item for item in title_list if item[0]=='d']
    kingdom_list = [item for item in title_list if item[0]=='k']
    empire_list  = [item for item in title_list if item[0]=='e']
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
    return titles_to_process

def generate_output_files(titles_to_process):
    languages = ['english','french','german','korean','russian','simp_chinese','spanish']
    
    #common/coat_of_arms/coat_of_arms/CK3CS_titles.txt
    with open('./CK3_Color_Storage/CK3CS/common/coat_of_arms/coat_of_arms/CK3CS_titles.txt','w') as f:
        for title in titles_to_process:
            f.write('d_'+title+'_color = { pattern = "pattern_solid.dds" color1 = "white"  color2 = "white" }\n')
    #common/landed_titles/CK3CS_titles.txt
    with open('./CK3_Color_Storage/CK3CS/common/landed_titles/CK3CS_titles.txt','w') as f:
        for title in titles_to_process:
            f.write('d_'+title+'_color = { definite_form = yes color ={0 0 0} can_create = { always = no } }\n')
    #localization/*/CK3CS_titles_l_*.yml
    for language in languages:
        with open('./CK3_Color_Storage/CK3CS/localization/'+language+'/CK3CS_titles_l_'+language+'.yml','w') as f:
            f.write('l_'+language+':\n')
            for title in titles_to_process:
                f.write('d_'+title+'_color: ""\n')
    #common/on_action/000_CK3CS_titles.txt
    with open('./CK3_Color_Storage/CK3CS/common/on_action/CK3CS_titles.txt','w') as f:
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
        f.write('\tCK3CS_build_color_variable_refs = {\n')
        f.write('\teffect = {\n')
        for title in titles_to_process:
            f.write('\t\ttitle:'+title+' = { set_variable = { name = color_storage value = title:d_'+title+'_color } }\n')
        f.write('\t}\n')
        f.write('}\n')
        f.write('\n')
        f.write('#Reset the actual color storage title\n')
        f.write('\tCK3CS_set_color_title_colors = {\n')
        f.write('\teffect = {\n')
        for title in titles_to_process:
            f.write('\t\ttitle:d_'+title+'_color = { set_color_from_title = title:'+title+' }\n')
        f.write('\t}\n')
        f.write('}\n')
        f.write('\n')

##### Main Code

def generate_files(root_dir,exclusion_list,console_output=False):
    print(os.getcwd())
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
