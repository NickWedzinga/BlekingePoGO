import discord
from discord.ext import commands


async def load_extensions(bot: commands.Bot):
    """Load all the extensions"""
    print("Loading extensions..")
    initial_extensions = ['utils.global_error_manager', 'testing.integration.integration_manager',
                          'sneaselcommands.list',
                          'sneaselcommands.support', 'sneaselcommands.leaderboards', 'sneaselcommands.ranks',
                          'sneaselcommands.configure', 'sneaselcommands.dex', 'sneaselcommands.refresh',
                          'sneaselcommands.raids.raid', 'sneaselcommands.raids.close', 'sneaselcommands.raids.update',
                          'sneaselcommands.raids.status', 'sneaselcommands.raids.raids', 'sneaselcommands.rolewindow',
                          'sneaselcommands.trainercode', 'sneaselcommands.roles.sub', 'sneaselcommands.roles.roles',
                          'sneaselcommands.achievements']
    for extension in initial_extensions:
        await bot.load_extension(extension)


def get_bot():
    intents = discord.Intents.default()
    intents.members = True
    intents.reactions = True
    intents.message_content = True
    return SneaselBot(command_prefix="?", intents=intents, case_insensitive=True)


class SneaselBot(commands.Bot):
    async def setup_hook(self):
        print("Starting..")
        print(f"Discord version: {discord.__version__}")
        await load_extensions(self)

    async def on_ready(self):
        print('Logged in as: ' + self.user.display_name)
        print("Ready for action")
        print('------')
        await self.change_presence(activity=discord.Game(name='Pokémon GO'))


"""Create instance of bot to run"""
bot = get_bot()
