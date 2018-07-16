import EventHandler

#Start the bot
EventHandler.startUp()
#Read message every loop,  act accordingly
EventHandler.checkMessages()
#Infinite blocking loop
with open("apitoken.txt","r") as apiFile:
	apitoken = apiFile.read()
EventHandler.client.run(apitoken)
EventHandler.client.close()

# TODO:
#GENERAL-----------------------------------------------------
#Change icon
#Svenska?

#LEADERBOARDS---------------------------------------------

#DELETE-----------------------------------------------------
#BRING BACK DELETE

#REFRESH----------------------------------------------------
#Rewrite to no longer post ?jogger 1, instead direct call? Maybe requires function

#RANKS-----------------------------------------------

#CLAIM----------------------------------------------
# claim nick, koppla till user.ID. DÅ kan folk med user.ID som inte matchar nick
# inte posta som denna nick.
# du har redan claimat namnet: %s, be admin ändra namn åt dig
# krävs 1h membership på server för name claim
#lägg in claim check i andra funtioner, seems like youve not claimed your nick yet...
#ADMIN_CLAIM----------------------------------------
# du har redan claimat namnet: %s, be admin ändra namn åt dig
 
#?HELP
#----------------------------------------------------
#?delete. Format: ?delete leaderboard_type,name. Exempel: ?delete jogger, mcmomo
#?leadererboard type, score. Exempel: ?jogger, 3000
#?ranks to list your score in each leaderboard
#ändra else invalid command till invalid command type ?help for commands

#IMPORTERING
#---------------------------------------------------
#Ändra leaderboard channel ID i alla funktioners embed message + delete channel
#Ändra command channel ID i alla funktionskall
#Ändra role ID för admin under DELETE command (skriv "\Admin" för att få admin ID)
#ctrl+f "message.channel", "message.channel.id", "46"