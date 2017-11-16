import numpy as np
import random
from math import exp

class MachineLearner:
    
    """
    58 inputs as tile colours either 0, 1 or 2
    outputs:
        source
        target
    143
    100
    """


    def __init__(self):
        data = np.load("params.npz")
        self.first, self.second, self.third = data["first"], data["second"], data["third"]
        

    def randomise_params(self):
        self.first = np.random.rand(143, 58) - 0.5
        self.second = np.random.rand(100, 143) - 0.5
        self.third = np.random.rand(3, 100) - 0.5
        np.savez("params", first=self.first, second=self.second, third=self.third)

    def get_input(self, board):
        w = []
        for t in board.tiles:
            if not t.blank:
                w.append(t.colour)
        self.v = np.array(w)

    def sigmoid(self, z):
        return 1.0 / (1  + exp(-z) ) 

    def forward_propogate(self, board):
        self.get_input(board)
        a1 = np.dot(self.first, self.v)
        z1 = map(self.sigmoid, a1)
        a2 = np.dot(self.second, z1)
        z2 = map(self.sigmoid, a2)
        a3 = np.dot(self.third, z2)
        z3 = map(self.sigmoid, a3)
        print z3

        
        
