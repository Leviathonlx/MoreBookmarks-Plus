# Script for generating sprawler files

# Imports and file paths

from dataclasses import dataclass, field # To save on boilerplate
from itertools import product # To make iteration easy

input_filename = "sprawl_lists.txt" # Which file to read the data from (so that people who are scared of snakes don't run away)
output_asset_filename = "sprawl_main_assets.asset"
output_buildings_filename = "sprawl_graphical_backgrounds.txt"
# Remember to make your own has_sprawl_building scripted trigger!

### Templates: The stuff that will actually be written to each file after doing some choice substitutions.

asset_wrapper = """
pdxmesh = { name = "$NAME$" file = "$NAME$.mesh" }
entity = { name = $NAME$ pdxmesh = $NAME$ }
"""
subasset_wrapper = """
entity = {
	name = $NAME$
	#SUBASSETS#
	locator = { name = city_center position = { 0 0 0 } scale = 0.4 }
}
"""
subasset_entry = "attach = { root = $NAME$ }\n\t"
graphical_background_wrapper = """
$NAME$ = {
	is_graphical_background = yes
    #VARIANTS#
	is_enabled = {
		#TRIGGERS#
	}
}
"""
variant_entry = """
	asset = {
		type = entity
		name = $NAME$
        #VARIANT_REQUIREMENTS#
	}"""
trigger_entry = "has_sprawl_building = { BUILDING = $NAME$ }"
graphical_culture_wrapper = """
graphical_cultures = {}
"""
building_gfx = """_building_gfx"""
graphical_region_wrapper = """
graphical_regions = {$$}
"""
### Globals

global ENTITYLIST
ENTITYLIST = []
global ENTITYLISTS
ENTITYLISTS = []
global PRINTED_ENTITY_SET
PRINTED_ENTITY_SET = {}
global VARIANT_LIST
VARIANT_LIST = []

# Entity class
@dataclass(order=True)
class Entity:
    sort_index: int = field(init=False, repr=False) # Apparently ordering matters for using dataclass ordering, so this needs to be the first field even though it's not called in the initializer.

    name: str
    subassets: list = field(default_factory=list)
    use_variants: bool = True
    invariant_subassets: list = field(default_factory=list)

    def __post_init__(self):
        if "*" in self.name and len(self.subassets) == 1:
            self.use_variants = False
        self.name = clear_asterisk(self.name)
        self.name = self.name.strip('_').replace('__','_').strip('_') # Syntax sanity cleanup for people using insanely many categories
        self.sort_index = len(self.subassets)*100 + sum(map(len,self.subassets))
        self.invariant_subassets = [asset for asset in self.subassets if "*" in asset]
    def get_asset(self):
        # print(self)
        if len(self.subassets) == 1: return self.get_main_asset()
        return self.get_combo_asset()
    def get_main_asset(self):
        #if not self.use_variants: return asset_wrapper.replace('$NAME$',self.name}
        asset = ""
        for name in self.name_variants():
            if not self.use_variants: print(name)
            asset += asset_wrapper.replace('$NAME$',name)
        return asset
    def get_combo_asset(self):
        wrapper = f"# Start {self.name} and its variants"
        for variant in VARIANT_LIST:
            subwrapper = ""
            for subasset in self.subassets:
                if subasset in self.invariant_subassets:
                    #subwrapper = "\n\t".join([subasset_entry.replace('$NAME$',subasset) for subasset in self.subassets])
                    subwrapper += subasset_entry.replace('$NAME$',clear_asterisk(subasset))
                else:
                    subwrapper += subasset_entry.replace('$NAME$',subasset + variant.suffix)
            wrapper += subasset_wrapper.replace('#SUBASSETS#',subwrapper).replace('$NAME$',self.name + variant.suffix)
        return wrapper
    def get_trigger(self):
        return "\n\t\t".join([trigger_entry.replace('$NAME$',subasset) for subasset in self.subassets])
    def __repr__(self):
        return self.name
    def debug_print(self): # For easy printing some extra details in the desired format 
        print(
            f"""{self.name}: {self.subassets} ({self.sort_index})
            {self.get_trigger()}
            """
        )
    def name_variants(self):
        if not self.use_variants: return [self.name]
        return get_variants(self.name)
    def get_graphical_background(self):
        graphical_background = graphical_background_wrapper.replace('$NAME$',self.name).replace('#TRIGGERS#',self.get_trigger())
        graphical_background = graphical_background.replace("#VARIANTS#",self.get_background_variants())
        return graphical_background
    def get_background_variants(self):
        background_variants = ""
        for variant in VARIANT_LIST:
            background_variants += variant_entry.replace("$NAME$",self.name + variant.suffix).replace("#VARIANT_REQUIREMENTS#",variant.requirements)
        return background_variants

