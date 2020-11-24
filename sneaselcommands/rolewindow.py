from collections import defaultdict
from datetime import datetime

import discord
from discord import utils
from discord.ext import commands

from common import tables, instances
from sneasel_types.window import Window
from utils.channel_wrapper import find_embed_in_channel_from_message_id
from utils.database_connector import create_insert_query, execute_statements, execute_statement, create_select_query, \
    create_delete_query
from utils.exception_wrapper import channel_send_error, catch_with_pm
from utils.message_wrapper import delete_message


def _extract_emoji_and_roles(*args):
    """
    Extracts the role window name, channel, emojis and roles from the input data.
    Returns the name, channel_id and a dict with emoji_name -> role_name.
    """
    rolewindow_emojis = args[0::2]
    rolewindow_roles = args[1::2]
    assert (len(rolewindow_emojis) == len(rolewindow_roles))
    assert (len(rolewindow_emojis) > 0)

    rolewindow_dict = dict(zip(rolewindow_emojis, rolewindow_roles))
    return rolewindow_dict


def _add_rolewindow_to_database_and_cache(message_id: int, unique: bool, name: str, channel_id: str,
                                          emoji_to_role_dict: dict):
    query_list = []
    for key, value in emoji_to_role_dict.items():
        query_list.append(create_insert_query(
            table_name=tables.ROLEWINDOW,
            keys="(name, channel_id, message_id, unique_roles, emoji, role)",
            values=f"('{name}', '{channel_id}', {message_id}, {unique}, '{key}', '{value}')"))
    execute_statements(query_list)

    instances.ROLEWINDOWS[message_id] = Window(message_id, unique, emoji_to_role_dict)


async def _verify_emojis_and_roles(ctx, rolewindow_dict: dict):
    """
    Fetches all the emojis and roles from the guild and verifies that they exist, then adds the new rolewindow to
    the existing dictionary in common.instances.

    Returns the verified dict for this specific rolewindow.
    """
    verified_dict = {}
    for key, value in rolewindow_dict.items():
        verified_emoji = discord.utils.get(ctx.guild.emojis, name=key)
        assert (verified_emoji is not None)

        verified_role = discord.utils.get(ctx.guild.roles, name=value)
        assert (verified_role is not None)

        verified_dict[verified_emoji] = verified_role
    return verified_dict


def _create_rolewindow(ctx, rolewindow_name: str, rolewindow_dict: dict, support_channel):
    embed = discord.Embed(title=f"{rolewindow_name.capitalize()} - Please react below",
                          color=0xff9900,
                          description=f"Feel free to ask for help in {support_channel.mention} if anything is unclear.",
                          timestamp=datetime.utcnow())
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text=f"Please react below with the emoji that matches the role you want access to.")

    for key, value in rolewindow_dict.items():
        embed.add_field(
            name="\u200b",
            value=f"{key} {value.mention}")
    return embed


def _create_dictionary_from_database():
    role_window_rows = execute_statement(create_select_query(table_name=tables.ROLEWINDOW)).all(as_dict=True)
    # split list of dicts into seperate list of dicts grouped by message_id
    result = defaultdict(list)
    for role_window_row in role_window_rows:
        result[role_window_row["message_id"]].append(role_window_row)

    # iterate the split list
    # create Window object for each rolewindow from database
    # add "message_id -> Window" to instances.ROLEWINDOWS cache
    for message_id, role_dicts in result.items():
        unique_roles = role_dicts[0].get("unique_roles")
        emoji_to_role_dict = {}
        for role_dict in role_dicts:
            emoji = role_dict.get("emoji")
            role = role_dict.get("role")
            emoji_to_role_dict[emoji] = role
        instances.ROLEWINDOWS[message_id] = Window(message_id, unique_roles, emoji_to_role_dict)
    return instances.ROLEWINDOWS


