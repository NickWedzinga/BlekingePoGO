"""
Contains common code
"""
import traceback
from Instance import bot


# list of channels in which Sneasel can trigger sneaselcommands
command_channel_list = ["leaderboards", "sneasel_commands", "support"]

# channel to send unit-test results to
test_results_channel = []#bot.get_channel(640964820732084233)

# list of all leaderboards
leaderboard_list = ['refresh', 'jogger', 'pikachu', 'battlegirl', 'pokedex', 'collector', 'scientist', 'breeder',
                    'backpacker', 'fisherman', 'youngster', 'berrymaster', 'gymleader', 'champion', 'battlelegend',
                    'ranger', 'unown', 'gentleman', 'pilot', 'totalxp', 'goldgyms', 'idol', 'greatleague',
                    'ultraleague', 'masterleague', 'acetrainer', 'cameraman', 'hero', 'purifier']

# list of channels that correspond to leaderboards
leaderboard_channels = []

# Developers: McMomo,
developers = [169688623699066880]

current_leaderboard = ""


async def validate(method_to_validate):
    try:
        method_to_validate()
    except Exception as e:
        traceback.print_exc()
        for dev in developers:
            user = bot.get_user(dev)
            await user.send(f"""Error: {e}""")