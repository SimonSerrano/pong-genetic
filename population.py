from player import Player

class Population:
    def __init__(self, size):
        self.players = []
        self.bestPlayer = None
        self.bestScore = 0
        self.globalBestScore = 0
        self.gen = 1
        self.edgeHistory = 0
        self.genPlayers = []
        self.species = []

        self.massExtinctionEvent = False
        self.newStage = False
        
        self.gensSinceNewWorld = 0

        for i in range(size):
            self.players.append(Player())
            self.players[len(self.players) - 1].brain.mutate(self.edgeHistory)
            self.players[len(self.players)-1].brain.generateNetwork()

        

    def getCurrentBest(self):
        for player in self.players :
            if not player.dead :
                return player

        return self.players[0]

    def done(self):
        for player in self.players:
            if not player.dead :
                return False
        return True
    


        
        