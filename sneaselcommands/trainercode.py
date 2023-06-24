"""Trainer code command Cog"""
from typing import Union

import discord
from discord.ext import commands

from common import tables
from utils.database_connector import execute_statement, create_select_query, create_upsert_query, create_delete_query
from utils.exception_wrapper import pm_dev_error


async def remove_trainercode(ctx, maybe_user):
    """
    Removes the trainer code of the message author
    """
    if len(maybe_user) > 1:
        db_key = "name"
        db_value = maybe_user[1] if not isinstance(maybe_user[1], discord.User) else maybe_user[1].display_name
    else:
        db_key = "user_id"
        db_value = str(ctx.author.id)

    maybe_found_code = execute_statement(create_select_query(
        table_name=tables.TRAINERCODES,
        where_key=db_key,
        where_value=f"'{db_value}'")).all(as_dict=True)

    if not maybe_found_code:
        await ctx.send(f"No registered trainer code found {ctx.author.mention}")
    else:
        if maybe_found_code[0].get("user_id") != str(ctx.author.id):
            await ctx.send(f"It looks like you're trying to remove a different user's code. "
                           f"If this is not the case, please contact an admin {ctx.author.mention}")
            raise AssertionError("User trying to remove another user's code")
        else:
            execute_statement(create_delete_query(
                table_name=tables.TRAINERCODES,
                where_key=db_key,
                where_value=f"'{db_value}'"))
            await ctx.send(f"Successfully removed your trainer code {ctx.author.mention}")


def format_trainer_code(raw_code: str):
    """Formats trainer codes like: 111122223333 -> 1111 2222 3333"""
    return ' '.join([raw_code[i:i + 4] for i in range(0, len(raw_code), 4)])


def build_code_string(trainer_codes: list) -> str:
    """Creates a new entry in the print for each registered code from the same user"""
    code_string = ""
    for trainer in trainer_codes:
        code_string += f"**{format_trainer_code(trainer.get('code'))}** is {trainer.get('name')}'s registered code\n"
    assert len(code_string) > 1
    return code_string


async def generic_or_specific_code(ctx, *code_or_user):
    """
    Checks if command was triggered from ?tc code, or ?tc code name
    In the case of ?tc code, checks if user has multiple registered codes, in that case respond they need to specify

    Returns the extracted name and code
    """
    # ?tc 111122223333
    if isinstance(code_or_user[0], str) and code_or_user[0].isnumeric():
        code = "".join(code_or_user)
        name = ctx.author.display_name

        # check if user has multiple codes registered, if so tell them they need to specify
        maybe_found_codes = execute_statement(create_select_query(
            table_name=tables.TRAINERCODES,
            where_key="user_id",
            where_value=ctx.author.id
        )).all(as_dict=True)
        if len(maybe_found_codes) > 1:
            await ctx.send(f"Multiple codes registered for your user {ctx.author.mention}. "
                           f"You need to specify which trainer code you want to replace with "
                           f"**?tc <name_to_change> {''.join(code_or_user)}**")
            raise AssertionError("Multiple codes, user needs to define which name to replace")
    # ?tc McMomo 111122223333
    else:
        code = "".join(code_or_user[1:])
        name = code_or_user[0] if isinstance(code_or_user[0], str) else code_or_user[0].display_name

        # check if user is trying to change a different user's code
        maybe_found_codes = execute_statement(create_select_query(
            table_name=tables.TRAINERCODES,
            where_key="name",
            where_value=f"'{name}'"
        )).all(as_dict=True)
        if maybe_found_codes and maybe_found_codes[0].get("user_id") != str(ctx.author.id):
            await ctx.send(f"It looks like you're trying to change a different user's code. "
                           f"If this is not the case, please contact an admin {ctx.author.mention}")
            raise AssertionError("User is trying to replace someone else's code")
    return name, code


class Trainercode(commands.Cog):
    """
    Allows members to register their trainer codes and look up other trainers' codes
    """

    def __init__(self, bot=None):
        self.bot = bot

    @commands.command(aliases=["tc"])
    async def trainercode(self, ctx, *code_or_user: Union[discord.User, str]):
        """
        Use this command to register your trainer code and look up other trainers' codes

        Usage:
        To register your trainer code use: ?trainercode 111122223333
        To print your own trainer code use: ?trainercode
        To print someone else's trainer code use: ?trainercode @McMomo

        To register multiple codes specify the name like: ?trainercode McMomo2 111122223333

        To remove your trainer code use: ?trainercode remove

        Instead of ?trainercode you can also use ?tc
        """
        # User is registering trainer code, hit by:
        # - ?tc 111122223333
        # - ?tc McMomo 111122223333
        if code_or_user and not isinstance(code_or_user[0], discord.User) and "".join(
                [str(part) for part in code_or_user]).isnumeric() or \
                "".join([str(part) for part in code_or_user[1:]]).isnumeric():
            try:
                name, code = await generic_or_specific_code(ctx, *code_or_user)
            except AssertionError:
                return

            if len(code) != 12:
                await ctx.send(f"Incorrect number of characters in your trainer code [{code}] "
                               f"{ctx.author.mention}")
                return

            execute_statement(create_upsert_query(
                tablename=tables.TRAINERCODES,
                keys="(name, user_id, code)",
                values=f"('{name}', '{ctx.author.id}', '{code}')",
                key_to_update="code",
                update_value=f"'{code}'"
            ))
            await ctx.send(f"Set the trainer code for {name} to **{format_trainer_code(str(code))}** "
                           f"{ctx.author.mention}")
            return
        # User it trying to remove a trainercode
        elif code_or_user and code_or_user[0] == "remove":
            try:
                await remove_trainercode(ctx, code_or_user)
            except AssertionError:
                return
        # Hit by: ?tc @McMomo and ?tc
        elif not code_or_user or all(isinstance(part, discord.User) for part in code_or_user):
            if len(code_or_user) > 3:
                await ctx.send(f"You can maximum check 3 users at once, "
                               f"please request fewer users at a time {ctx.author.mention}")
                return
            lookup_users = [ctx.author] if not code_or_user else code_or_user

            for lookup_user in lookup_users:
                maybe_found_codes = execute_statement(create_select_query(
                    table_name=tables.TRAINERCODES,
                    where_key="user_id",
                    where_value=lookup_user.id
                )).all(as_dict=True)

                if not maybe_found_codes:
                    await ctx.send(f"No trainer code registered for {lookup_user.mention}")
                else:
                    await ctx.send(build_code_string(maybe_found_codes))
        else:
            concat_name = "".join([str(part) for part in code_or_user])
            maybe_found_by_name = execute_statement(create_select_query(
                table_name=tables.TRAINERCODES,
                where_key="name",
                where_value=f"'{concat_name}'"
            )).all(as_dict=True)

            if not maybe_found_by_name:
                await ctx.send(f"{concat_name} has not registered a trainer code {ctx.author.mention}")
                return

            user_id = maybe_found_by_name[0].get("user_id")
            maybe_found_codes = execute_statement(create_select_query(
                table_name=tables.TRAINERCODES,
                where_key="user_id",
                where_value=user_id
            )).all(as_dict=True)

            await ctx.send(build_code_string(maybe_found_codes))

    @trainercode.error
    async def trainercode_on_error(self, _, error):
        """Error handler for trainer code command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="Trainercode")


async def setup(bot):
    await bot.add_cog(Trainercode(bot))
