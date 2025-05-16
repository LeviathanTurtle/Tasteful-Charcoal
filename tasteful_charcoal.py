# 
# William Wadsworth
# 5.15.2025
# todo: run setup.py before running?
# 

from typing import Optional, Literal

from config import MODS_IN_QUESTION
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

def get_mod_info(
    mod_dict: dict
) -> list[ModData]:
    """function def."""
    
    # make modlist of IDs
    mod_id_list = list(mod_dict.values())
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
    
    for mod_id in mod_id_list:
        url = f"https://api.curseforge.com/v1/mods/{mod_id}"
        #response = requests.post(url, headers=headers, json=payload)
        response = requests.get(url, headers=headers)
    
        if response.status_code == 200:
            data = response.json()["data"]
            
            versions = []
            loaders = []
            
            for file_index in data.get('latestFilesIndexes', []):
                #if not include_prerelease and file_index.get("releaseType", 1) != 1:  # 1 = Release
                #    continue

                versions.append(file_index["gameVersion"])
                # todo: that file index is not always present
                loaders.append(translate_modloader(file_index["modLoader"]))
                #loaders = translate_modloader(versions)
            
            mod_data.append(ModData(
                name=data["name"],
                id=data["id"],
                versions=versions,
                loaders=loaders
            ))
        else:
            print("Error fetching data:", response.status_code)
            print(response.text)
            return None
    
    return mod_data


def main():
    #print(API_KEY)
    
    # todo: include dependencies
    mod_data = get_mod_info(MODS_IN_QUESTION)
    
    for mod in mod_data:
        print(f"{mod}\n")
    
    #for mod_name, mod_id in MODS_IN_QUESTION.items():
    #    mod_info = get_mod_info(mod_id)
        
        #if mod_info:
        #    print(f"Supported versions and modloaders for '{mod_name}':")
        #    for version, modloader in mod_info:
        #        print(f"Minecraft {version} - {modloader}")
        #else:
        #    print(f"No supported versions or modloaders for '{mod_name}'")

if __name__ == "__main__":
    main()