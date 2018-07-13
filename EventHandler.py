import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import server
from datetime import datetime, timezone
import asyncio
import time
import numpy as np
import re

Client = discord.Client()
client = commands.Bot(command_prefix = "?")
researchList = []
joggerList = []
commandChannel = client.get_channel('466563505462575106')
#chat_filter = ["MEW", "SNEASEL", "VALOR"]

def startUp():
	print("Starting..")
	@client.event
	async def on_ready():
		print('Logged in as')
		print(client.user.name)
		print(client.user.id)
		print("Ready for action")
		print('------')


def checkMessages():
	print("Checking for messages..")
	@client.event
	async def on_message(message):
		#global researchList

		#Check if sentence contains certain words
		#filtercontents = message.content.split(" ")
		#for word in filtercontents:
		#	if word.upper() == chat_filter[0]:
		#		await client.send_message(message.channel, "Mew är en mus :smirk:")
		#	elif word.upper() == chat_filter[1]:
		#		await client.send_message(message.channel, "Yes, you called? :smirk:")
		#	elif word.upper() == chat_filter[2]:
		#		await client.send_message(message.channel, "VALOR BABYYYY :fire:")

		#Test if bot is still responsive
		if message.content.upper().startswith('?TEST') and message.channel.id == '466563505462575106':
			await client.send_message(message.channel, "I still send messages! :sweat_smile:")

		#Help, lists available commands
		#elif message.content.upper().startswith('?HELP'):
		#	args = message.content.split(' ')
		#	if len(args) > 1:
		#		if args[1] == 'research':
		#			await client.send_message(message.channel, "**Usage:** *?research* followed by *Pokéstop*, *Quest type* and *Reward*. Separated with commas")
		#			await client.send_message(message.channel, "**Example:** *?research John Hankes Mansion, Hatch 5 eggs, Chansey*")
		#		elif args[1] == 'repeat':
		#			await client.send_message(message.channel, "**Usage:** ?repeat followed by the word/ sentence you want Sneasel to repeat.")
		#		elif args[1] == 'list':
		#			await client.send_message(message.channel, "**Usage:** ?list research, to retrieve a list of today's reported quests.")
		#		else:
		#			await client.send_message(message.channel, "Command not found, please use lowercase letters for the commands.")
		#	elif len(args) == 1:
		#		await client.send_message(message.channel, "**Commands:**")
		#		await client.send_message(message.channel, "*?research X, Y, Z*")
		#		await client.send_message(message.channel, "*?list research*")
		#		await client.send_message(message.channel, "*?repeat X*")
		#		await client.send_message(message.channel, "For more detail on a specific command please type ?help followed by the requested command, **Example:** *?help research*")
		
		#JOGGER, updates Jogger leaderboards. Format: ?jogger DISTANCE
		elif message.content.upper().startswith('?JOGGER') and message.channel.id == '466563505462575106':
			tempScore = message.content
			tempScore = tempScore[8:] #remove "?jogger "
			tempJoggerList = []
			notUpdated = True
			skipUpdate = False
			current_dt = datetime.now()
			floatError = False

			try: 
				float(tempScore)
			except ValueError:
				await client.send_message(message.channel, "Score in numbers only, split decimal with '.' *Format: ?jogger SCORE.decimals*")
				floatError = True			
			
			if not floatError:
				tempScore = float(tempScore)
				p = re.compile('\d+(\.\d+)?')
				#.match() needs item to be string
				if not p.match(str(tempScore)):
					await client.send_message(message.channel, "Error: Illegal characters in score. *Format: ?jogger SCORE.decimals*")
				elif len(message.author.display_name) > 15:
					await client.send_message(message.channel, "Error: Name should be shorter than 15 characters, please updated your server nickname. Ask admins for help if you're not sure how to do that.")
				else:
					#Create temp joggerlist to be inserted if applicable
					tempJoggerList.append(message.author.display_name)
					tempJoggerList.append(tempScore)
					tempJoggerList.append(current_dt.date())#strftime("%Y-%m-%d %H:%M:%S"))

					

					#Cast entry number to float
					#tempScore = float(tempScore)
					if tempScore > 20000:
						await client.send_message(message.channel, "Score too high.")
					elif tempScore < 0:
						await client.send_message(message.channel, "Score can't be negative.")
					elif floatError == True:
						await client.send_message(message.channel, "Score in numbers only.")
					else:
						with open("jogger.txt") as file:
							joggerList = [line.split(" ") for line in file]

						#Check if player is already in standings, update
						found = False
						for index, elem in enumerate(joggerList):
							#If player already exists
							#print(message.author.display_name)
							#print(elem[0])
							#print("Comparing %s and %s" % (message.author.display_name, elem[0]))
							if message.author.display_name.lower() == elem[0].lower() and found == False:
								print("MATCH FOUND!")
								#Score is higher than previously submitted
								if tempScore > float(elem[1]) and found == False:
									print("%f%f" % (tempScore, float(elem[1])))
									print("Score is bigger than last")
									found = True
									#print("Similar player found: %s" % (tempJoggerList[0]))
									#Update player stats
									#joggerList[index][1] = float(tempJoggerList[1])
									joggerList[index][1] = tempScore
									joggerList[index][2] = current_dt.date()
									tempJoggerList = joggerList.pop(index) #remove updated score

									notUpdated = False
									#Move player to correct position
									moved = False
									for idx, elm in enumerate(joggerList):
										#print("Loop through joggerList for placing %f, scores: %f" %(tempScore, float(elm[1])))
										if moved:
											break
										elif tempScore > float(elm[1]):
											#print("Found place to fit at index %i updated score %f, because %f is >= %s" % (idx, tempScore, tempScore, elm[1]))
											joggerList.insert(idx, tempJoggerList) #insert updated score
											moved = True
								else:
									skipUpdate = True
									await client.send_message(message.channel, "To update your score, it has to be higher than your previous submission.")

						#Player is missing, insert new entry
						if notUpdated and not skipUpdate:
							insertedBool = False
							for index, elem in enumerate(joggerList):
								if tempScore >= float(elem[1]) and insertedBool == False:
									joggerList.insert(index, tempJoggerList)
									insertedBool = True

						file = open("jogger.txt", "w")
						for item in joggerList:
							item2 = ' '.join(str(x) for x in item)
							if item == tempJoggerList:
								file.write("%s\n" % item2)
							else:
								file.write("%s" % item2)
						file.close()

					embed = discord.Embed(title="Leaderboard Karlskrona: Jogger \n", color=0xff9900)
					embed.set_thumbnail(url="https://pokemongo.gamepress.gg/sites/pokemongo/files/2018-02/Badge_Walking_GOLD_01.png")
					embed.set_footer(text = "The remaining standings are hidden, find out your standings by typing ?standings")
					embed.add_field(name="\u200b", value = "\u200b", inline=False)

					#Add fields to be presented in table, fill with data
					for index, elem in enumerate(joggerList):
						if index < 10:
							embed.add_field(name="%i. %s - %s km " % (index+1, elem[0], elem[1]), value = "Updated: %s" % (elem[2]), inline=True)
					
					channel2 = client.get_channel('466913214656020493')

					async for x in client.logs_from(channel2, 10):
						try:
							await client.delete_message(x)
						except:
							print("somehow failed to delete message")

					await asyncio.sleep(1)

					await client.send_message(message.channel, "The leaderboard has been refreshed.")
					await client.send_message(channel2, embed=embed)
				
		#List ranks across leaderboards
		elif message.content.upper().startswith('?RANKS') and message.channel.id == '466563505462575106':
			print("Nibba we in")
			nickname = message.author.display_name
			tempJoggerList = []

			joggerFile = open("jogger.txt", "r")
			for index, line in enumerate(joggerFile):
				line = line.split(" ")
				#print("Line in loop: %s" % line)
				#print("Line[0].lower() is: %s" % line[0].lower())
				#print("Nickname.lower() is: %s" % nickname.lower())
				if line[0].lower() == nickname.lower():
					#print("WE HAVE A MATCH!")
					if(index+1 == 1):
						await client.send_message(message.channel, ":first_place: %s is ranked \#%i in the jogger leaderboards with a distance of %.1f km." % (nickname, index+1, float(line[1])))
					elif(index+1 == 2):
						await client.send_message(message.channel, ":second_place: %s is ranked \#%i in the jogger leaderboards with a distance of %.1f km." % (nickname, index+1, float(line[1])))
					elif(index+1 == 3):
						await client.send_message(message.channel, ":third_place: %s is ranked \#%i in the jogger leaderboards with a distance of %.1f km." % (nickname, index+1, float(line[1])))
					else:
						await client.send_message(message.channel, "%s is ranked \#%i in the jogger leaderboards with a distance of %.1f km." % (nickname, index+1, float(line[1])))

			#with open("jogger.txt") as file:
			#			joggerList = [line.split(" ") for line in file]

			
		#Add quest to list
		#elif message.content.upper().startswith('?RESEARCH'):
		#	args = message.content
		#	args = args[10:] #remove "?research "
		#	args2 = args.split(",")
		#	userID = message.author.name
			
			#Clean up
		#	if len(args2) == 3:
		#		tempList = []
		#		for elem in args2:
		#			if elem[0] == " ":
		#				elem = elem[1:]
		#			tempList.append(elem)
		#		tempList.append(userID)
		#		await client.send_message(message.channel, "**Pokéstop:** %s, **Quest:** %s, **Reward:** %s, **Added by:** %s" % (tempList[0], tempList[1], tempList[2], userID))
		#		researchList.append(tempList)
		#	else:
		#		await client.send_message(message.channel, "Too few or too many arguments..")

		#List quests
		#elif message.content.upper().startswith('?LIST RESEARCH'):
		#	await client.send_message(message.channel, "**Today's reported quests:** \n")
		#	for quest in researchList:
		#		await client.send_message(message.channel, ":gem: **Pokéstop name:** %s, **Quest type:** %s, **Reward:** %s, **Added by:** %s" % (quest[0], quest[1], quest[2], quest[3]))

		#Repeater
		#elif  message.content.upper().startswith('?REPEAT'):
		#	args = message.content.split(' ')
		#	await client.send_message(message.channel, "%s" % (" ".join(args[1:])))

		#E U R E K A
		elif message.content.upper().startswith('EUREKA') and message.channel.id == '466563505462575106':
			await client.send_message(message.channel, "We did it! :smile:")

		#Check if message author has a certain role
		#elif message.content.upper().startswith('?ADMIN'):
		#	if '435908470936698910' in [role.id for role in message.author.roles]:
		#		await client.send_message(message.channel, "Yes, you are admin")
		#	else:
		#		await client.send_message(message.channel, "No, you are not admin, unlucky.")

		#Last if statement, invalid command
		elif message.content.upper().startswith('?') and message.channel.id == '466563505462575106':
			await client.send_message(message.channel, "Invalid command :sob:")