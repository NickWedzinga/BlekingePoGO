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
commandChannel = client.get_channel('466563505462575106')


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


# Refresh function
@client.event
async def refresh(message, id_list):
    """Refresh function, parses and presents leaderboard of choosing."""
    leaderboard_type = message.content.lower().split(" ", 2)[1]
    leaderboard_list = ["jogger", "pikachu"]

    if leaderboard_type in leaderboard_list:
        await leaderboard(message, id_list)
        # await client.send_message(message.channel, "?%s 1" % leaderboard_type)
    else:
        await client.send_message(message.channel, "%s leaderboard existerar inte." % leaderboard_type.capitalize())


# Claim function, assigns claim role, adds user ID to a list
@client.event
async def claim(message):
    """Claim function, assigns claim role, adds user ID to a list."""
    claimMsg = message
    claimedIDs = []

    #Add information of user to temporary list
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

    with open("idclaims.txt") as file:
        claimedIDs = [line.split(" ") for line in file]

    # Read for ID in file
    claimFile = open("idclaims.txt", "r")
    for item in claimedIDs:
        print(item)
        if float(item[1]) == float(message.author.id):
            await client.send_message(message.channel, ":no_entry: Du har redan claimat ditt användarnamn %s, om du har bytt användarnamn kontakta en valfri admin." % message.author.mention)
            found = True
    claimFile.close()
    print(tempID)
    print(claimedIDs)
    # Write to file
    if not found:
        #Add to list
        claimedIDs.insert(0, tempID)
        print(claimedIDs)
        # Add ID to file
        print("Adding new user")
        claimFile = open("idclaims.txt", "w")
        for item in claimedIDs:
            claimFile.write(item[0])
            claimFile.write(" ")
            claimFile.write(item[1])

        claimFile.close()
        claimedRole = get(message.author.server.roles, name="claimed")
        await client.add_roles(message.author, claimedRole)
        # assign role is not claimed yet, send PM with help info
        await client.send_message(message.channel, ":white_check_mark: %s du har claimat användarnamnet %s. Du kommer få ett privatmeddelande alldeles strax med mer info." % (message.author.mention, message.author.display_name))
        await client.send_message(message.author, "Tjena, läget")

