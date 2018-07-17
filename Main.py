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
# botten randomly la av

# LEADERBOARDS---------------------------------------------
# Lägg till Battle Girl, gitignore, skapa .txt filer på PI, lägg till i help, loop through new files in admin claim
# lägg till i delete list

# GRATULERAT, inte korrekt svenska?


# DELETE-----------------------------------------------------


# REFRESH----------------------------------------------------


# RANKS-----------------------------------------------


# CLAIM----------------------------------------------
# Gör så att om någon skriver vad som helst som inte är ?claim i claim så tip

# Claimtiden buggar fortfarande, säger 1 minut kvar när man varit på
# servern i flera dagar. Utkommenterat atm.


# ADMIN_CLAIM----------------------------------------


# ?HELP
# ----------------------------------------------------


# IMPORTERING
# ---------------------------------------------------
# Ändra command channel ID i alla funktionskall
# Ändra role ID för admin under DELETE command (skriv "\Admin"
# Ändra role ID för admin function call för admin_claim command (skriv "\Admin")
# för att få admin ID)
# ctrl+f "message.channel", "message.channel.id", "46"
# skapa claimed kanal, alla andra kanaler kräver claimed role för att se
# claimedkanal får inte skrivas i av folk som är claimed
