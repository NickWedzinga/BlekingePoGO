import asyncio
import logging
import logging.handlers
import time
from typing import List, Dict

import discord
from discord.ext import commands

from common import constants, instances
from sneaselcommands.leaderboards.leaderboard_controller import LeaderboardController
from sneaselcommands.leaderboards.views.leaderboard_buttons_view_first import LeaderboardButtonsViewFirst
from sneaselcommands.leaderboards.views.leaderboard_buttons_view_second import LeaderboardButtonsViewSecond
from utils.exception_wrapper import catch_with_logging


class SneaselBot(commands.Bot):
    def __init__(self, initial_extensions: List[str], intents: discord.Intents):
        super().__init__(command_prefix=commands.when_mentioned_or('?'), intents=intents, case_insensitive=True)
        self.initial_extensions = initial_extensions
        self.leaderboard_controllers: Dict[constants.Leaderboards, LeaderboardController] = {}
        for leaderboard in constants.Leaderboards:
            self.leaderboard_controllers[leaderboard] = LeaderboardController(leaderboard.value)

    # load initial extensions prior to startup
    async def setup_hook(self) -> None:
        logging.info("Starting...")
        logging.info(f"Discord version: {discord.__version__}")
        for extension in self.initial_extensions:
            await self.load_extension(extension)

        # If we're in development environment, immediately load new application commands
        if instances.DATABASE_CONNECTION and "weavile" in instances.DATABASE_CONNECTION:
            guild = discord.Object(435139939206955018)
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            logging.info(f'Synced application commands: {[app.name for app in synced]}')

        # Load Leaderboard views for persistence
        self.add_view(LeaderboardButtonsViewFirst(self.leaderboard_controllers))
        self.add_view(LeaderboardButtonsViewSecond(self.leaderboard_controllers))

    async def on_ready(self):
        logging.info('Logged in as: ' + self.user.display_name)
        logging.info("Ready for action")
        logging.info('----------')
        await self.change_presence(activity=discord.Game(name='Pokémon GO'))
        await self.start_leaderboard()

    async def start_leaderboard(self):
        await self.wait_until_ready()
        leaderboard_channel = discord.utils.get(self.get_all_channels(), name='leaderboards')
        # Only send new buttons if the channel is empty
        logs = [log async for log in leaderboard_channel.history()]
        if len(logs) > 0:
            return

        await leaderboard_channel.send(view=LeaderboardButtonsViewFirst(self.leaderboard_controllers))
        await leaderboard_channel.send(view=LeaderboardButtonsViewSecond(self.leaderboard_controllers))


async def main():
    with open("textfiles/apitoken.txt", "r") as apiFile:
        api_token = apiFile.read()
    with open("textfiles/database_info.txt", "r") as apiFile:
        instances.DATABASE_CONNECTION = apiFile.read()

    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.getLogger('discord').setLevel(logging.ERROR)

    intents = discord.Intents.default()
    intents.members = True
    intents.reactions = True
    intents.message_content = True

    async with SneaselBot(constants.COMMAND_EXTENSIONS, intents) as bot:
        await bot.start(api_token)


for retry in range(5):
    asyncio.run(catch_with_logging(main, "MAIN LOOP"))
    time.sleep(5)
