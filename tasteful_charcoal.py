# 
# William Wadsworth
# 5.15.2025
# todo: run setup.py before running?
# 

from typing import Optional, Literal
from constants import API_KEY, ModData
from excel import write_to_spreadsheet

import requests
import config


def get_mod(mod_id: int):
    """function def."""
    
    headers = {
        #"Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": API_KEY
    }
    
    url = f"https://api.curseforge.com/v1/mods/{mod_id}"
    return requests.get(url, headers=headers)

def get_mods():
    """function def."""
    
    headers = {
        #"Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": API_KEY
    }
    data = {
        "modIds": list(config.MODS_IN_QUESTION.values())
    }

    url = "https://api.curseforge.com/v1/mods"
    return requests.post(url, headers=headers, json=data)

def translate_modloader(modloader: int | None) -> str:
    """function def."""
    
    match (modloader):
        case 0: return "Any"
        case 1: return "Forge"
        case 2: return "Cauldron"
        case 3: return "LiteLoader"
        case 4: return "Fabric"
        case 5: return "Quilt"
        case 6: return "NeoForge"
        case _: return "Unknown"

def extract_dependency(dependency_id: int):
    """function def."""
    
    # 
    response = get_mod(dependency_id)
    data = response.json()["data"]
    
    # 
    

def get_mod_info() -> list[ModData]:
    """function def."""
    
    response = get_mods()
    
    mod_data = []
    
    if response.status_code == 200:
        # extract data
        mods_data = response.json()["data"]
        
        for data in mods_data:
            versions_and_loaders = []
            
            # 1. extract data from latestFilesIndexes
            # use this one because we want the most recent of that game version
            for file_index in data.get('latestFilesIndexes', []):
                # 1: release, 2: beta, 3: alpha
                #if not include_prereleases and file_index.get("releaseType", 1) != 1:
                #    continue

                game_version = file_index['gameVersion']
                
                try:
                    modloader = translate_modloader(file_index["modLoader"])
                    
                    # filter out ones the user does not want to check
                    if modloader.lower() in config.MODLOADERS_TO_CHECK:# and game_version in config.VERSIONS_TO_CHECK:
                        versions_and_loaders.append(f"{modloader} {game_version}")
                except KeyError:
                    # todo: figure out a better way of handling this, not all unknowns are alphas
                    #if game_version in config.VERSIONS_TO_CHECK:
                    versions_and_loaders.append(f"Unknown {game_version}")
            
            # 2. extract dependencies
            #file_index = data.get('latestFiles', [])
            #for _ in range(len(file_index["dependencies"])):
            #    dependency = extract_dependency(file_index["dependencies"].modId)
            #    mod_data.append(dependency)
            
            mod_data.append(ModData(
                name=data["name"],
                id=data["id"],
                vers_load=versions_and_loaders
            ))
            
            # verify mod names
            #if mod_name != data["name"].lower():
            #    print(f"Warning: name mismatch detected (provided: {mod_name}, actual: {data['name']})")
            #    # todo: maybe something more than just a warning msg?
        
        return mod_data
    else:
        print("Error fetching data:", response.status_code)
        print(response.text)
        return None


def main():
    mod_data = get_mod_info()
    # sort alphabetically by name
    mod_data.sort(key=lambda mod: mod.name.lower())
    
    #for mod in mod_data:
    #    print(f"{mod.name}:")
    #    for i in range(len(mod.vers_load)):
    #        if "unknown" not in mod.vers_load[i].lower():
    #            print(f"{i+1}. {mod.vers_load[i]}")
    
    write_to_spreadsheet(mod_data)


if __name__ == "__main__":
    main()