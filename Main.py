import EventHandler

# Start the bot
EventHandler.startup()
# Read message every loop,  act accordingly

# Sneasel List
id_list = []
# Dev list: command channel, jogger, pikachu, claim channel,
# if EventHandler.client.display_name.lower() == "dev bot":
id_list = ['466563505462575106', '466913214656020493', '467754615413407745', '468760503125147648']

EventHandler.checkMessages(id_list)
# Infinite blocking loop
with open("apitoken.txt", "r") as apiFile:
    apitoken = apiFile.read()
EventHandler.client.run(apitoken)
EventHandler.client.close()

# GENERAL-----------------------------------------------------
# Ikoner till embeds lokalt istället för url


# LEADERBOARDS---------------------------------------------
# Lägg till Battle Girl, gitignore, skapa .txt filer på PI


# DELETE-----------------------------------------------------


# REFRESH----------------------------------------------------


# RANKS-----------------------------------------------

# CLAIM----------------------------------------------
# skriv pm

# krävs 1h membership på server för name claim

# ADMIN_CLAIM----------------------------------------
# ?admin_claim @mention nickname. Fetch user ID from mention, look for old nick, change


# ?HELP
# ----------------------------------------------------
# ?delete. Format: ?delete leaderboard_type,name. Exempel: ?delete jogger, momo
# ?leadererboard type, score. Exempel: ?jogger, 3000
# ?ranks to list your score in each leaderboard
# ändra else invalid command till invalid command type ?help for commands


# IMPORTERING
# ---------------------------------------------------
# Ändra command channel ID i alla funktionskall
# Ändra role ID för admin under DELETE command (skriv "\Admin"
# för att få admin ID)
# ctrl+f "message.channel", "message.channel.id", "46"
# skapa claimed kanal, alla andra kanaler kräver claimed role för att se
# claimedkanal får inte skrivas i av folk som är claimed
