import discord
from discord.ext import commands

initial_extensions = ['utils.global_error_manager', 'testing.integration.integration_manager', 'sneaselcommands.list',
                      'sneaselcommands.support', 'sneaselcommands.leaderboards', 'sneaselcommands.ranks',
                      'sneaselcommands.configure', 'sneaselcommands.dex', 'sneaselcommands.refresh',
                      'sneaselcommands.raids.raid', 'sneaselcommands.raids.close', 'sneaselcommands.raids.update',
                      'sneaselcommands.raids.status', 'sneaselcommands.raids.raids']

bot = commands.Bot(command_prefix="?", case_insensitive=True)
for extension in initial_extensions:
    bot.load_extension(extension)


def startup():
    print("Starting..")
    print(f"Discord version: {discord.__version__}")
    @bot.event
    async def on_ready():
        print('Logged in as: ' + bot.user.display_name)
        print("Ready for action")
        print('------')
        await bot.change_presence(activity=discord.Game(name='Pokémon GO'))
