import traceback

from discord.ext import commands

import Common


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list", pass_context=True, help="?list önskadleaderboard, används för att ut en lista på "
                                                           "top 5 samt din placering och dina närmsta konkurrenter. "
                                                           "Exempelanvändning: ?list jogger")
    async def list(self, ctx, leaderboard_type):
        leaderboard_type = leaderboard_type.lower()

        lookUpList = []
        messageOut = f"**---{leaderboard_type.capitalize()} list:---\n**"

        if not leaderboard_type in Common.leaderboard_list:
            await ctx.send("%s leaderboarden existerar inte." % leaderboard_type.capitalize())
        else:
            found = False
            file = open("leaderboards/%s.txt" % leaderboard_type, "r")
            index = 0
            currentRank = 0
            currentScore = 0
            for item in file:
                item2 = item.split(" ")
                tempList = []
                if not float(currentScore) == float(item2[1]):
                    currentScore = float(item2[1])
                    currentRank += 1
                if index < 5:
                    # found user among top 5
                    if item2[0].lower() == ctx.message.author.display_name.lower():
                        found = True
                        messageOut += "**%i. %s %s**\n" % (currentRank, item2[0], item2[1])
                    else:
                        messageOut += "%i. %s %s\n" % (currentRank, item2[0], item2[1])
                    tempList.append(item2[0])
                    tempList.append(item2[1])
                    lookUpList.append(tempList)
                elif not found:
                    tempList.append(item2[0])
                    tempList.append(item2[1])
                    lookUpList.append(tempList)
                    # found user lower down
                    if item2[0].lower() == ctx.message.author.display_name.lower():
                        messageOut += "-----------------\n%i. %s %s" % (
                            currentRank - 2, lookUpList[index - 2][0], lookUpList[index - 2][1])
                        messageOut += "\n%i. %s %s" % (
                            currentRank - 1, lookUpList[index - 1][0], lookUpList[index - 1][1])
                        messageOut += "\n**%i. %s %s**" % (currentRank, item2[0], item2[1])
                        found = True
                index += 1
            if found:
                if not Common.integrationtesting:
                    await ctx.send(messageOut)
            else:
                await ctx.send(f"Could not find {ctx.message.author.mention} in {leaderboard_type}")

    @list.error
    async def list_on_error(self, ctx, error):
        traceback.print_exc()
        for dev in Common.developers:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in LIST command: {error}""")

    # @commands.command(name="ranks", pass_context=True, help="Kommandot ?ranks används för att skriva ut en lista med "
    #                                                         "dina placeringar i de olika leaderboards."
    #                                                         "\nExempel: ?ranks")
    # async def ranks(self, ctx):
    #     nickname = ctx.message.author.display_name
    #
    #     # Check if users display name is in claim list--------------------------------
    #     nameButNotID = False
    #     IDButNotName = False
    #     fileCheck = open("textfiles/idclaims.txt", "r")
    #     for item in fileCheck:
    #         item = item.split(" ")
    #         item[0] = item[0].replace("\n", "")
    #         item[1] = item[1].replace("\n", "")
    #         # Check if previously claimed, nickname matches
    #         if str(item[0].lower()) == str(ctx.message.author.display_name.lower()):
    #             # Check if previously claimed, id matches
    #             if not (str(item[1]) == str(ctx.message.author.id)):
    #                 nameButNotID = True
    #         # Check if previously claimed, id matches
    #         if str(item[1]) == str(ctx.message.author.id):
    #             # Check if previously claimed, nickname matches
    #             if not (str(item[0].lower()) == str(ctx.message.author.display_name.lower())):
    #                 IDButNotName = True
    #     fileCheck.close()
    #     # ------------------------------------------------------------------------------
    #
    #     # Nickname exists, but not correct ID
    #     if nameButNotID and not IDButNotName:
    #         await ctx.send("Ditt användarnamn matchar inte med det du registrerat tidigare, "
    #                        "ändra tillbaka eller ta kontakt med valfri admin.")
    #     elif nameButNotID:
    #         await ctx.send("Ditt användarnamn matchar med någon annans och inte det du registrerat tidigare, "
    #                        "ändra tillbaka eller ta kontakt med valfri admin.")
    #     elif IDButNotName:
    #         await ctx.send("Ditt användarnamn matchar inte med det du registrerat tidigare, "
    #                        "ändra tillbaka det eller ta kontakt med valfri admin.")
    #     else:
    #         found = False
    #
    #         unitString = ""
    #         currentRank = 0
    #         currentScore = 0
    #         currentRankList = []
    #
    #         num2words1 = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
    #                       6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
    #                       11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen',
    #                       15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen'}
    #         messageOut = ""
    #         messageOut2 = ""  # "needed" because message too long
    #         loops = True
    #         # Loop through leaderboard types
    #         for item in Common.leaderboard_list[1:]:
    #             if item == "jogger":
    #                 unitString = "km"
    #             elif item == "pikachu":
    #                 unitString = "Pikachu"
    #             elif item == "battlegirl":
    #                 unitString = "battles"
    #             elif item == "pokedex":
    #                 unitString = "Pokémon"
    #             elif item == "collector":
    #                 unitString = "Pokémon"
    #             elif item == "scientist":
    #                 unitString = "evolves"
    #             elif item == "breeder":
    #                 unitString = "ägg"
    #             elif item == "backpacker":
    #                 unitString = "Pokéstops"
    #             elif item == "fisherman":
    #                 unitString = "Magikarp"
    #             elif item == "youngster":
    #                 unitString = "Rattata"
    #             elif item == "berrymaster":
    #                 unitString = "bär"
    #             elif item == "gymleader":
    #                 unitString = "timmar"
    #             elif item == "champion":
    #                 unitString = "raids"
    #             elif item == "battlelegend":
    #                 unitString = "legendary raids"
    #             elif item == "ranger":
    #                 unitString = "field research tasks"
    #             elif item == "unown":
    #                 unitString = "Unown"
    #             elif item == "gentleman":
    #                 unitString = "trades"
    #             elif item == "pilot":
    #                 unitString = "km trades"
    #             elif item == "totalxp":
    #                 unitString = "xp"
    #             elif item == "goldgyms":
    #                 unitString = "gyms"
    #             elif item == "idol":
    #                 unitString = "best friends"
    #             elif item == "greatleague":
    #                 unitString = "battles"
    #             elif item == "ultraleague":
    #                 unitString = "battles"
    #             elif item == "masterleague":
    #                 unitString = "battles"
    #             elif item == "acetrainer":
    #                 unitString = "battles"
    #             elif item == "cameraman":
    #                 unitString = "foton"
    #             elif item == "hero":
    #                 unitString = "vinster"
    #             elif item == "purifier":
    #                 unitString = "Pokémon"
    #
    #             leaderboard_file = open("leaderboards/%s.txt" % item, "r")
    #
    #             # Loop through file
    #
    #             for index, line in enumerate(leaderboard_file):
    #                 line = line.split(" ")
    #
    #                 # If score not same as previous player, update rank
    #                 if not float(currentScore) == float(line[1]):
    #                     currentRank = index + 1
    #                     currentScore = float(line[1])
    #
    #                 if line[0].lower() == nickname.lower():
    #                     found = True
    #                     tempMsg = ""
    #                     localScore = round(float(line[1]), 1)
    #                     if not item in "jogger":
    #                         localScore = int(localScore)
    #                     if currentRank == 1:
    #                         tempMsg = ":first_place: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (
    #                             ctx.message.author.mention, currentRank, item.capitalize(), localScore, unitString)
    #                     elif currentRank == 2:
    #                         tempMsg = ":second_place: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (
    #                             ctx.message.author.mention, currentRank, item.capitalize(), localScore, unitString)
    #                     elif currentRank == 3:
    #                         tempMsg = ":third_place: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (
    #                             ctx.message.author.mention, currentRank, item.capitalize(), localScore, unitString)
    #                     elif currentRank == 10:
    #                         tempMsg = ":keycap_%s: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (
    #                             num2words1[currentRank].lower(), ctx.message.author.mention, currentRank,
    #                             item.capitalize(),
    #                             localScore, unitString)
    #                     elif currentRank > 3 and currentRank < 11:
    #                         tempMsg = ":%s: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (
    #                             num2words1[currentRank].lower(), ctx.message.author.mention, currentRank,
    #                             item.capitalize(),
    #                             localScore, unitString)
    #                     elif currentRank > 10:
    #                         tempMsg = ":asterisk: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (
    #                             ctx.message.author.mention, currentRank, item.capitalize(), localScore, unitString)
    #                     else:
    #                         tempMsg = "%s är inte placerad i någon %s leaderboard, skicka in dina poäng genom att skriva ?%s poäng.\n" % (
    #                             ctx.message.author.mention, item.capitalize(), item)
    #
    #                     if loops:
    #                         messageOut += tempMsg
    #                         loops = False
    #                     else:
    #                         messageOut2 += tempMsg
    #                         loops = True
    #         if found:
    #             await ctx.message.author.send(messageOut)
    #             await ctx.message.author.send(messageOut2)
    #             await ctx.send("Du har fått ett privatmeddelande med alla dina placeringar %s."
    #                            % ctx.message.author.mention)
    #         if not found:
    #             await ctx.send("Vi lyckades inte hitta dig bland några leaderboards %s. "
    #                            "Du verkar inte registrerat några poäng ännu." % ctx.message.author.mention)
    #
    # @ranks.error
    # async def ranks_on_error(self, ctx, error):
    #     for dev in Common.developers:
    #         user = ctx.bot.get_user(dev)
    #         await user.send(f"""Error in RANKS command: {error}""")


def setup(bot):
    bot.add_cog(Information(bot))
