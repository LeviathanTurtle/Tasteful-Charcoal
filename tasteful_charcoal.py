# 
# William Wadsworth
# 5.15.2025
# todo: run setup.py before running?
# 

from typing import Optional, Literal

from config import MODS_IN_QUESTION, include_prereleases
from constants import API_KEY
from constants import ModData
from excel import write_to_spreadsheet

import requests



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

def get_mod_info() -> list[ModData]:
    """function def."""
    
    # make modlist of IDs
    mod_id_list = list(MODS_IN_QUESTION.values())
    #print(mod_id_list)
    
    headers = {
        #"Content-Type": "application/json",
        "Accept": "application/json",
        "x-api-key": API_KEY
    }
    #payload = {
    #    "modIds": modlist
    #}
    
    mod_data = []
    
    # for each mod ID
    for mod_id in mod_id_list:
        # query the API
        url = f"https://api.curseforge.com/v1/mods/{mod_id}"
        #response = requests.post(url, headers=headers, json=payload)
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            # extract data
            data = response.json()["data"]
            
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
                    # todo: INCLUDED_MODLOADERS check goes literally right here
                    versions_and_loaders.append(f"{modloader} {game_version}")
                except KeyError:
                    # todo: figure out a better way of handling this, not all unknowns are alphas
                    versions_and_loaders.append(f"Unknown {game_version}")
            
            # 2. extract dependencies
            # todo: this
            
            mod_data.append(ModData(
                name=data["name"],
                id=data["id"],
                vers_load=versions_and_loaders
            ))
        else:
            print("Error fetching data:", response.status_code)
            print(response.text)
            return None
    
    return mod_data


def main():
    #print(API_KEY)
    
    mod_data = get_mod_info()
    
    for mod in mod_data:
        print(f"\n{mod.name}:")

        for i in range(len(mod.vers_load)):
            if "unknown" not in mod.vers_load[i].lower():
                print(f"{i+1}. {mod.vers_load[i]}")
    
    print("\nUnknowns:")
    for mod in mod_data:
        for i in range(len(mod.vers_load)):
            if "unknown" in mod.vers_load[i].lower():
                print(f"{i+1}. {mod.vers_load[i]}")
    
    write_to_spreadsheet(mod_data)


if __name__ == "__main__":
    main()