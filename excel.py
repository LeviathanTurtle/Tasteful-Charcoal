
# 
# William Wadsworth
# 5.15.2025
# 

import pandas as pd
from constants import ModData
from xlsxwriter.utility import xl_rowcol_to_cell
from time import time


#class ExcelHandler:
#    """class def."""
#    
#    def __init__(self,
#        
#    ):
#        pass
    
    #def add_mod_data(
    #    
    #):
    #    """function def."""
    #    
    #    pass

def write_to_spreadsheet(
    mods: list[ModData]
) -> None:
    """function def."""
    
    # overview page
    overview = pd.DataFrame({
        "mod name": [mod.name for mod in mods],
        "mod id": [mod.id for mod in mods],
        "versions": [mod.versions[:5] for mod in mods], # needs to be only first 5
        "...+x": [f"...+{max(len(mod.versions)-5, 0)}" if len(mod.versions) > 5 else "" for mod in mods],
        "modloaders": [", ".join(mod.loaders) for mod in mods],
        "unknowns": [] # todo: this
    })
    
    # Collect all game versions and loaders
    all_versions = sorted({v for mod in mods for v in mod.versions})
    all_loaders = sorted({loader for mod in mods for loader in mod.loaders})

    # Create an Excel writer using openpyxl engine
    with pd.ExcelWriter(f"{time()}.xlsx", engine="xlsxwriter") as writer:
        overview.to_excel(writer, sheet_name="Overview", index=False)
        
        # Write sheet for each mod loader
        for loader in all_loaders:
            # Filter mods that support this loader
            loader_mods = [mod for mod in mods if loader in mod.loaders]

            # Build DataFrame: rows = mods, columns = game versions
            data = {
                "mod name": [mod.name for mod in loader_mods],
                "mod id": [mod.id for mod in loader_mods],
            }
            for version in all_versions:
                data[version] = [
                    "" for _ in loader_mods
                ]
            df = pd.DataFrame(data)

            # Write sheet
            df.to_excel(writer, sheet_name=loader.capitalize(), index=False)
            worksheet = writer.sheets[loader.capitalize()]
            workbook = writer.book

            # Define formats
            green_fmt = workbook.add_format({'bg_color': '#C6EFCE'}) # Excel green
            red_fmt = workbook.add_format({'bg_color': '#FFC7CE'})   # Excel red

            # Apply formatting to cells
            for row_idx, mod in enumerate(loader_mods, start=1):  # Skip header (row 0)
                for col_idx, version in enumerate(all_versions, start=2):  # Columns start at 2 (after name/id)
                    cell = xl_rowcol_to_cell(row_idx, col_idx)
                    is_supported = version in mod.versions
                    fmt = green_fmt if is_supported else red_fmt
                    worksheet.write(cell, "", fmt)

