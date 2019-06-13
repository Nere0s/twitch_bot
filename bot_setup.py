import socket
import time
import random

# load quote file
with open('stronhold.bot') as f:
    content = f.readlines()
stronhold = [x.strip() for x in content]

def openSocket(HOST, PORT, PASS, IDENT, CHANNEL):
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(('PASS ' + PASS + '\r\n').encode())
    s.send(('NICK ' + IDENT + '\r\n').encode())
    s.send(('JOIN #' + CHANNEL + '\r\n').encode())
    return s

def joinRoom(s):
    readbuffer = ''
    Loading = True
    while Loading:
        readbuffer = readbuffer + s.recv(1024).decode()
        temp = str.split(readbuffer, '\n')
        readbuffer = temp.pop()
        for line in temp:
            print('> ' + line)
            Loading = continueLoading(line)
    print('Joined room')

def continueLoading(line):
    if 'End of' in line:
        return False
    else:
        return True

class MainBot(object):
    def __init__(self, s, channel):
        self.s = s
        self.t_last_ping = time.time()
        self.s.settimeout(10)
        self.channel = channel

    # start the bot
    def start(self):
        try:
            self.loop()
        except KeyboardInterrupt:
            print('interrupted!')

    # main loop
    def loop(self):
        readbuffer = ''
        while True:
            # send ping every now and then
            if time.time() - self.t_last_ping > 120:
                self.sendPing()
                self.t_last_ping = time.time()

            # read incoing stuff
            try:
                readbuffer = readbuffer + self.s.recv(1024).decode()
            except socket.timeout:
                pass
            temp = str.split(readbuffer, '\n')
            readbuffer = temp.pop()
            for line in temp:
                print('> ' + line)

                # anwser ping from twitch
                if "PING :tmi.twitch.tv" in line:
                    response = line.replace('PING', 'PONG')
                    print('< ' + response)
                    self.s.send(response.encode())

                # get all chat messages
                elif 'PRIVMSG' in line:
                    user = self.getUser(line)
                    message = self.getMessage(line)
                    print('# ' + user + ': ' + message)
                    if message[0] == '!':
                        self.handle_command(message, user)

    # handle command from message
    def handle_command(self, command_msg, user):

        # decompose command message
        command = str(command_msg.split(" ", 1)[0])
        if len(command_msg.split(" ", 1)) > 1:
            args = command_msg.split(" ", 1)[1].strip('\r')
        else:
            args = None
            command = command[:-1]
        print('! {} | args: {} | usr: {}'.format(command[1:], args, user))

        # do the right thing with the command
        if command.startswith('!test'):
            self.sendMessage('beep boop MrDestructoid')
        elif command.startswith('!stronghold'):
            zitat = random.choice(stronhold)
            self.sendMessage(zitat)
        elif command.startswith('!invade'):
            if args.startswith('Prof_Dr_Nereos'):
                self.sendMessage('Hey!')

    # get user from chat message
    def getUser(self, line):
        seperate = line.split(':', 2)
        user = seperate[1].split('!', 1)[0]
        return user

    # get message from chat message
    def getMessage(self, line):
        seperate = line.split(':', 2)
        message = seperate[2]
        return message

    # send message to chat
    def sendMessage(self, message):
        messageTemp = 'PRIVMSG #' + self.channel + ' :' + message
        self.s.send((messageTemp + '\r\n').encode())
        print('< ' + messageTemp)

    # send ping to twitch server
    def sendPing(self):
        msg = 'PING :tmi.twitch.tv'
        print('< ' + msg)
        self.s.send(msg.encode())
