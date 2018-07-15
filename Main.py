import EventHandler

#Start the bot
EventHandler.startUp()
#Read message every loop,  act accordingly
EventHandler.checkMessages()
#Infinite blocking loop
EventHandler.client.run('')
EventHandler.client.close()

# TODO:
#Change icon

#LEADERBOARDS---------------------------------------------
#The leaderboard has been refreshed @mention
#you have reached #1 in the "P"ikachu, capitalize leaderboard_type
#?jogger should give format
#ta bort decimaler från Pikachu
#jogger 0, triggar refresh samma med pikachu 0, ändra till < 1 = "score too low" msg
#20000 övre gräns ska bero på vilken leaderboard det är som uppdateras
#möjlighet för komma som decimaldivider
#regex check i början så att username som kommer från discord endast innehåller a-z och 0-9
# ta bort begränsningen att sänka sin egna score?

#RANKS-----------------------------------------------
# Instead of McMOmo is #1, @McMomo is #1 user mention

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