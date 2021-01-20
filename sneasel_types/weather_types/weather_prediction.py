from common import constants


class WeatherPrediction:
    """Parses the icon_phrase and windy information into a predicted weather"""
    def __init__(self, icon_phrase: str, wind_speed: int, gust_speed: int):
        self.weather_phrase = None
        self.emoji = None

        self.__parse_phrase_as_weather_prediction(icon_phrase, wind_speed, gust_speed)

    # TODO: https://github.com/thornleaf/pgo-weatherbot
    def __parse_phrase_as_weather_prediction(self, icon_phrase: str, wind_speed: int, gust_speed: int):
        is_windy = wind_speed > 24 or gust_speed > 35

        if icon_phrase in constants.SUNNY_WEATHERS:
            self.weather_phrase = "Sunny"
            self.emoji = ":sunny:"
        elif icon_phrase in constants.PARTLY_CLOUDY_WEATHERS:
            self.weather_phrase = "Partly Cloudy"
            self.emoji = ":partly_sunny:"
        elif icon_phrase in constants.CLOUDY_WEATHERS:
            self.weather_phrase = "Cloudy"
            self.emoji = ":cloud:"
        elif icon_phrase in constants.FOGGY_WEATHERS:
            self.weather_phrase = "Foggy"
            self.emoji = ":fog:"
        elif icon_phrase in constants.RAINY_WEATHERS:
            self.weather_phrase = "Rainy"
            self.emoji = ":cloud_rain:"
        elif icon_phrase in constants.SNOWY_WEATHERS:
            self.weather_phrase = "Snowy"
            self.emoji = ":cloud_snow:"
        elif icon_phrase in constants.CLEAR_WEATHERS:
            self.weather_phrase = "Clear"
            self.emoji = ":crescent_moon:"

        if icon_phrase in constants.WINDYABLE_WEATHERS and is_windy:
            self.weather_phrase = "Windy"
            self.emoji = ":cloud_tornado:"

        if self.weather_phrase is None:
            self.weather_phrase = icon_phrase
            self.emoji = ":grey_question:"
