import EventHandler

# Start the bot
EventHandler.startup()
# Read message every loop,  act accordingly

# Sneasel List
id_list = []
with open("version.txt", "r") as versionFile:
    version = versionFile.read()
# Dev list: command channel[0], jogger[1], pikachu[2],
#           support[3], battlegirl[4], pokedex[5],
#           collector[6], scientist[7], breeder[8],
#           backpacker[9], fisherman[10], youngster[11],
#           berrymaster[12], gymleader[13], champion[14],
#           battlelegend[15], ranger[16], unown[17],
#           gentleman[18], pilot[19], totalxp[20]...
# Weavile - pc
if version == "1":
    id_list = ['466563505462575106', '466913214656020493', '467754615413407745',
               '468760503125147648', '469079191002939415', '469121554488360971',
               '469121572523737098', '469121587807780864', '469121601267433493',
               '469121615838576640', '469121630829019136', '469121663905300490',
               '469121687506518037', '469121703348273152', '469121718271868928',
               '469121735795539988', '469121769639378944', '469121782473949186',
               '469121809162174495', '469121836651642911', '469122055439384577',
               '478886996064993280', '493847327925075968', '540876695264034834',
               '540876711202652160', '540876727698718721', '560905350405029888',
               '560905402825310209', '605836493218643988', '605836537019760640']
# Sneasel - pi
elif version == "0":
    id_list = ['469095507759726603', '469095668137459712', '469095701947875338',
               '342760722058706945', '469095719178076170', '469117787076296705',
               '469150849642266624', '469150873776553994', '469150888150433802',
               '469150905384828939', '469150918139576320', '469150935663378442',
               '469150955372412928', '469150979200385025', '469150995268632576',
               '469151014302384128', '469151036188262420', '469151049828007946',
               '469151070137090048', '469151084124962816', '469150770881888266',
               '478894031678603266', '493848833932001301', '540882217845522432',
               '540882231816617986', '540882247142604810', '560906125026000897',
               '560906243258974231', '605837275061944355', '605837367764320284']

print("Version: %s" % version)
EventHandler.checkMessages(id_list)
# Infinite blocking loop
with open("apitoken.txt", "r") as apiFile:
    apitoken = apiFile.read()
EventHandler.client.run(apitoken)
EventHandler.client.close()

# BUG LIST ------------------------------------------
# ingen error decimaler pilot

# detached, solution: screen -r -d "PID". EX: screen -r -d 615

# unclosed client session, tyder på annan error händer ibland, stänger ner
# och loggar ut Sneasel.

# ?admin_claim does not work anymore, weird asyncio behavior
# takes too long to find, copy and write to file?
# rewrite function, must be easier.
# if x in line, file.write(line.replace(oldname, newname))
# tempfix: sed -i 's/oldText/newText/g' idclaims.txt


# TODO: ---------------------------------------------
# vid update skriv ut : Ny score: %i, gammal score %i
# skriv tester som langar grönt, testa allt som kan gå sönder, kommando ?tester, måste vara admin
# Notify om man som top 3 knuffas ner en spot

# GENERAL-----------------------------------------------------
# cp idclaims.txt idclaims2.txt


# FINDPLAYER------------------------------ch--------------------
# format: ?findplayer jogger mcmomo, returnar index på mcmomo i jogger


# OVERALL-----------------------------------------------------
# Funkar bara när spelaren är rankad i samtliga leaderboards

# När spelaren uppdaterar en leaderboard så uppdateras även overall

# score = index i samtliga leaderboards / antal leaderboards


# CREATING NEW LEADERBOARDS---------------------------------------------
# Lista på saker att fixa vid nya leaderboards:
#   Skapa Discord kanal
#   Lägg till kanal id i id_list här i main.py
#   Skapa .txt fil på PC (Sneasel 1 2018-07-11)
#   Lägg till .txt i .gitignore
#   Lägg till i checkMessage leaderboard_list
#   Om decimaler, lägg till i if not joggerTrue or..: int()
#   Lägg till joggerTrue i leaderboard(message, id_list)
#   Lägg till upperLimit i if joggerTrue i leaderboard(message, id_list)
#   Lägg till embed, ändra icon i leaderboards, samt ändra title, samt channel2 index
#   Lägg till enhet i checkmessages() -> ?RANKS
#   Om decimaler, Lägg till i ranks if not item in "jogger", ...
#   Om decimaler, ändra if joggertrue tempscore replace , med . i leaderboards
#   git push PC + git pull på PI
#   Skapa .txt fil på Pi, skapa 2.txt fil på PI (cat > idol.txt, skriv Sneasel 1 2018-07-11, ctrl+d ctrl+d) för att kontrollera "cat idol.txt"
#   Lägg till i cp listan på Pi, cp idol.txt idol2.txt


# DELETE-----------------------------------------------------


# REFRESH----------------------------------------------------


# RANKS-----------------------------------------------


# LIST ----------------------------------------------------


# CLAIM----------------------------------------------


# ADMIN_CLAIM----------------------------------------


# ?HELP ----------------------------------------------------


