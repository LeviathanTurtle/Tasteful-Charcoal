
# 
# William Wadsworth
# 5.15.2025
# 

from dataclasses import dataclass
from dotenv import load_dotenv

import os


load_dotenv()
API_KEY = os.getenv("CURSEFORGE_API_KEY")


@dataclass
class ModData:
    name: str
    id: int
    versions: list[str]
    loaders: list[str]

