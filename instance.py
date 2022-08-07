import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
bot = commands.Bot(command_prefix="?", intents=intents, case_insensitive=True)

initial_extensions = ['utils.global_error_manager', 'testing.integration.integration_manager', 'sneaselcommands.list',
                      'sneaselcommands.support', 'sneaselcommands.leaderboards', 'sneaselcommands.ranks',
                      'sneaselcommands.configure', 'sneaselcommands.dex', 'sneaselcommands.refresh',
                      'sneaselcommands.raids.raid', 'sneaselcommands.raids.close', 'sneaselcommands.raids.update',
                      'sneaselcommands.raids.status', 'sneaselcommands.raids.raids', 'sneaselcommands.rolewindow',
                      'sneaselcommands.trainercode', 'sneaselcommands.roles.sub', 'sneaselcommands.roles.roles',
                      'sneaselcommands.achievements']
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
