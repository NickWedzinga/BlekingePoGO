import json
from typing import Dict

import requests

from common import tables, instances
from sneasel_types.weather_types.forecast import Forecast
from sneasel_types.weather_types.hourly_forecast import HourlyForecast
from utils.database_connector import execute_statement, create_select_query


def __fetch_weather_forecast() -> dict:
    """Fetches a 12 hour weather forecast"""
    apitoken = execute_statement(create_select_query(
        table_name=tables.STATIC_DATA,
        where_key="name",
        where_value="'AccuWeather API Token'"
    )).all(as_dict=True)
    assert (len(apitoken) == 1)

    weather_url = f"http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/306839?apikey={apitoken[0].get('data')}&details=true&metric=true"
    json_data = requests.get(weather_url)
    # TODO: should either create new txtfile for each pull time or append to same file
    with open(instances.WEATHER_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(json_data.json(), file, ensure_ascii=False, indent=4)
    return json.load(open(instances.WEATHER_FILE_PATH))


# TODO should raw_dict be dict or List[dict]
def parse_forecast(raw_dict: dict) -> Forecast:
    """Parses the raw forecast dict as Forecast object"""
    hour_split_dict: Dict[str, HourlyForecast] = {}

    # Iterate first 8 hours
    for hour in raw_dict[:8]:
        hour_split_dict[hour.get("DateTime")] = HourlyForecast(hour)
    return Forecast(hour_split_dict)




def up_to_date() -> bool:
    """
    Checks if the local textfile is up-to-date.
    If it's up-to-date then we update the cache, if not we pull new info
    """
    # TODO: parse textfile(s?) and see if date and time are in future still or stale
    return True # TODO


def update_weather_cache():
    """Updates the weather cache for the next 8 hours"""
    if not up_to_date():
        raw_forecast = __fetch_weather_forecast()
    else:
        raw_forecast = # TODO parse the textfile(s?), maybe up_to_date() could do this already since it iterates the file(s)
    parse_forecast(raw_forecast)
    # TODO: should also schedule pulls for all pull-times repeating every 8 hours
