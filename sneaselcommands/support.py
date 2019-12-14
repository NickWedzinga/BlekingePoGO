import re

from discord.ext import commands
from instance import bot
import common
import discord.utils

# TODO: refactor to not do both error checking and reporting
async def _handle_rename_input_syntax_errors(ctx, name, id):
    if len(name) > 15:
        await ctx.send("Namnet är för långt, max 15 tecken. *Format: ?rename DESIRED_NAME USER_ID")
        return False
    elif not int(id.isdigit()):
        await ctx.send("USER_ID måste vara siffror endast. *Format: ?rename DESIRED_NAME USER_ID")
        return False
    return True



def _remove_user_from_file(file_name, user_name):
    """
    :param file_name: Name of the file to iterate
    :param user_name: Name of the user to remove
    :return: Checks if user_name is in the provided file and removes it if found, returns boolean if user was found
    """
    found = False
    with open(file_name, "r") as leaderboard_file:
        lines = leaderboard_file.readlines()

    with open(file_name, "w") as leaderboard_file:
        for line in lines:
            if user_name.lower() not in line.lower():
                leaderboard_file.write(line)
            else:
                found = True
    return found


async def _inform_user(ctx, found, user_name, leaderboard_type):
    if found and str(ctx.invoked_with) == "from_leaderboard":
        await ctx.send("%s was found, removing %s from the %s leaderboard." % (
            user_name, user_name, leaderboard_type))
    elif not found and str(ctx.invoked_with) == "from_leaderboard":
        await ctx.send(f"{user_name} could not be found in the {leaderboard_type} leaderboard.")


