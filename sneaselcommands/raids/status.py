from discord.ext import commands

from utils.channel_wrapper import find_embed_in_channel
from utils.exception_wrapper import pm_dev_error
from utils.global_error_manager import validate_active_raid_and_user


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="status")
    @validate_active_raid_and_user()
    async def status(self, ctx):
        """
        Usage: ?status

        Resends the raid information.
        These status images are merely copies of the original.
        If any changes are made to the original, the copies will not be updated.
        """
        embed_message = await find_embed_in_channel(self.bot, ctx.channel, "Raid / status")
        embed = embed_message.embeds[0]
        embed.title = embed.title + " (COPY)"
        await ctx.send(embed=embed)

    @status.error
    async def status_on_error(self, _, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="Status")


def setup(bot):
    bot.add_cog(Status(bot))
