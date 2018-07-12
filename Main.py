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
# Give error messages in one specific channel, only take commands from that channel
# When updating score "Updated go check in #jogger if you're top 10"
# Update leaderboards in different channels
# submission approval (client.wait_for_message)
# delete commands