class RoleWindow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.init_dictionary())

    async def init_dictionary(self):
        await self.bot.wait_until_ready()
        _create_dictionary_from_database()

    @commands.command(name="rolewindow", hidden=True)
    @commands.is_owner()
    async def rolewindow(self, ctx, name: str, channel_id: int, unique: bool, *args):
        """
        ?rolewindow one_worded_name channel_id unique_roles emoji_name1 role_name1 emoji_name2 role_name2...
        Usage: ?rolewindow teams 749612839332872283 true valor valor mystic mystic instinct instinct
        """
        rolewindow_dict = _extract_emoji_and_roles(*args)

        try:
            embed_channel = utils.get(ctx.guild.channels, id=channel_id)
            support_channel = utils.get(ctx.guild.channels, name="support")
        except:
            await ctx.send(f"Could not find a channel with id: [{channel_id}] or a channel with the name support")
            return

        verified_dict = await _verify_emojis_and_roles(
            ctx=ctx,
            rolewindow_dict=rolewindow_dict)

        embed = _create_rolewindow(
            ctx=ctx,
            rolewindow_name=name,
            rolewindow_dict=verified_dict,
            support_channel=support_channel)

        message = await embed_channel.send(embed=embed)

        _add_rolewindow_to_database_and_cache(
            message_id=message.id,
            unique=unique,
            name=name,
            channel_id=str(channel_id),
            emoji_to_role_dict=rolewindow_dict)

        for emoji in verified_dict.keys():
            await message.add_reaction(emoji)

    @rolewindow.error
    async def rolewindow_on_error(self, ctx, error):
        await channel_send_error(ctx=ctx, error_message=error, source="Role Window")

    @commands.command(name="remove_rolewindow", hidden=True)
    @commands.is_owner()
    async def remove_rolewindow(self, ctx, channel_id: int, message_id: int):
        """
        ?remove_rolewindow channel_id message_id
        Usage: ?remove_rolewindow 129836198723619263 780456757335687239
        """
        execute_statement(create_delete_query(
            table_name=tables.ROLEWINDOW,
            where_key="message_id",
            where_value=f"{message_id}"
        ))

        del instances.ROLEWINDOWS[message_id]

        # delete the correct embed
        embed_message = await find_embed_in_channel_from_message_id(utils.get(ctx.guild.channels, id=channel_id), message_id)
        if embed_message is not None:
            await delete_message(bot=self.bot, message=embed_message)
        else:
            await ctx.send(f"Message with id [{message_id}] can't be found in channel with id [{channel_id}]")

    @remove_rolewindow.error
    async def rolewindow_on_error(self, ctx, error):
        await channel_send_error(ctx=ctx, error_message=error, source="Remove Role Window")

    # TODO: could use a refactor
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        rolewindow_info = instances.ROLEWINDOWS.get(payload.message_id)  # check if message is a rolewindow message
        if payload.guild_id is not None and rolewindow_info is not None and not payload.member.bot:
            guild = self.bot.get_guild(payload.guild_id)
            member = payload.member

            role_name = rolewindow_info.emoji_to_role_dict.get(payload.emoji.name)
            role_to_add = utils.get(guild.roles, name=role_name)

            if role_to_add is not None:
                # checks if this role window is one role max and if member already has one of the rolls
                previous_unique_roll = [role for role in member.roles if role.name in rolewindow_info.emoji_to_role_dict.values()]
                if rolewindow_info.unique_roles and previous_unique_roll:
                    await member.remove_roles(previous_unique_roll[0])

                    channel = utils.get(guild.channels, id=payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)
                    emoji_name_to_remove = next((emoji for emoji, role in rolewindow_info.emoji_to_role_dict.items() if role == previous_unique_roll[0].name), None)
                    if emoji_name_to_remove is not None:
                        emoji = utils.get(guild.emojis, name=emoji_name_to_remove)
                        await message.remove_reaction(emoji, member)
                await catch_with_pm(self.bot, member.add_roles, "Raw Reaction Add", role_to_add)
            else:
                channel = utils.get(guild.channels, id=payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                await message.remove_reaction(payload.emoji, member)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        rolewindow_info = instances.ROLEWINDOWS.get(payload.message_id)  # check if message is a rolewindow message
        if payload.guild_id is not None and rolewindow_info is not None:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if not member.bot:
                role_name = rolewindow_info.emoji_to_role_dict.get(payload.emoji.name)
                role_to_remove = utils.get(guild.roles, name=role_name)
                if role_to_remove in member.roles:
                    await member.remove_roles(role_to_remove)


def setup(bot):
    bot.add_cog(RoleWindow(bot))
