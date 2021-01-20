from typing import Dict, Optional

from sneasel_types.weather_types.hourly_forecast import HourlyForecast


class Forecast:
    """An 8 hour weather forecast"""
    def __init__(self, forecast_dict: Dict[str, HourlyForecast]):
        self.forecast_dict = forecast_dict

    def lookup(self, hour: str) -> Optional[HourlyForecast]:
        return self.forecast_dict.get(hour)
