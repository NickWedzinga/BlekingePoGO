import discord
from discord.ext import commands

from common import tables
from utils.database_connector import execute_statement, create_select_query
from utils.exception_wrapper import pm_dev_error
import requests


# TODO: put pull time in database,
#  if pull time seems wrong Sneasel needs to be able to pull hourly
#  Sneasel should pull 8 different 8 hourly periods for 8 hours and ask each hour if that pull is correct
#  If a pull is wrong then that pull time is excluded until one pull time remains

#  TODO: EXAMPLE
#   Default pull time is 06:00, which translates to 06:00 -> 14:00 -> 22:00
#   Niantic changes pull time so Sneasel starts reporting incorrect weather
#   Admin can trigger pull time checker at any time, let's say for example it's 09:45
#   Sneasel will then pull 8 hours periods at 10:00, 11:00, 12:00, 13:00, 14:00, 15:00, 16:00 and 17:00
#   Each hour Sneasel will ask admin to verify if weather is correct
#   So for example at 13:00 Sneasel will ask:
#   React with all weather types that are INCORRECT: A(10:00): Cloudy, B(11:00): Partly Cloudy, C(12:00): Cloudy, D(13:00): Snowy
#   The weather in Pokémon GO is cloudy so pull times for 11:00 and 13:00 are excluded since they were incorrect
#   Sneasel will thus remove any pull times that get reactions
#   Sneasel keeps asking for all living pull times every hour until only one remains which must be the correct pull time
class Weatherman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="weather")
    async def weather(self, ctx, name):
        """
        TODO
        """
        # TODO:
        #   1. Check if local text forecast exists for today's date and time, if not instant pull 8 hours just to have some weather, note that it's inaccurate
        #   2. Update cached forecast from common.instances, should be an dict[pull time: str, Forecast] of max size 8, since we can have 8 pull times
        #   3. Fetch pull times from database and use scheduler to schedule updates to Accuweather according to pull times, could be multiple pull times
        #   4. Every time we pull replace the common.instances of that pull time, like common.instances[pull_time] = new Forecast
        #   5.



    @weather.error
    async def weather_on_error(self, _, error):
        """Catches errors with weather command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="weather")


def setup(bot):
    bot.add_cog(Weatherman(bot))
