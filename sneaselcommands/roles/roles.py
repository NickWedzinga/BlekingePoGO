from discord.ext import commands

from common import tables
from utils.database_connector import execute_statement, create_select_query
from utils.exception_wrapper import pm_dev_error


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roles")
    async def roles(self, ctx):
        """
        Lists all the available roles that you can give/remove.

        Usage: ?roles
        """
        registered_roles = execute_statement(create_select_query(
            table_name=tables.REGISTERED_ROLES
        )).all(as_dict=True)

        if not registered_roles:
            await ctx.send(f"There are currently no roles registered that you can give/remove {ctx.author.mention}")
            return

        role_string = f"Available roles {ctx.author.mention}\n----------\n"
        for role in registered_roles:
            role_string += f"{role.get('role_name')}\n"

        await ctx.send(role_string)

    @roles.error
    async def remove_on_error(self, _, error):
        """Catches errors with roles command"""
        await pm_dev_error(bot=self.bot, error_message=error, source="roles")


def setup(bot):
    bot.add_cog(Roles(bot))
