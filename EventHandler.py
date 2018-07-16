import discord
from discord.ext.commands import Bot
from discord.ext import commands
from discord import server
from datetime import datetime, timezone
import asyncio
import time
import re

Client = discord.Client()
client = commands.Bot(command_prefix = "?")
researchList = []
leaderboardList = []
commandChannel = client.get_channel('466563505462575106')
#chat_filter = ["MEW", "SNEASEL", "VALOR"]

#Could be useful for debugging, counts how many times jogger has been called this lifetime
#joggerCallsCounter = 0


def startUp():
	print("Starting..")
	@client.event
	async def on_ready():
		print('Logged in as')
		print(client.user.name)
		print(client.user.id)
		print("Ready for action")
		print('------')


def checkMessages(id_list):
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
			await client.send_message(message.channel, "I still sänd messages! :sweat_smile:")

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
		
		#REFRESH, Format: ?refresh LEADERBOARD_TYPE
		elif(message.content.upper().startswith('?REFRESH')):
			leaderboard_type = message.content.lower().split(" ",1)[1]
			leaderboard_list = ["jogger","pikachu"]

			if leaderboard_type in leaderboard_list:
				await client.send_message(message.channel, "?%s 1"%leaderboard_type)
			else:
				await client.send_message(message.channel, "That leaderboard does not exist.")
			#sneasel says ?jogger 1
			#sneasel says ?pika 1

		#LEADERBOARDS Format: ?LEADERBOARD_TYPE, SCORE
		elif (message.content.upper().startswith('?JOGGER') or message.content.upper().startswith('?PIKACHU')) and message.channel.id == '466563505462575106':
			joggerTrue = False
			pikachuTrue = False

			upperLimit = 0

			#Which leaderboard the user is updating
			leaderboard_type = message.content.lower().split(" ",1)[0]
			leaderboard_type = leaderboard_type[1:]

			#Score part of string
			try:
				tempScore = message.content.lower().split(" ",1)[1]
			except IndexError: #User only typed ?LEADERBOARD_TYPE
				await client.send_message(message.channel, "The correct use of %s is ?%s 'SCORE'. \n*Example: ?jogger 2500*" % (leaderboard_type,leaderboard_type))

			#Replace possible commas with dots
			tempScore = str(tempScore.replace(",","."))

			if leaderboard_type == "jogger":
				joggerTrue = True
				upperLimit=20000
			elif leaderboard_type == "pikachu":
				pikachuTrue = True
				upperLimit=5000

			tempList = []
			notUpdated = True
			skipUpdate = False
			current_dt = datetime.now()
			floatError = False
			scoreUpdated = False
			sneaselRefresh = False
			topThree = False
			newTopOne = False
			newRank = 0
			currentRank = 0
			currentScore = 0
			insertedIndex = 0

			#Check if score is numbers only
			try: 
				float(tempScore)
			except ValueError:
				await client.send_message(message.channel, "Score in numbers only. *Format: ?LEADERBOARD_TYPE SCORE*")
				floatError = True			
			
			if not floatError:
				tempScore = float(tempScore)
				p = re.compile('\d+(\.\d+)?')
				stringPattern=r'[^\.A-Za-z0-9]'
				#Check for illegal nickname symbols, + ensures min size == 1
				if re.search(stringPattern, message.author.display_name) and not message.author.display_name.lower() == "sneasel bot":
					await client.send_message(message.channel, "Discord nickname contains illegal character %r, please change it to match your Pokémon Go nickname."%message.author.display_name)
				elif not p.match(str(tempScore)):
					await client.send_message(message.channel, "Error: Illegal characters in score. *Format: ?LEADERBOARD_TYPE SCORE*")
				elif len(message.author.display_name) > 15:
					await client.send_message(message.channel, "Error: Name should be shorter than 15 characters, please updated your server nickname. Ask admins for help if you're not sure how to do that.")
				else:
					#Create temp leaderboardList to be inserted if applicable
					tempList.append(message.author.display_name)
					tempList.append(tempScore)
					tempList.append(current_dt.date())

					#Check if Sneasel is trying to refresh list
					if str(message.author.display_name.lower()) == "sneasel bot":
						#print("%ssneasel bot"%(str(message.author.display_name.lower())))
						print("Sneasel is trying to refresh")
						sneaselRefresh = True
						async for x in client.logs_from(message.channel, 1):
							try:
								await client.delete_message(x)
							except:
								print("Somehow failed to delete message.")

						await asyncio.sleep(1)

					#Cast entry number to float
					if tempScore > upperLimit:
						await client.send_message(message.channel, "Score too high.")
					elif tempScore < 1:
						await client.send_message(message.channel, "Score too low to be submitted.")
					elif floatError == True:
						await client.send_message(message.channel, "Score in numbers only.")
					else:
						with open("%s.txt"%leaderboard_type) as file:
							leaderboardList = [line.split(" ") for line in file]
						if not sneaselRefresh:
							#Check if player is already in standings, update
							found = False
							for index, elem in enumerate(leaderboardList):
								#If player already exists
								if message.author.display_name.lower() == elem[0].lower() and found == False:
									#Score is higher than previously submitted
									if found == False: #tempScore > float(elem[1]) and 
										found = True
										#Update player stats
										leaderboardList[index][1] = tempScore
										leaderboardList[index][2] = current_dt.date()
										tempList = leaderboardList.pop(index) #remove updated score

										notUpdated = False
										#Move player to correct position
										moved = False
										for idx, elm in enumerate(leaderboardList):
											if moved:
												break
											elif tempScore > float(elm[1]):
												#Insert updated score
												if pikachuTrue:
													tempList[1] = int(tempList[1])
												insertedIndex = idx
												leaderboardList.insert(idx, tempList) #insert updated score
												newRank = idx
												moved = True
												scoreUpdated = True
												#Updated score gets top one, was not top one before
												if idx < 1 and index > 0:
													newTopOne = True
												#Updated score gets top three, was not top three
												elif idx < 3 and index > 2:
													topThree = True
									else:
										skipUpdate = True
										#await client.send_message(message.channel, "To update your score, it has to be higher than your previous submission.")

							#Player is missing, insert new entry
							if notUpdated and not skipUpdate:
								insertedBool = False
								for index, elem in enumerate(leaderboardList):
									if tempScore >= float(elem[1]) and insertedBool == False:
										if pikachuTrue:
											tempList[1] = int(tempList[1])
										insertedIndex = index
										leaderboardList.insert(index, tempList)
										insertedBool = True
										scoreUpdated = True
										newRank = index
										#New score is top one
										if index < 1:
											newTopOne = True
										#New score is among top three
										if index < 3:
											topThree = True

						file = open("%s.txt"%leaderboard_type, "w")
						for item in leaderboardList:
							item2 = ' '.join(str(x) for x in item)
							if item == tempList:
								file.write("%s\n" % item2)
							else:
								file.write("%s" % item2)
						file.close()

					#Medal images: http://pokemongo.wikia.com/wiki/Medals
					#https://pokemongo.gamepress.gg/sites/pokemongo/files/2018-02/Badge_Walking_GOLD_01.png
					unitString = ""
					if joggerTrue:
						embed = discord.Embed(title="Leaderboard Karlskrona: Jogger \n", color=0xff9900)
						embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/98/Jogger_Gold.png/revision/latest?cb=20161013235539")
						embed.set_footer(text = "The remaining ranks are hidden, find out your rankings by typing ?ranks")
						embed.add_field(name="\u200b", value = "\u200b", inline=False)
						channel2 = client.get_channel('466913214656020493')
						unitString = "km"
					elif pikachuTrue:
						embed = discord.Embed(title="Leaderboard Karlskrona: Pikachu \n", color=0xff9900)
						embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/94/PikachuFan_Gold.png/revision/latest?cb=20161013235542")
						embed.set_footer(text = "The remaining ranks are hidden, find out your rankings by typing ?ranks")
						embed.add_field(name="\u200b", value = "\u200b", inline=False)
						channel2 = client.get_channel('467754615413407745')

					currentRank = 0
					currentScore = 0
					currentRankList = []
					#Add fields to be presented in table, fill with data
					for index, elem in enumerate(leaderboardList):
						currentRankList.append(index+1)
						if index < 10:
							#Score not same as previous user, dont update score index rank
							if not currentScore == float(elem[1]):
								currentRank = index+1
								currentScore = float(elem[1])
							else:
								currentRankList[index] = currentRank
								print(currentRankList)
		
							#Pikachu can't have decimals
							if pikachuTrue:
								embed.add_field(name="%i. %s - %i %s" % (int(currentRank), elem[0], int(elem[1]), unitString), value = "Updated: %s" % (elem[2]), inline=True)
							else:
								embed.add_field(name="%i. %s - %.1f %s" % (int(currentRank), elem[0], float(elem[1]), unitString), value = "Updated: %s" % (elem[2]), inline=True)

					async for x in client.logs_from(channel2, 10):
						try:
							await client.delete_message(x)
						except:
							print("somehow failed to delete message")

					await asyncio.sleep(1)
					if newTopOne:
						await client.send_message(message.channel, ":crown: :first_place: CONGRATULATIONS %s, you have reached #%i in the %s leaderboard. \nPlease send an in game screenshot to any admin so they may confirm your entry." % (message.author.mention, currentRankList[insertedIndex], leaderboard_type.capitalize()))
					elif topThree:
						await client.send_message(message.channel, ":crown: Congratulations %s on your #%i placing in the %s leaderboard, please send an in game screenshot to any admin so they may confirm your entry." % (message.author.mention,currentRankList[insertedIndex], leaderboard_type.capitalize()))
					elif scoreUpdated:
						await client.send_message(message.channel, "Congratulations %s, you placed #%i in the %s leaderboard. Check %s to see the top 10." % (message.author.mention,currentRankList[insertedIndex], leaderboard_type.capitalize(), channel2.mention))
					await client.send_message(message.channel, "The leaderboard has been refreshed.")
					await client.send_message(channel2, embed=embed)
				
		#List ranks across leaderboards
		elif message.content.upper().startswith('?RANKS') and message.channel.id == '466563505462575106':
			nickname = message.author.display_name
			tempList = []
			leaderboard_list = ["jogger","pikachu"]
			unitString = ""
			currentRank = 0
			currentScore = 0
			currentRankList = []

			num2words1 = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', \
            6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', \
            11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', \
            15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen'}

            #Loop through leaderboard types
			for item in leaderboard_list:
				if item == "jogger":
					unitString = "km"
				elif item == "pikachu":
					unitString = "catches"
				leaderboard_file = open("%s.txt"%item, "r")
				#Loop through file
				for index, line in enumerate(leaderboard_file):
					line = line.split(" ")

					#If score not same as previous player, update rank
					if not float(currentScore) == float(line[1]):
						currentRank = index+1
						currentScore = float(line[1])

					if line[0].lower() == nickname.lower():
						localScore = round(float(line[1]),1)
						if item == "pikachu":
							localScore = int(localScore)
						#print("WE HAVE A MATCH!")
						if(currentRank == 1):
							await client.send_message(message.channel, ":first_place: %s is ranked \#%i in the %s leaderboards with a score of %s %s." % (message.author.mention, currentRank, item.capitalize(), localScore,unitString))
						elif(currentRank == 2):
							await client.send_message(message.channel, ":second_place: %s is ranked \#%i in the %s leaderboards with a score of %s %s." % (message.author.mention, currentRank, item.capitalize(), localScore,unitString))
						elif(currentRank == 3):
							await client.send_message(message.channel, ":third_place: %s is ranked \#%i in the %s leaderboards with a score of %s %s." % (message.author.mention, currentRank, item.capitalize(), localScore,unitString))
						elif(currentRank > 3 and currentRank < 11):
							await client.send_message(message.channel, ":%s: %s is ranked \#%i in the %s leaderboards with a score of %s %s." % (num2words1[index+1].lower(),message.author.mention, currentRank, item.capitalize(), localScore,unitString))
						elif currentRank > 10:
							await client.send_message(message.channel, ":asterisk: %s is ranked \#%i in the %s leaderboards with a score of %s %s." % (message.author.mention, currentRank, item.capitalize(), localScore,unitString))
						else:
							await client.send_message(message.channel, "%s is not ranked in the %s leaderboards, submit a score by typing ?%s 'YOUR_SCORE'." % (message.author.mention, item.capitalize(), item))
							

		#DELETE, admins may delete leaderboard entries Format: ?delete leaderboard_type, name_to_delete
		#elif message.content.upper().startswith('?DELETE') and message.channel.id == '466563505462575106':
			#Which leaderboard the user is updating
		#	leaderboard_type = message.content.lower().split(" ",1)[0]
		#	leaderboard_type = leaderboard_type[1:] #removes "?"

			#Name to delete part of string
		#	deleteName = message.content.lower().split(" ",1)[1]

		#	print(leaderboard_type)
		#	print(deleteName)

			#beautiful variable name
			#linesToKeepInFile = []
			#deleteIndex = 0

			#Check if author is admin (TESTROLE)
			#if '435908470936698910' in [role.id for role in message.author.roles]:
				#Admin is trying to remove entry from Leaderboard
			#	if deleteName.lower() == "jogger":
			#		dltFile = open("%s.txt"%leaderboard_type, "r")
			#		for index, line in enumerate(dltFile):
			#			splitLine = line.split(' ')
			#			#Found name trying to delete from file in file
			#			if splitLine[0].lower() == deleteName.lower():
			#				await client.send_message(message.channel, "%s found, deleting %s from the %s leaderboard." % (deleteName,deleteName,leaderboard_type))
			#			else:
			#				linesToKeepInFile.append(line)
			#		#Write back lines with the exception of the deleted element
			#		dltFile = open("%s.txt"%leaderboard_type, "w")
			#		for elem in linesToKeepInFile:
			#			dltFile.write(elem)
			#		await client.send_message(message.channel, "?%s 1"%leaderboard_type)
			#else:
			#	await client.send_message(message.channel, "Only admins are allowed to delete entries, please contact an admin.")


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