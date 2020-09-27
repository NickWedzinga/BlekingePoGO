"""
Contains common code
"""

# connection to database
DATABASE_CONNECTION = None

# data tables
SCHEDULE_RAID = "configure__schedule_raid_channel"
SCHEDULE_WEEKLY = "configure__schedule_weekly"
ACTIVE_RAID_CHANNEL_OWNERS = "raid__active_channel_owners"
STATS_REPORTED_RAIDS = "stats__reported_raids"

# list of channels in which Sneasel can trigger sneaselcommands
COMMAND_CHANNEL_LIST = ["leaderboards", "sneasel_commands", "support", "momos_test_dungeon"]

# list of raid report channels
RAID_REPORT_CHANNEL_LIST = ["raids"]
RAID_ACTIVES_CHANNEL = "raids-active"

# raid egg types
RAID_EGG_TYPES = ["T1", "T3", "T5", "LEGENDARY", "MEGA"]

# channel to send test results to
TEST_RESULTS_CHANNEL = None

# list of all leaderboards
LEADERBOARD_LIST = ['jogger', 'pikachu', 'battlegirl', 'pokedex', 'collector', 'scientist', 'breeder',
                    'backpacker', 'fisher', 'youngster', 'berrymaster', 'gymleader', 'champion', 'battlelegend',
                    'ranger', 'unown', 'gentleman', 'pilot', 'totalxp', 'goldgyms', 'idol', 'greatleague',
                    'ultraleague', 'masterleague', 'acetrainer', 'cameraman', 'hero', 'purifier', 'bestbuddy']

# Developers: McMomo,
DEVELOPERS = [169688623699066880]

# used in global check to mute bot from spamming during tests
INTEGRATION_TESTING = False

# CP-Multiplier values form https://gamepress.gg/pokemongo/cp-multiplier
CPM_VALUES = {
    1:      0.094,
    1.5:    0.1351374318,
    2:      0.16639787,
    2.5:    0.192650919,
    3:      0.21573247,
    3.5:    0.2365726613,
    4:      0.25572005,
    4.5:    0.2735303812,
    5:      0.29024988,
    5.5:    0.3060573775,
    6:      0.3210876,
    6.5:    0.3354450362,
    7:      0.34921268,
    7.5:    0.3624577511,
    8:      0.3752356,
    8.5:    0.387592416,
    9:      0.39956728,
    9.5:    0.4111935514,
    10:     0.4225,
    10.5:   0.4329264091,
    11:     0.44310755,
    11.5:   0.4530599591,
    12:     0.4627984,
    12.5:   0.472336093,
    13:     0.48168495,
    13.5:   0.4908558003,
    14:     0.49985844,
    14.5:   0.508701765,
    15:     0.51739395,
    15.5:   0.5259425113,
    16:     0.5343543,
    16.5:   0.5426357375,
    17:     0.5507927,
    17.5:   0.5588305862,
    18:     0.5667545,
    18.5:   0.5745691333,
    19:     0.5822789,
    19.5:   0.5898879072,
    20:     0.5974,
    20.5:   0.6048236651,
    21:     0.6121573,
    21.5:   0.6194041216,
    22:     0.6265671,
    22.5:   0.6336491432,
    23:     0.64065295,
    23.5:   0.6475809666,
    24:     0.65443563,
    24.5:   0.6612192524,
    25:     0.667934,
    25.5:   0.6745818959,
    26:     0.6811649,
    26.5:   0.6876849038,
    27:     0.69414365,
    27.5:   0.70054287,
    28:     0.7068842,
    28.5:   0.7131691091,
    29:     0.7193991,
    29.5:   0.7255756136,
    30:     0.7317,
    30.5:   0.7347410093,
    31:     0.7377695,
    31.5:   0.7407855938,
    32:     0.74378943,
    32.5:   0.7467812109,
    33:     0.74976104,
    33.5:   0.7527290867,
    34:     0.7556855,
    34.5:   0.7586303683,
    35:     0.76156384,
    35.5:   0.7644860647,
    36:     0.76739717,
    36.5:   0.7702972656,
    37:     0.7731865,
    37.5:   0.7760649616,
    38:     0.77893275,
    38.5:   0.7817900548,
    39:     0.784637,
    39.5:   0.7874736075,
    40:     0.7903,
    41:     0.79530001,
    42:     0.8003,
    43:     0.8053,
    44:     0.81029999,
    45:     0.81529999
}

# Icon urls to leaderboards
MEDAL_ICON_URLS = {
    "acetrainer": "9/9c/AceTrainer_Gold.png",
    "backpacker": "b/bb/Backpacker_Gold.png",
    "battlegirl": "9/93/BattleGirl_Gold.png",
    "battlelegend": "6/61/BattleLegend_Gold.png",
    "berrymaster": "9/92/BerryMaster_Gold.png",
    "bestbuddy": "7/76/BestBuddy_Gold.png",
    "breeder": "b/b7/Breeder_Gold.png",
    "cameraman": "1/19/Cameraman_Gold.png",
    "champion": "2/20/Champion_Gold.png",
    "collector": "8/86/Collector_Gold.png",
    "fisher": "6/66/Fisher_Gold.png",
    "gentleman": "f/f0/Gentleman_Gold.png",
    "goldgyms": "/0/0a/Gym_Badge_Tier_Gold.png",
    "greatleague": "2/28/GreatLeague_Gold.png",
    "gymleader": "f/f9/GymLeader_Gold.png",
    "hero": "5/52/Hero_Gold.png",
    "idol": "9/9b/Idol_Gold.png",
    "jogger": "9/98/Jogger_Gold.png",
    "masterleague": "d/d7/MasterLeague_Gold.png",
    "pikachu": "9/94/PikachuFan_Gold.png",
    "pilot": "4/4e/Pilot_Gold.png",
    "pokedex": "4/43/Kanto_Gold.png",
    "purifier": "4/47/Purifier_Gold.png",
    "ranger": "7/77/Researcher_Gold.png",
    "scientist": "7/7c/Scientist_Gold.png",
    "totalxp": "b/bd/Pok%C3%A9mon_GO_Fest_Chicago_2017.png",
    "ultraleague": "5/5e/UltraLeague_Gold.png",
    "unown": "1/1b/Unown_Gold.png",
    "youngster": "9/94/Youngster_Gold.png",
}

# icon urls to raid eggs
RAID_EGG_ICON_URLS = {
    "T1": "https://vignette.wikia.nocookie.net/pokemongo/images/5/5a/Egg_Raid_Normal.png/",
    "T3": "https://vignette.wikia.nocookie.net/pokemongo/images/e/e3/Egg_Raid_Rare.png/",
    "T5": "https://vignette.wikia.nocookie.net/pokemongo/images/c/cd/Egg_Raid_Legendary.png",
    "LEGENDARY": "https://vignette.wikia.nocookie.net/pokemongo/images/c/cd/Egg_Raid_Legendary.png",
    "MEGA": "https://vignette.wikia.nocookie.net/pokemongo/images/c/c2/Egg_Raid_Mega.png"
}
