from typing import Dict, Optional


class Extras:
    def __init__(self, extras_dict: Optional[Dict[str, str]] = None):
        self.extras_dict = extras_dict
        self.release_date = None
        self.shiny_date = None

        self.__set_dates()

    def __set_dates(self):
        if self.extras_dict is None:
            return
        release = self.extras_dict.get("RELD")
        shiny = self.extras_dict.get("SHD")

        self.release_date = None if release == "" else release[:-2] + "20" + release[-2:]
        self.shiny_date = None if shiny == "" else shiny[:-2] + "20" + shiny[-2:]

