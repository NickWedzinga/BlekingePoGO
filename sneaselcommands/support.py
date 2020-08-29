import re

import discord.utils
from discord.ext import commands

import common
from utils import message_wrapper, exception_wrapper
from utils.database_connector import execute_statement, create_select_query, create_update_query, execute_statements, \
    create_delete_query


def _handle_rename_input_syntax_errors(name, user_id, old_name):
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


# TODO: integration test this
async def _report_possible_renaming_errors(ctx, name_too_long, id_non_number, name_not_updated, name, mention):
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
        status += "Namnet är för långt, max 15 tecken. *Format: ?rename DESIRED_NAME USER_ID\n"
    if id_non_number:
        error_found = True
        status += "USER_ID måste vara siffror endast. *Format: ?rename DESIRED_NAME USER_ID\n"
    if name_not_updated:
        status += f"Don't forget to change your name to {name} {mention}"

    if status != "":
        await ctx.send(status)
    return error_found


def _rename_user_in_idclaims(new_name, user_id) -> bool:
    """
    :param new_name: The new name to replace the previous name with
    :param user_to_replace: The string to find in the entry
    :return: Returns bool if the user was found and the name that was replaced
    """
    previous_entry = execute_statement(create_select_query("leaderboard__idclaims", "user_id", f"'{user_id}'")).all(as_dict=True)
    execute_statement(create_update_query("leaderboard__idclaims", "name", f"'{new_name}'", "user_id", f"'{user_id}'"))
    updated_entry = execute_statement(create_select_query("leaderboard__idclaims", "user_id", f"'{user_id}'")).all(as_dict=True)

    try:
        if previous_entry[0].get("name") != new_name and updated_entry[0].get("name") == new_name:
            return True
        else:
            return False
    except:
        return False


def _rename_user_in_leaderboards(new_name: str, old_name: str):
    """Updates all the leaderboard tables with the new name"""
    statements = []
    for leaderboard in common.LEADERBOARD_LIST:
        statements.append(create_update_query(f"leaderboard__{leaderboard}", "name", f"'{new_name}'", "name", f"'{old_name}'"))
    execute_statements(statements)


def _check_invalid_nickname(name: str):
    """
    Validates that the Discord nickname follows the rules that apply to the Pokémon GO nicknames.

    Returns false if the validation was okay, else returns an error message in String format.
    """
    if re.search(r'[^A-Za-z0-9]', name):
        return "Your Discord nickname contains illegal characters, please change it to match your nickname from " \
               "Pokémon GO."
    elif len(name) > 15:
        return "Your Discord nickname is too long, please change it to match your nickname from Pokémon GO."
    else:
        return False


# TODO: English, don't hard-code #leaderboards, get command channel from leaderboard list
def _create_introductory_message():
    return "Välkommen till Blekinges leaderboards! \n\n" \
           "**__KOMMANDON TILLGÄNGLIGA__**\n\n" \
           "*Alla kommandon skrivs i #leaderboards*\n\n" \
           "1. ?önskadleaderboard poäng, används för att rapportera in dina poäng till de olika leaderboards. \n    " \
           "*Exempelanvändning 1: '?jogger 2320'*, för att lägga in dina 2320km i Jogger leaderboarden. \n    \"" \
           "*Exempelanvändning 2: '?pikachu 463'*, för att skicka in dina 463 Pikachu fångster i Pikachu Fan leaderboarden.\n" \
           "2. ?list önskadleaderboard, används för att ut en lista på top 5 samt din placering och dina närmsta konkurrenter. " \
           "*Exempelanvändning: ?list jogger*\n" \
           "3. ?ranks, används för att visa hur du rankas mot övriga medlemmar.\n" \
           "4. ?help kommando, används för att få mer information om ett specifikt kommando. *Exempel: ?help jogger*\n"


