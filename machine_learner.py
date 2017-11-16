import numpy as np
import random

class MachineLearner:
    
    """
    58 inputs as tile colours either 0, 1 or 2
    3 outputs:
        choice of jump or clone
        source
        target
    143
    100
    """


    def __init__(self):
        s = 3
        
    def load_params(self):
        data = np.load("params.npz")
        self.first, self.second, self.third = data["first"], data["second"], data["third"]
        

    def randomise_params(self):
        self.first = np.random.rand(143, 58)
        self.second = np.random.rand(100, 143)
        self.third = np.random.rand(3, 100)
        np.savez("params", first=self.first, second=self.second, third=self.third)

        
        
