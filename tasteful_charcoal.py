# 
# William Wadsworth
# 5.15.2025
# todo: run setup.py before running?
# 

from typing import Optional, Literal

from config import MODS_IN_QUESTION, include_prereleases
from constants import API_KEY
from constants import ModData
#from excel import write_to_spreadsheet

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

def translate_modloader_version(gameVersions: list[str]) -> list[str]:
    """function def."""
    
    loaders = set()
    for version in gameVersions:
        v = version.lower()
        if "forge" in v:
            loaders.add("Forge")
        elif "cauldron" in v:
            loaders.add("Cauldron")
        elif "liteloader" in v:
            loaders.add("LiteLoader")
        elif "fabric" in v:
            loaders.add("Fabric")
        elif "quilt" in v:
            loaders.add("Quilt")
        elif "neoforge" in v:
            loaders.add("NeoForge")
    return list(loaders)

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
            #print(data)
            
            versions = []
            loaders = []
            
            # extract data from latestFilesIndexes
            # use this one because we want the most recent of that game version
            for file_index in data.get('latestFilesIndexes', []):
                # 1: release, 2: beta, 3: alpha
                #if not include_prereleases and file_index.get("releaseType", 1) != 1:
                #    continue

                versions.append(file_index["gameVersion"])
                #print(file_index["modLoader"])

                try:
                    loaders.append(translate_modloader(file_index["modLoader"]))
                except KeyError:
                    print(f"Error checking loader version due to missing modLoader attribute")
                    loaders.append("Unknown")
                    # todo: figure out a better way of handling this, not all unknowns are alphas
            
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
    mod_data = get_mod_info()
    
    for mod in mod_data:
        print(f"{mod.name}:")
        #print(f"Versions: {mod.versions}")
        #print(f"Loaders: {mod.loaders}")
        for i in range(len(mod.versions)):
            print(f"{i+1}. {mod.loaders[i]} {mod.versions[i]}")
    
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