import discord
from discord.ext import commands

from common import tables
from utils.database_connector import execute_statement, create_select_query
from utils.exception_wrapper import pm_dev_error


class Remove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="remove")
    async def remove(self, ctx, name):
        """
        Removes a role from you.

        Usage: ?remove unown
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
            await ctx.send(f":no_entry: You cannot remove the role [{name.capitalize()}]. "
                           f"Use *?roles* to see all the available roles that you can give/remove {ctx.author.mention}")
            return

        maybe_role = discord.utils.get(ctx.guild.roles, id=int(maybe_registered_role[0].get("role_id")))
        if maybe_role is None:
            await ctx.send(f":no_entry: Somehow could not find the registered role on this server. "
                           f"Contact an admin, did they register this role properly? {ctx.author.mention}")
            return

        await ctx.author.remove_roles(maybe_role)
        await ctx.send(f":white_check_mark: Successfully removed your [{name}] role {ctx.author.mention}")


    @remove.error
    async def remove_on_error(self, _, error):
        """Catches errors with remove command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="remove")


def setup(bot):
    bot.add_cog(Remove(bot))
