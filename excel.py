
# 
# William Wadsworth
# 5.15.2025
# 

import pandas as pd
from constants import ModData
from collections import defaultdict
from xlsxwriter.utility import xl_rowcol_to_cell
from time import time

import config


def split_loader_version(entry: str) -> tuple:
    """Helper function to split a mod's loader and version."""
    
    parts = entry.split()
    if len(parts) == 2:
        return parts[0], parts[1] # (loader, version)
    return "Unknown", entry  # fallback if format is unexpected

def count_extra_versions(mod: ModData) -> int:
    """function def."""
    
    unique_versions = {split_loader_version(v)[1] for v in mod.vers_load}
    return max(len(unique_versions)-5, 0)

def get_unique_versions(mod: ModData) -> list:
    """Helper function that returns the five most recent, unique, supported game versions."""
    
    seen = set()
    unique = []
    for v in sorted(mod.vers_load, reverse=True):
        loader, version = split_loader_version(v)
        if version not in seen and loader != "Unknown":
            seen.add(version)
            unique.append(version)
        if len(unique) == 5:
            break
        
    # Pad with empty strings if fewer than 5
    return unique + [""] * (5-len(unique))

def write_to_spreadsheet(
    mods: list[ModData]
) -> None:
    """function def."""
    
    # overview page
    overview = pd.DataFrame({
        "mod name": [mod.name for mod in mods],
        "mod id": [mod.id for mod in mods],
        "lastest version 1": [get_unique_versions(mod)[0] for mod in mods],
        "lastest version 2": [get_unique_versions(mod)[1] for mod in mods],
        "lastest version 3": [get_unique_versions(mod)[2] for mod in mods],
        "lastest version 4": [get_unique_versions(mod)[3] for mod in mods],
        "lastest version 5": [get_unique_versions(mod)[4] for mod in mods],
        "...+x": [
            f"...+{count_extra_versions(mod)}" #if len(mod.vers_load) > 5 else "...+0"
            for mod in mods
        ],
        "modloaders": [
            ", ".join({split_loader_version(vers)[0] for vers in sorted(mod.vers_load,reverse=True) if split_loader_version(vers)[0] != "Unknown"})
            for mod in mods
        ],
        "unknowns": [
            ", ".join([v for v in mod.vers_load if split_loader_version(v)[0] == "Unknown"])
            for mod in mods
        ]
    })
    
    # Collect all game versions and loaders
    # 1. extract all loader-version pairs as tuples, e.g. ("Forge", "1.20.1")
    loader_version_pairs = {
        tuple(vers.split(maxsplit=1)) for mod in mods for vers in mod.vers_load #if " " in vers
    }
    # 2. group versions by loader for easier access, e.g. "Forge": ["1.19.2", "1.18.2", ...]
    versions_by_loader = defaultdict(set)
    for loader, version in loader_version_pairs:
        versions_by_loader[loader].add(version)
    # 3. sort the versions for each loader
    for loader in versions_by_loader:
        versions_by_loader[loader] = sorted(versions_by_loader[loader],reverse=True)
    # todo: remove unknowns
    
    # Create an Excel writer using xlsxwriter engine (not openpyxl)
    filename = f"{time()}.xlsx"
    with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
        overview.to_excel(writer, sheet_name="Overview", index=False)
        
        # update each modloader subsheet 
        # NOTE: WE MOVE FROM ONE SUBSHEET TO THE NEXT
        for loader, versions in versions_by_loader.items():
            # for each mod, check if it supports the current loader and keep if it does
            loader_mods = [mod for mod in mods if any(v.startswith(loader) for v in mod.vers_load)]
            # todo: sort backwards?

            # Build DataFrame columns: mod name, mod id, then all versions for this loader
            data = {
                "mod name": [mod.name for mod in loader_mods],
                "mod id": [mod.id for mod in loader_mods],
                #f"{version}": [] # todo: this?
            }
            # for each version supported by current loader, add column with empty strings
            for version in config.VERSIONS_TO_CHECK:
                data[version] = ["" for _ in loader_mods]
            # todo: is this necessary? (see above for potential alt)
            
            # convert dict to DataFrame for excel
            df = pd.DataFrame(data)
            df.to_excel(writer, sheet_name=loader.capitalize(), index=False)
            
            # NOW, we need to set the background color (cell formatting)
            # open the subsheet
            worksheet = writer.sheets[loader.capitalize()]
            workbook = writer.book

            # Define formats
            green_fmt = workbook.add_format({'bg_color': '#C6EFCE'})
            red_fmt = workbook.add_format({'bg_color': '#FFC7CE'})

            # Apply formatting to indicate if mod supports loader-version combo
            for row_idx, mod in enumerate(loader_mods, start=1): # start at 1 to skip header
                # for each mod, build set of supported game versions
                mod_loader_versions = {
                    vers.split(maxsplit=1)[1]
                    for vers in mod.vers_load if vers.startswith(loader)
                }
                # for each game version, set background accordingly
                for col_idx, version in enumerate(config.VERSIONS_TO_CHECK, start=2): # start at third column
                    cell = xl_rowcol_to_cell(row_idx, col_idx)
                    fmt = green_fmt if version in mod_loader_versions else red_fmt
                    worksheet.write(cell, "", fmt)