# Leaderboard function
@client.event
async def leaderboard(message, id_list):
    """Leaderboard function, records, adds and presents leaderboards."""
    joggerTrue = False
    pikachuTrue = False
    sneaselRefresh = False

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
                                  "Korrekt sätt att skicka in dina poäng är ?%s 'POÄNG. \n*Exempel: ?jogger 2500*" %
                                  (leaderboard_type))

    # Replace possible commas with dots
    tempScore = str(tempScore.replace(",", "."))

    if leaderboard_type == "jogger":
        joggerTrue = True
        upperLimit = 20000
    elif leaderboard_type == "pikachu":
        pikachuTrue = True
        upperLimit = 5000

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
            await client.send_message(message.channel, "Poäng endast i siffror. *Format: ?LEADERBOARD_TYPE POÄNG*")
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
                await client.send_message(message.channel, "Error: Otillåtna tecken i poängen. *Format: ?LEADERBOARD_TYPE POÄNG*")
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
                elif tempScore < 1 and not sneaselRefresh:
                    await client.send_message(message.channel, "Poäng lägre än tillåtet.")
                elif floatError and not sneaselRefresh:
                    await client.send_message(message.channel, "Poäng får inte innehålla annat än siffror.")
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
                                    elif tempScore > float(elm[1]):
                                        # Insert updated score
                                        if pikachuTrue:
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
                            if tempScore >= float(elem[1]) and not insertedBool:
                                if pikachuTrue:
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

            # Medal images: http://pokemongo.wikia.com/wiki/Medals
            # https://pokemongo.gamepress.gg/sites/pokemongo/files/2018-02/Badge_Walking_GOLD_01.png
            unitString = ""
            if joggerTrue:
                embed = discord.Embed(title="Leaderboard Karlskrona: Jogger \n", color=0xff9900)
                embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/98/Jogger_Gold.png/revision/latest?cb=20161013235539")
                embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                embed.add_field(name="\u200b", value="\u200b", inline=False)
                channel2 = client.get_channel(id_list[1])
                unitString = "km"
            elif pikachuTrue:
                embed = discord.Embed(title="Leaderboard Karlskrona: Pikachu \n", color=0xff9900)
                embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/pokemongo/images/9/94/PikachuFan_Gold.png/revision/latest?cb=20161013235542")
                embed.set_footer(text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                embed.add_field(name="\u200b", value="\u200b", inline=False)
                channel2 = client.get_channel(id_list[2])

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

                    # Pikachu can't have decimals
                    if pikachuTrue:
                        embed.add_field(name="%i. %s - %i %s" % (int(currentRank), elem[0], int(elem[1]), unitString), value="Updated: %s" % (elem[2]), inline=True)
                    else:
                        embed.add_field(name="%i. %s - %.1f %s" % (int(currentRank), elem[0], float(elem[1]), unitString), value="Updated: %s" % (elem[2]), inline=True)

            async for x in client.logs_from(channel2, 10):
                try:
                    await client.delete_message(x)
                except:
                    print("somehow failed to delete message")

            await asyncio.sleep(1)
            if newTopOne:
                await client.send_message(message.channel, ":crown: :first_place: GRATULERAT %s, du har nått #%i i %s leaderboarden. \nVar god skicka in en in-game-screenshot till valfri admin för att bekräfta dina poäng." % (message.author.mention, currentRankList[insertedIndex], leaderboard_type.capitalize()))
            elif topThree:
                await client.send_message(message.channel, ":crown: Gratulerat %s till din #%i placering i %s leaderboarden. \nVar god skicka in en in-game-screenshot till valfri admin för att bekräfta dina poäng." % (message.author.mention, currentRankList[insertedIndex], leaderboard_type.capitalize()))
            elif scoreUpdated:
                await client.send_message(message.channel, "Gratulerat %s, du placerade #%i i %s leaderboarden. Kolla %s för att se top 10." % (message.author.mention, currentRankList[insertedIndex], leaderboard_type.capitalize(), channel2.mention))
            await client.send_message(message.channel, "Leaderboarden har skapats om.")
            await client.send_message(channel2, embed=embed)


def checkMessages(id_list):
    """Checks for messages, calls appropriate functions."""
    print("Checking for messages..")

    @client.event
    async def on_message(message):

        # Test if bot is still responsive
        if (message.content.upper().startswith('?TEST') and message.channel.id == id_list[0]):
            await client.send_message(message.channel, "Ja, hej! Hallå! :sweat_smile:")

        # Claim nick for your ID
        if (message.content.upper().startswith('?CLAIM') and message.channel.id == id_list[3]):
            await claim(message)


        # REFRESH, Format: ?refresh LEADERBOARD_TYPE
        elif(message.content.upper().startswith('?REFRESH') and message.channel.id == id_list[0]):
            await refresh(message, id_list)

        # LEADERBOARDS Format: ?LEADERBOARD_TYPE, SCORE
        elif ((message.content.upper().startswith('?JOGGER') or message.content.upper().startswith('?PIKACHU')) and message.channel.id == id_list[0]):
            await leaderboard(message, id_list)


        # List ranks across leaderboards
        elif message.content.upper().startswith('?RANKS') and message.channel.id == id_list[0]:
            nickname = message.author.display_name
            tempList = []
            leaderboard_list = ["jogger","pikachu"]
            unitString = ""
            currentRank = 0
            currentScore = 0
            currentRankList = []

            num2words1 = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five',
                          6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten',
                          11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen',
                          15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen'}

            # Loop through leaderboard types
            for item in leaderboard_list:
                if item == "jogger":
                    unitString = "km"
                elif item == "pikachu":
                    unitString = "fångster"
                leaderboard_file = open("%s.txt" % item, "r")
                # Loop through file
                for index, line in enumerate(leaderboard_file):
                    line = line.split(" ")

                    # If score not same as previous player, update rank
                    if not float(currentScore) == float(line[1]):
                        currentRank = index + 1
                        currentScore = float(line[1])

                    if line[0].lower() == nickname.lower():
                        localScore = round(float(line[1]), 1)
                        if item == "pikachu":
                            localScore = int(localScore)
                        if(currentRank == 1):
                            await client.send_message(message.channel, ":first_place: %s är placerad \#%i i %s leaderboarden med %s %s." % (message.author.mention, currentRank, item.capitalize(), localScore, unitString))
                        elif(currentRank == 2):
                            await client.send_message(message.channel, ":second_place: %s är placerad \#%i i %s leaderboarden med %s %s." % (message.author.mention, currentRank, item.capitalize(), localScore, unitString))
                        elif(currentRank == 3):
                            await client.send_message(message.channel, ":third_place: %s är placerad \#%i i %s leaderboarden med %s %s." % (message.author.mention, currentRank, item.capitalize(), localScore, unitString))
                        elif(currentRank == 10):
                            await client.send_message(message.channel, ":keycap_%s: %s is ranked \#%i in the %s leaderboards with a score of %s %s." % (num2words1[currentRank].lower(), message.author.mention, currentRank, item.capitalize(), localScore, unitString))
                        elif(currentRank > 3 and currentRank < 11):
                            await client.send_message(message.channel, ":%s: %s is ranked \#%i in the %s leaderboards with a score of %s %s." % (num2words1[currentRank].lower(), message.author.mention, currentRank, item.capitalize(), localScore, unitString))
                        elif currentRank > 10:
                            await client.send_message(message.channel, ":asterisk: %s is ranked \#%i in the %s leaderboards with a score of %s %s." % (message.author.mention, currentRank, item.capitalize(), localScore, unitString))
                        else:
                            await client.send_message(message.channel, "%s is not ranked in the %s leaderboards, submit a score by typing ?%s 'YOUR_SCORE'." % (message.author.mention, item.capitalize(), item))

        #DELETE, admins may delete leaderboard entries Format: ?delete leaderboard_type name_to_delete
        elif message.content.upper().startswith('?DELETE') and message.channel.id == '466563505462575106':
            leaderboard_type = ""
            message2 = message
            deleteName = ""
            found = False
            if "," in message2.content.lower():
                await client.send_message(message.channel, "**(ENDAST ADMINS)** Inga kommatecken. *Format* ?delete LEADERBOARD_TYPE NAMN")
            else:
                #Which leaderboard the user is updating
                try:
                    message2 = message2.content.lower()
                    #message2 = message2.replace(",","")
                    message2 = message2[8:].split(" ")

                    leaderboard_type = message2[0]

                    #Name to delete part of string
                    deleteName = message2[1]

                except Exception as e:
                    print("Error deleting: %s" % str(e))
                    await client.send_message(message.channel, "**(ENDAST ADMINS)** *Format* ?delete LEADERBOARD_TYPE NAMN")

                #beautiful variable name
                linesToKeepInFile = []
                deleteIndex = 0

                #Check if author is admin (TESTROLE)
                if '435908470936698910' in [role.id for role in message.author.roles]:
                    #Admin is trying to remove entry from Leaderboard
                    if leaderboard_type.lower() == "jogger":
                        print("Deleting name from jogger leaderboard")
                        dltFile = open("%s.txt"%leaderboard_type, "r")
                        for index, line in enumerate(dltFile):
                            splitLine = line.split(' ')
                            #Found name trying to delete from file in file
                            if splitLine[0].lower() == deleteName.lower():
                                found = True
                                await client.send_message(message.channel, "%s hittades, %s tas bort från %s leaderboarden." % (deleteName,deleteName,leaderboard_type))
                            else:
                                linesToKeepInFile.append(line)
                        if found:
                            #Write back lines with the exception of the deleted element
                            dltFile = open("%s.txt"%leaderboard_type, "w")
                            for elem in linesToKeepInFile:
                                dltFile.write(elem)
                            dltFile.close()
                            await refresh(message, id_list)
                        else:
                            await client.send_message(message.channel, "%s kunde inte hittas i %s leaderboarden." % (deleteName,leaderboard_type))
                else:
                    await client.send_message(message.channel, "Endast admins är tillåtna att radera resultat från leaderboards, var god kontakta en admin.")

        # E U R E K A
        elif message.content.upper().startswith('EUREKA'):
            await client.send_message(message.channel, "We did it! :smile:")

        #Last if statement, invalid command
        elif message.content.upper().startswith('?') and message.channel.id == id_list[0]:
            await client.send_message(message.channel, "Detta kommandot finns inte, skriv ?help för en lista på kommandon :sob:")