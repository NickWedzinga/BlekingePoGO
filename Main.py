import EventHandler

#Start the bot
EventHandler.startUp()
#Read message every loop,  act accordingly
EventHandler.checkMessages()
#Infinite blocking loop
EventHandler.client.run('NDM1ODg1MDIyNTA0MDI2MTEy.Dbineg.scoWXTLQWPsJc64XXv8daggHk1U')
EventHandler.client.close()

# TODO:
#Change icon

#JOGGER---------------------------------------------
#

#?HELP
#----------------------------------------------------
#?delete. Format: ?delete leaderboard_type,name. Exempel: ?delete jogger, mcmomo
#?leadererboard type, score. Exempel: ?jogger, 3000
#?ranks to list your score in each leaderboard

#IMPORTERING
#---------------------------------------------------
#Ändra leaderboard channel ID i alla funktioners embed message + delete channel
#Ändra command channel ID i alla funktionskall
#Ändra role ID för admin under DELETE command (skriv "\Admin" för att få admin ID)