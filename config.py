
# 
# William Wadsworth
# 

# collection of mods to check
# "mod_name": mod_id,
MODS_IN_QUESTION: dict[str,int] = {
    "create": 328085,
    "just enough items": 238222,
    "mouse tweaks": 60089,
    "appleskin": 248787,
    "jade": 324717,
    "waystones": 245755,
    "enchantment descriptions": 250419,
    "sophisticated backpacks": 422301,
}

# set to true if you want to include non-release versions
include_prereleases: bool = False

# collection of game versions to check
VERSIONS_TO_CHECK: list[str] = [
    "1.21.1",
    "1.20.1",
]
