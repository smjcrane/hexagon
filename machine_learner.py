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
        self.alpha = 0.0001
        

    def randomise_params(self):
        self.first = np.random.rand(143, 58) - 0.5
        self.second = np.random.rand(500, 143) - 0.5
        self.third = np.random.rand(834, 500) - 0.5
        self.save_params()

    def save_params(self):
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
        self.find_allowed(board, colour)
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

    def find_allowed(self, board, colour):
        mine = []
        self.allowed_clones = []
        self.allowed_jumps = []
        for t in board.tiles:
            if t.colour == colour:
                mine.append(t)
        for t in mine:
            for n in t.neighbours:
                    m = board.tile_lookup[n]
                    if m.colour == 0 and not m.blank:
                        self.allowed_clones.append((t, m))
            for f in t.far_neighbours:
                    m = board.tile_lookup[f]
                    if m.colour == 0 and not m.blank:
                        self.allowed_jumps.append((t, m))

    def make_move(self, board):
        v = get_input(board)
        p = self.forward_propogate(v)
        t = Turn(board, p)
        m = np.min(p)
        p = map( lambda x: x-m, p )
        s = np.sum(p)
        p = map( lambda x: x/s, p)
        #r = random.random()
        #c = 0
        #for i in range(0, len(self.moves)):
        #    if c >= r:
        #        t.put_move(i)
        #        self.history.append(t)
        #        return self.moves[i]
        #    else:
        #        c += p[i]
        #return self.moves[-1]
        max_so_far = 0
        best_so_far = 0
        i=-1
        for (source, target) in self.allowed_clones:
            i = self.moves.index( ( (source.x, source.y), (target.x, target.y), "c") )
            if p[i] > max_so_far:
                best_so_far = i
                max_so_far = p[i]
        for (source, target) in self.allowed_jumps:
            i = self.moves.index( ( (source.x, source.y), (target.x, target.y), "j") )
            if p[i] > max_so_far:
                best_so_far = i
                max_so_far = p[i]
        t.put_move(i)
        self.history.append(t)
        return self.moves[i]
        
    def forward_propogate(self, v):
        #TODO add bias term
        self.a1 = np.dot(self.first, v)
        self.z1 = map(sigmoid, self.a1)
        self.a2 = np.dot(self.second, self.z1)
        self.z2 = map(sigmoid, self.a2)
        self.a3 = np.dot(self.third, self.z2)
        z3 = map(sigmoid, self.a3)
        return z3

    def list_scores(self):
        for t in self.history:
            print t.scores_before

    def regularise(self):
        tot1 = np.sum(self.first**2)
        tot2 = np.sum(self.second**2)
        tot3 = np.sum(self.third**2)
        self.first /= tot1
        self.second /= tot2
        self.third /= tot3

    def back_propogate(self, scores):
        delta1 = np.zeros((143,  58), dtype=np.float)
        delta2 = np.zeros((500, 143), dtype=np.float)
        delta3 = np.zeros((834, 500), dtype=np.float)
        victory = 0
        if scores[1] > scores[0]:
            victory = 1
        for t in self.history:
            z3 = self.forward_propogate(t.before)
            if victory:
                y = np.zeros(834)
                y[t.move] = 1
            else:
                y = np.zeros(834)
                y.fill(1/833)
                y[t.move] = 0
            d3 = self.a3 - y
            d2 = np.dot( (np.transpose(self.third)), d3 ) * map(sig_grad, self.z2)
            d1 = np.dot( np.transpose(self.second), d2 ) * map(sig_grad, self.z1)
            delta3 += np.dot(d3.reshape(-1,1), self.a2.reshape(1,-1))
            delta2 += np.dot(d2.reshape(-1,1), self.a1.reshape(1,-1))
            delta1 += np.dot(d1.reshape(-1,1), t.before.reshape(1,-1))
        delta3 = delta3 / len(self.history)
        delta2 = delta2 / len(self.history)
        delta1 = delta1 / len(self.history)
        self.first += (delta1 * self.alpha)
        self.second += (delta2 * self.alpha)
        self.third += (delta3 * self.alpha)
        self.regularise()
        self.save_params()

    def mimic(self, turn, move):
        delta1 = np.zeros((143, 58), dtype=np.float)
        delta2 = np.zeros((500, 143), dtype=np.float)
        delta3 = np.zeros((834, 500), dtype=np.float)
        z3 = self.forward_propogate(turn.before)
        y = np.zeros(834)
        y[move] = 1
        d3 = self.a3 - y
        d2 = np.dot( (np.transpose(self.third)), d3 ) * map(sig_grad, self.z2)
        d1 = np.dot( np.transpose(self.second), d2 ) * map(sig_grad, self.z1)
        delta3 += np.dot(d3.reshape(-1,1), self.a2.reshape(1,-1))
        delta2 += np.dot(d2.reshape(-1,1), self.a1.reshape(1,-1))
        delta1 += np.dot(d1.reshape(-1,1), turn.before.reshape(1,-1))
        delta3 = delta3 / len(self.history)
        delta2 = delta2 / len(self.history)
        delta1 = delta1 / len(self.history)
        self.first += (delta1 * self.alpha)
        self.second += (delta2 * self.alpha)
        self.third += (delta3 * self.alpha)

            
        

def sigmoid(z):
    return 1.0 / (1  + exp(-z) )

def sig_grad(z):
    return sigmoid(z) * (1 - sigmoid(z) )


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
        self.move = 0

    def put_move(self, move):
        self.move = move
        
        
