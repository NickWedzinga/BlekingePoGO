import discord
from discord.ext import commands as discordcommands


# list of all cogs to add
initial_extensions = ['commands.test', 'commands.list']

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
