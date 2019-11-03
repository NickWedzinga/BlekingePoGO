from discord.ext import commands

import Includes


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list", pass_context=True, help="?list önskadleaderboard, används för att ut en lista på "
                                                           "top 5 samt din placering och dina närmsta konkurrenter. "
                                                           "*Exempelanvändning: ?list jogger*")
    async def list(self, ctx, args):
        leaderboard_type = args.lower()

        lookUpList = []
        messageOut = ""

        if not leaderboard_type in Includes.leaderboard_list:
            await ctx.send("%s leaderboarden existerar inte." % leaderboard_type.capitalize())
        else:
            found = False
            file = open("%s.txt" % leaderboard_type, "r")
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
                index += 1
            await ctx.send(messageOut)

    @list.error
    async def list_on_error(self, ctx, error):
        for dev in Includes.developers:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in LIST command: {error}""")


def setup(bot):
    bot.add_cog(Information(bot))