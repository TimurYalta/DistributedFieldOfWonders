import Pyro4


@Pyro4.expose
class Player(object):
    def __init__(self):
        self.letters = []
        self.playerURIs = {}
        self.players = {}
        self.daemon = Pyro4.Daemon()
        self.URI = self.daemon.register(Player)
        # TODO self.number

    def register(self):
        # TODO SEND REQUEST TO SERVER TO REGISTER
        pass

    def start_game(self, players, description, letters, answer):
        self.codedLetters = letters
        self.hashedAnswer = answer
        self.playerURIs = players
        self.description = description
        players = {}
        for number, uri in self.playerURIs.items():
            if self.URI == uri:
                continue
            players[number] = Pyro4.Proxy(uri)
        for id in self.players:
            if self.players[id] == self.URI:
                self.ID = self.players[id]
        if self.ID == 1:
            self.performTurn()

    def performTurn(self):
        isWhole = ''
        inp = ''
        while isWhole != 'y' or isWhole != 'n':
            isWhole = input('Would you like to enter the whole word? (y/n) ')
            if isWhole == 'y':
                inp = input('Enter the word: ')
                if inp == '':
                    isWhole = ''
                    print('Wrong input')
                    break
            elif isWhole == 'n':
                inp= input('Enter the letter: ')
                if len(inp) != 1:
                    isWhole = ''
                    print('Wrong input')
                    break
            else:
                print('Only "y" or "n" inputs are allowed')
        self.broadcastTurn(inp)

    def broadcastTurn(self,inp):
        for player in self.players:
            self.players[player].receiveTurn(inp)



    def startFirstTimer(self):
        self.firstTimer =

#     def get_fortune(self, name):
#         return "Hello, {0}. Here is your fortune message:\n" \
#                "Behold the warranty -- the bold print giveth and the fine print taketh away.".format(name)
#
# daemon = Pyro4.Daemon()                # make a Pyro daemon
# #uri = daemon.register(Player)   # register the greeting maker as a Pyro object
#
# print("Ready. Object uri =", uri)      # print the uri so we can use it in the client later
# daemon.requestLoop()
