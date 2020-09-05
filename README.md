# BlekingePoGO

BlekingePoGO is a Discord bot currently server-specific for the Blekinge Pokémon GO server.
It acts as a moderation tool as well as provides an array of features for its users.

BlekingePoGO is written in Python and based on the discord.py Discord API wrapper.
The application contains an array of tech including mysql, REST-lookup, discord.py, schedule and JSON parsing.

## Scheduling

By utilizing the schedule Python package and storing scheduling information in the mysql database, BlekingePoGO supports the ability to schedule any task.

## Raids

BlekingePoGO acts as an orchestration tool for raids. Users are able to create raid-specific channels through a command.
The created channels are automatically deleted upon raid-end through the scheduling component.
Each created channel is provided with an informative embed containing data on the Pokémon that's being raided, the application is able to do this through the Pokédex lookup functionality.

## Leaderboards

Users may submit their scores in several medals and categories to the BlekingePoGO bot.
The score data is stored in the mysql database.
BlekingePoGO then compiles all the data into separate leaderboards, one for each medal/category and ranks it's users, showing the top 10.

Users are also able to lookup their own specific scores by using the ?ranks and ?list commands.

## Pokédex Lookup

Through REST lookup, BlekingePoGO is able to provide its users with up-to-date information on any Pokémon in Pokémon GO.
It's able to list every Pokémons typing, available move-pools as well as calculates their maximum CP at several important levels.
In addition to that, the lookup is also able to provide information as to wether the Pokémon has been released and if their shiny version has been released.

## Public Use

Currently BlekingePoGO is server-specific to the Blekinge PoGO Discord server and does not support additional servers.
