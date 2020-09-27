from datetime import datetime, timedelta

import discord
import schedule
from discord.ext import commands

import common
import common_instances
from sneaselcommands.dex import create_no_matches_info_message, find_corrected_pokemon, \
    create_found_correction_info_message
from sneaselcommands.raids.raid import create_raid_embed
from sneaselcommands.raids.utils.raid_embeds import update_time_in_embed
from sneaselcommands.raids.utils.raid_scheduler import update_raids_channel, schedule_delete_channel_at, \
    schedule_edit_embed, schedule_reminding_task
from sneaselcommands.raids.utils.raid_stats import update_pokemon_in_stats
from utils.channel_wrapper import find_embed_in_channel
from utils.database_connector import execute_statement, create_delete_query, create_select_query, create_update_query
from utils.exception_wrapper import pm_dev_error
from utils.global_error_manager import validate_active_raid_and_user
from utils.time_wrapper import valid_time_mm, valid_time_hhmm, format_as_hhmm


def _clear_previous_jobs(channel_id):
    """Deletes all rows related to this raid and cancels all jobs"""
    execute_statement(create_delete_query(
        table_name=common.SCHEDULE_RAID,
        where_key="channel_id",
        where_value=channel_id))

    schedule.clear(f"delete{channel_id}")
    schedule.clear(f"edit_embed{channel_id}")
    schedule.clear(f"send{channel_id}")


async def _start_new_jobs(bot, ctx, channel, hatch_time: datetime, minutes_until_despawn: int = 60):
    """Insert new jobs in database and starts new scheduled jobs"""
    schedule_reminding_task(bot, ctx, channel, f"This channel will close in 1 minute", format_as_hhmm(hatch_time + timedelta(minutes=minutes_until_despawn - 1)), "daily")
    schedule_delete_channel_at(bot, ctx, channel, format_as_hhmm(hatch_time + timedelta(minutes=minutes_until_despawn)))
    if hatch_time.time() > datetime.now().time():
        schedule_edit_embed(bot, ctx, channel, format_as_hhmm(hatch_time))
    return await update_time_in_embed(bot=bot, channel=channel, at_time=format_as_hhmm(hatch_time))


async def _maybe_update_channel_name(ctx, channel, new_channel_name: str, field_name_to_update: str, field_new_value: str):
    """Updates the channel name if it has not been updated within the last 10 minutes"""
    raid_channel_info = execute_statement(create_select_query(
        table_name=common.ACTIVE_RAID_CHANNEL_OWNERS,
        where_key="channel_id",
        where_value=channel.id
    )).all(as_dict=True)[0]

    last_updated = raid_channel_info.get("last_updated")

    if last_updated == "empty" or valid_time_hhmm(last_updated).time() < (datetime.now() - timedelta(minutes=10)).time():
        execute_statement(create_update_query(
            table_name=common.ACTIVE_RAID_CHANNEL_OWNERS,
            column="last_updated",
            new_value=f"'{format_as_hhmm(datetime.now())}'",
            where_key="channel_id",
            where_value=channel.id
        ))
        await channel.edit(name=new_channel_name)
        await ctx.send(f"{field_name_to_update.title()} updated to: {field_new_value.title()}")
    else:
        await ctx.send(f"{field_name_to_update.title()} updated to: {field_new_value.title()}, but I cannot "
                       f"change the channel's name again due to Discord rate limits.")


