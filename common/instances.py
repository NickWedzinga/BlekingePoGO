from typing import Dict
from sneasel_types.window import Window

# pokedex info
POKEDEX_FILE_PATH = "textfiles/pokedex.json"
POKEDEX_URL = "https://fight.pokebattler.com/pokemon"
SHINY_FILE_PATH = "textfiles/shiny.json"
SHINY_URL = "https://p337.info/pokemongo/pokedex/?show=shiny&hide=unreleased"

# weather info
WEATHER_FILE_PATH = "textfiles/weather.json"

POKEDEX = None
SPELLCHECKER = None
WEATHER = None

ROLEWINDOWS: Dict[int, Window] = {}

DATABASE_CONNECTION = None
