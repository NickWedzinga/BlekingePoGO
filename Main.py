import EventHandler

# Start the bot
EventHandler.startup()
# Read message every loop,  act accordingly

# Sneasel List
id_list = []
with open("version.txt", "r") as versionFile:
    version = versionFile.read()
# Dev list: command channel[0], jogger[1], pikachu[@],
#           support[3], battlegirl[4], collector[5],
#
if version == "1":
    id_list = ['466563505462575106', '466913214656020493', '467754615413407745',
               '468760503125147648', '469079191002939415']
elif version == "0":
    id_list = ['469095507759726603', '469095668137459712', '469095701947875338',
               '342760722058706945', '469095719178076170']
print("Version: %s" % version)
EventHandler.checkMessages(id_list)
# Infinite blocking loop
with open("apitoken.txt", "r") as apiFile:
    apitoken = apiFile.read()
EventHandler.client.run(apitoken)
EventHandler.client.close()

# GENERAL-----------------------------------------------------
# test sending backup txt from pi to pc


# OVERALL-----------------------------------------------------
# Funkar bara när spelaren är rankad i samtliga leaderboards

# När spelaren uppdaterar en leaderboard så uppdateras även overall

# score = index i samtliga leaderboards / antal leaderboards


# LEADERBOARDS---------------------------------------------
# Lista på saker att fixa vid nya leaderboards:
#   Skapa Discord kanal
#   Skapa .txt fil på PC (Sneasel 1 2018-07-11)
#   Lägg till .txt i .gitignore + git push + git pull på PI
#   Skapa .txt fil på Pi
#   Lägg till i checkMessage leaderboard_list
#   Lägg till if pikachuTrue or battlegirl: int()
#   Lägg till joggerTrue och if joggerTrue i leaderboards
#   Lägg till embed icon i leaderboards
#   Lägg till channel ID i main.py, uppdatera channel2 under embeds
#   Lägg till enhet i ranks

# Leaderboards to add:
#Pokedex
#Collector
#Scientist
#Breeder
#Backpacker
#Fisherman
#Battle Girl
#Youngster
#Berry Master
#Gym Leader
#Champion
#Battle Legend
#Pokémon Ranger
#Unown
#Idol
#Gentleman
#Pilot


# DELETE-----------------------------------------------------


# REFRESH----------------------------------------------------
# ?refresh ger inget error


# RANKS-----------------------------------------------
# ?rank borde ge samma output

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
