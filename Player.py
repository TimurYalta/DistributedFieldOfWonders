import Pyro4
import requests


@Pyro4.expose
class Player(object):
    def __init__(self):
        self.letters = []
        self.codedLetters = []
        self.hashedAnswer = []
        self.description = ''
        self.playerURIs = {}
        self.players = {}
        #self.daemon = Pyro4.Daemon()
        self.URI = None
        self.ID = None
        self.receivedFrom = []
        # TODO self.number

    def register(self):
        r = requests.post('http://127.0.0.1:5000/registerUser', json={"uri": str(self.URI)})
        if r.status_code == 200:
            #self.daemon.requestLoop()
            return


    def start_game(self, players, description, letters, answer):
        print('here')
        self.codedLetters = letters
        self.letters = ['*' for _ in range(len(letters))]
        self.hashedAnswer = answer
        self.players = players
        self.description = description
        players = {}
        for number, uri in self.playerURIs.items():
            if str(self.URI)== str(uri):
                continue
            players[number] = Pyro4.Proxy(str(uri))
        for id in self.players:
            if str(self.players[id]) == str(self.URI):
                self.ID = id
        self.players = players
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
                inp = input('Enter the letter: ')
                if len(inp) != 1:
                    isWhole = ''
                    print('Wrong input')
                    break
            else:
                print('Only "y" or "n" inputs are allowed')
        if isWhole:
            if hash(inp) == self.hashedAnswer:
                self.letters = list(inp)
                self.broadcastVictory()
                return
        else:
            for i, hashedLetter in enumerate(self.codedLetters):
                if hash(inp) == hashedLetter:
                    self.letters[i] = inp
        self.broadcastTurn()

    def broadcastTurn(self):
        stack = []
        for player in self.players:
            self.players[player].receiveTurn(self.ID, self.letters, stack)

    # def rebroadcastTurn(self, stack):
    #     stack.append(self.ID)
    #     for player in self.players:
    #         if player not in stack:
    #             self.players[player].receiveTurn(stack[0], self.letters, stack)

    def receiveTurn(self, id, letters, stack):
        print(self.ID)
        print(stack)
        print()
        stack.append(self.ID)
        self.letters = letters
        for player in self.players:
            if player not in stack and player != self.ID:
                self.players[player].receiveTurn(id, letters, stack)

if __name__ == '__main__':
    player = Player()
    daemon = Pyro4.Daemon()
    uri = daemon.register(player)
    player.URI = uri
    player.register()
    daemon.requestLoop()

    #
    # def startFirstTimer(self):
    #     self.firstTimer =

    # def broadcastVictory(self):

#     def get_fortune(self, name):
#         return "Hello, {0}. Here is your fortune message:\n" \
#                "Behold the warranty -- the bold print giveth and the fine print taketh away.".format(name)
#
# daemon = Pyro4.Daemon()                # make a Pyro daemon
# #uri = daemon.register(Player)   # register the greeting maker as a Pyro object
#
# print("Ready. Object uri =", uri)      # print the uri so we can use it in the client later
# daemon.requestLoop()
