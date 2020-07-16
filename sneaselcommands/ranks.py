import traceback

from discord.ext import commands

import common


async def _check_if_member_claimed(ctx, nickname, id):
    """
    :param nickname: Nickname of the member
    :param id: Id of the member
    :return: Checks if the member's nickname and id match the previously collected information
    """
    missing_id = missing_name = False
    with open("textfiles/idclaims.txt") as file:
        for entry in file:
            if nickname in entry.lower():
                if id not in entry.lower():
                    missing_id = True
            if id in entry.lower():
                if nickname not in entry.lower():
                    missing_name = True
    await _handle_missing_information(ctx, missing_id, missing_name)


async def _handle_missing_information(ctx, missing_id, missing_name):
    """
    :param ctx:
    :param missing_id:
    :param missing_name:
    :return:
    """
    if missing_id:
        await ctx.send("Ditt användarnamn matchar inte det du registrerat tidigare, "
                 "har du skapat ett nytt Discord-konto med samma namn? Ta kontakt med valfri admin.")
        raise Exception(
            "Member was missing from list of previously claimed members, assuming new Discord user with same name.")
    elif missing_name:
        await ctx.send("Ditt användarnamn matchar inte det du registrerat tidigare, "
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
    return """%s %s is ranked #%i in the %s leaderboard with a score of %s.""" % (
        num2words1.get(rank, ":asterisk:"), name, rank, leaderboard_type.capitalize(), score)


def _build_rank_message(message_list, from_, to_):
    """
    :param message_list: Concatenated list of all detailed rank messages
    :param from_: Index in the list to start at
    :param to_: Index in the list to end at
    :return: Takes a list of strings and returns a joined string with a newline denominator
    """
    return "\n".join(message_list[from_:to_+1])


def _extract_score(leaderboard_entry):
    """
    :param leaderboard_entry: The member's entry in the leaderboard
    :return: Returns the score extracted from the member's entry
    """
    return leaderboard_entry.split(" ")[1]


def _every_fifteenth_or_last(number, last):
    """
    :param number: Current index in iteration of leaderboard list
    :param last: Index of last iteration of leaderboard list
    :return: Returns True every 15th index and for the last index
    """
    if (number != 0 and number % 15 == 0) or number == last:
        return True
    return False


# TODO: maybe send as embed?
# TODO: send list of ranks ordered from highest to lowest
async def _send_ranks(ctx, concat_message):
    """
    :param ctx: The member's sent message context
    :param concat_message: The message to send to the member, contains details on rank and score for each leaderboard
    :return: Sends message with leaderboard details to the member that requested them
    """
    previously_sent = 0
    for num, msg in enumerate(concat_message):
        if _every_fifteenth_or_last(num, len(concat_message) - 1):
            await ctx.message.author.send(_build_rank_message(concat_message, previously_sent, num))
            previously_sent += 16
    await ctx.send("Du har fått ett privatmeddelande med alla dina placeringar %s." % ctx.message.author.mention)


class Ranks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ranks", help="Kommandot ?ranks används för att skriva ut en lista med "
                                                            "dina placeringar i de olika leaderboards."
                                                            "\nExempel: ?ranks")
    async def ranks(self, ctx):
        nickname = ctx.message.author.display_name.lower()
        id_ = str(ctx.message.author.id)
        concat_message = []

        await _check_if_member_claimed(ctx, nickname, id_)

        for leaderboard_number, leaderboard in enumerate(common.LEADERBOARD_LIST[1:], 1):
            with open("leaderboards/%s.txt" % leaderboard) as leaderboard_file:
                for rank, line in enumerate(leaderboard_file, 1):
                    if nickname in line.lower():
                        concat_message.append(
                            _create_rank_string(
                                rank=rank,
                                name=ctx.message.author.mention,
                                leaderboard_type=leaderboard,
                                score=_extract_score(line)
                            )
                        )
        await _send_ranks(ctx, concat_message)

    @ranks.error
    async def ranks_on_error(self, ctx, error):
        for dev in common.DEVELOPERS:
            traceback.print_exc()
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in RANKS command: {error}""")


def setup(bot):
    bot.add_cog(Ranks(bot))
