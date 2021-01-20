from sneasel_types.weather_types.weather_prediction import WeatherPrediction


class HourlyForecast:
    """Extracts relevant information from an hourly forecast"""
    def __init__(self, forecast_dict: dict):
        self.forecast_dict = forecast_dict

        self.predicted_weather = None

        self.icon_phrase = None
        self.daylight = None
        self.temperature = None
        self.feel_temperature = None

        # updates this hour's forecast´s values
        self.__parse_dict_as_forecast()

    def __parse_dict_as_forecast(self):
        self.icon_phrase = self.forecast_dict.get("IconPhrase")
        self.daylight = self.forecast_dict.get("IsDaylight")
        self.temperature = self.forecast_dict.get("Temperature.Value")  # TODO: does this work?
        self.feel_temperature = self.forecast_dict.get("RealFeelTemperature.Value")  # TODO: does this work?

        self.predicted_weather = WeatherPrediction(self.icon_phrase)
