from discord import utils
from discord.ext import commands

from common import constants
from utils.database_connector import execute_statement, create_select_query, create_update_query, execute_statements, \
    create_delete_query
from utils.exception_wrapper import pm_dev_error


class Support(commands.Cog):
    def __init__(self, bot=None):
        self.bot = bot

    @commands.command(name="rename", hidden=True)
    @commands.has_role("Admin")
    async def rename(self, ctx, new_name, user_id):
        """
        [Admin only]: This command renames a given player.

        Usage: ?rename McMomo 133713371337
        """
        try:
            user_to_change = utils.get(ctx.guild.members, id=int(user_id))
            old_name = user_to_change.display_name
        except:
            await ctx.send("Could not find a user on this Discord server with that id.")
            return

        name_too_long, id_non_number, name_not_updated = self.__handle_rename_input_syntax_errors(new_name, user_id,
                                                                                                  old_name)
        error_found = await self.__report_possible_renaming_errors(ctx, name_too_long, id_non_number, name_not_updated,
                                                                   new_name, user_to_change.mention)

        if not error_found:
            self.__rename_user_in_leaderboards(new_name, old_name)
            await ctx.send(f"Username updated from {old_name} to {new_name}")

    @rename.error
    async def rename_on_error(self, _, error):
        """Catches errors with rename command"""
        await pm_dev_error(client=self.bot, error_message=error, source="rename")

    @commands.group(hidden=True)
    @commands.has_role("Admin")
    async def delete(self, ctx):
        """Delete base function"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid delete command, options: delete user, delete from_leaderboard")

    @delete.command()
    @commands.has_role("Admin")
    async def user(self, ctx, user_name):
        """
        [Admin only]: Deletes user from all leaderboards.

        Usage: ?delete McMomo 133713371337
        """
        statements = []
        for leaderboard in [lb.value for lb in constants.Leaderboards]:
            statements.append(create_delete_query(f"leaderboard__{leaderboard}", "name", f"'{user_name}'"))
        execute_statements(statements)
        await ctx.send(f"{user_name} is removed from all leaderboards.")

    @delete.command()
    @commands.has_role("Admin")
    async def from_leaderboard(self, ctx, leaderboard, user_name):
        """
        [Admin only]: Delete a user from a given leaderboard.

        Usage: ?delete from_leaderboard jogger McMomo
        """
        if leaderboard in [lb.value for lb in constants.Leaderboards]:
            in_leaderboard_before = execute_statement(
                create_select_query(f"leaderboard__{leaderboard}", "name", f"'{user_name}'")).all(True)
            execute_statement(create_delete_query(f"leaderboard__{leaderboard}", "name", f"'{user_name}'"))
            in_leaderboard_after = execute_statement(
                create_select_query(f"leaderboard__{leaderboard}", "name", f"'{user_name}'")).all(True)

            if len(in_leaderboard_before) == 1 and len(in_leaderboard_after) == 0:
                await ctx.send(f"Removed {user_name} from {leaderboard}")
            else:
                await ctx.send(f"Could not find {user_name} in {leaderboard}")
        else:
            await ctx.send(f"Can't find the {leaderboard} leaderboard")

    @delete.error
    async def delete_on_error(self, _, error):
        """Catches errors with delete command"""
        await pm_dev_error(client=self.bot, error_message=error, source="delete")

    # ----- helper methods

    @staticmethod
    def __handle_rename_input_syntax_errors(name, user_id, old_name):
        """
        :param name: The name of the user to rename
        :param user_id: The id of the user to rename
        :return: Returns booleans for every error check
        """
        name_too_long = id_non_number = name_not_updated = False

        if len(name) > 15:
            name_too_long = True
        if not int(user_id.isdigit()):
            id_non_number = True
        if old_name != name:
            name_not_updated = True

        return name_too_long, id_non_number, name_not_updated

    # TODO: test this
    @staticmethod
    async def __report_possible_renaming_errors(ctx, name_too_long, id_non_number, name_not_updated, name, mention):
        """
        :param ctx: The context of the user to rename
        :param name_too_long: True if characters in name > 15
        :param id_non_number: True if id is not a digit
        :param name_not_updated: True if user's nickname hasn't been changed to reflect rename
        :return: Returns True if any errors occur
        """
        status = ""
        error_found = False

        if name_too_long:
            error_found = True
            status += "Name is too long, max 15 letters. *Format: ?rename DESIRED_NAME USER_ID\n"
        if id_non_number:
            error_found = True
            status += "USER_ID must be numbers only. *Format: ?rename DESIRED_NAME USER_ID\n"
        if name_not_updated:
            status += f"Don't forget to change your name to {name} {mention}"

        if status != "":
            await ctx.send(status)
        return error_found

    # TODO: test this
    @staticmethod
    def __rename_user_in_leaderboards(new_name: str, old_name: str):
        """Updates all the leaderboard tables with the new name"""
        statements = []
        for leaderboard in [lb.value for lb in constants.Leaderboards]:
            statements.append(
                create_update_query(f"leaderboard__{leaderboard}", "name", f"'{new_name}'", "name", f"'{old_name}'"))
        execute_statements(statements)


async def setup(bot):
    await bot.add_cog(Support(bot))
