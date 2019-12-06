import discord
from discord.ext import commands as discordcommands

# list of all cogs to add
# TODO: perhaps put this in a function? Will that allow import bot from Instance.py as it now does not load extensions every time?
initial_extensions = ['global_error_manager', 'testing.integration.integration_manager', 'sneaselcommands.information',
                      'sneaselcommands.support', 'sneaselcommands.leaderboards', 'sneaselcommands.ranks']

bot = discordcommands.Bot(command_prefix="?")
for extension in initial_extensions:
    bot.load_extension(extension)


def startup():
    print("Starting..")
    # Printing client info
    @bot.event
    async def on_ready():
        print('Logged in as: ' + bot.user.display_name)
        print("Ready for action")
        print('------')
        await bot.change_presence(activity=discord.Game(name='Pokémon GO'))
