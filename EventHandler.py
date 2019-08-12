"""EventHandler."""

import asyncio
import re
from datetime import datetime

import discord
from discord.ext import commands
from discord.utils import get

Client = discord.Client()
client = commands.Bot(command_prefix="?")
leaderboardList = []


# Start up
def startup():
    """Start up function, ready to run after dashes."""
    print("Starting..")

    @client.event
    async def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print("Ready for action")
        print('------')


@client.event
async def help(message, leaderboard_list):
    helpString = message.content.lower()
    helpString = helpString[6:]  # remove "help? "

    if helpString == "ranks":
        await client.send_message(message.channel, "Kommandot ?ranks används för att skriva ut en lista med dina placeringar i de olika leaderboards.\n*Exempel: ?ranks*")
    elif helpString in leaderboard_list:
        await client.send_message(message.channel, "Kommandot ?%s används för att ut en lista på top 5 samt din placering och dina närmsta konkurrenter.\n*Exempel: ?%s 250*" % (helpString,helpString))
    elif helpString == "list":
        await client.send_message(message.channel, "Kommandot ?%s används för att skriva in dina poäng i de olika leaderboards.\n*Exempel: ?list jogger*" % (helpString))

    else:
        codeMessage = "**__KOMMANDON TILLGÄNGLIGA__**\n\n"
        codeMessage += "1. ?önskadleaderboard poäng, används för att rapportera in dina poäng till de olika leaderboards. *Exempelanvändning 1: ?jogger 2320*, *Exempelanvändning 2: ?pikachu 463*\n"
        codeMessage += "2. ?list önskadleaderboard, används för att ut en lista på top 5 samt din placering och dina närmsta konkurrenter. *Exempelanvändning: ?list jogger*\n"
        codeMessage += "3. ?ranks, används för att visa hur du rankas mot övriga medlemmar.\n"
        codeMessage += "4. ?help kommando, används för att få mer information om ett specifikt kommando. *Exempel: ?help jogger*\n"
        await client.send_message(message.channel, codeMessage)


# List, sends complete list of leaderboard
@client.event
async def list(message, leaderboard_list):
    #leaderboard_list = ["jogger", "pikachu"]
    leaderboard_type = message.content.lower()
    leaderboard_type = leaderboard_type[6:]

    lookUpList = []

    messageOut = ""

    lengthTest = message.content.split(" ")
    if len(lengthTest) < 2:
        await client.send_message(message.channel, "Det saknas information. *Format: ?list LEADERBOARD_TYPE*")
    elif not leaderboard_type in leaderboard_list:
        await client.send_message(message.channel, "%s leaderboarden existerar inte." % leaderboard_type.capitalize())
    else:
        found = False
        file = open("%s.txt" % leaderboard_type, "r")
        index = 0
        currentRank = 0
        currentScore = 0
        for item in file:
            item2 = item.split(" ")
            tempList = []
            if not float(currentScore) == float(item2[1]):
                currentScore = float(item2[1])
                currentRank += 1
            if index < 5:
                # found user among top 5
                if item2[0].lower() == message.author.display_name.lower():
                    found = True
                    messageOut += "**%i. %s %s**\n" % (currentRank, item2[0], item2[1])
                else:
                    messageOut += "%i. %s %s\n" % (currentRank, item2[0], item2[1])
                tempList.append(item2[0])
                tempList.append(item2[1])
                lookUpList.append(tempList)
            elif not found:
                tempList.append(item2[0])
                tempList.append(item2[1])
                lookUpList.append(tempList)
                # found user lower down
                if item2[0].lower() == message.author.display_name.lower():
                    messageOut += "-----------------\n%i. %s %s" % (currentRank - 2, lookUpList[index-2][0], lookUpList[index-2][1])
                    messageOut += "\n%i. %s %s" % (currentRank-1, lookUpList[index-1][0], lookUpList[index-1][1])
                    messageOut += "\n**%i. %s %s**" % (currentRank, item2[0], item2[1])
            index += 1
        #print(lookUpList)
        await client.send_message(message.channel, messageOut)


