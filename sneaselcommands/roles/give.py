import discord
from discord.ext import commands

from common import tables
from utils.database_connector import execute_statement, create_select_query
from utils.exception_wrapper import pm_dev_error


class Give(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="give")
    async def give(self, ctx, name):
        """
        Gives you a desired role.

        Usage: ?give unown

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
        await ctx.send(f":white_check_mark: You now have the [{name.capitalize()}] role {ctx.author.mention}")

    @give.error
    async def give_on_error(self, _, error):
        """Catches errors with give command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="give")


def setup(bot):
    bot.add_cog(Give(bot))
