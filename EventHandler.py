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

			#Which leaderboard the user is updating
			leaderboard_type = message.content.lower().split(" ",1)[0]
			leaderboard_type = leaderboard_type[1:]

			#Score part of string
			tempScore = message.content.lower().split(" ",1)[1]

			if leaderboard_type == "jogger":
				joggerTrue = True
			elif leaderboard_type == "pikachu":
				pikachuTrue = True

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

			try: 
				float(tempScore)
			except ValueError:
				await client.send_message(message.channel, "Score in numbers only, split decimal with '.' *Format: ?leaderboard_type SCORE.decimals*")
				floatError = True			
			
			if not floatError:
				tempScore = float(tempScore)
				p = re.compile('\d+(\.\d+)?')
				#.match() needs item to be string
				if not p.match(str(tempScore)):
					await client.send_message(message.channel, "Error: Illegal characters in score. *Format: ?leaderboard_type SCORE.decimals*")
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
					if tempScore > 20000:
						await client.send_message(message.channel, "Score too high.")
					elif tempScore < 0:
						await client.send_message(message.channel, "Score can't be negative.")
					elif floatError == True:
						await client.send_message(message.channel, "Score in numbers only.")
					else:
						with open("%s.txt"%leaderboard_type) as file:
							leaderboardList = [line.split(" ") for line in file]
							print(leaderboardList)
						if not sneaselRefresh:
							#Check if player is already in standings, update
							found = False
							for index, elem in enumerate(leaderboardList):
								#If player already exists
								if message.author.display_name.lower() == elem[0].lower() and found == False:
									#Score is higher than previously submitted
									if tempScore > float(elem[1]) and found == False:
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
										await client.send_message(message.channel, "To update your score, it has to be higher than your previous submission.")

							#Player is missing, insert new entry
							if notUpdated and not skipUpdate:
								insertedBool = False
								for index, elem in enumerate(leaderboardList):
									if tempScore >= float(elem[1]) and insertedBool == False:
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
						embed.set_footer(text = "The remaining standings are hidden, find out your standings by typing ?standings")
						embed.add_field(name="\u200b", value = "\u200b", inline=False)
						channel2 = client.get_channel('466913214656020493')
						unitString = "km"
					elif pikachuTrue:
						embed = discord.Embed(title="Leaderboard Karlskrona: Pikachu \n", color=0xff9900)
						embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/94/PikachuFan_Gold.png/revision/latest?cb=20161013235542")
						embed.set_footer(text = "The remaining standings are hidden, find out your standings by typing ?standings")
						embed.add_field(name="\u200b", value = "\u200b", inline=False)
						channel2 = client.get_channel('467754615413407745')

					#Add fields to be presented in table, fill with data
					print(leaderboardList)
					for index, elem in enumerate(leaderboardList):
						if index < 10:
							print("Scores going in fields: %s"%elem[1])
							embed.add_field(name="%i. %s - %.1f %s" % (index+1, elem[0], float(elem[1]), unitString), value = "Updated: %s" % (elem[2]), inline=True)

					async for x in client.logs_from(channel2, 10):
						try:
							await client.delete_message(x)
						except:
							print("somehow failed to delete message")

					await asyncio.sleep(1)
					if newTopOne:
						await client.send_message(message.channel, ":crown: :first_place: CONGRATULATIONS, you have reached #%i in the %s leaderboard. \nPlease send an in game screenshot to any admin so they may confirm your entry." % (newRank+1, leaderboard_type))
					elif topThree:
						await client.send_message(message.channel, ":crown: Congratulations on your #%i placing in the %s leaderboard, please send an in game screenshot to any admin so they may confirm your entry." % (newRank+1, leaderboard_type))
					elif scoreUpdated:
						await client.send_message(message.channel, "Congratulations, you placed #%i in the %s leaderboard. Check %s to see the top 10." % (newRank+1, leaderboard_type, channel2.mention))
					await client.send_message(message.channel, "The leaderboard has been refreshed.")
					await client.send_message(channel2, embed=embed)
				
		#List ranks across leaderboards
		elif message.content.upper().startswith('?RANKS') and message.channel.id == '466563505462575106':
			nickname = message.author.display_name
			tempList = []
			leaderboard_list = ["jogger","pikachu"]
			unitString = ""

			for item in leaderboard_list:
				if item == "jogger":
					unitString = "km"
				leaderboard_file = open("%s.txt"%item, "r")
				for index, line in enumerate(leaderboard_file):
					line = line.split(" ")
					if line[0].lower() == nickname.lower():
						#print("WE HAVE A MATCH!")
						if(index+1 == 1):
							await client.send_message(message.channel, ":first_place: %s is ranked \#%i in the %s leaderboards with a score of %.1f%s." % (nickname, index+1, item, float(line[1]),unitString))
						elif(index+1 == 2):
							await client.send_message(message.channel, ":second_place: %s is ranked \#%i in the %s leaderboards with a score of %.1f%s." % (nickname, index+1, item, float(line[1]),unitString))
						elif(index+1 == 3):
							await client.send_message(message.channel, ":third_place: %s is ranked \#%i in the %s leaderboards with a score of %.1f%s." % (nickname, index+1, item, float(line[1]),unitString))
						elif(index+1 > 3):
							await client.send_message(message.channel, "%s is ranked \#%i in the %s leaderboards with a score of %.1f km." % (nickname, index+1, item, float(line[1]),unitString))
						else:
							await client.send_message(message.channel, "%s is not ranked in the %s leaderboards, submit a score by typing ?%s 'YOUR_SCORE'." % (nickname, item, item))
							

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