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


# LEADERBOARDS---------------------------------------------
# Lista på saker att fixa vid nya leaderboards:
#   Skapa Discord kanal
#   Skapa .txt fil på PC
#   Lägg till .txt i .gitignore + git push + git pull på PI
#   Skapa .txt fil på Pi
#   Lägg till i help
#   Lägg till i file loopen i admin_claim
#   Lägg till i delete list
#   Lägg till i list funktionens kommandolista
#   Lägg till enhet i leaderboards embeds
#   Lägg till enhet i ranks



# DELETE-----------------------------------------------------


# REFRESH----------------------------------------------------
# ?refresh ger inget error


# RANKS-----------------------------------------------


# LIST ----------------------------------------------------



# CLAIM----------------------------------------------
# Claimtiden buggar fortfarande, säger 1 minut kvar när man varit på
# servern i flera dagar. Utkommenterat atm.


# ADMIN_CLAIM----------------------------------------


# ?HELP ----------------------------------------------------



# IMPORTERING
# ---------------------------------------------------
# Ändra command channel ID i alla funktionskall
# Ändra role ID för admin under DELETE command (skriv "\Admin"
# Ändra role ID för admin function call för admin_claim command (skriv "\Admin")
# för att få admin ID)
# ctrl+f "message.channel", "message.channel.id", "46"
# skapa claimed kanal, alla andra kanaler kräver claimed role för att se
# claimedkanal får inte skrivas i av folk som är claimed
