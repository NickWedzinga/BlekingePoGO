"""
Contains common code
"""

# list of channels in which Sneasel can trigger sneaselcommands
command_channel_list = ["leaderboards", "sneasel_commands", "support"]

# channel to send unit-test results to
test_results_channel = []

# list of all leaderboards
leaderboard_list = ['refresh', 'jogger', 'pikachu', 'battlegirl', 'pokedex', 'collector', 'scientist', 'breeder',
                    'backpacker', 'fisherman', 'youngster', 'berrymaster', 'gymleader', 'champion', 'battlelegend',
                    'ranger', 'unown', 'gentleman', 'pilot', 'totalxp', 'goldgyms', 'idol', 'greatleague',
                    'ultraleague', 'masterleague', 'acetrainer', 'cameraman', 'hero', 'purifier']

# list of channels that correspond to leaderboards
leaderboard_channels = []

# Developers: McMomo,
developers = [169688623699066880]

# used in global check to mute bot from spamming during tests
unittesting = False