class Support(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="claim", pass_context=True, help="This command allows members access to the leaderboards.")
    async def claim(self, ctx):
        claimedIDs = []

        # Add information of user to temporary list
        tempID = []
        tempID.append(str(ctx.message.author.display_name))
        tempID.append(str(ctx.message.author.id) + "\n")

        found = False
        # delete msg
        try:
            await ctx.delete_message()  # TODO: Doesn't work
        except:
            print("Somehow failed to delete CLAIM message.")
        # Check for illegal nickname symbols, + ensures min size == 1
        stringPattern = r'[^\.A-Za-z0-9]'
        if (re.search(stringPattern, ctx.message.author.display_name)):
            await ctx.send(
                "Ditt Discord användarnamn innehåller otillåtna tecken, var god ändra ditt användarnamn så att det matchar det i Pokémon Go.")
        elif len(ctx.message.author.display_name) > 15:
            await ctx.send(
                "Ditt Discord användarnamn får inte överstiga 15 tecken, var god ändra ditt namn så det matchar det i Pokémon Go.")
        else:
            with open("textfiles/idclaims.txt") as file:
                claimedIDs = [line.split(" ") for line in file]

            # Read for ID in file
            claimFile = open("textfiles/idclaims.txt", "r")
            for item in claimedIDs:
                if float(item[1]) == float(ctx.message.author.id):
                    await ctx.send(":no_entry: Du har redan claimat ditt användarnamn %s, om du har bytt användarnamn "
                                   "kontakta en valfri admin." % ctx.message.author.mention)
                    found = True
            claimFile.close()
            # Write to file
            if not found:
                # Add to list
                claimedIDs.insert(0, tempID)
                # Add ID to file
                print("Adding new user")
                claimFile = open("idclaims.txt", "w")
                for item in claimedIDs:
                    claimFile.write(item[0])
                    claimFile.write(" ")
                    claimFile.write(item[1])
                claimFile.close()

                channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[0])
                claimedRole = discord.utils.get(ctx.message.author.server.roles, name="claimed")
                await bot.add_roles(ctx.message.author, claimedRole)
                # assign role is not claimed yet, send PM with help info
                await ctx.send(
                    ":white_check_mark: %s du har claimat användarnamnet %s. Skriv ?help i %s för hjälp med att komma igång." % (
                        ctx.message.author.mention, ctx.message.author.display_name, channel2.mention))
                codeMessage = "Välkommen till Blekinges leaderboards! \n\n"
                codeMessage += "**__KOMMANDON TILLGÄNGLIGA__**\n\n"
                codeMessage += "*Alla kommandon skrivs i #leaderboards*\n\n"
                codeMessage += "1. ?önskadleaderboard poäng, används för att rapportera in dina poäng till de olika leaderboards. \n    *Exempelanvändning 1: '?jogger 2320'*, för att lägga in dina 2320km i Jogger leaderboarden. \n    *Exempelanvändning 2: '?pikachu 463'*, för att skicka in dina 463 Pikachu fångster i Pikachu Fan leaderboarden.\n"
                codeMessage += "2. ?list önskadleaderboard, används för att ut en lista på top 5 samt din placering och dina närmsta konkurrenter. *Exempelanvändning: ?list jogger*\n"
                codeMessage += "3. ?ranks, används för att visa hur du rankas mot övriga medlemmar.\n"
                codeMessage += "4. ?help kommando, används för att få mer information om ett specifikt kommando. *Exempel: ?help jogger*\n"
                await ctx.message.author.send(codeMessage)

    @claim.error
    async def claim_on_error(self, ctx, error):
        for dev in common.DEVELOPERS:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in CLAIM command: {error}""")

    @commands.command(name="rename", pass_context=True, help="This command renames a given player."
                                                             "Example: ?rename McMouse 169688623699066880")
    @commands.has_role("Admin")
    async def rename(self, ctx, new_name, user_id):
        """
        :param ctx:
        :param new_name:
        :param user_id:
        :return:
        """

        replacedNick = ""
        newNick = ""

        no_errors = await _handle_rename_input_syntax_errors(ctx, new_name, user_id)
        if no_errors:
            insertList = []
            changedIndex = 0
            changed = False
            claimList = []

            file = open("textfiles/idclaims.txt", "r")
            for index, item in enumerate(file):
                item = item.split(" ")

                # Put line in tempList to write back later
                temp2 = []
                temp2.append(item[0])
                temp2.append(" ")
                temp2.append(item[1])

                # compare ID to list IDs
                item[1] = item[1].replace("\n", "")
                if str(item[1]) == str(user_id):
                    changedIndex = index
                    changed = True
                    replacedNick = temp2[0]
                    temp2[0] = new_name
                    newNick = temp2[0]
                    insertList = temp2
                claimList.append(temp2)
            file.close()
            # if user ID was found, pop that entry
            if changed:
                claimList.pop(changedIndex)
                claimList.insert(changedIndex, insertList)

                file = open("textfiles/idclaims.txt", "w")
                for item in claimList:
                    file.write(item[0])
                    file.write(item[1])
                    file.write(item[2])
                file.close()

                leaderboard_list = ["leaderboards/" + x + ".txt" for x in common.LEADERBOARD_LIST]
                # Loop through files and update to new nickname
                for leaderboard in leaderboard_list[1:]:
                    fileList = []
                    # Read from file and look for nickname to update
                    file = open(leaderboard, "r")
                    for item in file:
                        item = item.split(" ")
                        # if name in file matches old name
                        if item[0].lower() == replacedNick.lower():
                            item[0] = newNick
                        temp = []
                        temp.append(item[0])
                        temp.append(" ")
                        temp.append(item[1])
                        temp.append(" ")
                        temp.append(item[2])
                        fileList.append(temp)
                    file.close()

                    # Write back to file with updated nickname
                    file = open(leaderboard, "w")
                    for item in fileList:
                        # if name in file matches old name
                        file.write(item[0])
                        file.write(" ")
                        file.write(item[2])
                        file.write(" ")
                        file.write(item[4])
                    file.close()
                await ctx.send("Användarnamnet har uppdaterats från %s till %s" % (
                    replacedNick, newNick))
            else:
                await ctx.send("Jag kunde inte hitta spelaren, felaktig ID eller aldrig claimat.")

    @rename.error
    async def rename_on_error(self, ctx, error):
        """Catches errors with rename command"""
        for dev in common.DEVELOPERS:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in RENAME command: {error}""")

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
            cmd = bot.get_command("delete from_leaderboard")
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
            found = _remove_user_from_file(
                file_name=f"leaderboards/{leaderboard_type}.txt",
                user_name=user_name)
            await _inform_user(ctx, found, user_name, leaderboard_type)

    @delete.error
    async def delete_on_error(self, ctx, error):
        """Catches errors with delete command"""
        for dev in common.DEVELOPERS:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in DELETE command: {error}""")


def setup(bot):
    bot.add_cog(Support(bot))
