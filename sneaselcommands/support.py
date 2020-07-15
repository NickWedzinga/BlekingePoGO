import re

import discord.utils
from discord.ext import commands

import common
from utils import message_wrapper, exception_wrapper, file_wrapper


def _handle_rename_input_syntax_errors(bot, name, id_):
    """
    :param name: The name of the user to rename
    :param id_: The id of the user to rename
    :return: Returns booleans for every error check
    """
    name_too_long = id_non_number = name_not_updated = False
    if len(name) > 15:
        name_too_long = True
    if not int(id_.isdigit()):
        id_non_number = True
    if bot.get_user(int(id_)).display_name != name:
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


def _rename_user_in_file(filename, new_name, user_to_replace):
    """
    :param new_name: The new name to replace the previous name with
    :param user_to_replace: The string to find in the entry
    :return: Returns bool if the user was found and the name that was replaced
    """
    changed = False

    with open(filename, "r") as file:
        lines = file.readlines()

    with open(filename, "w") as file:
        for line in lines:
            if user_to_replace not in line:
                file.write(line)
            else:
                changed = True
                file.write(line.replace(user_to_replace, new_name))
    return changed, user_to_replace


def _update_leaderboards(old_name, new_name, leaderboard_to_update=None):
    """
    :param old_name: The name to replace
    :param new_name: The new name to replace the old name with
    :param leaderboard_to_update: The leaderboard to update, defaults to None in which case all leaderboards will be updated
    """
    if leaderboard_to_update is None:
        leaderboard_list = ["leaderboards/" + x + ".txt" for x in common.LEADERBOARD_LIST]
        for leaderboard in leaderboard_list[1:]:
            _rename_user_in_file(leaderboard, new_name, old_name)
    else:
        _rename_user_in_file(leaderboard_to_update, new_name, old_name)


async def _inform_deleted_user(ctx, found, user_name, leaderboard_type):
    """
    TODO: add docstring
    """
    if found and str(ctx.invoked_with) == "from_leaderboard":
        await ctx.send("%s was found, removing %s from the %s leaderboard." % (
            user_name, user_name, leaderboard_type))
    elif not found and str(ctx.invoked_with) == "from_leaderboard":
        await ctx.send(f"{user_name} could not be found in the {leaderboard_type} leaderboard.")


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
    return "Välkommen till Blekinges leaderboards! \n\n"\
           "**__KOMMANDON TILLGÄNGLIGA__**\n\n"\
           "*Alla kommandon skrivs i #leaderboards*\n\n"\
           "1. ?önskadleaderboard poäng, används för att rapportera in dina poäng till de olika leaderboards. \n    "\
           "*Exempelanvändning 1: '?jogger 2320'*, för att lägga in dina 2320km i Jogger leaderboarden. \n    \"" \
           "*Exempelanvändning 2: '?pikachu 463'*, för att skicka in dina 463 Pikachu fångster i Pikachu Fan leaderboarden.\n" \
           "2. ?list önskadleaderboard, används för att ut en lista på top 5 samt din placering och dina närmsta konkurrenter. "\
           "*Exempelanvändning: ?list jogger*\n" \
           "3. ?ranks, används för att visa hur du rankas mot övriga medlemmar.\n" \
           "4. ?help kommando, används för att få mer information om ett specifikt kommando. *Exempel: ?help jogger*\n"


