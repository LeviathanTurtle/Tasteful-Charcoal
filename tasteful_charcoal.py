# 
# William Wadsworth
# 5.15.2025
# 

from constants import API_KEY, ModData
from excel import write_to_spreadsheet

import requests
import config


def get_mods() -> requests.Response:
    """
    Queries the CurseForge API using the mods specified in the configuration file.
    
    Returns:
        Request: API response
    """
    
    headers = {
        "Accept": "application/json",
        "x-api-key": API_KEY
    }
    data = {
        "modIds": list(config.MODS_IN_QUESTION.values())
    }

    return requests.post("https://api.curseforge.com/v1/mods", headers=headers, json=data)


def translate_modloader(modloader: int | None) -> str:
    """
    Translates the modloader name from CurseForge's numerical classification.
    
    Params:
        modloader (int | None): a CurseForge modloader number 
    
    Returns:
        str: modloader in text form
    """
    
    match (modloader):
        case 0: return "Any"
        case 1: return "Forge"
        case 2: return "Cauldron"
        case 3: return "LiteLoader"
        case 4: return "Fabric"
        case 5: return "Quilt"
        case 6: return "NeoForge"
        case _: return "Unknown" 
    

def get_mod_info() -> list[ModData] | None:
    """
    Builds the list of mod data.
    
    Returns:
        list[ModData]: list of each mod data object
    """
    
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
        
        return mod_data
    else:
        print("Error fetching data:", response.status_code)
        print(response.text)
        return None


if __name__ == "__main__":
    mod_data = get_mod_info()
    # sort alphabetically by name
    mod_data.sort(key=lambda mod: mod.name.lower())
    
    #for mod in mod_data:
    #    print(f"{mod.name}:")
    #    for i in range(len(mod.vers_load)):
    #        if "unknown" not in mod.vers_load[i].lower():
    #            print(f"{i+1}. {mod.vers_load[i]}")
    
    write_to_spreadsheet(mod_data)