import discord
from discord.ext import commands

from common import tables
from utils.database_connector import execute_statement, create_select_query
from utils.exception_wrapper import pm_dev_error


class Sub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sub")
    async def sub(self, ctx, name):
        """
        Subscribes you to a desired role.

        Usage: ?sub unown

        For a complete list of available roles type *?roles*
        """
        maybe_registered_role = execute_statement(create_select_query(
            table_name=tables.REGISTERED_ROLES,
            where_key="role_name",
            where_value=f"'{name}'"
        )).all(as_dict=True)

        if not maybe_registered_role:
            await ctx.send(f":no_entry: No role available with the name [{name.capitalize()}]. "
                           f"Use *?roles* to see all the available roles {ctx.author.mention}")
            return

        maybe_role = discord.utils.get(ctx.guild.roles, id=int(maybe_registered_role[0].get("role_id")))
        if maybe_role is None:
            await ctx.send(f":no_entry: Somehow could not find the registered role on this server. "
                           f"Contact an admin, did they register this role properly? {ctx.author.mention}")
            return

        if any(role == maybe_role for role in ctx.author.roles):
            await ctx.send(f":no_entry: You already have the [{name.capitalize()}] role {ctx.author.mention}")
            return

        await ctx.author.add_roles(maybe_role)
        await ctx.send(f":white_check_mark: Successfully subscribed to the [{name.capitalize()}] role {ctx.author.mention}")

    @sub.error
    async def sub_on_error(self, _, error):
        """Catches errors with sub command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="sub")

    @commands.command(name="unsub")
    async def unsub(self, ctx, name):
        """
        Unsubscribe to a role.

        Usage: ?unsub unown
        """
        if not any(role.name == name for role in ctx.author.roles):
            await ctx.send(f"You have no role with the name [{name}] {ctx.author.mention}")
            return

        maybe_registered_role = execute_statement(create_select_query(
            table_name=tables.REGISTERED_ROLES,
            where_key="role_name",
            where_value=f"'{name}'"
        )).all(as_dict=True)

        if not maybe_registered_role:
            await ctx.send(f":no_entry: You cannot unsubscribe from the role [{name.capitalize()}]. "
                           f"Use *?roles* to see all the available roles that you can sub/unsub {ctx.author.mention}")
            return

        maybe_role = discord.utils.get(ctx.guild.roles, id=int(maybe_registered_role[0].get("role_id")))
        if maybe_role is None:
            await ctx.send(f":no_entry: Somehow could not find the registered role on this server. "
                           f"Contact an admin, did they register this role properly? {ctx.author.mention}")
            return

        await ctx.author.remove_roles(maybe_role)
        await ctx.send(f":white_check_mark: Successfully unsubscribed from the [{name}] role {ctx.author.mention}")

    @unsub.error
    async def unsub_on_error(self, _, error):
        """Catches errors with unsub command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="unsub")


async def setup(bot):
    await bot.add_cog(Sub(bot))
