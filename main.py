import asyncio
import logging
import logging.handlers
import time
from typing import List

import discord
from discord.ext import commands

from common import constants, instances
from utils.exception_wrapper import catch_with_logging


class SneaselBot(commands.Bot):
    def __init__(self, initial_extensions: List[str], intents: discord.Intents):
        super().__init__(command_prefix='?', intents=intents, case_insensitive=True)
        self.initial_extensions = initial_extensions

    # load initial extensions prior to startup
    async def setup_hook(self) -> None:
        logging.info("Starting...")
        logging.info(f"Discord version: {discord.__version__}")
        for extension in self.initial_extensions:
            await self.load_extension(extension)

    async def on_ready(self):
        logging.info('Logged in as: ' + self.user.display_name)
        logging.info("Ready for action")
        logging.info('----------')
        await self.change_presence(activity=discord.Game(name='Pokémon GO'))


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