class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @validate_active_raid_and_user()
    async def update(self, ctx):
        """
        ?update pokemon <pokemon name>
        Example: ?update pokemon mewtwo

        ?update gym <gym name>
        Example: ?update gym adam och eva

        ?update hatch <hatch time>
        Example: ?update hatch 15:09

        ?update despawn <minutes to despawn>
        Example: ?update despawn 32

        ?status, to ask Sneasel to re-send the raid information
        ?close, to close the raid channel early
        """
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid update command, options:\n"
                           "update pokemon <pokemon name>\n"
                           "update gym <gym name>\n"
                           "update hatch <hatch time in HH:MM>\n"
                           "update despawn <despawn in minutes>")

    @update.error
    async def update_on_error(self, _, error):
        """Catches errors with update base command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="update")

    @update.command(aliases=["pokémon", "Pokémon", "Pokemon"])
    @validate_active_raid_and_user()
    async def pokemon(self, ctx, *pokemon_name, channel_id=None):
        """
        ?update pokemon <pokemon name>
        Usage: ?update pokemon mewtwo

        Update a raid's Pokémon.
        Can only be used by the reporter and admins/moderators.
        """
        channel = ctx.channel if channel_id is None else discord.utils.get(ctx.guild.channels, id=channel_id)

        pokemon_name_concat = " ".join(pokemon_name).capitalize()
        pokemon = common_instances.POKEDEX.lookup(pokemon_name_concat)

        if pokemon is None and pokemon_name_concat.upper() not in common.RAID_EGG_TYPES:
            maybe_found_pokemon = await find_corrected_pokemon(ctx, list(pokemon_name))
            if maybe_found_pokemon is not None:
                await ctx.send(create_found_correction_info_message(ctx, maybe_found_pokemon.name, " ".join(pokemon_name)))
                pokemon_name_concat = maybe_found_pokemon.name
            else:
                await ctx.send(create_no_matches_info_message(ctx=ctx, pokemon_name=pokemon_name_concat))

        embed_message = await find_embed_in_channel(self.bot, channel, source="Raid: Update pokemon")
        if embed_message is None:
            return

        old_embed_description = embed_message.embeds[0].description.split("\n")
        old_hatch_or_despawn_time = old_embed_description[2]
        if "Despawn" in old_hatch_or_despawn_time:
            hatch_time = format_as_hhmm(valid_time_hhmm(old_hatch_or_despawn_time.replace("Despawn time: ", "")) - timedelta(minutes=45))
        else:
            hatch_time = old_hatch_or_despawn_time.replace("Hatch time: ", "")
        embed = create_raid_embed(
            ctx=ctx,
            reporter=old_embed_description[0].replace("Reporter: ", ""),
            pokemon_name=pokemon_name_concat,
            gym_name=old_embed_description[1].replace("Gym: ", ""),
            hatch_time=hatch_time
        )
        await embed_message.edit(embed=embed)

        channel_name = channel.name.split("_")
        if len(channel_name) > 2:
            del channel_name[1]
            channel_name.insert(1, pokemon_name_concat.lower())
        else:
            del channel_name[0]
            channel_name.insert(0, pokemon_name_concat.lower())

        await _maybe_update_channel_name(
            ctx=ctx,
            channel=channel,
            new_channel_name="_".join(channel_name),
            field_name_to_update="Pokémon",
            field_new_value=pokemon_name_concat)

        execute_statement(create_update_query(
            table_name=common.ACTIVE_RAID_CHANNEL_OWNERS,
            column="pokemon",
            new_value=f"'{pokemon_name_concat}'",
            where_key="channel_id",
            where_value=channel.id
        ))
        update_pokemon_in_stats(
            channel_id=channel.id,
            column="pokemon",
            new_value=f"'{pokemon_name_concat}'"
        )
        await update_raids_channel(self.bot, ctx)

    @pokemon.error
    async def pokemon_on_error(self, _, error):
        """Catches errors with update pokemon command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="update pokemon")

    @update.command(aliases=["Hatch"])
    @validate_active_raid_and_user()
    async def hatch(self, ctx, time, channel_id=None):
        """
        Update a raid's hatch time.
        ?update hatch <hatch time>
        Usage: ?update hatch 18:15

        Can only be used by the reporter and admins/moderators.
        """
        channel = ctx.channel if channel_id is None else discord.utils.get(ctx.guild.channels, id=channel_id)

        if channel.name[-5:] == "train":
            await ctx.send(f"This is a raid-train channel, discuss the times instead {ctx.author.mention}")
            return

        maybe_valid_time = valid_time_hhmm(time)
        if maybe_valid_time is None:
            await ctx.send(f"{time} does not follow the HH:MM format {ctx.author.mention}")
            return

        if maybe_valid_time.time() < (datetime.now() - timedelta(minutes=45)).time():
            await ctx.send(f"{time} is longer than 45 minutes ago, should have already despawned {ctx.author.mention}")
            return

        if time.replace(":", "") == channel.name[:4]:
            await ctx.send(f"{time} is already the current hatch time {ctx.author.mention}")
            return

        _clear_previous_jobs(channel.id)
        await _start_new_jobs(self.bot, ctx, channel, maybe_valid_time)

        if valid_time_hhmm(f"{channel.name[:2]}:{channel.name[2:4]}") is None:
            channel_name = f"{time}_{channel.name}"
        else:
            channel_name = f"{time}_{channel.name[5:]}"

        await _maybe_update_channel_name(
            ctx=ctx,
            channel=channel,
            new_channel_name=channel_name,
            field_name_to_update="Hatch time",
            field_new_value=time)

        execute_statement(create_update_query(
            table_name=common.ACTIVE_RAID_CHANNEL_OWNERS,
            column="hatch_time",
            new_value=f"'{time}'",
            where_key="channel_id",
            where_value=channel.id
        ))
        update_pokemon_in_stats(
            channel_id=channel.id,
            column="hatch_time",
            new_value=f"'{time}'"
        )
        await update_raids_channel(self.bot, ctx)

    @hatch.error
    async def hatch_on_error(self, _, error):
        """Catches errors with update hatch command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="update hatch")

    @update.command(aliases=["Despawn"])
    @validate_active_raid_and_user()
    async def despawn(self, ctx, minutes_until_despawn, channel_id=None):
        """
        Update a raid's despawn time.
        ?update despawn <minutes to despawn>
        Usage: ?update despawn 33

        Can only be used by the reporter and admins/moderators.
        """
        channel = ctx.channel if channel_id is None else discord.utils.get(ctx.guild.channels, id=channel_id)

        if channel.name[-5:] == "train":
            await ctx.send(f"This is a raid-train channel, discuss the times instead {ctx.author.mention}")
            return

        maybe_valid_time = valid_time_mm(minutes_until_despawn)
        if maybe_valid_time is None:
            await ctx.send(f"{minutes_until_despawn} contains other characters than just minutes {ctx.author.mention}")
            return

        if maybe_valid_time.minute > 45:
            await ctx.send(f"A raid should not be alive for {minutes_until_despawn} minutes, if it hasn't hatched yet use *?update hatch HH:MM*")
            return

        _clear_previous_jobs(channel.id)
        await _start_new_jobs(self.bot, ctx, channel, datetime.now() - timedelta(minutes=45-maybe_valid_time.minute))

        time = format_as_hhmm(datetime.now() - timedelta(minutes=45 - maybe_valid_time.minute))
        if valid_time_hhmm(f"{channel.name[:2]}:{channel.name[2:4]}") is None:
            channel_name = f"{time}_{channel.name}"
        else:
            channel_name = f"{time}_{channel.name[5:]}"

        await _maybe_update_channel_name(
            ctx=ctx,
            channel=channel,
            new_channel_name=channel_name,
            field_name_to_update="Hatch time",
            field_new_value=time)

        execute_statement(create_update_query(
            table_name=common.ACTIVE_RAID_CHANNEL_OWNERS,
            column="hatch_time",
            new_value=f"'{time}'",
            where_key="channel_id",
            where_value=channel.id
        ))
        update_pokemon_in_stats(
            channel_id=channel.id,
            column="hatch_time",
            new_value=f"'{time}'"
        )
        await update_raids_channel(self.bot, ctx)

    @despawn.error
    async def despawn_on_error(self, _, error):
        """Catches errors with update despawn command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="update despawn")

    @update.command(aliases=["Gym"])
    @validate_active_raid_and_user()
    async def gym(self, ctx, *gym, channel_id=None):
        """
        Update a raid's gym.
        ?update gym <gym name>
        Usage: ?update gym klockstapeln

        Can only be used by the reporter and admins/moderators.
        """
        channel = ctx.channel if channel_id is None else discord.utils.get(ctx.guild.channels, id=channel_id)
        embed_message = await find_embed_in_channel(self.bot, channel, source="Raid: Update gym")
        if embed_message is None:
            return

        gym = " ".join(gym).title()
        embed = embed_message.embeds[0]
        old_embed_description = embed.description.split("\n")
        old_reporter_info = old_embed_description[0]
        old_gym_info = old_embed_description[1]
        old_hatch_info = old_embed_description[2]
        embed.description = f"{old_reporter_info}\n{old_gym_info[:5]} {gym}\n{old_hatch_info}"
        await embed_message.edit(embed=embed)

        channel_name = channel.name.split("_")
        if len(channel_name) > 2:
            del channel_name[2]
            channel_name.insert(2, gym.lower())
        else:
            del channel_name[1]
            channel_name.insert(1, gym.lower())

        if "train" not in embed.description.lower():
            await _maybe_update_channel_name(
                ctx=ctx,
                channel=channel,
                new_channel_name="_".join(channel_name),
                field_name_to_update="Gym",
                field_new_value=gym)
        else:
            await ctx.send(f"Gym updated to: {gym}")

        execute_statement(create_update_query(
            table_name=common.ACTIVE_RAID_CHANNEL_OWNERS,
            column="gym",
            new_value=f"'{gym}'",
            where_key="channel_id",
            where_value=channel.id
        ))
        update_pokemon_in_stats(
            channel_id=channel.id,
            column="gym",
            new_value=f"'{gym}'"
        )
        await update_raids_channel(self.bot, ctx)

    @gym.error
    async def gym_on_error(self, _, error):
        """Catches errors with update gym command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="update gym")


def setup(bot):
    bot.add_cog(Update(bot))