"""
Traceback (most recent call last):
  File "/home/pi/.local/lib/python3.5/site-packages/discord/gateway.py", line 430, in poll_event
    msg = yield from self.recv()
  File "/home/pi/.local/lib/python3.5/site-packages/websockets/protocol.py", line 319, in recv
    raise ConnectionClosed(self.close_code, self.close_reason)
websockets.exceptions.ConnectionClosed: WebSocket connection is closed: code = 1006, no reason.

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/pi/.local/lib/python3.5/site-packages/discord/client.py", line 448, in connect
    yield from self.ws.poll_event()
  File "/home/pi/.local/lib/python3.5/site-packages/discord/gateway.py", line 435, in poll_event
    raise ResumeWebSocket() from e
discord.gateway.ResumeWebSocket

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "Main.py", line 44, in <module>
    EventHandler.client.run(apitoken)
  File "/home/pi/.local/lib/python3.5/site-packages/discord/client.py", line 519, in run
    self.loop.run_until_complete(self.start(*args, **kwargs))
  File "/usr/lib/python3.5/asyncio/base_events.py", line 466, in run_until_complete
    return future.result()
  File "/usr/lib/python3.5/asyncio/futures.py", line 293, in result
    raise self._exception
  File "/usr/lib/python3.5/asyncio/tasks.py", line 239, in _step
    result = coro.send(None)
  File "/home/pi/.local/lib/python3.5/site-packages/discord/client.py", line 491, in start
    yield from self.connect()
  File "/home/pi/.local/lib/python3.5/site-packages/discord/client.py", line 452, in connect
    self.ws = yield from DiscordWebSocket.from_client(self, resume=resume)
  File "/home/pi/.local/lib/python3.5/site-packages/discord/gateway.py", line 207, in from_client
    timeout=60, loop=client.loop)
  File "/usr/lib/python3.5/asyncio/tasks.py", line 400, in wait_for
    return fut.result()
  File "/usr/lib/python3.5/asyncio/futures.py", line 293, in result
    raise self._exception
  File "/usr/lib/python3.5/asyncio/tasks.py", line 239, in _step
    result = coro.send(None)
  File "/home/pi/.local/lib/python3.5/site-packages/discord/gateway.py", line 65, in _ensure_coroutine_connect
    ws = yield from websockets.connect(gateway, loop=loop, klass=klass)
  File "/home/pi/.local/lib/python3.5/site-packages/websockets/py35/client.py", line 19, in __await__
    return (yield from self.client)
  File "/home/pi/.local/lib/python3.5/site-packages/websockets/client.py", line 215, in connect
    extra_headers=extra_headers)
  File "/home/pi/.local/lib/python3.5/site-packages/websockets/client.py", line 125, in handshake
    raise InvalidStatusCode(status_code)
websockets.exceptions.InvalidStatusCode: Status code not 101: 520
Unclosed client session
client_session: <aiohttp.client.ClientSession object at 0x75e179b0>
Unclosed client session
client_session: <aiohttp.client.ClientSession object at 0x75e3c3b0>
Task exception was never retrieved
future: <Task finished coro=<WebSocketCommonProtocol.run() done, defined at /home/pi/.local/lib/python3.5/site-packages/websockets/protocol.py:428> exception=ConnectionResetError(104, 'Connection reset by peer')>
Traceback (most recent call last):
  File "/usr/lib/python3.5/asyncio/tasks.py", line 241, in _step
    result = coro.throw(exc)
  File "/home/pi/.local/lib/python3.5/site-packages/websockets/protocol.py", line 434, in run
    msg = yield from self.read_message()
  File "/home/pi/.local/lib/python3.5/site-packages/websockets/protocol.py", line 456, in read_message
    frame = yield from self.read_data_frame(max_size=self.max_size)
  File "/home/pi/.local/lib/python3.5/site-packages/websockets/protocol.py", line 511, in read_data_frame
    frame = yield from self.read_frame(max_size)
  File "/home/pi/.local/lib/python3.5/site-packages/websockets/protocol.py", line 546, in read_frame
    self.reader.readexactly, is_masked, max_size=max_size)
  File "/home/pi/.local/lib/python3.5/site-packages/websockets/framing.py", line 86, in read_frame
    data = yield from reader(2)
  File "/usr/lib/python3.5/asyncio/streams.py", line 668, in readexactly
    yield from self._wait_for_data('readexactly')
  File "/usr/lib/python3.5/asyncio/streams.py", line 458, in _wait_for_data
    yield from self._waiter
  File "/usr/lib/python3.5/asyncio/futures.py", line 380, in __iter__
    yield self  # This tells Task to wait for completion.
  File "/usr/lib/python3.5/asyncio/tasks.py", line 304, in _wakeup
    future.result()
  File "/usr/lib/python3.5/asyncio/futures.py", line 293, in result
    raise self._exception
  File "/usr/lib/python3.5/asyncio/selector_events.py", line 723, in _read_ready
    data = self._sock.recv(self.max_size)
ConnectionResetError: [Errno 104] Connection reset by peer

"""
