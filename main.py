import time

import instance
from common import instances
from utils.exception_wrapper import catch_with_print

instance.startup()

with open("textfiles/apitoken.txt", "r") as apiFile:
    apitoken = apiFile.read()
with open("textfiles/database_info.txt", "r") as apiFile:
    instances.DATABASE_CONNECTION = apiFile.read()

for retry in range(5):
    instance.bot.loop.run_until_complete(catch_with_print(instance.bot.start, "MAIN LOOP", apitoken))
    time.sleep(5)
