import asyncio
import re
import discord
from discord.ext import commands
import common
from datetime import datetime
from instance import bot


class Leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=common.LEADERBOARD_LIST, help="This command adds an entry to a given"
                                                                               " leaderboard.\nExample: ?jogger 507")
    async def leaderboard(self, ctx, score):

        # needed for integration-test invoke, because invoked_with returns ?test
        # instead of ?leaderboard_type, attempts float cast to check
        invoked = ctx.invoked_with
        try:
            float(score)
        except:
            if not invoked == "refresh":
                invoked = score
                score = "3.0"

        # Check if users display name is in claim list
        earlyCheck = False
        tempScore = score
        unitString = ""
        fileCheck = open("textfiles/idclaims.txt", "r")
        for item in fileCheck:
            item = item.split(" ")
            if str(item[0].lower()) == str(ctx.message.author.display_name.lower()):
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
            leaderboard_type = invoked

            # Sneasel is trying to refresh, set true and set leaderboard type
            if leaderboard_type.lower() == "refresh":
                sneaselRefresh = True
                leaderboard_type = score.lower()

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
                upperLimit = 50000
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
            channel2 = []
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
                    await ctx.send("Poäng endast i siffror. *Format: ?leaderboard poäng*")
                    floatError = True

            # if integration-testing, only update totalxp embed
            if (not floatError and not common.INTEGRATION_TESTING) or sneaselRefresh or (common.INTEGRATION_TESTING and totalxpTrue): # need to skip with integration test because otherwise leaderboards test takes ages
                # if Sneasel is not refreshing, check name for illegal characters
                if not sneaselRefresh:
                    tempScore = float(tempScore)
                    p = re.compile('\d+(\.\d+)?')
                    stringPattern = r'[^\.A-Za-z0-9]'
                    # Check for illegal nickname symbols, + ensures min size == 1
                    if re.search(stringPattern, ctx.message.author.display_name):
                        checkFailed = True
                        await ctx.send("Ditt Discord användarnamn innehåller otillåtna tecken, var god ändra ditt "
                                       "användarnamn så att det matchar Pokémon Go användarnamnet.")
                    elif not p.match(str(tempScore)):
                        checkFailed = True
                        await ctx.send("Error: Otillåtna tecken i poängen. *Format: ?leaderboard poäng*")
                    elif len(ctx.message.author.display_name) > 15:
                        checkFailed = True
                        await ctx.send("Error: Namn får vara max 15 tecken. Var god uppdatera ditt Discord "
                                       "användarnamn. Fråga admins om hjälp vid besvär.")
                if not checkFailed:
                    # Create temp leaderboardList to be inserted if applicable
                    tempList.append(ctx.message.author.display_name)
                    tempList.append(tempScore)
                    tempList.append(current_dt.date())

                    # if Sneasel is not refreshing, check score for illegal characters
                    if not sneaselRefresh:
                        # Cast entry number to float
                        if tempScore > upperLimit:
                            await ctx.send(f"Poäng [{tempScore}] högre än tillåtet [{upperLimit}] i {leaderboard_type}.")
                            checkFailed = True
                        elif tempScore < 1 and not sneaselRefresh:
                            await ctx.send(f"Poäng [{tempScore}] lägre än tillåtet [{1}] i {leaderboard_type}.")
                            checkFailed = True
                        elif floatError and not sneaselRefresh:
                            await ctx.send(f"Poäng [{tempScore}] får inte innehålla annat än siffror.")
                            checkFailed = True
                    if not checkFailed:
                        with open("leaderboards/%s.txt" % leaderboard_type) as file:
                            leaderboardList = [line.split(" ") for line in file]
                        if not sneaselRefresh:
                            # Check if player is already in standings, update
                            found = False
                            for index, elem in enumerate(leaderboardList):
                                # If player already exists
                                if ctx.message.author.display_name.lower() == elem[0].lower() and not found:
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
                                            elif tempScore > float(elm[1]) or (
                                                    tempScore == 1 and float(elm[1]) == 1):
                                                # Insert updated score
                                                if not joggerTrue:
                                                    tempList[1] = float(tempList[1])
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
                                    if (tempScore > float(elem[1]) or (
                                            tempScore == 1 and float(elem[1]) == 1)) and not insertedBool:
                                        if not joggerTrue:
                                            tempList[1] = float(tempList[1])
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
                        file = open("leaderboards/%s.txt" % leaderboard_type, "w")
                        for item in leaderboardList:
                            item2 = ' '.join(str(x) for x in item)
                            if item == tempList:
                                file.write("%s\n" % item2)
                            else:
                                file.write("%s" % item2)
                        file.close()
                    embed = discord.Embed()
                    # http://pokemongo.wikia.com/wiki/Medals
                    if joggerTrue:
                        embed = discord.Embed(title="Leaderboard Karlskrona: Jogger \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/9/98/Jogger_Gold.png/revision/latest?cb=20161013235539")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[1])
                    elif pikachuTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Pikachu Fan \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/9/94/PikachuFan_Gold.png/revision/latest?cb=20161013235542")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[2])
                    elif battlegirlTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Battle Girl \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/9/93/BattleGirl_Gold.png/revision/latest?cb=20161013235336")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[4])
                    elif pokedexTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Pokédex \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/4/43/Kanto_Gold.png/revision/latest?cb=20161013235541")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[5])
                    elif collectorTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Collector \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/8/86/Collector_Gold.png/revision/latest?cb=20161014002520")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[6])
                    elif scientistTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Scientist \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/7/7c/Scientist_Gold.png/revision/latest?cb=20161013235610")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[7])
                    elif breederTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Breeder \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/b/b7/Breeder_Gold.png/revision/latest?cb=20161013235426")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[8])
                    elif backpackerTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Backpacker \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/b/bb/Backpacker_Gold.png/revision/latest?cb=20161013235335")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[9])
                    elif fishermanTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Fisherman \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/6/69/Fisherman_Gold.png/revision/latest?cb=20161013235429")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[10])
                    elif youngsterTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Youngster \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/9/94/Youngster_Gold.png/revision/latest?cb=20161013235612")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[11])
                    elif berrymasterTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Berry Master \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/9/92/BerryMaster_Gold.png/revision/latest?cb=20170623010756")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[12])
                    elif gymleaderTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Gym Leader \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/f/f9/GymLeader_Gold.png/revision/latest?cb=20170623010816")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[13])
                    elif championTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Champion \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/2/20/Champion_Gold.png/revision/latest?cb=20170623133823")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[14])
                    elif battlelegendTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Battle Legend \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/6/61/BattleLegend_Gold.png/revision/latest?cb=20170623133841")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[15])
                    elif rangerTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Pokémon Ranger \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/7/77/Researcher_Gold.png/revision/latest?cb=20180328115039")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[16])
                    elif unownTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Unown \n", color=0xff9900, description=(
                                    "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/1/1b/Unown_Gold.png/revision/latest?cb=20170217162806")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[17])
                    elif gentlemanTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Gentleman \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/f/f0/Gentleman_Gold.png/revision/latest?cb=20180621120608")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[18])
                    elif pilotTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Pilot \n", color=0xff9900, description=(
                                    "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/4/4e/Pilot_Gold.png/revision/latest?cb=20180621120613")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[19])
                    elif totalxpTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Total XP \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/b/bd/Pok%C3%A9mon_GO_Fest_Chicago_2017.png/revision/latest?cb=20170726115410")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[20])
                    elif goldgymsTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Gold Gyms \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/0/0a/Gym_Badge_Tier_Gold.png/revision/latest?cb=20170620224940")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[21])
                    elif idolTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Idol \n", color=0xff9900, description=(
                                    "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/9/9b/Idol_Gold.png/revision/latest?cb=20180621120611")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[22])
                    elif greatleagueTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Great League Veteran \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/2/28/GreatLeague_Gold.png/revision/latest?cb=20190113004308")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[23])
                    elif ultraleagueTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Ultra League Veteran \n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/5/5e/UltraLeague_Gold.png/revision/latest?cb=20190113004309")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[24])
                    elif masterleagueTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Master League Veteran \n",
                                              color=0xff9900, description=(
                                        "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/d/d7/MasterLeague_Gold.png/revision/latest?cb=20190113004311")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[25])
                    elif acetrainerTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Ace Trainer\n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/9/9c/AceTrainer_Gold.png/revision/latest?cb=20161013235333")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[26])
                    elif cameramanTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Cameraman\n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/1/19/Cameraman_Gold.png/revision/latest?cb=20190220234724")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[27])
                    elif heroTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Hero\n", color=0xff9900, description=(
                                    "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/5/52/Hero_Gold.png/revision/latest?cb=20190722124317")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[28])
                    elif purifierTrue:
                        embed = discord.Embed(title="Leaderboard Blekinge: Purifier\n", color=0xff9900,
                                              description=(
                                                          "Skriv '?%s poäng' i #leaderboards för att bli tillagd" % leaderboard_type))
                        embed.set_thumbnail(
                            url="https://vignette.wikia.nocookie.net/pokemongo/images/4/47/Purifier_Gold.png/revision/latest?cb=20190722124336")
                        embed.set_footer(
                            text="Övriga poäng är gömda, ta reda på hur du matchar mot övriga spelare med kommandot ?ranks")
                        embed.add_field(name="\u200b", value="\u200b", inline=False)
                        channel2 = bot.get_channel(common.LEADERBOARD_CHANNELS[29])

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
                                embed.add_field(
                                    name="%i. %s - %i %s" % (float(currentRank), elem[0], float(elem[1]), unitString),
                                    value="Updated: %s" % (elem[2]), inline=True)
                            else:
                                embed.add_field(name="%i. %s - %.1f %s" % (
                                float(currentRank), elem[0], float(elem[1]), unitString),
                                                value="Updated: %s" % (elem[2]), inline=True)
                    try:
                        await channel2.purge(limit=5)
                    except Exception as e:
                        for dev in common.DEVELOPERS:
                            user = ctx.bot.get_user(dev)
                            await user.send(f"""Error in LEADERBOARD command: 
                                                Failed to delete {invoked} embed with error: {e}""")

                    await asyncio.sleep(1)
                    if newTopOne and not common.INTEGRATION_TESTING:
                        await ctx.send(":crown: :first_place: GRATULERAR %s, du har nått #%i i %s leaderboarden. "
                                       "\nVar god skicka in en in-game-screenshot till valfri admin för att "
                                       "bekräfta dina poäng." % (
                                                  ctx.message.author.mention, currentRankList[insertedIndex],
                                                  leaderboard_type.capitalize()))
                    elif topThree and not common.INTEGRATION_TESTING:
                        await ctx.send(":crown: Gratulerar %s till din #%i placering i %s leaderboarden. "
                                       "\nVar god skicka in en in-game-screenshot till valfri admin för att "
                                       "bekräfta dina poäng." % (
                                                  ctx.message.author.mention, currentRankList[insertedIndex],
                                                  leaderboard_type.capitalize()))
                    elif scoreUpdated and not common.INTEGRATION_TESTING:
                        await ctx.send("Gratulerar %s, du är placerad #%i i %s leaderboarden. "
                                       "Kolla %s för att se top 10." % (
                                                  ctx.message.author.mention, currentRankList[insertedIndex],
                                                  leaderboard_type.capitalize(), channel2.mention))
                    if sneaselRefresh:
                        await ctx.send("Leaderboarden har laddats om.")
                    await channel2.send(embed=embed)
        else:
            if not common.INTEGRATION_TESTING:
                await ctx.send("Dina poäng har inte skickats vidare då ditt användarnamn inte matchar det tidigare satta. "
                           "Ta kontakt med valfri admin.")
            raise AssertionError("Error: Member tried to submit to leaderboard with changed nickname.")

    @leaderboard.error
    async def leaderboard_on_error(self, ctx, error):
        for dev in common.DEVELOPERS:
            user = ctx.bot.get_user(dev)
            await user.send(f"""Error in LEADERBOARD command: {error}""")


def setup(bot):
    bot.add_cog(Leaderboards(bot))
