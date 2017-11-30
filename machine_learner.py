import numpy as np
import random
from math import exp
import boardmaker
import os

class MachineLearner:
    
    """
    58 inputs as tile colours either 0, 1 or 2
    outputs:
        how much it would like to perform each move in the list self.moves
        (this vector is generated deterministically)
        There are 834 outputs
    143
    100
    """


    def __init__(self):
        self.verbose = False
        if os.path.exists("params.npz"):
            print "Loading parameters from file..."
            data = np.load("params.npz")
            self.first, self.second, self.third = data["first"], data["second"], data["third"]
            print "Done"
        else:
            print "No paramaters found. Creating random ones..."
            self.randomise_params()
            print "Done"
        self.moves = []
        board = boardmaker.Board()
        self.vectorize_moves(board)
        self.history = []
        

    def randomise_params(self):
        self.first = np.random.rand(143, 58) - 0.5
        self.second = np.random.rand(500, 143) - 0.5
        self.third = np.random.rand(834, 500) - 0.5
        np.savez("params", first=self.first, second=self.second, third=self.third)


    def vectorize_moves(self, board):
        for t in board.tiles:
            for n in t.neighbours:
                #clone
                self.moves.append( ( (t.x, t.y) , n , "c" ) )
            for nn in t.far_neighbours:
                #jump
                self.moves.append( ( (t.x, t.y) , nn , "j" ) )

    def play(self, board, colour):
        move = self.make_move(board)
        if self.verbose:
            print move
        source = board.tile_lookup[move[0]]
        if source.colour != colour:
            if self.verbose:
                print "Not my tile"
            return
        target = board.tile_lookup[move[1]]
        if move[2] == "c":
            board.clone(source, target)
        elif move[2] == "j":
            board.jump(source, target)

    def make_move(self, board):
        p = self.forward_propogate(board)
        t = Turn(board, p)
        m = np.min(p)
        p = map( lambda x: x-m, p )
        s = np.sum(p)
        p = map( lambda x: x/s, p)
        r = random.random()
        c = 0
        for i in range(0, len(self.moves)):
            if c >= r:
                t.put_move(self.moves[i])
                self.history.append(t)
                return self.moves[i]
            else:
                c += p[i]

    def forward_propogate(self, board):
        #TODO add bias term
        v = get_input(board)
        a1 = np.dot(self.first, v)
        z1 = map(sigmoid, a1)
        a2 = np.dot(self.second, z1)
        z2 = map(sigmoid, a2)
        a3 = np.dot(self.third, z2)
        z3 = map(sigmoid, a3)
        return z3

    def list_scores(self):
        for t in self.history:
            print t.scores_before

    #TODO
    def back_propogate(self, scores):
        victory = 0
        if scores[1] > scores[0]:
            victory = 1

def sigmoid(z):
    return 1.0 / (1  + exp(-z) )


def get_input(board):
    w = []
    for t in board.tiles:
        if not t.blank:
            w.append(t.colour)
    return np.array(w)

    
class Turn:

    def __init__(self, board, predicts):
        self.before = get_input(board)
        self.scores_before = board.get_scores()
        self.predicts = predicts
        self.move = []

    def put_move(self, move):
        self.move = move
        
        
