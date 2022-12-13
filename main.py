import asyncio
import time

from common import instances
from sneasel_bot import bot
from utils.exception_wrapper import catch_with_print

with open("textfiles/apitoken.txt", "r") as apiFile:
    apitoken = apiFile.read()
with open("textfiles/database_info.txt", "r") as apiFile:
    instances.DATABASE_CONNECTION = apiFile.read()


async def main():
    async with bot:
        await bot.start(apitoken)

for retry in range(5):
    asyncio.run(catch_with_print(main, "MAIN LOOP"))
    time.sleep(5)