# Format: ?admin_claim nickname userID
@client.event
async def admin_claim(message, leaderboard_list):
    """Admins can use this to fix nicknames of people that missclaimed."""
    #leaderboard_list = ["jogger.txt", "pikachu.txt"]
    claimString = message.content
    claimString = claimString[13:]
    claimString.replace(",", " ")

    replacedNick = ""
    newNick = ""

    # Format claimList: nickname userID
    tempList = []
    tempList = claimString.split(" ")

    if not '435908470936698910' in [role.id for role in message.author.roles] and not '342771363884302339' in [role.id for role in message.author.roles]:
        await client.send_message(message.channel, "Detta kommando är till för admins endast. Om du behöver hjälp att ändra leaderboard användarnamn, fråga en valfri admin.")
    elif len(tempList[0]) > 15:
        await client.send_message(message.channel, "Namnet är för långt, max 15 tecken. *Format: ?admin_claim DESIRED_NAME USER_ID")
    elif not int(tempList[1].isdigit()):
        await client.send_message(message.channel, "USER_ID måste vara siffror endast. *Format: ?admin_claim DESIRED_NAME USER_ID")
    elif len(claimString) < 2:
        await client.send_message(message.channel, "Det saknas information. *Format: ?admin_claim DESIRED_NAME USER_ID")
    else:
        insertList = []
        changedIndex = 0
        changed = False

        claimList = []
        file = open("idclaims.txt", "r")
        for index, item in enumerate(file):
            item = item.split(" ")

            # Put line in tempList to write back later
            temp2 = []
            temp2.append(item[0])
            temp2.append(" ")
            temp2.append(item[1])

            # compare ID to list IDs
            item[1] = item[1].replace("\n", "")
            if str(item[1]) == str(tempList[1]):
                changedIndex = index
                changed = True
                replacedNick = temp2[0]
                temp2[0] = tempList[0]
                newNick = temp2[0]
                insertList = temp2
            claimList.append(temp2)
        file.close()

        # if user ID was found, pop that entry
        if changed:
            claimList.pop(changedIndex)
            claimList.insert(changedIndex, insertList)
            await client.send_message(message.channel, "Användarnamnet har uppdaterats från %s till %s" % (replacedNick, newNick))
        file = open("idclaims.txt", "w")
        for item in claimList:
            file.write(item[0])
            file.write(item[1])
            file.write(item[2])
        file.close()

        leaderboard_list = [x+".txt" for x in leaderboard_list]
        # Loop through files and update to new nickname
        for leaderboard in leaderboard_list:
            fileList = []
            # Read from file and look for nickname to update
            file = open(leaderboard, "r")
            for item in file:
                item = item.split(" ")
                # if name in file matches old name
                if item[0].lower() == replacedNick.lower():
                    item[0] = newNick
                temp = []
                temp.append(item[0])
                temp.append(" ")
                temp.append(item[1])
                temp.append(" ")
                temp.append(item[2])
                fileList.append(temp)
            file.close()

            # Write back to file with updated nickname
            file = open(leaderboard, "w")
            for item in fileList:
                # if name in file matches old name
                file.write(item[0])
                file.write(" ")
                file.write(item[2])
                file.write(" ")
                file.write(item[4])
            file.close()


# Refresh function
@client.event
async def refresh(message, id_list, leaderboard_list):
    """Refresh function, parses and presents leaderboard of choosing."""
    leaderboard_type = message.content.lower().split(" ", 2)[1]

    tempCheck = message.content.split(" ")
    if len(tempCheck) < 2:
        await client.send_message(message.channel, "Det saknas information. Format: ?refresh leaderboard.")
    elif (len(tempCheck) > 2 and not message.content.lower().split(" ", 1)[0] == "?delete"):
        await client.send_message(message.channel, "För mycket information. Format: ?refresh leaderboard.")
    elif leaderboard_type in leaderboard_list:
        await leaderboard(message, id_list)
        # await client.send_message(message.channel, "?%s 1" % leaderboard_type)
    else:
        await client.send_message(message.channel, "%s leaderboard existerar inte." % leaderboard_type.capitalize())


# Claim function, assigns claim role, adds user ID to a list
@client.event
async def claim(message, id_list):
    """Claim function, assigns claim role, adds user ID to a list."""
    claimedIDs = []

    #does this work
    #memberTime = datetime.now()
    #memberTime = memberTime - message.author.joined_at

    #seconds = memberTime.total_seconds()
    #minutes = (seconds % 3600) // 60
    #minutesLeft = int(10 - minutes)

    # Add information of user to temporary list
    tempID = []
    tempID.append(message.author.display_name)
    tempID.append(message.author.id + "\n")

    found = False
    # delete msg
    async for x in client.logs_from(message.channel, 1):
        try:
            await client.delete_message(x)
        except:
            print("Somehow failed to delete CLAIM message.")
    # Check for illegal nickname symbols, + ensures min size == 1
    stringPattern = r'[^\.A-Za-z0-9]'
    # Check if member too new, stops spamming new accounts and entering scores
    #if minutesLeft > 0:
    #    await client.send_message(message.channel, "Du har inte varit medlem på denna Discord server tillräckligt länge %s, försök igen om %i minuter." % (message.author.mention, minutesLeft))
    if (re.search(stringPattern, message.author.display_name)):
        await client.send_message(message.channel, "Ditt Discord användarnamn innehåller otillåtna tecken, var god ändra ditt användarnamn så att det matchar det i Pokémon Go.")
    elif len(message.author.display_name) > 15:
        await client.send_message(message.channel, "Ditt Discord användarnamn får inte överstiga 15 tecken, var god ändra ditt namn så det matchar det i Pokémon Go.")
    else:
        with open("idclaims.txt") as file:
            claimedIDs = [line.split(" ") for line in file]

        # Read for ID in file
        claimFile = open("idclaims.txt", "r")
        for item in claimedIDs:
            if float(item[1]) == float(message.author.id):
                await client.send_message(message.channel, ":no_entry: Du har redan claimat ditt användarnamn %s, om du har bytt användarnamn kontakta en valfri admin." % message.author.mention)
                found = True
        claimFile.close()
        # Write to file
        if not found:
            # Add to list
            claimedIDs.insert(0, tempID)
            # Add ID to file
            print("Adding new user")
            claimFile = open("idclaims.txt", "w")
            for item in claimedIDs:
                claimFile.write(item[0])
                claimFile.write(" ")
                claimFile.write(item[1])
            claimFile.close()

            channel2 = client.get_channel(id_list[0])
            claimedRole = get(message.author.server.roles, name="claimed")
            await client.add_roles(message.author, claimedRole)
            # assign role is not claimed yet, send PM with help info
            await client.send_message(message.channel, ":white_check_mark: %s du har claimat användarnamnet %s. Skriv ?help i %s för hjälp med att komma igång." % (message.author.mention, message.author.display_name, channel2.mention))
            codeMessage = "Välkommen till Blekinges leaderboards! \n\n"
            codeMessage += "**__KOMMANDON TILLGÄNGLIGA__**\n\n"
            codeMessage += "*Alla kommandon skrivs i #leaderboards*\n\n"
            codeMessage += "1. ?önskadleaderboard poäng, används för att rapportera in dina poäng till de olika leaderboards. \n    *Exempelanvändning 1: '?jogger 2320'*, för att lägga in dina 2320km i Jogger leaderboarden. \n    *Exempelanvändning 2: '?pikachu 463'*, för att skicka in dina 463 Pikachu fångster i Pikachu Fan leaderboarden.\n"
            codeMessage += "2. ?list önskadleaderboard, används för att ut en lista på top 5 samt din placering och dina närmsta konkurrenter. *Exempelanvändning: ?list jogger*\n"
            codeMessage += "3. ?ranks, används för att visa hur du rankas mot övriga medlemmar.\n"
            codeMessage += "4. ?help kommando, används för att få mer information om ett specifikt kommando. *Exempel: ?help jogger*\n"
            await client.send_message(message.author, codeMessage)