async def _validate_eligibility(ctx):
    """
    Checks that the user has not already claimed access to the leaderboards and has a valid nickname.
    """
    error_in_nickname = _check_invalid_nickname(ctx.message.author.display_name)
    already_claimed = file_wrapper.found_in_file(str(ctx.message.author.id), "textfiles/idclaims.txt")

    if already_claimed:
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

        Example usage: ?claim
        """
        await message_wrapper.delete_message(bot=self.bot, message=ctx.message)

        if await _validate_eligibility(ctx):
            entry = f"""{ctx.message.author.display_name} {ctx.message.author.id}"""
            file_wrapper.append_to_file(str_to_add=entry, file_name="textfiles/idclaims.txt")

            role = discord.utils.get(ctx.message.guild.roles, name="claimed")
            await ctx.message.author.add_roles(role)

            command_channel = self.bot.get_channel(common.LEADERBOARD_CHANNELS[0])
            await message_wrapper.message_user(self.bot, ctx.message.author, _create_introductory_message())
            await message_wrapper.message_channel(
                bot=self.bot,
                channel=ctx.message.channel,
                message=f""":white_check_mark: {ctx.message.author.mention} you have claimed the nickname """ 
                f"""{ctx.message.author.display_name}. Type ?help in {command_channel.mention} """
                f"""for help on how to get started.""")

    @claim.error
    async def claim_on_error(self, ctx, error):
        await exception_wrapper.pm_dev_error(bot=self.bot, source="claim", error_message=error)

    @commands.command(name="rename")
    @commands.has_role("Admin")
    async def rename(self, ctx, new_name, user_id):
        """
        "This command renames a given player."
        "Example: ?rename McMomo 169688623699066880"

        :param ctx: The context of the user's message
        :param new_name: The new name to replace the old name with
        :param user_id: The id of the member to rename
        :return: Updates the user data in the claim_id list and all leaderboards
        """

        name_too_long, id_non_number, name_not_updated = _handle_rename_input_syntax_errors(self.bot, new_name, user_id)
        error_found = await _report_possible_renaming_errors(ctx, name_too_long, id_non_number, name_not_updated, new_name, ctx.author.mention)

        if not error_found:
            changed, old_name = _rename_user_in_file("textfiles/idclaims.txt", new_name, user_id)
            if changed:
                _update_leaderboards(old_name, new_name)
                await ctx.send("Användarnamnet har uppdaterats från %s till %s" % (
                    old_name, new_name))
            else:
                await ctx.send(f"I could not find this user in the claimed id list. Incorrect id or the user has not claimed their name")

    @rename.error
    async def rename_on_error(self, ctx, error):
        """Catches errors with rename command"""
        await exception_wrapper.pm_dev_error(bot=self.bot, error_message=error, source="rename")

    @commands.group()
    @commands.has_role("Admin")
    async def delete(self, ctx):
        """Delete base function"""
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid delete command, options: delete user, delete from_leaderboard")

    @delete.command(help="Deletes user from all leaderboards. Usage: ?delete user USER_ID")
    @commands.has_role("Admin")
    async def user(self, ctx, user_name):
        """
        :param ctx: The message's context
        :param user_name: The user to remove from all leaderboards
        :return: Removes the user from all leaderboards they have entered
        """
        for leaderboard in common.LEADERBOARD_LIST[1:]:
            cmd = self.bot.get_command("delete from_leaderboard")
            await ctx.invoke(cmd, leaderboard, user_name)
        await ctx.send(f"{user_name} tas bort från alla leaderboards.")

    @delete.command(help="Delete a user from a given leaderboard. "
                         "Usage: ?delete from_leaderboard LEADERBOARD_TYPE USER_NAME")
    @commands.has_role("Admin")
    async def from_leaderboard(self, ctx, leaderboard_type, user_name):
        """
        :param ctx: The message's context
        :param leaderboard_type: Which leaderboard to iterate
        :param user_name: The user to remove
        :return: Removes a user from a provided leaderboard, if found
        """
        if leaderboard_type.lower() in common.LEADERBOARD_LIST:
            found = file_wrapper.remove_line_from_file(
                file_name=f"leaderboards/{leaderboard_type}.txt",
                str_to_remove=user_name)
            await _inform_deleted_user(ctx, found, user_name, leaderboard_type)

    @delete.error
    async def delete_on_error(self, ctx, error):
        """Catches errors with delete command"""
        await exception_wrapper.pm_dev_error(bot=self.bot, error_message=error, source="delete")


def setup(bot):
    bot.add_cog(Support(bot))
