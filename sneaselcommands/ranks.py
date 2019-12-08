import traceback

from discord.ext import commands

import common


# TODO: refactor
def _check_if_member_claimed(nickname, id):
    fileCheck = open("textfiles/idclaims.txt", "r")
    nameButNotID = IDButNotName = False

    for item in fileCheck:
        item = item.split(" ")
        item[0] = item[0].replace("\n", "")
        item[1] = item[1].replace("\n", "")
        # Check if previously claimed, nickname matches
        if str(item[0].lower()) == str(nickname):
            # Check if previously claimed, id matches
            if not (str(item[1]) == str(id)):
                nameButNotID = True
        # Check if previously claimed, id matches
        if str(item[1]) == str(id):
            # Check if previously claimed, nickname matches
            if not (str(item[0].lower()) == str(nickname)):
                IDButNotName = True
    fileCheck.close()
    return nameButNotID, IDButNotName


async def _handle_missing_information(ctx, missing_id, missing_name):
    if missing_id:
        await ctx.send("Ditt användarnamn matchar inte med det du registrerat tidigare, "
                 "ändra tillbaka eller ta kontakt med valfri admin.")
        raise Exception(
            "Member was missing from list of previously claimed members, assuming renamed member.")
    elif missing_name:
        await ctx.send("Ditt användarnamn matchar inte med det du registrerat tidigare, "
                 "ändra tillbaka det eller ta kontakt med valfri admin.")
        raise Exception(
            "Member was missing from list of previously claimed members, assuming renamed member.")


def _create_rank_string(rank, name, leaderboard_type, score):
    """
    :param rank: The member's leaderboard rank
    :param name: The member's name
    :param leaderboard_type: Name of the leaderboard that is being processed
    :param score: The member's submitted score
    :return: Returns a prettified string listing the member's name, rank and score in this leaderboard
    """
    num2words1 = {1: ':first_place:', 2: ':second_place:', 3: ':third_place:', 4: ':keycap_four:', 5: ':keycap_five:',
                  6: ':keycap_six:', 7: ':keycap_seven:', 8: ':keycap_eight:', 9: ':keycap_nine:', 10: ':keycap_ten:'}
    return """%s %s är placerad #%i i %s leaderboarden med %s poäng.\n""" % (
        num2words1.get(rank, ":asterisk:"), name, rank, leaderboard_type.capitalize(), score)


def _extract_score(leaderboard_entry):
    """
    :param leaderboard_entry: The member's entry in the leaderboard
    :return: Returns the score extracted from the member's entry
    """
    return leaderboard_entry.split(" ")[1]


# TODO: maybe send as embed?
# TODO: send list of ranks ordered from highest to lowest
async def _send_ranks(ctx, first_message):
    if first_message != "":
        await ctx.message.author.send(first_message)
        # await ctx.message.author.send(second_message)
        await ctx.send("Du har fått ett privatmeddelande med alla dina placeringar %s."
                 % ctx.message.author.mention)
    else:
        await ctx.send("Vi lyckades inte hitta dig bland några leaderboards %s. "
                 "Du verkar inte registrerat några poäng ännu." % ctx.message.author.mention)


class Ranks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ranks", pass_context=True, help="Kommandot ?ranks används för att skriva ut en lista med "
                                                            "dina placeringar i de olika leaderboards."
                                                            "\nExempel: ?ranks")
    async def ranks(self, ctx):
        nickname = ctx.message.author.display_name.lower()
        id_ = ctx.message.author.id


        # holds message to be sent to user, needs two separate messages due to Discord message restrictions
        first_message = ""

        missing_id, missing_name = _check_if_member_claimed(nickname, id_)
        await _handle_missing_information(ctx, missing_id, missing_name)

        for leaderboard_number, leaderboard in enumerate(common.LEADERBOARD_LIST[1:], 1):
            with open("leaderboards/%s.txt" % leaderboard) as leaderboard_file:
                for rank, line in enumerate(leaderboard_file, 1):
                    if nickname in line.lower():
                        # TODO: fix permanent solution to chat limit, dynamically split and send more messages
                        if leaderboard_number % 15 == 0:
                            await _send_ranks(ctx, first_message)
                            first_message = ""
                        else:
                            first_message += _create_rank_string(rank, ctx.message.author.mention, leaderboard, _extract_score(line))
        await _send_ranks(ctx, first_message)

    @ranks.error
    async def ranks_on_error(self, ctx, error):
        for dev in common.DEVELOPERS:
            traceback.print_exc()
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in RANKS command: {error}""")


def setup(bot):
    bot.add_cog(Ranks(bot))
