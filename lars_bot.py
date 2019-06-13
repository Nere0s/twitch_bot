from bot_setup import *

HOST = 'irc.twitch.tv'
PORT = 6667
PASS = 'oauth:'+'YOUR_SECRET_FOR_LOGIN_HERE'
IDENT = 'YOUR_IDENT_HERE'
CHANNEL = 'larsmenstreaming'

s = openSocket(HOST, PORT, PASS, IDENT, CHANNEL)
joinRoom(s)

main_bot = MainBot(s, CHANNEL)
main_bot.start()