# Leaderboard function
@client.event
async def leaderboard(message, id_list):
    """Leaderboard function, records, adds and presents leaderboards."""
    # Check if users display name is in claim list
    earlyCheck = False
    tempScore = ""
    unitString = ""
    fileCheck = open("idclaims.txt", "r")
    for item in fileCheck:
        item = item.split(" ")
        if str(item[0].lower()) == str(message.author.display_name.lower()):
            earlyCheck = True
    fileCheck.close()

    if earlyCheck:
        joggerTrue = False
        pikachuTrue = False
        battlegirlTrue = False
        pokedexTrue = False
        collectorTrue = False
        scientistTrue = False
        breederTrue = False
        backpackerTrue = False
        fishermanTrue = False
        youngsterTrue = False
        berrymasterTrue = False
        gymleaderTrue = False
        championTrue = False
        battlelegendTrue = False
        rangerTrue = False
        unownTrue = False
        gentlemanTrue = False
        pilotTrue = False
        totalxpTrue = False
        goldgymsTrue = False
        idolTrue = False
        greatleagueTrue = False
        ultraleagueTrue = False
        masterleagueTrue = False
        acetrainerTrue = False
        cameramanTrue = False
        heroTrue = False
        purifierTrue = False

        sneaselRefresh = False
        leaderboardList = []

        upperLimit = 0

        # Which leaderboard the user is updating
        leaderboard_type = message.content.lower().split(" ", 1)[0]
        leaderboard_type = leaderboard_type[1:]

        # Sneasel is trying to refresd, set true and set leaderboard type
        if leaderboard_type.lower() == "refresh" or leaderboard_type.lower() == "delete":
            sneaselRefresh = True
            leaderboard_type = message.content.lower().split(" ", 2)[1]

        # Score part of string
        try:
            tempScore = message.content.lower().split(" ", 1)[1]
        except IndexError:  # User only typed ?LEADERBOARD_TYPE
            await client.send_message(message.channel,
                                      "Korrekt sätt att skicka in dina poäng är ?%s POÄNG. \n*Exempel: ?%s 2500*" % (leaderboard_type, leaderboard_type))

        # set specific leaderboard values
        if leaderboard_type == "jogger":
            joggerTrue = True
            upperLimit = 20000
            unitString = "km"
        elif leaderboard_type == "pikachu":
            pikachuTrue = True
            upperLimit = 5000
        elif leaderboard_type == "battlegirl":
            battlegirlTrue = True
            upperLimit = 100000
        elif leaderboard_type == "pokedex":
            pokedexTrue = True
            upperLimit = 600
        elif leaderboard_type == "collector":
            collectorTrue = True
            upperLimit = 500000
        elif leaderboard_type == "scientist":
            scientistTrue = True
            upperLimit = 40000
        elif leaderboard_type == "breeder":
            breederTrue = True
            upperLimit = 50000
        elif leaderboard_type == "backpacker":
            backpackerTrue = True
            upperLimit = 500000
        elif leaderboard_type == "fisherman":
            fishermanTrue = True
            upperLimit = 10000
        elif leaderboard_type == "youngster":
            youngsterTrue = True
            upperLimit = 10000
        elif leaderboard_type == "berrymaster":
            berrymasterTrue = True
            upperLimit = 500000
        elif leaderboard_type == "gymleader":
            gymleaderTrue = True
            upperLimit = 500000
        elif leaderboard_type == "champion":
            championTrue = True
            upperLimit = 10000
        elif leaderboard_type == "battlelegend":
            battlelegendTrue = True
            upperLimit = 10000
        elif leaderboard_type == "ranger":
            rangerTrue = True
            upperLimit = 10000
        elif leaderboard_type == "unown":
            unownTrue = True
            upperLimit = 30
        elif leaderboard_type == "gentleman":
            gentlemanTrue = True
            upperLimit = 50000
        elif leaderboard_type == "pilot":
            pilotTrue = True
            upperLimit = 200000000
        elif leaderboard_type == "totalxp":
            totalxpTrue = True
            upperLimit = 200000000
        elif leaderboard_type == "goldgyms":
            goldgymsTrue = True
            upperLimit = 500
        elif leaderboard_type == "idol":
            idolTrue = True
            upperLimit = 200
        elif leaderboard_type == "greatleague":
            greatleagueTrue = True
            upperLimit = 50000
        elif leaderboard_type == "ultraleague":
            ultraleagueTrue = True
            upperLimit = 50000
        elif leaderboard_type == "masterleague":
            masterleagueTrue = True
            upperLimit = 50000
        elif leaderboard_type == "acetrainer":
            acetrainerTrue = True
            upperLimit = 50000
        elif leaderboard_type == "cameraman":
            cameramanTrue = True
            upperLimit = 1000
        elif leaderboard_type == "hero":
            heroTrue = True
            upperLimit = 100000
        elif leaderboard_type == "purifier":
            purifierTrue = True
            upperLimit = 100000

        # Replace possible commas with dots
        if joggerTrue:
            tempScore = str(tempScore.replace(",", "."))

        tempList = []
        notUpdated = True
        skipUpdate = False
        current_dt = datetime.now()
        floatError = False
        scoreUpdated = False

        checkFailed = False
        topThree = False
        newTopOne = False
        currentRank = 0
        currentScore = 0
        insertedIndex = 0

        # Check if score is numbers only
        if not sneaselRefresh:
            try:
                float(tempScore)
            except ValueError:
                await client.send_message(message.channel, "Poäng endast i siffror. *Format: ?leaderboard poäng*")
                floatError = True
        if not floatError or sneaselRefresh:
            # if Sneasel is not refreshing, check name for illegal characters
            if not sneaselRefresh:
                tempScore = float(tempScore)
                p = re.compile('\d+(\.\d+)?')
                stringPattern = r'[^\.A-Za-z0-9]'
                # Check for illegal nickname symbols, + ensures min size == 1
                if (re.search(stringPattern, message.author.display_name)):
                    checkFailed = True
                    await client.send_message(message.channel, "Ditt Discord användarnamn innehåller otillåtna tecken, var god ändra ditt användarnamn så att det matchar Pokémon Go användarnamnet.")
                elif not p.match(str(tempScore)):
                    checkFailed = True
                    await client.send_message(message.channel, "Error: Otillåtna tecken i poängen. *Format: ?leaderboard poäng*")
                elif len(message.author.display_name) > 15:
                    checkFailed = True
                    await client.send_message(message.channel, "Error: Namn får vara max 15 tecken. Var god uppdatera ditt Discord användarnamn. Fråga admins om hjälp vid besvär.")
            if not checkFailed:
                # Create temp leaderboardList to be inserted if applicable
                tempList.append(message.author.display_name)
                tempList.append(tempScore)
                tempList.append(current_dt.date())

                # if Sneasel is not refreshing, check score for illegal characters
                if not sneaselRefresh:
                    # Cast entry number to float
                    if tempScore > upperLimit:
                        await client.send_message(message.channel, "Poäng högre än tillåtet.")
                        checkFailed = True
                    elif tempScore < 1 and not sneaselRefresh:
                        await client.send_message(message.channel, "Poäng lägre än tillåtet.")
                        checkFailed = True
                    elif floatError and not sneaselRefresh:
                        await client.send_message(message.channel, "Poäng får inte innehålla annat än siffror.")
                        checkFailed = True
                if not checkFailed:
                    with open("%s.txt" % leaderboard_type) as file:
                        leaderboardList = [line.split(" ") for line in file]
                    if not sneaselRefresh:
                        # Check if player is already in standings, update
                        found = False
                        for index, elem in enumerate(leaderboardList):
                            # If player already exists
                            if (message.author.display_name.lower() == elem[0].lower() and not found):
                                if not found:
                                    found = True
                                    # Update player stats
                                    leaderboardList[index][1] = tempScore
                                    leaderboardList[index][2] = current_dt.date()
                                    # Remove updated score
                                    tempList = leaderboardList.pop(index)

                                    notUpdated = False
                                    # Move player to correct position
                                    moved = False
                                    for idx, elm in enumerate(leaderboardList):
                                        if moved:
                                            break
                                        elif tempScore > float(elm[1]) or (tempScore == 1 and float(elm[1]) == 1):
                                            # Insert updated score
                                            if not joggerTrue:
                                                tempList[1] = int(tempList[1])
                                            insertedIndex = idx
                                            leaderboardList.insert(idx, tempList)  # insert updated score
                                            moved = True
                                            scoreUpdated = True
                                            # Updated score gets top one, was not top one before
                                            if idx < 1 and index > 0:
                                                newTopOne = True
                                            # Updated score gets top three, was not top three
                                            elif idx < 3 and index > 2:
                                                topThree = True
                                else:
                                    skipUpdate = True

                        # Player is missing, insert new entry
                        if notUpdated and not skipUpdate and not sneaselRefresh:
                            insertedBool = False
                            for index, elem in enumerate(leaderboardList):
                                if (tempScore > float(elem[1]) or (tempScore == 1 and float(elem[1]) == 1)) and not insertedBool:
                                    if not joggerTrue:
                                        tempList[1] = int(tempList[1])
                                    insertedIndex = index
                                    leaderboardList.insert(index, tempList)
                                    insertedBool = True
                                    scoreUpdated = True
                                    # New score is top one
                                    if index < 1:
                                        newTopOne = True
                                    # New score is among top three
                                    if index < 3:
                                        topThree = True
                    file = open("%s.txt" % leaderboard_type, "w")
                    for item in leaderboardList:
                        item2 = ' '.join(str(x) for x in item)
                        if item == tempList:
                            file.write("%s\n" % item2)
                        else:
                            file.write("%s" % item2)
                    file.close()

                # http://pokemongo.wikia.com/wiki/Medals
                if joggerTrue:
                    embed = discord.Embed(title="Leaderboard Karlskrona: Jogger \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/98/Jogger_Gold.png/revision/latest?cb=20161013235539")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[1])
                elif pikachuTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Pikachu Fan \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/94/PikachuFan_Gold.png/revision/latest?cb=20161013235542")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[2])
                elif battlegirlTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Battle Girl \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/93/BattleGirl_Gold.png/revision/latest?cb=20161013235336")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[4])
                elif pokedexTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Pokédex \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/4/43/Kanto_Gold.png/revision/latest?cb=20161013235541")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[5])
                elif collectorTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Collector \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/8/86/Collector_Gold.png/revision/latest?cb=20161014002520")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[6])
                elif scientistTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Scientist \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/7/7c/Scientist_Gold.png/revision/latest?cb=20161013235610")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[7])
                elif breederTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Breeder \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/b/b7/Breeder_Gold.png/revision/latest?cb=20161013235426")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[8])
                elif backpackerTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Backpacker \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/b/bb/Backpacker_Gold.png/revision/latest?cb=20161013235335")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[9])
                elif fishermanTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Fisherman \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/6/69/Fisherman_Gold.png/revision/latest?cb=20161013235429")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[10])
                elif youngsterTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Youngster \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/94/Youngster_Gold.png/revision/latest?cb=20161013235612")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[11])
                elif berrymasterTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Berry Master \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/92/BerryMaster_Gold.png/revision/latest?cb=20170623010756")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[12])
                elif gymleaderTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Gym Leader \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/f/f9/GymLeader_Gold.png/revision/latest?cb=20170623010816")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[13])
                elif championTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Champion \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/2/20/Champion_Gold.png/revision/latest?cb=20170623133823")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[14])
                elif battlelegendTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Battle Legend \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/6/61/BattleLegend_Gold.png/revision/latest?cb=20170623133841")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[15])
                elif rangerTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Pokémon Ranger \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/7/77/Researcher_Gold.png/revision/latest?cb=20180328115039")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[16])
                elif unownTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Unown \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/1/1b/Unown_Gold.png/revision/latest?cb=20170217162806")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[17])
                elif gentlemanTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Gentleman \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/f/f0/Gentleman_Gold.png/revision/latest?cb=20180621120608")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[18])
                elif pilotTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Pilot \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/4/4e/Pilot_Gold.png/revision/latest?cb=20180621120613")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[19])
                elif totalxpTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Total XP \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/b/bd/Pok%C3%A9mon_GO_Fest_Chicago_2017.png/revision/latest?cb=20170726115410")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[20])
                elif goldgymsTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Gold Gyms \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/0/0a/Gym_Badge_Tier_Gold.png/revision/latest?cb=20170620224940")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[21])
                elif idolTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Idol \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/9b/Idol_Gold.png/revision/latest?cb=20180621120611")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[22])
                elif greatleagueTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Great League Veteran \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/2/28/GreatLeague_Gold.png/revision/latest?cb=20190113004308")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[23])
                elif ultraleagueTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Ultra League Veteran \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/5/5e/UltraLeague_Gold.png/revision/latest?cb=20190113004309")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[24])
                elif masterleagueTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Master League Veteran \n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/d/d7/MasterLeague_Gold.png/revision/latest?cb=20190113004311")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[25])
                elif acetrainerTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Ace Trainer\n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/9c/AceTrainer_Gold.png/revision/latest?cb=20161013235333")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[26])
                elif cameramanTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Cameraman\n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/1/19/Cameraman_Gold.png/revision/latest?cb=20190220234724")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[27])
                elif heroTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Hero\n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/5/52/Hero_Gold.png/revision/latest?cb=20190722124317")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[28])
                elif purifierTrue:
                    embed = discord.Embed(title="Leaderboard Blekinge: Purifier\n", color=0xff9900, description=("Skriv '?%s poäng' i #leaderboards för att bli tillagd"%leaderboard_type))
                    embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/4/47/Purifier_Gold.png/revision/latest?cb=20190722124336")
                    embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                    embed.add_field(name="\u200b", value="\u200b", inline=False)
                    channel2 = client.get_channel(id_list[29])

                currentRank = 0
                currentScore = 0
                currentRankList = []
                # Add fields to be presented in table, fill with data
                for index, elem in enumerate(leaderboardList):
                    currentRankList.append(index + 1)
                    if index < 10:
                        # Score not same as previous user, dont update score index rank
                        if not currentScore == float(elem[1]):
                            currentRank = index + 1
                            currentScore = float(elem[1])
                        else:
                            currentRankList[index] = currentRank

                        # Upper case no decimals, lower case decimals
                        if not joggerTrue:
                            embed.add_field(name="%i. %s - %i %s" % (int(currentRank), elem[0], int(elem[1]), unitString), value="Updated: %s" % (elem[2]), inline=True)
                        else:
                            embed.add_field(name="%i. %s - %.1f %s" % (int(currentRank), elem[0], float(elem[1]), unitString), value="Updated: %s" % (elem[2]), inline=True)
                try:
                    async for x in client.logs_from(channel2, 10):
                        await client.delete_message(x)
                except:
                        print("somehow failed to delete message")

                await asyncio.sleep(1)
                if newTopOne:
                    await client.send_message(message.channel, ":crown: :first_place: GRATULERAR %s, du har nått #%i i %s leaderboarden. \nVar god skicka in en in-game-screenshot till valfri admin för att bekräfta dina poäng." % (message.author.mention, currentRankList[insertedIndex], leaderboard_type.capitalize()))
                elif topThree:
                    await client.send_message(message.channel, ":crown: Gratulerar %s till din #%i placering i %s leaderboarden. \nVar god skicka in en in-game-screenshot till valfri admin för att bekräfta dina poäng." % (message.author.mention, currentRankList[insertedIndex], leaderboard_type.capitalize()))
                elif scoreUpdated:
                    await client.send_message(message.channel, "Gratulerar %s, du är placerad #%i i %s leaderboarden. Kolla %s för att se top 10." % (message.author.mention, currentRankList[insertedIndex], leaderboard_type.capitalize(), channel2.mention))
                if sneaselRefresh:
                    await client.send_message(message.channel, "Leaderboarden har laddats om.")
                await client.send_message(channel2, embed=embed)
    else:
        await client.send_message(message.channel, "Dina poäng har inte skickats vidare då ditt användarnamn inte matchar det tidigare satta. Ta kontakt med valfri admin.")