def uses_variants(x):
    return not "*" in x
def clear_asterisk(x):
    return x.replace("*","")
@dataclass
class Variant:
    culture: str = ""
    region: str = ""
    dlc: str = ""
    suffix: str = ""
    requirements: str = ""
    def __post_init__(self):
        if self.culture: self.requirements += f"graphical_cultures = {{{self.culture}{building_gfx}}}\n\t\t"
        if self.region: self.requirements += f"graphical_regions = {{{self.region}}}\n\t\t"
        if self.dlc: self.requirements += f"requires_dlc_flag = {self.dlc}"
        self.requirements = self.requirements.strip()
        global VARIANT_LIST
        VARIANT_LIST.append(self)
        if self.culture: self.suffix+= f"_{self.culture}"
        if self.region: self.suffix+= f"_{self.region}"
    def __repr__(self):
        return f"{self.culture} {self.region} {self.dlc}"

def get_variants(x: str):
    return [x + variant.suffix for variant in VARIANT_LIST]


def print_assets():
    with open(output_asset_filename,'w') as file:
        for entity in ENTITYLIST:
            file.write(entity.get_asset())

def print_graphical_backgrounds():
    with open(output_buildings_filename,'w',encoding = "utf-8-sig") as file:
        for entity in ENTITYLIST:
            line = entity.get_graphical_background()
            file.write(line)

def load_assets():
    with open(input_filename,'r') as file:
        for line in file.readlines():
            # print(line)
            line = line.split("#")[0].strip()
            if not line or line[0] == "#": pass
            else:
                key, entries = line.split(':')
                # print(key)
                # print(entries)
                if key.lower() == "variants": # Loads variants
                    for entry in entries.split():
                        culture = ""
                        region = ""
                        dlc = ""
                        parameters = entry.split("&")
                        # print(parameters)
                        for parameter in parameters:
                            datapair = parameter.split("=")
                            if datapair[0].strip()=="culture": culture = datapair[1].strip().replace(building_gfx,"") # In case someone added the suffix by mistake
                            elif datapair[0].strip()=="region": region = datapair[1].strip()
                            elif datapair[0].strip()=="dlc": dlc = datapair[1].strip()
                            else: culture = datapair[1]
                        Variant(culture,region,dlc)
                else: # Loads entity names
                    entries = list(entries.split())
                    entries.append("") # Add a default blank option for the ability to choose an empty asset
                    ENTITYLISTS.append(entries)
    clean = lambda i: [x for x in i if x] # Get rid of any completely null entries
    combinations = product(*ENTITYLISTS) # Build all possible combinations of elements from each list
    combinations = [('_'.join(clean(i)),clean(i)) for i in combinations if clean(i)] # Build strings from combinations
    global ENTITYLIST
    ENTITYLIST = [Entity(*i) for i in combinations] # Populate entity list with Entity dataclasses.
    list.sort(ENTITYLIST, reverse=True) # Because the declaration order of graphical backgrounds matters.

def main():
    Variant() # Make the default variant
    load_assets()
    print_assets()
    print_graphical_backgrounds()

if __name__ == "__main__":
    main()