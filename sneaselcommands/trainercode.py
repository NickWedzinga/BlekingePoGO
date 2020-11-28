import discord.utils
from discord.ext import commands

from common import tables
from utils.database_connector import execute_statement, create_select_query, create_upsert_query, create_delete_query
from utils.exception_wrapper import pm_dev_error
from typing import Union

async def remove_trainercode(ctx):
    """
    Removes the trainer code of the message author
    """
    maybe_found_code = execute_statement(create_select_query(
        table_name=tables.TRAINERCODES,
        where_key="user_id",
        where_value=ctx.author.id
    )).all(as_dict=True)

    if not maybe_found_code:
        await ctx.send(f"You have not previously registered a trainer code {ctx.author.mention}")
    else:
        execute_statement(create_delete_query(
            table_name=tables.TRAINERCODES,
            where_key="user_id",
            where_value=ctx.author.id
        ))
        await ctx.send(f"Successfully removed your trainer code {ctx.author.mention}")


class Trainercode(commands.Cog):
    def __init__(self, bot=None):
        self.bot = bot

    @commands.command(aliases=["tc"])
    async def trainercode(self, ctx, *code_or_user: Union[discord.User, str]):
        """
        Use this command to register your trainer code and look up other trainer's codes

        Usage:
        To register your trainer code use: ?trainercode 111122223333
        To print your own trainer code use: ?trainercode
        To print someone else's trainer code use: ?trainercode @McMomo

        To remove your trainer code use: ?trainercode remove

        Instead of ?trainercode you can also use ?tc
        """
        if code_or_user and not isinstance(code_or_user[0], discord.User) and "".join(code_or_user).isnumeric():
            code_or_user = int("".join(code_or_user))

            if len(str(code_or_user)) != 12:
                await ctx.send(f"Incorrect number of characters in your trainer code [{code_or_user}] {ctx.author.mention}")
                return

            execute_statement(create_upsert_query(
                tablename=tables.TRAINERCODES,
                keys="(user_id, code)",
                values=f"('{ctx.author.id}', '{code_or_user}')",
                key_to_update="code",
                update_value=f"'{code_or_user}'"
            ))
            await ctx.send(f"Set your trainer code to [{code_or_user}] {ctx.author.mention}")
            return
        elif code_or_user and code_or_user[0] == "remove":
            await remove_trainercode(ctx)
        elif not code_or_user or isinstance(code_or_user[0], discord.User):
            lookup_user = ctx.author if not code_or_user else code_or_user[0]

            maybe_found_code = execute_statement(create_select_query(
                table_name=tables.TRAINERCODES,
                where_key="user_id",
                where_value=lookup_user.id
            )).all(as_dict=True)

            if not maybe_found_code:
                await ctx.send(f"No trainer code registered for {lookup_user.mention}")
                return

            try:
                code = maybe_found_code[0].get("code")
                assert(len(maybe_found_code) == 1)
                assert(code is not None)
            except:
                await pm_dev_error(self.bot, error_message="Trainercode: Multiple codes for same user OR issue extracting code")
                return

            await ctx.send(f"Trainer code for {lookup_user.mention}: {code}")
            return
        else:
            await ctx.send(f"Incorrect use of trainer codes, please type **?help trainercode** for help {ctx.author.mention}")

    @trainercode.error
    async def trainercode_on_error(self, _, error):
        await pm_dev_error(bot=self.bot, error_message=error, source="Trainercode")


def setup(bot):
    bot.add_cog(Trainercode(bot))