async def _validate_eligibility(ctx):
    """
    Checks that the user has not already claimed access to the leaderboards and has a valid nickname.
    """
    error_in_nickname = _check_invalid_nickname(ctx.message.author.display_name)
    rows = execute_statement(
        create_select_query(table_name="leaderboard__idclaims", where_key="user_id", where_value=str(ctx.message.author.id))).all(
        as_dict=True)

    if len(rows) > 0:
        await message_wrapper.message_channel(
            bot=ctx.bot,
            channel=ctx.message.channel,
            message=f""":no_entry: You have already claimed access to the leaderboards, """
                    f"""{ctx.message.author.mention}, if you have recently changed your nickname, """
                    f"""please contact an admin.""",
            source="claim")
        return False
    elif error_in_nickname:
        await message_wrapper.message_channel(bot=ctx.bot, channel=ctx.channel, message=error_in_nickname)
        return False
    return True


class Support(commands.Cog):
    def __init__(self, bot=None):
        self.bot = bot

    @commands.command(name="claim")
    async def claim(self, ctx):
        """
        Use this command to gain access to the leaderboards.

        Usage: ?claim
        """
        await message_wrapper.delete_message(bot=self.bot, message=ctx.message, source="Claim")

        if await _validate_eligibility(ctx):
            execute_statement(
                f"INSERT INTO idclaims (name, user_id) VALUES ('{ctx.author.display_name}', {ctx.author.id})")

            role = discord.utils.get(ctx.message.guild.roles, name="claimed")
            await ctx.message.author.add_roles(role)

            command_channel = discord.utils.get(ctx.message.guild.channels, name="leaderboards")
            await message_wrapper.message_user(self.bot, ctx.message.author, _create_introductory_message(),
                                               source="Claim")
            await message_wrapper.message_channel(
                bot=self.bot,
                channel=ctx.message.channel,
                message=f""":white_check_mark: {ctx.message.author.mention} you have claimed the nickname """
                        f"""{ctx.message.author.display_name}. Type ?help in {command_channel.mention} """
                        f"""for help on how to get started."""
            )

    @claim.error
    async def claim_on_error(self, _, error):
        await exception_wrapper.pm_dev_error(bot=self.bot, source="claim", error_message=error)

    @commands.command(name="rename", hidden=True)
    @commands.has_role("Admin")
    async def rename(self, ctx, new_name, user_id):
        """
        [Admin only]: This command renames a given player.

        Usage: ?rename McMomo 133713371337
        """
        try:
            user_to_change = discord.utils.get(ctx.guild.members, id=int(user_id))
            old_name = user_to_change.display_name
        except:
            await ctx.send("Could not find a user on this Discord server with that id.")
            return

        name_too_long, id_non_number, name_not_updated = _handle_rename_input_syntax_errors(new_name, user_id, old_name)
        error_found = await _report_possible_renaming_errors(ctx, name_too_long, id_non_number, name_not_updated,
                                                             new_name, user_to_change.mention)

        if not error_found:
            changed = _rename_user_in_idclaims("idclaims", new_name, user_id)
            if changed:
                _rename_user_in_leaderboards(new_name, old_name)
                await ctx.send(f"Username updated from {old_name} to {new_name}")
            else:
                await ctx.send(
                    f"Error with renaming {user_to_change.mention} in the database. "
                    f"\nEither incorrect id, the user has never claimed or the user has already claimed with that name")

    @rename.error
    async def rename_on_error(self, _, error):
        """Catches errors with rename command"""
        await exception_wrapper.pm_dev_error(bot=self.bot, error_message=error, source="rename")

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
        for leaderboard in common.LEADERBOARD_LIST:
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
        if leaderboard in common.LEADERBOARD_LIST:
            in_leaderboard_before = execute_statement(create_select_query(f"leaderboard__{leaderboard}", "name", f"'{user_name}'")).all(True)
            execute_statement(create_delete_query(f"leaderboard__{leaderboard}", "name", f"'{user_name}'"))
            in_leaderboard_after = execute_statement(create_select_query(f"leaderboard__{leaderboard}", "name", f"'{user_name}'")).all(True)

            if len(in_leaderboard_before) == 1 and len(in_leaderboard_after) == 0:
                await ctx.send(f"Removed {user_name} from {leaderboard}")
            else:
                await ctx.send(f"Could not find {user_name} in {leaderboard}")
        else:
            await ctx.send(f"Can't find the {leaderboard} leaderboard")

    @delete.error
    async def delete_on_error(self, _, error):
        """Catches errors with delete command"""
        await exception_wrapper.pm_dev_error(bot=self.bot, error_message=error, source="delete")


def setup(bot):
    bot.add_cog(Support(bot))