# CHECKS MESSAGES, MAIN DRIVER
def checkMessages(id_list):
    """Checks for messages, calls appropriate functions."""
    print("Checking for messages..")
    leaderboard_list = ["jogger", "pikachu", "battlegirl", "pokedex", "collector", "scientist", "breeder", "backpacker", "fisherman",
                        "youngster", "berrymaster", "gymleader", "champion", "battlelegend", "ranger", "unown", "gentleman",
                        "pilot", "totalxp", "goldgyms", "idol", "greatleague", "ultraleague", "masterleague", "acetrainer",
                        "cameraman", "hero", "purifier"]

    @client.event
    async def on_message(message):
        leaderboardString = message.content.lower()[1:].split(" ")

        # Test if bot is still responsive
        if (message.content.upper().startswith('?TEST') and message.channel.id == id_list[0]):
            await client.send_message(message.channel, "Ja, hej %s! Hallå! :sweat_smile:" % message.author.mention)

        # Claim nick for your ID
        elif (message.content.upper().startswith('?HELP') and message.channel.id == id_list[0]):
            await help(message, leaderboard_list)

        # List top 5 and the two ahead of you
        elif (message.content.upper().startswith('?LIST') and message.channel.id == id_list[0]):
            await list(message, leaderboard_list)

        # Claim nick for your ID in #support
        elif (message.content.upper().startswith('?CLAIM') and message.channel.id == id_list[3]):
            await claim(message, id_list)

        # REFRESH, Format: ?refresh LEADERBOARD_TYPE
        elif(message.content.upper().startswith('?REFRESH') and message.channel.id == id_list[0]):
            await refresh(message, id_list, leaderboard_list)

        # LEADERBOARDS Format: ?LEADERBOARD_TYPE, SCORE
        elif (leaderboardString[0] in leaderboard_list and message.channel.id == id_list[0] and message.content.lower().startswith('?')):
            await leaderboard(message, id_list)

        # List ranks across leaderboards
        elif (message.content.upper().startswith('?RANKS') or message.content.upper().startswith('?RANK')) and message.channel.id == id_list[0]:
            nickname = message.author.display_name

            # Check if users display name is in claim list--------------------------------
            nameButNotID = False
            IDButNotName = False
            fileCheck = open("idclaims.txt", "r")
            for item in fileCheck:
                item = item.split(" ")
                item[0] = item[0].replace("\n", "")
                item[1] = item[1].replace("\n", "")
                # Check if previously claimed, nickname matches
                if (str(item[0].lower()) == str(message.author.display_name.lower())):
                    # Check if previously claimed, id matches
                    if not (str(item[1]) == str(message.author.id)):
                        nameButNotID = True
                # Check if previously claimed, id matches
                if (str(item[1]) == str(message.author.id)):
                    # Check if previously claimed, nickname matches
                    if not (str(item[0].lower()) == str(message.author.display_name.lower())):
                        IDButNotName = True
            fileCheck.close()
            # ------------------------------------------------------------------------------

            # Nickname exists, but not correct ID
            if nameButNotID and not IDButNotName:
                await client.send_message(message.channel, "Ditt användarnamn matchar inte med det du registrerat tidigare, ändra tillbaka eller ta kontakt med valfri admin.")
            elif nameButNotID:
                await client.send_message(message.channel, "Ditt användarnamn matchar med någon annans och inte det du registrerat tidigare, ändra tillbaka eller ta kontakt med valfri admin.")
            elif IDButNotName:
                await client.send_message(message.channel, "Ditt användarnamn matchar inte med det du registrerat tidigare, ändra tillbaka det eller ta kontakt med valfri admin.")
            else:
                found = False

                #leaderboard_list = ["jogger", "pikachu"]
                unitString = ""
                currentRank = 0
                currentScore = 0
                currentRankList = []

                num2words1 = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
                              6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
                              11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen',
                              15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen'}
                messageOut = ""
                messageOut2 = ""   # "needed" because message too long
                loops = True
                # Loop through leaderboard types
                for item in leaderboard_list:
                    if item == "jogger":
                        unitString = "km"
                    elif item == "pikachu":
                        unitString = "Pikachu"
                    elif item == "battlegirl":
                        unitString = "battles"
                    elif item == "pokedex":
                        unitString = "Pokémon"
                    elif item == "collector":
                        unitString = "Pokémon"
                    elif item == "scientist":
                        unitString = "evolves"
                    elif item == "breeder":
                        unitString = "ägg"
                    elif item == "backpacker":
                        unitString = "Pokéstops"
                    elif item == "fisherman":
                        unitString = "Magikarp"
                    elif item == "youngster":
                        unitString = "Rattata"
                    elif item == "berrymaster":
                        unitString = "bär"
                    elif item == "gymleader":
                        unitString = "timmar"
                    elif item == "champion":
                        unitString = "raids"
                    elif item == "battlelegend":
                        unitString = "legendary raids"
                    elif item == "ranger":
                        unitString = "field research tasks"
                    elif item == "unown":
                        unitString = "Unown"
                    elif item == "gentleman":
                        unitString = "trades"
                    elif item == "pilot":
                        unitString = "km trades"
                    elif item == "totalxp":
                        unitString = "xp"
                    elif item == "goldgyms":
                        unitString = "gyms"
                    elif item == "idol":
                        unitString = "best friends"
                    elif item == "greatleague":
                        unitString = "battles"
                    elif item == "ultraleague":
                        unitString = "battles"
                    elif item == "masterleague":
                        unitString = "battles"
                    elif item == "acetrainer":
                        unitString = "battles"
                    elif item == "cameraman":
                        unitString = "foton"
                    elif item == "hero":
                        unitString = "vinster"
                    elif item == "purifier":
                        unitString = "Pokémon"


                    leaderboard_file = open("%s.txt" % item, "r")

                    # Loop through file
                    
                    for index, line in enumerate(leaderboard_file):
                        line = line.split(" ")

                        # If score not same as previous player, update rank
                        if not float(currentScore) == float(line[1]):
                            currentRank = index + 1
                            currentScore = float(line[1])

                        if line[0].lower() == nickname.lower():
                            found = True
                            tempMsg = ""
                            localScore = round(float(line[1]), 1)
                            if not item in ("jogger"):
                                localScore = int(localScore)
                            if(currentRank == 1):
                                tempMsg = ":first_place: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (message.author.mention, currentRank, item.capitalize(), localScore, unitString)
                            elif(currentRank == 2):
                                tempMsg = ":second_place: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (message.author.mention, currentRank, item.capitalize(), localScore, unitString)
                            elif(currentRank == 3):
                                tempMsg = ":third_place: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (message.author.mention, currentRank, item.capitalize(), localScore, unitString)
                            elif(currentRank == 10):
                                tempMsg = ":keycap_%s: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (num2words1[currentRank].lower(), message.author.mention, currentRank, item.capitalize(), localScore, unitString)
                            elif(currentRank > 3 and currentRank < 11):
                                tempMsg = ":%s: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (num2words1[currentRank].lower(), message.author.mention, currentRank, item.capitalize(), localScore, unitString)
                            elif currentRank > 10:
                                tempMsg = ":asterisk: %s är placerad \#%i i %s leaderboarden med %s %s.\n" % (message.author.mention, currentRank, item.capitalize(), localScore, unitString)
                            else:
                                tempMsg = "%s är inte placerad i någon %s leaderboard, skicka in dina poäng genom att skriva ?%s poäng.\n" % (message.author.mention, item.capitalize(), item)

                            if (loops):
                                messageOut += tempMsg
                                loops = False
                            else:
                                messageOut2 += tempMsg
                                loops = True
                if found:
                    await client.send_message(message.author, messageOut)
                    await client.send_message(message.author, messageOut2)
                    await client.send_message(message.channel, "Du har fått ett privatmeddelande med alla dina placeringar %s." % message.author.mention)
                if not found:
                    await client.send_message(message.channel, "Vi lyckades inte hitta dig bland några leaderboards %s. Du verkar inte registrerat några poäng ännu." % message.author.mention)

        # DELETE, admins may delete leaderboard entries Format: ?delete leaderboard_type name_to_delete
        elif message.content.upper().startswith('?DELETE') and message.channel.id == id_list[0]:
            leaderboard_type = ""
            message2 = message
            deleteName = ""
            found = False

            #leaderboard_list = ["jogger", "pikachu"]

            if "," in message2.content.lower():
                await client.send_message(message.channel, "**(ENDAST ADMINS)** Inga kommatecken. *Format* ?delete LEADERBOARD_TYPE NAMN")
            else:
                # Which leaderboard the user is updating
                try:
                    message2 = message2.content.lower()
                    message2 = message2[8:].split(" ")

                    leaderboard_type = message2[0]

                    # Name to delete part of string
                    deleteName = message2[1]

                except Exception as e:
                    print("Error deleting: %s" % str(e))
                    await client.send_message(message.channel, "**(ENDAST ADMINS)** *Format* ?delete LEADERBOARD_TYPE NAMN")

                # beautiful variable name
                linesToKeepInFile = []
                deleteIndex = 0

                # Check if author is admin or (TESTROLE)
                if '435908470936698910' or '342771363884302339' in [role.id for role in message.author.roles]:
                    #Admin is trying to remove entry from Leaderboard
                    if leaderboard_type.lower() in leaderboard_list:
                        print("Deleting %s from %s leaderboard" % (deleteName, leaderboard_type))
                        dltFile = open("%s.txt"%leaderboard_type, "r")
                        for index, line in enumerate(dltFile):
                            splitLine = line.split(' ')
                            # Found name trying to delete from file in file
                            if splitLine[0].lower() == deleteName.lower():
                                found = True
                                await client.send_message(message.channel, "%s hittades, %s tas bort från %s leaderboarden." % (deleteName,deleteName,leaderboard_type))
                            else:
                                linesToKeepInFile.append(line)
                        if found:
                            # Write back lines with the exception of the deleted element
                            dltFile = open("%s.txt"%leaderboard_type, "w")
                            for elem in linesToKeepInFile:
                                dltFile.write(elem)
                            dltFile.close()
                            await refresh(message, id_list, leaderboard_list)
                        else:
                            await client.send_message(message.channel, "%s kunde inte hittas i %s leaderboarden." % (deleteName,leaderboard_type))
                else:
                    await client.send_message(message.channel, "Endast admins är tillåtna att radera resultat från leaderboards, var god kontakta en admin.")

        # E U R E K A
        elif message.content.upper().startswith('GODNATT') and message.author.id == '169688623699066880':
            await client.send_message(message.channel, "Godnatt %s! :slight_smile: :sleeping:" % message.author.mention)

        elif message.content.upper().startswith('?CLAIM') and message.channel.id == id_list[0]:
            await client.send_message(message.channel, "Du har redan claimat ditt användarnamn %s, kontakta admins om du bytt användarnamn." % message.author.mention)

        elif message.content.upper().startswith('?ADMIN_CLAIM') and message.channel.id == id_list[0]:
            await admin_claim(message, leaderboard_list)

        # elif message.content.upper().startswith('?') and message.channel.id == id_list[3]:
        #    await client.send_message(message.channel, "Denna kanal är endast till för att få tillgång till leaderboards %s. Se till att ditt Discord användarnamn matchar det i Pokémon Go och skriv ?claim för att börja." % message.author.mention)

        elif '@EVERYONE' in message.content.upper() and not ('342771363884302339' in [role.id for role in message.author.roles]):
            # Weavile Bot
            for role in message.server.roles:
                if '435908470936698910' in role.id:
                    await client.send_message(message.channel, "Ping! %s" % role.mention)
                elif '342771363884302339' in role.id:
                    await client.send_message(message.channel, "Ping! %s" % role.mention)

        # Last if statement, invalid command
        elif message.content.upper().startswith('?') and message.channel.id == id_list[0]:
            await client.send_message(message.channel, "Detta kommandot finns inte, skriv ?help för en lista på kommandon.")
