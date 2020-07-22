import traceback

from discord.ext import commands

import common


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list")
    async def list(self, ctx, leaderboard_type):
        """
        List your position in a given leaderboard.

        This command will list the top 5 of the leaderboard as well as your position and your closest competitors.

        Usage: ?list jogger
        """
        leaderboard_type = leaderboard_type.lower()

        lookUpList = []
        messageOut = f"**---{leaderboard_type.capitalize()} list:---**\n"

        if not leaderboard_type in common.LEADERBOARD_LIST:
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
                if not common.INTEGRATION_TESTING:
                    await ctx.send(messageOut)
            else:
                await ctx.send(f"Could not find {ctx.message.author.mention} in {leaderboard_type}")

    @list.error
    async def list_on_error(self, ctx, error):
        traceback.print_exc()
        for dev in common.DEVELOPERS:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in LIST command: {error}""")


def setup(bot):
    bot.add_cog(Information(bot))
