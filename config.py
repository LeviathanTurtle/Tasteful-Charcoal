
# 
# William Wadsworth
# 5.15.2025
# 

# collection of mods to check (BE SURE TO INCLUDE DEPENDENCIES)
MODS_IN_QUESTION: dict[str,int] = {
    #"mod_name": mod_id,
    "cave dweller reimagined": 921557,
    "the spineclaw": 1179481,
    "face of horror": 1240824,
    "zombie awareness": 237754,
    "true herobrine": 914926,
    "the mimicer": 970277,
    "sophisticated backpacks": 422301,
    "emi": 580555,
    "emi: enchants": 1036393,
    "emi: loot": 681783,
    "emi: ores": 974009,
    "emi: create schematics": 940673,
    "not enough animations": 433760,
    "distant horizons": 508933,
    "just enough items": 238222,
    "corpse": 316582,
    "jade": 324717,
    "jade: addons": 583345,
    "item highlighter": 521590,
    "skin layers 3d": 521480,
    "auditory": 636199,
    "appleskin": 248787,
    "betterf3": 401648,
    "clumps": 256717,
    "clickable advancements": 511733,
    "creeper overhaul": 561625,
    "cull leaves": 423254,
    "cursor mod": 278476,
    "drip sounds": 390986,
    "dynamic crosshair": 623800,
    "dynamic fps": 335493,
    "dynamic view": 366140,
    "entity model features": 844662,
    "entity texture features": 568563,
    "more vanilla weapons": 410999,
    "entity culling": 448233,
    "falling tree": 349559,
    "fancy block particles - renewed": 937011,
    "immediatelyfast": 686911,
    "item borders": 513769,
    "legendary tooltips": 532127,
    "modernfix": 790626,
    "more mob variants": 695107,
    "mouse tweaks": 60089,
    "neruina - ticking entity fixer": 851046,
    "no chat reports": 634062,
    "noisium": 951546,
    "not enough crashes": 442354,
    "not enough recipe book (nerb)": 738663,
    "ore excavation": 250898,
    "particular": 793109,
    "patchouli": 306770,
    "polymorph": 388800,
    "polytone": 958094,
    "presence footsteps": 433068,
    "quark": 243121,
    "quark oddities": 301051,
    "separated leaves": 905482,
    "server performance - smooth chunk save": 582327,
    "smooth swapping": 513689,
    "soul fire'd": 662413,
    "sound physics remastered": 535489,
    "spark": 361579,
    "supplementaries": 412082,
    "tectonic": 686836,
    "the box of horrors": 408707,
    "visuality: reforged": 704256,
    "better than mending": 264738,
    "explosive enhancement: reforged": 1036246,
    "enhanced horror experience": 1162688,
    "the anomaly": 1043571,
    "schizo dweller": 1169037,
    
    "awesome dungeon": 531320,
    "awesome dungeon: ocean": 556490,
    "explorify - dungeons & structures": 698309,
    "integrated api": 817709,
    "integrated dunegons and structures": 605375,
}

# set to true if you want to include non-release versions (NON-FUNCTIONAL)
include_prereleases: bool = False

# collection of game versions to check
VERSIONS_TO_CHECK: list[str] = [
    #"version",
    "1.21.1",
    "1.20.1",
    "1.19.2",
]

# collection of mod loaders you want to use
MODLOADERS_TO_CHECK: list[str] = [
    #"loader",
    "forge",
    "fabric",
    "neoforge"
]
