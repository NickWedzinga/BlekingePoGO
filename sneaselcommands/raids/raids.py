from datetime import datetime, timedelta

import discord
import discord.ext.commands.context
from discord.ext import commands

from common import constants, tables
from sneaselcommands.raids.raid import valid_time_hhmm
from utils.channel_wrapper import find_first_embed_in_channel
from utils.database_connector import execute_statement
from utils.exception_wrapper import pm_dev_error


def _sort_raid_dict(active_raids_dict: list) -> list:
    hatched_first_raid_dict = []
    for raid in active_raids_dict:
        if raid.get("hatch_time") == "Hatched!":
            hatched_first_raid_dict.insert(0, raid)
        else:
            hatched_first_raid_dict.append(raid)
    return hatched_first_raid_dict


def _create_embed(ctx, active_raids_dict: list, max_field_count: int = 24):
    """Creates an embed listing all active raids, max of 24 listings"""
    embed = discord.Embed(title=f"Active raids",
                          color=0xff9900,
                          description="Visit the raid channels below to join the discussion",
                          timestamp=datetime.utcnow())

    if not active_raids_dict:
        embed.description = "There are currently no active raids reported"

    for index, raid in enumerate(_sort_raid_dict(active_raids_dict)):
        pokemon = raid.get("pokemon")
        gym = raid.get("gym")
        channel = discord.utils.get(ctx.guild.channels, id=raid.get("channel_id"))

        maybe_valid_hatch = valid_time_hhmm(raid.get("hatch_time"))
        hatch_time = f"Hatched, despawns at {'{:%H:%M}'.format(maybe_valid_hatch + timedelta(minutes=45))}" \
            if maybe_valid_hatch is not None and maybe_valid_hatch.time() < datetime.now().time() \
            else raid.get("hatch_time")

        if index < max_field_count and channel is not None and pokemon is not None and gym is not None:
            embed.add_field(
                name=f"...",
                value=f"Pokémon: {pokemon}\nGym: {gym}\nHatch time: {hatch_time}\nChannel: {channel.mention}\n",
                inline=False)
        elif index == max_field_count:
            break

    if len(embed.fields) == max_field_count:
        embed.set_footer(text="Too many active raids to list all of them",
                         icon_url="https://vignette.wikia.nocookie.net/pokemongo/images/5/55/Emblem_Raid.png")
    else:
        embed.set_footer(text="These are all the currently active raids",
                         icon_url="https://vignette.wikia.nocookie.net/pokemongo/images/5/55/Emblem_Raid.png")
    return embed


class Raids(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role("Admin")
    @commands.command(name="raids", hidden=True)
    async def raids(self, ctx):
        """
        Lists all currently active raids

        Usage: ?raids
        """
        await ctx.send(f"[?raid, ?raids] commands are temporarily disabled {ctx.author.mention}")
        return

        # active_raids_dict = execute_statement(
        #     statement=f"SELECT * from {tables.ACTIVE_RAID_CHANNEL_OWNERS} ORDER BY hatch_time"
        # ).all(as_dict=True)
        #
        # embed = _create_embed(ctx, active_raids_dict)
        #
        # raids_channel = discord.utils.get(ctx.guild.channels, name=constants.RAID_ACTIVES_CHANNEL)
        # if raids_channel is None:
        #     await pm_dev_error(self.bot, "Can't find the raids channel to post list of active raids", "raids")
        #     return
        #
        # embed_message = await find_first_embed_in_channel(self.bot, raids_channel, "raids listing", should_pm=False)
        # if embed_message is None:
        #     await raids_channel.send(embed=embed)
        # else:
        #     await embed_message.edit(embed=embed)

    @raids.error
    async def raids_on_error(self, _, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="raid/Raids")


async def setup(bot):
    await bot.add_cog(Raids(bot))
