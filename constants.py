
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
    """
    Object to store a mod's relevant queried data.
    
    Attributes:
        name (str): mod name
        id (int): mod ID
        vers_load (list[int]): list of compatible versions
    """
    
    name: str
    id: int
    #dependency: bool # todo: also lib mod flag?
    vers_load: list[str]

